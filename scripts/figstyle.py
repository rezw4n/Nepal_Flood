"""Shared figure style (Nature-portfolio specifications) and map helpers.

Widths: single column 88 mm, double column 180 mm. Text 5-7 pt Arial, panel labels 8 pt bold.
Colours were checked for colour-vision-deficiency separation (ordinal damage ramp; adjacent-pair
categorical sources); maps use emphasis encoding (damage hues, undamaged in recessive grey).
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path as MPath
from matplotlib.patches import PathPatch
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patheffects as pe
HALO = [pe.withStroke(linewidth=1.6, foreground='white')]
import rasterio
from rasterio.windows import from_bounds

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT/'figures'
DER = ROOT/'data'/'derived'
MM = 1/25.4
W1, W2 = 88*MM, 180*MM

INK, INK2, MUTED, GRID, AXIS = '#1a1a1a', '#52514e', '#898781', '#e1e0d9', '#8f8d86'
# ordinal damage ramp (validated) and neutral
DMG = {0: '#8c99a6', 1: '#f0a06c', 2: '#d9622b', 3: '#9e2f0d'}
DMG_LABEL = {0: 'No damage / no record', 1: 'Minor / possibly damaged', 2: 'Major / damaged', 3: 'Destroyed'}
DAMAGED = '#e0773a'          # minor+major merged on maps
DESTROYED = DMG[3]
# categorical sources (validated adjacent order)
SRC = {'HOT': '#2a78d6', 'CEMS': '#1baf7a', 'UNOSAT': '#eda100', 'RDNA': '#6250d6'}
# sequential blue ramp (validated ordinal subset); full ramp for continuous fields
BLUE = ['#cde2fb', '#b7d3f6', '#9ec5f4', '#86b6ef', '#6da7ec', '#5598e7', '#3987e5', '#2a78d6', '#256abf',
        '#1c5cab', '#184f95', '#104281', '#0d366b']
CM_BLUE = LinearSegmentedColormap.from_list('blue_seq', BLUE)
CM_BLUE_R = LinearSegmentedColormap.from_list('blue_seq_r', BLUE[::-1])
FLOW = '#56a3e9'              # mapped flow extent wash
RIVER = '#2a78d6'

plt.rcParams.update({
    'font.family': 'Arial', 'font.size': 6.5, 'axes.titlesize': 7, 'axes.labelsize': 6.5,
    'xtick.labelsize': 6, 'ytick.labelsize': 6, 'legend.fontsize': 6, 'legend.title_fontsize': 6.5,
    'axes.linewidth': 0.5, 'xtick.major.width': 0.5, 'ytick.major.width': 0.5, 'xtick.major.size': 2.5,
    'ytick.major.size': 2.5, 'xtick.minor.size': 1.5, 'ytick.minor.size': 1.5, 'lines.linewidth': 1.0,
    'axes.spines.top': False, 'axes.spines.right': False, 'axes.edgecolor': AXIS, 'axes.labelcolor': INK,
    'xtick.color': AXIS, 'ytick.color': AXIS, 'xtick.labelcolor': INK2, 'ytick.labelcolor': INK2,
    'text.color': INK, 'axes.titleweight': 'bold', 'axes.titlelocation': 'left', 'axes.titlepad': 3,
    'legend.frameon': False, 'legend.handlelength': 1.2, 'legend.borderaxespad': 0.2,
    'savefig.dpi': 600, 'svg.fonttype': 'none', 'pdf.fonttype': 42, 'ps.fonttype': 42,
    'figure.dpi': 150, 'axes.grid': False, 'grid.color': GRID, 'grid.linewidth': 0.4,
})


def save(fig, name):
    FIG.mkdir(exist_ok=True)
    for ext in ('png', 'pdf', 'svg'):
        fig.savefig(FIG/f'{name}.{ext}', bbox_inches='tight', pad_inches=0.02, facecolor='white')
    plt.close(fig)


def panel(ax, letter, x=-0.02, y=1.02, **kw):
    ax.text(x, y, letter, transform=ax.transAxes, fontsize=8, fontweight='bold', va='bottom', ha='right', color=INK, **kw)


def hgrid(ax, axis='y'):
    ax.grid(True, axis=axis, color=GRID, lw=0.4, zorder=0)
    ax.set_axisbelow(True)


def raster_window(path, bounds, band=1):
    with rasterio.open(path) as s:
        w = from_bounds(*bounds, transform=s.transform)
        a = s.read(band, window=w, boundless=True, fill_value=s.nodata if s.nodata is not None else 0).astype('float32')
        if s.nodata is not None and not np.isnan(s.nodata):
            a[a == s.nodata] = np.nan
    return a


def extent(bounds, scale=1.0):
    return [bounds[0]*scale, bounds[2]*scale, bounds[1]*scale, bounds[3]*scale]


def geom_patch(geom, scale=1.0, **kw):
    """Matplotlib patch for (multi)polygons with holes."""
    verts, codes = [], []
    polys = [geom] if geom.geom_type == 'Polygon' else [g for g in getattr(geom, 'geoms', []) if g.geom_type == 'Polygon']
    for p in polys:
        for ring in [p.exterior] + list(p.interiors):
            xy = np.asarray(ring.coords)*scale
            verts.append(xy); codes.append([MPath.MOVETO] + [MPath.LINETO]*(len(xy) - 2) + [MPath.CLOSEPOLY])
    if not verts:
        return None
    return PathPatch(MPath(np.concatenate(verts), np.concatenate(codes)), **kw)


def add_geom(ax, geom, scale=1.0, **kw):
    if geom is None or geom.is_empty:
        return
    if geom.geom_type in ('LineString', 'MultiLineString', 'LinearRing'):
        lines = [geom] if geom.geom_type != 'MultiLineString' else list(geom.geoms)
        for l in lines:
            xy = np.asarray(l.coords)*scale
            ax.plot(xy[:, 0], xy[:, 1], **kw)
        return
    if geom.geom_type == 'GeometryCollection':
        for g in geom.geoms:
            add_geom(ax, g, scale, **kw)
        return
    p = geom_patch(geom, scale, **kw)
    if p is not None:
        ax.add_patch(p)


def scalebar(ax, length_km, x=0.05, y=0.05, scale=1/1000, color=INK, label=None):
    """Scale bar for an axis in projected km (scale converts metres to axis units)."""
    x0, x1 = ax.get_xlim(); y0, y1 = ax.get_ylim()
    xs = x0 + x*(x1 - x0); ys = y0 + y*(y1 - y0)
    L = length_km*1000*scale
    ax.plot([xs, xs + L], [ys, ys], color=color, lw=1.4, solid_capstyle='butt', zorder=20)
    ax.text(xs + L/2, ys + 0.012*(y1 - y0), label or f'{length_km:g} km', ha='center', va='bottom', fontsize=5.5,
            color=color, zorder=20, path_effects=HALO)


def north(ax, x=0.94, y=0.88, size=0.06, color=INK):
    ax.annotate('', xy=(x, y + size), xytext=(x, y), xycoords='axes fraction',
                arrowprops=dict(arrowstyle='-|>', lw=0.8, color=color, mutation_scale=7), zorder=20)
    ax.text(x, y - 0.012, 'N', transform=ax.transAxes, ha='center', va='top', fontsize=6, color=color, zorder=20,
            path_effects=HALO)


def clean_map(ax):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(True); s.set_color(AXIS); s.set_linewidth(0.5)
    ax.set_aspect('equal')
