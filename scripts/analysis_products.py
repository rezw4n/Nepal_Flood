"""Harmonised multi-product damage inventory and inter-product agreement.

Products: HOT local inventory (1,053 footprints), CEMS EMSR927 latest grading (4,685 points),
UNDP RAPIDA footprints (2,359 CEMS/SERTIT-attributed + 684 UNOSAT-attributed).
Matching (one-to-one) is done in build_buildings.py; here we count, compare and attribute.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import shapely
from shapely.geometry import shape
from shapely.ops import transform
from pyproj import Transformer
from sklearn.metrics import cohen_kappa_score
from corridor import DER, ROOT
from analyse import SRC

TAB = ROOT/'tables'
PROJ = Transformer.from_crs('OGC:CRS84', 'EPSG:32645', always_xy=True).transform
GRADE = {0: 'No record / no damage', 1: 'Possibly damaged / minor', 2: 'Damaged / major', 3: 'Destroyed'}


def municipalities():
    feats = json.loads((SRC/'boundaries_adm3.json').read_text(encoding='utf-8'))['features']
    names = [f['properties']['shapeName'] for f in feats]
    geoms = [transform(PROJ, shape(f['geometry'])) for f in feats]
    return names, geoms


def assign(names, geoms, x, y):
    out = np.array(['Unassigned']*len(x), dtype=object)
    pts = shapely.points(np.asarray(x), np.asarray(y))
    tree = shapely.STRtree(np.array(geoms, dtype=object))
    pi, gi = tree.query(pts, predicate='within')
    out[pi] = np.array(names, dtype=object)[gi]
    return out


def main():
    st = pd.read_parquet(DER/'corridor_buildings.parquet').drop(columns=['wkb_utm'])
    names, geoms = municipalities()
    st['municipality'] = assign(names, geoms, st.x, st.y)
    hot_level = st.hot_class.where(st.hot_class >= 0, 0)
    st['max_level'] = np.maximum.reduce([st.reg_level.to_numpy(), st.cems_level.to_numpy(), hot_level.to_numpy()])
    st['n_products_destroyed'] = ((st.reg_level == 3).astype(int) + (st.cems_level == 3).astype(int) + (st.hot_class == 3).astype(int))
    st['any_damage'] = st.max_level >= 1
    st['destroyed'] = st.max_level == 3
    st[['id', 'origin', 'municipality', 'x', 'y', 'lon', 'lat', 'chainage_km', 'rem_m', 'dist_channel_m', 'area_m2',
        'reg_level', 'reg_source', 'cems_level', 'cems_type', 'hot_class', 'max_level', 'n_products_destroyed',
        'cems_aoi', 'in_hot_aoi', 'in_flow_extent']].to_parquet(DER/'harmonised_inventory.parquet', index=False)
    # 1. Product summary
    rows = []
    rows.append(dict(product='HOT (local, AI-assisted labels on OSM footprints)', assessed=1053,
                     damaged=int((st.hot_class >= 1).sum()), destroyed=int((st.hot_class == 3).sum())))
    rows.append(dict(product='CEMS EMSR927 latest grading (photo-interpretation)', assessed=17299,
                     damaged=int((st.cems_level >= 1).sum()), destroyed=int((st.cems_level == 3).sum())))
    for src, lab in [('EMSR927', 'UNDP RAPIDA: CEMS-attributed'), ('Sertit', 'UNDP RAPIDA: SERTIT-attributed'),
                     ('UNOSAT_FL20260826NPL', 'UNDP RAPIDA: UNOSAT-attributed')]:
        s = st[st.reg_source == src]
        rows.append(dict(product=lab, assessed=np.nan, damaged=int(s.reg_n.sum() if 'reg_n' in s else len(s)),
                         destroyed=int((s.reg_level == 3).sum())))
    rows.append(dict(product='Harmonised union (>=1 product)', assessed=np.nan, damaged=int(st.any_damage.sum()),
                     destroyed=int(st.destroyed.sum())))
    rows.append(dict(product='Destroyed in >=2 products', assessed=np.nan, damaged=np.nan,
                     destroyed=int((st.n_products_destroyed >= 2).sum())))
    pd.DataFrame(rows).to_csv(TAB/'products_summary.csv', index=False)
    # 2. Harmonised inventory by municipality (with building type from CEMS where available)
    g = st.groupby('municipality')
    mt = pd.DataFrame(dict(damaged=g.any_damage.sum(), destroyed=g.destroyed.sum(),
                           destroyed_2plus=g.n_products_destroyed.apply(lambda v: int((v >= 2).sum())),
                           damaged_cems=g.cems_level.apply(lambda v: int((v >= 1).sum())),
                           destroyed_hot=g.hot_class.apply(lambda v: int((v == 3).sum())),
                           destroyed_undp=g.reg_level.apply(lambda v: int((v == 3).sum())),
                           residential_cems=g.apply(lambda d: int(((d.cems_level >= 1) & (d.cems_type == 'Residential')).sum())),
                           nonresidential_cems=g.apply(lambda d: int(((d.cems_level >= 1) & d.cems_type.isin(
                               ['Non residential', 'School, university and research buildings'])).sum())),
                           chainage_median_km=g.chainage_km.median())).reset_index()
    mt = mt[mt.damaged > 0].sort_values('chainage_median_km')
    mt.to_csv(TAB/'harmonised_by_municipality.csv', index=False, float_format='%.4g')
    # 3. Agreement: HOT vs CEMS where both graded (CEMS AOI 1-2 and HOT inventory)
    both = st[(st.hot_class >= 0) & (st.cems_aoi.isin([1, 2]))]
    ct = pd.crosstab(both.hot_class.map({0: 'HOT no damage', 1: 'HOT minor', 2: 'HOT major', 3: 'HOT destroyed'}),
                     both.cems_level.map({0: 'CEMS no record', 1: 'CEMS possibly damaged', 2: 'CEMS damaged', 3: 'CEMS destroyed'}))
    ct.to_csv(TAB/'agreement_hot_cems.csv')
    kap_bin = cohen_kappa_score(both.hot_class == 3, both.cems_level == 3)
    kap_any = cohen_kappa_score(both.hot_class >= 1, both.cems_level >= 1)
    kap_w = cohen_kappa_score(both.hot_class, both.cems_level, weights='linear')
    agree = dict(n=int(len(both)), kappa_destroyed=kap_bin, kappa_any_damage=kap_any, kappa_linear_weighted=kap_w,
                 pct_agree_destroyed=100*float(((both.hot_class == 3) == (both.cems_level == 3)).mean()),
                 hot_destroyed_confirmed_by_cems_pct=100*float((both[both.hot_class == 3].cems_level == 3).mean()),
                 cems_destroyed_confirmed_by_hot_pct=100*float((both[both.cems_level == 3].hot_class == 3).mean()))
    # UNOSAT-attributed vs CEMS inside CEMS AOIs
    u = st[(st.cems_aoi > 0) & (st.reg_source == 'UNOSAT_FL20260826NPL')]
    agree['unosat_destroyed_in_cems_aoi'] = int(len(u))
    agree['unosat_destroyed_confirmed_by_cems_pct'] = 100*float((u.cems_level == 3).mean()) if len(u) else np.nan
    agree['unosat_destroyed_any_cems_damage_pct'] = 100*float((u.cems_level >= 1).mean()) if len(u) else np.nan
    (DER/'products_results.json').write_text(json.dumps(agree, indent=1, default=float), encoding='utf-8')
    print(pd.DataFrame(rows).to_string()); print(mt.to_string()); print(ct); print(json.dumps(agree, indent=1, default=float))


if __name__ == '__main__':
    main()
