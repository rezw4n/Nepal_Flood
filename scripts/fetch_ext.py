"""Retrieve the additional open datasets used in the extended analysis.

Every request is logged to sources_ext/retrieval_log_ext.json with UTC time, URL,
HTTP status, byte size and SHA-256 of the stored file. Run a subset with e.g.
    python scripts/fetch_ext.py overture worldcover
"""
from pathlib import Path
import datetime as dt
import hashlib
import json
import sys
import zipfile
import io
import requests
import numpy as np
import rasterio
from rasterio.windows import from_bounds

ROOT = Path(__file__).resolve().parents[1]
EXT = ROOT/'sources_ext'
LOG = EXT/'retrieval_log_ext.json'
BBOX = (84.40, 27.66, 85.60, 28.36)          # corridor window, lon/lat (source to Devghat)
OVERTURE_RELEASE = '2026-09-23.1'
OVERTURE = f's3://overturemaps-us-west-2/release/{OVERTURE_RELEASE}'
WORLDCOVER = 'https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ESA_WorldCover_10m_2021_v200_N27E084_Map.tif'
WORLDPOP = 'https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/{y}/NPL/v1/100m/constrained/npl_pop_{y}_CN_100m_R2025A_v1.tif'
GHSL = ('https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_S_GLOBE_R2023A/'
        'GHS_BUILT_S_E{y}_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_S_E{y}_GLOBE_R2023A_54009_100_V1_0_R6_C26.zip')


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def log(entry):
    entries = json.loads(LOG.read_text(encoding='utf-8')) if LOG.exists() else []
    entry['retrieved_utc'] = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
    entries.append(entry)
    LOG.write_text(json.dumps(entries, indent=1), encoding='utf-8')
    print(entry)


def download(url, path, timeout=600):
    path.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=timeout) as r:
        status = r.status_code
        if status == 200:
            with open(path, 'wb') as f:
                for chunk in r.iter_content(1 << 20):
                    f.write(chunk)
    entry = dict(url=url, file=str(path.relative_to(ROOT)), status=status)
    if status == 200:
        entry.update(bytes=path.stat().st_size, sha256=sha256(path))
    log(entry)
    return status == 200


def duck():
    import duckdb
    con = duckdb.connect()
    for s in ['INSTALL httpfs', 'LOAD httpfs', 'INSTALL spatial', 'LOAD spatial',
              "SET s3_region='us-west-2'", 'SET enable_progress_bar=false']:
        con.execute(s)
    return con


def overture():
    """Buildings, transport segments and infrastructure inside the corridor window."""
    out = EXT/'overture'; out.mkdir(parents=True, exist_ok=True)
    x0, y0, x1, y1 = BBOX
    where = f'bbox.xmin >= {x0} AND bbox.xmax <= {x1} AND bbox.ymin >= {y0} AND bbox.ymax <= {y1}'
    queries = {
        'buildings': f"""SELECT id, sources[1].dataset AS source_dataset, sources[1].update_time AS source_update,
                height, num_floors, subtype, class, ST_AsWKB(geometry) AS wkb
            FROM read_parquet('{OVERTURE}/theme=buildings/type=building/*', hive_partitioning=1) WHERE {where}""",
        'segments': f"""SELECT id, subtype, class, subclass, names.primary AS name, road_flags, ST_AsWKB(geometry) AS wkb
            FROM read_parquet('{OVERTURE}/theme=transportation/type=segment/*', hive_partitioning=1) WHERE {where}""",
        'infrastructure': f"""SELECT id, subtype, class, names.primary AS name, sources[1].record_id AS osm_record,
                ST_AsWKB(geometry) AS wkb
            FROM read_parquet('{OVERTURE}/theme=base/type=infrastructure/*', hive_partitioning=1) WHERE {where}""",
        'water': f"""SELECT id, subtype, class, names.primary AS name, ST_AsWKB(geometry) AS wkb
            FROM read_parquet('{OVERTURE}/theme=base/type=water/*', hive_partitioning=1)
            WHERE {where} AND subtype IN ('river','stream','canal','lake','reservoir','water')""",
    }
    con = duck()
    for name, q in queries.items():
        path = out/f'{name}.parquet'
        con.execute(f"COPY ({q}) TO '{path.as_posix()}' (FORMAT PARQUET)")
        n = con.execute(f"SELECT count(*) FROM read_parquet('{path.as_posix()}')").fetchone()[0]
        log(dict(url=f'{OVERTURE}/{name} bbox={BBOX}', file=str(path.relative_to(ROOT)), status=200,
                 records=int(n), bytes=path.stat().st_size, sha256=sha256(path), release=OVERTURE_RELEASE))


def clip_remote(url, path, bounds_lonlat):
    """Windowed read of a remote COG (no full download)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open('/vsicurl/' + url) as src:
        win = from_bounds(*bounds_lonlat, transform=src.transform).round_offsets().round_lengths()
        data = src.read(1, window=win)
        meta = src.profile.copy()
        meta.update(width=data.shape[1], height=data.shape[0], transform=src.window_transform(win),
                    compress='deflate', tiled=True, blockxsize=512, blockysize=512)
        meta.pop('photometric', None)
    with rasterio.open(path, 'w', **meta) as dst:
        dst.write(data, 1)
    log(dict(url=url, file=str(path.relative_to(ROOT)), status=200, window_lonlat=list(bounds_lonlat),
             bytes=path.stat().st_size, sha256=sha256(path)))


def worldcover():
    clip_remote(WORLDCOVER, EXT/'worldcover'/'worldcover2021_corridor.tif', BBOX)


def worldpop():
    for y in (2015, 2020, 2026):
        url = WORLDPOP.format(y=y)
        tmp = EXT/'worldpop'/f'npl_pop_{y}_CN_100m_R2025A_v1.tif'
        if download(url, tmp):
            # keep only the corridor window to limit archive size
            clip = EXT/'worldpop'/f'worldpop_{y}_corridor.tif'
            with rasterio.open(tmp) as src:
                win = from_bounds(*BBOX, transform=src.transform).round_offsets().round_lengths()
                data = src.read(1, window=win)
                meta = src.profile.copy()
                meta.update(width=data.shape[1], height=data.shape[0], transform=src.window_transform(win), compress='deflate')
            with rasterio.open(clip, 'w', **meta) as dst:
                dst.write(data, 1)
            log(dict(url=url, file=str(clip.relative_to(ROOT)), status=200, derived_from=tmp.name,
                     window_lonlat=list(BBOX), bytes=clip.stat().st_size, sha256=sha256(clip)))
            tmp.unlink()


def ghsl():
    from pyproj import Transformer
    to_moll = Transformer.from_crs('EPSG:4326', 'ESRI:54009', always_xy=True)
    xs, ys = to_moll.transform([BBOX[0], BBOX[2], BBOX[0], BBOX[2]], [BBOX[1], BBOX[1], BBOX[3], BBOX[3]])
    mb = (min(xs) - 1000, min(ys) - 1000, max(xs) + 1000, max(ys) + 1000)
    for y in range(1975, 2021, 5):
        url = GHSL.format(y=y)
        r = requests.get(url, timeout=600)
        if r.status_code != 200:
            log(dict(url=url, status=r.status_code)); continue
        z = zipfile.ZipFile(io.BytesIO(r.content))
        tif = next(n for n in z.namelist() if n.endswith('.tif'))
        raw = EXT/'ghsl'/tif
        raw.parent.mkdir(parents=True, exist_ok=True)
        raw.write_bytes(z.read(tif))
        clip = EXT/'ghsl'/f'ghs_built_s_{y}_corridor.tif'
        with rasterio.open(raw) as src:
            win = from_bounds(*mb, transform=src.transform).round_offsets().round_lengths()
            data = src.read(1, window=win)
            meta = src.profile.copy()
            meta.update(width=data.shape[1], height=data.shape[0], transform=src.window_transform(win), compress='deflate')
        with rasterio.open(clip, 'w', **meta) as dst:
            dst.write(data, 1)
        log(dict(url=url, file=str(clip.relative_to(ROOT)), status=200, zip_bytes=len(r.content),
                 zip_sha256=hashlib.sha256(r.content).hexdigest(), window_moll=list(mb),
                 bytes=clip.stat().st_size, sha256=sha256(clip)))
        raw.unlink()


CEMS_API = 'https://mapping.emergency.copernicus.eu/activations/api/activations/EMSR927/'
CEMS_S3 = 'https://rapidmapping-viewer.s3.eu-west-1.amazonaws.com/EMSR927'
CEMS_DASHBOARD = 'https://rapidmapping.emergency.copernicus.eu/backend/dashboard-api/public-activations/?code=EMSR927'
CEMS_LAYERS = {
    ('AOI01', 'GRA_PRODUCT', 1): ['builtUpP', 'facilitiesA', 'observedEventA', 'transportationA', 'transportationL', 'transportationP'],
    ('AOI02', 'GRA_PRODUCT', 2): ['builtUpP', 'facilitiesA', 'observedEventA', 'transportationL', 'transportationP'],
    ('AOI03', 'GRA_PRODUCT', 1): ['builtUpP', 'facilitiesA', 'facilitiesL', 'notAnalysedA', 'observedEventA',
                                   'transportationA', 'transportationL', 'transportationP'],
    ('AOI03', 'GRA_MONIT01', 1): ['builtUpP', 'facilitiesA', 'facilitiesL', 'notAnalysedA', 'observedEventA',
                                   'transportationA', 'transportationL', 'transportationP'],
    ('AOI05', 'GRA_PRODUCT', 2): ['builtUpP', 'notAnalysedA', 'observedEventA', 'transportationL'],
    ('AOI05', 'GRA_MONIT01', 2): ['builtUpP', 'notAnalysedA', 'observedEventA', 'transportationL', 'transportationP'],
}


def cems():
    """Copernicus EMS rapid-mapping grading layers for EMSR927 (public viewer JSON) and activation metadata."""
    out = EXT/'cems'
    download(CEMS_API, out/'EMSR927_activation.json', timeout=120)
    download(CEMS_DASHBOARD, out/'EMSR927_dashboard.json', timeout=120)   # AOI polygons, images, AOI statistics
    for (aoi, prod, v), layers in CEMS_LAYERS.items():
        for lay in layers:
            name = f'EMSR927_{aoi}_{prod}_{lay}_v{v}.json'
            download(f'{CEMS_S3}/{aoi}/{prod}/{name}', out/name, timeout=300)


def dem():
    """Copernicus GLO-30 tiles (AWS open data); existing tiles are checksummed and logged, not re-downloaded."""
    base = 'https://copernicus-dem-30m.s3.amazonaws.com'
    for t in ('N27_00_E084_00', 'N27_00_E085_00', 'N28_00_E084_00', 'N28_00_E085_00'):
        name = f'Copernicus_DSM_COG_10_{t}_DEM'
        url, path = f'{base}/{name}/{name}.tif', ROOT/'sources_ext'/'dem'/f'{name}.tif'
        if path.exists():
            log(dict(url=url, file=str(path.relative_to(ROOT)), status='cached', bytes=path.stat().st_size,
                     sha256=sha256(path)))
        else:
            download(url, path)


if __name__ == '__main__':
    jobs = dict(dem=dem, overture=overture, worldcover=worldcover, worldpop=worldpop, ghsl=ghsl, cems=cems)
    for name in (sys.argv[1:] or list(jobs)):
        jobs[name]()
