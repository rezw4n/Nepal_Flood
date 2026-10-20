"""Terrain products for the corridor from Copernicus GLO-30 (pre-event DSM).

Outputs (data/derived/):
  dem_utm30.tif        DEM mosaic reprojected to EPSG:32645, 30 m
  hillshade_utm30.tif  multidirectional hillshade (uint8) for basemaps
  flowacc_utm30.tif    D8 flow accumulation (cells) on the conditioned DEM
  rem_utm30.tif        relative elevation above the traced cascade channel (m)
  flowpath.geojson     D8 path traced downstream from the HiRISK source point
  flowpath_profile.csv chainage, raw and smoothed channel elevation, slope
"""
from pathlib import Path
import heapq
import json
from numba import njit
import numpy as np
import pandas as pd
import rasterio
from rasterio.merge import merge
from rasterio.warp import reproject, Resampling
from pyproj import Transformer
from scipy.spatial import cKDTree
from scipy.ndimage import uniform_filter1d

ROOT = Path(__file__).resolve().parents[1]
DEM_DIR = ROOT/'sources_ext'/'dem'
OUT = ROOT/'data'/'derived'
DST_CRS = 'EPSG:32645'
RES = 30.0
# Lon/lat window: source area to the Trishuli-Kali Gandaki confluence at Devghat.
BBOX = (84.30, 27.60, 85.70, 28.50)
# HiRISK RHA NP3: detachment location (28.288708 N, 85.528159 E).
SOURCE_LONLAT = (85.528159, 28.288708)
# Trace stops at Devghat confluence (Trishuli joins Kali Gandaki).
DEVGHAT_LONLAT = (84.433, 27.710)
DIRMAP = (64, 128, 1, 2, 4, 8, 16, 32)  # ESRI D8 codes for N, NE, E, SE, S, SW, W, NW
STEP = {64: (-1, 0), 128: (-1, 1), 1: (0, 1), 2: (1, 1), 4: (1, 0), 8: (1, -1), 16: (0, -1), 32: (-1, -1)}


def mosaic_and_project():
    tiles = sorted(DEM_DIR.glob('Copernicus_DSM_COG_10_*_DEM.tif'))
    assert len(tiles) == 4, tiles
    srcs = [rasterio.open(t) for t in tiles]
    mosaic, transform = merge(srcs, bounds=BBOX, nodata=-32767.0)  # tiles declare no nodata; avoid 0-padding
    profile = srcs[0].profile
    for s in srcs:
        s.close()
    # Explicit, reproducible target grid snapped to 30 m.
    to_utm = Transformer.from_crs('EPSG:4326', DST_CRS, always_xy=True)
    xs, ys = to_utm.transform([BBOX[0], BBOX[2], BBOX[0], BBOX[2]], [BBOX[1], BBOX[1], BBOX[3], BBOX[3]])
    x0, x1 = np.floor(max(min(xs), 0) / RES) * RES, np.ceil(max(xs) / RES) * RES
    y0, y1 = np.floor(min(ys) / RES) * RES, np.ceil(max(ys) / RES) * RES
    width, height = int((x1 - x0) / RES), int((y1 - y0) / RES)
    dst_transform = rasterio.transform.from_origin(x0, y1, RES, RES)
    dst = np.full((height, width), -32767.0, dtype='float32')
    reproject(mosaic[0].astype('float32'), dst, src_transform=transform, src_crs=profile['crs'],
              dst_transform=dst_transform, dst_crs=DST_CRS, resampling=Resampling.bilinear,
              src_nodata=-32767.0, dst_nodata=-32767.0)
    meta = dict(driver='GTiff', dtype='float32', count=1, crs=DST_CRS, transform=dst_transform,
                width=width, height=height, nodata=-32767.0, compress='deflate', predictor=3, tiled=True)
    with rasterio.open(OUT/'dem_utm30.tif', 'w', **meta) as f:
        f.write(dst, 1)
    return dst, dst_transform, meta


def hillshade(z, az_list=(225, 270, 315, 360), alt=40, zf=1.5):
    """Multidirectional hillshade (weighted mean of four azimuths), returned as 0-255."""
    gy, gx = np.gradient(z * zf, RES)
    slope = np.arctan(np.hypot(gx, gy))
    aspect = np.arctan2(-gx, gy)
    out = np.zeros_like(z, dtype='float64')
    for az in az_list:
        a = np.deg2rad(360 - az + 90)
        out += np.sin(np.deg2rad(alt)) * np.cos(slope) + np.cos(np.deg2rad(alt)) * np.sin(slope) * np.cos(a - aspect)
    out /= len(az_list)
    return np.clip(np.nan_to_num(out * 255, nan=0.0), 0, 255).astype('uint8')


DR = np.array([-1, -1, 0, 1, 1, 1, 0, -1])
DC = np.array([0, 1, 1, 1, 0, -1, -1, -1])
CODES = np.array(DIRMAP)


@njit(cache=True)
def _priority_flood_eps(z, valid):
    """Priority-Flood+epsilon (Barnes et al., 2014): every valid cell drains to the grid edge."""
    H, W = z.shape
    out = z.copy()
    closed = ~valid
    heap = [(0.0, np.int64(0))]
    heap.pop()
    for r in range(H):
        for c in range(W):
            if not valid[r, c]:
                continue
            edge = r == 0 or c == 0 or r == H - 1 or c == W - 1
            if not edge:
                for k in range(8):
                    if not valid[r + DR[k], c + DC[k]]:
                        edge = True
                        break
            if edge:
                heapq.heappush(heap, (out[r, c], np.int64(r * W + c)))
                closed[r, c] = True
    while len(heap) > 0:
        e, idx = heapq.heappop(heap)
        r = idx // W
        c = idx % W
        for k in range(8):
            rr = r + DR[k]
            cc = c + DC[k]
            if rr < 0 or cc < 0 or rr >= H or cc >= W or closed[rr, cc]:
                continue
            closed[rr, cc] = True
            if out[rr, cc] <= e:
                out[rr, cc] = np.nextafter(e, np.inf)
            heapq.heappush(heap, (out[rr, cc], np.int64(rr * W + cc)))
    return out


@njit(cache=True)
def _d8(zf, valid, res):
    H, W = zf.shape
    fdir = np.zeros((H, W), np.int16)
    for r in range(H):
        for c in range(W):
            if not valid[r, c]:
                continue
            best, bk = 0.0, -1
            for k in range(8):
                rr = r + DR[k]
                cc = c + DC[k]
                if rr < 0 or cc < 0 or rr >= H or cc >= W or not valid[rr, cc]:
                    continue
                dist = res * (1.4142135623730951 if DR[k] != 0 and DC[k] != 0 else 1.0)
                s = (zf[r, c] - zf[rr, cc]) / dist
                if s > best:
                    best, bk = s, k
            if bk >= 0:
                fdir[r, c] = CODES[bk]
    return fdir


@njit(cache=True)
def _accumulate(fdir, order):
    H, W = fdir.shape
    acc = np.ones((H, W), np.float64)
    for i in range(order.size):
        idx = order[i]
        r = idx // W
        c = idx % W
        d = fdir[r, c]
        for k in range(8):
            if CODES[k] == d:
                rr = r + DR[k]
                cc = c + DC[k]
                if 0 <= rr < H and 0 <= cc < W:
                    acc[rr, cc] += acc[r, c]
                break
    return acc


def flow_routing(z, valid):
    zf = _priority_flood_eps(np.where(valid, z, -1e9).astype('float64'), valid)
    fdir = _d8(zf, valid, RES)
    order = np.argsort(-np.where(valid, zf, -np.inf), axis=None, kind='stable')
    order = order[valid.ravel()[order]]
    acc = _accumulate(fdir, order.astype(np.int64))
    acc[~valid] = -1
    return fdir, acc


def trace(fdir, transform, start_xy, stop_xy, stop_radius=600.0):
    inv = ~transform
    col, row = inv * start_xy
    r, c = int(row), int(col)
    path = []
    seen = set()
    while 0 <= r < fdir.shape[0] and 0 <= c < fdir.shape[1] and (r, c) not in seen:
        seen.add((r, c))
        x, y = transform * (c + .5, r + .5)
        path.append((r, c, x, y))
        if np.hypot(x - stop_xy[0], y - stop_xy[1]) < stop_radius:
            break
        d = int(fdir[r, c])
        if d not in STEP:
            break
        dr, dc = STEP[d]
        r, c = r + dr, c + dc
    return path


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    z, transform, meta = mosaic_and_project()
    valid = z > -1000
    print('DEM grid', z.shape, 'valid fraction', valid.mean(), 'range', z[valid].min(), z[valid].max())
    hs = hillshade(np.where(valid, z, np.nan))
    m8 = dict(meta, dtype='uint8', nodata=0, predictor=2)
    with rasterio.open(OUT/'hillshade_utm30.tif', 'w', **m8) as f:
        f.write(hs, 1)
    gy, gx = np.gradient(np.where(valid, z, np.nan).astype('float64'), RES)
    slope_deg = np.degrees(np.arctan(np.hypot(gx, gy))).astype('float32')
    with rasterio.open(OUT/'slope_utm30.tif', 'w', **dict(meta, nodata=np.nan)) as f:
        f.write(slope_deg, 1)
    fdir, acc = flow_routing(z, valid)
    with rasterio.open(OUT/'flowacc_utm30.tif', 'w', **dict(meta, dtype='float32', nodata=-1, predictor=3)) as f:
        f.write(acc.astype('float32'), 1)
    to_utm = Transformer.from_crs('EPSG:4326', DST_CRS, always_xy=True)
    path = trace(fdir, transform, to_utm.transform(*SOURCE_LONLAT), to_utm.transform(*DEVGHAT_LONLAT))
    rows = np.array([p[0] for p in path]); cols = np.array([p[1] for p in path])
    xy = np.array([(p[2], p[3]) for p in path])
    seg = np.hypot(np.diff(xy[:, 0]), np.diff(xy[:, 1]))
    chain = np.concatenate([[0], np.cumsum(seg)])
    zr = z[rows, cols].astype('float64')
    # Enforce downstream non-increase (removes DSM artefacts such as bridges/vegetation), then smooth.
    zc = np.minimum.accumulate(zr)
    zs = uniform_filter1d(zc, size=11, mode='nearest')
    zs = np.minimum.accumulate(zs)
    slope = -np.gradient(uniform_filter1d(zs, size=67, mode='nearest'), chain)  # ~2 km window
    lonlat = Transformer.from_crs(DST_CRS, 'EPSG:4326', always_xy=True).transform(xy[:, 0], xy[:, 1])
    prof = pd.DataFrame(dict(chainage_m=chain, x=xy[:, 0], y=xy[:, 1], lon=lonlat[0], lat=lonlat[1],
                             z_raw=zr, z_channel=zs, slope=slope, acc_cells=acc[rows, cols]))
    prof.to_csv(OUT/'flowpath_profile.csv', index=False, float_format='%.6g')
    gj = dict(type='FeatureCollection', features=[dict(type='Feature', properties=dict(
        name='D8 flow path from HiRISK source point', length_km=float(chain[-1] / 1000), crs='EPSG:4326'),
        geometry=dict(type='LineString', coordinates=[[float(a), float(b)] for a, b in zip(*lonlat)]))])
    (OUT/'flowpath.geojson').write_text(json.dumps(gj), encoding='utf-8')
    print('flow path length km', chain[-1] / 1000, 'cells', len(path), 'end lonlat', lonlat[0][-1], lonlat[1][-1])
    # Relative elevation model: DEM minus IDW-interpolated channel elevation (k nearest channel nodes).
    tree = cKDTree(xy)
    H, W = z.shape
    rem = np.full(z.shape, np.nan, dtype='float32')
    xs = transform.c + (np.arange(W) + .5) * transform.a
    for r0 in range(0, H, 256):
        r1 = min(H, r0 + 256)
        ys = transform.f + (np.arange(r0, r1) + .5) * transform.e
        gx, gy = np.meshgrid(xs, ys)
        d, i = tree.query(np.c_[gx.ravel(), gy.ravel()], k=16, distance_upper_bound=6000)
        ok = np.isfinite(d[:, 0])
        dd = np.where(np.isfinite(d), d, np.inf)
        ii = np.where(np.isfinite(d), i, 0)
        wts = 1.0 / np.maximum(dd, 1.0) ** 2
        with np.errstate(invalid='ignore', divide='ignore'):  # cells beyond 6 km have no channel neighbours
            zint = (wts * zs[ii]).sum(1) / wts.sum(1)
        block = z[r0:r1].ravel().astype('float64') - zint
        block[~ok] = np.nan
        rem[r0:r1] = block.reshape(r1 - r0, W)
    rem[~valid] = np.nan
    with rasterio.open(OUT/'rem_utm30.tif', 'w', **dict(meta, nodata=np.nan)) as f:
        f.write(rem, 1)
    print('REM done; finite fraction', np.isfinite(rem).mean())


if __name__ == '__main__':
    main()
