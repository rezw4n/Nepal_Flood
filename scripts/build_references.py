"""Assemble paper/references.json: the curated literature database (sources_ext/references_verified.json)
plus entries added during the analysis."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'sources_ext'/'references_verified.json'

EXTRA = [
    dict(key='NDRRMA2026update', authors='National Disaster Risk Reduction and Management Authority (NDRRMA)', year=2026,
         title='Bhotekoshi–Trishuli Flood: Search, Rescue and Relief Update (26 August–3 October 2026)',
         journal='NDRRMA, Government of Nepal, Kathmandu', volume='', pages='', doi='',
         url='https://ndrrma.gov.np/mediafiles/publications/Bhotekoshi-Trishuli_Flood_Update_From_August_26_2026_to_October_3_2026.pdf',
         verified=True, type='report'),
    dict(key='RDNA2026', authors='Government of Nepal, National Disaster Risk Reduction and Management Authority & National Planning Commission',
         year=2026, title='Rapid Damage and Needs Assessment (RDNA): Rasuwa–Bhotekoshi Flood 2026', journal='NDRRMA, Kathmandu',
         volume='', pages='', doi='',
         url='https://ndrrma.gov.np/mediafiles/rasuwa/Rapid_Damage_and_Needs_Assessment_RDNA_Rasuwa-Bhotekoshi_Flood_2026.pdf',
         verified=True, type='report'),
    dict(key='CHWRR2026', authors='Centre of Hydrology and Water Resources Research (CHWRR), Water and Energy Commission Secretariat',
         year=2026, title='Assessment Report II: Rasuwa–Bhote Koshi Flood Event, 2026 (2083)',
         journal='Government of Nepal, Kathmandu (13 September 2026)', volume='', pages='', doi='',
         url='https://giwmscdnone.gov.np/media/pdf_upload/1_Situation_Report_Bhotekoshi%20Flood_2026_CHWRR_hnmns6o.pdf',
         verified=True, type='report'),
    dict(key='Roy2026', authors='Roy, P. et al.', year=2026,
         title='26 August 2026 rock–ice avalanche in Nepal: rapid assessment of the cascading disaster using satellite data',
         journal='Journal of the Indian Society of Remote Sensing', volume='', pages='', doi='10.1007/s12524-026-02611-x',
         url='https://doi.org/10.1007/s12524-026-02611-x', verified=True, type='journal-article'),
    dict(key='Hassan2026', authors='Hassan, M. et al.', year=2026,
         title='Extreme heat and snow drought preconditioned the August 2026 Nepal rock–ice avalanche flood',
         journal='Research Square (preprint)', volume='', pages='', doi='10.21203/rs.3.rs-11167819/v1',
         url='https://doi.org/10.21203/rs.3.rs-11167819/v1', verified=True, type='preprint'),
    dict(key='WWA2026', authors='World Weather Attribution', year=2026,
         title='Rapid warming in the Himalaya exacerbates geohazard cascades beyond adaptation limits',
         journal='World Weather Attribution (17 September 2026)', volume='', pages='', doi='',
         url='https://worldweatherattribution.org/rapid-warming-in-the-himalaya-exacerbates-geohazard-cascades-beyond-adaptation-limits',
         verified=True, type='report'),
    dict(key='Barnes2014', authors='Barnes, R., Lehman, C. & Mulla, D.', year=2014,
         title='Priority-flood: an optimal depression-filling and watershed-labeling algorithm for digital elevation models',
         journal='Computers & Geosciences', volume='62', pages='117–127', doi='10.1016/j.cageo.2013.04.024',
         url='https://doi.org/10.1016/j.cageo.2013.04.024', verified=True, type='journal-article'),
    dict(key='Seabold2010', authors='Seabold, S. & Perktold, J.', year=2010, title='Statsmodels: econometric and statistical modeling with Python',
         journal='Proceedings of the 9th Python in Science Conference', volume='', pages='92–96', doi='10.25080/Majora-92bf1922-011',
         url='https://doi.org/10.25080/Majora-92bf1922-011', verified=True, type='proceedings'),
    dict(key='Pedregosa2011', authors='Pedregosa, F. et al.', year=2011, title='Scikit-learn: machine learning in Python',
         journal='Journal of Machine Learning Research', volume='12', pages='2825–2830', doi='',
         url='https://jmlr.org/papers/v12/pedregosa11a.html', verified=True, type='journal-article'),
    dict(key='Cohen1960', authors='Cohen, J.', year=1960, title='A coefficient of agreement for nominal scales',
         journal='Educational and Psychological Measurement', volume='20', pages='37–46', doi='10.1177/001316446002000104',
         url='https://doi.org/10.1177/001316446002000104', verified=True, type='journal-article'),
    dict(key='Otsu1979', authors='Otsu, N.', year=1979, title='A threshold selection method from gray-level histograms',
         journal='IEEE Transactions on Systems, Man, and Cybernetics', volume='9', pages='62–66', doi='10.1109/TSMC.1979.4310076',
         url='https://doi.org/10.1109/TSMC.1979.4310076', verified=True, type='journal-article'),
    dict(key='Runfola2020', authors='Runfola, D. et al.', year=2020, title='geoBoundaries: a global database of political administrative boundaries',
         journal='PLOS ONE', volume='15', pages='e0231866', doi='10.1371/journal.pone.0231866',
         url='https://doi.org/10.1371/journal.pone.0231866', verified=True, type='journal-article'),
    dict(key='HOT2026', authors='Humanitarian OpenStreetMap Team (HOT)', year=2026,
         title='Nepal flood building damage inventory and analysed-area polygon (fAIR-assisted labels on OpenStreetMap footprints)',
         journal='HOT raw-data API (retrieved 9 September 2026)', volume='', pages='', doi='',
         url='https://production-raw-data-api.s3.amazonaws.com/ISO3/NPL/buildings/hot_flood_npl_buildings_damage_overview.html',
         verified=True, type='dataset'),
    dict(key='UNDP2026RAPIDA', authors='United Nations Development Programme (UNDP)', year=2026,
         title='RAPIDA assessment of the floods in Nepal (StoryMap and feature services for building debris, economic estimate, exposure and affected population)',
         journal='UNDP GeoSMART (retrieved 9 September 2026)', volume='', pages='', doi='',
         url='https://geosmart.undp.org/arcgis/apps/storymaps/stories/7450cd01c584424f8a10ccfc166b167a', verified=True, type='dataset'),
    dict(key='WorldPopGlobal2', authors='WorldPop', year=2025,
         title='Global2 constrained population counts, 2015–2030, 100 m (release R2025A): Nepal',
         journal='WorldPop, University of Southampton (dataset)', volume='', pages='', doi='',
         url='https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/', verified=True, type='dataset'),
    dict(key='EarthSearch', authors='Element 84', year=2026,
         title='Earth Search STAC API: Sentinel-2 Level-2A cloud-optimised GeoTIFFs (collection sentinel-2-l2a)',
         journal='Amazon Web Services Open Data Registry (accessed 19–20 October 2026)', volume='', pages='', doi='',
         url='https://earth-search.aws.element84.com/v1', verified=True, type='dataset'),
    dict(key='RadioNepal2026', authors='Radio Nepal', year=2026,
         title='Government to relocate and rebuild Bhotekoshi flood-affected settlements in safer areas',
         journal='Radio Nepal Online (21 September 2026)', volume='', pages='', doi='',
         url='https://radionepalonline.com/en/2026/09/21/436388.html', verified=True, type='news'),
    # metadata checked on Crossref (chapter, book and article DOIs) and on the publisher pages, 20 October 2026
    dict(key='AhmedR2024Flood', authors='Ahmed, R.; Jarin, N. Z.; Rahman, O.', year=2024,
         title='Spatiotemporal dynamics of flood exposure in Bangladesh: a GIS and remote sensing based approach',
         journal='Flood Risk Management: Assessment and Strategy', book='Flood Risk Management: Assessment and Strategy',
         book_apa='Flood risk management: Assessment and strategy', editors_nature='Biswas, B. & Ghute, B. B.',
         editors_apa='B. Biswas & B. B. Ghute', publisher='Springer Nature Singapore', volume='', pages='1–22',
         doi='10.1007/978-981-97-2688-2_1', url='https://doi.org/10.1007/978-981-97-2688-2_1', verified=True,
         type='book-chapter'),
    dict(key='AhmedA2024Shelter', authors='Ahmed, A.; Ferdous, Z.; Kabir, M. H.; Rahman, O.; Ahmed, R.; Ryhan, M. A.',
         year=2024,
         title='Assessment of physical accessibility to cyclone shelters in the exposed coastal area of Bangladesh by using geospatial approach',
         journal='The Dhaka University Journal of Earth and Environmental Sciences', volume='13(2)', pages='63–75',
         doi='10.3329/dujees.v13i2.79455', url='https://doi.org/10.3329/dujees.v13i2.79455', verified=True,
         type='journal-article'),
    dict(key='CEMSdash2026', authors='Copernicus Emergency Management Service', year=2026,
         title='EMSR927 Flood in Nepal: rapid-mapping activation record (areas of interest, imagery and grading statistics) and vector products',
         journal='Copernicus EMS Rapid Mapping (accessed 20 October 2026)', volume='', pages='', doi='',
         url='https://rapidmapping.emergency.copernicus.eu/backend/dashboard-api/public-activations/?code=EMSR927',
         verified=True, type='dataset'),
    dict(key='DHM2026', authors='Department of Hydrology and Meteorology (DHM), Government of Nepal', year=2026,
         title='Real-time river water levels: Trishuli River at Kali Khola (station 449.91)',
         journal='Department of Hydrology and Meteorology, Kathmandu (accessed 19 October 2026)', volume='', pages='',
         doi='', url='https://hydrology.gov.np', verified=True, type='dataset'),
]
# author lists completed from the publication itself where the DOI record is incomplete
AUTHORS = {'Maharjan2021ICIMOD': 'Maharjan, S. B.; Steiner, J. F.; Shrestha, A. B.; Maharjan, A.; Nepal, S.; Shrestha, M. S.; '
                                 'Bajracharya, B.; Rasul, G.; Shrestha, M.; Jackson, M.; Gupta, N.'}


def main():
    R = json.loads(BASE.read_text(encoding='utf-8'))
    have = {r['key'] for r in R}
    R += [e for e in EXTRA if e['key'] not in have]
    R = [r for r in R if r.get('verified')]
    for r in R:
        r['authors'] = AUTHORS.get(r['key'], r['authors'])
    (ROOT/'paper'/'references.json').write_text(json.dumps(R, indent=1, ensure_ascii=False), encoding='utf-8')
    print(len(R), 'verified references')


if __name__ == '__main__':
    main()
