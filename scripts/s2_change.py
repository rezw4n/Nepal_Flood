"""Sentinel-2 L2A pre/post composites and surface-change indices along the whole corridor.

Clear-sky median composites (SCL classes 4, 5, 6, 7 kept) are built at 20 m for a seasonally
matched pre-event window (Oct 2025, after the July 2025 flood) and post-event window
(21 Sep - 18 Oct 2026). Reflectance = DN x scale, plus the raster:bands offset only where Earth Search
has not already removed the processing-baseline offset ('earthsearch:boa_offset_applied'); clipped at
1e-4 before computing indices. Composites are built per MGRS tile and mosaicked by
the larger number of clear observations. Change = post - pre for NDVI, BSI, NDWI and visible
brightness, within 1.5 km of the traced channel (chainage 0-207 km).
Contains modified Copernicus Sentinel data (2025, 2026).
"""
import os
os.environ.setdefault('GDAL_DISABLE_READDIR_ON_OPEN', 'EMPTY_DIR')
os.environ.setdefault('CPL_VSIL_CURL_ALLOWED_EXTENSIONS', '.tif')
os.environ.setdefault('GDAL_HTTP_MULTIRANGE', 'YES')
os.environ.setdefault('GDAL_HTTP_MERGE_CONSECUTIVE_RANGES', 'YES')
os.environ.setdefault('VSI_CACHE', 'TRUE')
from pathlib import Path
import json
import datetime as dt
import numpy as np
import requests
import rasterio
from rasterio.windows import from_bounds
from rasterio.enums import Resampling
from corridor import Channel, DER, ROOT

STAC = 'https://earth-search.aws.element84.com/v1'
OUT = ROOT/'sources_ext'/'s2'
RES = 20.0
BANDS = {'blue': 'B02', 'green': 'B03', 'red': 'B04', 'nir': 'B08', 'swir16': 'B11', 'swir22': 'B12', 'scl': 'SCL'}
CLEAR = (4, 5, 6, 7)
PERIODS = {'pre': '2025-10-01T00:00:00Z/2025-10-31T23:59:59Z', 'post': '2026-09-21T00:00:00Z/2026-10-18T23:59:59Z'}
GRID = (243000.0, 3062000.0, 347000.0, 3138000.0)   # UTM 45N window covering chainage 0-207 km
SEARCH_BBOX = [84.40, 27.68, 85.56, 28.33]
MAX_PER_TILE = {'pre': 5, 'post': 8}                 # clearest scenes per MGRS tile
CHIPS = {'Timure': (85.369, 28.252), 'Syaphrubesi': (85.343, 28.161), 'Betrawati': (85.186, 27.972),
         'Trishuli Bazar': (85.147, 27.920), 'Galchhi': (84.996, 27.805), 'Benighat': (84.830, 27.814)}


def items(period, cap=True):
    body = {'collections': ['sentinel-2-l2a'], 'bbox': SEARCH_BBOX, 'datetime': PERIODS[period],
            'limit': 300, 'query': {'eo:cloud_cover': {'lt': 70}}}
    feats = requests.post(f'{STAC}/search', json=body, timeout=120).json()['features']
    # one processing per tile and acquisition time (e.g. ..._0_L2A and ..._1_L2A): keep the latest
    uniq = {}
    for f in feats:
        tile, k = f['id'].split('_')[1], f['properties']['datetime'][:16]
        if (tile, k) not in uniq or f['id'] > uniq[(tile, k)]['id']:
            uniq[(tile, k)] = f
    feats = list(uniq.values())
    if cap:
        by_tile = {}
        for f in sorted(feats, key=lambda f: f['properties']['eo:cloud_cover']):
            by_tile.setdefault(f['id'].split('_')[1], []).append(f)   # e.g. S2B_45RUM_20251021_0_L2A -> 45RUM
        feats = [f for v in by_tile.values() for f in v[:MAX_PER_TILE[period]]]
    return sorted(feats, key=lambda f: f['properties']['datetime'])


def scale_offset(item, key):
    """Scale and offset to reflectance. Earth Search removes the -1000 DN baseline offset itself for most
    items ('earthsearch:boa_offset_applied': true) while still listing offset -0.1 in raster:bands, so the
    offset is applied only when the flag is false."""
    rb = (item['assets'][key].get('raster:bands') or [{}])[0]
    applied = item['properties'].get('earthsearch:boa_offset_applied', False)
    return rb.get('scale', 1e-4), (0.0 if applied else rb.get('offset', -0.1))


def read_band(href, shape_, resampling):
    """Read the part of a COG overlapping the target grid, resampled to the 20-m grid (0 = no data)."""
    out = np.zeros(shape_, 'uint16')
    with rasterio.open('/vsicurl/' + href) as s:
        if rasterio.coords.disjoint_bounds(s.bounds, GRID):
            return out
        x0 = max(s.bounds.left, GRID[0]); x1 = min(s.bounds.right, GRID[2])
        y0 = max(s.bounds.bottom, GRID[1]); y1 = min(s.bounds.top, GRID[3])
        w = from_bounds(x0, y0, x1, y1, transform=s.transform).round_offsets().round_lengths()
        c0 = int(round((x0 - GRID[0])/RES)); r0 = int(round((GRID[3] - y1)/RES))
        h = int(round((y1 - y0)/RES)); wd = int(round((x1 - x0)/RES))
        out[r0:r0+h, c0:c0+wd] = s.read(1, window=w, out_shape=(h, wd), resampling=resampling)
    return out


def composite(period, corridor_mask, log):
    """Per-tile clear-sky medians, mosaicked by number of clear observations; corridor pixels only in memory."""
    H, W = corridor_mask.shape
    sel = corridor_mask.ravel()
    n_sel = int(sel.sum())
    keys = [k for k in BANDS if k != 'scl']
    best = {k: np.full(n_sel, np.nan, 'float32') for k in keys}
    best_n = np.zeros(n_sel, 'int16')
    used = []
    by_tile = {}
    for f in items(period):
        by_tile.setdefault(f['id'].split('_')[1], []).append(f)
    for tile, feats in by_tile.items():
        stacks = {k: [] for k in keys}
        for f in feats:
            a = f['assets']
            scl = read_band(a['scl']['href'], (H, W), Resampling.nearest).ravel()[sel]
            ok = np.isin(scl, CLEAR)
            if ok.sum() < 0.02*n_sel:
                continue
            used.append(dict(id=f['id'], datetime=f['properties']['datetime'], clear_frac=float(ok.mean()),
                             cloud_cover=f['properties']['eo:cloud_cover']))
            for k in keys:
                dn = read_band(a[k]['href'], (H, W), Resampling.average).ravel()[sel]
                dn = np.where(ok & (dn > 0), dn, 0).astype('uint16')
                stacks[k].append(dn)
            print(period, f['id'], round(used[-1]['clear_frac'], 3), flush=True)
        if not stacks['red']:
            continue
        sc, of = scale_offset(feats[0], 'red')
        if any(scale_offset(f_, 'red') != (sc, of) for f_ in feats):
            raise ValueError(f'mixed reflectance scaling within tile {tile}')
        n = np.sum(np.stack(stacks['red']) > 0, axis=0).astype('int16')
        take = n > best_n
        for k in keys:
            arr = np.stack(stacks[k]).astype('float32')
            arr[arr == 0] = np.nan
            with np.errstate(all='ignore'):
                med = np.nanmedian(arr, axis=0)*sc + of
            best[k][take] = np.clip(med[take], 1e-4, None)
        best_n[take] = n[take]
        del stacks
    log[period] = used
    comp = {}
    for k in keys:
        full = np.full(H*W, np.nan, 'float32'); full[sel] = best[k]; comp[k] = full.reshape(H, W)
    full = np.zeros(H*W, 'float32'); full[sel] = best_n; comp['n_obs'] = full.reshape(H, W)
    return comp


def indices(c):
    with np.errstate(all='ignore'):
        ndvi = (c['nir'] - c['red'])/(c['nir'] + c['red'])
        bsi = ((c['swir16'] + c['red']) - (c['nir'] + c['blue']))/((c['swir16'] + c['red']) + (c['nir'] + c['blue']))
        bright = (c['blue'] + c['green'] + c['red'])/3
        ndwi = (c['green'] - c['nir'])/(c['green'] + c['nir'])
    return dict(ndvi=ndvi, bsi=bsi, bright=bright, ndwi=ndwi)


def chips(log):
    """10-m true-colour chips (3.2 km squares) from the clearest single scene per period covering each site."""
    from pyproj import Transformer
    t = Transformer.from_crs('EPSG:4326', 'EPSG:32645', always_xy=True)
    meta = {}
    for period in PERIODS:
        feats = {f['id']: f for f in items(period, cap=False)}
        for name, (lo, la) in CHIPS.items():
            x, y = t.transform(lo, la)
            bb = (x - 1600, y - 1600, x + 1600, y + 1600)
            best = None
            for u in sorted(log[period], key=lambda r: -r['clear_frac']):
                f = feats.get(u['id'])
                if f is None:
                    continue
                with rasterio.open('/vsicurl/' + f['assets']['scl']['href']) as s:
                    if rasterio.coords.disjoint_bounds(s.bounds, bb):
                        continue
                    w = from_bounds(*bb, transform=s.transform)
                    scl = s.read(1, window=w, out_shape=(160, 160), boundless=True, fill_value=0)
                clear = np.isin(scl, CLEAR).mean()
                if best is None or clear > best[1]:
                    best = (f, clear)
                if clear > 0.97:
                    break
            if best is None:
                continue
            f, clear = best
            rgb = []
            for k in ('red', 'green', 'blue'):
                sc, of = scale_offset(f, k)
                with rasterio.open('/vsicurl/' + f['assets'][k]['href']) as s:
                    w = from_bounds(*bb, transform=s.transform)
                    rgb.append(s.read(1, window=w, out_shape=(320, 320), boundless=True, fill_value=0)*sc + of)
            np.save(OUT/f'chip_{period}_{name.replace(" ", "_")}.npy', np.clip(np.stack(rgb), 0, None).astype('float32'))
            meta[f'{period}_{name}'] = dict(id=f['id'], datetime=f['properties']['datetime'], clear=float(clear), bounds=bb)
    (OUT/'chips.json').write_text(json.dumps(meta, indent=1), encoding='utf-8')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    H = int((GRID[3]-GRID[1])/RES); W = int((GRID[2]-GRID[0])/RES)
    T = rasterio.transform.from_origin(GRID[0], GRID[3], RES, RES)
    ch = Channel()
    xs = GRID[0] + (np.arange(W) + .5)*RES; ys = GRID[3] - (np.arange(H) + .5)*RES
    gx, gy = np.meshgrid(xs, ys)
    d, i = ch.tree.query(np.c_[gx.ravel(), gy.ravel()])
    corridor = ((d <= 1500) & (ch.chain[i] <= 207000)).reshape(H, W)
    del gx, gy, d, i
    log = {'retrieved_utc': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'), 'stac': STAC,
           'grid_utm45n': GRID, 'resolution_m': RES}
    comp = {p: composite(p, corridor, log) for p in PERIODS}
    idx = {p: indices(comp[p]) for p in PERIODS}
    meta = dict(driver='GTiff', height=H, width=W, count=1, crs='EPSG:32645', transform=T, dtype='float32',
                nodata=np.nan, compress='deflate', predictor=3, tiled=True)
    for p in PERIODS:
        for k, v in list(idx[p].items()) + [('n_obs', comp[p]['n_obs'])]:
            with rasterio.open(OUT/f's2_{p}_{k}.tif', 'w', **meta) as f:
                f.write(np.where(corridor, v, np.nan).astype('float32'), 1)
    for k in ('ndvi', 'bsi', 'bright', 'ndwi'):
        with rasterio.open(OUT/f's2_delta_{k}.tif', 'w', **meta) as f:
            f.write(np.where(corridor, idx['post'][k] - idx['pre'][k], np.nan).astype('float32'), 1)
    (OUT/'s2_log.json').write_text(json.dumps(log, indent=1), encoding='utf-8')
    chips(log)
    print('done', {p: len(log[p]) for p in PERIODS})


if __name__ == '__main__':
    main()
