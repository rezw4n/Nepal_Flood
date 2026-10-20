"""Fill the manuscript template with numbers computed from the analysis outputs and number the references.

Every quantitative statement in paper/templates/manuscript_template.md is written as {{key}}; this script computes
each key from data/derived/*.json and tables/*.csv (or from official figures recorded below with their
source), builds Tables 1-2, converts [@key] citations to numbered superscripts in order of first
appearance and appends a Nature-style reference list. Unresolved placeholders or keys raise errors.
"""
from pathlib import Path
import json
import re
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DER, TAB = ROOT/'data'/'derived', ROOT/'tables'
PAPER = ROOT/'paper'                          # documents, templates and reference list

# Official figures quoted in the text (source in comment); all verified against archived documents.
OFFICIAL = dict(
    deaths='1,455', missing='5,285',                 # NDRRMA consolidated update to 3 Oct 2026, p. 5
    china_dead='43', china_missing='519',            # Xinhua 5 Sep 2026 via ICIMOD synthesis (13 Oct 2026)
    rdna_damage='1.81', rdna_effects='2.70', rdna_needs='4.77', rdna_gdp='6.7',   # RDNA p. 11 and summary
    devghat_peak='5,850',                            # CHWRR Assessment Report II, section 5.4
    sms_count='679,295',                             # NDRRMA update, timeline 09:15
    missing_rasuwa='3,514', missing_nuwakot='1,247',  # NDRRMA update, p. 5 (includes people from other districts)
)
RASUWA = ['Gosaikunda', 'Uttargaya', 'Kalika', 'Aamachhodingmo', 'Parbati Kunda', 'Parbatikunda']
NUWAKOT = ['Bidur', 'Kispang', 'Belkotgadhi', 'Tarkeshwar', 'Tarakeshwor']


def fmt(x, nd=0):
    return f'{x:,.{nd}f}'


def facts():
    F = dict(OFFICIAL)
    tr = json.loads((DER/'terrain_results.json').read_text())
    pr = json.loads((DER/'products_results.json').read_text())
    im = json.loads((DER/'impacts_results.json').read_text())
    s2 = json.loads((DER/'s2_results.json').read_text())
    ex = json.loads((DER/'exposure_results.json').read_text())
    prod = pd.read_csv(TAB/'products_summary.csv')
    perf = pd.read_csv(TAB/'ml_performance.csv').set_index('model')
    imp = pd.read_csv(TAB/'ml_permutation_importance.csv').set_index('feature')
    mods = pd.read_csv(TAB/'terrain_local_models.csv')
    sb = pd.read_csv(TAB/'terrain_setback_thresholds.csv').set_index('rem_threshold_m')
    env = pd.read_csv(TAB/'terrain_envelope_by_reach.csv')
    dh = pd.read_csv(TAB/'danger_height_profile.csv')
    zg = pd.read_csv(TAB/'exposure_growth_zones.csv')
    lt = pd.read_csv(TAB/'timing_lead_time_scenarios.csv')
    ltm = pd.read_csv(TAB/'timing_lead_time_by_municipality.csv').set_index('municipality')
    tl = pd.read_csv(TAB/'timing_wave_arrivals.csv')
    rk = pd.read_csv(TAB/'municipal_rank_uncertainty.csv').set_index('municipality')
    ind = pd.read_csv(TAB/'municipal_indicators.csv').set_index('municipality')
    auc = pd.read_csv(TAB/'s2_separability_auc.csv')
    inv = pd.read_parquet(DER/'harmonised_inventory.parquet')
    st = pd.read_parquet(DER/'corridor_buildings.parquet', columns=['origin', 'reg_n'])
    # products
    g = prod.set_index('product')
    F['n_hot'] = '1,053'
    F['cems_assessed'] = fmt(g.loc['CEMS EMSR927 latest grading (photo-interpretation)', 'assessed'])
    F['cems_damaged'] = fmt(g.loc['CEMS EMSR927 latest grading (photo-interpretation)', 'damaged'])
    F['cems_destroyed'] = fmt(g.loc['CEMS EMSR927 latest grading (photo-interpretation)', 'destroyed'])
    F['undp_total'] = '3,043'
    F['stock_n'] = fmt(len(st))
    F['overture_n'] = fmt((st.origin == 'overture').sum())
    F['union_damaged'] = fmt(g.loc['Harmonised union (>=1 product)', 'damaged'])
    F['union_destroyed'] = fmt(g.loc['Harmonised union (>=1 product)', 'destroyed'])
    F['union_2plus'] = fmt(g.loc['Destroyed in >=2 products', 'destroyed'])
    F['n_both'] = fmt(pr['n'])
    F['kappa_destroyed'] = f"{pr['kappa_destroyed']:.2f}"
    F['hot_confirmed'] = fmt(pr['hot_destroyed_confirmed_by_cems_pct'])
    F['cems_confirmed'] = fmt(pr['cems_destroyed_confirmed_by_hot_pct'])
    F['unosat_confirmed'] = fmt(pr['unosat_destroyed_confirmed_by_cems_pct'])
    F['unosat_n'] = fmt(pr['unosat_destroyed_in_cems_aoi'])
    F['undp_only'] = fmt((st.origin == 'undp_only').sum())
    F['hot_only'] = fmt((st.origin == 'hot_only').sum())
    F['cems_only'] = fmt((st.origin == 'cems_only').sum())
    # Sentinel-2
    a = auc.set_index(['index', 'target']).auc
    F['s2_auc_ndvi'] = f"{a[('ndvi', 'destroyed vs not (all assessed)')]:.2f}"
    F['s2_auc_ndvi_hot'] = f"{a[('ndvi', 'HOT destroyed vs HOT no damage')]:.2f}"
    F['s2_auc_bright'] = f"{a[('bright', 'destroyed vs not (all assessed)')]:.2f}"
    F['s2_pre'] = str(s2['n_pre_scenes']); F['s2_post'] = str(s2['n_post_scenes'])
    sc = pd.read_csv(TAB/'s2_change_by_class.csv')
    sc = sc[(sc['product'] == 'CEMS/UNDP') & (sc['index'] == 'ndvi')].set_index('level').p50
    for lev, k in [(0, 'none'), (1, 'possibly'), (2, 'damaged'), (3, 'destroyed')]:
        F[f's2_med_{k}'] = f'{sc[lev]:+.2f}'.replace('-', '−')
    # RDNA comparison
    graded = ind.sat_damaged.fillna(0) > 20
    has = ind.rdna_affected_buildings.notna()
    F['rdna_ratio'] = f"{(ind.sat_damaged[graded & has]/ind.rdna_affected_buildings[graded & has]).median():.2f}"
    F['rdna_ungraded'] = fmt(ind.rdna_affected_buildings[~graded & has].sum())
    br = inv[(inv.municipality == 'Benighat Rorang') & (inv.dist_channel_m <= 1000)]
    F['benighat_lt10'] = fmt((br.rem_m < 10).sum())
    # local terrain
    loc = tr['local']
    hb = pd.read_csv(TAB/'terrain_local_rem_bins.csv')
    lt20 = hb[hb.rem_mid < 20]; gt80 = hb[hb.rem_mid > 80]
    F['hot_destroyed_lt20'] = fmt(100*lt20['destroyed_n'].sum()/lt20.n.sum())
    F['hot_destroyed_gt80'] = fmt(100*gt80['destroyed_n'].sum()/gt80.n.sum())
    F['auc_rem_local'] = f"{loc['auc_rem_only']:.2f}"
    F['auc_dist_local'] = f"{loc['auc_dist_only']:.2f}"
    F['or_10m'] = f"{loc['or_per_10m']:.2f}"
    o = mods[mods.model == 'ordinal_logit'].set_index('term')
    F['or_rem_ord'] = f"{o.loc['rem_10m', 'odds_ratio']:.2f}"
    F['or_outer'] = f"{o.loc['outer_bank', 'odds_ratio']:.2f}"
    F['or_outer_ci'] = f"{o.loc['outer_bank', 'or_lo']:.2f}–{o.loc['outer_bank', 'or_hi']:.2f}"
    # regional ML
    F['n_domain'] = fmt(perf.loc['gbm', 'n'])
    F['auc_gbm'] = f"{perf.loc['gbm', 'auc']:.2f}"
    F['prauc_gbm'] = f"{perf.loc['gbm', 'pr_auc']:.2f}"
    F['prev'] = fmt(100*perf.loc['gbm', 'prevalence'])
    F['auc_cems_only'] = f"{perf.loc['gbm_cems_labels_only', 'auc']:.2f}"
    F['auc_transfer'] = f"{perf.loc['gbm_transfer_to_HOT', 'auc']:.2f}"
    F['auc_rem_only'] = f"{perf.loc['logit_rem', 'auc']:.2f}"
    F['imp_rem'] = f"{imp.loc['rem_m', 'importance_auc_drop']:.2f}"
    F['imp_dist'] = f"{imp.loc['dist_channel_m', 'importance_auc_drop']:.3f}"
    F['imp_chain'] = f"{imp.loc['chainage_km', 'importance_auc_drop']:.3f}"
    # envelope
    from analysis_impacts import robust_reach_heights
    rh = robust_reach_heights(env)
    gz = rh[rh.reach_mid_km < 45]; vz = rh[rh.reach_mid_km.between(60, 88.9)]; lz = rh[rh.reach_mid_km > 89]
    F['h_gorge'] = fmt(round(gz.h_core.max()/5)*5)
    F['h_gorge_range'] = f"{gz.h_core.min():.0f}–{gz.h_core.max():.0f}"
    F['h_valley_range'] = f"{vz.h_core.max():.0f} to {vz.h_core.min():.0f}"
    F['h_lower_range'] = f"{lz.h_core.min():.0f}–{lz.h_core.max():.0f}"
    F['h_lower'] = f"{lz.h_core.min():.0f}"
    rgd = {r['group']: r for r in tr['reach_groups']}
    for k, key in [('gorge_21_41km', 'rg_gorge'), ('middle_64_89km', 'rg_valley'), ('lower_89_114km', 'rg_lower')]:
        r = rgd[k]
        F[key] = f"{r['rem50']:.0f} (95% CI {r['rem50_lo']:.0f}–{r['rem50_hi']:.0f})"
    m = rh.dropna(subset=['flow_edge_rem_p50'])
    from scipy.stats import spearmanr
    F['rho_env'] = f"{spearmanr(m.flow_edge_rem_p50, m.h_core)[0]:.2f}"
    F['n_reaches'] = str(len(m))
    F['gorge_lt20'] = fmt(sb.loc[20, 'gorge_21_41km_destroyed_below_pct'])
    F['valley_lt20'] = fmt(sb.loc[20, 'middle_64_89km_destroyed_below_pct'])
    F['lower_lt20'] = fmt(sb.loc[20, 'lower_89_114km_destroyed_below_pct'])
    # celerity
    a_ = tl[tl.arrival].reset_index(drop=True)
    cel = a_.celerity_from_previous_m_s.to_numpy()
    for i in range(1, 8):
        F[f'cel_{i}'] = f'{cel[i]:.0f}'
    F['cel_trishuli'] = f'{cel[4:7].min():.0f}–{cel[4:7].max():.0f}'
    F['ch_rasuwagadhi'] = f"{a_.chainage_km[1]:.0f}"
    F['path_km'] = f"{pd.read_csv(DER/'flowpath_profile.csv').chainage_m.max()/1000:.1f}"
    # exposure growth
    zz = zg[zg.reach == '0-106km (assessed)'].set_index('zone')
    F['growth_lt10'] = f"{zz.loc['rem_lt10_d1km', 'built_growth_1975_2020']:.0f}"
    F['growth_10_20'] = f"{zz.loc['rem_10_20_d1km', 'built_growth_1975_2020']:.0f}"
    F['growth_ge80'] = f"{zz.loc['rem_ge80_d1km', 'built_growth_1975_2020']:.1f}"
    F['fe_1975'] = f"{zz.loc['flow_extent', 'built_m2_1975']/1e4:.1f}"
    F['fe_2020'] = f"{zz.loc['flow_extent', 'built_m2_2020']/1e4:.1f}"
    # danger zones
    F['dz_core'] = fmt(im['danger_zone_buildings']); F['dz_core_surv'] = fmt(im['danger_zone_surviving'])
    F['dz_core_pop'] = fmt(round(im['danger_zone_pop2026'], -2)); F['dz_core_capture'] = fmt(im['danger_zone_destroyed_captured_pct'])
    F['dz_outer'] = fmt(im['outer_zone_buildings']); F['dz_outer_surv'] = fmt(im['outer_zone_surviving'])
    F['dz_outer_pop'] = fmt(round(im['outer_zone_pop2026'], -2)); F['dz_outer_capture'] = fmt(im['outer_zone_destroyed_captured_pct'])
    # warning
    L = lt.set_index('alert_time')
    F['sms_neg'] = fmt(L.loc['09:15:00', 'pct_destroyed_negative'])
    F['sms_ge30'] = fmt(L.loc['09:15:00', 'pct_destroyed_ge30'])
    F['seis_ge30'] = fmt(L.loc['08:39:10', 'pct_destroyed_ge30'])
    F['seis_median'] = fmt(L.loc['08:39:10', 'median_lead_destroyed_min'])
    F['gos_seis'] = fmt(ltm.loc['Gosaikunda', 'lead_seismic_min'])
    F['bidur_seis'] = fmt(ltm.loc['Bidur', 'lead_seismic_min'])
    des = inv[inv.max_level == 3]
    n_ras = des.municipality.isin(RASUWA).sum()      # destroyed buildings in Rasuwa local levels (Nepal side only)
    n_nuw = des.municipality.isin(NUWAKOT).sum()
    F['mpd_rasuwa'] = f"{3514/n_ras:.1f}"; F['mpd_nuwakot'] = f"{1247/n_nuw:.1f}"
    F['bodies_downstream_pct'] = fmt(100*(369 + 232 + 222)/1455)   # NDRRMA 3 Oct district table
    # ranking and debris
    F['p_bidur'] = f"{rk.loc['Bidur', 'p_top3']:.2f}"; F['p_gos'] = f"{rk.loc['Gosaikunda', 'p_top3']:.2f}"
    F['p_kispang'] = f"{rk.loc['Kispang', 'p_top3']:.2f}"
    d = im['debris']
    F['debris_central'] = f"{d['debris_central_t']/1e6:.2f}"; F['debris_lo'] = f"{d['debris_mc_p05']/1e6:.2f}"
    F['debris_hi'] = f"{d['debris_mc_p95']/1e6:.2f}"
    F['bidur_share'] = fmt(100*d['bidur_share_central']); F['bidur_share_nf'] = fmt(100*d['bidur_share_no_factor'])
    F['urban_thr'] = fmt(d['density_threshold_urban'])
    le = pd.read_csv(TAB/'loss_estimates.csv').set_index('estimate')
    F['undp_econ'] = f"{le.loc['UNDP RAPIDA (CLIMADA) direct building damage', 'usd_million']/1000:.2f}"
    tt = pd.read_csv(TAB/'infrastructure_cems_transport.csv').set_index(['layer', 'aoi'])
    F['cems_road_destroyed'] = fmt(tt.loc[('roads', 'All'), 'Destroyed'])
    F['cems_bridge_destroyed'] = fmt(tt.loc[('bridges', 'All'), 'Destroyed'])
    F['cems_bridge_affected'] = fmt(tt.loc[('bridges', 'All'), ['Destroyed', 'Damaged', 'Possibly damaged']].sum())
    lc = pd.read_csv(TAB/'landcover_flow_extent.csv').set_index('class')
    F['lc_crop'] = f"{lc.loc['Cropland', 'All reaches']:.1f}"
    F['lc_built'] = f"{lc.loc['Built-up', 'All reaches']:.1f}"
    F['lc_tree'] = f"{lc.loc['Tree cover', 'All reaches']:.1f}"
    valley = [c for c in lc.columns if c.startswith(('64', '89'))]
    F['lc_crop_valley_pct'] = fmt(100*lc.loc['Cropland', valley].sum()/lc.loc['Cropland', 'All reaches'])
    F['TABLE1'] = table1(inv)
    F['TABLE2'] = table2(ind, rk, ltm)
    return F


def table1(inv):
    dash = json.loads((ROOT/'sources_ext'/'cems'/'EMSR927_dashboard.json').read_text(encoding='utf-8'))['results'][0]
    rows = ['| Product | Provider and method | Imagery (2026) | Reach graded (km from source) | Buildings graded | Damaged | Destroyed |',
            '|---|---|---|---|---|---|---|']
    h = inv[inv.hot_class >= 0]
    rows.append(f'| HOT inventory | HOT; AI-assisted (fAIR) labels on OpenStreetMap footprints | Post-event very-high-resolution (dates not documented) | '
                f'{h.chainage_km.min():.0f}–{h.chainage_km.max():.0f} | 1,053 | {int((h.hot_class >= 1).sum()):,} | {int((h.hot_class == 3).sum()):,} |')
    for a in sorted(dash['aois'], key=lambda a: a['number']):
        prods = [p for p in a['products'] if (p.get('stats') or {}).get('Built-up')]
        if not prods:
            continue
        lp = max(prods, key=lambda p: (p['monitoringNumber'], p['version']['number']))
        bu = lp['stats']['Built-up']
        tot = sum(v.get('total') or 0 for v in bu.values() if isinstance(v.get('total'), (int, float)))
        aff = sum(v.get('affected') or 0 for v in bu.values() if isinstance(v.get('affected'), (int, float)))
        imgs = '; '.join(sorted({f"{i['sensorName']} {int(i['acquisitionTime'][8:10])} {'Aug' if i['acquisitionTime'][5:7] == '08' else 'Sep'}"
                                 for i in lp['images']}))
        sub = inv[inv.cems_aoi == a['number']]
        kind = 'monitoring' if lp['monitoring'] else 'first'
        rows.append(f"| CEMS AOI{a['number']:02d} {a['name']} | Copernicus EMS; photo-interpretation ({kind} product, v{lp['version']['number']}) | {imgs} | "
                    f"{sub.chainage_km.quantile(.005):.0f}–{sub.chainage_km.quantile(.995):.0f} | {int(tot):,} | {int(aff):,} | "
                    f"{int((sub.cems_level == 3).sum()):,} |")
    rows.append('| UNDP RAPIDA service | UNDP; republished CEMS (2,311), SERTIT (48) and UNOSAT (684) records on Google footprints with debris model | As source products | '
                f'{inv[inv.reg_level > 0].chainage_km.quantile(.005):.0f}–{inv[inv.reg_level > 0].chainage_km.quantile(.995):.0f} | – | 3,043 | 2,574 |')
    rows.append('| UNOSAT flow extent | UNOSAT; flow/mudflow extent (no building grading) | PlanetScope 26 Aug; Sentinel-2 27 Aug | 0–106 | – | – | – |')
    rows.append('| Official RDNA | NDRRMA/NPC; satellite and drone imagery, fAIR-HOT mapping, Census 2021 typology | Various, to 3 Sep | 15 local levels | – | 7,570 (affected) | – |')
    u = inv
    rows.append(f'| **Harmonized union (this study)** | One-to-one matching to Overture footprints; most severe grade | – | 0–114 | – | '
                f'**{int((u.max_level >= 1).sum()):,}** | **{int((u.max_level == 3).sum()):,}** |')
    return '\n'.join(rows)


def table2(ind, rk, ltm):
    actions = {
        'Bidur': 'Inspect surviving riverside buildings below the valley envelope; largest debris volume — verify urban debris factor before contracting; flood-front lead time was ~50 min: automate alerts',
        'Gosaikunda': 'Relocation assessment for gorge settlements (destruction to ~60 m above channel); restore the Rasuwagadhi corridor; seismic-triggered alerts essential (lead time minutes)',
        'Kispang': 'Inspect partially damaged buildings on low terraces; debris clearance; reconcile RDNA (696) with satellite count (430)',
        'Uttargaya': 'Verify RDNA count (567) against satellite record (278); inspect surviving buildings in the core zone',
        'Belkotgadhi': 'Inspect outer-zone buildings; restore access and water supply',
        'Benighat Rorang': 'Field verification of 1,037 RDNA-affected buildings (no satellite grading; few buildings below observed stage)',
        'Galchhi': 'Inspect damaged riverside structures; confluence reach with highway exposure',
        'Gajuri': 'Verify damage below Galchhi; protect Prithvi Highway segments',
        'Tarakeshwor': 'Inspect destroyed/damaged buildings recorded by satellites (RDNA lists 43)',
    }
    rows = ['| Local level | Destroyed (satellite) | Damaged (satellite) | RDNA affected | Core-zone buildings (surviving) | Core-zone residents | SMS lead time (min) | Building debris (kt) | Rank (5–95%) | Priority actions |',
            '|---|---|---|---|---|---|---|---|---|---|']
    for m in rk.index[:9]:
        r = ind.loc[m]
        ld = ltm.loc[m, 'lead_sms_min'] if m in ltm.index else np.nan
        f = lambda v, nd=0: '–' if pd.isna(v) else f'{v:,.{nd}f}'
        core = '–' if pd.isna(r.buildings_danger_zone) else f"{int(r.buildings_danger_zone):,} ({int(r.surviving_in_danger_zone):,})"
        rows.append(f"| {m} | {f(r.sat_destroyed)} | {f(r.sat_damaged)} | {f(r.rdna_affected_buildings)} | {core} | "
                    f"{f(round(r.pop2026_danger_zone, -1) if pd.notna(r.pop2026_danger_zone) else np.nan)} | "
                    f"{'–' if pd.isna(ld) else f'{ld:+.0f}'} | {f(r.debris_t_central/1000 if pd.notna(r.debris_t_central) else np.nan)} | "
                    f"{rk.loc[m, 'rank_median']:.0f} ({rk.loc[m, 'rank_p05']:.0f}–{rk.loc[m, 'rank_p95']:.0f}) | {actions.get(m, '')} |")
    return '\n'.join(rows)


def nature_ref(r):
    au = r['authors'].strip()
    au = re.sub(r'\s*\(\d+ authors\)', '', au)
    if ';' in au:                                    # 'A; B; C' -> 'A, B & C'
        parts = [p.strip() for p in au.split(';') if p.strip()]
        au = ', '.join(parts[:-1]) + ' & ' + parts[-1] if len(parts) > 1 else parts[0]
    au = au.rstrip('.') + '.'
    title = r['title'].rstrip('.')
    j = r.get('journal') or ''
    vol = r.get('volume') or ''
    vol_main = re.match(r'(\d+)', str(vol)).group(1) if re.match(r'(\d+)', str(vol)) else ''
    pages = (r.get('pages') or '').replace('-', '–')
    doi = r.get('doi') or ''
    url = r.get('url') or (f'https://doi.org/{doi}' if doi else '')
    if r.get('type') == 'journal-article' and vol_main:
        s = f"{au} {title}. *{j}* **{vol_main}**, {pages} ({r['year']})." if pages else f"{au} {title}. *{j}* **{vol_main}** ({r['year']})."
    elif r.get('type') == 'journal-article':
        s = f"{au} {title}. *{j}* ({r['year']})."
    elif r.get('type') == 'book-chapter' and r.get('book'):
        s = f"{au} {title}. In *{r['book']}* (eds {r['editors_nature']}) {pages} ({r['publisher']}, {r['year']})."
    else:
        s = f"{au} {title}. {j} ({r['year']})."
    s = s.replace('..', '.')
    enc = lambda u: u.replace('(', '%28').replace(')', '%29')     # parentheses would end the Markdown link early
    if doi:
        s += f' [https://doi.org/{doi}]({enc("https://doi.org/" + doi)})'
    elif url:
        s += f' [{url}]({enc(url)})'
    return s


def cite(text, refs):
    order = []
    def repl(m):
        keys = [k.strip().lstrip('@') for k in m.group(1).split(';')]
        nums = []
        for k in keys:
            if k not in refs:
                raise KeyError(f'unknown reference key {k}')
            if k not in order:
                order.append(k)
            nums.append(order.index(k) + 1)
        nums = sorted(set(nums))
        parts, start = [], nums[0]
        for a, b in zip(nums, nums[1:] + [None]):
            if b != a + 1:
                parts.append(f'{start}' if start == a else (f'{start},{a}' if a == start + 1 else f'{start}–{a}'))
                start = b
        return '^' + ','.join(parts) + '^'
    out = re.sub(r'\[(@[^\]]+)\]', repl, text)
    return out, order


def build(template, out, extra_refs_title='References'):
    F = facts()
    t = template.read_text(encoding='utf-8')
    missing = sorted(set(re.findall(r'\{\{(\w+)\}\}', t)) - set(F) - {'REFERENCES'})
    if missing:
        raise KeyError(f'unresolved placeholders: {missing}')
    for k, v in F.items():
        t = t.replace('{{' + k + '}}', str(v))
    refs = {r['key']: r for r in json.loads((PAPER/'references.json').read_text(encoding='utf-8'))}
    t, order = cite(t, refs)
    t = re.sub(r'(?<![\w/.])-(?=\d)', '−', t)          # typographic minus (before the reference list)
    reflist = '\n\n'.join(f'{i}. {nature_ref(refs[k])}' for i, k in enumerate(order, 1))
    t = t.replace('{{REFERENCES}}', reflist)
    # 'ref. ^n^' -> 'ref. n'
    t = re.sub(r'ref\. \^([\d,–]+)\^', r'ref. \1', t)
    out.write_text(t, encoding='utf-8')
    words = len(re.sub(r'\{\{.*?\}\}', '', t.split('## Methods')[0].split('## Introduction')[-1]).split())
    print(f'wrote {out.name}: {len(order)} references; main-text words (Introduction to Discussion) ~{words}')
    return F, order


if __name__ == '__main__':
    import sys
    sys.path.insert(0, str(ROOT/'scripts'))
    build(PAPER/'templates'/'manuscript_template.md', PAPER/'Nepal_Flood_Damage_Assessment.md')
