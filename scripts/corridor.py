"""Shared corridor geometry: channel nodes, transects and raster sampling.

Chainage is distance along the D8 path traced from the HiRISK source point
(terrain.py). Bank side is defined looking downstream.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import rasterio
import shapely
from scipy.spatial import cKDTree
from scipy.ndimage import uniform_filter1d

ROOT = Path(__file__).resolve().parents[1]
DER = ROOT/'data'/'derived'

# Reference places on the traced path (closest-approach chainage, km), checked in terrain QA.
PLACES = {'Source': (85.5282, 28.2887), 'Rasuwagadhi': (85.379, 28.274), 'Syaphrubesi': (85.343, 28.159),
          'Betrawati': (85.188, 27.969), 'Trishuli Bazar': (85.146, 27.917), 'Galchhi': (84.996, 27.805),
          'Benighat': (84.830, 27.814), 'Mugling': (84.556, 27.855), 'Devghat': (84.433, 27.710)}


class Channel:
    def __init__(self):
        p = pd.read_csv(DER/'flowpath_profile.csv')
        self.p = p
        self.xy = p[['x', 'y']].to_numpy()
        self.chain = p.chainage_m.to_numpy()
        self.z = p.z_channel.to_numpy()
        self.tree = cKDTree(self.xy)
        # Unit tangent from a ~300 m centred difference; curvature from heading change over ~600 m.
        k = 5
        xs = uniform_filter1d(self.xy[:, 0], 11, mode='nearest')
        ys = uniform_filter1d(self.xy[:, 1], 11, mode='nearest')
        dx = np.gradient(xs); dy = np.gradient(ys)
        n = np.hypot(dx, dy); n[n == 0] = 1
        self.tx, self.ty = dx/n, dy/n
        heading = np.unwrap(np.arctan2(self.ty, self.tx))
        dh = np.zeros_like(heading); dh[k:-k] = heading[2*k:] - heading[:-2*k]
        ds = np.zeros_like(heading); ds[k:-k] = self.chain[2*k:] - self.chain[:-2*k]
        ds[ds == 0] = np.nan
        self.curv = uniform_filter1d(np.nan_to_num(dh/ds), 21, mode='nearest')  # rad/m, + = turning left

    def locate(self, x, y):
        x = np.asarray(x, float); y = np.asarray(y, float)
        d, i = self.tree.query(np.c_[x, y])
        vx, vy = x - self.xy[i, 0], y - self.xy[i, 1]
        cross = self.tx[i]*vy - self.ty[i]*vx          # >0: left of flow direction
        side = np.where(cross > 0, 'left', 'right')
        curv = self.curv[i]
        outer = ((curv > 0) & (side == 'right')) | ((curv < 0) & (side == 'left'))
        return pd.DataFrame(dict(node=i, chainage_km=self.chain[i]/1000, dist_channel_m=d, bank=side,
                                 curvature_per_km=curv*1000, outer_bank=outer, z_channel_m=self.z[i]))

    def place_chainage(self):
        from pyproj import Transformer
        t = Transformer.from_crs('EPSG:4326', 'EPSG:32645', always_xy=True)
        out = {}
        for k, (lo, la) in PLACES.items():
            x, y = t.transform(lo, la)
            d, i = self.tree.query([x, y])
            out[k] = self.chain[i]/1000
        return out


def sample(path, x, y, band=1):
    with rasterio.open(path) as s:
        vals = np.array([v[0] for v in s.sample(zip(np.asarray(x), np.asarray(y)), indexes=band)], dtype='float64')
        if s.nodata is not None and not np.isnan(s.nodata):
            vals[vals == s.nodata] = np.nan
    return vals


def transect_metrics(ch, rem_path, flood_geom=None, half_len=1500, step=15, heights=(10, 20, 40)):
    """Per channel node: valley-floor width below REM thresholds and UNOSAT flow-extent width/edge REM."""
    from shapely.geometry import LineString
    if flood_geom is not None:
        shapely.prepare(flood_geom)
    with rasterio.open(rem_path) as s:
        rem = s.read(1); T = s.transform
    inv = ~T
    offs = np.arange(-half_len, half_len + step, step)
    rows = []
    for i in range(0, len(ch.xy), 3):  # every ~90 m
        nx, ny = -ch.ty[i], ch.tx[i]                 # left-pointing normal
        px = ch.xy[i, 0] + offs*nx; py = ch.xy[i, 1] + offs*ny
        c, r = inv * (px, py)
        r = r.astype(int); c = c.astype(int)
        ok = (r >= 0) & (r < rem.shape[0]) & (c >= 0) & (c < rem.shape[1])
        h = np.full(offs.shape, np.nan); h[ok] = rem[r[ok], c[ok]]
        row = dict(node=i, chainage_km=ch.chain[i]/1000)
        mid = len(offs)//2
        for thr in heights:
            below = np.nan_to_num(h, nan=1e9) < thr
            # contiguous run containing the channel node
            lo = mid
            while lo > 0 and below[lo-1]: lo -= 1
            hi = mid
            while hi < len(offs)-1 and below[hi+1]: hi += 1
            row[f'valley_width_{thr}m'] = (hi - lo + 1)*step if below[mid] else 0.0
        if flood_geom is not None:
            line = LineString(np.c_[px, py])
            inter = line.intersection(flood_geom)
            row['flow_width_m'] = inter.length
            if not inter.is_empty:
                # outermost flow-extent samples on each side of the channel
                inside = shapely.contains_xy(flood_geom, px, py)
                left = np.where(inside & (offs > 0))[0]; right = np.where(inside & (offs < 0))[0]
                row['flow_edge_rem_left'] = h[left.max()] if len(left) else np.nan
                row['flow_edge_rem_right'] = h[right.min()] if len(right) else np.nan
                row['flow_edge_dist_left'] = offs[left.max()] if len(left) else np.nan
                row['flow_edge_dist_right'] = -offs[right.min()] if len(right) else np.nan
        rows.append(row)
    return pd.DataFrame(rows)


if __name__ == '__main__':
    # Transects every ~90 m: valley-floor widths and UNOSAT flow-edge heights (used by build_buildings.py)
    from analyse import read_shape_zip, SRC
    flood, _, _ = read_shape_zip(SRC/'unosat_3.html')
    t = transect_metrics(Channel(), DER/'rem_utm30.tif', flood)
    t.to_csv(DER/'transects.csv', index=False, float_format='%.5g')
    print('wrote transects.csv', len(t))
