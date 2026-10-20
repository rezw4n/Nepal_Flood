"""Reproduce the descriptive damage assessment from archived source data."""
from pathlib import Path
import datetime as dt
import hashlib
import io
import json
from zipfile import ZipFile
import numpy as np
import pandas as pd
import shapefile
from pyproj import CRS, Transformer
from shapely.geometry import shape
from shapely.ops import transform, unary_union
from shapely.affinity import translate
from shapely import make_valid

ROOT = Path(__file__).resolve().parents[1]
SRC, TAB, DATA = ROOT/'sources', ROOT/'tables', ROOT/'data'
PROJ = Transformer.from_crs('OGC:CRS84', 'EPSG:32645', always_xy=True).transform
CLASSES = ['no-damage', 'minor-damage', 'major-damage', 'destroyed', 'no-data']
THRESHOLDS = [0, .25, .5, .75, .9, .95]

def read(name):
    return json.loads((SRC/(name+'.json')).read_text(encoding='utf-8'))

def frame(name):
    return pd.DataFrame(f['properties'] for f in read(name)['features'])

def save(df,name):
    df.to_csv(TAB/(name+'.csv'), index=False, float_format='%.10g')

def read_shape_zip(path):
    if not path.exists() and path.with_suffix('.zip').exists():
        path=path.with_suffix('.zip')
    with ZipFile(path) as z:
        names=z.namelist()
        get=lambda ext: z.read(next(n for n in names if n.endswith(ext)))
        reader=shapefile.Reader(shp=io.BytesIO(get('.shp')), shx=io.BytesIO(get('.shx')), dbf=io.BytesIO(get('.dbf')))
        crs=CRS.from_wkt(get('.prj').decode())
        project=Transformer.from_crs(crs, 'EPSG:32645', always_xy=True).transform
        raw=[transform(project,shape(s.__geo_interface__)) for s in reader.shapes()]
        invalid=sum(not g.is_valid for g in raw)
        # Repair only explicitly counted invalid geometries; retained in quality results.
        repaired=[make_valid(g) if not g.is_valid else g for g in raw]
        return unary_union(repaired), invalid, crs.to_string()

def main():
    for p in [TAB,DATA]:p.mkdir(exist_ok=True)
    raw=read('hot_buildings'); aoi_raw=read('hot_aoi')
    geoms=[transform(PROJ,shape(f['geometry'])) for f in raw['features']]
    assert all(g.is_valid and not g.is_empty for g in geoms), 'Do not silently repair building footprints'
    aoi=unary_union([transform(PROJ,shape(f['geometry'])) for f in aoi_raw['features']])
    assert aoi.is_valid
    pts=[g.representative_point() for g in geoms]
    df=frame('hot_buildings')
    assert set(df.damage)==set(CLASSES)
    assert all(df.damage_class==df.damage.map(dict(zip(CLASSES,[0,1,2,3,-1]))))
    assert df.loc[df.damage!='no-data','damage_confidence'].between(0,1).all()
    df['area_m2']=[g.area for g in geoms]
    df['easting_m']=[p.x for p in pts];df['northing_m']=[p.y for p in pts]
    df['severe']=df.damage.isin(['major-damage','destroyed'])
    df['aoi_member']=[aoi.covers(p) for p in pts]
    admin_features=read('admin_local')['features']
    admins=[(f['properties'],transform(PROJ,shape(f['geometry']))) for f in admin_features]
    matches=[[a for a,g in admins if g.covers(p)] for p in pts]
    df['municipality']=[m[0]['adm3_name'] if len(m)==1 else 'UNRESOLVED' for m in matches]
    df['district']=[m[0]['adm2_name'] if len(m)==1 else 'UNRESOLVED' for m in matches]
    lower=aoi.bounds[1];width=(aoi.bounds[3]-lower)/3
    df['band']=np.array(['South','Middle','North'])[np.clip(((df.northing_m-lower)/width).astype(int),0,2)]
    df['northing_bin_2km']=np.floor(df.northing_m/2000).astype(int)*2
    flood, invalid_flood, flood_crs=read_shape_zip(SRC/'unosat_3.html')
    un_aoi, invalid_un_aoi, un_aoi_crs=read_shape_zip(SRC/'unosat_4.html')
    df['in_unosat_analysis']=[un_aoi.covers(p) for p in pts]
    df['in_unosat_extent']=[flood.covers(p) for p in pts]
    df['footprint_overlap_fraction']=[g.intersection(flood).area/g.area for g in geoms]
    counts=[]
    for c in CLASSES:
        sub=df[df.damage==c]; n=len(sub)
        counts.append(dict(damage=c,n=n,percent=100*n/len(df),area_m2=sub.area_m2.sum(),
          area_percent=100*sub.area_m2.sum()/df.area_m2.sum(),median_area_m2=sub.area_m2.median(),
          score_median=sub.damage_confidence.median(),score_q25=sub.damage_confidence.quantile(.25),
          score_q75=sub.damage_confidence.quantile(.75),score_min=sub.damage_confidence.min(),
          score_ge_090=int((sub.damage_confidence>=.9).sum()),
          unosat_inside=int(sub.in_unosat_extent.sum()),unosat_inside_percent=100*sub.in_unosat_extent.mean()))
    save(pd.DataFrame(counts),'building_damage')
    threshold=[]
    for t in THRESHOLDS:
        d=df[(df.damage_confidence>=t)&(df.damage!='no-data')]; n=len(d); severe=int(d.severe.sum()); missing=len(df)-n
        row=dict(threshold=t,retained=n,coverage_percent=100*n/len(df),abstained=missing,
                 severe=severe,severe_percent_retained=100*severe/n,
                 severe_percent_all=100*severe/len(df),conditional_lower_percent=100*severe/len(df),
                 conditional_upper_percent=100*(severe+missing)/len(df))
        row.update({c:int((d.damage==c).sum()) for c in CLASSES});threshold.append(row)
    save(pd.DataFrame(threshold),'confidence_sensitivity')
    def group_table(column):
        out=[]
        for name,d in df.groupby(column):
            row={column:name,'assessed':len(d),'severe':int(d.severe.sum()),'severe_percent':100*d.severe.mean(),
                 'area_m2':d.area_m2.sum(),'unosat_inside':int(d.in_unosat_extent.sum())}
            row.update({c:int((d.damage==c).sum()) for c in CLASSES})
            h=d[d.damage_confidence>=.9]; row['retained_090']=len(h)
            row['severe_090_percent']=100*h.severe.mean() if len(h) else None
            row['destroyed_area_m2']=d.loc[d.damage=='destroyed','area_m2'].sum()
            out.append(row)
        return pd.DataFrame(out).sort_values('severe',ascending=False)
    save(group_table('municipality'),'municipality_damage')
    save(group_table('band'),'band_damage')
    save(group_table('northing_bin_2km'),'northing_profile')
    band_tests=[]
    for shift in [-.1,0,.1]:
        labels=np.array(['South','Middle','North'])[np.clip(np.digitize(df.northing_m,[lower+width*(1+shift),lower+width*(2+shift)]),0,2)]
        for t in [0,.9]:
            for band in ['South','Middle','North']:
                d=df[(labels==band)&(df.damage_confidence>=t)]
                band_tests.append(dict(cut_shift_bandwidth=shift,threshold=t,band=band,n=len(d),
                                       severe_percent=100*d.severe.mean() if len(d) else None))
    save(pd.DataFrame(band_tests),'band_sensitivity')
    position=[]
    original_admin=df.municipality.tolist()
    for direction,dx,dy in [('original',0,0),('east',5,0),('west',-5,0),('north',0,5),('south',0,-5)]:
        shifted=[translate(p,dx,dy) for p in pts]
        inside=[flood.covers(p) for p in shifted]
        assignment=[]
        for p in shifted:
            found=[a['adm3_name'] for a,g in admins if g.covers(p)]
            assignment.append(found[0] if len(found)==1 else 'UNRESOLVED')
        position.append(dict(direction=direction,dx_m=dx,dy_m=dy,aoi_members=sum(aoi.covers(p) for p in shifted),
                             unosat_members=sum(inside),severe_inside=sum(bool(s) and i for s,i in zip(df.severe,inside)),
                             changed_municipality=sum(x!=y for x,y in zip(assignment,original_admin))))
    save(pd.DataFrame(position),'position_sensitivity')
    # Full public UNDP attribute inventories, with pagination checked against count requests.
    debris_features=sum([read('debris_features_'+str(o))['features'] for o in [0,2000]],[])
    debris=pd.DataFrame(f['properties'] for f in debris_features)
    assert len(debris)==read('debris_count')['count']==debris.objectid.nunique()
    dp_features=sum([read('damagepoints_features_'+str(o))['features'] for o in [0,2000]],[])
    assert len(dp_features)==read('damagepoints_count')['count']
    save(debris.drop(columns=[c for c in debris.columns if c.startswith('addr_') or c in ['name','name_en','name_ne','longitude_latitude']]),'undp_debris_records')
    debris_summary=debris.groupby(['damage_level'],dropna=False).agg(records=('objectid','size'),
                  debris_t=('debris','sum'),debris_total_t=('debris_total','sum'),floor_area_m2=('surface_m2','sum')).reset_index()
    save(debris_summary,'regional_damage')
    debris['municipality']=debris.adm3_name.fillna('Unassigned')
    debris_muni=debris.groupby(['municipality'],dropna=False).agg(records=('objectid','size'),
           debris_t=('debris','sum'),debris_total_t=('debris_total','sum'),floor_area_m2=('surface_m2','sum')).reset_index()
    dcounts=pd.crosstab(debris.municipality,debris.damage_level).reset_index()
    debris_muni=debris_muni.merge(dcounts,on='municipality',how='left').sort_values('debris_t',ascending=False)
    save(debris_muni,'regional_municipality_damage')
    core=debris[debris.source_y.isin(['EMSR927','Sertit'])].copy()
    source_groups=debris.groupby('source_y').agg(records=('objectid','size'),debris_t=('debris','sum')).reset_index()
    save(source_groups,'regional_source_groups')
    core_muni=core.groupby('municipality').agg(assessed=('objectid','size'),debris_t=('debris','sum'),
            floor_area_m2=('surface_m2','sum')).reset_index()
    core_muni=core_muni.merge(pd.crosstab(core.municipality,core.damage_level).reset_index(),on='municipality')
    core_muni['share_debris_percent']=100*core_muni.debris_t/core.debris.sum()
    core_muni['destroyed_share_records_percent']=100*core_muni.Destroyed/core_muni.assessed
    save(core_muni.sort_values('debris_t',ascending=False),'core_regional_municipalities')
    core_class=core.groupby('damage_level').agg(records=('objectid','size'),debris_t=('debris','sum')).reset_index()
    core_class['percent']=100*core_class.records/len(core)
    save(core_class,'core_regional_damage')
    save(core.groupby(['municipality','source_y','damage_level']).size().rename('n').reset_index(),'core_source_classes')
    econ=frame('economic_features')
    econ=econ.rename(columns={'shapename':'province','damage_usd':'lower_usd','damage_u_1':'central_usd','damage_u_2':'upper_usd'})
    assert np.allclose(econ.lower_usd,econ.central_usd*.7) and np.allclose(econ.upper_usd,econ.central_usd*1.3)
    assert np.allclose(econ.damage_rat,100*econ.central_usd/econ.exposure_u,atol=1e-7)
    econ['share_percent']=100*econ.central_usd/econ.central_usd.sum()
    save(econ[['province','lower_usd','central_usd','upper_usd','share_percent','damage_rat','exposure_u']],'economic_damage')
    population=frame('population_features').sort_values('people_affected',ascending=False)
    save(population[['adm2_name','adm3_name','people_affected','share_of_population_affected']],'affected_population')
    exposure=frame('exposure_features')
    save(exposure[['adm2_name','adm3_name','name','pop_total','building_count','road_km','bridge_count','health_count','educ_count']],'exposure_by_municipality')
    ex_sum=exposure.groupby('name')[['pop_total','building_count','road_km','bridge_count','health_count','educ_count']].sum().reset_index()
    save(ex_sum,'exposure_scenarios')
    integrity=dict(n=len(df),duplicate_osm_ids=int(df.osm_id.duplicated().sum()),
        duplicate_geometries=len(geoms)-len({g.wkb for g in geoms}),invalid_building_geometries=0,
        missing_properties=int(df[['osm_id','damage_class','damage','damage_confidence']].isna().sum().sum()),
        aoi_members=int(df.aoi_member.sum()),aoi_centroid_members=sum(aoi.covers(g.centroid) for g in geoms),
        aoi_intersections=sum(aoi.intersects(g) for g in geoms),aoi_area_km2=aoi.area/1e6,
        aoi_bounds_wgs84=shape(aoi_raw['features'][0]['geometry']).bounds,
        footprint_area_m2=df.area_m2.sum(),footprint_union_area_m2=unary_union(geoms).area,
        confidence_below_025=int((df.damage_confidence<.25).sum()),
        admin_unmatched=sum(len(m)==0 for m in matches),admin_multiple=sum(len(m)>1 for m in matches),
        severe=int(df.severe.sum()),severe_percent=100*df.severe.mean(),
        severe_area_percent=100*df.loc[df.severe,'area_m2'].sum()/df.area_m2.sum(),
        any_damage=int(df.damage.isin(['minor-damage','major-damage','destroyed']).sum()),
        classified=int((df.damage!='no-data').sum()),unclassified=int((df.damage=='no-data').sum()),
        unosat_flood_area_km2=flood.area/1e6,unosat_analysis_area_km2=un_aoi.area/1e6,
        unosat_invalid_repaired=invalid_flood,unosat_analysis_invalid_repaired=invalid_un_aoi,
        unosat_flood_crs=flood_crs,unosat_analysis_crs=un_aoi_crs,
        in_unosat_analysis=int(df.in_unosat_analysis.sum()),in_unosat_extent=int(df.in_unosat_extent.sum()),
        severe_in_unosat=int(df.loc[df.severe,'in_unosat_extent'].sum()),
        footprint_any_unosat=int((df.footprint_overlap_fraction>0).sum()),
        footprint_half_unosat=int((df.footprint_overlap_fraction>=.5).sum()),
        hot_buildings_sha256=hashlib.sha256((SRC/'hot_buildings.json').read_bytes()).hexdigest(),
        hot_aoi_sha256=hashlib.sha256((SRC/'hot_aoi.json').read_bytes()).hexdigest(),
        user_buildings_match=((ROOT.parent/'hot_flood_npl_buildings_damage.geojson').read_bytes()==(SRC/'hot_buildings.json').read_bytes()) if (ROOT.parent/'hot_flood_npl_buildings_damage.geojson').exists() else None,
        user_aoi_match=((ROOT.parent/'hot_flood_npl_buildings_damage_analyzed_aoi.geojson').read_bytes()==(SRC/'hot_aoi.json').read_bytes()) if (ROOT.parent/'hot_flood_npl_buildings_damage_analyzed_aoi.geojson').exists() else None,
        regional_records=len(debris),regional_duplicate_building_ids=int(debris.building_id.duplicated().sum()),
        regional_damage_levels={str(k):int(v) for k,v in debris.damage_level.value_counts().items()},
        regional_debris_t=float(debris.debris.sum()),regional_debris_total_t=float(debris.debris_total.sum()),
        core_records=len(core),core_debris_t=float(core.debris.sum()),
        core_synthetic_count=int((core.synthetic==1).sum()),
        core_damage_levels={str(k):int(v) for k,v in core.damage_level.value_counts().items()},
        core_sources={str(k):int(v) for k,v in core.source_y.value_counts().items()},
        regional_missing_adm2=int(debris.adm2_name.isna().sum()),
        regional_synthetic={str(k):int(v) for k,v in debris.synthetic.value_counts(dropna=False).items()},
        regional_sources={str(k):int(v) for k,v in debris.source_y.value_counts(dropna=False).items()},
        economic_central_usd=float(econ.central_usd.sum()),economic_lower_usd=float(econ.lower_usd.sum()),
        economic_upper_usd=float(econ.upper_usd.sum()),people_affected=int(population.people_affected.sum()),
        affected_municipalities=len(population),affected_districts=int(population.adm2_name.nunique()),
        top3_affected_people=int(population.people_affected.head(3).sum()),
        generated_utc=dt.datetime.now(dt.timezone.utc).isoformat())
    (DATA/'results.json').write_text(json.dumps(integrity,indent=2),encoding='utf-8')
    df.to_csv(DATA/'building_analysis.csv',index=False)
    # Keep the raw combined regional geometries local for map generation.
    (DATA/'undp_debris_combined.geojson').write_text(json.dumps({'type':'FeatureCollection','features':debris_features}),encoding='utf-8')
    print(json.dumps(integrity,indent=2))
    print('\nLOCAL MUNICIPALITIES\n'+group_table('municipality').to_string(index=False))
    print('\nREGIONAL MUNICIPALITIES\n'+debris_muni.to_string(index=False))
    print('\nCLASSES\n'+pd.DataFrame(counts).to_string(index=False))
    print('\nCONFIDENCE\n'+pd.DataFrame(threshold).to_string(index=False))

if __name__=='__main__':main()
