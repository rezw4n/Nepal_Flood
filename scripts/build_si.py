"""Build Supplementary_Information.md from the analysis tables and results (numbers are never typed by hand)."""
from pathlib import Path
import json
import re
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_manuscript_v2 import facts, cite, nature_ref, ROOT, DER, TAB          # noqa: E402
from analysis_impacts import robust_reach_heights, STAGE_RISE                    # noqa: E402

CANON = {'Galchi': 'Galchhi', 'Tarkeshwar': 'Tarakeshwor', 'Parbati Kunda': 'Parbatikunda',
         'Sahid Lakhan': 'Shahid Lakhan', 'Unassigned': 'Outside Nepal (Gyirong, China)'}


def n0(v):
    return '–' if v is None or (isinstance(v, float) and np.isnan(v)) else f'{int(round(v)):,}'


def f1(v, nd=1):
    return '–' if v is None or (isinstance(v, float) and np.isnan(v)) else f'{v:,.{nd}f}'


WORDS = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def words(n):
    return WORDS[n] if 0 <= n < 10 else f'{n:,}'


def minus(text):
    """Typographic minus for negative numbers (not hyphens in dates, ranges or identifiers)."""
    return re.sub(r'(?<![\w/.])-(?=\d)', '−', text)


def table(header, rows):
    out = ['| ' + ' | '.join(header) + ' |', '|' + '|'.join(['---']*len(header)) + '|']
    out += ['| ' + ' | '.join(str(c).replace('|', '/') for c in r) + ' |' for r in rows]
    return '\n'.join(out)


def link(url, text=None):
    text = text or re.sub(r'^https?://', '', url).split('/')[0]
    return f'[{text}]({url})'


# ----------------------------------------------------------------------------------------------- tables
def t_sources(s2log):
    pre = sorted({x['datetime'][:10] for x in s2log['pre']}); post = sorted({x['datetime'][:10] for x in s2log['post']})
    rows = [
        ['HOT building-damage inventory and analysed area', 'Humanitarian OpenStreetMap Team; AI-assisted (fAIR) labels on OpenStreetMap footprints',
         'Post-event imagery; acquisition times not published', '1,053 footprints; 13.9 km^2^ analysed area',
         'Damage labels (local models, harmonization)', link('https://production-raw-data-api.s3.amazonaws.com/ISO3/NPL/buildings/hot_flood_npl_buildings_damage.geojson', 'HOT raw-data API') + '; terms unconfirmed'],
        ['CEMS EMSR927 grading', 'Copernicus EMS Rapid Mapping; AOI01, AOI02 first products; AOI03, AOI05 monitoring products (MONIT01)',
         'Imagery 27 Aug–5 Sep 2026', 'Building points; road lines; bridge points; not-analysed areas',
         'Damage labels, graded domain, road and bridge damage', link('https://rapidmapping.emergency.copernicus.eu/EMSR927', 'rapidmapping.emergency.copernicus.eu') + '; © European Union'],
        ['UNDP RAPIDA building debris layer', 'UNDP; records attributed to CEMS (2,311), SERTIT (48), UNOSAT (684)',
         'StoryMap of 27 Aug, updated 2 Sep 2026', '3,043 footprints with floors, site type, debris',
         'Damage labels, debris model', link('https://geosmarthosting.undp.org/arcgis/rest/services/Hosted/NPL_debris/FeatureServer/1', 'UNDP NPL_debris service') + '; terms unconfirmed'],
        ['UNDP RAPIDA economic estimate and affected population', 'UNDP (CLIMADA-based)', 'Reference date 31 Aug 2026',
         'Local-level US$ and people', 'Monetary comparison; affected-people indicator',
         link('https://geosmarthosting.undp.org/arcgis/rest/services/Hosted/NPL_Flooding_Economic_Estimate__20260826/FeatureServer/0', 'UNDP economic service') + '; terms unconfirmed'],
        ['UNOSAT flow extent FL20260826NPL', 'UNITAR/UNOSAT via UNESCO IHP-WINS', 'Imagery 26–27 Aug 2026',
         '37.35 km^2^ polygon in a 363 km^2^ analysed area', 'Flow-edge heights, exposure',
         link('https://ihp-wins.unesco.org/dataset/054c3516-e2b8-49a4-a256-1de4b7431ec6', 'IHP-WINS dataset') + '; redistribution terms unconfirmed'],
        ['NDRRMA situation reports and consolidated update', 'Government of Nepal', '26 Aug–3 Oct 2026',
         'Deaths, missing, warning timeline', 'Casualties, alert times', link('https://ndrrma.gov.np/mediafiles/publications/Bhotekoshi-Trishuli_Flood_Update_From_August_26_2026_to_October_3_2026.pdf', 'ndrrma.gov.np')],
        ['Rapid Damage and Needs Assessment (RDNA)', 'NDRRMA and National Planning Commission', '10 Sep 2026',
         'Affected buildings by local level; sector damage and needs', 'Comparison, ranking, monetary scope',
         link('https://ndrrma.gov.np/mediafiles/rasuwa/Rapid_Damage_and_Needs_Assessment_RDNA_Rasuwa-Bhotekoshi_Flood_2026.pdf', 'ndrrma.gov.np')],
        ['Propagation timeline and gauge records', 'Centre of Hydrology and Water Resources Research (CHWRR)', '26 Aug 2026',
         'Gauge-loss and threshold times; stage', 'Wave timing, stage rises', link('https://giwmscdnone.gov.np/media/pdf_upload/1_Situation_Report_Bhotekoshi%20Flood_2026_CHWRR_hnmns6o.pdf', 'giwmscdnone.gov.np')],
        ['Rapid Hazard Assessment NP3', 'HiRISK', '28 Aug 2026', 'Source coordinates and process interpretation',
         'Start of the traced flow path', link('https://hirisk.org/wp-content/uploads/2026/08/RHA_NP3_RasuwaFlood-1.pdf', 'hirisk.org')],
        ['Copernicus GLO-30 DEM', 'ESA/Airbus; tiles N27–N28, E084–E085', 'Data acquired 2011–2015', '30 m',
         'Flow path, height above channel, slope, transects', link('https://copernicus-dem-30m.s3.amazonaws.com/', 'AWS open data') + '; Copernicus DEM licence'],
        ['Sentinel-2 Level-2A', 'ESA Copernicus; Earth Search v1 cloud-optimized GeoTIFFs',
         f'{pre[0]} to {pre[-1]} ({len(s2log["pre"])} scenes); {post[0]} to {post[-1]} ({len(s2log["post"])} scenes)', '10–20 m',
         'Change indices, true-colour chips', link('https://earth-search.aws.element84.com/v1', 'Earth Search STAC') + '; Copernicus Sentinel data terms'],
        ['Overture Maps release 2026-09-23.1', 'Overture Maps Foundation; buildings, transportation, base (infrastructure, water)',
         'Release 23 Sep 2026', 'Footprints, lines, points', 'Common building stock; infrastructure exposure', 'Amazon S3 (overturemaps-us-west-2); ODbL for OpenStreetMap-derived themes'],
        ['GHS-BUILT-S R2023A', 'European Commission JRC', '1975–2020, 5-year epochs', '100 m', 'Built-up growth by height band',
         link('https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_S_GLOBE_R2023A/', 'JRC open data') + '; CC BY 4.0'],
        ['WorldPop Global2 R2025A constrained counts', 'WorldPop, University of Southampton', '2015, 2020, 2026', '100 m',
         'Population in zones', link('https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/', 'data.worldpop.org') + '; CC BY 4.0'],
        ['geoBoundaries gbOpen NPL ADM3', 'William & Mary geoLab (commit 9469f09)', 'Current release', 'Local-level polygons',
         'Assignment to local levels', link('https://github.com/wmgeolab/geoBoundaries', 'github.com/wmgeolab') + '; CC BY-SA 4.0 (metadata)'],
        ['Seismic onset of the failure', 'NRSC/ISRO; USGS event us7000tbwb', '26 Aug 2026, 08:37:10 NPT', 'Time', 'Time zero of the propagation timeline', 'Published sources [@Roy2026; @USGS2026]'],
        ['Not used: DHM gauge observations', 'Department of Hydrology and Meteorology API', '–', '–', 'Requests returned HTTP 403 (application key required)', link('https://hydrology.gov.np', 'hydrology.gov.np')],
        ['ESA WorldCover 2021 v200', 'European Space Agency', '2021', '10 m', 'Pre-event land cover in the flow extent',
         link('https://esa-worldcover.org', 'esa-worldcover.org') + '; CC BY 4.0'],
        ['Not used: Planet imagery catalogue', 'Planet', '–', '–', 'Inspected for reference only (CC BY-NC 4.0)', '–'],
    ]
    return table(['Dataset', 'Provider and version', 'Date or epoch', 'Resolution or unit', 'Use in this study', 'Access and terms'], rows)


def t_timeline():
    t = pd.read_csv(TAB/'timing_wave_arrivals.csv')
    rows = [[r.place, f1(r.chainage_km), r.time, f1(r.minutes_after_onset), f1(r.celerity_from_previous_m_s),
             'yes' if r.arrival else 'no (threshold crossing)', r.source.replace('CHWRR Table 2', 'CHWRR report, its table 2')]
            for r in t.itertuples()]
    return table(['Place', 'Distance (km)', 'Time (NPT)', 'Minutes after failure', 'Mean celerity from previous (m s^−1^)',
                  'Used as arrival', 'Source'], rows)


def t_municipal():
    h = pd.read_csv(TAB/'harmonised_by_municipality.csv')
    inv = pd.read_parquet(DER/'harmonised_inventory.parquet')
    dm = inv[inv.max_level >= 1].assign(municipality=lambda d: d.municipality.fillna('Unassigned'))
    h['chainage_median_km'] = h.municipality.map(dm.groupby('municipality').chainage_km.median())
    h['municipality'] = h.municipality.replace(CANON)
    h = h.sort_values('chainage_median_km')
    cols = ['damaged', 'destroyed', 'destroyed_2plus', 'damaged_cems', 'residential_cems', 'nonresidential_cems',
            'destroyed_hot', 'destroyed_undp']
    rows = [[r.municipality, f1(r.chainage_median_km)] + [n0(getattr(r, c)) for c in cols] for r in h.itertuples()]
    rows.append(['**Total**', ''] + [f'**{n0(h[c].sum())}**' for c in cols])
    return table(['Local level', 'Median distance (km)', 'Damaged (any grade)', 'Destroyed', 'Destroyed in ≥2 products',
                  'CEMS affected', 'CEMS residential', 'CEMS non-residential', 'HOT destroyed', 'UNDP destroyed'], rows)


def t_products():
    p = pd.read_csv(TAB/'products_summary.csv')
    a = table(['Product', 'Assessed', 'Damaged (any grade)', 'Destroyed'],
              [[r.product.replace('>=', '≥').replace('Harmonised', 'Harmonized'), n0(r.assessed), n0(r.damaged), n0(r.destroyed)]
               for r in p.itertuples()])
    ct = pd.read_csv(TAB/'agreement_hot_cems.csv', index_col=0)
    cols = ['CEMS no record', 'CEMS possibly damaged', 'CEMS damaged', 'CEMS destroyed']
    ct = ct.reindex(index=['HOT no damage', 'HOT minor', 'HOT major', 'HOT destroyed'], columns=cols).fillna(0)
    b = table(['HOT label'] + [c.replace('CEMS ', '').capitalize() for c in cols] + ['Total'],
              [[i] + [n0(v) for v in r] + [n0(r.sum())] for i, r in ct.iterrows()])
    return a, b


def t_s2():
    a = pd.read_csv(TAB/'s2_separability_auc.csv')
    names = {'ndvi': 'NDVI change', 'ndwi': 'NDWI change', 'bright': 'Visible brightness change', 'bsi': 'Bare-soil index change'}
    tg = ['destroyed vs not (all assessed)', 'destroyed vs no record (CEMS AOIs)', 'HOT destroyed vs HOT no damage']
    n = {t: int(a[a.target == t].n.iloc[0]) for t in tg}
    rows = [[names[k]] + [f"{a[(a['index'] == k) & (a.target == t)].auc.iloc[0]:.3f}" for t in tg] for k in names]
    return table(['Index (post minus pre)', f'All graded: destroyed vs other (n = {n[tg[0]]:,})',
                  f'CEMS areas: destroyed vs no record (n = {n[tg[1]]:,})', f'HOT: destroyed vs no damage (n = {n[tg[2]]:,})'], rows)


def t_local(tr):
    b = pd.read_csv(TAB/'terrain_local_rem_bins.csv')
    b.columns = [c.replace('-', '_') for c in b.columns]
    rows = []
    for r in b.itertuples():
        lab = r.rem_bin.replace('(', '').replace(']', '').replace(', ', ' to ')
        rows.append([lab, n0(r.n)] + [f"{getattr(r, c.replace('-', '_') + '_pct'):.0f}" for c in ['no-damage', 'minor-damage', 'major-damage']]
                    + [f'{r.destroyed_pct:.0f} ({r.destroyed_lo:.0f}–{r.destroyed_hi:.0f})'])
    a = table(['Height above channel (m)', 'Buildings', 'No damage (%)', 'Minor (%)', 'Major (%)', 'Destroyed (%, 95% CI)'], rows)
    m = pd.read_csv(TAB/'terrain_local_models.csv')
    terms = {'rem_10m': 'Height above channel (per 10 m)', 'log_dist': 'Distance to channel (log m)',
             'chainage_10km': 'Distance downstream (per 10 km)', 'valley_100m': 'Valley-floor width (per 100 m)',
             'outer_bank': 'Outer bank of bend', 'slope_10deg': 'Hillslope angle (per 10°)', 'log_area': 'Footprint area (log m^2^)',
             'density_10': 'Buildings within 100 m (per 10)'}
    rows = []
    for t, lab in terms.items():
        row = [lab]
        for mod in ['logit_destroyed', 'logit_severe', 'ordinal_logit']:
            r = m[(m.model == mod) & (m.term == t)].iloc[0]
            p = 'P < 0.001' if r.p < 0.001 else f'P = {r.p:.3f}'
            row.append(f'{r.odds_ratio:.2f} ({r.or_lo:.2f}–{r.or_hi:.2f}); {p}')
        rows.append(row)
    loc = tr['local']
    pr2 = m.groupby('model').pseudo_r2.first()
    rows.append(['McFadden pseudo-R^2^', f"{pr2['logit_destroyed']:.2f}", f"{pr2['logit_severe']:.2f}", '–'])
    b_ = table(['Term', 'Logistic: destroyed', 'Logistic: major or destroyed', 'Ordinal: four HOT classes'], rows)
    return a, b_, loc


def t_ml():
    p = pd.read_csv(TAB/'ml_performance.csv')
    names = {'gbm': 'Gradient-boosted trees, nine attributes', 'logit_full': 'Logistic regression, nine attributes',
             'logit_rem': 'Logistic regression, height only', 'gbm_cems_labels_only': 'Gradient-boosted trees, CEMS labels only',
             'gbm_transfer_to_HOT': 'Gradient-boosted trees trained outside HOT reach, tested on HOT labels'}
    cvl = {'GroupKFold(6) on 5-km chainage blocks': 'Six folds grouped by 5-km reaches',
           'GroupKFold(4), CEMS AOIs only': 'Four folds grouped by 5-km reaches, CEMS areas',
           'trained outside HOT reach': 'Independent HOT labels'}
    a = table(['Model', 'Validation', 'Buildings', 'Prevalence (%)', 'ROC AUC', 'PR AUC', 'Brier score'],
              [[names[r.model], cvl.get(r.cv, r.cv), n0(r.n), f'{100*r.prevalence:.1f}', f'{r.auc:.3f}', f'{r.pr_auc:.3f}', f'{r.brier:.3f}']
               for r in p.itertuples()])
    i = pd.read_csv(TAB/'ml_permutation_importance.csv')
    b = table(['Attribute', 'Mean decrease in AUC', 'Standard deviation across folds'],
              [[r.label, f'{0 if abs(r.importance_auc_drop) < 5e-4 else r.importance_auc_drop:.3f}', f'{r.importance_sd:.3f}']
               for r in i.itertuples()])
    return a, b


def t_envelope():
    env = robust_reach_heights(pd.read_csv(TAB/'terrain_envelope_by_reach.csv'))
    rows = []
    for r in env.itertuples():
        wide = (r.rem50_hi - r.rem50_lo) > 60
        ci = 'unbounded' if (r.rem50_lo < -50 or r.rem50_hi > 400) else f'{r.rem50_lo:.0f} to {r.rem50_hi:.0f}'
        rows.append([f'{r.reach_start_km:.0f}–{r.reach_end_km:.0f}', n0(r.n_buildings), n0(r.n_destroyed),
                     f"{r.rem50_m:.1f} ({ci}){'†' if wide else ''}", f1(r.rem_destroyed_p90),
                     '–' if np.isnan(r.flow_edge_rem_p50) else f'{r.flow_edge_rem_p50:.1f} ({r.flow_edge_rem_p25:.0f}–{r.flow_edge_rem_p75:.0f})',
                     n0(r.valley_width_20m_median), f1(r.h_core), f1(r.h_outer)])
    return table(['Reach (km)', 'Graded buildings', 'Destroyed', 'Height at 50% destruction (95% CI) (m)',
                  '90th percentile, destroyed (m)', 'Flow-edge height, median (IQR) (m)', 'Valley-floor width <20 m (m)',
                  'Core height (m)', 'Outer height (m)'], rows)


def t_setback():
    s = pd.read_csv(TAB/'terrain_setback_thresholds.csv')
    rows = [[f'{r.rem_threshold_m:.0f}', f'{r.destroyed_below_pct:.0f}', f'{r.gorge_21_41km_destroyed_below_pct:.0f}',
             f'{r.middle_64_89km_destroyed_below_pct:.0f}', f'{r.lower_89_114km_destroyed_below_pct:.0f}',
             n0(r.undamaged_stock_below_0_207km), n0(r.undamaged_stock_below_106_207km)] for r in s.itertuples()]
    return table(['Height threshold (m)', 'Destroyed below, all graded (%)', 'Gorge, 21–41 km (%)', 'Middle valley, 64–89 km (%)',
                  'Lower valley, 89–114 km (%)', 'Undamaged buildings below, 0–207 km', 'of which 106–207 km'], rows)


def t_exposure():
    e = pd.read_csv(TAB/'exposure_growth_zones.csv')
    zl = {'flow_extent': 'UNOSAT flow extent', 'rem_lt10_d1km': '<10 m above channel', 'rem_10_20_d1km': '10–20 m',
          'rem_20_40_d1km': '20–40 m', 'rem_40_80_d1km': '40–80 m', 'rem_ge80_d1km': '≥80 m',
          'corridor_d1km': 'All land within 1 km', 'corridor_d2km': 'All land within 2 km'}
    rl = {'0-106km (assessed)': '0–106 km', '106-207km (downstream)': '106–207 km'}
    rows = []
    for r in e.itertuples():
        if r.area_km2 == 0:
            continue
        rows.append([zl[r.zone], rl[r.reach], f1(r.area_km2), f1(r.built_m2_1975/1e4), f1(r.built_m2_2000/1e4),
                     f1(r.built_m2_2020/1e4), f'{r.built_growth_1975_2020:.1f}', n0(r.pop_2015), n0(r.pop_2026)])
    return table(['Zone', 'Reach', 'Area (km^2^)', 'Built-up 1975 (ha)', 'Built-up 2000 (ha)',
                  'Built-up 2020 (ha)', 'Growth 1975–2020 (×)', 'Population 2015', 'Population 2026'], rows)


def t_lead():
    s = pd.read_csv(TAB/'timing_lead_time_scenarios.csv')
    a = table(['Alert scenario', 'Alert time (NPT)', 'Reached before alert (%)', '≥10 min (%)', '≥30 min (%)', '≥60 min (%)',
               'Median lead time (min)'],
              [[r.scenario.replace('08:46-08:54', '08:46–08:54'), r.alert_time[:5], f1(r.pct_destroyed_negative), f1(r.pct_destroyed_ge10), f1(r.pct_destroyed_ge30),
                f1(r.pct_destroyed_ge60), f1(r.median_lead_destroyed_min)] for r in s.itertuples()])
    m = pd.read_csv(TAB/'timing_lead_time_by_municipality.csv')
    m['municipality'] = m.municipality.replace(CANON)
    b = table(['Local level', 'Destroyed buildings', 'Median distance (km)', 'Seismic alert, 08:39 (min)', 'Phone warnings, 08:50 (min)',
               'Mass SMS, 09:15 (min)'],
              [[r.municipality, n0(r.destroyed), f1(r.chainage_median_km), f1(r.lead_seismic_min, 0), f1(r.lead_phone_min, 0),
                f1(r.lead_sms_min, 0)] for r in m.itertuples()])
    return a, b


def t_casualties():
    c = pd.read_csv(TAB/'casualty_series.csv')
    return table(['Date', 'Time (NPT)', 'Deaths', 'Missing', 'Source', 'Type'],
                 [[r.date, r.time_npt if isinstance(r.time_npt, str) else '–', n0(r.deaths), n0(r.missing),
                   link(r.url, r.source.replace('26 Aug-3 Oct', '26 Aug–3 Oct')), r.source_type.replace('-', ' ')]
                  for r in c.itertuples()])


def t_infra():
    t = pd.read_csv(TAB/'infrastructure_cems_transport.csv')
    rows = []
    for aoi in ['AOI01', 'AOI02', 'AOI03', 'AOI05', 'All']:
        rd = t[(t.layer == 'roads') & (t.aoi == aoi)].iloc[0]; br = t[(t.layer == 'bridges') & (t.aoi == aoi)].iloc[0]
        lab = {'AOI01': 'AOI01 Syapru Besi', 'AOI02': 'AOI02 Timure', 'AOI03': 'AOI03 Bidur', 'AOI05': 'AOI05 Phosretar',
               'All': '**All**'}[aoi]
        prod = {'GRA_PRODUCT': 'First grading', 'GRA_MONIT01': 'Monitoring 1', 'latest': 'Latest'}[rd['product']]
        rows.append([lab, prod, f1(rd.Destroyed), f1(rd.Damaged), f1(rd['Possibly damaged']),
                     f1(rd['No visible damage']), n0(br.Destroyed), n0(br.Damaged), n0(br['Possibly damaged'])])
    a = table(['Area of interest', 'Product', 'Roads destroyed (km)', 'Roads damaged (km)', 'Roads possibly damaged (km)',
               'Roads, no visible damage (km)', 'Bridges destroyed', 'Bridges damaged', 'Bridges possibly damaged'], rows)
    s = pd.read_csv(TAB/'infrastructure_assets_in_extent.csv')
    lab = {'bridge': 'Bridges', 'dam': 'Dams', 'generator': 'Power generators', 'plant': 'Power plants', 'power_tower': 'Transmission towers',
           'substation': 'Substations', 'weir': 'Weirs'}
    b = table(['Asset (Overture)', 'In UNOSAT flow extent', 'Within 500 m of channel and <20 m above it', 'In study window'],
              [[lab.get(r._1, r._1), n0(r.in_flow_extent), n0(r.within_500m_rem_lt20), n0(r.total_in_window)]
               for r in s.rename(columns={'class': '_1'}).itertuples()])
    rd = pd.read_csv(TAB/'infrastructure_roads_in_extent.csv')
    c = table(['Road class (Overture)', 'Length in UNOSAT flow extent (km)'],
              [[r._1.capitalize(), f1(r.km_in_extent)] for r in rd.rename(columns={'class': '_1'}).itertuples()]
              + [['**Total**', f'**{f1(rd.km_in_extent.sum())}**']])
    return a, b, c, t


def t_landcover():
    t = pd.read_csv(TAB/'landcover_flow_extent.csv')
    cols = [c for c in t.columns if c != 'class']
    rows = [[('**' + r['class'] + '**') if r['class'] == 'Total' else r['class']]
            + [(f"**{r[c]:.2f}**" if r['class'] == 'Total' else f'{r[c]:.2f}') for c in cols] for _, r in t.iterrows()]
    return table(['Land cover (2021)'] + cols, rows)


def t_losses():
    l = pd.read_csv(TAB/'loss_estimates.csv')
    return table(['Estimate', 'Scope', 'US$ million', 'Range (US$ million)', 'Reference date', 'Source'],
                 [[r.estimate, r.scope, f1(r.usd_million), '–' if np.isnan(r.low_usd_million) else f'{r.low_usd_million:,.0f}–{r.high_usd_million:,.0f}',
                   r.reference_date, link(r.url, r.source)] for r in l.itertuples()])


# ----------------------------------------------------------------------------------------------- document
def build():
    F = facts()
    tr = json.loads((DER/'terrain_results.json').read_text())
    s2log = json.loads((ROOT/'sources_ext'/'s2'/'s2_log.json').read_text())
    s2r = json.loads((DER/'s2_results.json').read_text())
    s2a = pd.read_csv(TAB/'s2_separability_auc.csv')
    s2c = pd.read_csv(TAB/'s2_change_by_class.csv')
    ir = json.loads((DER/'impacts_results.json').read_text())
    conf = pd.read_csv(TAB/'confidence_sensitivity.csv').set_index('threshold')
    pos = pd.read_csv(TAB/'position_sensitivity.csv').set_index('direction')
    env = robust_reach_heights(pd.read_csv(TAB/'terrain_envelope_by_reach.csv'))
    cal = pd.read_csv(TAB/'ml_calibration.csv')
    sb = pd.read_csv(TAB/'terrain_setback_thresholds.csv').set_index('rem_threshold_m')
    t4a, t4b = t_products()
    t6a, t6b, loc = t_local(tr)
    t7a, t7b = t_ml()
    t11a, t11b = t_lead()
    t13a, t13b, t13c, cems_tr = t_infra()
    ct = pd.read_csv(TAB/'agreement_hot_cems.csv', index_col=0)
    hot_des_norec = int(ct.loc['HOT destroyed', 'CEMS no record']); hot_des = int(ct.loc['HOT destroyed'].sum())
    wide = env[(env.rem50_hi - env.rem50_lo) > 60]
    auc = lambda k, t: s2a[(s2a['index'] == k) & s2a.target.str.startswith(t)].auc.iloc[0]
    med = lambda prod, lev, k: s2c[(s2c['product'] == prod) & (s2c.level == lev) & (s2c['index'] == k)].p50.iloc[0]
    shift = (pos.drop('original').unosat_members - pos.loc['original', 'unosat_members']).abs().max()
    shift_sev = (pos.drop('original').severe_inside - pos.loc['original', 'severe_inside']).abs().max()
    rall = cems_tr[(cems_tr.layer == 'roads') & (cems_tr.aoi == 'All')].iloc[0]
    ball = cems_tr[(cems_tr.layer == 'bridges') & (cems_tr.aoi == 'All')].iloc[0]
    deb = ir['debris']
    lcr = json.loads((DER/'landcover_results.json').read_text())
    lc_crop, lc_tot, lc_unosat = lcr['Cropland'], lcr['total_km2'], lcr['unosat_area_km2']

    md = f"""# Supplementary Information

## What height is safe? An analysis of building destruction along the 207-km path of Nepal's 2026 flood

**Nusrat Zahan Jarin^1^, Obaidur Rahman^2^, Rezwan Ahmed^3^**

^1^Department of Geography, University of California, Santa Barbara, CA, USA. ^2^Department of Geography, Oklahoma State University, Stillwater, OK, USA. ^3^Department of Geography and Environment, University of Dhaka, Dhaka, Bangladesh.

This file contains Supplementary Notes 1–6, Supplementary Tables 1–15, Supplementary Figs. 1–6 and Supplementary References. Every number is generated by the scripts that accompany the manuscript; table sources are named in each legend.

\\pagebreak

## Supplementary Notes

### Supplementary Note 1 | Sources, versions and provenance

The analysis combines two kinds of evidence (Supplementary Table 1). Event observations comprise the building-damage grading of HOT, CEMS and UNDP RAPIDA [@HOT2026; @EMSR927; @UNDP2026RAPIDA], the UNOSAT flow extent [@UNOSAT2026], the propagation timeline [@CHWRR2026] and official reports [@NDRRMA2026update; @RDNA2026]. Pre-event context comprises the Copernicus GLO-30 elevation model [@CopDEM], Sentinel-2 Level-2A imagery [@Drusch2012; @EarthSearch], the Overture building stock and infrastructure [@Overture], GHS-BUILT-S settlement history [@GHSBUILTS2023], WorldPop population [@WorldPopGlobal2] and geoBoundaries local levels [@Runfola2020]. All sources were retrieved between 9 September and 20 October 2026; every download was logged with its URL, HTTP status, size and SHA-256 checksum.

Three limitations of access shaped the design. Gauge observations of the Department of Hydrology and Meteorology could not be retrieved because the public interface requires an application key, so stage rises were taken from the CHWRR report. HOT, UNDP and UNOSAT layers carry no product-specific redistribution licence; they are cited and archived for verification but should not be republished until permission is confirmed. Planet imagery is released for non-commercial use only and was not used.

### Supplementary Note 2 | Harmonization of damage records and its sensitivity

Grades were mapped to a common ordinal scale: 0, no damage (HOT) or no record inside a graded area; 1, minor (HOT) or possibly damaged (CEMS); 2, major (HOT) or damaged (CEMS, UNDP); and 3, destroyed. Matching to the Overture stock (Methods) left {F['undp_only']} UNDP footprints, {F['hot_only']} HOT footprints and {F['cems_only']} CEMS points without a counterpart; they were retained as separate buildings so that the harmonized total of {F['union_damaged']} damaged buildings ({F['union_destroyed']} destroyed) includes every damage record (Supplementary Tables 3 and 4). The {n0(ir['debris']['n_buildings'])} damaged buildings used in the debris model are the same set.

HOT and CEMS agreed closely on destruction but not on lesser damage (Supplementary Table 4b). Of the {hot_des} buildings that HOT classed as destroyed inside CEMS AOI01 and AOI02, {hot_des_norec} ({100*hot_des_norec/hot_des:.0f}%) carried no CEMS record, whereas {F['cems_confirmed']}% of CEMS-destroyed buildings were destroyed in HOT; a building recorded as destroyed by either product was therefore treated as destroyed. Only {F['unosat_confirmed']}% of the {F['unosat_n']} UNOSAT-attributed records inside CEMS areas were also destroyed in CEMS, and these records are the only ones available north of the border (Supplementary Table 3).

Two checks retained from the first analysis address the quality of the HOT labels (Supplementary Fig. 6). Requiring a HOT confidence score of at least 0.75 retained {conf.loc[0.75, 'coverage_percent']:.0f}% of records and removed almost all minor and major labels (minor {int(conf.loc[0.0, 'minor-damage'])} to {int(conf.loc[0.75, 'minor-damage'])}; major {int(conf.loc[0.0, 'major-damage'])} to {int(conf.loc[0.75, 'major-damage'])}) but only {int(conf.loc[0.0, 'destroyed']) - int(conf.loc[0.75, 'destroyed'])} of {int(conf.loc[0.0, 'destroyed'])} destroyed labels, so the destruction labels on which the models rest are the most confident ones. Translating all HOT footprints by 5 m in each cardinal direction changed the number inside the UNOSAT extent by at most {words(int(shift))} buildings and the number of severely damaged buildings inside it by at most {words(int(shift_sev))}.

### Supplementary Note 3 | Model specification and diagnostics

The local models used the {loc['n']:,} HOT buildings with a damage label, of which {loc['n_destroyed']:,} were destroyed. Height alone separated destroyed from other buildings with an AUC of {F['auc_rem_local']} (odds ratio {F['or_10m']} per 10 m; height at 50% probability {loc['rem50_m']:.0f} m, 95% interval {loc['rem50_ci'][0]:.0f}–{loc['rem50_ci'][1]:.0f} m). In the multivariable models (Supplementary Table 6b), height, distance and hillslope angle are strongly correlated within this narrow reach, so their individual coefficients are less precise than the joint fit. Distance downstream and hillslope angle remained significant in both logistic models and building density in the model of major damage or destruction; in the ordinal model, all terms except valley width and footprint area were significant.

For the regional gradient-boosted model, out-of-fold predictions were well calibrated apart from slight overconfidence at the top of the range (Supplementary Fig. 3a): in the highest decile the mean predicted probability was {cal.p_mean.iloc[-1]:.2f} against an observed share of {cal.y_mean.iloc[-1]:.2f}, and in the next decile {cal.p_mean.iloc[-2]:.2f} against {cal.y_mean.iloc[-2]:.2f}. Partial dependence (Supplementary Fig. 3b–f) shows a sharp decline in the probability of destruction between about 10 and 35 m above the channel and a weaker decline with distance from the channel. Because partial dependence averages over the observed values of all other attributes, including distances of up to 1 km, its 50% contour lies below the reach-wise envelope, which is conditional on the buildings present in each reach; the contour is shown only to illustrate the downstream decline. Permutation importance (Supplementary Table 7b) attributes most of the skill to height above the channel.

### Supplementary Note 4 | Height above the channel and the damage-calibrated height

Height above the channel is a relative elevation: it measures how far a building stands above the pre-event channel, not the depth of the flow. In the gorge it integrates water depth, run-up, superelevation and the collapse of undercut terraces; in the wider valley it approximates the stage reached by the flow more closely. The reach-wise height at 50% destruction is therefore a damage-calibrated envelope rather than a hydraulic quantity.

Reach estimates and their smoothing are listed in Supplementary Table 8. In {words(len(wide))} gorge reaches (marked †) the 50% height was poorly constrained, with a bootstrap interval wider than 60 m; there the 90th-percentile height of destroyed buildings was used when it was smaller. A three-reach running median within each contiguous graded segment then removed the influence of a few far up-slope destroyed records in the 31–36-km reach, whose 90th-percentile height ({f1(env.set_index('reach_start_km').loc[31, 'rem_destroyed_p90'], 0)} m) would otherwise have dominated the outer envelope. The pooled estimates for all buildings in each reach group (gorge {F['rg_gorge']} m; middle valley {F['rg_valley']} m; lower valley {F['rg_lower']} m) are consistent with the smoothed reach values. The damage-calibrated height correlated with the height of the UNOSAT flow-extent edge across {F['n_reaches']} reaches (Spearman ρ = {F['rho_env']}), negatively with the width of the valley floor and positively with the mean celerity of the wave front (Supplementary Fig. 4). Both relationships share a common downstream trend and are descriptive.

No uniform threshold matched the damage. A 20-m height threshold would have contained {sb.loc[20, 'destroyed_below_pct']:.0f}% of destroyed buildings in the graded corridor but only {sb.loc[20, 'gorge_21_41km_destroyed_below_pct']:.0f}% in the gorge, against {sb.loc[20, 'lower_89_114km_destroyed_below_pct']:.0f}% in the lower valley, while including {n0(sb.loc[20, 'undamaged_stock_below_0_207km'])} undamaged buildings along the whole corridor (Supplementary Table 9).

### Supplementary Note 5 | Sentinel-2 processing and corroboration

Sentinel-2 Level-2A scenes were read directly from the Earth Search cloud-optimized archive [@EarthSearch]. All scenes used had the processing-baseline offset already removed by the archive (property earthsearch:boa_offset_applied), so reflectance was computed as the digital number × 10^−4^; the offset listed in the band metadata was applied only to scenes without this flag. Where an acquisition had been processed twice, only the later processing was used. Medians of clear-sky pixels (scene classes 4–7) were computed per MGRS tile at 20 m for {len(s2log['pre'])} pre-event scenes ({min(x['datetime'][:10] for x in s2log['pre'])} to {max(x['datetime'][:10] for x in s2log['pre'])}) and {len(s2log['post'])} post-event scenes ({min(x['datetime'][:10] for x in s2log['post'])} to {max(x['datetime'][:10] for x in s2log['post'])}), and the tile with more clear observations was kept where tiles overlapped.

All four indices separated destroyed from other buildings (Supplementary Table 5 and Supplementary Fig. 2b). NDVI separated them with an AUC of {auc('ndvi', 'destroyed vs not'):.2f} across all graded buildings and {auc('ndvi', 'HOT'):.2f} against HOT labels; the median NDVI change was {med('HOT', 0, 'ndvi'):+.2f} for HOT buildings without damage and {med('HOT', 3, 'ndvi'):+.2f} for destroyed ones. A threshold on NDVI loss chosen without reference to the damage data (Otsu's method [@Otsu1979], ΔNDVI < {s2r['otsu_threshold_dndvi']:.2f}) delineated {s2r['change_area_km2']:.1f} km^2^ of disturbed ground within 1.5 km of the channel over the first 106 km; {100*s2r['precision']:.0f}% of it lay inside the UNOSAT flow extent, which it covered to {100*s2r['recall']:.0f}% (intersection over union {s2r['iou']:.2f}). Differences from the UNOSAT extent arise where the flow left vegetation standing, where clouds or terrain shadow removed observations (Supplementary Fig. 2a) and where post-event landslides or construction changed the surface. At 20 m, a building pixel also contains gardens, fields and roads, so the indices corroborate the damage labels at the scale of a building's surroundings rather than grading roofs. The post-event window began on 21 September, a few weeks earlier in the season than the pre-event window, which probably explains the slightly positive median change for undamaged buildings; such a phenological difference cannot produce the grade-dependent contrast observed.

### Supplementary Note 6 | Timing, exposure, infrastructure, debris and ranking

The propagation timeline (Supplementary Table 2) starts at the seismic onset of the failure (08:37:10 NPT) [@Roy2026; @USGS2026]. Gauge-loss times bound arrival from above, and the Kali Khola entry is a threshold crossing that was excluded from the interpolation. Lead times by local level are given in Supplementary Table 11.

Built-up surface grew fastest on the lowest ground in both the graded corridor and the ungraded corridor downstream (Supplementary Table 10). CEMS graded {f1(rall.Destroyed)} km of road as destroyed, {f1(rall.Damaged)} km as damaged and {f1(rall['Possibly damaged'])} km as possibly damaged in its four areas of interest, and recorded {n0(ball.Destroyed + ball.Damaged + ball['Possibly damaged'])} bridges as affected, of which {n0(ball.Destroyed)} were destroyed (Supplementary Table 13a). {words(int(rall.records_without_geometry)).capitalize()} road records lacked geometry and were counted but not measured. Overture infrastructure inside the UNOSAT flow extent is listed as exposure in Supplementary Table 13b,c; it records presence before the event, not damage. ESA WorldCover 2021 [@Zanaga2022] shows what the flow covered (Supplementary Table 15): tree cover, grassland and bare ground dominated above the border and in the gorge, whereas cropland ({lc_crop:.1f} km^2^) and built-up land were concentrated in the Trishuli valley. The land-cover areas sum to {lc_tot:.2f} km^2^, matching the area of the UNOSAT polygon ({lc_unosat:.2f} km^2^).

The debris estimate is most sensitive to the settlement factor applied to urban buildings (Supplementary Fig. 5a,b). The central estimate of {deb['debris_central_t']/1e6:.2f} Mt uses UNDP's factors and therefore lies at the upper end of the Monte Carlo range, whose median is {deb['debris_mc_p50']/1e6:.2f} Mt; without settlement factors the total is {deb['debris_no_settlement_factor_t']/1e6:.2f} Mt. The ranking of local levels was robust at the top and bottom but not in the middle (Supplementary Fig. 5c). In the casualty series (Supplementary Table 12) the number of missing people rose until mid-September and then fell, while the number of deaths continued to rise; the figures used here (to 3 October 2026) remain provisional. Published monetary estimates differ in scope (Supplementary Table 14) [@UNDP2026RAPIDA; @GRADE2026; @RDNA2026].

\\pagebreak

## Supplementary Tables

**Supplementary Table 1 | Data sources.** Datasets used in this study, with version, date, resolution, use and access. Retrieval logs with URLs, dates and SHA-256 checksums accompany the code.

{t_sources(s2log)}

*Note:* "Terms unconfirmed" means that no product-specific licence was found; such layers are cited and archived for verification but not redistributed. OpenStreetMap data © OpenStreetMap contributors (ODbL).

**Supplementary Table 2 | Propagation timeline of the flood wave.** Distances are along the traced flow path. Mean celerity is the distance between consecutive arrival points divided by the time between them. Source: timing_wave_arrivals.csv.

{t_timeline()}

*Note:* Gauge-loss times are upper bounds on arrival. The Kali Khola time marks the crossing of the danger level and is not used as an arrival.

**Supplementary Table 3 | Harmonized building damage by local level.** Damaged includes possibly damaged, damaged and destroyed. Median distance is measured along the flow path for damaged buildings. CEMS residential and non-residential refer to the building type recorded by CEMS for affected buildings. Source: harmonised_by_municipality.csv.

{t_municipal()}

*Note:* Buildings outside Nepal are UNOSAT-attributed records in the UNDP layer, north of the border crossing at Rasuwagadhi. Local-level names follow the RDNA.

**Supplementary Table 4 | Damage products and their agreement.** **a**, Buildings assessed, damaged and destroyed by each product after one-to-one matching to the common stock. **b**, Cross-tabulation of HOT labels against the latest CEMS grade for the {F['n_both']} buildings graded by both (Cohen's κ for destruction = {F['kappa_destroyed']}). Sources: products_summary.csv, agreement_hot_cems.csv.

{t4a}

{t4b}

**Supplementary Table 5 | Separation of destroyed buildings by Sentinel-2 change indices.** Area under the receiver-operating-characteristic curve for post-minus-pre change averaged over 3 × 3 pixels (20 m) at each building. Source: s2_separability_auc.csv.

{t_s2()}

**Supplementary Table 6 | HOT damage by height above the channel and local models.** **a**, Composition of HOT damage classes by band of height above the channel, with Wilson 95% confidence intervals for the share destroyed. **b**, Odds ratios (95% confidence intervals) from logistic models of destruction and of major damage or destruction and from a proportional-odds model of the four HOT classes, with standard errors clustered by 1-km reach (n = {loc['n']:,}). Sources: terrain_local_rem_bins.csv, terrain_local_models.csv.

{t6a}

{t6b}

**Supplementary Table 7 | Regional models of destruction.** **a**, Performance under spatial cross-validation and transfer tests. **b**, Permutation importance of the gradient-boosted model (mean decrease in test-fold AUC over ten permutations). Sources: ml_performance.csv, ml_permutation_importance.csv.

{t7a}

{t7b}

**Supplementary Table 8 | Damage-calibrated destructive height by reach.** Height above the channel at which a logistic model of destruction reached 50% probability (block-bootstrap 95% interval), the 90th percentile height of destroyed buildings, the height of the UNOSAT flow-extent edge, valley-floor width, and the smoothed core and outer heights used for the danger zones. Source: terrain_envelope_by_reach.csv.

{t_envelope()}

*Note:* † Bootstrap interval wider than 60 m; the core height uses the smaller of the 50% height and the 90th percentile of destroyed buildings before smoothing. Downstream of 114 km the envelope is interpolated between stage rises of {STAGE_RISE[1][1]} m at Kali Khola ({STAGE_RISE[1][0]:.0f} km) and {STAGE_RISE[2][1]} m at Devghat ({STAGE_RISE[2][0]:.1f} km) [@CHWRR2026].

**Supplementary Table 9 | Share of destroyed buildings and undamaged stock below uniform height thresholds.** Source: terrain_setback_thresholds.csv.

{t_setback()}

**Supplementary Table 10 | Built-up surface and population by band of height above the channel.** GHS-BUILT-S R2023A and WorldPop Global2 R2025A interpolated to the 30-m grid; bands are within 1 km of the traced channel. Source: exposure_growth_zones.csv.

{t_exposure()}

**Supplementary Table 11 | Warning lead time for destroyed buildings.** **a**, Distribution of lead times under three alert scenarios for the {F['union_destroyed']} destroyed buildings. **b**, Median lead time by local level (negative values: the flood arrived before the alert). Sources: timing_lead_time_scenarios.csv, timing_lead_time_by_municipality.csv.

{t11a}

{t11b}

**Supplementary Table 12 | Reported deaths and missing people in Nepal.** Values as published at each date; some secondary compilations report official figures. Source: casualty_series.csv.

{t_casualties()}

**Supplementary Table 13 | Infrastructure.** **a**, Road length and bridges graded by CEMS EMSR927 (latest product for each area of interest). **b**, Infrastructure assets mapped in Overture before the event inside the UNOSAT flow extent and on low ground near the channel. **c**, Overture road length inside the flow extent by class. Sources: infrastructure_cems_transport.csv, infrastructure_assets_in_extent.csv, infrastructure_roads_in_extent.csv.

{t13a}

{t13b}

{t13c}

**Supplementary Table 14 | Published monetary estimates.** Values are reported as published; this study did not recompute monetary losses. Source: loss_estimates.csv.

{t_losses()}

**Supplementary Table 15 | Pre-event land cover inside the UNOSAT flow extent.** Area (km^2^) of ESA WorldCover 2021 classes inside the mapped flow extent by reach of the traced flow path; pixel areas are computed on the WGS 84 ellipsoid. Source: landcover_flow_extent.csv.

{t_landcover()}

\\pagebreak

## Supplementary Figures

![Supplementary Figure 1](figures/figure_s1_workflow.png)

**Supplementary Fig. 1 | Workflow.** Inputs, harmonization steps, analyses and outputs. All steps are scripted and rebuilt from the archived inputs by a single command.

![Supplementary Figure 2](figures/figure_s2_sentinel2.png)

**Supplementary Fig. 2 | Sentinel-2 change at building locations.** **a**, Change in NDVI between clear-sky median composites of October 2025 and 21 September–18 October 2026 around Timure, Syaphrubesi and Trishuli Bazar; changes smaller than 0.1 in magnitude are transparent, areas without a clear observation in either composite are tinted, and the black line is the UNOSAT flow extent. **b**, Change in visible brightness, NDWI and the bare-soil index at building locations by harmonized damage grade (boxes, interquartile range; whiskers, 10th–90th percentiles; line, median), with the AUC for separating destroyed from other buildings. Contains modified Copernicus Sentinel data (2025, 2026).

![Supplementary Figure 3](figures/figure_s3_model_diagnostics.png)

**Supplementary Fig. 3 | Diagnostics of the regional gradient-boosted model.** **a**, Calibration of out-of-fold predicted probabilities (deciles) under six-fold cross-validation grouped by 5-km reaches; dashed line, perfect calibration. **b**–**e**, Partial dependence of the probability of destruction on height above the channel, distance to the channel, distance downstream and valley-floor width. **f**, Two-way partial dependence on height above the channel and distance downstream, with the 50% contour. Partial dependence was computed on the log-odds scale and is shown after logistic transformation; it averages over the observed values of the other attributes (Supplementary Note 3).

![Supplementary Figure 4](figures/figure_s4_reach_physics.png)

**Supplementary Fig. 4 | The damage-calibrated height in relation to valley form and wave speed.** **a**, Core damage-calibrated height of each graded reach against the median width of valley floor less than 20 m above the channel. **b**, The same height against the mean celerity of the wave front interpolated to the reach midpoint. Colours show distance downstream. **c**, Cross-sections of height above the channel perpendicular to the flow path in the gorge (26 km) and the valley (79 km), with the damage-calibrated heights of the two reaches (dashed lines).

![Supplementary Figure 5](figures/figure_s5_debris_rank.png)

**Supplementary Fig. 5 | Uncertainty in debris and priorities.** **a**, Building debris in 5,000 Monte Carlo draws with grade coefficients scaled between 0.6 and 1.4 and the urban settlement factor between 1 and 3, compared with the central estimate using UNDP's factors (solid), the estimate without settlement factors (dotted) and the UNDP RAPIDA totals for the CEMS/SERTIT records and for all records (dashed). **b**, Share of debris in Bidur in the same draws; lines as in **a**. **c**, Probability of each rank of the composite priority index across 20,000 draws of weights, normalization and aggregation; local levels are ordered by median rank and probabilities below 0.5% are blank.

![Supplementary Figure 6](figures/figure_s6_hot_checks.png)

**Supplementary Fig. 6 | Checks on the HOT inventory.** **a**, Cumulative distributions of HOT confidence scores by damage class (number of buildings in brackets). **b**, Share of records retained and share of severe damage (major or destroyed) among retained records as the minimum confidence score increases. **c**, Change in the number of HOT buildings inside the UNOSAT flow extent, and of severely damaged buildings inside it, when all footprints are translated by 5 m in each direction.

## Supplementary References

{{{{REFERENCES}}}}
"""
    refs = {r['key']: r for r in json.loads((ROOT/'paper'/'references.json').read_text(encoding='utf-8'))}
    md, order = cite(md, refs)
    md = minus(md)
    md = md.replace('{{REFERENCES}}', '\n\n'.join(f'{i}. {nature_ref(refs[k])}' for i, k in enumerate(order, 1)))
    left = re.findall(r'\{\{\w+\}\}', md)
    if left:
        raise KeyError(f'unresolved placeholders {left}')
    (ROOT/'paper'/'Supplementary_Information.md').write_text(md, encoding='utf-8')
    print(f'wrote Supplementary_Information.md: {len(order)} references, {md.count("**Supplementary Table")} table captions, '
          f'{md.count("**Supplementary Fig.")} figure legends')


if __name__ == '__main__':
    build()
