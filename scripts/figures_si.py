"""Supplementary figures S1-S6."""
import sys
import json
import numpy as np
import pandas as pd
import rasterio
from shapely.geometry import box
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyBboxPatch, Patch, Rectangle
from matplotlib.lines import Line2D
from matplotlib.colors import LinearSegmentedColormap
from figstyle import (ROOT, DER, W2, MM, INK, INK2, MUTED, GRID, AXIS, DMG, DESTROYED, CM_BLUE, CM_BLUE_R,
                      BLUE, HALO, save, panel, hgrid, raster_window, extent, add_geom, scalebar, clean_map)
from figures_v2 import load_common, soft_hillshade, PROJ
from analysis_impacts import robust_reach_heights

TAB = ROOT/'tables'
NODATA = '#e9dfc9'                      # pale warm tint for 'no clear observation'


def logistic(v):
    return 1/(1 + np.exp(-np.asarray(v, float)))


def undp_debris_kt():
    """UNDP RAPIDA debris totals (kt) for the CEMS/SERTIT records and for all records."""
    f = json.loads((ROOT/'data'/'undp_debris_combined.geojson').read_text(encoding='utf-8'))['features']
    d = pd.DataFrame([x['properties'] for x in f])
    return d.loc[d.source_y.isin(['EMSR927', 'Sertit']), 'debris'].sum()/1e3, d.debris.sum()/1e3


def s1(c):
    """Workflow schematic."""
    inv = c['inv']
    n_dmg, n_des = int((inv.max_level >= 1).sum()), int((inv.max_level == 3).sum())
    length = c['ch'].chain[-1]/1000
    fig = plt.figure(figsize=(W2, 78*MM))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(0, 50); ax.axis('off')
    cols = [('Inputs', ['Building-damage grading: HOT,\nCEMS EMSR927, UNDP RAPIDA\n(CEMS, SERTIT, UNOSAT records)',
                        'Official records: NDRRMA updates,\nRDNA, CHWRR propagation timeline',
                        'Pre-event terrain:\nCopernicus GLO-30 DEM',
                        'Sentinel-2 L2A composites\n(Oct 2025; Sep–Oct 2026)',
                        'Stock and exposure: Overture,\nGHS-BUILT-S 1975–2020,\nWorldPop 2015–2026']),
            ('Harmonization', [f'D8 flow path from the reported\nsource to Devghat ({length:.0f} km)',
                               'Height above channel (REM),\ndistance, chainage, valley width',
                               'One-to-one matching of damage\nrecords to a common stock',
                               'Graded domain: CEMS AOIs\n(minus not-analysed) and HOT']),
            ('Analyses', ['Inter-product agreement and\nSentinel-2 corroboration',
                          'Terrain controls: logistic, ordinal\nand boosted trees, spatial CV',
                          'Reach-wise destructive height vs\nflow-edge heights and gauges',
                          'Exposure growth, wave timing,\nwarning lead-time scenarios',
                          'Composite ranking and debris,\nMonte Carlo uncertainty']),
            ('Outputs', [f'Harmonized inventory: {n_dmg:,}\ndamaged, {n_des:,} destroyed',
                         'Damage-calibrated danger\nzones (core and outer)',
                         'Municipal priorities with\nrank uncertainty',
                         'Warning-chain and\nreconstruction recommendations'])]
    bw, bh, gap, x0, step = 22.5, 7.0, 1.6, 1.0, 25.2
    for k, (title, items) in enumerate(cols):
        x = x0 + k*step
        ax.text(x + bw/2, 47.6, title, ha='center', va='center', fontsize=7, fontweight='bold', color=INK)
        n = len(items); tot = n*bh + (n - 1)*gap; top = 23 + tot/2
        for i, t in enumerate(items):
            y = top - i*(bh + gap) - bh
            ax.add_patch(FancyBboxPatch((x, y), bw, bh, boxstyle='round,pad=0,rounding_size=0.9',
                                        fc='#fbefe8' if title == 'Outputs' else '#eef3f7', ec=AXIS, lw=0.5))
            ax.text(x + bw/2, y + bh/2, t, ha='center', va='center', fontsize=5.5, color=INK, linespacing=1.25)
        if k < 3:
            ax.annotate('', xy=(x + step - 0.2, 23), xytext=(x + bw + 0.2, 23),
                        arrowprops=dict(arrowstyle='-|>', lw=0.9, color=INK2, mutation_scale=9))
    save(fig, 'figure_s1_workflow')


def s2(c):
    """Sentinel-2 NDVI change around three settlements and other change indices by damage grade."""
    s2dir = ROOT/'sources_ext'/'s2'
    fig = plt.figure(figsize=(W2, 116*MM))
    gs = GridSpec(1, 3, figure=fig, top=0.98, bottom=0.555, wspace=0.25)
    gb = GridSpec(1, 3, figure=fig, top=0.445, bottom=0.05, wspace=0.40)
    sites = [('Timure', (85.369, 28.252)), ('Syaphrubesi', (85.343, 28.161)), ('Trishuli Bazar', (85.147, 27.920))]
    for j, (nm, ll) in enumerate(sites):
        ax = fig.add_subplot(gs[j])
        x0, y0 = PROJ(*ll); Bz = (x0 - 2200, y0 - 2200, x0 + 2200, y0 + 2200)
        dn = raster_window(s2dir/'s2_delta_ndvi.tif', Bz)
        dem = raster_window(DER/'dem_utm30.tif', Bz)
        ax.imshow(soft_hillshade(dem), cmap='Greys_r', extent=extent(Bz), vmin=0, vmax=1, alpha=0.55)
        ax.imshow(np.where(np.isnan(dn), 1.0, np.nan), cmap=LinearSegmentedColormap.from_list('nd', [NODATA, NODATA]),
                  extent=extent(Bz), alpha=0.75, interpolation='nearest')
        im = ax.imshow(np.ma.masked_where(~(np.abs(dn) >= 0.1), dn), cmap='RdBu', vmin=-1, vmax=1,
                       extent=extent(Bz), interpolation='nearest')
        add_geom(ax, c['flood'].intersection(box(*Bz)).boundary, color=INK, lw=0.6)
        ax.set_xlim(Bz[0], Bz[2]); ax.set_ylim(Bz[1], Bz[3]); clean_map(ax)
        scalebar(ax, 1, x=0.05, y=0.05, scale=1.0, label='1 km')
        ax.text(0.03, 0.96, nm, transform=ax.transAxes, fontsize=6, va='top',
                bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.9))
        if j == 0:
            panel(ax, 'a', x=-0.02, y=1.02)
    pos = fig.axes[2].get_position()
    cax = fig.add_axes([pos.x1 + 0.015, pos.y0 + 0.03, 0.011, pos.height - 0.06])
    cb = fig.colorbar(im, cax=cax); cb.set_label('NDVI change (|Δ| ≥ 0.1)', fontsize=5.6); cb.ax.tick_params(labelsize=5)
    fig.legend(handles=[Patch(fc=NODATA, ec='none', label='No clear observation in one or both composites'),
                        Line2D([], [], color=INK, lw=0.8, label='UNOSAT flow extent')],
               loc='upper center', bbox_to_anchor=(0.5, pos.y0 - 0.012), ncol=2, fontsize=5.6, frameon=False)
    s2 = pd.read_parquet(DER/'s2_building_samples.parquet')
    s2['level'] = np.maximum(s2.reg_level, s2.cems_level)
    auc = pd.read_csv(TAB/'s2_separability_auc.csv').set_index(['index', 'target']).auc
    for j, (k, lab) in enumerate([('d_bright', 'Visible brightness change'), ('d_ndwi', 'NDWI change'),
                                  ('d_bsi', 'Bare-soil index change')]):
        ax = fig.add_subplot(gb[j])
        for lev in range(4):
            v = s2.loc[s2.level == lev, k].dropna().to_numpy()
            q = np.percentile(v, [10, 25, 50, 75, 90])
            ax.plot([lev, lev], [q[0], q[4]], color=DMG[lev], lw=0.8)
            ax.add_patch(Rectangle((lev - 0.3, q[1]), 0.6, q[3] - q[1], fc=DMG[lev], ec='none'))
            ax.plot([lev - 0.3, lev + 0.3], [q[2], q[2]], color='white' if lev >= 2 else INK, lw=1)
        ax.set_xticks(range(4), ['None', 'Possibly', 'Damaged', 'Destroyed'], fontsize=5.2)
        ax.set_ylabel(lab)
        ax.set_title(f'AUC, destroyed vs other: {auc[(k[2:], "destroyed vs not (all assessed)")]:.2f}',
                     fontsize=5.8, fontweight='normal')
        hgrid(ax)
        if j == 0:
            panel(ax, 'b', x=-0.25, y=1.02)
    save(fig, 'figure_s2_sentinel2')


def s3(c):
    """Model diagnostics: calibration, one-way partial dependence and the height x chainage interaction."""
    fig = plt.figure(figsize=(W2, 112*MM))
    gs = GridSpec(2, 3, figure=fig, wspace=0.42, hspace=0.48)
    ax = fig.add_subplot(gs[0, 0])
    cal = pd.read_csv(TAB/'ml_calibration.csv')
    ax.plot([0, 1], [0, 1], color=MUTED, lw=0.7, ls='--')
    ax.plot(cal.p_mean, cal.y_mean, 'o-', color=INK, ms=3, lw=1)
    ax.set_xlabel('Mean predicted probability'); ax.set_ylabel('Observed share destroyed')
    ax.set_title('Calibration, out-of-fold deciles', fontsize=6, fontweight='normal')
    hgrid(ax); panel(ax, 'a', x=-0.25)
    pdp = pd.read_csv(TAB/'ml_partial_dependence.csv')
    for (f_, lab), slot, letter in zip([('rem_m', 'Height above channel (m)'), ('dist_channel_m', 'Distance to channel (m)'),
                                        ('chainage_km', 'Distance downstream (km)'), ('valley_width_20m', 'Valley-floor width <20 m (m)')],
                                       [gs[0, 1], gs[0, 2], gs[1, 0], gs[1, 1]], 'bcde'):
        ax = fig.add_subplot(slot)
        g = pdp[pdp.feature == f_]
        ax.plot(g.value, logistic(g.pd), color=BLUE[11], lw=1.2)
        ax.set_ylim(0, 1); ax.set_xlabel(lab); ax.set_ylabel('Partial dependence, P(destroyed)')
        hgrid(ax); panel(ax, letter, x=-0.25)
    ax = fig.add_subplot(gs[1, 2])
    p2 = pd.read_csv(TAB/'ml_partial_dependence_2d.csv')
    piv = p2.pivot(index='rem_m', columns='chainage_km', values='pd')
    P = logistic(piv.values)
    im = ax.pcolormesh(piv.columns, piv.index, P, cmap=CM_BLUE, shading='auto', vmin=0, vmax=1, rasterized=True)
    ax.contour(piv.columns, piv.index, P, levels=[0.5], colors='white', linewidths=1.0)
    ax.text(45, 12, 'P = 0.5', color='white', fontsize=5.2, ha='center', va='center')
    ax.set_xlabel('Distance downstream (km)'); ax.set_ylabel('Height above channel (m)')
    cb = fig.colorbar(im, ax=ax, fraction=0.05, pad=0.03); cb.set_label('P(destroyed)', fontsize=5.6); cb.ax.tick_params(labelsize=5)
    panel(ax, 'f', x=-0.25)
    save(fig, 'figure_s3_model_diagnostics')


def s4(c):
    """HOT confidence scores and positional sensitivity (retained from the first analysis)."""
    df = pd.read_csv(ROOT/'data'/'building_analysis.csv')
    conf = pd.read_csv(TAB/'confidence_sensitivity.csv')
    pos = pd.read_csv(TAB/'position_sensitivity.csv')
    fig = plt.figure(figsize=(W2, 58*MM))
    gs = GridSpec(1, 3, figure=fig, wspace=0.40)
    ax = fig.add_subplot(gs[0])
    for cls, k in [('no-damage', 0), ('minor-damage', 1), ('major-damage', 2), ('destroyed', 3)]:
        v = np.sort(df.loc[df.damage == cls, 'damage_confidence'].dropna())
        ax.plot(v, np.arange(1, len(v) + 1)/len(v), color=DMG[k], lw=1.2, label=f"{cls.replace('-', ' ')} ({len(v)})")
    ax.set_xlabel('HOT confidence score'); ax.set_ylabel('Cumulative share within class')
    ax.legend(fontsize=5.2, loc='center', bbox_to_anchor=(0.585, 0.42), handlelength=1.2)
    hgrid(ax); panel(ax, 'a', x=-0.25)
    ax = fig.add_subplot(gs[1])
    ax.plot(conf.threshold, conf.coverage_percent, 'o-', color=BLUE[8], ms=3, lw=1, label='Records retained')
    ax.plot(conf.threshold, conf.severe_percent_retained, 's-', color=DESTROYED, ms=3, lw=1, label='Severe among retained')
    ax.set_xlabel('Minimum confidence score'); ax.set_ylabel('Percent'); ax.set_ylim(0, 105)
    ax.legend(fontsize=5.2, loc='lower left'); hgrid(ax); panel(ax, 'b', x=-0.25)
    ax = fig.add_subplot(gs[2])
    o = pos[pos.direction == 'original'].iloc[0]; sh = pos[pos.direction != 'original'].reset_index(drop=True)
    xs = np.arange(len(sh))
    for col, lab, mk, colr, dx in [('unosat_members', f'Inside UNOSAT extent (original {o.unosat_members})', 'o', BLUE[8], -0.12),
                                   ('severe_inside', f'Severe inside extent (original {o.severe_inside})', 's', DESTROYED, 0.12)]:
        dv = sh[col] - o[col]
        ax.vlines(xs + dx, 0, dv, color=colr, lw=1)
        ax.plot(xs + dx, dv, mk, color=colr, ms=3.6, label=lab)
    ax.axhline(0, color=AXIS, lw=0.6)
    ax.set_xticks(xs, [d.capitalize() for d in sh.direction], fontsize=5.4)
    ax.set_ylim(-6, 6); ax.set_ylabel('Change after 5-m shift (buildings)')
    ax.legend(fontsize=5.0, loc='lower left'); hgrid(ax); panel(ax, 'c', x=-0.25)
    save(fig, 'figure_s6_hot_checks')


def s5(c):
    """Debris uncertainty and rank robustness."""
    draws = np.load(DER/'debris_mc_draws.npy')
    ranks = np.load(DER/'municipal_rank_draws.npy')
    rk = pd.read_csv(TAB/'municipal_rank_uncertainty.csv')
    ind = pd.read_csv(TAB/'municipal_indicators.csv').reset_index(drop=True)
    ir = json.loads((DER/'impacts_results.json').read_text())['debris']
    u_cs, u_all = undp_debris_kt()
    fig = plt.figure(figsize=(W2, 70*MM))
    gs = GridSpec(1, 3, figure=fig, width_ratios=[1, 1, 1.5], wspace=0.42)
    ax = fig.add_subplot(gs[0])
    ax.hist(draws[:, 0]/1e3, bins=40, color=BLUE[3], ec='none')
    ax.set_ylim(0, ax.get_ylim()[1]*1.45)
    ax.axvline(ir['debris_central_t']/1e3, ymax=0.72, color=INK, lw=1.1)
    ax.axvline(ir['debris_no_settlement_factor_t']/1e3, ymax=0.72, color=INK2, lw=1.0, ls=':')
    for v in (u_cs, u_all):
        ax.axvline(v, ymax=0.72, color=INK2, lw=0.9, ls='--')
    ax.set_xlabel('Building debris (kt)'); ax.set_ylabel('Monte Carlo draws')
    ax.legend(handles=[Line2D([], [], color=INK, lw=1.1, label=f'Central, UNDP factors ({ir["debris_central_t"]/1e3:,.0f})'),
                       Line2D([], [], color=INK2, lw=1.0, ls=':', label=f'No settlement factor ({ir["debris_no_settlement_factor_t"]/1e3:,.0f})'),
                       Line2D([], [], color=INK2, lw=0.9, ls='--', label=f'UNDP RAPIDA ({u_cs:,.0f}; {u_all:,.0f})')],
              fontsize=4.9, loc='upper right', frameon=False)
    hgrid(ax); panel(ax, 'a', x=-0.25)
    ax = fig.add_subplot(gs[1])
    ax.hist(100*draws[:, 1], bins=40, color=BLUE[3], ec='none')
    ax.axvline(100*ir['bidur_share_central'], color=INK, lw=1.1)
    ax.axvline(100*ir['bidur_share_no_factor'], color=INK2, lw=1.0, ls=':')
    ax.set_xlim(40, 64); ax.set_ylim(0, ax.get_ylim()[1]*1.15)
    ax.set_xlabel('Bidur share of debris (%)'); ax.set_ylabel('Monte Carlo draws')
    hgrid(ax); panel(ax, 'b', x=-0.25)
    ax = fig.add_subplot(gs[2])
    order = rk.municipality.tolist()
    idx = [ind.index[ind.municipality == m][0] for m in order]
    n = len(order)
    P = np.array([[np.mean(ranks[:, i] == r) for r in range(1, n + 1)] for i in idx])
    cmap = CM_BLUE.copy(); cmap.set_bad('white')
    im = ax.imshow(np.ma.masked_less(P, 0.005), cmap=cmap, vmin=0, vmax=1, aspect='auto', interpolation='nearest')
    ax.set_yticks(range(n), order, fontsize=5.0); ax.set_xticks(range(0, n, 2), range(1, n + 1, 2), fontsize=5)
    ax.set_xlabel('Rank'); ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
    cb = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02); cb.set_label('Probability', fontsize=5.6); cb.ax.tick_params(labelsize=5)
    panel(ax, 'c', x=-0.30)
    save(fig, 'figure_s5_debris_rank')


def s6(c):
    """Reach-level relationships: destructive height against valley width and front celerity; example cross-sections."""
    env = robust_reach_heights(pd.read_csv(TAB/'terrain_envelope_by_reach.csv'))
    tl = pd.read_csv(TAB/'timing_wave_arrivals.csv'); a_ = tl[tl.arrival]
    cel = np.interp(env.reach_mid_km, (a_.chainage_km.values[:-1] + a_.chainage_km.values[1:])/2,
                    a_.celerity_from_previous_m_s.values[1:])
    fig = plt.figure(figsize=(W2, 62*MM))
    gs = GridSpec(1, 3, figure=fig, wspace=0.38)
    for j, (x, lab) in enumerate([(env.valley_width_20m_median, 'Valley-floor width <20 m (m)'),
                                  (cel, 'Front celerity (m s$^{-1}$)')]):
        ax = fig.add_subplot(gs[j])
        sc = ax.scatter(x, env.h_core, c=env.reach_mid_km, cmap=CM_BLUE_R, vmin=0, vmax=120, s=24, ec=INK, lw=0.4, zorder=3)
        r, _ = spearmanr(x, env.h_core)
        ax.set_xlabel(lab); ax.set_ylabel('Damage-calibrated height (m)')
        ax.set_title(f'Spearman ρ = {r:.2f} (n = {len(env)} reaches)', fontsize=6, fontweight='normal')
        hgrid(ax); panel(ax, 'ab'[j], x=-0.25)
    cax = ax.inset_axes([0.50, 0.16, 0.44, 0.035])
    cb = fig.colorbar(sc, cax=cax, orientation='horizontal'); cb.ax.tick_params(labelsize=5, length=2)
    cb.set_label('Reach midpoint (km downstream)', fontsize=5.2, labelpad=1)
    ax = fig.add_subplot(gs[2])
    ch = c['ch']
    with rasterio.open(DER/'rem_utm30.tif') as s:
        rem = s.read(1); T = s.transform
    for km, col, nm, va, dy in [(26, BLUE[12], 'gorge', 'bottom', 1.5), (79, BLUE[6], 'valley', 'top', -2.0)]:
        i = int(np.argmin(np.abs(ch.chain/1000 - km)))
        nx, ny = -ch.ty[i], ch.tx[i]
        offs = np.arange(-800, 801, 15)
        rr, cc = rasterio.transform.rowcol(T, ch.xy[i, 0] + offs*nx, ch.xy[i, 1] + offs*ny)
        ax.plot(offs, rem[np.array(rr), np.array(cc)], color=col, lw=1.1)
        hz = float(np.interp(km, env.reach_mid_km, env.h_core))
        ax.axhline(hz, color=col, lw=0.7, ls='--')
        ax.text(-785, hz + dy, f'{hz:.0f} m', fontsize=5.2, color=col, va=va, ha='left', path_effects=HALO)
    ax.set_xlabel('Distance across valley (m; left bank positive)'); ax.set_ylabel('Height above channel (m)')
    ax.set_xlim(-800, 800); ax.set_ylim(-5, 160)
    ax.text(395, 150, '26 km (gorge)', fontsize=5.4, color=BLUE[12], ha='left', va='center', path_effects=HALO)
    ax.text(790, 77, '79 km (valley)', fontsize=5.4, color=BLUE[6], ha='right', va='bottom', path_effects=HALO)
    hgrid(ax); panel(ax, 'c', x=-0.25)
    save(fig, 'figure_s4_reach_physics')


FIGS = dict(s1=s1, s2=s2, s3=s3, s4=s6, s5=s5, s6=s4)   # s4 = reach relationships, s6 = HOT checks

if __name__ == '__main__':
    c = load_common()
    for k in (sys.argv[1:] or list(FIGS)):
        FIGS[k](c); print('rendered', k)
