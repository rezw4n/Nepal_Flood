"""Pre-event land cover (ESA WorldCover 2021, 10 m) inside the UNOSAT flow extent, by reach.

Output: tables/landcover_flow_extent.csv (km2 by class and reach) and data/derived/landcover_results.json.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import rasterio
from rasterio.features import rasterize
from pyproj import Transformer
from shapely.ops import transform
from corridor import Channel
from analyse import read_shape_zip, SRC

ROOT = Path(__file__).resolve().parents[1]
DER, TAB = ROOT/'data'/'derived', ROOT/'tables'
WC = ROOT/'sources_ext'/'worldcover'/'worldcover2021_corridor.tif'
CLASSES = {10: 'Tree cover', 20: 'Shrubland', 30: 'Grassland', 40: 'Cropland', 50: 'Built-up', 60: 'Bare or sparse vegetation',
           70: 'Snow and ice', 80: 'Permanent water', 90: 'Herbaceous wetland', 95: 'Mangroves', 100: 'Moss and lichen'}
REACHES = [('0–21 km (source to border)', 0, 21), ('21–41 km (gorge)', 21, 41), ('41–64 km', 41, 64),
           ('64–89 km (middle valley)', 64, 89), ('89–106 km (lower valley)', 89, 106.5)]


def main():
    flood_utm, _, _ = read_shape_zip(SRC/'unosat_3.html')
    to_ll = Transformer.from_crs('EPSG:32645', 'EPSG:4326', always_xy=True).transform
    flood = transform(to_ll, flood_utm)
    with rasterio.open(WC) as s:
        b = flood.bounds
        win = rasterio.windows.from_bounds(*b, transform=s.transform).round_offsets().round_lengths()
        lc = s.read(1, window=win)
        T = s.window_transform(win)
    inside = rasterize([(flood, 1)], out_shape=lc.shape, transform=T, fill=0, dtype='uint8').astype(bool)
    rows, cols = np.nonzero(inside)
    lon = T.c + (cols + 0.5)*T.a; lat = T.f + (rows + 0.5)*T.e
    phi = np.deg2rad(lat)                                    # metres per degree on the WGS 84 ellipsoid
    m_lat = 111132.92 - 559.82*np.cos(2*phi) + 1.175*np.cos(4*phi)
    m_lon = 111412.84*np.cos(phi) - 93.5*np.cos(3*phi)
    area = abs(T.a)*m_lon*abs(T.e)*m_lat/1e6                 # km2 per pixel
    to_utm = Transformer.from_crs('EPSG:4326', 'EPSG:32645', always_xy=True)
    x, y = to_utm.transform(lon, lat)
    ch = Channel()
    _, i = ch.tree.query(np.c_[x, y])
    km = ch.chain[i]/1000
    d = pd.DataFrame(dict(cls=lc[rows, cols], km=km, area=area))
    d['class'] = d.cls.map(CLASSES).fillna('No data')
    d['reach'] = pd.cut(d.km, [r[1] for r in REACHES] + [REACHES[-1][2]], labels=[r[0] for r in REACHES], right=False)
    t = d.pivot_table(index='class', columns='reach', values='area', aggfunc='sum', observed=False).fillna(0)
    t['All reaches'] = t.sum(axis=1)
    t = t.sort_values('All reaches', ascending=False)
    t.loc['Total'] = t.sum()
    t.round(3).reset_index().to_csv(TAB/'landcover_flow_extent.csv', index=False)
    tot = t.loc['Total', 'All reaches']
    res = {k: float(t.loc[k, 'All reaches']) if k in t.index else 0.0 for k in CLASSES.values()}
    res.update(total_km2=float(tot), unosat_area_km2=float(flood_utm.area/1e6),
               cropland_pct=100*res['Cropland']/tot, tree_pct=100*res['Tree cover']/tot, builtup_pct=100*res['Built-up']/tot)
    (DER/'landcover_results.json').write_text(json.dumps(res, indent=1), encoding='utf-8')
    print(t.round(2).to_string())


if __name__ == '__main__':
    main()
