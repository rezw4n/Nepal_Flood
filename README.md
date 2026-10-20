# What height is safe? An analysis of building destruction along the 207-km path of Nepal's 2026 flood

Code, data products and manuscript files for a study of the buildings destroyed by the 26 August 2026 rock–ice
avalanche and flood in the Bhote Koshi–Trishuli valley, Nepal.

**Authors:** Nusrat Zahan Jarin (Department of Geography, University of California, Santa Barbara), Obaidur Rahman
(Department of Geography, Oklahoma State University) and Rezwan Ahmed (Department of Geography and Environment,
University of Dhaka).

## Main results

- Combining the Copernicus EMS, HOT and UNDP RAPIDA damage maps with the government's damage assessment gives
  **5,781 damaged buildings, 4,530 of them destroyed**, along the 207-km flood path.
- **Height above the pre-event river channel** was the dominant control on destruction (spatially cross-validated
  AUC 0.95).
- The height at which destruction became more likely than not fell from **about 60 m in the gorge to about 7 m
  110 km downstream**, closely following the independently mapped flow margin (Spearman ρ = 0.97).
- Built-up area less than 10 m above the river grew **17-fold between 1975 and 2020**.
- An automatic alert triggered by the seismic signal could have given at least 30 minutes of warning to **73% of
  destroyed buildings**, against 24% for the SMS warning that was sent.

## Contents

| Folder | Contents |
|---|---|
| `paper/` | Manuscript (`Nepal_Flood_Damage_Assessment`), Supplementary Information and the full-length article (`Nepal Flood Document.docx`) in Word, PDF and Markdown; `templates/` holds their sources and `references.json` the reference list |
| `scripts/` | Data download, analysis, figure and document-building code |
| `figures/` | Main and supplementary figures (PNG, PDF and editable SVG) |
| `tables/` | Aggregated source data for every table and figure |
| `data/derived/` | Height-above-channel raster, traced flow path and transects, result summaries and Monte Carlo draws |
| `sources/`, `sources_ext/` | Retrieval logs (URL, date and SHA-256 checksum of every input) and the reference database |

## Reproducing the analysis

Requirements: Windows with PowerShell and Python 3.14. The PDF export uses the Times New Roman and Arial fonts
installed with Windows.

```powershell
powershell -ExecutionPolicy Bypass -File .\rebuild.ps1 -Refresh -Sentinel2
```

`-Refresh` downloads all input data (damage maps, official reports, Copernicus DEM, Overture Maps, GHSL, WorldPop and
Copernicus EMS products) and `-Sentinel2` rebuilds the Sentinel-2 composites; both need an internet connection. The
script creates a virtual environment with the pinned packages in `requirements.txt`, runs the analysis, renders all
figures, writes the documents in `paper/` and checks them (`validation_report.json`). Every number in the documents is
inserted by the scripts from the analysis outputs. Online services can change, so a later download may differ slightly
from the archived run; compare against the checksums in the retrieval logs.

## Data

Input data are not stored here; the scripts download them from the providers listed in Supplementary Table 1 and in
[LICENCES.md](LICENCES.md). Building-level damage records from HOT, UNDP and UNOSAT are not redistributed because their
redistribution terms have not been confirmed.

## Citation

Please cite the paper when using this code or its results; citation details are in [CITATION.cff](CITATION.cff) and
will be completed on publication.
