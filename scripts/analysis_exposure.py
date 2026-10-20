"""Exposure growth (GHSL 1975-2020, WorldPop 2015-2026) and infrastructure in hazard zones.

Zones are defined on the 30-m UTM grid of the DEM:
  flow_extent        UNOSAT satellite-detected flow extent (observed, chainage 0-106 km)
  rem<h, d<=1 km     valley floor below h metres above the traced channel, within 1 km of it
GHSL built-up surface and WorldPop counts are areally interpolated to the 30-m grid
assuming uniform density inside each source cell (nearest-neighbour + area scaling).
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import rasterio
from rasterio.features import rasterize
from rasterio.warp import reproject, Resampling
from scipy.ndimage import distance_transform_edt
import shapely
from shapely.geometry import shape, LineString
from shapely.ops import transform
from pyproj import Transformer
from corridor import Channel, DER, ROOT
from analyse import read_shape_zip, SRC

TAB = ROOT/'tables'
EXT = ROOT/'sources_ext'
EPOCHS = list(range(1975, 2021, 5))
POP_YEARS = [2015, 2020, 2026]
PROJ = Transformer.from_crs('OGC:CRS84', 'EPSG:32645', always_xy=True).transform


def grid():
    with rasterio.open(DER/'dem_utm30.tif') as s:
        return s.profile.copy(), s.transform, s.shape


def channel_rasters(ch, T, shape_):
    """Distance to channel (m) and chainage (km) of the nearest channel cell for every grid cell."""
    rows, cols = rasterio.transform.rowcol(T, ch.xy[:, 0], ch.xy[:, 1])
    mask = np.ones(shape_, bool)
    mask[rows, cols] = False
    chain = np.full(shape_, np.nan, 'float32')
    chain[rows, cols] = ch.chain/1000
    dist, (ir, ic) = distance_transform_edt(mask, sampling=30.0, return_indices=True)
    return dist.astype('float32'), chain[ir, ic]


def to_grid(path, T, shape_, kind):
    """Reproject a source raster to the 30-m grid preserving totals (uniform density within cells)."""
    with rasterio.open(path) as s:
        a = s.read(1).astype('float64')
        nd = s.nodata
        if nd is not None:
            a[a == nd] = 0
        a[~np.isfinite(a)] = 0
        if kind == 'ghsl':                 # m2 built-up per 100x100 m cell -> density
            dens = a/(abs(s.transform.a)*abs(s.transform.e))
        else:                               # WorldPop counts per geographic cell -> density per m2
            lat = s.transform.f + (np.arange(s.height) + .5)*s.transform.e
            cell = (abs(s.transform.a)*111320*np.cos(np.radians(lat)))*(abs(s.transform.e)*110574)
            dens = a/cell[:, None]
        out = np.zeros(shape_, 'float64')
        reproject(dens, out, src_transform=s.transform, src_crs=s.crs, dst_transform=T, dst_crs='EPSG:32645',
                  resampling=Resampling.nearest)
    return out*900.0


def municipality_raster(T, shape_):
    feats = json.loads((SRC/'boundaries_adm3.json').read_text(encoding='utf-8'))['features']
    names, shapes = [], []
    for i, f in enumerate(feats, start=1):
        names.append(f['properties']['shapeName'])
        shapes.append((transform(PROJ, shape(f['geometry'])), i))
    r = rasterize(shapes, out_shape=shape_, transform=T, fill=0, dtype='int32')
    return r, {i: n for i, n in enumerate(names, start=1)}


def main():
    prof, T, shp = grid()
    ch = Channel()
    with rasterio.open(DER/'rem_utm30.tif') as s:
        rem = s.read(1)
    dist, chain = channel_rasters(ch, T, shp)
    flood, _, _ = read_shape_zip(SRC/'unosat_3.html')
    flow = rasterize([(flood, 1)], out_shape=shp, transform=T, fill=0, dtype='uint8').astype(bool)
    muni, names = municipality_raster(T, shp)
    near = dist <= 1000
    zones = {
        'flow_extent': flow,
        'rem_lt10_d1km': near & (rem < 10),
        'rem_10_20_d1km': near & (rem >= 10) & (rem < 20),
        'rem_20_40_d1km': near & (rem >= 20) & (rem < 40),
        'rem_40_80_d1km': near & (rem >= 40) & (rem < 80),
        'rem_ge80_d1km': near & (rem >= 80),
        'corridor_d1km': near,
        'corridor_d2km': dist <= 2000,
    }
    reaches = {'0-106km (assessed)': (chain >= 0) & (chain < 106), '106-207km (downstream)': (chain >= 106) & (chain <= 207)}
    ghsl = {y: to_grid(EXT/'ghsl'/f'ghs_built_s_{y}_corridor.tif', T, shp, 'ghsl') for y in EPOCHS}
    pop = {y: to_grid(EXT/'worldpop'/f'worldpop_{y}_corridor.tif', T, shp, 'pop') for y in POP_YEARS}
    rows = []
    for zn, z in zones.items():
        for rn, r in reaches.items():
            m = z & r
            row = dict(zone=zn, reach=rn, area_km2=m.sum()*900/1e6)
            row.update({f'built_m2_{y}': float(ghsl[y][m].sum()) for y in EPOCHS})
            row.update({f'pop_{y}': float(pop[y][m].sum()) for y in POP_YEARS})
            rows.append(row)
    zt = pd.DataFrame(rows)
    zt['built_growth_1975_2020'] = zt.built_m2_2020/zt.built_m2_1975.replace(0, np.nan)
    zt['built_growth_2000_2020'] = zt.built_m2_2020/zt.built_m2_2000.replace(0, np.nan)
    zt['pop_growth_2015_2026'] = zt.pop_2026/zt.pop_2015.replace(0, np.nan)
    zt.to_csv(TAB/'exposure_growth_zones.csv', index=False, float_format='%.6g')
    # Built-up within each REM band by chainage (5-km bins) for 1975 and 2020 -> where growth concentrated
    bins = np.arange(0, 210, 5)
    cb = np.digitize(chain, bins) - 1
    prof_rows = []
    for k in range(len(bins) - 1):
        r = (cb == k) & near
        row = dict(chainage_start_km=int(bins[k]))
        for y in (1975, 2000, 2020):
            row[f'built_lt20_{y}'] = float(ghsl[y][r & (rem < 20)].sum())
            row[f'built_all_{y}'] = float(ghsl[y][r].sum())
        row['pop_lt20_2026'] = float(pop[2026][r & (rem < 20)].sum())
        row['pop_flow_2026'] = float(pop[2026][r & flow].sum())
        prof_rows.append(row)
    pd.DataFrame(prof_rows).to_csv(TAB/'exposure_profile_5km.csv', index=False, float_format='%.6g')
    # Municipality exposure (assessed + downstream) within flow extent and REM<20 m
    mrows = []
    for mid in np.unique(muni[near & (muni > 0)]):
        mm = (muni == mid)
        if (mm & near).sum() < 50:
            continue
        row = dict(municipality=names[mid])
        for zn in ('flow_extent', 'rem_lt10_d1km', 'rem_10_20_d1km'):
            z = zones[zn] & mm
            row[f'{zn}_area_km2'] = z.sum()*900/1e6
            row[f'{zn}_pop2026'] = float(pop[2026][z].sum())
            row[f'{zn}_built2020_m2'] = float(ghsl[2020][z].sum())
            row[f'{zn}_built1975_m2'] = float(ghsl[1975][z].sum())
        row['chainage_median_km'] = float(np.nanmedian(chain[mm & near]))
        mrows.append(row)
    mt = pd.DataFrame(mrows).sort_values('chainage_median_km')
    mt.to_csv(TAB/'exposure_by_municipality_v2.csv', index=False, float_format='%.6g')
    # Infrastructure: roads, bridges, power assets in the flow extent and REM<20 m zone
    seg = pd.read_parquet(EXT/'overture'/'segments.parquet')
    sg = shapely.transform(shapely.from_wkb(seg.wkb.to_numpy()),
                           lambda c: np.c_[Transformer.from_crs('EPSG:4326', 'EPSG:32645', always_xy=True).transform(c[:, 0], c[:, 1])])
    shapely.prepare(flood)
    hit = shapely.intersects(sg, flood)
    inter = shapely.length(shapely.intersection(sg[hit], flood))
    roads = seg.loc[hit, ['class']].assign(km_in_extent=inter/1000)
    is_bridge = seg.road_flags.astype(str).str.contains('is_bridge')
    rsum = roads.groupby('class').km_in_extent.sum().sort_values(ascending=False).reset_index()
    rsum.to_csv(TAB/'infrastructure_roads_in_extent.csv', index=False, float_format='%.4g')
    inf = pd.read_parquet(EXT/'overture'/'infrastructure.parquet')
    ig = shapely.transform(shapely.from_wkb(inf.wkb.to_numpy()),
                           lambda c: np.c_[Transformer.from_crs('EPSG:4326', 'EPSG:32645', always_xy=True).transform(c[:, 0], c[:, 1])])
    inf['in_extent'] = shapely.intersects(ig, flood)
    pts = shapely.point_on_surface(ig)
    px, py = shapely.get_coordinates(pts).T
    ix = np.clip(rasterio.transform.rowcol(T, px, py)[0], 0, shp[0]-1)
    iy = np.clip(rasterio.transform.rowcol(T, px, py)[1], 0, shp[1]-1)
    inf['rem_m'] = rem[ix, iy]; inf['dist_channel_m'] = dist[ix, iy]; inf['chainage_km'] = chain[ix, iy]
    inf['low_valley'] = (inf.rem_m < 20) & (inf.dist_channel_m <= 500)
    sel = inf[inf['class'].isin(['bridge', 'plant', 'generator', 'substation', 'dam', 'weir', 'power_tower'])]
    isum = sel.groupby('class').agg(total_in_window=('id', 'size'), in_flow_extent=('in_extent', 'sum'),
                                    within_500m_rem_lt20=('low_valley', 'sum')).reset_index()
    isum.to_csv(TAB/'infrastructure_assets_in_extent.csv', index=False)
    power = inf[inf['class'].isin(['plant', 'generator', 'substation', 'dam', 'weir']) & (inf.dist_channel_m <= 1500)
                & (inf.chainage_km <= 207)].drop(columns=['wkb'])
    power.to_csv(TAB/'infrastructure_power_near_channel.csv', index=False, float_format='%.6g')
    res = dict(roads_km_in_extent=float(roads.km_in_extent.sum()),
               roads_km_in_extent_major=float(roads[roads['class'].isin(['trunk', 'primary', 'secondary', 'tertiary'])].km_in_extent.sum()),
               bridge_segments_in_extent=int((hit & is_bridge.to_numpy()).sum()),
               bridge_features_in_extent=int(inf[(inf['class'] == 'bridge') & inf.in_extent].shape[0]))
    (DER/'exposure_results.json').write_text(json.dumps(res, indent=1), encoding='utf-8')
    print(zt[['zone', 'reach', 'area_km2', 'built_m2_1975', 'built_m2_2000', 'built_m2_2020', 'built_growth_1975_2020',
              'pop_2015', 'pop_2026', 'pop_growth_2015_2026']].round(2).to_string())
    print(mt.round(2).to_string())
    print(rsum.round(2).to_string()); print(isum.to_string()); print(res)


if __name__ == '__main__':
    main()
