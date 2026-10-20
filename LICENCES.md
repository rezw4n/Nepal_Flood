# Data licences and attribution

Input data are not stored in this repository: `scripts/download_sources.py` and `scripts/fetch_ext.py` retrieve
them from the providers below, and the retrieval logs record the URL, date and SHA-256 checksum of each file.
Terms are those stated by each provider at retrieval (9 September and 19–20 October 2026); "unconfirmed" means
that no product-specific licence was found.

| Source | Use | Terms found | Treatment |
|---|---|---|---|
| HOT building-damage GeoJSON and analysed area | Damage labels | No product-specific licence; footprints from OpenStreetMap (ODbL) | Cite HOT and © OpenStreetMap contributors; confirm terms before redistributing derived labels |
| CEMS EMSR927 grading products | Damage labels, roads, bridges | Copernicus EMS products, © European Union | Cite the activation; attribution in figure legends |
| UNDP RAPIDA building, debris, economic and population services | Damage labels, debris model, monetary comparison | Item licence fields empty | Preserve UNDP attribution; confirm derivative-publication rights |
| UNOSAT flow extent (via UNESCO IHP-WINS) | Flow-edge heights, exposure | Public download; no redistribution licence established | Cite dataset DOI; confirm before redistributing |
| NDRRMA reports, RDNA, CHWRR report | Casualties, timeline, stage, monetary scope | Government publications | Cite; figures transcribed, documents not redistributed |
| Copernicus GLO-30 DEM | Terrain | Copernicus DEM licence (free use with attribution) | "Copernicus DEM © DLR e.V. 2010–2014 and © Airbus Defence and Space GmbH 2014–2018, provided under COPERNICUS by the European Union and ESA" |
| Sentinel-2 Level-2A (Earth Search) | Change indices, image chips | Copernicus Sentinel data terms (free, full and open) | "Contains modified Copernicus Sentinel data (2025, 2026)" in legends |
| Overture Maps 2026-09-23.1 (buildings, transportation, base) | Building stock, infrastructure | ODbL for OpenStreetMap-derived themes; other components as stated by Overture | Attribute Overture Maps Foundation and © OpenStreetMap contributors; share-alike applies to redistributed derived databases |
| GHS-BUILT-S R2023A (JRC) | Settlement growth | CC BY 4.0 | Cite dataset |
| WorldPop Global2 R2025A | Population | CC BY 4.0 | Cite dataset |
| geoBoundaries gbOpen NPL ADM3 | Local-level assignment | CC BY-SA 4.0 (metadata) | Cite; share-alike applies to redistributed boundary data |
| Planet disaster imagery catalogue | Not used | CC BY-NC 4.0 | No imagery downloaded or reproduced |
| ESA WorldCover 2021 v200 | Pre-event land cover in the flow extent | CC BY 4.0 | "© ESA WorldCover project 2021 / Contains modified Copernicus Sentinel data (2021) processed by ESA WorldCover consortium" |
| DHM hydrology API | Not used | Application key required (HTTP 403) | Access controls respected; no data obtained |

This repository contains aggregated tables, products derived from the Copernicus DEM and Sentinel-2 data, and
the figures and documents of the study. Building-level damage records from HOT, UNDP and UNOSAT are not included
because their redistribution terms have not been confirmed.
