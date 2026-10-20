"""Main and supplementary figures for the revised manuscript.

Run all:      python scripts/figures_v2.py
Run a subset: python scripts/figures_v2.py fig1 fig3
"""
import sys
import json
import numpy as np
import pandas as pd
import shapely
from shapely.geometry import shape, box
from shapely.ops import transform, unary_union
from pyproj import Transformer
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle
from figstyle import (ROOT, DER, W1, W2, MM, INK, INK2, MUTED, GRID, AXIS, DMG, DMG_LABEL, DAMAGED, DESTROYED, SRC,
                      CM_BLUE, CM_BLUE_R, BLUE, FLOW, RIVER, save, panel, hgrid, raster_window, extent, add_geom,
                      scalebar, north, clean_map)
from corridor import Channel, PLACES
from analyse import read, read_shape_zip, SRC as V1SRC

TAB = ROOT/'tables'
PROJ = Transformer.from_crs('OGC:CRS84', 'EPSG:32645', always_xy=True).transform
TOLL = Transformer.from_crs('EPSG:32645', 'EPSG:4326', always_xy=True)


def load_common():
    c = {}
    c['ch'] = Channel()
    c['flood'], _, _ = read_shape_zip(V1SRC/'unosat_3.html')
    c['inv'] = pd.read_parquet(DER/'harmonised_inventory.parquet')
    adm = json.loads((V1SRC/'boundaries_adm3.json').read_text(encoding='utf-8'))['features']
    c['adm3'] = [(f['properties']['shapeName'], transform(PROJ, shape(f['geometry']))) for f in adm]
    adm2 = json.loads((V1SRC/'boundaries_adm2.json').read_text(encoding='utf-8'))['features']
    c['nepal'] = unary_union([shape(f['geometry']) for f in adm2]).buffer(0)
    return c


def place_xy(name):
    lo, la = PLACES[name]
    return PROJ(lo, la)


def map_label(ax, x, y, text, dx, dy, ha='left', fs=5.6):
    ax.plot(x, y, 'o', ms=2.8, mfc='white', mec=INK, mew=0.6, zorder=9)
    ax.annotate(text, (x, y), xytext=(x + dx, y + dy), fontsize=fs, color=INK, zorder=10, ha=ha, va='center',
                arrowprops=dict(arrowstyle='-', lw=0.4, color=INK2, shrinkA=0, shrinkB=2),
                bbox=dict(boxstyle='round,pad=0.18', fc='white', ec='none', alpha=0.88))


# ---------------------------------------------------------------------------------------------
def fig1(c):
    """Corridor overview: map, along-channel profile, damage density, casualty series."""
    ch, inv, flood = c['ch'], c['inv'], c['flood']
    B = (243500, 3063000, 362000, 3138500)                 # UTM 45N map window (m)
    fig = plt.figure(figsize=(W2, 184*MM))
    gs = GridSpec(2, 1, figure=fig, height_ratios=[1.86, 1], hspace=0.09)
    ax = fig.add_subplot(gs[0])
    hs = raster_window(DER/'hillshade_utm30.tif', B)
    ax.imshow(hs, cmap='Greys_r', extent=extent(B, 1/1000), vmin=30, vmax=255, alpha=0.95, zorder=0,
              interpolation='bilinear')
    for name, g in c['adm3']:
        if g.intersects(box(*B)):
            add_geom(ax, g.boundary.intersection(box(*B)), scale=1/1000, color='white', lw=0.3, alpha=0.7, zorder=2)
    npl = transform(PROJ, c['nepal'])
    add_geom(ax, npl.boundary.intersection(box(*B)), scale=1/1000, color=INK, lw=0.9, zorder=3)
    add_geom(ax, flood.intersection(box(*B)), scale=1/1000, facecolor=FLOW, edgecolor='none', alpha=0.6, zorder=4)
    xy = ch.xy/1000
    ax.plot(xy[:, 0], xy[:, 1], color=RIVER, lw=0.9, zorder=5, solid_capstyle='round')
    d = inv[inv.max_level >= 1]
    dd = d[d.max_level < 3]; dz = d[d.max_level == 3]
    ax.scatter(dd.x/1000, dd.y/1000, s=1.0, c=DAMAGED, lw=0, zorder=6, rasterized=True)
    ax.scatter(dz.x/1000, dz.y/1000, s=1.0, c=DESTROYED, lw=0, zorder=7, rasterized=True)
    chain_of = ch.place_chainage()
    labels = {'Source': (-3, 4.5, 'right'), 'Rasuwagadhi': (-4, 3, 'right'), 'Syaphrubesi': (4, -2, 'left'),
              'Betrawati': (4, 2.5, 'left'), 'Trishuli Bazar': (5, -2.5, 'left'), 'Galchhi': (-3, -5.5, 'right'),
              'Benighat': (-3, 6, 'center'), 'Mugling': (2, 6.5, 'center'), 'Devghat': (7, 3.5, 'left')}
    for name, (dx, dy, ha) in labels.items():
        x, y = place_xy(name)
        lab = f'{name} ({chain_of[name]:.0f} km)' if name != 'Source' else 'Source (0 km)'
        map_label(ax, x/1000, y/1000, lab, dx, dy, ha)
    ax.text(331, 3135.8, 'CHINA (Tibet AR)', fontsize=6, color=INK, ha='center', style='italic', zorder=10,
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.75))
    ax.text(292, 3101, 'NEPAL', fontsize=6.5, color=INK, ha='center', style='italic', zorder=10,
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.75))
    ax.text(351.5, 3121.6, 'Langtang Lirung', fontsize=5.3, color=INK2, ha='center', style='italic', zorder=10,
            bbox=dict(boxstyle='round,pad=0.12', fc='white', ec='none', alpha=0.8))
    ax.set_xlim(B[0]/1000, B[2]/1000); ax.set_ylim(B[1]/1000, B[3]/1000)
    clean_map(ax)
    scalebar(ax, 20, x=0.22, y=0.035); north(ax, x=0.97, y=0.06, size=0.07)
    leg = [Line2D([], [], color=RIVER, lw=1, label='Traced flow path (207 km)'),
           Patch(fc=FLOW, alpha=0.6, label='Mapped flow extent (UNOSAT, 26-27 Aug)'),
           Line2D([], [], ls='', marker='o', ms=3, mfc=DESTROYED, mec='none', label='Destroyed building (≥1 product)'),
           Line2D([], [], ls='', marker='o', ms=3, mfc=DAMAGED, mec='none', label='Damaged building'),
           Line2D([], [], color=INK, lw=0.9, label='International border')]
    ax.legend(handles=leg, loc='lower right', bbox_to_anchor=(0.94, 0.0), fontsize=5.6, frameon=True, framealpha=0.92,
              edgecolor='none', borderpad=0.5, handletextpad=0.5)
    panel(ax, 'a', x=-0.005, y=1.0)
    ins = ax.inset_axes([0.005, 0.70, 0.26, 0.295])
    add_geom(ins, c['nepal'], facecolor='#efeeea', edgecolor=INK2, lw=0.4)
    bb = shapely.geometry.box(*TOLL.transform(B[0], B[1]), *TOLL.transform(B[2], B[3]))
    add_geom(ins, bb, facecolor='none', edgecolor=DESTROYED, lw=0.9)
    ins.text(82.0, 27.4, 'Nepal', fontsize=5.5, color=INK2, ha='center')
    ins.set_xlim(80, 88.3); ins.set_ylim(26.2, 30.6); ins.set_aspect('equal')
    ins.set_xticks([]); ins.set_yticks([])
    for sp in ins.spines.values():
        sp.set_visible(True); sp.set_color(AXIS); sp.set_linewidth(0.4)
    ins.set_facecolor('white')
    # lower row: along-channel profile, damage density, casualty reporting
    low = GridSpecFromSubplotSpec(2, 2, subplot_spec=gs[1], width_ratios=[1.75, 1], height_ratios=[1, 1.1],
                                  hspace=0.12, wspace=0.22)
    p = ch.p
    axb = fig.add_subplot(low[0, 0])
    axb.fill_between(p.chainage_m/1000, 0, p.z_channel, color='#e9e7e1', lw=0)
    axb.plot(p.chainage_m/1000, p.z_channel, color=INK, lw=0.8)
    for name in ['Rasuwagadhi', 'Syaphrubesi', 'Betrawati', 'Trishuli Bazar', 'Galchhi', 'Benighat', 'Mugling', 'Devghat']:
        k = chain_of[name]; z = np.interp(k*1000, p.chainage_m, p.z_channel)
        axb.plot([k, k], [z + 80, 5200], color=GRID, lw=0.5, zorder=0)
        axb.text(k + 1.2, 5150, name, rotation=90, fontsize=5, ha='left', va='top', color=INK2)
    axb.set_xlim(0, 207); axb.set_ylim(0, 5300)
    axb.set_ylabel('Channel\nelevation (m)')
    plt.setp(axb.get_xticklabels(), visible=False)
    axb.set_yticks([0, 2000, 4000])
    panel(axb, 'b', x=-0.085, y=0.92)
    axc = fig.add_subplot(low[1, 0], sharex=axb)
    for (a, b_) in [(21, 41), (64, 114)]:
        axc.axvspan(a, b_, color='#f4f3ef', zorder=0, lw=0)
    bins = np.arange(0, 210, 2)
    hd = np.histogram(dd.chainage_km, bins)[0]
    hz = np.histogram(dz.chainage_km, bins)[0]
    axc.bar(bins[:-1] + 1, hz, width=1.7, color=DESTROYED, lw=0, label='Destroyed', zorder=2)
    axc.bar(bins[:-1] + 1, hd, width=1.7, bottom=hz, color=DAMAGED, lw=0, label='Damaged', zorder=2)
    axc.set_ylabel('Buildings\nper 2 km')
    mi = pd.read_csv(TAB/'municipal_indicators.csv')
    down = mi[(mi.sat_damaged.fillna(0) <= 20) & (mi.chainage_median_km > 114)].rdna_affected_buildings.sum()
    axc.text(160, 330, f'No satellite damage grading downstream of 114 km;\nRDNA reports {down:,.0f} affected buildings here',
             fontsize=5.2, ha='center', va='center', color=INK2)
    axc.text(31, 560, 'graded\nreaches', fontsize=5, ha='center', color=MUTED)
    axc.legend(loc='upper right', fontsize=5.5, bbox_to_anchor=(1.0, 1.05))
    axc.set_xlabel('Distance downstream of source (km)')
    axc.set_ylim(0, 650)
    hgrid(axc)
    panel(axc, 'c', x=-0.085, y=0.92)
    cs = pd.read_csv(TAB/'casualty_series.csv', parse_dates=['date'])
    axd = fig.add_subplot(low[:, 1])
    m = cs.dropna(subset=['deaths']); m2 = cs.dropna(subset=['missing'])
    axd.plot(m2.date, m2.missing, color=SRC['RDNA'], lw=1.0, marker='o', ms=2.3, mfc=SRC['RDNA'], mec='white', mew=0.3)
    axd.plot(m.date, m.deaths, color=INK, lw=1.0, marker='o', ms=2.3, mfc=INK, mec='white', mew=0.3)
    axd.text(m2.date.iloc[-1], m2.missing.iloc[-1] - 650, f'{int(m2.missing.iloc[-1]):,} missing', ha='right',
             fontsize=5.6, color=INK)
    axd.text(m.date.iloc[-1], m.deaths.iloc[-1] + 330, f'{int(m.deaths.iloc[-1]):,} confirmed deaths', ha='right',
             fontsize=5.6, color=INK)
    axd.text(m.date.iloc[0], 6650, 'Nepal; NDRRMA-reported,\n26 Aug to 3 Oct 2026', fontsize=5.3, color=INK2, va='top')
    axd.set_ylim(0, 7000); axd.set_ylabel('People')
    axd.set_yticks([0, 2000, 4000, 6000]); axd.set_yticklabels(['0', '2K', '4K', '6K'])
    axd.xaxis.set_major_locator(mdates.DayLocator(bymonthday=[1, 15]))
    axd.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    hgrid(axd)
    panel(axd, 'd', x=-0.12, y=0.97)
    save(fig, 'figure_1_overview')


def fig2(c):
    """Multi-product damage synthesis: coverage, counts, agreement, comparison with the RDNA."""
    inv = c['inv']
    dash = json.loads((ROOT/'sources_ext'/'cems'/'EMSR927_dashboard.json').read_text(encoding='utf-8'))['results'][0]
    fig = plt.figure(figsize=(W2, 196*MM))
    gs = GridSpec(3, 2, figure=fig, width_ratios=[1.3, 1], height_ratios=[1, 1.05, 1.0], wspace=0.34, hspace=0.45)
    # a: where each product graded buildings along the corridor
    ax = fig.add_subplot(gs[0, 0])
    yH, yC, yU, yR = 3, 2, 1, 0
    h = inv[inv.hot_class >= 0]
    ax.add_patch(Rectangle((h.chainage_km.min(), yH - 0.26), h.chainage_km.max() - h.chainage_km.min(), 0.52,
                           fc=SRC['HOT'], ec='none'))
    ax.text(h.chainage_km.max() + 2, yH, 'n = 1,053 graded footprints', va='center', fontsize=5.2, color=INK2)
    names = {1: 'AOI1\nSyaphrubesi', 2: 'AOI2\nTimure', 3: 'AOI3 Bidur', 5: 'AOI5 Phosretar'}
    for a in dash['aois']:
        prods = [p for p in a['products'] if (p.get('stats') or {}).get('Built-up')]
        if not prods:
            continue
        pts = inv[(inv.cems_aoi == a['number'])]
        lo_, hi_ = pts.chainage_km.quantile(.005), pts.chainage_km.quantile(.995)
        ax.add_patch(Rectangle((lo_, yC - 0.26), hi_ - lo_, 0.52, fc=SRC['CEMS'], ec='none'))
        above = a['number'] in (2, 3)
        ax.text((lo_ + hi_)/2, yC + (0.33 if above else -0.33), names[a['number']].replace(chr(10), ' '),
                ha='center', va='bottom' if above else 'top', fontsize=4.8, color=INK2)
    ax.add_patch(Rectangle((0, yU - 0.26), 106, 0.52, fc=SRC['UNOSAT'], ec='none', alpha=0.35))
    u = inv[inv.reg_source == 'UNOSAT_FL20260826NPL']
    ax.vlines(u.chainage_km, yU - 0.26, yU + 0.26, color=SRC['UNOSAT'], lw=0.25, alpha=0.9)
    ax.text(107.5, yU, 'flow extent mapped;\n684 destroyed records (ticks)', va='center', fontsize=5.0, color=INK2)
    rd = pd.read_csv(TAB/'municipal_indicators.csv')
    alias = {'Tarakeshwor': 'Tarkeshwar', 'Galchhi': 'Galchi', 'Shahid Lakhan': 'Sahid Lakhan'}
    for _, r in rd[rd.rdna_affected_buildings.notna()].iterrows():
        sub = inv[(inv.municipality == alias.get(r.municipality, r.municipality)) & (inv.dist_channel_m <= 500)]
        if len(sub) < 5:
            continue
        a_, b_ = sub.chainage_km.quantile(.02), sub.chainage_km.quantile(.98)
        ax.add_patch(Rectangle((a_, yR - 0.22), b_ - a_, 0.44, fc=SRC['RDNA'], ec='white', lw=0.4, alpha=0.75))
    ax.text(0, yR + 0.42, 'local levels reported in the RDNA (15)', fontsize=5.0, color=INK2, va='bottom')
    for y_, lab in [(yH, 'HOT (AI-assisted)'), (yC, 'Copernicus EMS'), (yU, 'UNOSAT'), (yR, 'Official RDNA')]:
        ax.text(-4, y_, lab, ha='right', va='center', fontsize=5.8, color=INK)
    ax.axvspan(114, 207, ymin=0.25, color='#f4f3ef', lw=0, zorder=0)
    ax.text(160, 2.5, 'no satellite building\ngrading downstream', ha='center', va='center', fontsize=5.0, color=INK2)
    ax.set_xlim(0, 207); ax.set_ylim(-0.6, 3.55)
    ax.set_yticks([]); ax.spines['left'].set_visible(False)
    ax.set_xlabel('Distance downstream of source (km)')
    hgrid(ax, 'x')
    panel(ax, 'a', x=-0.30, y=1.0)
    # b: counts per product, harmonised union and the official count
    axb = fig.add_subplot(gs[0, 1])
    pr = pd.read_csv(TAB/'products_summary.csv')
    lab = ['HOT', 'CEMS (latest)', 'UNDP: CEMS', 'UNDP: SERTIT', 'UNDP: UNOSAT', 'Union (≥1 product)',
           'Destroyed in ≥2', 'Official RDNA']
    des = np.r_[pr.destroyed.to_numpy(), 0]
    dam = np.r_[(pr.damaged.fillna(pr.destroyed) - pr.destroyed).clip(lower=0).to_numpy(), 0]
    yv = np.arange(len(lab))[::-1]
    axb.barh(yv, des, height=0.62, color=DESTROYED, lw=0, label='Destroyed')
    axb.barh(yv, dam, left=des, height=0.62, color=DAMAGED, lw=0, label='Other damage grades')
    axb.barh(yv[-1], 7570, height=0.62, color=SRC['RDNA'], lw=0, label='Affected (official)')
    tot = list(des + dam); tot[-1] = 7570
    for y_, t_ in zip(yv, tot):
        axb.text(t_ + 90, y_, f'{int(t_):,}', va='center', fontsize=5.4, color=INK)
    axb.axhline(2.5, color=GRID, lw=0.6)
    axb.set_yticks(yv, lab); axb.tick_params(axis='y', length=0)
    axb.set_xlim(0, 8600); axb.set_xticks([0, 2000, 4000, 6000, 8000], ['0', '2K', '4K', '6K', '8K'])
    axb.set_xlabel('Buildings')
    axb.legend(loc='center right', fontsize=5.3, bbox_to_anchor=(1.02, 0.60))
    hgrid(axb, 'x')
    panel(axb, 'b', x=-0.38, y=1.0)
    # c: HOT vs CEMS agreement on the same buildings
    axc = fig.add_subplot(gs[1, 0])
    ct = pd.read_csv(TAB/'agreement_hot_cems.csv', index_col=0)
    rows_o = ['HOT no damage', 'HOT minor', 'HOT major', 'HOT destroyed']
    cols_o = ['CEMS no record', 'CEMS possibly damaged', 'CEMS damaged', 'CEMS destroyed']
    ct = ct.reindex(index=rows_o, columns=cols_o).fillna(0)
    pct = ct.div(ct.sum(axis=1), axis=0)*100
    axc.imshow(pct.to_numpy(), cmap=CM_BLUE, vmin=0, vmax=100, aspect='auto')
    for i in range(4):
        for j in range(4):
            v = pct.iat[i, j]; n = int(ct.iat[i, j])
            axc.text(j, i, f'{v:.0f}%\n({n})', ha='center', va='center', fontsize=5.3,
                     color='white' if v > 55 else INK)
    axc.set_xticks(range(4), ['No record', 'Possibly\ndamaged', 'Damaged', 'Destroyed'])
    axc.set_yticks(range(4), ['No damage', 'Minor', 'Major', 'Destroyed'])
    axc.set_xlabel('CEMS EMSR927 grade (same buildings)'); axc.set_ylabel('HOT label')
    axc.tick_params(length=0)
    for sp in axc.spines.values():
        sp.set_visible(False)
    res = json.loads((DER/'products_results.json').read_text())
    axc.set_title(f"n = {res['n']} buildings graded by both; Cohen’s κ (destroyed) = {res['kappa_destroyed']:.2f}",
                  fontweight='normal', fontsize=6)
    panel(axc, 'c', x=-0.22, y=1.04)
    # d: satellite union vs official RDNA by local level
    axd = fig.add_subplot(gs[1, 1])
    ind = pd.read_csv(TAB/'municipal_indicators.csv')
    ind = ind[ind.rdna_affected_buildings.notna()].copy()
    ind['sat'] = ind.sat_damaged.fillna(0)
    graded = ind.sat > 20
    lim = (8, 7000)
    axd.plot(lim, lim, color=MUTED, lw=0.6, zorder=1)
    axd.text(14, 18.5, '1:1', fontsize=5.2, color=MUTED, rotation=38)
    axd.scatter(ind.rdna_affected_buildings[graded], ind.sat[graded], s=18, color=SRC['CEMS'], ec='white', lw=0.5,
                zorder=3, label='Graded by satellite products')
    axd.scatter(ind.rdna_affected_buildings[~graded], np.full((~graded).sum(), 11), s=18, marker='v',
                color=SRC['RDNA'], ec='white', lw=0.5, zorder=3, label='Not graded (plotted at axis floor)')
    nudge = {'Bidur': (-4, 4, 'right', 'bottom'), 'Gosaikunda': (-4, 3, 'right', 'bottom'),
             'Kispang': (4, -1, 'left', 'bottom'), 'Uttargaya': (4, -5, 'left', 'bottom'),
             'Belkotgadhi': (0, -5, 'center', 'top'), 'Galchhi': (-4, 2, 'right', 'bottom'),
             'Tarakeshwor': (-4, 2, 'right', 'bottom'), 'Gajuri': (4, -4, 'left', 'bottom')}
    for _, r in ind[graded].iterrows():
        dx, dy, ha, va = nudge.get(r.municipality, (3, 2, 'left', 'bottom'))
        axd.annotate(r.municipality, (r.rdna_affected_buildings, r.sat), xytext=(dx, dy), textcoords='offset points',
                     fontsize=4.9, color=INK2, ha=ha, va=va)
    ug = ind[~graded].set_index('municipality').rdna_affected_buildings
    for names_ in (['Kalika', 'Ichchhyakamana'], ['Gandaki', 'Siddhalek'], ['Benighat Rorang']):
        xg = float(np.exp(np.log(ug[names_]).mean()))           # neighbouring triangles share one label
        axd.annotate(',\n'.join(names_), (xg, 11), xytext=(0, 6), textcoords='offset points', fontsize=4.5,
                     color=INK2, rotation=90, ha='center', va='bottom', linespacing=1.0)
    rat = (ind.sat[graded]/ind.rdna_affected_buildings[graded])
    axd.text(9.5, 1150, f'Graded local levels: median ratio {rat.median():.2f}', fontsize=4.9, color=INK2, va='top')
    axd.set_xscale('log'); axd.set_yscale('log')
    axd.set_xlim(*lim); axd.set_ylim(*lim)
    axd.set_xlabel('RDNA affected private buildings'); axd.set_ylabel('Satellite-graded damaged buildings')
    axd.legend(loc='upper left', fontsize=5.0, bbox_to_anchor=(-0.02, 1.02))
    panel(axd, 'd', x=-0.26, y=1.04)
    # e: Sentinel-2 true-colour pairs (gorge and valley)
    s2dir = ROOT/'sources_ext'/'s2'
    meta = json.loads((s2dir/'chips.json').read_text(encoding='utf-8'))
    sub = GridSpecFromSubplotSpec(2, 2, subplot_spec=gs[2, 0], wspace=0.04, hspace=0.10)
    for i, site in enumerate(['Syaphrubesi', 'Trishuli_Bazar']):
        for j, per in enumerate(['pre', 'post']):
            a = np.load(s2dir/f'chip_{per}_{site}.npy')
            rgb = np.transpose(a, (1, 2, 0))
            axi = fig.add_subplot(sub[i, j])
            axi.imshow(np.clip(rgb/0.20, 0, 1)**(1/1.5), interpolation='bilinear')   # one stretch for all chips
            axi.set_xticks([]); axi.set_yticks([])
            for sp in axi.spines.values():
                sp.set_visible(True); sp.set_color(AXIS); sp.set_linewidth(0.4)
            dt_ = meta[f"{per}_{site.replace('_', ' ')}"]['datetime'][:10]
            axi.text(0.03, 0.95, f"{site.replace('_', ' ')}, {dt_}", transform=axi.transAxes, fontsize=5.0, va='top',
                     color=INK, bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.85))
            if i == 0 and j == 0:
                panel(axi, 'e', x=-0.04, y=1.03)
            if i == 1:
                axi.plot([0.05, 0.05 + 1000/3200], [0.07, 0.07], transform=axi.transAxes, color='white', lw=1.2)
                axi.text(0.05 + 500/3200, 0.10, '1 km', transform=axi.transAxes, fontsize=4.8, color='white', ha='center')
    # f: NDVI change by damage grade
    axf = fig.add_subplot(gs[2, 1])
    s2 = pd.read_parquet(DER/'s2_building_samples.parquet')
    auc = pd.read_csv(TAB/'s2_separability_auc.csv')
    s2['level'] = np.maximum(s2.reg_level, s2.cems_level)
    groups = [('HOT', 0, s2[s2.hot_class == 0]), ('HOT', 1, s2[s2.hot_class == 1]), ('HOT', 2, s2[s2.hot_class == 2]),
              ('HOT', 3, s2[s2.hot_class == 3]), ('CEMS', 0, s2[(s2.level == 0) & (s2.hot_class < 0)]),
              ('CEMS', 1, s2[s2.level == 1]), ('CEMS', 2, s2[s2.level == 2]), ('CEMS', 3, s2[s2.level == 3])]
    pos = [0, 1, 2, 3, 5, 6, 7, 8]
    for p_, (prod, lev, g) in zip(pos, groups):
        v = g.d_ndvi.dropna().to_numpy()
        q = np.percentile(v, [10, 25, 50, 75, 90])
        col = DMG[lev]
        axf.plot([p_, p_], [q[0], q[4]], color=col, lw=0.8)
        axf.add_patch(Rectangle((p_ - 0.3, q[1]), 0.6, q[3] - q[1], fc=col, ec='none', alpha=0.9))
        axf.plot([p_ - 0.3, p_ + 0.3], [q[2], q[2]], color='white' if lev >= 2 else INK, lw=1.0)
        axf.text(p_, 0.15, f'{len(v):,}', fontsize=4.6, ha='center', color=INK2)
    axf.set_xticks(pos, ['None', 'Minor', 'Major', 'Destr.', 'None', 'Poss.', 'Dam.', 'Destr.'], fontsize=5.0)
    a1 = auc[(auc['index'] == 'ndvi') & auc.target.str.startswith('HOT')].auc.iloc[0]
    a2 = auc[(auc['index'] == 'ndvi') & auc.target.str.startswith('destroyed vs no record')].auc.iloc[0]
    axf.text(1.5, 0.215, f'HOT (AUC {a1:.2f})', fontsize=5.4, ha='center', color=INK)
    axf.text(6.5, 0.215, f'CEMS/UNDP (AUC {a2:.2f})', fontsize=5.4, ha='center', color=INK)
    axf.axhline(0, color=MUTED, lw=0.5)
    axf.set_ylim(-0.72, 0.27); axf.set_xlim(-0.7, 8.7)
    axf.set_ylabel('Sentinel-2 NDVI change\n(Oct 2026 minus Oct 2025)')
    hgrid(axf)
    panel(axf, 'f', x=-0.26, y=1.04)
    save(fig, 'figure_2_inventories')


def soft_hillshade(z, res=30.0, az=315, alt=45):
    gy, gx = np.gradient(np.nan_to_num(z, nan=np.nanmean(z)), res)
    slope = np.arctan(np.hypot(gx, gy)); aspect = np.arctan2(-gx, gy)
    a = np.deg2rad(360 - az + 90)
    hs = np.sin(np.deg2rad(alt))*np.cos(slope) + np.cos(np.deg2rad(alt))*np.sin(slope)*np.cos(a - aspect)
    return np.clip(hs, 0, 1)


def zoom_map(ax, c, center_ll, half=1100, label=''):
    x0, y0 = PROJ(*center_ll)
    Bz = (x0 - half, y0 - half*0.75, x0 + half, y0 + half*0.75)
    pad = 300
    Bp = (Bz[0] - pad, Bz[1] - pad, Bz[2] + pad, Bz[3] + pad)
    from scipy.ndimage import zoom as ndzoom
    dem = ndzoom(np.nan_to_num(raster_window(DER/'dem_utm30.tif', Bp), nan=0.0), 4, order=1)
    rem_raw = raster_window(DER/'rem_utm30.tif', Bp)
    rem = ndzoom(np.nan_to_num(rem_raw, nan=999.0), 4, order=1)
    ax.set_facecolor('#f2f1ed')
    ax.imshow(np.ma.masked_where(~np.isfinite(rem) | (rem > 80), rem), cmap=CM_BLUE_R, vmin=0, vmax=80,
              extent=extent(Bp), alpha=0.85, interpolation='bicubic', zorder=1)
    ax.imshow(soft_hillshade(dem, res=7.5), cmap='Greys_r', vmin=0, vmax=1, extent=extent(Bp), alpha=0.30,
              interpolation='bicubic', zorder=2)
    xs = np.linspace(Bp[0], Bp[2], rem.shape[1]); ys = np.linspace(Bp[3], Bp[1], rem.shape[0])
    cs = ax.contour(xs, ys, np.where(np.isfinite(rem), rem, 999), levels=[10, 20, 40, 60], colors='white',
                    linewidths=0.5, zorder=3)
    ax.clabel(cs, fmt='%d m', fontsize=4.6, inline=True, inline_spacing=1)
    add_geom(ax, c['flood'].intersection(box(*Bp)).boundary, color=INK, lw=0.55, zorder=4)
    st = c['geoms']
    sel = (c['inv'].x.between(Bp[0], Bp[2]) & c['inv'].y.between(Bp[1], Bp[3])).to_numpy()
    lev = c['inv'].max_level.to_numpy()
    for k, col in [(0, '#f7f7f5'), (1, DAMAGED), (2, DAMAGED), (3, DESTROYED)]:
        for g in st[sel & (lev == k)]:
            add_geom(ax, g, facecolor=col, edgecolor=INK if k == 0 else 'none', lw=0.2 if k == 0 else 0, zorder=5 + k)
    ax.set_xlim(Bz[0], Bz[2]); ax.set_ylim(Bz[1], Bz[3])
    clean_map(ax)
    scalebar(ax, 0.5, x=0.04, y=0.05, scale=1.0, label='500 m')
    north(ax, x=0.95, y=0.06, size=0.08)
    ax.text(0.015, 0.975, label, transform=ax.transAxes, fontsize=6, va='top', color=INK,
            bbox=dict(boxstyle='round,pad=0.22', fc='white', ec='none', alpha=0.92), zorder=30)


def fig3(c):
    """Height above the channel governs destruction."""
    if 'geoms' not in c:
        c['geoms'] = shapely.from_wkb(pd.read_parquet(DER/'corridor_buildings.parquet', columns=['wkb_utm']).wkb_utm.to_numpy())
    fig = plt.figure(figsize=(W2, 147*MM))
    gs = GridSpec(3, 1, figure=fig, height_ratios=[1.27, 0.25, 1], hspace=0.12)
    top = GridSpecFromSubplotSpec(1, 2, subplot_spec=gs[0], wspace=0.04)
    a1 = fig.add_subplot(top[0]); a2 = fig.add_subplot(top[1])
    zoom_map(a1, c, (85.3660, 28.2530), label='Timure, gorge reach (~26 km downstream)')
    zoom_map(a2, c, (85.1460, 27.9150), label='Trishuli Bazar–Bidur, valley reach (~79 km)')
    panel(a1, 'a', x=-0.005, y=1.0); panel(a2, 'b', x=-0.005, y=1.0)
    # legend strip
    leg = fig.add_subplot(gs[1]); leg.axis('off')
    hdl = [Patch(fc=DESTROYED, label='Destroyed (≥1 product)'), Patch(fc=DAMAGED, label='Damaged'),
           Patch(fc='#f7f7f5', ec=INK, lw=0.3, label='No damage record'),
           Line2D([], [], color=INK, lw=0.6, label='UNOSAT flow-extent edge')]
    leg.legend(handles=hdl, loc='center left', ncol=4, fontsize=5.6, frameon=False, bbox_to_anchor=(0.0, 0.62),
               columnspacing=1.2)
    cax = leg.inset_axes([0.70, 0.52, 0.29, 0.17])
    sm = plt.cm.ScalarMappable(cmap=CM_BLUE_R, norm=plt.Normalize(0, 80))
    cb = fig.colorbar(sm, cax=cax, orientation='horizontal')
    cb.set_label('Height above pre-event channel (m); white contours', fontsize=5.4, labelpad=1.5)
    cb.ax.xaxis.set_label_position('top')
    cb.ax.tick_params(labelsize=5.0, length=1.5); cb.outline.set_linewidth(0.3)
    bot = GridSpecFromSubplotSpec(1, 4, subplot_spec=gs[2], wspace=0.55, width_ratios=[1.05, 1, 1, 0.9])
    # c: HOT class composition by height bin
    axc = fig.add_subplot(bot[0])
    b = pd.read_csv(TAB/'terrain_local_rem_bins.csv')
    b = b[b.n >= 10].reset_index(drop=True)
    left = np.zeros(len(b))
    for cls, k, nm in [('destroyed', 3, 'Destroyed'), ('major-damage', 2, 'Major'), ('minor-damage', 1, 'Minor'),
                       ('no-damage', 0, 'None')]:
        v = b[f'{cls}_pct'].to_numpy()
        axc.barh(np.arange(len(b)), v, left=left, color=DMG[k], height=0.78, lw=0, label=nm)
        left += v
    ylab = [s.replace('(', '').replace(']', '').replace(', ', '–').replace('-', '−') for s in b.rem_bin]
    axc.set_yticks(np.arange(len(b)), ylab)
    axc.invert_yaxis(); axc.set_xlim(0, 100); axc.set_xticks([0, 50, 100])
    axc.set_xlabel('HOT-graded buildings (%)'); axc.set_ylabel('Height above channel (m)')
    axc.legend(loc='lower center', bbox_to_anchor=(0.45, 1.0), ncol=4, fontsize=4.9, columnspacing=0.6,
               handlelength=0.9, handletextpad=0.3)
    axc.tick_params(axis='y', length=0, labelsize=5.2)
    panel(axc, 'c', x=-0.42, y=1.08)
    # d: logistic curves by reach group with labelled 50% thresholds
    axd = fig.add_subplot(bot[1])
    cur = pd.read_csv(TAB/'terrain_curves_by_reachgroup.csv')
    cols = {'gorge_21_41km': BLUE[12], 'middle_64_89km': BLUE[8], 'lower_89_114km': BLUE[4]}
    labs = {'gorge_21_41km': 'Gorge 21–41 km', 'middle_64_89km': 'Valley 64–89 km', 'lower_89_114km': 'Lower 89–114 km'}
    for k in ['gorge_21_41km', 'middle_64_89km', 'lower_89_114km']:
        g = cur[cur.group == k]
        axd.fill_between(g.rem_m, g.lo, g.hi, color=cols[k], alpha=0.18, lw=0)
        axd.plot(g.rem_m, g.p, color=cols[k], lw=1.2, label=labs[k])
        r50 = g.rem50.iloc[0]
        axd.plot(r50, 0.5, 'o', ms=3.2, mfc=cols[k], mec='white', mew=0.5, zorder=5)
        if k == 'lower_89_114km':
            axd.text(r50 - 2, 0.45, f'{r50:.0f} m', fontsize=5.2, color=INK, va='top', ha='right')
        else:
            axd.text(r50 + 2, 0.53, f'{r50:.0f} m', fontsize=5.2, color=INK, va='bottom')
    axd.axhline(0.5, color=MUTED, lw=0.5)
    axd.set_xlim(-5, 110); axd.set_ylim(0, 1.0)
    axd.set_xlabel('Height above channel (m)'); axd.set_ylabel('P(destroyed)')
    axd.legend(loc='upper right', fontsize=4.9, handlelength=1.0)
    hgrid(axd)
    panel(axd, 'd', x=-0.30, y=1.08)
    # e: ROC curves
    axe = fig.add_subplot(bot[2])
    roc = pd.read_csv(TAB/'ml_roc_curves.csv')
    perf = pd.read_csv(TAB/'ml_performance.csv').set_index('model')
    spec = [('Gradient boosting, spatial CV', 'Boosted trees', perf.loc['gbm', 'auc'], INK),
            ('Height above channel only', 'Height only', perf.loc['logit_rem', 'auc'], BLUE[8]),
            ('Transfer to HOT labels', 'Transfer to HOT', perf.loc['gbm_transfer_to_HOT', 'auc'], SRC['CEMS'])]
    for key, lab, auc, col in spec:
        g = roc[roc.model == key]
        axe.plot(g.fpr, g.tpr, color=col, lw=1.1, label=f'{lab} ({auc:.2f})')
    axe.plot([0, 1], [0, 1], color=GRID, lw=0.6)
    axe.set_xlim(0, 1); axe.set_ylim(0, 1.01); axe.set_xticks([0, 0.5, 1]); axe.set_yticks([0, 0.5, 1])
    axe.set_xlabel('False-positive rate'); axe.set_ylabel('True-positive rate')
    axe.legend(loc='lower right', fontsize=4.8, title='Model (AUC)', title_fontsize=4.9, handlelength=0.9,
               bbox_to_anchor=(1.04, -0.01))
    panel(axe, 'e', x=-0.30, y=1.08)
    # f: permutation importance
    axf = fig.add_subplot(bot[3])
    imp = pd.read_csv(TAB/'ml_permutation_importance.csv').head(6)[::-1]
    axf.barh(np.arange(len(imp)), imp.importance_auc_drop, xerr=imp.importance_sd, color=BLUE[8], height=0.6, lw=0,
             error_kw=dict(lw=0.5, capsize=1.2, ecolor=INK2))
    axf.set_yticks(np.arange(len(imp)), [l.replace(' (log)', '') for l in imp.label], fontsize=5.0)
    axf.tick_params(axis='y', length=0)
    axf.set_xlabel('AUC loss when permuted')
    axf.set_xlim(0, 0.3)
    hgrid(axf, 'x')
    panel(axf, 'f', x=-0.75, y=1.08)
    save(fig, 'figure_3_height_controls')


def fig4(c):
    """Damage-calibrated destructive height attenuates downstream with wave celerity and valley widening."""
    env = pd.read_csv(TAB/'terrain_envelope_by_reach.csv')
    dh = pd.read_csv(TAB/'danger_height_profile.csv')
    tl = pd.read_csv(TAB/'timing_wave_arrivals.csv')
    tr = pd.read_csv(DER/'transects.csv')
    chain_of = c['ch'].place_chainage()
    fig = plt.figure(figsize=(W2, 118*MM))
    gs = GridSpec(3, 2, figure=fig, width_ratios=[2.15, 1], height_ratios=[1.6, 0.9, 0.9], hspace=0.12, wspace=0.28)
    # a: envelope
    ax = fig.add_subplot(gs[0, 0])
    ax.fill_between(dh.chainage_km, dh.h_m, dh.h_outer_m, color=DESTROYED, alpha=0.10, lw=0)
    ax.plot(dh.chainage_km, dh.h_m, color=DESTROYED, lw=1.0, label='Damage-calibrated danger height (core)')
    ax.plot(dh.chainage_km, dh.h_outer_m, color=DESTROYED, lw=0.6, alpha=0.55, label='Outer envelope (90% of destroyed)')
    ok = env.rem50_m.notna() & (env.rem50_m > 0) & ((env.rem50_hi - env.rem50_lo) < 60)
    e = env[ok]
    ax.errorbar(e.reach_mid_km, e.rem50_m, yerr=[e.rem50_m - e.rem50_lo, e.rem50_hi - e.rem50_m], fmt='o', ms=3.4,
                mfc=DESTROYED, mec='white', mew=0.5, ecolor=DESTROYED, elinewidth=0.7, capsize=1.5, zorder=5,
                label='Height at 50% destruction (95% CI)')
    ax.plot(env.reach_mid_km, env.rem_destroyed_p90, 'D', ms=2.8, mfc='white', mec=DESTROYED, mew=0.7, zorder=5,
            label='90th percentile height of destroyed buildings')
    f = env.dropna(subset=['flow_edge_rem_p50'])
    ax.vlines(f.reach_mid_km + 1.2, f.flow_edge_rem_p25, f.flow_edge_rem_p75, color=SRC['HOT'], lw=1.6, alpha=0.7, zorder=4)
    ax.plot(f.reach_mid_km + 1.2, f.flow_edge_rem_p50, 's', ms=3, mfc=SRC['HOT'], mec='white', mew=0.5, zorder=5,
            label='UNOSAT flow-extent edge height (median, IQR)')
    sg = [(105.9, 8.9, 'Galchhi'), (172.0, 9.1, 'Kali Khola'), (206.8, 2.6, 'Devghat')]
    ax.plot([s[0] for s in sg], [s[1] for s in sg], '*', ms=6.5, mfc=INK, mec='white', mew=0.4, zorder=6,
            label='Stage rise, gauged or reconstructed (CHWRR, ICIMOD)')
    for x_, y_, n_ in sg:
        if n_ == 'Galchhi':
            ax.annotate(n_, (x_, y_), xytext=(124, 33), fontsize=5, ha='left', va='center', color=INK2,
                        arrowprops=dict(arrowstyle='-', lw=0.4, color=INK2, shrinkA=1, shrinkB=3))
        else:
            ax.text(x_, y_ + 4, n_, fontsize=5, ha='center', color=INK2)
    ax.set_ylim(0, 110); ax.set_xlim(0, 207)
    ax.set_ylabel('Height above\npre-event channel (m)')
    ax.axvspan(41, 64, color='#f4f3ef', lw=0, zorder=0); ax.axvspan(114, 207, color='#f4f3ef', lw=0, zorder=0)
    ax.text(52.5, 104, 'no grading', fontsize=5, ha='center', color=MUTED)
    ax.text(160, 104, 'no grading: gauges only', fontsize=5, ha='center', color=MUTED)
    for nm in ['Rasuwagadhi', 'Syaphrubesi', 'Betrawati', 'Trishuli Bazar', 'Galchhi', 'Benighat', 'Mugling', 'Devghat']:
        ax.axvline(chain_of[nm], color=GRID, lw=0.5, zorder=0)
    ax.legend(loc='upper right', fontsize=5.0, ncol=1, bbox_to_anchor=(1.0, 0.93))
    plt.setp(ax.get_xticklabels(), visible=False)
    hgrid(ax)
    panel(ax, 'a', x=-0.075, y=0.98)
    # b: front celerity
    axb = fig.add_subplot(gs[1, 0], sharex=ax)
    a_ = tl[tl.arrival].reset_index(drop=True)
    for i in range(1, len(a_)):
        axb.plot([a_.chainage_km[i-1], a_.chainage_km[i]], [a_.celerity_from_previous_m_s[i]]*2, color=INK, lw=1.2,
                 solid_capstyle='butt')
        axb.text((a_.chainage_km[i-1] + a_.chainage_km[i])/2, a_.celerity_from_previous_m_s[i]*1.18,
                 f'{a_.celerity_from_previous_m_s[i]:.0f}', fontsize=5, ha='center', color=INK2)
    for i, r in a_.iterrows():
        axb.plot(r.chainage_km, 1.15, '|', ms=4, color=INK2)
        axb.text(r.chainage_km + 1.2, 1.25, r.time[:5], fontsize=4.6, ha='left', va='bottom', color=INK2, rotation=90)
    axb.set_yscale('log'); axb.set_ylim(1.0, 160)
    axb.set_yticks([2, 5, 10, 20, 50, 100], ['2', '5', '10', '20', '50', '100'])
    axb.set_ylabel('Front celerity\n(m s$^{-1}$)')
    plt.setp(axb.get_xticklabels(), visible=False)
    hgrid(axb)
    panel(axb, 'b', x=-0.075, y=0.92)
    # c: valley-floor width and mapped flow width
    axc = fig.add_subplot(gs[2, 0], sharex=ax)
    t = tr.sort_values('chainage_km')
    vw = t.valley_width_20m.where(t.valley_width_20m > 0).rolling(31, center=True, min_periods=5).median()
    fw = t.flow_width_m.where(t.flow_width_m > 0).rolling(31, center=True, min_periods=5).median()
    axc.plot(t.chainage_km, vw, color=INK, lw=0.9, label='Valley floor <20 m above channel')
    axc.plot(t.chainage_km, fw, color=SRC['HOT'], lw=0.9, label='Mapped flow-extent width')
    axc.set_ylim(0, 800); axc.set_yticks([0, 400, 800])
    axc.set_ylabel('Width (m)')
    axc.set_xlabel('Distance downstream of source (km)')
    axc.legend(loc='upper left', fontsize=5.0, ncol=2)
    hgrid(axc)
    panel(axc, 'c', x=-0.075, y=0.92)
    # d: agreement between damage-derived and flow-edge heights
    axd = fig.add_subplot(gs[:2, 1])
    from analysis_impacts import robust_reach_heights
    m = robust_reach_heights(env).dropna(subset=['flow_edge_rem_p50']).copy()
    m['dmg_h'] = m.h_core
    axd.plot([0, 90], [0, 90], color=MUTED, lw=0.6)
    axd.text(78, 72, '1:1', fontsize=5.2, color=MUTED, rotation=45)
    sc = axd.scatter(m.flow_edge_rem_p50, m.dmg_h, c=m.reach_mid_km, cmap=CM_BLUE_R, vmin=0, vmax=120, s=26,
                     ec=INK, lw=0.4, zorder=3)
    axd.errorbar(m.flow_edge_rem_p50, m.dmg_h, xerr=[m.flow_edge_rem_p50 - m.flow_edge_rem_p25,
                                                     m.flow_edge_rem_p75 - m.flow_edge_rem_p50],
                 fmt='none', ecolor=MUTED, elinewidth=0.5, zorder=2)
    from scipy.stats import spearmanr
    rho, pv = spearmanr(m.flow_edge_rem_p50, m.dmg_h)
    axd.text(3, 85, f'Spearman ρ = {rho:.2f}\nn = {len(m)} reaches', fontsize=5.4, color=INK, va='top')
    axd.set_xlim(0, 90); axd.set_ylim(0, 90)
    axd.set_xlabel('UNOSAT flow-extent edge height (m)')
    axd.set_ylabel('Damage-calibrated height (m)')
    cax = axd.inset_axes([0.52, 0.10, 0.44, 0.035])
    cb = fig.colorbar(sc, cax=cax, orientation='horizontal')
    cb.set_label('Reach midpoint (km)', fontsize=5.2, labelpad=1); cb.ax.tick_params(labelsize=4.8, length=1.5)
    cb.ax.xaxis.set_label_position('top')
    cb.outline.set_linewidth(0.3)
    panel(axd, 'd', x=-0.2, y=1.0)
    # e: text panel with the reach-group thresholds and setback statistics
    axe = fig.add_subplot(gs[2, 1]); axe.axis('off')
    sb = pd.read_csv(TAB/'terrain_setback_thresholds.csv').set_index('rem_threshold_m')
    lines = [('Destroyed buildings below 20 m', f"{sb.loc[20, 'destroyed_below_pct']:.0f}%"),
             ('  gorge / valley / lower reach', f"{sb.loc[20, 'gorge_21_41km_destroyed_below_pct']:.0f} / "
                                                f"{sb.loc[20, 'middle_64_89km_destroyed_below_pct']:.0f} / "
                                                f"{sb.loc[20, 'lower_89_114km_destroyed_below_pct']:.0f}%"),
             ('Undamaged buildings <20 m above\nchannel, ≤500 m (whole corridor)', f"{int(sb.loc[20, 'undamaged_stock_below_0_207km']):,}")]
    axe.text(0.0, 0.62, 'Setback implications', fontsize=6, fontweight='bold', va='top', transform=axe.transAxes)
    for i, (k, v) in enumerate(lines):
        axe.text(0.0, 0.45 - i*0.22, k, fontsize=5.3, va='top', color=INK2, transform=axe.transAxes)
        axe.text(1.08, 0.45 - i*0.22, v, fontsize=5.8, va='top', ha='right', color=INK, fontweight='bold',
                 transform=axe.transAxes)
    panel(axe, 'e', x=-0.2, y=0.62)
    save(fig, 'figure_4_height_envelope')


EPOCH_RAMP = ['#a596ec', '#8574e2', '#6250d6', '#4636a8', '#2c2275']        # validated ordinal (violet)
LEAD_RAMP = ['#0d366b', '#1c5cab', '#2a78d6', '#5598e7', '#86b6ef']         # validated ordinal (blue), dark = less time


def repel(values, factor=1.16):
    """Spread end-label positions on a log axis so neighbours are at least `factor` apart."""
    order = np.argsort(values)
    pos = np.array(values, float)
    for a, b in zip(order[:-1], order[1:]):
        if pos[b] < pos[a]*factor:
            pos[b] = pos[a]*factor
    return pos


def fig5(c):
    """Exposure growth into the destructive zone and warning time along the corridor."""
    fig = plt.figure(figsize=(W2, 130*MM))
    gs = GridSpec(2, 2, figure=fig, width_ratios=[1, 1.15], hspace=0.42, wspace=0.26)
    # a: built-up growth by height band (0-106 km, within 1 km of channel)
    ax = fig.add_subplot(gs[0, 0])
    z = pd.read_csv(TAB/'exposure_growth_zones.csv')
    z = z[z.reach == '0-106km (assessed)'].set_index('zone')
    years = list(range(1975, 2021, 5))
    bands = [('rem_lt10_d1km', '<10 m', BLUE[12]), ('rem_10_20_d1km', '10–20 m', BLUE[10]),
             ('rem_20_40_d1km', '20–40 m', BLUE[8]), ('rem_40_80_d1km', '40–80 m', BLUE[5]), ('rem_ge80_d1km', '≥80 m', BLUE[3])]
    ends = []
    for k, lab, col in bands:
        v = z.loc[k, [f'built_m2_{y}' for y in years]].to_numpy(float)/z.loc[k, 'built_m2_1975']
        ax.plot(years, v, color=col, lw=1.2, marker='o', ms=2.2, mec='white', mew=0.3)
        ends.append(v[-1])
    for (k, lab, col), yl, ye in zip(bands, repel(ends), ends):
        ax.plot([2020.5, 2022.5], [ye, yl], color=GRID, lw=0.5)
        ax.text(2023, yl, f'{lab}  ×{ye:.1f}', fontsize=5.2, va='center', color=INK)
    fe = z.loc['flow_extent', [f'built_m2_{y}' for y in years]].to_numpy(float)
    ax.set_xlim(1973, 2037); ax.set_ylim(0.8, 24)
    ax.set_yscale('log'); ax.set_yticks([1, 2, 5, 10, 20], ['1', '2', '5', '10', '20'])
    ax.set_ylabel('Built-up surface\n(relative to 1975)')
    ax.set_xticks([1975, 1990, 2005, 2020])
    ax.text(1975, 21, f'Mapped flow extent: {fe[0]/1e4:.1f} ha (1975) → {fe[-1]/1e4:.1f} ha (2020)',
            fontsize=5.2, color=INK2, va='top')
    ax.text(2023, 1.0, 'height above\nchannel band', fontsize=5.0, color=MUTED, va='center')
    hgrid(ax)
    panel(ax, 'a', x=-0.17, y=1.02)
    # b: epoch of first built-up, Trishuli Bazar-Bidur, with flow extent and destroyed buildings
    axb = fig.add_subplot(gs[0, 1])
    from analysis_exposure import to_grid
    import rasterio as _rio
    x0, y0 = PROJ(85.150, 27.917)
    Bz = (x0 - 2600, y0 - 1700, x0 + 2600, y0 + 1700)
    with _rio.open(DER/'dem_utm30.tif') as s_:
        T = s_.transform; shp = s_.shape
    win = _rio.windows.from_bounds(*Bz, transform=T).round_offsets().round_lengths()
    r0, c0, hh, ww = int(win.row_off), int(win.col_off), int(win.height), int(win.width)
    first = np.full((hh, ww), np.nan)
    for i, (lo, hi) in enumerate([(1975, 1975), (1980, 1990), (1995, 2000), (2005, 2010), (2015, 2020)]):
        for y in range(lo, hi + 1, 5):
            g = to_grid(ROOT/'sources_ext'/'ghsl'/f'ghs_built_s_{y}_corridor.tif', T, shp, 'ghsl')[r0:r0+hh, c0:c0+ww]
            first[np.isnan(first) & (g > 90)] = i       # first epoch with >10% of the 30-m cell built up
    dem = raster_window(DER/'dem_utm30.tif', Bz)
    axb.imshow(soft_hillshade(dem), cmap='Greys_r', extent=extent(Bz), vmin=0, vmax=1, alpha=0.45, interpolation='bilinear')
    from matplotlib.colors import ListedColormap, BoundaryNorm
    axb.imshow(np.ma.masked_invalid(first), cmap=ListedColormap(EPOCH_RAMP), norm=BoundaryNorm(np.arange(-0.5, 5), 5),
               extent=(Bz[0], Bz[0] + ww*30, Bz[3] - hh*30, Bz[3]), interpolation='nearest', alpha=0.9)
    add_geom(axb, c['flood'].intersection(box(*Bz)), facecolor='none', edgecolor=FLOW, lw=0.9)
    inv = c['inv']
    dz = inv[(inv.max_level == 3) & inv.x.between(Bz[0], Bz[2]) & inv.y.between(Bz[1], Bz[3])]
    axb.scatter(dz.x, dz.y, s=1.2, c=DESTROYED, lw=0, zorder=5)
    axb.set_xlim(Bz[0], Bz[2]); axb.set_ylim(Bz[1], Bz[3])
    clean_map(axb)
    scalebar(axb, 1, x=0.04, y=0.05, scale=1.0, label='1 km')
    hdl = [Patch(fc=col, label=lab) for col, lab in zip(EPOCH_RAMP, ['≤1975', '1980–90', '1995–2000', '2005–10', '2015–20'])]
    hdl += [Line2D([], [], color=FLOW, lw=1, label='Flow extent'),
            Line2D([], [], ls='', marker='o', ms=2.5, mfc=DESTROYED, mec='none', label='Destroyed')]
    axb.legend(handles=hdl, loc='upper left', fontsize=4.9, title='First built-up (GHSL)', title_fontsize=5.0, frameon=True,
               framealpha=0.9, edgecolor='none', ncol=1, bbox_to_anchor=(0.0, 1.0))
    axb.text(0.99, 0.02, 'Trishuli Bazar–Bidur', transform=axb.transAxes, ha='right', fontsize=5.4,
             bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.9))
    panel(axb, 'b', x=-0.02, y=1.02)
    # c: arrival time vs alerts (log time since failure)
    sub = GridSpecFromSubplotSpec(2, 1, subplot_spec=gs[1, 0], height_ratios=[1, 0.22], hspace=0.08)
    axc = fig.add_subplot(sub[0])
    tl = pd.read_csv(TAB/'timing_wave_arrivals.csv')
    a_ = tl[tl.arrival]
    onset = 8*60 + 37 + 10/60
    tm = lambda s: max((int(s[:2])*60 + int(s[3:5]) + int(s[6:8])/60) - onset, 0.5)
    ch_grid = np.linspace(0, 207, 400)
    arr = np.interp(ch_grid, a_.chainage_km, [tm(t) for t in a_.time])
    axc.plot(ch_grid, arr, color=INK, lw=1.2, zorder=4)
    axc.plot(a_.chainage_km, [tm(t) for t in a_.time], 'o', ms=3, mfc=INK, mec='white', mew=0.5, zorder=5)
    alerts = [('08:39:10', 'Seismic alert (counterfactual)', BLUE[5]),
              ('08:50:00', 'Phone warnings', BLUE[8]),
              ('09:15:00', 'Mass SMS', BLUE[12])]
    for t_, lab, col in alerts:
        axc.axhline(tm(t_), color=col, lw=0.9, zorder=3)
        axc.text(206, tm(t_)*1.07, f'{lab} ({t_[:5]})', fontsize=4.9, ha='right', va='bottom', color=INK2)
        cross = np.interp(tm(t_), arr, ch_grid)
        axc.fill_between(ch_grid[ch_grid <= cross], 0.5, 800, color=col, alpha=0.05, lw=0)
    for _, r in a_.iterrows():
        if r.place.startswith('Source'):
            continue
        right = r.place.startswith('Rasuwagadhi')
        axc.text(r.chainage_km + (2 if right else -2), tm(r.time)*(0.80 if right else 1.12), r.place.split(' ')[0],
                 fontsize=4.6, color=INK2, ha='left' if right else 'right', va='top' if right else 'bottom')
    axc.set_yscale('log'); axc.set_ylim(1, 700); axc.set_xlim(0, 207)
    ticks = [1, 2, 5, 10, 20, 50, 100, 200, 400]
    axc.set_yticks(ticks, [f'{t}' for t in ticks])
    axc.set_ylabel('Minutes after failure\n(08:37 NPT)')
    plt.setp(axc.get_xticklabels(), visible=False)
    hgrid(axc)
    panel(axc, 'c', x=-0.17, y=1.03)
    axs = fig.add_subplot(sub[1], sharex=axc)
    hist = np.histogram(inv[inv.max_level == 3].chainage_km, bins=np.arange(0, 210, 3))[0]
    axs.bar(np.arange(1.5, 207, 3), hist, width=2.6, color=DESTROYED, lw=0)
    axs.set_yticks([0, 500]); axs.set_ylim(0, 700)
    axs.set_ylabel('Destroyed\nper 3 km', fontsize=5.2)
    axs.set_xlabel('Distance downstream of source (km)')
    # d: lead-time classes for destroyed buildings under three alert scenarios
    axd = fig.add_subplot(gs[1, 1])
    hi = pd.read_parquet(DER/'harmonised_inventory.parquet')
    hi = hi[hi.max_level == 3]
    arr_b = np.interp(hi.chainage_km, a_.chainage_km, [tm(t) for t in a_.time])
    cats = ['Hit before alert', '0–10 min', '10–30 min', '30–60 min', '>60 min']
    edges = [-np.inf, 0, 10, 30, 60, np.inf]
    yv = np.arange(3)[::-1]
    for j, (t_, lab, _) in enumerate(alerts):
        lt = arr_b - tm(t_)
        left = 0
        for k in range(5):
            v = 100*np.mean((lt > edges[k]) & (lt <= edges[k+1]))
            axd.barh(yv[j], v, left=left, color=LEAD_RAMP[k], height=0.62, lw=0, label=cats[k] if j == 0 else None)
            if v >= 6:
                axd.text(left + v/2, yv[j], f'{v:.0f}%', ha='center', va='center', fontsize=5.2,
                         color='white' if k <= 2 else INK)
            left += v
    for y_, lab in zip(yv, ['Seismic-triggered alert at 08:39 (counterfactual)', 'Telephone warnings from 08:46 (actual)',
                            'Mass SMS at 09:15 (actual)']):
        axd.text(0, y_ + 0.35, lab, fontsize=5.6, color=INK, va='bottom', ha='left')
    axd.set_yticks([]); axd.spines['left'].set_visible(False)
    axd.set_ylim(-0.45, 2.78)
    axd.set_xlim(0, 100); axd.set_xlabel(f'Share of {len(hi):,} destroyed buildings (%)')
    axd.legend(loc='lower center', bbox_to_anchor=(0.45, 1.0), ncol=5, fontsize=4.9, handlelength=0.9, columnspacing=0.6,
               title='Time between alert and wave arrival', title_fontsize=5.0)
    panel(axd, 'd', x=-0.06, y=1.02)
    save(fig, 'figure_5_exposure_warning')


def fig6(c):
    """Municipal recovery priorities: indicators, rank robustness, danger-zone stock, losses and debris."""
    ind = pd.read_csv(TAB/'municipal_indicators.csv')
    rk = pd.read_csv(TAB/'municipal_rank_uncertainty.csv')
    d = rk.merge(ind, on='municipality', how='left').reset_index(drop=True)
    fig = plt.figure(figsize=(W2, 150*MM))
    gs = GridSpec(2, 1, figure=fig, height_ratios=[1.35, 1], hspace=0.34)
    top = GridSpecFromSubplotSpec(1, 2, subplot_spec=gs[0], width_ratios=[2.7, 1], wspace=0.04)
    ax = fig.add_subplot(top[0])
    cols = [('sat_destroyed', 'Destroyed\nbuildings\n(satellite)', '{:,.0f}'),
            ('rdna_affected_buildings', 'Affected\nbuildings\n(RDNA)', '{:,.0f}'),
            ('people_affected', 'Affected\npeople\n(gov.)', '{:,.0f}'),
            ('debris_t_central', 'Building\ndebris\n(kt)', '{:,.0f}'),
            ('buildings_danger_zone', 'Buildings in\ndanger zone', '{:,.0f}'),
            ('pop2026_danger_zone', 'People in\ndanger zone', '{:,.0f}'),
            ('lead_seismic_min', 'Lead time,\nseismic alert\n(min)', '{:,.0f}'),
            ('lead_sms_min', 'Lead time,\nactual SMS\n(min)', '{:+,.0f}')]
    n = len(d)
    M = np.full((n, len(cols)), np.nan)
    for j, (k, _, _) in enumerate(cols):
        v = d[k].astype(float)
        if k == 'debris_t_central':
            v = v/1000
        if k.startswith('lead'):
            M[:, j] = 1 - (v.clip(-30, 120) + 30)/150           # shorter lead time = darker
        else:
            M[:, j] = (np.log1p(v.fillna(0)))/np.log1p(v.fillna(0)).max()
    ax.imshow(M, cmap=CM_BLUE, vmin=0, vmax=1.05, aspect='auto')
    for i in range(n):
        for j, (k, _, fmt) in enumerate(cols):
            v = d[k].iloc[i]
            if k == 'debris_t_central':
                v = v/1000 if pd.notna(v) else v
            txt = '–' if pd.isna(v) else fmt.format(v).replace('-', '−')
            ax.text(j, i, txt, ha='center', va='center', fontsize=5.0, color='white' if M[i, j] > 0.62 else INK)
    ax.set_xticks(range(len(cols)), [cl[1] for cl in cols], fontsize=5.2)
    ax.xaxis.tick_top(); ax.tick_params(axis='x', length=0, pad=2)
    ax.set_yticks(range(n), d.municipality, fontsize=5.6); ax.tick_params(axis='y', length=0)
    ax.axvline(5.5, color='white', lw=2)
    for sp in ax.spines.values():
        sp.set_visible(False)
    panel(ax, 'a', x=-0.13, y=1.17)
    axr = fig.add_subplot(top[1], sharey=ax)
    for i, r in d.iterrows():
        axr.plot([r.rank_p05, r.rank_p95], [i, i], color=MUTED, lw=1.4, solid_capstyle='round')
        axr.plot(r.rank_median, i, 'o', ms=3.6, mfc=INK, mec='white', mew=0.5)
        if r.p_top3 >= 0.05:
            axr.text(r.rank_p95 + 0.5, i, f'P(top 3) = {r.p_top3:.2f}', fontsize=4.9, va='center', color=INK2)
    axr.set_xlim(0.5, 19); axr.set_xticks([1, 5, 10, 15])
    axr.set_xlabel('Composite rank\n(median, 90% interval)', fontsize=5.6)
    axr.xaxis.set_label_position('top'); axr.xaxis.tick_top()
    plt.setp(axr.get_yticklabels(), visible=False); axr.tick_params(axis='y', length=0)
    axr.spines['left'].set_visible(False); axr.spines['bottom'].set_visible(False); axr.spines['top'].set_visible(True)
    hgrid(axr, 'x')
    panel(axr, 'b', x=-0.05, y=1.17)
    bot = GridSpecFromSubplotSpec(1, 3, subplot_spec=gs[1], width_ratios=[1.15, 1.15, 0.9], wspace=0.55)
    # c: danger-zone building stock
    axc = fig.add_subplot(bot[0])
    z = d.dropna(subset=['buildings_outer_zone']).sort_values('buildings_outer_zone', ascending=False).head(10)[::-1]
    des_c = (z.buildings_danger_zone - z.surviving_in_danger_zone).fillna(0)
    sur_c = z.surviving_in_danger_zone.fillna(0)
    sur_o = (z.surviving_in_outer_zone - z.surviving_in_danger_zone).fillna(0).clip(lower=0)
    y = np.arange(len(z))
    axc.barh(y, des_c, color=DESTROYED, height=0.66, lw=0, label='Destroyed (core zone)')
    axc.barh(y, sur_c, left=des_c, color=INK2, height=0.66, lw=0, label='Surviving, core zone')
    axc.barh(y, sur_o, left=des_c + sur_c, color='#b9b7b0', height=0.66, lw=0, label='Surviving, outer zone')
    axc.set_yticks(y, z.municipality, fontsize=5.4); axc.tick_params(axis='y', length=0)
    axc.set_xlabel('Buildings below the damage-calibrated height')
    axc.legend(loc='lower right', fontsize=4.9)
    hgrid(axc, 'x')
    panel(axc, 'c', x=-0.42, y=1.02)
    # d: loss and needs estimates by scope
    axd = fig.add_subplot(bot[1])
    le = pd.read_csv(TAB/'loss_estimates.csv')
    lab = ['UNDP CLIMADA:\nbuildings', 'RDNA: private\nhousing damage', 'RDNA: energy\ndamage', 'GRADE: physical\ndamage',
           'RDNA: physical\ndamage', 'RDNA: total\neffects', 'RDNA: recovery\nneeds']
    yv = np.arange(len(le))[::-1]
    for y_, (_, r) in zip(yv, le.iterrows()):
        col = SRC['RDNA'] if r.estimate.startswith('RDNA') else (SRC['HOT'] if 'GRADE' in r.estimate else SRC['UNOSAT'])
        if pd.notna(r.low_usd_million):
            axd.plot([r.low_usd_million/1000, r.high_usd_million/1000], [y_, y_], color=col, lw=2, solid_capstyle='round')
        axd.plot(r.usd_million/1000, y_, 'o', ms=4, mfc=col, mec='white', mew=0.5)
        xl = (r.high_usd_million if pd.notna(r.high_usd_million) else r.usd_million)/1000
        axd.text(xl*1.15, y_, f'{r.usd_million/1000:.2f}', fontsize=5.0, va='center', color=INK)
    axd.set_xscale('log'); axd.set_xlim(0.08, 9)
    axd.set_xticks([0.1, 0.3, 1, 3], ['0.1', '0.3', '1', '3'])
    axd.set_yticks(yv, lab, fontsize=4.9); axd.tick_params(axis='y', length=0)
    axd.set_xlabel('US$ billion (log scale)')
    hgrid(axd, 'x')
    panel(axd, 'd', x=-0.52, y=1.02)
    # e: debris
    axe = fig.add_subplot(bot[2])
    ir = json.loads((DER/'impacts_results.json').read_text())['debris']
    rows = [('UNDP RAPIDA,\nCEMS/SERTIT set', 556.2, None, None), ('UNDP RAPIDA,\nall records', 692.9, None, None),
            ('This study:\nharmonized set', ir['debris_central_t']/1000, ir['debris_mc_p05']/1000, ir['debris_mc_p95']/1000),
            ('This study: no\nsettlement factor', ir['debris_no_settlement_factor_t']/1000, None, None)]
    yv = np.arange(len(rows))[::-1]
    for y_, (lab_, v, lo, hi) in zip(yv, rows):
        col = SRC['UNOSAT'] if lab_.startswith('UNDP') else DESTROYED
        if lo is not None:
            axe.plot([lo, hi], [y_, y_], color=col, lw=2, solid_capstyle='round', alpha=0.6)
        axe.plot(v, y_, 'o', ms=4, mfc=col, mec='white', mew=0.5)
        axe.text(v, y_ + 0.32, f'{v:,.0f}', fontsize=5.0, ha='center', color=INK)
    axe.set_yticks(yv, [r[0] for r in rows], fontsize=4.9); axe.tick_params(axis='y', length=0)
    axe.set_xlim(0, 1400); axe.set_xticks([0, 500, 1000])
    axe.set_xlabel('Building debris (kt)')
    axe.set_ylim(-0.6, len(rows) - 0.3)
    hgrid(axe, 'x')
    panel(axe, 'e', x=-0.62, y=1.02)
    save(fig, 'figure_6_priorities')


FIGS = {'fig1': fig1, 'fig2': fig2, 'fig3': fig3, 'fig4': fig4, 'fig5': fig5, 'fig6': fig6}

if __name__ == '__main__':
    common = load_common()
    for name in (sys.argv[1:] or list(FIGS)):
        FIGS[name](common)
        print('rendered', name)
