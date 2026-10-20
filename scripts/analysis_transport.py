"""Road and bridge damage graded by CEMS EMSR927 (latest product per area of interest).

Lengths are measured in UTM 45N. AOI01 and AOI02 use the first grading product; AOI03 and AOI05 use the
monitoring product (MONIT01), which supersedes it. Output: tables/infrastructure_cems_transport.csv.
"""
from pathlib import Path
import json
import pandas as pd
from pyproj import Transformer
from shapely.geometry import shape
from shapely.ops import transform

ROOT = Path(__file__).resolve().parents[1]
CEMS = ROOT/'sources_ext'/'cems'
LATEST = {'AOI01': 'GRA_PRODUCT', 'AOI02': 'GRA_PRODUCT', 'AOI03': 'GRA_MONIT01', 'AOI05': 'GRA_MONIT01'}
GRADES = ['Destroyed', 'Damaged', 'Possibly damaged', 'No visible damage']
PROJ = Transformer.from_crs(4326, 32645, always_xy=True).transform


def layer(aoi, product, kind):
    files = sorted(CEMS.glob(f'EMSR927_{aoi}_{product}_{kind}_v*.json'))
    if not files:
        return []
    return json.loads(files[-1].read_text(encoding='utf-8'))['features']


def main():
    rows = []
    for aoi, product in LATEST.items():
        for f in layer(aoi, product, 'transportationL'):
            p = f['properties']
            g = f['geometry']                       # a few records carry no geometry: counted, no length
            rows.append(dict(aoi=aoi, product=product, layer='roads', cls=p.get('simplified'), grade=p.get('damage_gra'),
                             km=transform(PROJ, shape(g)).length/1000 if g else 0.0, n=1, no_geom=g is None))
        for f in layer(aoi, product, 'transportationP'):
            p = f['properties']
            rows.append(dict(aoi=aoi, product=product, layer='bridges' if 'Bridge' in (p.get('simplified') or '') else 'other points',
                             cls=p.get('simplified'), grade=p.get('damage_gra'), km=0.0, n=1, no_geom=f['geometry'] is None))
    d = pd.DataFrame(rows)
    out = []
    for (lay, aoi), g in d.groupby(['layer', 'aoi']):
        r = dict(layer=lay, aoi=aoi, product=g['product'].iat[0])
        for gr in GRADES:
            r[gr] = round(g.loc[g.grade == gr, 'km'].sum(), 2) if lay == 'roads' else int((g.grade == gr).sum())
        r['records'] = len(g); r['records_without_geometry'] = int(g.no_geom.sum())
        out.append(r)
    t = pd.DataFrame(out)
    tot = t.groupby('layer')[GRADES + ['records', 'records_without_geometry']].sum().reset_index().assign(aoi='All', product='latest')
    t = pd.concat([t, tot], ignore_index=True)
    t.to_csv(ROOT/'tables'/'infrastructure_cems_transport.csv', index=False)
    print(t.to_string(index=False))


if __name__ == '__main__':
    main()
