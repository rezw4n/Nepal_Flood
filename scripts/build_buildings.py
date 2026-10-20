"""Building-level tables linking damage inventories, building stock and terrain.

Outputs (data/derived/):
  hot_buildings_features.csv   local HOT inventory (1,053) with terrain/channel attributes
  corridor_buildings.parquet   Overture stock within 2 km of the channel, augmented with
                               UNDP damage footprints that have no overlapping stock polygon,
                               labelled with regional (CEMS/SERTIT, UNOSAT) and HOT damage classes
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import shapely
from shapely import wkb as swkb
from shapely.geometry import shape
from shapely.ops import transform
from pyproj import Transformer
from corridor import Channel, sample, DER, ROOT
from analyse import read, read_shape_zip, SRC

PROJ = Transformer.from_crs('OGC:CRS84', 'EPSG:32645', always_xy=True).transform
TO_LL = Transformer.from_crs('EPSG:32645', 'EPSG:4326', always_xy=True)
REG_RANK = {'Possibly damaged': 1, 'Damaged': 2, 'Destroyed': 3}
HOT_RANK = {'no-data': -1, 'no-damage': 0, 'minor-damage': 1, 'major-damage': 2, 'destroyed': 3}
MAX_DIST = 2000.0


def terrain_columns(ch, trans, x, y):
    out = ch.locate(x, y)
    out['elev_m'] = sample(DER/'dem_utm30.tif', x, y)
    out['rem_m'] = sample(DER/'rem_utm30.tif', x, y)
    out['slope_deg'] = sample(DER/'slope_utm30.tif', x, y)
    # valley-floor and flow-extent widths from the nearest transect node
    tn = trans.node.to_numpy()
    j = np.searchsorted(tn, out.node.to_numpy()).clip(0, len(tn) - 1)
    j0 = (j - 1).clip(0)
    j = np.where(np.abs(tn[j0] - out.node) < np.abs(tn[j] - out.node), j0, j)
    for c in ['valley_width_10m', 'valley_width_20m', 'valley_width_40m', 'flow_width_m']:
        out[c] = trans[c].to_numpy()[j]
    # channel gradient (2-km smoothed) at the nearest node
    out['channel_slope'] = ch.p.slope.to_numpy()[out.node.to_numpy()]
    return out


def hot_table(ch, trans, flood):
    feats = read('hot_buildings')['features']
    geoms = [transform(PROJ, shape(f['geometry'])) for f in feats]
    pts = [g.representative_point() for g in geoms]
    df = pd.DataFrame([f['properties'] for f in feats])[['osm_id', 'damage', 'damage_class', 'damage_confidence']]
    df['area_m2'] = [g.area for g in geoms]
    df['x'] = [p.x for p in pts]; df['y'] = [p.y for p in pts]
    df['lon'], df['lat'] = TO_LL.transform(df.x.to_numpy(), df.y.to_numpy())
    df = pd.concat([df, terrain_columns(ch, trans, df.x, df.y)], axis=1)
    df['in_flow_extent'] = shapely.contains_xy(flood, df.x, df.y)
    prev = pd.read_csv(ROOT/'data'/'building_analysis.csv', usecols=['osm_id', 'municipality'])
    df = df.merge(prev, on='osm_id', how='left')
    df.to_csv(DER/'hot_buildings_features.csv', index=False, float_format='%.6g')
    return df, geoms


CEMS_LATEST = ['EMSR927_AOI01_GRA_PRODUCT_builtUpP_v1.json', 'EMSR927_AOI02_GRA_PRODUCT_builtUpP_v2.json',
               'EMSR927_AOI03_GRA_MONIT01_builtUpP_v1.json', 'EMSR927_AOI05_GRA_MONIT01_builtUpP_v2.json']


def cems_aois():
    """Extent of the latest grading product per AOI (dashboard API) and union of not-analysed areas."""
    j = json.loads((ROOT/'sources_ext'/'cems'/'EMSR927_dashboard.json').read_text(encoding='utf-8'))['results'][0]
    aois = {}
    for a in j['aois']:
        prods = [p for p in a['products'] if (p.get('stats') or {}).get('Built-up')]
        if not prods:
            continue
        latest = max(prods, key=lambda p: (p['monitoringNumber'], p['version']['number']))
        aois[a['number']] = transform(PROJ, shapely.from_wkt(latest['extent']))
    na = []
    for f in CEMS_LATEST:
        fn = ROOT/'sources_ext'/'cems'/f.replace('builtUpP', 'notAnalysedA')
        if fn.exists():
            na += [transform(PROJ, shape(ft['geometry'])) for ft in json.loads(fn.read_text(encoding='utf-8'))['features']
                   if ft.get('geometry')]
    return aois, (shapely.unary_union(na) if na else None)


def cems_points():
    """Latest version of each CEMS EMSR927 grading AOI; duplicate points (<2 m) across AOIs removed."""
    rows = []
    for f in CEMS_LATEST:
        for ft in json.loads((ROOT/'sources_ext'/'cems'/f).read_text(encoding='utf-8'))['features']:
            if not ft.get('geometry'):
                continue
            x, y = PROJ(*ft['geometry']['coordinates'][:2])
            p = ft['properties']
            rows.append(dict(cems_file=f, aoi=f.split('_')[1], x=x, y=y, grade=p.get('damage_gra'),
                             building_type=p.get('simplified'), obj_type=p.get('obj_type'), dmg_src_id=p.get('dmg_src_id')))
    cp = pd.DataFrame(rows)
    cp['level'] = cp.grade.map(REG_RANK).fillna(0).astype(int)
    keep = np.ones(len(cp), bool)
    t = shapely.STRtree(shapely.points(cp.x, cp.y))
    for i, j in zip(*t.query(shapely.points(cp.x, cp.y), predicate='dwithin', distance=2.0)):
        if i < j and keep[i] and cp.aoi[i] != cp.aoi[j]:
            keep[j] = False
    cp = cp[keep].reset_index(drop=True)
    cp.to_csv(DER/'cems_latest_points.csv', index=False, float_format='%.3f')
    return cp


def add_cems_latest(st, gu):
    cp = cems_points()
    pts = shapely.points(cp.x, cp.y)
    tree = shapely.STRtree(gu)
    # greedy one-to-one assignment: closest point-footprint pairs first (distance 0 = point inside footprint)
    pi, si = tree.query(pts, predicate='dwithin', distance=10.0)
    cand = pd.DataFrame(dict(pi=pi, si=si, d=shapely.distance(pts[pi], gu[si]))).sort_values(['d', 'pi'])
    match = pd.Series(-1, index=cp.index)
    used = set()
    for p, s_, _ in cand.itertuples(index=False):
        if match[p] < 0 and s_ not in used:
            match[p] = s_; used.add(s_)
    st['cems_level'] = 0; st['cems_type'] = ''
    for ci, si_ in match[match >= 0].items():
        st.at[si_, 'cems_level'] = cp.level[ci]; st.at[si_, 'cems_type'] = cp.building_type[ci]
    un = match[match < 0].index
    add = pd.DataFrame(dict(id=[f'cems_{i}' for i in un], origin='cems_only', source_dataset='CEMS point',
                            reg_level=0, reg_source='', reg_building_id=-1, reg_n=0, hot_class=-2,
                            cems_level=cp.level[un].to_numpy(), cems_type=cp.building_type[un].to_numpy()))
    sq = shapely.buffer(pts[un.to_numpy()], 4.0, cap_style='square')   # nominal 8 m footprint for unmatched points
    print('CEMS latest points', len(cp), 'matched to footprints', int((match >= 0).sum()), 'added as points', len(un))
    return pd.concat([st, add], ignore_index=True), np.concatenate([gu, sq])


def corridor_table(ch, trans, flood, analysed, hot_geoms, hot_df):
    st = pd.read_parquet(ROOT/'sources_ext'/'overture'/'buildings.parquet')
    g = shapely.from_wkb(st.wkb.to_numpy())
    st = st.drop(columns='wkb')
    xs, ys = shapely.get_coordinates(shapely.centroid(g)).T
    ex, ey = Transformer.from_crs('EPSG:4326', 'EPSG:32645', always_xy=True).transform(xs, ys)
    d, _ = ch.tree.query(np.c_[ex, ey])
    keep = d <= MAX_DIST
    st = st[keep].reset_index(drop=True)
    gu = shapely.transform(g[keep], lambda c: np.c_[Transformer.from_crs('EPSG:4326', 'EPSG:32645', always_xy=True)
                                                   .transform(c[:, 0], c[:, 1])])
    st['origin'] = 'overture'
    # Regional damage footprints (UNDP; CEMS/SERTIT and UNOSAT attributed)
    reg = json.loads((ROOT/'data'/'undp_debris_combined.geojson').read_text(encoding='utf-8'))['features']
    rg = np.array([transform(PROJ, shape(f['geometry'])) for f in reg], dtype=object)
    rp = pd.DataFrame([f['properties'] for f in reg])[['building_id', 'damage_level', 'source_y', 'synthetic',
                                                       'surface_m2', 'debris', 'site_type', 'n_floors', 'height_used', 'adm3_name']]
    tree = shapely.STRtree(gu)
    pairs = tree.query(rg, predicate='intersects')          # (reg index, stock index)
    # one-to-one: each regional footprint goes to the stock polygon it overlaps most
    ov = shapely.area(shapely.intersection(rg[pairs[0]], gu[pairs[1]]))
    best = pd.DataFrame(dict(ri=pairs[0], si=pairs[1], ov=ov)).sort_values('ov', ascending=False)
    best = best[best.ov > 0].drop_duplicates('ri')
    st['reg_level'] = 0; st['reg_source'] = ''; st['reg_building_id'] = -1; st['reg_n'] = 0
    for ri, si in zip(best.ri, best.si):
        lvl = REG_RANK[rp.damage_level[ri]]
        st.at[si, 'reg_n'] += 1
        if lvl > st.at[si, 'reg_level']:
            st.at[si, 'reg_level'] = lvl
            st.at[si, 'reg_source'] = rp.source_y[ri]
            st.at[si, 'reg_building_id'] = rp.building_id[ri]
    unmatched = np.setdiff1d(np.arange(len(rg)), best.ri.to_numpy())
    add = pd.DataFrame(dict(id=[f'undp_{rp.building_id[i]}' for i in unmatched], origin='undp_only',
                            source_dataset='UNDP footprint', reg_level=[REG_RANK[rp.damage_level[i]] for i in unmatched],
                            reg_source=rp.source_y[unmatched].to_numpy(), reg_building_id=rp.building_id[unmatched].to_numpy(),
                            reg_n=1))
    st = pd.concat([st, add], ignore_index=True)
    gu = np.concatenate([gu, rg[unmatched]])
    # HOT labels: greedy one-to-one by overlap area; HOT footprints without a stock match are added
    st['hot_class'] = -2  # not in HOT inventory
    hg = np.array(hot_geoms, dtype=object)
    hi_, si_ = shapely.STRtree(gu).query(hg, predicate='intersects')
    cand = pd.DataFrame(dict(hi=hi_, si=si_, ov=shapely.area(shapely.intersection(hg[hi_], gu[si_]))))
    cand = cand[cand.ov > 0].sort_values('ov', ascending=False)
    hmatch, used = {}, set()
    for h, s_, _ in cand.itertuples(index=False):
        if h not in hmatch and s_ not in used:
            hmatch[h] = s_; used.add(s_)
    for h, s_ in hmatch.items():
        st.at[s_, 'hot_class'] = HOT_RANK[hot_df.damage[h]]
    hu = np.array([h for h in range(len(hg)) if h not in hmatch])
    add = pd.DataFrame(dict(id=[f'hot_{hot_df.osm_id[h]}' for h in hu], origin='hot_only', source_dataset='HOT footprint',
                            reg_level=0, reg_source='', reg_building_id=-1, reg_n=0,
                            hot_class=[HOT_RANK[hot_df.damage[h]] for h in hu]))
    st = pd.concat([st, add], ignore_index=True)
    gu = np.concatenate([gu, hg[hu]]) if len(hu) else gu
    print('HOT footprints matched to stock', len(hmatch), 'added', len(hu))
    st, gu = add_cems_latest(st, gu)
    pts = shapely.point_on_surface(gu)
    st['x'], st['y'] = shapely.get_coordinates(pts).T
    st['area_m2'] = shapely.area(gu)
    st['lon'], st['lat'] = TO_LL.transform(st.x.to_numpy(), st.y.to_numpy())
    st = pd.concat([st, terrain_columns(ch, trans, st.x, st.y)], axis=1)
    st['in_flow_extent'] = shapely.contains_xy(flood, st.x, st.y)
    st['in_unosat_analysed'] = shapely.contains_xy(analysed, st.x, st.y)
    aois, notan = cems_aois()
    st['cems_aoi'] = 0
    for num, g in aois.items():
        st.loc[shapely.contains_xy(g, st.x, st.y) & (st.cems_aoi == 0), 'cems_aoi'] = num
    st['cems_not_analysed'] = shapely.contains_xy(notan, st.x, st.y) if notan is not None else False
    hot_aoi = shapely.unary_union([transform(PROJ, shape(f['geometry'])) for f in read('hot_aoi')['features']])
    st['in_hot_aoi'] = shapely.contains_xy(hot_aoi, st.x, st.y)
    # local density: stock buildings within 100 m
    t = shapely.STRtree(pts)
    st['n_within_100m'] = np.bincount(t.query(pts, predicate='dwithin', distance=100)[0], minlength=len(pts)) - 1
    st['wkb_utm'] = shapely.to_wkb(gu)
    st.to_parquet(DER/'corridor_buildings.parquet', index=False)
    return st


def main():
    ch = Channel()
    trans = pd.read_csv(DER/'transects.csv')
    flood, _, _ = read_shape_zip(SRC/'unosat_3.html')
    analysed, _, _ = read_shape_zip(SRC/'unosat_4.html')
    shapely.prepare(flood); shapely.prepare(analysed)
    hot, hot_geoms = hot_table(ch, trans, flood)
    print('HOT table', hot.shape)
    print(hot.groupby('damage')[['rem_m', 'dist_channel_m', 'chainage_km', 'valley_width_20m']].median().round(1))
    if (ROOT/'sources_ext'/'overture'/'buildings.parquet').exists():
        st = corridor_table(ch, trans, flood, analysed, hot_geoms, hot)
        print('corridor stock', st.shape, st.origin.value_counts().to_dict())
        print('regional damage levels matched', st.reg_level.value_counts().to_dict())
        print('HOT classes matched', st.hot_class.value_counts().to_dict())


if __name__ == '__main__':
    main()
