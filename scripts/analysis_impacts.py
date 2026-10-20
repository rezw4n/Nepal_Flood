"""Wave timing and warning lead time, municipal impact indicators, comparison with the official
RDNA, damage-calibrated danger zone, composite ranking with uncertainty, and debris sensitivity.

Reported times/values are transcribed from official documents archived in sources_ext/official
(CHWRR Assessment Report II, 13 Sep 2026; NDRRMA consolidated update to 3 Oct 2026; RDNA Table 10)
and from the NRSC/ISRO and ICIMOD syntheses; each is cited in the manuscript.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import rasterio
import shapely
from shapely.geometry import shape
from shapely.ops import transform
from pyproj import Transformer
from corridor import Channel, DER, ROOT, sample
from analysis_products import municipalities, assign

TAB = ROOT/'tables'
SEED = 20260826
RNG = np.random.default_rng(SEED)
PROJ = Transformer.from_crs('OGC:CRS84', 'EPSG:32645', always_xy=True).transform

# Front arrival / gauge-loss times, 26 Aug 2026 (NPT). Source: CHWRR Assessment Report II Table 2; NRSC (failure time).
TIMELINE = [
    ('Source failure (seismic onset)', 85.528159, 28.288708, '08:37:10', 'NRSC/ISRO; USGS us7000tbwb'),
    ('Rasuwagadhi (border)', 85.377649, 28.271297, '08:44:00', 'ICIMOD (22 km in 6 min 50 s); gauge lost 08:40, border hit 08:45 (CHWRR)'),
    ('Syaphrubesi gauge lost', 85.342554, 28.170650, '08:50:00', 'CHWRR Table 2'),
    ('Betrawati gauge lost', 85.180000, 27.970000, '09:20:00', 'CHWRR Table 2'),
    ('Galchhi', 85.003050, 27.802328, '10:28:00', 'CHWRR Table 2'),
    ('Phurke/Malekhu warning level', 84.844102, 27.802439, '11:26:00', 'CHWRR Table 2'),
    ('Mugling', 84.556000, 27.855000, '13:00:00', 'CHWRR Table 2; HiRISK'),
    ('Kali Khola danger level (threshold crossing, not arrival)', 84.546000, 27.833000, '14:14:00', 'CHWRR Table 2'),
    ('Devghat arrival', 84.430000, 27.710000, '15:20:00', 'CHWRR Table 2 (peak 16:00)'),
]
ALERTS = {'Seismic-triggered automatic alert (onset + 2 min)': '08:39:10',
          'First official phone warnings (08:46-08:54)': '08:50:00',
          'Mass SMS by DHM (09:15)': '09:15:00'}
# Observed stage rise (m) used for the downstream (unassessed) reach: Galchhi ~8.9 m (ICIMOD reconstruction),
# Kali Khola maximum 12.3 m vs ~3.2 m normal (CHWRR; DHM live level 19 Oct), Devghat 6.57 m vs ~4 m normal (CHWRR).
STAGE_RISE = [(105.9, 8.9), (172.0, 9.1), (206.8, 2.6)]
# RDNA Table 10 (data to 3 Sep 2026): affected private buildings by local level and construction type.
RDNA = pd.DataFrame([
    ('Rasuwa', 'Gosaikunda', 1043, 271, 370, 402, 1030.70), ('Rasuwa', 'Kalika', 112, 27, 59, 26, 88.78),
    ('Rasuwa', 'Aamachhodingmo', 57, 32, 16, 9, 37.18), ('Rasuwa', 'Uttargaya', 567, 127, 344, 96, 411.60),
    ('Nuwakot', 'Belkotgadhi', 212, 72, 108, 32, 145.42), ('Nuwakot', 'Bidur', 3026, 596, 1407, 1023, 2877.63),
    ('Nuwakot', 'Kispang', 696, 231, 342, 123, 497.54), ('Nuwakot', 'Tarakeshwor', 43, 22, 16, 5, 26.69),
    ('Dhading', 'Benighat Rorang', 1037, 565, 264, 208, 757.33), ('Dhading', 'Gajuri', 107, 45, 40, 22, 81.34),
    ('Dhading', 'Galchhi', 79, 29, 33, 17, 61.10), ('Dhading', 'Siddhalek', 228, 113, 94, 21, 134.65),
    ('Gorkha', 'Gandaki', 248, 134, 89, 25, 147.95), ('Gorkha', 'Shahid Lakhan', 15, 8, 5, 2, 9.65),
    ('Chitwan', 'Ichchhyakamana', 100, 47, 28, 25, 80.93)],
    columns=['district', 'municipality', 'rdna_affected_buildings', 'mud_bonded', 'cement_bonded', 'rcc_other',
             'rdna_damage_npr_crore'])
# Canonical names (geoBoundaries ADM3 / UNDP / RDNA spellings differ)
CANON = {'Tarkeshwar': 'Tarakeshwor', 'Galchi': 'Galchhi', 'Ichchhyakamana': 'Ichchhyakamana',
         'Ichchha Kamana': 'Ichchhyakamana', 'Sahid Lakhan': 'Shahid Lakhan', 'Anbukhaireni': 'Aanbu Khaireni',
         'Aanbu Khaireni': 'Aanbu Khaireni', 'Parbati Kunda': 'Parbatikunda', 'Amachodingmo': 'Aamachhodingmo'}


def canon(s):
    return s.map(lambda v: CANON.get(v, v))


def tsec(hms):
    h, m, s = map(int, hms.split(':'))
    return h*3600 + m*60 + s


def timing(ch):
    rows = []
    for name, lo, la, t, src in TIMELINE:
        x, y = PROJ(lo, la)
        d, i = ch.tree.query([x, y])
        rows.append(dict(place=name, chainage_km=ch.chain[i]/1000, offset_m=d, time=t, t_s=tsec(t), source=src))
    tl = pd.DataFrame(rows).sort_values('chainage_km').reset_index(drop=True)
    tl['minutes_after_onset'] = (tl.t_s - tl.t_s.iloc[0])/60
    tl['arrival'] = ~tl.place.str.contains('threshold')
    a = tl[tl.arrival]
    v = np.diff(a.chainage_km.to_numpy()*1000)/np.diff(a.t_s.to_numpy())
    tl.loc[a.index, 'celerity_from_previous_m_s'] = np.r_[np.nan, v]
    tl.to_csv(TAB/'timing_wave_arrivals.csv', index=False, float_format='%.4g')
    return tl


def arrival_seconds(tl, chain_km):
    a = tl[tl.arrival]
    return np.interp(chain_km, a.chainage_km, a.t_s)


def lead_times(tl, inv):
    out = inv[['id', 'municipality', 'chainage_km', 'destroyed', 'any_damage']].copy()
    out['arrival_s'] = arrival_seconds(tl, out.chainage_km)
    rows = []
    for name, t in ALERTS.items():
        lt = (out.arrival_s - tsec(t))/60
        out[name] = lt
        dz = lt[out.destroyed]
        rows.append(dict(scenario=name, alert_time=t, destroyed_n=int(out.destroyed.sum()),
                         pct_destroyed_negative=100*(dz <= 0).mean(), pct_destroyed_ge10=100*(dz >= 10).mean(),
                         pct_destroyed_ge30=100*(dz >= 30).mean(), pct_destroyed_ge60=100*(dz >= 60).mean(),
                         median_lead_destroyed_min=float(dz.median())))
    sc = pd.DataFrame(rows)
    sc.to_csv(TAB/'timing_lead_time_scenarios.csv', index=False, float_format='%.4g')
    by_m = out[out.destroyed].groupby('municipality').agg(destroyed=('id', 'size'), chainage_median_km=('chainage_km', 'median'),
                                                           **{f'lead_{k[:7]}_median_min': (k, 'median') for k in ALERTS})
    by_m = by_m.reset_index().sort_values('chainage_median_km')
    by_m.columns = ['municipality', 'destroyed', 'chainage_median_km', 'lead_seismic_min', 'lead_phone_min', 'lead_sms_min']
    by_m.to_csv(TAB/'timing_lead_time_by_municipality.csv', index=False, float_format='%.4g')
    return sc, by_m


def robust_reach_heights(env):
    """Per-reach core and outer destructive heights.
    core:  REM at 50% destruction probability where its CI is narrower than 60 m, otherwise the smaller of
           that estimate and the 90th-percentile height of destroyed buildings;
    outer: 90th-percentile height of destroyed buildings.
    Both are smoothed with a 3-reach running median inside each contiguous graded segment (gaps >10 km
    split segments), which suppresses single-reach outliers caused by a few up-slope records."""
    e = env.sort_values('reach_mid_km').reset_index(drop=True)
    good = e.rem50_m.notna() & (e.rem50_m > 0) & ((e.rem50_hi - e.rem50_lo) < 60)
    core = np.where(good, e.rem50_m, np.fmin(e.rem50_m.where(e.rem50_m > 0), e.rem_destroyed_p90)).astype(float)
    outer = np.array(e.rem_destroyed_p90, dtype=float)   # writable copy (pandas copy-on-write)
    seg = np.r_[0, np.cumsum(np.diff(e.reach_mid_km.to_numpy()) > 10)]
    for arr in (core, outer):
        for s in np.unique(seg):
            m = seg == s
            raw = pd.Series(arr[m])
            arr[m] = raw.rolling(3, center=True, min_periods=3).median().fillna(raw).to_numpy()   # ends keep raw values
    e['h_core'] = core; e['h_outer'] = np.maximum(outer, core)
    return e


def danger_height(chain_km, env, kind='core'):
    """Damage-calibrated destructive height (m above channel) along the corridor (see robust_reach_heights).
    Downstream of the last assessed reach: observed stage rise at gauges, linearly interpolated."""
    e = robust_reach_heights(env)
    e['h'] = e.h_core if kind == 'core' else e.h_outer
    xs = list(e.reach_mid_km) + [s[0] for s in STAGE_RISE if s[0] > e.reach_mid_km.max()]
    hs = list(e.h) + [s[1] for s in STAGE_RISE if s[0] > e.reach_mid_km.max()]
    order = np.argsort(xs)
    return np.interp(chain_km, np.array(xs)[order], np.array(hs)[order]), pd.DataFrame(dict(chainage_km=np.array(xs)[order], h_m=np.array(hs)[order]))


def debris_mc(inv, n=5000):
    """UNDP-style building-debris model (floor area x grade coefficient x settlement factor) with
    multiplicative uncertainty on coefficients and the urban settlement factor."""
    reg = json.loads((ROOT/'data'/'undp_debris_combined.geojson').read_text(encoding='utf-8'))['features']
    rp = pd.DataFrame([f['properties'] for f in reg])[['building_id', 'surface_m2', 'n_floors', 'site_type']]
    d = inv[inv.max_level >= 1].copy()
    d = d.merge(rp.rename(columns={'building_id': 'reg_building_id'}), on='reg_building_id', how='left')
    # site type for buildings without a UNDP record: density threshold calibrated on UNDP site types
    known = d.site_type.notna()
    thr = np.nanmedian([d.loc[known & (d.site_type == 'urban'), 'n_within_100m'].quantile(.25),
                        d.loc[known & (d.site_type == 'rural'), 'n_within_100m'].quantile(.75)])
    d['site'] = np.where(known, d.site_type, np.where(d.n_within_100m >= thr, 'urban', 'rural'))
    floors_med = d.loc[known].groupby('site_type').n_floors.mean().to_dict()
    area = d.area_m2.clip(lower=10).where(d.origin.isin(['overture', 'undp_only', 'hot_only']),
                                          d.loc[d.origin == 'overture', 'area_m2'].median())
    d['floor_area'] = np.where(d.surface_m2.notna(), d.surface_m2, area*d.site.map(floors_med).fillna(1.0))
    coef = d.max_level.map({1: 0.05, 2: 0.5, 3: 1.0}).to_numpy()
    sf = d.site.map({'urban': 3.0, 'peri-urban': 2.0, 'rural': 1.0}).to_numpy()
    base = d.floor_area.to_numpy()*coef*sf
    d['debris_t'] = base
    tot = np.empty(n); bidur_share = np.empty(n)
    is_bidur = (d.municipality == 'Bidur').to_numpy()
    urban = d.site.eq('urban').to_numpy()
    for k in range(n):
        m = RNG.uniform(0.6, 1.4)                 # +/-40% on grade coefficients (common factor)
        f_u = RNG.uniform(1.0, 3.0)               # urban settlement factor between none and UNDP's x3
        v = d.floor_area.to_numpy()*coef*m*np.where(urban, f_u, sf)
        tot[k] = v.sum(); bidur_share[k] = v[is_bidur].sum()/v.sum()
    np.save(DER/'debris_mc_draws.npy', np.c_[tot, bidur_share])
    nofactor = (d.floor_area.to_numpy()*coef).sum()
    res = dict(n_buildings=int(len(d)), debris_central_t=float(base.sum()),
               debris_mc_p05=float(np.percentile(tot, 5)), debris_mc_p50=float(np.percentile(tot, 50)),
               debris_mc_p95=float(np.percentile(tot, 95)), debris_no_settlement_factor_t=float(nofactor),
               bidur_share_central=float(base[is_bidur].sum()/base.sum()),
               bidur_share_no_factor=float((d.floor_area.to_numpy()*coef)[is_bidur].sum()/nofactor),
               bidur_share_mc_p05=float(np.percentile(bidur_share, 5)), bidur_share_mc_p95=float(np.percentile(bidur_share, 95)),
               density_threshold_urban=float(thr))
    bym = d.groupby('municipality').debris_t.sum().rename('debris_t_central').reset_index()
    return res, bym


def composite_rank(ind, cols, n=20000):
    """Rank uncertainty from random weights (Dirichlet), normalisation (min-max / rank / z) and aggregation."""
    X = ind[cols].astype(float).fillna(0).to_numpy()
    m = len(ind)
    ranks = np.zeros((n, m), int)
    for k in range(n):
        w = RNG.dirichlet(np.ones(len(cols)))
        norm = RNG.integers(3)
        if norm == 0:
            Z = (X - X.min(0))/np.where(np.ptp(X, 0) > 0, np.ptp(X, 0), 1)
        elif norm == 1:
            Z = (pd.DataFrame(X).rank(pct=True)).to_numpy()
        else:
            Z = (X - X.mean(0))/np.where(X.std(0) > 0, X.std(0), 1)
            Z = 1/(1 + np.exp(-Z))
        if RNG.random() < 0.5:
            s = Z @ w
        else:
            s = np.exp(np.log(np.clip(Z, 1e-3, None)) @ w)
        ranks[k] = (-s).argsort().argsort() + 1
    out = ind[['municipality']].copy()
    out['rank_median'] = np.median(ranks, 0)
    out['rank_p05'] = np.percentile(ranks, 5, 0); out['rank_p95'] = np.percentile(ranks, 95, 0)
    out['p_top3'] = (ranks <= 3).mean(0)
    return out.sort_values('rank_median'), ranks


def main():
    ch = Channel()
    tl = timing(ch)
    inv = pd.read_parquet(DER/'harmonised_inventory.parquet')
    st = pd.read_parquet(DER/'corridor_buildings.parquet', columns=['id', 'reg_building_id', 'n_within_100m'])
    inv = inv.merge(st, on='id', how='left')
    inv['municipality'] = canon(inv.municipality)
    inv['destroyed'] = inv.max_level == 3
    inv['any_damage'] = inv.max_level >= 1
    sc, lt_m = lead_times(tl, inv)
    # Danger zone: damage-calibrated height envelope applied to the whole corridor (<=500 m from channel)
    env = pd.read_csv(TAB/'terrain_envelope_by_reach.csv')
    inv['h_danger_m'], hprof = danger_height(inv.chainage_km, env)
    inv['h_outer_m'], hprof_o = danger_height(inv.chainage_km, env, 'outer')
    hprof.merge(hprof_o.rename(columns={'h_m': 'h_outer_m'}), on='chainage_km').to_csv(
        TAB/'danger_height_profile.csv', index=False, float_format='%.4g')
    inv['in_danger_zone'] = (inv.rem_m < inv.h_danger_m) & (inv.dist_channel_m <= 500)
    inv['in_outer_zone'] = (inv.rem_m < inv.h_outer_m) & (inv.dist_channel_m <= 500)
    # population in danger zone (WorldPop 2026 at 30 m)
    with rasterio.open(DER/'rem_utm30.tif') as s:
        rem = s.read(1); T = s.transform
    H, W = rem.shape
    xs = T.c + (np.arange(W) + .5)*T.a; ys = T.f + (np.arange(H) + .5)*T.e
    from scipy.ndimage import distance_transform_edt
    rows_, cols_ = rasterio.transform.rowcol(T, ch.xy[:, 0], ch.xy[:, 1])
    mask = np.ones((H, W), bool); mask[rows_, cols_] = False
    chain = np.full((H, W), np.nan, 'float32'); chain[rows_, cols_] = ch.chain/1000
    dist, (ir, ic) = distance_transform_edt(mask, sampling=30.0, return_indices=True)
    chain = chain[ir, ic]
    hgrid, _ = danger_height(chain, env)
    hgrid_o, _ = danger_height(chain, env, 'outer')
    from analysis_exposure import to_grid, municipality_raster
    pop = to_grid(ROOT/'sources_ext'/'worldpop'/'worldpop_2026_corridor.tif', T, (H, W), 'pop')
    dz = (rem < hgrid) & (dist <= 500) & (chain <= 207)
    dzo = (rem < hgrid_o) & (dist <= 500) & (chain <= 207)
    mr, names = municipality_raster(T, (H, W))
    pop_dz = pd.DataFrame(dict(municipality=[names.get(i, 'Unassigned') for i in mr[dz]], pop=pop[dz]))
    pop_dz['municipality'] = canon(pop_dz.municipality)
    pop_dz = pop_dz.groupby('municipality').pop.sum().rename('pop2026_danger_zone').reset_index()
    # Buildings in the danger zone (all stock) and surviving (not destroyed) stock in the zone
    bdz = inv[inv.in_danger_zone].groupby('municipality').agg(buildings_danger_zone=('id', 'size'),
                                                             surviving_in_danger_zone=('destroyed', lambda v: int((~v).sum()))).reset_index()
    bdo = inv[inv.in_outer_zone].groupby('municipality').agg(buildings_outer_zone=('id', 'size'),
                                                            surviving_in_outer_zone=('destroyed', lambda v: int((~v).sum()))).reset_index()
    bdz = bdz.merge(bdo, on='municipality', how='outer')
    # Satellite inventory vs RDNA, and envelope-based screening in reaches without satellite grading
    sat = inv.groupby('municipality').agg(sat_damaged=('any_damage', 'sum'), sat_destroyed=('destroyed', 'sum'),
                                          chainage_median_km=('chainage_km', 'median')).reset_index()
    ind = RDNA.merge(sat, on='municipality', how='outer').merge(bdz, on='municipality', how='left').merge(pop_dz, on='municipality', how='left')
    ind = ind.merge(lt_m[['municipality', 'lead_seismic_min', 'lead_sms_min']], on='municipality', how='left')
    aff = pd.read_csv(TAB/'affected_population.csv').rename(columns={'adm3_name': 'municipality'})
    aff['municipality'] = canon(aff.municipality)
    ind = ind.merge(aff[['municipality', 'people_affected']], on='municipality', how='left')
    dres, dbym = debris_mc(inv)
    ind = ind.merge(dbym, on='municipality', how='left')
    ind = ind[(ind.rdna_affected_buildings.fillna(0) > 0) | (ind.sat_damaged.fillna(0) > 0)]
    ind = ind[ind.municipality != 'Unassigned']
    ind.to_csv(TAB/'municipal_indicators.csv', index=False, float_format='%.6g')
    cols = ['sat_destroyed', 'rdna_affected_buildings', 'people_affected', 'debris_t_central', 'pop2026_danger_zone',
            'buildings_danger_zone']
    rank, ranks = composite_rank(ind.reset_index(drop=True), cols)
    rank.to_csv(TAB/'municipal_rank_uncertainty.csv', index=False, float_format='%.4g')
    np.save(DER/'municipal_rank_draws.npy', ranks)
    r = ind[['municipality', 'rdna_affected_buildings', 'sat_damaged', 'buildings_danger_zone']].dropna()
    res = dict(timeline=tl.to_dict(orient='records'), lead=sc.to_dict(orient='records'), debris=dres,
               danger_zone_buildings=int(inv.in_danger_zone.sum()),
               danger_zone_surviving=int((inv.in_danger_zone & ~inv.destroyed).sum()),
               danger_zone_pop2026=float(pop[dz].sum()),
               danger_zone_destroyed_captured_pct=float(100*inv[inv.destroyed].in_danger_zone.mean()),
               outer_zone_buildings=int(inv.in_outer_zone.sum()),
               outer_zone_surviving=int((inv.in_outer_zone & ~inv.destroyed).sum()),
               outer_zone_pop2026=float(pop[dzo].sum()),
               outer_zone_destroyed_captured_pct=float(100*inv[inv.destroyed].in_outer_zone.mean()),
               spearman_rdna_vs_sat=float(r.rdna_affected_buildings.corr(r.sat_damaged, method='spearman')),
               spearman_rdna_vs_dangerzone=float(r.rdna_affected_buildings.corr(r.buildings_danger_zone, method='spearman')))
    (DER/'impacts_results.json').write_text(json.dumps(res, indent=1, default=float), encoding='utf-8')
    print(tl.round(2).to_string()); print(sc.round(1).to_string()); print(lt_m.round(1).to_string())
    print(ind.round(1).to_string()); print(rank.round(2).to_string())
    print(json.dumps({k: v for k, v in res.items() if k not in ('timeline', 'lead')}, indent=1, default=float))


if __name__ == '__main__':
    main()
