"""Terrain controls on building damage, destructive-height envelope and predictive models.

Inputs: data/derived/hot_buildings_features.csv, data/derived/corridor_buildings.parquet,
        data/derived/transects.csv
Outputs: tables/terrain_*.csv, tables/ml_*.csv, data/derived/model_predictions.parquet,
         data/derived/terrain_results.json
All resampling uses a fixed seed; blocks are 1-km chainage segments (spatial clustering).
"""
from pathlib import Path
import json
import warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.miscmodels.ordinal_model import OrderedModel
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GroupKFold
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss
from sklearn.inspection import permutation_importance, partial_dependence
from scipy.spatial import cKDTree

ROOT = Path(__file__).resolve().parents[1]
DER, TAB = ROOT/'data'/'derived', ROOT/'tables'
SEED = 20260826
RNG = np.random.default_rng(SEED)
NBOOT = 1000
MAXDIST = 1000.0                # m from channel for regional modelling
REACH_GROUPS = {'gorge_21_41km': (21, 41), 'middle_64_89km': (64, 89), 'lower_89_114km': (89, 114)}
REM_BINS = [-20, 0, 10, 20, 30, 40, 50, 60, 80, 100, 150, 400]
FEATURES = ['rem_m', 'dist_channel_m', 'chainage_km', 'valley_width_20m', 'channel_slope',
            'outer_bank', 'slope_deg', 'log_area', 'n_within_100m']
LABELS = {'rem_m': 'Height above channel', 'dist_channel_m': 'Distance to channel', 'chainage_km': 'Distance downstream',
          'valley_width_20m': 'Valley-floor width', 'channel_slope': 'Channel gradient', 'outer_bank': 'Outer bank of bend',
          'slope_deg': 'Hillslope angle', 'log_area': 'Footprint area (log)', 'n_within_100m': 'Building density'}


def save(df, name):
    df.to_csv(TAB/f'{name}.csv', index=False, float_format='%.6g')


def wilson(k, n, z=1.96):
    if n == 0:
        return np.nan, np.nan
    p = k/n; d = 1 + z*z/n
    c = (p + z*z/(2*n))/d; h = z*np.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return c - h, c + h


def block_ids(chainage_km, size_km=1.0):
    return np.floor(np.asarray(chainage_km)/size_km).astype(int)


def logit_fit(x, y):
    X = sm.add_constant(np.asarray(x, float))
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        return sm.Logit(np.asarray(y, float), X).fit(disp=0)


def block_bootstrap_logit(x, y, blocks, grid, nboot=NBOOT):
    """Percentile CI of P(y|x) on grid and of x50 = -b0/b1, resampling 1-km blocks with replacement."""
    ub = np.unique(blocks)
    idx_by = {b: np.where(blocks == b)[0] for b in ub}
    curves, x50 = [], []
    for _ in range(nboot):
        take = np.concatenate([idx_by[b] for b in RNG.choice(ub, len(ub), replace=True)])
        yy = y[take]
        if yy.min() == yy.max():
            continue
        try:
            m = logit_fit(x[take], yy)
        except Exception:
            continue
        b0, b1 = m.params
        curves.append(1/(1 + np.exp(-(b0 + b1*grid))))
        if b1 != 0:
            x50.append(-b0/b1)
    curves = np.array(curves)
    return np.percentile(curves, [2.5, 97.5], axis=0), np.percentile(x50, [2.5, 50, 97.5]) if x50 else [np.nan]*3


def load():
    hot = pd.read_csv(DER/'hot_buildings_features.csv')
    hot['log_area'] = np.log(hot.area_m2)
    reg = pd.read_parquet(DER/'corridor_buildings.parquet').drop(columns=['wkb_utm'])
    reg['log_area'] = np.log(reg.area_m2.clip(lower=1))
    # density for HOT buildings from the full stock (consistent definition)
    t = cKDTree(reg[['x', 'y']].to_numpy())
    hot['n_within_100m'] = [len(v) - 1 for v in t.query_ball_point(hot[['x', 'y']].to_numpy(), 100)]
    hot['n_within_100m'] = hot.n_within_100m.clip(lower=0)
    for d in (hot, reg):
        d['outer_bank'] = d.outer_bank.astype(int)
    reg['destroyed'] = ((reg.reg_level == 3) | (reg.cems_level == 3) | (reg.hot_class == 3)).astype(int)
    reg['any_damage'] = ((reg.reg_level >= 1) | (reg.cems_level >= 1) | (reg.hot_class >= 1)).astype(int)
    reg['assessed'] = ((reg.cems_aoi > 0) & ~reg.cems_not_analysed) | (reg.hot_class >= 0)
    return hot, reg


def local_curves(hot):
    c = hot[hot.damage != 'no-data'].copy()
    c['rem_bin'] = pd.cut(c.rem_m, REM_BINS)
    rows = []
    for b, g in c.groupby('rem_bin', observed=True):
        n = len(g)
        row = dict(rem_bin=str(b), rem_mid=b.mid, n=n)
        for cls in ['no-damage', 'minor-damage', 'major-damage', 'destroyed']:
            k = int((g.damage == cls).sum()); lo, hi = wilson(k, n)
            row.update({f'{cls}_n': k, f'{cls}_pct': 100*k/n, f'{cls}_lo': 100*lo, f'{cls}_hi': 100*hi})
        rows.append(row)
    save(pd.DataFrame(rows), 'terrain_local_rem_bins')
    # logistic P(destroyed | REM) with 1-km block bootstrap
    y = (c.damage == 'destroyed').to_numpy(int); x = c.rem_m.to_numpy()
    grid = np.linspace(-10, 200, 211)
    m = logit_fit(x, y)
    ci, x50 = block_bootstrap_logit(x, y, block_ids(c.chainage_km), grid)
    b0, b1 = m.params
    curve = pd.DataFrame(dict(rem_m=grid, p=1/(1+np.exp(-(b0+b1*grid))), lo=ci[0], hi=ci[1]))
    save(curve, 'terrain_local_logit_curve')
    # distance curve
    xd = c.dist_channel_m.to_numpy()
    md = logit_fit(xd, y)
    gd = np.linspace(0, 450, 226)
    cid, d50 = block_bootstrap_logit(xd, y, block_ids(c.chainage_km), gd)
    save(pd.DataFrame(dict(dist_m=gd, p=1/(1+np.exp(-(md.params[0]+md.params[1]*gd))), lo=cid[0], hi=cid[1])),
         'terrain_local_logit_dist_curve')
    return dict(rem50_m=float(-b0/b1), rem50_ci=[float(x50[0]), float(x50[2])], logit_b1_per_10m=float(10*b1),
                or_per_10m=float(np.exp(10*b1)), dist50_m=float(-md.params[0]/md.params[1]),
                dist50_ci=[float(d50[0]), float(d50[2])], n=int(len(c)), n_destroyed=int(y.sum()),
                auc_rem_only=float(roc_auc_score(y, x*-1)), auc_dist_only=float(roc_auc_score(y, -xd)))


def multivariable(hot):
    c = hot[hot.damage != 'no-data'].copy()
    X = pd.DataFrame(dict(rem_10m=c.rem_m/10, log_dist=np.log(c.dist_channel_m.clip(lower=5)), chainage_10km=c.chainage_km/10,
                          valley_100m=c.valley_width_20m/100, outer_bank=c.outer_bank, slope_10deg=c.slope_deg/10,
                          log_area=c.log_area, density_10=c.n_within_100m/10))
    groups = block_ids(c.chainage_km)
    out = []
    for name, y in [('destroyed', (c.damage == 'destroyed').astype(int)),
                    ('severe', c.damage.isin(['major-damage', 'destroyed']).astype(int))]:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            m = sm.Logit(y.to_numpy(), sm.add_constant(X)).fit(disp=0, cov_type='cluster', cov_kwds={'groups': groups})
        ci = m.conf_int()
        for k in X.columns:
            out.append(dict(model=f'logit_{name}', term=k, coef=m.params[k], se=m.bse[k], odds_ratio=np.exp(m.params[k]),
                            or_lo=np.exp(ci.loc[k, 0]), or_hi=np.exp(ci.loc[k, 1]), p=m.pvalues[k],
                            n=int(m.nobs), pseudo_r2=m.prsquared))
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        om = OrderedModel(c.damage_class.to_numpy(), X, distr='logit').fit(method='bfgs', disp=0, maxiter=2000)
    ci = om.conf_int()
    for k in X.columns:
        out.append(dict(model='ordinal_logit', term=k, coef=om.params[k], se=om.bse[k], odds_ratio=np.exp(om.params[k]),
                        or_lo=np.exp(ci.loc[k, 0]), or_hi=np.exp(ci.loc[k, 1]), p=om.pvalues[k], n=int(om.nobs),
                        pseudo_r2=np.nan))
    df = pd.DataFrame(out)
    save(df, 'terrain_local_models')
    return df


def regional_domain(reg):
    """Buildings inside an area actually graded by CEMS (excluding not-analysed zones) or graded by HOT."""
    d = reg[reg.assessed & (reg.dist_channel_m <= MAXDIST) & reg.rem_m.notna()].copy()
    return d


def envelope(reg, trans):
    d = regional_domain(reg)
    reaches = [(21, 26), (26, 31), (31, 36), (36, 41), (64, 70), (70, 76), (76, 82), (82, 88), (88, 94), (94, 100),
               (100, 107), (107, 114)]
    rows = []
    for a, b in reaches:
        g = d[(d.chainage_km >= a) & (d.chainage_km < b) & (d.rem_m < 250)]
        nd = int(g.destroyed.sum())
        row = dict(reach_start_km=a, reach_end_km=b, reach_mid_km=(a+b)/2, n_buildings=len(g), n_destroyed=nd)
        if nd >= 15 and (len(g) - nd) >= 15:
            m = logit_fit(g.rem_m, g.destroyed)
            b0, b1 = m.params
            _, x50 = block_bootstrap_logit(g.rem_m.to_numpy(), g.destroyed.to_numpy(), block_ids(g.chainage_km, .5),
                                           np.array([0.0]), nboot=500)
            row.update(rem50_m=-b0/b1 if b1 < 0 else np.nan, rem50_lo=x50[0], rem50_hi=x50[2], slope_per_10m=10*b1)
        dz = g[g.destroyed == 1].rem_m
        if len(dz) >= 5:
            row.update(rem_destroyed_p50=dz.quantile(.5), rem_destroyed_p90=dz.quantile(.9), rem_destroyed_p95=dz.quantile(.95))
        t = trans[(trans.chainage_km >= a) & (trans.chainage_km < b)]
        e = pd.concat([t.flow_edge_rem_left, t.flow_edge_rem_right]).dropna()
        e = e[e > -20]
        if len(e) >= 5:
            row.update(flow_edge_rem_p25=e.quantile(.25), flow_edge_rem_p50=e.quantile(.5), flow_edge_rem_p75=e.quantile(.75))
        row.update(valley_width_20m_median=t.valley_width_20m.median(), flow_width_median=t.flow_width_m.median())
        rows.append(row)
    env = pd.DataFrame(rows)
    save(env, 'terrain_envelope_by_reach')
    return env


def ml(reg, hot):
    d = regional_domain(reg)
    X = d[FEATURES].astype(float).to_numpy(); y = d.destroyed.to_numpy()
    groups = block_ids(d.chainage_km, 5.0)
    gkf = GroupKFold(n_splits=6)
    oof = {'gbm': np.zeros(len(d)), 'logit_full': np.zeros(len(d)), 'logit_rem': np.zeros(len(d))}
    imps = []
    for k, (tr, te) in enumerate(gkf.split(X, y, groups)):
        gbm = HistGradientBoostingClassifier(max_iter=400, learning_rate=0.05, max_leaf_nodes=31, min_samples_leaf=40,
                                             l2_regularization=1.0, random_state=SEED)
        gbm.fit(X[tr], y[tr]); oof['gbm'][te] = gbm.predict_proba(X[te])[:, 1]
        lf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)); lf.fit(X[tr], y[tr])
        oof['logit_full'][te] = lf.predict_proba(X[te])[:, 1]
        lr = LogisticRegression(max_iter=2000); lr.fit(X[tr][:, [0]], y[tr])
        oof['logit_rem'][te] = lr.predict_proba(X[te][:, [0]])[:, 1]
        if y[te].min() != y[te].max():
            pi = permutation_importance(gbm, X[te], y[te], scoring='roc_auc', n_repeats=10, random_state=SEED)
            imps.append(pi.importances_mean)
    perf = []
    for name, p in oof.items():
        perf.append(dict(model=name, auc=roc_auc_score(y, p), pr_auc=average_precision_score(y, p),
                         brier=brier_score_loss(y, p), prevalence=y.mean(), n=len(y), cv='GroupKFold(6) on 5-km chainage blocks'))
    # sensitivity: CEMS labels only, inside CEMS-graded areas
    cm = (d.cems_aoi > 0).to_numpy()
    yc = (d.cems_level == 3).to_numpy(int)[cm]
    pc = np.zeros(cm.sum())
    for tr, te in GroupKFold(n_splits=4).split(X[cm], yc, groups[cm]):
        m_ = HistGradientBoostingClassifier(max_iter=400, learning_rate=0.05, max_leaf_nodes=31, min_samples_leaf=40,
                                            l2_regularization=1.0, random_state=SEED).fit(X[cm][tr], yc[tr])
        pc[te] = m_.predict_proba(X[cm][te])[:, 1]
    perf.append(dict(model='gbm_cems_labels_only', auc=roc_auc_score(yc, pc), pr_auc=average_precision_score(yc, pc),
                     brier=brier_score_loss(yc, pc), prevalence=yc.mean(), n=len(yc), cv='GroupKFold(4), CEMS AOIs only'))
    imp = pd.DataFrame(dict(feature=FEATURES, label=[LABELS[f] for f in FEATURES],
                            importance_auc_drop=np.mean(imps, axis=0), importance_sd=np.std(imps, axis=0)))
    imp = imp.sort_values('importance_auc_drop', ascending=False)
    save(imp, 'ml_permutation_importance')
    # final model on all assessed data; partial dependence
    gbm = HistGradientBoostingClassifier(max_iter=400, learning_rate=0.05, max_leaf_nodes=31, min_samples_leaf=40,
                                         l2_regularization=1.0, random_state=SEED).fit(X, y)
    pds = []
    for f in ['rem_m', 'dist_channel_m', 'chainage_km', 'valley_width_20m']:
        j = FEATURES.index(f)
        pdr = partial_dependence(gbm, X, [j], grid_resolution=60, percentiles=(0.01, 0.99), kind='average')
        pds.append(pd.DataFrame(dict(feature=f, value=pdr['grid_values'][0], pd=pdr['average'][0])))
    save(pd.concat(pds), 'ml_partial_dependence')
    j0, j1 = FEATURES.index('rem_m'), FEATURES.index('chainage_km')
    pd2 = partial_dependence(gbm, X, [(j0, j1)], grid_resolution=40, percentiles=(0.01, 0.99), kind='average')
    gx, gy = pd2['grid_values']
    save(pd.DataFrame([(a, b, pd2['average'][0][i, k]) for i, a in enumerate(gx) for k, b in enumerate(gy)],
                      columns=['rem_m', 'chainage_km', 'pd']), 'ml_partial_dependence_2d')
    # transfer test: train on regional labels outside the HOT reach, predict HOT labels
    hot_c = hot[hot.damage != 'no-data'].copy()
    lo_c, hi_c = hot_c.chainage_km.min() - 1, hot_c.chainage_km.max() + 1
    trn = (d.chainage_km < lo_c) | (d.chainage_km > hi_c)
    gbm_t = HistGradientBoostingClassifier(max_iter=400, learning_rate=0.05, max_leaf_nodes=31, min_samples_leaf=40,
                                           l2_regularization=1.0, random_state=SEED).fit(X[trn], y[trn])
    Xh = hot_c[FEATURES].astype(float).to_numpy()
    ph = gbm_t.predict_proba(Xh)[:, 1]
    yh = (hot_c.damage == 'destroyed').astype(int).to_numpy()
    lr_t = LogisticRegression(max_iter=2000).fit(X[trn][:, [0]], y[trn])
    transfer = dict(train_n=int(trn.sum()), train_reach_excluded_km=[float(lo_c), float(hi_c)], test_n=len(yh),
                    auc_gbm=roc_auc_score(yh, ph), auc_logit_rem=roc_auc_score(yh, lr_t.predict_proba(Xh[:, [0]])[:, 1]),
                    spearman_ordinal=float(pd.Series(ph).corr(pd.Series(hot_c.damage_class.to_numpy()), method='spearman')))
    perf.append(dict(model='gbm_transfer_to_HOT', auc=transfer['auc_gbm'], pr_auc=average_precision_score(yh, ph),
                     brier=brier_score_loss(yh, ph), prevalence=yh.mean(), n=len(yh), cv='trained outside HOT reach'))
    save(pd.DataFrame(perf), 'ml_performance')
    # predictions for verification screening within the assessed reach
    d = d.assign(p_destroyed_oof=oof['gbm'])
    d[['id', 'origin', 'x', 'y', 'lon', 'lat', 'chainage_km', 'rem_m', 'dist_channel_m', 'destroyed', 'any_damage',
       'reg_level', 'hot_class', 'p_destroyed_oof']].to_parquet(DER/'model_predictions.parquet', index=False)
    hot_c.assign(p_destroyed_transfer=ph)[['osm_id', 'damage', 'chainage_km', 'rem_m', 'p_destroyed_transfer']].to_csv(
        DER/'hot_transfer_predictions.csv', index=False)
    calib = pd.DataFrame(dict(p=oof['gbm'], y=y)).assign(bin=lambda t: pd.qcut(t.p, 10, duplicates='drop'))
    save(calib.groupby('bin', observed=True).agg(p_mean=('p', 'mean'), y_mean=('y', 'mean'), n=('y', 'size')).reset_index(drop=True),
         'ml_calibration')
    screen = d[(d.destroyed == 0) & (d.any_damage == 0) & (d.p_destroyed_oof >= 0.5)]
    return dict(perf=perf, transfer=transfer, n_domain=int(len(d)), n_destroyed=int(y.sum()),
                n_unlabelled_high_risk=int(len(screen)))


def setbacks(reg, hot):
    d = regional_domain(reg)
    dz = d[d.destroyed == 1]
    out = []
    for h in [5, 10, 15, 20, 30, 40, 50, 75, 100]:
        row = dict(rem_threshold_m=h, destroyed_below_pct=100*(dz.rem_m < h).mean())
        for name, (a, b) in REACH_GROUPS.items():
            zz = dz[dz.chainage_km.between(a, b)]
            row[f'{name}_destroyed_below_pct'] = 100*(zz.rem_m < h).mean() if len(zz) else np.nan
        full = reg[(reg.dist_channel_m <= 500) & (reg.destroyed == 0)]
        row['undamaged_stock_below_0_207km'] = int((full.rem_m < h).sum())
        row['undamaged_stock_below_106_207km'] = int(((full.rem_m < h) & (full.chainage_km > 106)).sum())
        out.append(row)
    df = pd.DataFrame(out)
    save(df, 'terrain_setback_thresholds')
    return df


def reach_group_curves(reg):
    """P(destroyed | height above channel) by reach group, 1-km block bootstrap bands."""
    d = regional_domain(reg)
    grid = np.linspace(-5, 120, 126)
    out = []
    for name, (a, b) in REACH_GROUPS.items():
        g = d[d.chainage_km.between(a, b) & (d.rem_m < 250)]
        m = logit_fit(g.rem_m, g.destroyed)
        ci, x50 = block_bootstrap_logit(g.rem_m.to_numpy(), g.destroyed.to_numpy(), block_ids(g.chainage_km), grid, nboot=500)
        p = 1/(1 + np.exp(-(m.params[0] + m.params[1]*grid)))
        out.append(pd.DataFrame(dict(group=name, rem_m=grid, p=p, lo=ci[0], hi=ci[1], n=len(g), n_destroyed=int(g.destroyed.sum()),
                                     rem50=-m.params[0]/m.params[1], rem50_lo=x50[0], rem50_hi=x50[2])))
    df = pd.concat(out)
    save(df, 'terrain_curves_by_reachgroup')
    return df


def roc_tables(reg, hot):
    """ROC curve coordinates for the spatially cross-validated models and the transfer test."""
    from sklearn.metrics import roc_curve
    pr = pd.read_parquet(DER/'model_predictions.parquet')
    rows = []
    fpr, tpr, _ = roc_curve(pr.destroyed, pr.p_destroyed_oof)
    rows.append(pd.DataFrame(dict(model='Gradient boosting, spatial CV', fpr=fpr, tpr=tpr)))
    d = regional_domain(reg)
    fpr, tpr, _ = roc_curve(d.destroyed, -d.rem_m)
    rows.append(pd.DataFrame(dict(model='Height above channel only', fpr=fpr, tpr=tpr)))
    t = pd.read_csv(DER/'hot_transfer_predictions.csv')
    fpr, tpr, _ = roc_curve(t.damage == 'destroyed', t.p_destroyed_transfer)
    rows.append(pd.DataFrame(dict(model='Transfer to HOT labels', fpr=fpr, tpr=tpr)))
    # thin to <= 400 points per model for plotting
    rows = [r.iloc[np.unique(np.linspace(0, len(r) - 1, 400).astype(int))] for r in rows]
    save(pd.concat(rows), 'ml_roc_curves')


def main():
    hot, reg = load()
    trans = pd.read_csv(DER/'transects.csv')
    res = {'local': local_curves(hot)}
    mv = multivariable(hot)
    env = envelope(reg, trans)
    res['ml'] = ml(reg, hot)
    sb = setbacks(reg, hot)
    rg = reach_group_curves(reg)
    res['reach_groups'] = rg.groupby('group')[['n', 'n_destroyed', 'rem50', 'rem50_lo', 'rem50_hi']].first().reset_index().to_dict(orient='records')
    roc_tables(reg, hot)
    res['envelope'] = env.to_dict(orient='records')
    (DER/'terrain_results.json').write_text(json.dumps(res, indent=1, default=float), encoding='utf-8')
    print(json.dumps(res['local'], indent=1))
    print(mv[mv.model == 'logit_destroyed'][['term', 'odds_ratio', 'or_lo', 'or_hi', 'p']].round(3).to_string())
    print(mv[mv.model == 'ordinal_logit'][['term', 'odds_ratio', 'or_lo', 'or_hi', 'p']].round(3).to_string())
    print(env.round(1).to_string())
    print(pd.DataFrame(res['ml']['perf']).round(3).to_string()); print(res['ml']['transfer'])
    print(pd.read_csv(TAB/'ml_permutation_importance.csv').round(4).to_string())
    print(sb.round(1).to_string())


if __name__ == '__main__':
    main()
