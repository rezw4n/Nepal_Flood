"""Independent Sentinel-2 corroboration of the building-damage labels and of the UNOSAT flow extent.

Change indices (post - pre; seasonally matched clear-sky medians, 20 m) are sampled as the mean
of a 3 x 3 pixel window (60 m) centred on each building. Separability of damage classes is
summarised by ROC AUC; the disturbance map is an Otsu threshold of the NDVI decrease within
1.5 km of the channel, compared with the UNOSAT extent.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import rasterio
from scipy.ndimage import uniform_filter
from sklearn.metrics import roc_auc_score
from skimage.filters import threshold_otsu
from rasterio.features import rasterize
from corridor import DER, ROOT
from analyse import read_shape_zip, SRC

S2 = ROOT/'sources_ext'/'s2'
TAB = ROOT/'tables'
IDX = ['ndvi', 'bsi', 'bright', 'ndwi']


def load_delta():
    out = {}
    for k in IDX:
        with rasterio.open(S2/f's2_delta_{k}.tif') as s:
            a = s.read(1).astype('float64'); T = s.transform
        valid = np.isfinite(a)
        num = uniform_filter(np.where(valid, a, 0), 3); den = uniform_filter(valid.astype(float), 3)
        with np.errstate(invalid='ignore', divide='ignore'):
            out[k] = np.where(den > 0.5, num/den, np.nan)
    return out, T


def sample(arr, T, x, y):
    r, c = rasterio.transform.rowcol(T, np.asarray(x), np.asarray(y))
    r = np.asarray(r); c = np.asarray(c)
    ok = (r >= 0) & (r < arr.shape[0]) & (c >= 0) & (c < arr.shape[1])
    v = np.full(len(r), np.nan); v[ok] = arr[r[ok], c[ok]]
    return v


def main():
    d, T = load_delta()
    st = pd.read_parquet(DER/'corridor_buildings.parquet').drop(columns=['wkb_utm'])
    st['destroyed'] = ((st.reg_level == 3) | (st.cems_level == 3) | (st.hot_class == 3)).astype(int)
    st['any_damage'] = ((st.reg_level >= 1) | (st.cems_level >= 1) | (st.hot_class >= 1)).astype(int)
    st['assessed'] = ((st.cems_aoi > 0) & ~st.cems_not_analysed) | (st.hot_class >= 0)
    for k in IDX:
        st[f'd_{k}'] = sample(d[k], T, st.x, st.y)
    a = st[st.assessed & st.d_ndvi.notna() & (st.dist_channel_m <= 1000)].copy()
    rows = []
    for k, sign in [('ndvi', -1), ('bsi', 1), ('bright', 1), ('ndwi', 1)]:
        for target, sub in [('destroyed vs not (all assessed)', a),
                            ('destroyed vs no record (CEMS AOIs)', a[(a.cems_aoi > 0) & ((a.destroyed == 1) | (a.any_damage == 0))]),
                            ('HOT destroyed vs HOT no damage', a[a.hot_class.isin([0, 3])])]:
            y = (sub.hot_class == 3).astype(int) if target.startswith('HOT') else sub.destroyed
            if y.nunique() < 2:
                continue
            rows.append(dict(index=k, target=target, n=len(sub), auc=roc_auc_score(y, sign*sub[f'd_{k}'])))
    auc = pd.DataFrame(rows)
    auc.to_csv(TAB/'s2_separability_auc.csv', index=False, float_format='%.4f')
    # class-wise distributions (HOT four classes; harmonised levels)
    hot = a[a.hot_class >= 0]
    dist = []
    for lev, g in hot.groupby('hot_class'):
        for k in IDX:
            q = g[f'd_{k}'].quantile([.1, .25, .5, .75, .9]).to_numpy()
            dist.append(dict(product='HOT', level=int(lev), index=k, n=len(g), p10=q[0], p25=q[1], p50=q[2], p75=q[3], p90=q[4]))
    a['level'] = np.maximum(a.reg_level, a.cems_level)
    for lev, g in a[a.cems_aoi > 0].groupby('level'):
        for k in IDX:
            q = g[f'd_{k}'].quantile([.1, .25, .5, .75, .9]).to_numpy()
            dist.append(dict(product='CEMS/UNDP', level=int(lev), index=k, n=len(g), p10=q[0], p25=q[1], p50=q[2], p75=q[3],
                             p90=q[4]))
    pd.DataFrame(dist).to_csv(TAB/'s2_change_by_class.csv', index=False, float_format='%.4f')
    a[['id', 'x', 'y', 'chainage_km', 'rem_m', 'destroyed', 'any_damage', 'hot_class', 'reg_level', 'cems_level',
       'd_ndvi', 'd_bsi', 'd_bright', 'd_ndwi']].to_parquet(DER/'s2_building_samples.parquet', index=False)
    # disturbance map vs UNOSAT extent (chainage 0-106 km, within 1.5 km of channel)
    with rasterio.open(S2/'s2_delta_ndvi.tif') as s:
        dn = s.read(1)
    with rasterio.open(S2/'s2_pre_ndvi.tif') as s:
        pre = s.read(1)
    flood, _, _ = read_shape_zip(SRC/'unosat_3.html')
    fm = rasterize([(flood, 1)], out_shape=dn.shape, transform=T, fill=0, dtype='uint8').astype(bool)
    from corridor import Channel
    ch = Channel()
    H, W = dn.shape
    xs = T.c + (np.arange(W) + .5)*T.a; ys = T.f + (np.arange(H) + .5)*T.e
    gx, gy = np.meshgrid(xs, ys)
    dist_, i = ch.tree.query(np.c_[gx.ravel(), gy.ravel()])
    dom = ((dist_ <= 1500) & (ch.chain[i] <= 106000)).reshape(H, W) & np.isfinite(dn)
    thr = threshold_otsu(dn[dom])
    chg = dom & (dn < thr)
    tp = (chg & fm).sum(); fp = (chg & ~fm).sum(); fn = (dom & fm & ~chg).sum()
    res = dict(otsu_threshold_dndvi=float(thr), precision=float(tp/(tp + fp)), recall=float(tp/(tp + fn)),
               iou=float(tp/(tp + fp + fn)), change_area_km2=float(chg.sum()*400/1e6),
               unosat_area_in_domain_km2=float((dom & fm).sum()*400/1e6),
               median_dndvi_in_extent=float(np.nanmedian(dn[dom & fm])), median_dndvi_outside=float(np.nanmedian(dn[dom & ~fm])),
               n_pre_scenes=len(json.loads((S2/'s2_log.json').read_text())['pre']),
               n_post_scenes=len(json.loads((S2/'s2_log.json').read_text())['post']))
    (DER/'s2_results.json').write_text(json.dumps(res, indent=1), encoding='utf-8')
    with rasterio.open(S2/'s2_delta_ndvi.tif') as s:
        meta = s.profile.copy()
    meta.update(dtype='uint8', nodata=0)
    with rasterio.open(DER/'s2_disturbance_mask.tif', 'w', **meta) as f:
        f.write((chg.astype('uint8')*1 + (dom & ~chg).astype('uint8')*2), 1)
    print(auc.round(3).to_string()); print(json.dumps(res, indent=1))
    print(pd.DataFrame(dist).query("index=='ndvi'").round(3).to_string())


if __name__ == '__main__':
    main()
