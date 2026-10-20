# What height is safe? An analysis of building destruction along the 207-km path of Nepal's 2026 flood

Rezwan Ahmed^1^, Nusrat Zahan Jarin^2^, Obaidur Rahman^3^

^1^Department of Geography and Environment, University of Dhaka, Dhaka, Bangladesh

^2^Department of Geography, University of California, Santa Barbara, CA, USA

^3^Department of Geography, Oklahoma State University, Stillwater, OK, USA

ORCID iD, Rezwan Ahmed: [https://orcid.org/0009-0002-8003-099X](https://orcid.org/0009-0002-8003-099X)

ORCID iD, Nusrat Zahan Jarin: [https://orcid.org/0000-0003-2657-8559](https://orcid.org/0000-0003-2657-8559)

## Abstract

On 26 August 2026, a rock–ice avalanche from Langtang Lirung, Nepal, generated a flood that travelled 207 km down the Bhote Koshi–Trishuli valley, leaving 1,455 dead and 5,285 missing. Reconciling five satellite and official damage inventories, we find 5,781 damaged buildings, 4,530 of them destroyed. Height above the pre-event channel dominated a spatially cross-validated model of destruction (AUC 0.95). The height at which destruction became more likely than not fell from about 60 m in the gorge to about 7 m 110 km downstream, tracking independently mapped flow margins (Spearman ρ = 0.97). Built-up area less than 10 m above the channel had grown 17-fold since 1975. An automatic seismic alert could have given at least 30 minutes of warning for 73% of destroyed buildings, against 24% under the SMS actually issued. Damage-calibrated heights offer an objective basis for danger zoning and warning in Himalayan valleys.

**Keywords:** cascading hazard; flood damage; Nepal; Bhote Koshi–Trishuli; height above the river; rapid damage mapping; early warning; recovery planning

## 1. Introduction

Cascading hazards that begin with a slope or glacier failure high in a mountain range and end as a flood far downstream are among the deadliest processes in High Mountain Asia (Kirschbaum et al., 2019; Mani et al., 2023). Recent examples include the 2021 Chamoli rock–ice avalanche in India (Shugar et al., 2021), the 2021 Melamchi flood (Chen et al., 2025; Maharjan et al., 2021) and the 2024 Thame outburst (Khadka et al., 2026) in Nepal, and the 2023 South Lhonak cascade in Sikkim (Sattar et al., 2025). Each overwhelmed settlements and hydropower assets that had been built in narrow valley floors, many tens of kilometres from the source. Glacier and permafrost change is altering the likelihood of such failures (R. Ahmed et al., 2026; Bashkova et al., 2026; Hock et al., 2019), while the population and infrastructure exposed to glacial floods and riverine hazards continue to grow (D. Li et al., 2022; Rentschler et al., 2023; Schwanghart et al., 2016; Taylor et al., 2023; Zheng et al., 2021).

Measuring the damage these floods cause is itself difficult. Research on flood losses has long pointed to incomplete observations, uncertain asset values and the divergence of loss models (Gerl et al., 2016; Merz et al., 2010), problems that are most acute in data-scarce mountain regions (Romali et al., 2025). Cascading floods add a further complication, because damage develops through the interaction of a moving, sediment-laden flow with the valley it passes through (Chen et al., 2025; Cook et al., 2018), so that its pattern can change markedly from one reach to the next.

At 08:37 Nepal Time (NPT) on 26 August 2026, bedrock and part of a hanging glacier failed on the north face of Langtang Lirung at about 5,200 m above sea level (ICIMOD, 2026; Liu et al., 2026; Roy et al., 2026). Estimates of the failed volume range from 99 ± 10 × 10^6^ m^3^ (Roy et al., 2026) to about 132 × 10^6^ m^3^ (ICIMOD, 2026). The mass struck the Lhende glacier, briefly dammed the Lhende Khola and released a debris-laden flood that reached the Nepal–China border at Rasuwagadhi within about seven minutes and the confluence with the Kali Gandaki at Devghat, 207 km from the source, in the afternoon (CHWRR, 2026; NDRRMA, 2026). By 3 October, Nepal's National Disaster Risk Reduction and Management Authority (NDRRMA) had recorded 1,455 deaths and 5,285 people missing; Chinese authorities reported 43 deaths and 519 missing at Gyirong (Kyirong) port (ICIMOD, 2026; NDRRMA, 2026). The government's Rapid Damage and Needs Assessment (RDNA) estimated US$1.81 billion of physical damage, US$2.70 billion of total effects (6.7% of gross domestic product) and US$4.77 billion of recovery needs (NDRRMA & NPC, 2026). The consequences extended well beyond buildings: about 10,000 households needed immediate relief, three health posts were fully damaged, one hospital was partly damaged and access to two hospitals was cut, while damaged water and sanitation systems raised further public-health concerns (WHO, 2026). The event followed a supraglacial-lake outburst in July 2025 that had already damaged the same border crossing and hydropower plants (Q. Xu et al., 2026; Zhang et al., 2026).

Within days, the disaster had been mapped by several independent systems: the Copernicus Emergency Management Service (CEMS) (Copernicus EMS, 2026a, 2026b), the United Nations Satellite Centre (UNOSAT) (UNOSAT, 2026), the Humanitarian OpenStreetMap Team (HOT) (HOT, 2026), the United Nations Development Programme (UNDP) (UNDP, 2026) and the World Bank (World Bank & GFDRR, 2026), alongside the government's RDNA. An early analysis of the first rapid maps counted 695 destroyed building points and 15.7 km of destroyed road (R. Li, 2026). Such rapid products are indispensable when valleys are cut off (Voigt et al., 2016), but they differ in imagery, coverage, damage scales and purpose, and their reported totals for this event ranged from fewer than 1,000 to more than 12,000 buildings depending on what was counted (R. Li, 2026; Liu et al., 2026; NDRRMA & NPC, 2026). They are rarely reconciled, and even more rarely used to ask why particular buildings were destroyed while neighbours survived. That question now matters for recovery. The government has announced that settlements in high-risk parts of the corridor will be relocated (Radio Nepal, 2026), but no event-calibrated, physically grounded basis yet exists for deciding where reconstruction is unsafe, and the warning of 26 August reached many riverside communities only after the flood had passed (Acharya, 2026; ICIMOD, 2026; C. Xu, 2026).

This study reconciles the building-damage records of four mapping products and the RDNA into a single corridor-scale inventory, and relates it to the pre-event terrain, to Sentinel-2 surface change, to the documented propagation of the flood wave and to five decades of settlement growth. It asks four questions. How much damage did the products record, and how far do they agree? What controlled which buildings were destroyed? How did the destructive reach of the flood change downstream? And how much warning time was available, and how was it used? We show that height above the pre-event river channel explains most of where buildings were destroyed; that the height reached by destruction declined systematically downstream, in step with independently mapped flow margins and the decay of the wave front; that settlement had expanded fastest into exactly this destructive zone; and that warning time was available for most destroyed buildings but was not used. We translate these results into municipality-level priorities for inspection, debris clearance, danger-zone mapping and early warning.

## 2. Data and Methodology

### 2.1 Study area

The study area is the corridor followed by the flood from the failure on the north face of Langtang Lirung to the confluence of the Trishuli and Kali Gandaki rivers at Devghat (Figure 1; the full corridor is mapped in Section 3.1). Measured along the traced flow path, the flood descended the Lhende Khola to the Nepal–China border at Rasuwagadhi (23 km from the source), followed the Bhote Koshi past Timure to Syaphrubesi (38 km), where the river becomes the Trishuli, and passed Betrawati (69 km), Trishuli Bazar–Bidur (78 km), Galchhi (106 km), Benighat (129 km) and Mugling (170 km) before reaching Devghat (206.8 km). Over this distance the channel falls from about 5,050 m to 180 m above sea level. More than 3,300 m of this drop occurs before the border; between Rasuwagadhi and Syaphrubesi the river runs through a narrow gorge in which the valley floor less than 20 m above the river is typically about 100 m wide, whereas below Betrawati it is about 260 m wide.

![Figure 1](figures/figure_study_area.jpg)

**Figure 1.** Location of the study area. (a) Location of Nepal. (b) Nepal and its districts, with the study area outlined in red. (c) The Bhote Koshi–Trishuli corridor in Rasuwa, Nuwakot and Dhading districts, with buildings recorded as affected by the 26 August 2026 flood (magenta). (d) Enlarged view of the area marked in (c).

The flood affected Rasuwa, Nuwakot, Dhading and Chitwan districts in Bagmati Province and Gorkha and Tanahun districts in Gandaki Province, and the government declared 15 municipalities disaster crisis-affected areas for three months (WHO, 2026). The corridor carries the road to the Rasuwagadhi border crossing, a major trade route between Nepal and China, and a chain of hydropower plants (Liu et al., 2026); 13 hydropower projects with a combined capacity of 759 MW were affected (NDRRMA & NPC, 2026). In 2026 about 115,000 people lived within 1 km of the river along the corridor, and the September 2026 Overture Maps release contained 113,533 building footprints within 2 km of it (Overture Maps Foundation, 2026; WorldPop, 2025).

### 2.2 Data

We assembled every openly accessible building-damage record for the event, together with official reports, terrain, imagery, settlement and population data (Table 1). All sources were retrieved between 9 September and 20 October 2026 and archived with retrieval logs and SHA-256 checksums. Damage records comprised (i) the HOT inventory of 1,053 OpenStreetMap footprints graded as no damage, minor, major or destroyed, with an analysed-area polygon (HOT, 2026); (ii) the latest CEMS grading products for the four areas of interest that were graded (AOI01 Syapru Besi, AOI02 Timure, AOI03 Bidur and AOI05 Phosretar), comprising 4,685 building points graded as possibly damaged, damaged or destroyed, with area-of-interest polygons, not-analysed areas, imagery metadata and per-area statistics (Copernicus EMS, 2026a, 2026b); and (iii) the UNDP RAPIDA building-debris service, which re-published 3,043 footprints attributed to CEMS (2,311), SERTIT (48) and UNOSAT (684) (UNDP, 2026). The UNOSAT flow-extent polygon (37.35 km^2^ within a 363 km^2^ analysed area) was used as an independent observation of the flood footprint (UNOSAT, 2026). Official information came from the NDRRMA situation reports and consolidated update to 3 October 2026 (NDRRMA, 2026), the RDNA (NDRRMA & NPC, 2026) and the propagation timeline of the Centre of Hydrology and Water Resources Research (CHWRR, 2026).

The building stock was taken from the Overture Maps release 2026-09-23.1 (Overture Maps Foundation, 2026), which conflates OpenStreetMap (Haklay & Weber, 2008), Google Open Buildings (Sirko et al., 2021) and Microsoft footprints; we retained 113,533 footprints within 2 km of the channel. Terrain came from the Copernicus GLO-30 digital elevation model (European Space Agency & Airbus, 2022), settlement history from GHS-BUILT-S R2023A (1975–2020, 100 m) (Pesaresi, 2023; Pesaresi et al., 2024), population from WorldPop Global2 R2025A constrained counts for 2015, 2020 and 2026 (Stevens et al., 2015; WorldPop, 2025), land cover from ESA WorldCover 2021 (Zanaga et al., 2022), infrastructure from Overture transportation and base themes, administrative boundaries from geoBoundaries (Runfola et al., 2020) and imagery from Sentinel-2 Level-2A (Drusch et al., 2012; Element 84, 2026).

**Table 1.** Data used in this study.

| Dataset | Provider and version | Date or epoch | Resolution or unit | Use in this study |
| --- | --- | --- | --- | --- |
| HOT building-damage inventory and analysed area | Humanitarian OpenStreetMap Team; AI-assisted (fAIR) labels on OpenStreetMap footprints | Post-event imagery; acquisition times not published | 1,053 footprints; 13.9 km^2^ analysed area | Damage labels (local models, harmonization) |
| CEMS EMSR927 grading | Copernicus EMS Rapid Mapping; AOI01, AOI02 first products; AOI03, AOI05 monitoring products (MONIT01) | Imagery 27 Aug–5 Sep 2026 | Building points; road lines; bridge points; not-analysed areas | Damage labels, graded domain, road and bridge damage |
| UNDP RAPIDA building debris layer | UNDP; records attributed to CEMS (2,311), SERTIT (48), UNOSAT (684) | StoryMap of 27 Aug, updated 2 Sep 2026 | 3,043 footprints with floors, site type, debris | Damage labels, debris model |
| UNDP RAPIDA economic estimate and affected population | UNDP (CLIMADA-based) | Reference date 31 Aug 2026 | Local-level US$ and people | Monetary comparison; affected-people indicator |
| UNOSAT flow extent FL20260826NPL | UNITAR/UNOSAT via UNESCO IHP-WINS | Imagery 26–27 Aug 2026 | 37.35 km^2^ polygon in a 363 km^2^ analysed area | Flow-edge heights, exposure |
| NDRRMA situation reports and consolidated update | Government of Nepal | 26 Aug–3 Oct 2026 | Deaths, missing, warning timeline | Casualties, alert times |
| Rapid Damage and Needs Assessment (RDNA) | NDRRMA and National Planning Commission | 10 Sep 2026 | Affected buildings by local level; sector damage and needs | Comparison, ranking, monetary scope |
| Propagation timeline and gauge records | Centre of Hydrology and Water Resources Research (CHWRR) | 26 Aug 2026 | Gauge-loss and threshold times; stage | Wave timing, stage rises |
| Rapid Hazard Assessment NP3 | HiRISK | 28 Aug 2026 | Source coordinates and process interpretation | Start of the traced flow path |
| Copernicus GLO-30 DEM | ESA/Airbus; tiles N27–N28, E084–E085 | Data acquired 2011–2015 | 30 m | Flow path, height above channel, slope, transects |
| Sentinel-2 Level-2A | ESA Copernicus; Earth Search v1 cloud-optimized GeoTIFFs | 2025-10-11 to 2025-10-26 (14 scenes); 2026-09-21 to 2026-10-18 (19 scenes) | 10–20 m | Change indices, true-colour chips |
| Overture Maps release 2026-09-23.1 | Overture Maps Foundation; buildings, transportation, base (infrastructure, water) | Release 23 Sep 2026 | Footprints, lines, points | Common building stock; infrastructure exposure |
| GHS-BUILT-S R2023A | European Commission JRC | 1975–2020, 5-year epochs | 100 m | Built-up growth by height band |
| WorldPop Global2 R2025A constrained counts | WorldPop, University of Southampton | 2015, 2020, 2026 | 100 m | Population in zones |
| geoBoundaries gbOpen NPL ADM3 | William & Mary geoLab (commit 9469f09) | Current release | Local-level polygons | Assignment to local levels |
| Seismic onset of the failure | NRSC/ISRO; USGS event us7000tbwb | 26 Aug 2026, 08:37:10 NPT | Time | Time zero of the propagation timeline |
| ESA WorldCover 2021 v200 | European Space Agency | 2021 | 10 m | Pre-event land cover in the flow extent |

*Note:* Retrieval dates, URLs and checksums of every source are recorded in the accompanying retrieval logs; access terms are listed in Supplementary Table 1.

### 2.3 Damage analysis

Figure 2 summarizes the workflow, from the harmonization of damage records and terrain processing to the analyses and their outputs.

![Figure 2](figures/figure_s1_workflow.png)

**Figure 2.** Workflow of the study: inputs, harmonization steps, analyses and outputs. All steps are scripted and rebuilt from the archived inputs by a single command.

#### 2.3.1 Harmonizing the damage records

All records were matched to the common building stock. Each UNDP footprint was assigned to the stock polygon with which it shared the largest overlap; each HOT footprint was matched greedily by decreasing overlap, with at most one HOT footprint per stock polygon; and each CEMS point was matched greedily by increasing distance (zero inside a footprint, maximum 10 m) with at most one point per footprint. Records without a match — 521 UNDP footprints, 363 HOT footprints and 631 CEMS points, many of them destroyed buildings deleted from OpenStreetMap after the event — were added to the stock as separate buildings, so that no damage record was lost; the common stock comprised 115,048 buildings. Damage grades were mapped to a common ordinal scale (none; minor or possibly damaged; major or damaged; destroyed), and each building took the most severe grade recorded by any product. Inter-product agreement was measured with Cohen's κ (Cohen, 1960) on the 867 buildings graded by both HOT and CEMS (CEMS AOI01 and AOI02). Because CEMS and UNDP list only damaged buildings, a building was treated as graded-undamaged only if it lay inside a CEMS area of interest and outside its not-analysed areas, or if it carried a HOT label; statistical models were restricted to this graded domain (23,453 buildings within 1 km of the channel). HOT confidence scores and a 5-m translation of all HOT footprints were used to check the sensitivity of the local labels and of their overlap with the flow extent (Supplementary Fig. 6 and Supplementary Note 2).

#### 2.3.2 Flow path and height above the river

The four GLO-30 tiles covering 84.3–85.7° E and 27.6–28.5° N were mosaicked and reprojected by bilinear interpolation to a 30-m grid in WGS 84 / UTM zone 45N. The elevation model was hydrologically conditioned with the Priority-Flood+ε algorithm (Barnes et al., 2014), which guarantees that every cell drains to the grid edge, and D8 flow directions (O'Callaghan & Mark, 1984) and flow accumulation were computed. The flow path was traced downstream from the source coordinates reported by HiRISK (28.2887° N, 85.5282° E) (Liu et al., 2026) to the Trishuli–Kali Gandaki confluence at Devghat, a distance of 206.8 km. The path passed within 0.6 km of every reference settlement and its flow accumulation increased at the confluences of the Budhi Gandaki and Marsyangdi, confirming that it followed the main channel. Channel elevations along the path were made non-increasing downstream by a cumulative minimum, smoothed with an 11-cell running mean and constrained again, which removes artefacts from bridges and vegetation in the surface model.

Height above the channel (relative elevation) was computed for every cell within 6 km of the path as the cell elevation minus the inverse-distance-weighted (power 2) mean of the 16 nearest channel elevations (Garousi‐Nejad, I et al., 2019; Nobre et al., 2011; Rennó et al., 2008). It measures how far a building stands above the pre-event river, not the depth of the flow. For each building we also computed distance to the channel, distance downstream (chainage), the bank side and whether the building lay on the outer bank of a bend (from the signed curvature of the smoothed path over ±300 m), the local hillslope gradient, the channel gradient over a 2-km window and the width of the valley floor below 20 m relative elevation along a transect perpendicular to the path. The same transects, spaced every 90 m, were intersected with the UNOSAT flow extent to obtain the height of its outer edge on each bank.

#### 2.3.3 Statistical and machine-learning models

For the HOT inventory, the probability of destruction was modelled by logistic regression on height above the channel, and 95% confidence bands and the height at 50% probability were obtained from 1,000 bootstrap resamples of 1-km reaches, which preserves spatial dependence (Efron & Tibshirani, 1993; Künsch, 1989). A multivariable logistic model and a proportional-odds ordinal model of the four HOT classes (Seabold & Perktold, 2010) included height (per 10 m), log distance, chainage, valley-floor width, outer-bank position, hillslope gradient, log footprint area and building density, with standard errors clustered by 1-km reach.

For the graded domain, we fitted histogram-based gradient-boosted trees (400 iterations, learning rate 0.05, 31 leaves, minimum 40 samples per leaf, L2 regularization 1) (Friedman, 2001; Pedregosa et al., 2011) to predict destruction from nine terrain and building attributes. Performance was estimated by six-fold cross-validation grouped by 5-km reaches, so that test buildings were spatially separated from training buildings (Meyer & Pebesma, 2022; Ploton et al., 2020; Roberts et al., 2017), and compared with logistic models using all attributes or height alone. Variable importance was the mean decrease in test-fold AUC over ten permutations (Fisher et al., 2019; Hooker et al., 2021; Strobl et al., 2007). Two further tests examined dependence on the labels: a model trained and cross-validated on CEMS labels alone within CEMS areas, and a model trained on all labels outside the HOT reach (21.4–41.5 km) and evaluated against HOT's independent labels (Supplementary Note 3).

#### 2.3.4 Damage-calibrated destructive height

The damage-calibrated destructive height was estimated separately for 12 reaches of 5–7 km within the graded areas, as the height at which a logistic model of destruction on height above the channel reached 50% probability, with 500 block-bootstrap resamples of 0.5-km reaches. Where the bootstrap interval exceeded 60 m, we used the smaller of this estimate and the 90th percentile height of destroyed buildings. Reach estimates were smoothed with a three-reach running median within each contiguous graded segment to suppress single-reach outliers caused by a few up-slope records; an outer envelope used the 90th percentile height of destroyed buildings smoothed in the same way. Downstream of the last graded reach, the envelope was interpolated linearly between the stage rises recorded or reconstructed at Galchhi (8.9 m) (ICIMOD, 2026), Kali Khola (12.3 m maximum against a normal level of about 3.2 m) and Devghat (6.57 m against about 4 m) (CHWRR, 2026). Agreement with the UNOSAT flow-edge height (median of both banks within each reach) was measured by Spearman's rank correlation (Supplementary Note 4).

### 2.4 Population exposure

GHS-BUILT-S and WorldPop grids were interpolated to the 30-m grid by assigning each fine cell the density of its source cell, which preserves totals. Combining multi-temporal settlement and population layers in this way follows GIS and remote-sensing approaches for tracking how flood exposure changes over time (R. Ahmed et al., 2024; Tellman et al., 2021). Built-up surface and population were summed within the UNOSAT flow extent and within bands of height above the channel within 1 km of the path. Two danger zones were then defined from the damage-calibrated heights: a core zone below the reach-wise 50%-destruction height and within 500 m of the channel, and an outer zone below the height that bounded 90% of destroyed buildings. Buildings, surviving buildings and residents in 2026 were counted in each zone. Pre-event land cover inside the flow extent was taken from ESA WorldCover 2021 (10 m) (Zanaga et al., 2022). Roads, bridges and power assets inside the flow extent were taken from Overture; damaged road lengths and bridge counts graded by CEMS are reported separately (Supplementary Table 13) because they are observations rather than exposure.

### 2.5 Other methods

#### 2.5.1 Sentinel-2 corroboration

Medium-resolution Copernicus imagery can detect building damage in many disasters despite its 10-m resolution, although models trained on past events transfer imperfectly to new ones (Dietrich et al., 2026). We therefore used Sentinel-2 not to grade buildings but to test the labels independently. Clear-sky median composites were built at 20 m from all Sentinel-2 Level-2A scenes with less than 70% cloud cover acquired in October 2025 (pre-event, after the July 2025 flood; 14 scenes) and between 21 September and 18 October 2026 (post-event; 19 scenes), keeping only pixels classed as vegetation, bare soil, water or unclassified in the scene classification layer (Drusch et al., 2012; Element 84, 2026). Reflectance was computed with each scene's scale factor; the processing-baseline offset listed in the metadata was applied only where the archive had not already removed it, and reflectance was clipped at 10^−4^ before computing visible brightness, the normalized difference vegetation index, the bare soil index and the normalized difference water index. Where an acquisition had been processed twice, only the later processing was used (Supplementary Note 5). Composites were built per MGRS tile and mosaicked by the larger number of clear observations. Post-minus-pre differences were averaged over a 3 × 3-pixel window around each building, and their ability to separate destroyed from undamaged buildings was measured by the AUC.

#### 2.5.2 Wave timing and warning lead time

Arrival times of the wave front were assembled from the seismic failure time and the CHWRR timeline (Supplementary Table 2) and interpolated linearly along the channel. Gauge-loss times are upper bounds on arrival. Lead time for each destroyed building was the interpolated arrival time minus the alert time under three scenarios: the mass SMS (09:15), the first telephone warnings (08:50, the midpoint of 08:46–08:54) and a counterfactual automatic alert two minutes after the seismic signal (08:39:10) (Supplementary Note 6).

#### 2.5.3 Recovery priorities, debris and economic estimates

Indicators were assigned to local levels using geoBoundaries (Runfola et al., 2020) with spelling harmonized to the RDNA. The composite index combined six indicators: satellite-recorded destroyed buildings, RDNA-affected buildings, government-reported affected people (UNDP, 2026), modelled building debris and buildings and population in the core danger zone. In each of 20,000 Monte Carlo draws, weights were sampled from a flat Dirichlet distribution, indicators were normalized by min–max scaling, percentile ranks or logistic-transformed z-scores, and aggregated arithmetically or geometrically; we report the median rank, its 5–95% interval and the probability of a top-three rank (OECD et al., 2008; Saisana et al., 2005; Tate, 2012).

Building debris was estimated for the harmonized inventory with the UNDP model: floor area (footprint area × number of floors) × a grade coefficient (1.0, 0.5 and 0.05 t m^−2^ for destroyed, damaged and possibly damaged buildings) × a settlement factor (3, 2 and 1 for urban, peri-urban and rural buildings) (UNDP, 2026). Floors and settlement type were taken from UNDP records where available; otherwise floors were set to the mean for the settlement type and buildings with at least 40 neighbours within 100 m were treated as urban, a threshold calibrated on UNDP's classification. Uncertainty was explored with 5,000 draws in which grade coefficients were scaled by a common factor between 0.6 and 1.4 and the urban factor varied between 1 and 3 (Supplementary Fig. 5). Monetary estimates were not recomputed; we compare published estimates and state their scope.

#### 2.5.4 Reproducibility

All analyses were run in Python 3.14 with NumPy, pandas, Shapely, rasterio, statsmodels (Seabold & Perktold, 2010) and scikit-learn (Pedregosa et al., 2011). The scripts, a one-command rebuild, retrieval logs and checksums accompany this document. Random seeds were fixed (20260826). No field survey was conducted, no new satellite classifier was trained and no hydraulic simulation was performed.

## 3. Results

### 3.1 The flood and its 207-km impact corridor

The flood wave decelerated sharply as it travelled down the corridor (Figure 3a,b). Using the failure time recorded seismically (08:37:10 NPT) (Roy et al., 2026), the reported arrival at Rasuwagadhi and the times at which river gauges stopped transmitting or crossed warning levels (CHWRR, 2026), the front averaged 57 m s^−1^ over the first 23 km, 36 m s^−1^ to Syaphrubesi and 19 m s^−1^ to Betrawati, before slowing to 6–9 m s^−1^ along the Trishuli and 4 m s^−1^ above Devghat (Supplementary Table 2). Peak discharge was reconstructed at about 17,000 m^3^ s^−1^ at Galchhi (ICIMOD, 2026) and measured at 5,850 m^3^ s^−1^ at Devghat (CHWRR, 2026). Damaged buildings were concentrated in two reaches: the confined gorge between Rasuwagadhi and Syaphrubesi (21–41 km from the source), and the wider Trishuli valley between Betrawati and Galchhi (64–114 km) (Figure 3c). The number of people reported dead rose steadily for a month after the event, while the number missing peaked in mid-September before falling to 5,285 (Figure 3d).

![Figure 3](figures/figure_1_overview.png)

**Figure 3.** The 26 August 2026 flood and its 207-km impact corridor. (a) Shaded-relief map of the corridor from the failure on the north face of Langtang Lirung to the Trishuli–Kali Gandaki confluence at Devghat, showing the D8 flow path traced from the reported source, the UNOSAT flow extent mapped from imagery of 26–27 August, and buildings recorded as destroyed or damaged by at least one product. Distances are along the traced path. (b) Elevation of the channel along the path. (c) Damaged and destroyed buildings per 2 km of path; shading marks reaches graded by satellite products. (d) Deaths and missing people in Nepal reported by NDRRMA between 26 August and 3 October 2026. Map projection: WGS 84 / UTM zone 45N. Data: Copernicus DEM; UNOSAT; HOT; CEMS EMSR927; UNDP RAPIDA; NDRRMA.

### 3.2 Reconciling the damage record

The products that recorded this damage overlapped only partly (Figure 4a; Table 2). The CEMS photo-interpreted 17,299 buildings in four areas of interest using 0.3–1 m imagery acquired between 27 August and 5 September and graded 4,685 of them as affected (3,571 destroyed) (Copernicus EMS, 2026a). The HOT inventory graded 1,053 buildings in the upper corridor with an artificial-intelligence-assisted workflow (HOT, 2026), and the UNDP RAPIDA service re-published 3,043 damaged footprints attributed to CEMS, SERTIT and UNOSAT (UNDP, 2026). After one-to-one matching of points and footprints to a common stock of 115,048 buildings (Section 2.3.1), the products together recorded **5,781 damaged buildings, of which 4,530 were destroyed**; 1,912 buildings were classed as destroyed by at least two products (Figure 4b). This harmonized total is 2.5 times the 2,359 records available to the first UNDP assessment, because later CEMS monitoring products extended grading to Kispang, Belkotgadhi and Galchhi (Supplementary Table 3).

**Table 2.** Damage evidence reconciled in this study.

| Product | Provider and method | Imagery (2026) | Reach graded (km from source) | Buildings graded | Damaged | Destroyed |
|---|---|---|---|---|---|---|
| HOT inventory | HOT; AI-assisted (fAIR) labels on OpenStreetMap footprints | Post-event very-high-resolution (dates not documented) | 22–40 | 1,053 | 937 | 677 |
| CEMS AOI01 Syapru Besi | Copernicus EMS; photo-interpretation (first product, v1) | WorldView-3 27 Aug | 35–38 | 559 | 433 | 323 |
| CEMS AOI02 Timure | Copernicus EMS; photo-interpretation (first product, v2) | Legion 27 Aug | 23–27 | 441 | 431 | 372 |
| CEMS AOI03 Bidur | Copernicus EMS; photo-interpretation (monitoring product, v1) | PeruSAT-1 27 Aug; Resurs-P 28 Aug | 65–88 | 11,486 | 3,058 | 2,479 |
| CEMS AOI05 Phosretar | Copernicus EMS; photo-interpretation (monitoring product, v2) | Legion 5 Sep; Pleiades Neo 5 Sep | 89–114 | 4,813 | 763 | 397 |
| UNDP RAPIDA service | UNDP; republished CEMS (2,311), SERTIT (48) and UNOSAT (684) records on Google footprints with debris model | As source products | 22–101 | – | 3,043 | 2,574 |
| UNOSAT flow extent | UNOSAT; flow/mudflow extent (no building grading) | PlanetScope 26 Aug; Sentinel-2 27 Aug | 0–106 | – | – | – |
| Official RDNA | NDRRMA/NPC; satellite and drone imagery, fAIR-HOT mapping, Census 2021 typology | Various, to 3 Sep | 15 local levels | – | 7,570 (affected) | – |
| **Harmonized union (this study)** | One-to-one matching to Overture footprints; most severe grade | – | 0–114 | – | **5,781** | **4,530** |

*Note:* Counts refer to buildings within 2 km of the traced channel after matching. Imagery and dates are those reported by each provider. CEMS 'affected' combines possibly damaged, damaged and destroyed.

Where two products graded the same buildings, they agreed on destruction but not on lesser damage. Among 867 buildings graded by both HOT and CEMS, 97% of buildings that CEMS classed as destroyed were also destroyed in HOT, and 65% of HOT-destroyed buildings were destroyed in CEMS (Cohen's κ = 0.49) (Cohen, 1960), whereas the two products disagreed on most minor and major damage (Figure 4c and Supplementary Table 4). Only 34% of the 367 UNOSAT-attributed 'destroyed' records that fell inside CEMS areas were also destroyed in CEMS, indicating that records of unknown provenance should not be merged without checking. Sentinel-2 composites from the same season before and after the event, which no product used for building grading, independently corroborated the destruction labels. The loss of vegetation signal at building locations, consistent with sediment covering roofs, gardens and fields, separated destroyed from undamaged buildings with an area under the receiver-operating-characteristic curve (AUC) of 0.95 across all graded areas and 0.94 against HOT's labels (normalized difference vegetation index, NDVI; visible brightness gave 0.94). In the CEMS grading, the median NDVI change was +0.02 for buildings without damage, −0.03 for possibly damaged, −0.18 for damaged and −0.41 for destroyed buildings (Figure 4e,f, Supplementary Fig. 2 and Supplementary Table 5).

The satellite-graded counts matched the government's RDNA in the graded reaches (median ratio 1.16; Figure 4d), but not elsewhere. In local levels without satellite grading, most of them below Galchhi, the RDNA reported 1,797 affected buildings, including 1,037 in Benighat Rorang (NDRRMA & NPC, 2026). Yet only 33 buildings in Benighat Rorang lie within 10 m of the channel's elevation, and stage rises of about 9 m were recorded or reconstructed in this reach (CHWRR, 2026; ICIMOD, 2026). The RDNA counts there therefore probably include buildings affected by proximity, erosion of slopes and roads, or service loss rather than direct flooding, and they are the clearest target for field verification.

![Figure 4](figures/figure_2_inventories.png)

**Figure 4.** Reconciling the damage record. (a) Reaches graded by each product along the corridor and the local levels reported in the RDNA; ticks show individual UNOSAT-attributed records. (b) Buildings recorded as damaged by each product, by the harmonized union and by the RDNA. (c) Agreement between HOT and CEMS for the 867 buildings graded by both, as row percentages with counts. (d) Satellite-graded damaged buildings against RDNA-affected buildings by local level; local levels without satellite grading are plotted at the axis floor. (e) Sentinel-2 true-colour images from the clearest pre-event (October 2025) and post-event (September–October 2026) scenes at Syaphrubesi (top) and Trishuli Bazar (bottom), with acquisition dates and the same reflectance stretch for all images. (f) Post-minus-pre change in NDVI at building locations by HOT grade and by CEMS/UNDP grade (boxes, interquartile range; whiskers, 10th–90th percentiles; numbers, buildings), with the AUC for separating destroyed from undamaged buildings within each set. Contains modified Copernicus Sentinel data (2025, 2026).

### 3.3 Height above the river governed destruction

Within the HOT inventory, the share of destroyed buildings fell from 95% for buildings less than 20 m above the channel to 7% for buildings more than 80 m above it, while the shares of minor damage and no damage rose (Figure 5c). Height above the pre-event channel — the relative elevation of each building above the traced flow path, similar to height above nearest drainage (Nobre et al., 2011; Rennó et al., 2008) — discriminated destroyed from surviving buildings with an AUC of 0.92; each additional 10 m of height halved the odds of destruction (odds ratio 0.50). Distance from the channel was a weaker discriminator (AUC 0.83). In an ordinal model of the four HOT damage classes with errors clustered by 1-km reach, height (odds ratio 0.85 per 10 m), distance, distance downstream and hillslope gradient were all associated with less severe damage, and buildings on the outer banks of bends had 1.5 times the odds of more severe damage (odds ratio 1.53, 95% confidence interval 1.07–2.17; Supplementary Table 6) — consistent with superelevation and erosion where flows impinge on the outside of bends.

Across the 23,453 buildings in all graded areas, a gradient-boosted classifier (Friedman, 2001; Pedregosa et al., 2011) trained on terrain and building attributes predicted destruction with an AUC of 0.95 under spatial block cross-validation (Ploton et al., 2020; Roberts et al., 2017) (precision–recall AUC 0.76 at a prevalence of 18%; Figure 5e and Supplementary Table 7). Height above the channel was by far the most important predictor: permuting it reduced the AUC by 0.20, against 0.045 for distance from the channel and 0.036 for distance downstream (Figure 5f and Supplementary Fig. 3) (Fisher et al., 2019). The result did not depend on which product supplied the labels: a model using CEMS labels alone achieved an AUC of 0.95, and a model trained outside the HOT reach predicted HOT's independent labels with an AUC of 0.89. Height alone retained an AUC of 0.86, but its effect differed strongly between reaches (Figure 5d), which motivated a reach-specific analysis.

The two zoomed maps in Figure 5 illustrate the contrast. At Timure, in the gorge, buildings were destroyed up to the upper limit of the valley floor, tens of metres above the river. At Trishuli Bazar–Bidur, destroyed buildings were confined to the lower river terraces, below about 20 m, while the town on the higher terrace survived almost intact (Figure 5a,b).

![Figure 5](figures/figure_3_height_controls.png)

**Figure 5.** Height above the river governed destruction. (a, b) Height above the pre-event channel (shading and white contours), the UNOSAT flow-extent edge and building footprints coloured by the most severe grade recorded, at Timure in the gorge (a) and Trishuli Bazar–Bidur in the valley (b). (c) Composition of HOT damage classes by height above the channel; numbers at right give buildings per band (Supplementary Table 6). (d) Probability of destruction against height above the channel for the three graded reach groups, with 95% block-bootstrap bands; dots mark the height at 50% probability. (e) Receiver-operating-characteristic curves for gradient-boosted trees under spatial cross-validation, for height alone, and for the model transferred to HOT labels. (f) Permutation importance (mean loss of AUC ± s.d. across folds).

### 3.4 A destructive height that declined downstream

We estimated, for each graded reach, the height above the channel at which the probability of destruction reached 50% (Section 2.3.4). This damage-calibrated height was 55–60 m in the gorge (all gorge buildings pooled: 62 (95% CI 56–88) m), declined from 33 to 15 m between Betrawati and Bidur (pooled: 21 (95% CI 19–24) m) and was 7–12 m below Bidur (pooled: 9 (95% CI 7–11) m) (Figure 6a and Supplementary Table 8). It closely matched an independent measure — the height of the outer edge of the UNOSAT flow extent, mapped from imagery rather than from buildings — across all 11 reaches (Spearman ρ = 0.97; Figure 6d). Downstream of the last graded reach, stage rises recorded or reconstructed at Galchhi (about 9 m), Kali Khola (about 9 m) and Devghat (about 2.6 m) (CHWRR, 2026; ICIMOD, 2026) were consistent with the lowest damage-calibrated heights.

The downstream decline in destructive height paralleled the deceleration of the wave front from more than 50 m s^−1^ to less than 10 m s^−1^ and the widening of the valley floor from about 100 m in the gorge to more than 250 m below Betrawati (Figure 6b,c and Supplementary Fig. 4). In the gorge, destruction extended well beyond plausible water depths: only 16% of destroyed buildings lay less than 20 m above the channel, compared with 61% in the middle valley and 87% in the lower reach (Figure 6e). This pattern implicates the high momentum of a sediment-laden surge confined in a narrow valley, superelevation in bends and the collapse of undercut terraces, rather than inundation alone (Cook et al., 2018; Jakob et al., 2012; Papathoma-Köhle et al., 2017). It also means that a single setback distance or flood-mark height cannot define safe ground along the whole corridor (Supplementary Table 9).

![Figure 6](figures/figure_4_height_envelope.png)

**Figure 6.** The destructive height declined downstream. (a) Damage-calibrated destructive height (height at 50% probability of destruction, with 95% intervals), 90th-percentile height of destroyed buildings, height of the UNOSAT flow-extent edge (median and interquartile range) and stage rises gauged or reconstructed downstream, with the core and outer envelopes used for the danger zones. (b) Mean celerity of the wave front between timed locations, with times (NPT). (c) Width of the valley floor less than 20 m above the channel and width of the mapped flow extent (running medians). (d) Damage-calibrated height against flow-extent edge height for the 11 graded reaches. (e) Shares of destroyed buildings below 20 m and the number of undamaged buildings below 20 m.

### 3.5 Settlement growth into the destructive zone

Built-up surface on the valley floor had expanded far faster than on higher ground (Figure 7a). Within 1 km of the channel in the graded corridor, built-up area less than 10 m above the channel grew 17-fold between 1975 and 2020, and that 10–20 m above the channel 13-fold, compared with 7.7-fold for land more than 80 m above it (Supplementary Table 10) (Pesaresi, 2023; Pesaresi et al., 2024). Inside the area later mapped as flow extent, built-up surface increased from 3.5 ha to 43.7 ha, consistent with an independent estimate (R. Li, 2026). At Trishuli Bazar–Bidur, much of the riverside building destroyed in 2026 had appeared since 2005 (Figure 7b). The pattern mirrors the faster growth of settlements in flood zones observed worldwide (Rentschler et al., 2023; Tellman et al., 2021) and in Nepal's road and hydropower corridors (McAdoo et al., 2018; Schwanghart et al., 2016). Before the event, the land later covered by the flow included 3.4 km^2^ of cropland, 98% of it in the Trishuli valley, 1.0 km^2^ of built-up land and 12.3 km^2^ of tree cover (Supplementary Table 15) (Zanaga et al., 2022).

Applying the damage-calibrated height to the whole corridor identifies the ground that the 2026 event showed to be most hazardous. The core zone contained 4,868 buildings, of which 1,541 survived, and an estimated 6,100 residents in 2026 (WorldPop, 2025). It captured 73% of all destroyed buildings. The outer zone contained 7,415 buildings (3,377 surviving) and about 9,600 residents and captured 89% of destroyed buildings (Figure 8c). These zones are an evidence base, not a regulatory map, but they indicate the scale of the relocation and reconstruction decisions now facing local and national government (Radio Nepal, 2026).

### 3.6 Warning time was available for most destroyed buildings

The propagation record shows that warning time was short only in the uppermost reach (Figure 7c). The first official warnings were telephoned from Rasuwa between 08:46 and 08:54, requesting evacuation of residents up to 200 m above the riverbank, and the Department of Hydrology and Meteorology sent 679,295 SMS warnings at 09:15 (NDRRMA, 2026). By then the wave had passed Syaphrubesi and was approaching Betrawati. Interpolating arrival times along the channel, 29% of destroyed buildings were reached before the SMS was sent, and only 24% received it at least 30 minutes ahead of the flood (Figure 7d). Had an alert been issued automatically two minutes after the seismic signal, which exceeded magnitude 5 (Roy et al., 2026; Slaughter et al., 2026), no destroyed building would have been reached before the alert, and 73% would have had at least 30 minutes (median 41 min). Even so, the median warning in Gosaikunda would have been only 6 min, compared with 54 min in Bidur (Supplementary Table 11).

Mortality cannot yet be located — 57% of the bodies were recovered beyond the corridor, in Chitwan and Nawalparasi (NDRRMA, 2026), and the reported totals were still being revised in late September (Supplementary Table 12) — but the distribution of the missing is consistent with the warning gradient. Rasuwa district, where the flood arrived within minutes of the failure, recorded 3,514 missing people (2.6 per destroyed building in its local levels), whereas Nuwakot, reached 30–90 minutes after the failure, recorded 1,247 (0.4 per destroyed building). The difference also reflects the many travellers, pilgrims, customs officers and hydropower workers present at the border on the day of the disaster (NDRRMA, 2026).

![Figure 7](figures/figure_5_exposure_warning.png)

**Figure 7.** Exposure growth into the destructive zone and warning time. (a) Built-up surface within 1 km of the channel in the graded corridor, relative to 1975, by band of height above the channel (GHS-BUILT-S R2023A). (b) Epoch in which each 30-m cell first exceeded 10% built-up surface at Trishuli Bazar–Bidur, with the flow extent and destroyed buildings. (c) Arrival time of the wave front after the failure (log scale) along the corridor and the times of the counterfactual seismic-triggered alert, the first telephone warnings and the mass SMS; the lower panel shows destroyed buildings per 3 km. (d) Time between alert and wave arrival for the 4,530 destroyed buildings under the three alert scenarios.

### 3.7 Recovery priorities, debris and losses

The composite index combining satellite-recorded destruction, RDNA-affected buildings, government-reported affected people, modelled building debris and the buildings and population in the core danger zone placed Bidur and Gosaikunda first and second in almost every simulation (probability of a top-three rank 1.00 and 0.99), followed by Kispang (0.77) (Figure 8a,b, Table 3 and Supplementary Fig. 5c) (OECD et al., 2008; Saisana et al., 2005). Benighat Rorang ranked sixth on average but with the widest interval, reflecting the absence of satellite grading and the large RDNA count.

Building debris, modelled with the coefficients used by UNDP for the harmonized inventory, amounted to 1.04 million tonnes (90% range 0.44–1.22 million tonnes under uncertain material coefficients and settlement factors; Figure 8e and Supplementary Fig. 5a,b), roughly 1.9 times the first UNDP estimate (UNDP, 2026). Bidur accounted for 60% of this tonnage, but only 44% if the threefold multiplier applied to urban buildings is removed, so that clearance planning in Bidur depends strongly on an untested assumption. In its four areas of interest, CEMS also graded 73 km of road and 44 of 54 affected bridges as destroyed (Supplementary Table 13). The available monetary estimates differ by more than an order of magnitude because they measure different things (Figure 8d and Supplementary Table 14): modelled direct building damage (US$0.17 billion) (UNDP, 2026), private housing and household assets (US$0.42 billion), all physical damage (US$1.66–1.81 billion) (NDRRMA & NPC, 2026; World Bank & GFDRR, 2026), total effects (US$2.70 billion) and recovery needs (US$4.77 billion) (NDRRMA & NPC, 2026). Energy alone accounted for US$0.89 billion of damage, with 13 hydropower projects (759 MW) affected and about 431 MW of generation, roughly a tenth of national capacity, interrupted (NDRRMA & NPC, 2026).

![Figure 8](figures/figure_6_priorities.png)

**Figure 8.** Recovery priorities. (a) Indicators by local level, shaded by their log-scaled magnitude (lead-time columns are shaded so that shorter warning is darker). (b) Median rank and 5–95% interval of the composite index over 20,000 Monte Carlo draws of weights, normalization and aggregation, with the probability of a top-three rank. (c) Buildings below the damage-calibrated height within 500 m of the channel: destroyed and surviving in the core zone, and additional surviving buildings in the outer zone. (d) Published monetary estimates by scope (log scale). (e) Building debris estimated by UNDP and in this study (5–95% Monte Carlo range).

**Table 3.** Recovery indicators and priorities for the most affected local levels.

| Local level | Destroyed (satellite) | Damaged (satellite) | RDNA affected | Core-zone buildings (surviving) | Core-zone residents | SMS lead time (min) | Building debris (kt) | Rank (5–95%) | Priority actions |
|---|---|---|---|---|---|---|---|---|---|
| Bidur | 2,221 | 2,775 | 3,026 | 2,172 (650) | 2,680 | +18 | 625 | 1 (1–1) | Inspect surviving riverside buildings below the valley envelope; largest debris volume — verify urban debris factor before contracting; flood-front lead time was ~50 min: automate alerts |
| Gosaikunda | 1,040 | 1,366 | 1,043 | 1,174 (233) | 1,030 | −30 | 188 | 2 (2–2) | Relocation assessment for gorge settlements (destruction to ~60 m above channel); restore the Rasuwagadhi corridor; seismic-triggered alerts essential (lead time minutes) |
| Kispang | 409 | 430 | 696 | 568 (171) | 460 | +2 | 60 | 3 (3–6) | Inspect partially damaged buildings on low terraces; debris clearance; reconcile RDNA (696) with satellite count (430) |
| Uttargaya | 269 | 278 | 567 | 463 (221) | 400 | −3 | 44 | 4 (4–9) | Verify RDNA count (567) against satellite record (278); inspect surviving buildings in the core zone |
| Belkotgadhi | 209 | 256 | 212 | 72 (23) | 140 | +47 | 50 | 5 (4–7) | Inspect outer-zone buildings; restore access and water supply |
| Benighat Rorang | 0 | 0 | 1,037 | 19 (19) | 170 | – | – | 6 (3–10) | Field verification of 1,037 RDNA-affected buildings (no satellite grading; few buildings below observed stage) |
| Galchhi | 127 | 353 | 79 | 57 (36) | 190 | +79 | 30 | 6 (4–8) | Inspect damaged riverside structures; confluence reach with highway exposure |
| Gajuri | 64 | 118 | 107 | 11 (7) | 140 | +92 | 14 | 8 (5–11) | Verify damage below Galchhi; protect Prithvi Highway segments |
| Tarakeshwor | 113 | 122 | 43 | 119 (31) | 190 | +57 | 16 | 9 (6–12) | Inspect destroyed/damaged buildings recorded by satellites (RDNA lists 43) |

*Note:* Destroyed and damaged counts are from the harmonized satellite inventory; RDNA counts are affected private buildings (NDRRMA & NPC, 2026). Danger-zone counts are buildings within 500 m of the channel below the core damage-calibrated height. Lead times are medians for destroyed buildings under the actual SMS (09:15). Ranks are medians (5–95% interval) of the Monte Carlo composite index.

## 4. Discussion

### 4.1 Height above the river as a basis for danger zoning

The 2026 cascade shows that a single, easily measured terrain variable — height above the pre-event channel — explains most of the observed building destruction along a 207-km corridor, and that the height reached by destruction declined systematically downstream. Height above the channel integrates the factors that empirical vulnerability models express through flow depth, velocity and impact pressure (Fuchs et al., 2007; Jakob et al., 2012; Kang & Kim, 2016; Luo et al., 2023; Prieto et al., 2018), which are not observable for most buildings after an event of this kind. Because the damage-calibrated height agreed closely with the independently mapped flow margins (ρ = 0.97), with gauged stage rises and with the deceleration of the wave, it captures the physical envelope of the flow rather than artefacts of any one product. The approach needs only a pre-event elevation model, a traced flow path and the damage grading that is now routinely produced within days of a disaster (Voigt et al., 2016).

Three implications follow for recovery in the Bhote Koshi–Trishuli corridor. First, danger zones should be defined by reach-specific heights above the channel rather than by a uniform flood mark or setback distance: a criterion appropriate to the lower Trishuli, where the destructive height was 7–12 m, would leave out most of the gorge, where destruction reached about 60 m above the river. Second, 1,541 buildings that survived within the core zone, and 3,377 within the outer zone, require structural inspection and a decision on whether they can be safely reoccupied; reconstruction in these zones would recreate the exposure that grew fastest before 2026 (Figure 7a). Third, the largest debris and housing burdens lie in Bidur and Gosaikunda, but the uncertain urban debris multiplier and the unexplained RDNA counts below Galchhi should be resolved by field survey before large clearance contracts or compensation are committed. Because buildings recover their function only when the services and networks around them work again (L. Li et al., 2023), these decisions also need to be coordinated with the restoration of roads, bridges, water supply and the damaged health facilities (WHO, 2026).

### 4.2 Early warning

The warning analysis points to an achievable improvement. Telephone warnings and SMS messages were issued 9 and 38 minutes after the failure but were overtaken by a flood moving at more than 50 m s^−1^ in the upper reach (Acharya, 2026; ICIMOD, 2026). Downstream of Betrawati, however, the flood took between 45 minutes and nearly seven hours to arrive. An automated chain that converts a strong seismic signal from a known high-hazard slope into immediate, location-specific alerts — combined with transboundary data sharing, which was absent on 26 August (Liu et al., 2026; C. Xu, 2026) — would have provided at least 30 minutes for most of the buildings that were destroyed. Whether such warning saves lives also depends on how quickly people can reach safe ground; travel-time models of the kind used to assess access to cyclone shelters in coastal Bangladesh (A. Ahmed et al., 2024) could map evacuation times to ground above the damage-calibrated height. The same principle applies to the many Himalayan valleys where hydropower development has drawn settlements and workers onto valley floors below glacial and periglacial sources (Allen et al., 2022; D. Li et al., 2022; Schwanghart et al., 2016).

### 4.3 Limitations

The analysis has limitations. The 30-m Copernicus elevation model (European Space Agency & Airbus, 2022; Guth & Geoffroy, 2021) is a surface model built from data acquired before 2015; vegetation, buildings and later changes in the channel, including deposition by the 2025 outburst (Q. Xu et al., 2026), affect heights by several metres, more in narrow gorges. Height above the channel is not water depth: in the gorge it also captures run-up, erosion and terrace collapse. Damage labels were not validated in the field, and mapped damage classes are not equivalent to reference-validated estimates (Olofsson et al., 2014); the building stock is drawn from open footprints whose completeness varies (Herfort et al., 2023) and some destroyed buildings had been deleted from OpenStreetMap after the event. We therefore restricted inference to graded areas and corroborated labels with independent Sentinel-2 change. Arrival times between gauges were interpolated, and gauge-loss times approximate arrival only to within several minutes. Casualty figures remain provisional and cannot yet be assigned to locations. Finally, the composite ranking reflects the indicators chosen; we report its sensitivity rather than a single order.

## 5. Conclusion

The 26 August 2026 flood killed at least 1,455 people in Nepal and left 5,285 missing as it travelled 207 km from Langtang Lirung to Devghat. By reconciling four rapid-mapping products and the government's damage assessment into a single inventory, and relating it to pre-event terrain, satellite change, the propagation of the flood wave and five decades of settlement growth, this study reached five conclusions.

First, the products together recorded 5,781 damaged buildings, 4,530 of them destroyed. They agreed on destruction but not on lesser damage, and records of unknown provenance, or from areas that no product graded, need checking before they are used for compensation or planning.

Second, height above the pre-event river channel was the dominant control on which buildings were destroyed, far more important than distance from the river or position along the corridor.

Third, the height reached by destruction fell from about 60 m in the gorge to 7–12 m below Bidur, closely following the independently mapped flow margin and the slowing of the flood wave. No single setback distance or flood mark can therefore define safe ground along the whole corridor.

Fourth, building on low ground had grown fastest before the disaster: built-up area less than 10 m above the river increased 17-fold between 1975 and 2020, and 4,868 buildings, 1,541 of which survived, stand within the core danger zone defined by the 2026 event.

Fifth, warning time was available for most destroyed buildings but was not used. An automatic alert triggered by the seismic signal could have given at least 30 minutes of warning to 73% of them, against 24% under the SMS actually sent.

For recovery, these results support reach-specific danger zones based on height above the river, structural inspection of surviving buildings inside those zones, field verification of the RDNA counts below Galchhi and of the debris assumptions for Bidur, and an automated, transboundary warning chain for the upper corridor. Because the approach needs only a pre-event elevation model, a traced flow path and the rapid damage maps that are now produced within days of a disaster, it can be repeated quickly after future cascading floods in the Himalaya.

## Data availability

All input data are publicly accessible from the sources listed in Table 1 and Supplementary Table 1; the scripts in the code repository retrieve them, and their retrieval dates, URLs and SHA-256 checksums are recorded in the repository. Aggregated results, the height-above-channel raster, the traced flow path and the source data of every figure and table are available at [https://github.com/rezw4n/Nepal_Flood](https://github.com/rezw4n/Nepal_Flood). Building-level damage records from HOT, UNDP and UNOSAT are not redistributed because their redistribution terms have not been confirmed; they are available from the original providers. Gauge records of the Department of Hydrology and Meteorology could not be accessed through its public interface without an application key.

## Code availability

The Python code that reproduces every number, table and figure, with a one-command rebuild and pinned dependencies, is available at [https://github.com/rezw4n/Nepal_Flood](https://github.com/rezw4n/Nepal_Flood).

## Supplementary Information

Supplementary Notes 1–6, Supplementary Tables 1–15 and Supplementary Figures 1–6 are provided in the accompanying file Supplementary_Information.docx.

## Acknowledgements

We thank the agencies and volunteers who produced and openly shared the damage, imagery and official data used here.

## Funding

No funding was received for this study.

## References

Acharya, S. (2026). *The Bhote Koshi–Trishuli flash flood of 26 August 2026, Rasuwa, Nepal: warning latency exceeded flood travel time*. EarthArXiv preprint. [https://doi.org/10.31223/X5HN5H](https://doi.org/10.31223/X5HN5H)

Ahmed, A., Ferdous, Z., Kabir, M. H., Rahman, O., Ahmed, R., & Ryhan, M. A. (2024). Assessment of physical accessibility to cyclone shelters in the exposed coastal area of Bangladesh by using geospatial approach. *The Dhaka University Journal of Earth and Environmental Sciences*, *13*(2), 63–75. [https://doi.org/10.3329/dujees.v13i2.79455](https://doi.org/10.3329/dujees.v13i2.79455)

Ahmed, R., Bhardwaj, A., Sam, L., & Van Tricht, L. (2026). Ice-rock avalanches in a warming Himalaya indicate pathways toward effective preparedness. *Communications Earth & Environment*, *7*(1), 217. [https://doi.org/10.1038/s43247-026-03352-y](https://doi.org/10.1038/s43247-026-03352-y)

Ahmed, R., Jarin, N. Z., & Rahman, O. (2024). Spatiotemporal dynamics of flood exposure in Bangladesh: a GIS and remote sensing based approach. In B. Biswas & B. B. Ghute (Eds.), *Flood risk management: Assessment and strategy* (pp. 1–22). Springer Nature Singapore. [https://doi.org/10.1007/978-981-97-2688-2_1](https://doi.org/10.1007/978-981-97-2688-2_1)

Allen, S. K., Sattar, A., King, O., Zhang, G., Bhattacharya, A., Yao, T., & Bolch, T. (2022). Glacial lake outburst flood hazard under current and future conditions: worst-case scenarios in a transboundary Himalayan basin. *Natural Hazards and Earth System Sciences*, *22*(11), 3765–3785. [https://doi.org/10.5194/nhess-22-3765-2022](https://doi.org/10.5194/nhess-22-3765-2022)

Barnes, R., Lehman, C., & Mulla, D. (2014). Priority-flood: an optimal depression-filling and watershed-labeling algorithm for digital elevation models. *Computers & Geosciences*, *62*, 117–127. [https://doi.org/10.1016/j.cageo.2013.04.024](https://doi.org/10.1016/j.cageo.2013.04.024)

Bashkova, E., Rupper, S. B., Shugar, D. H., & Forster, R. R. (2026). *Global database of glacier failures (1900–2025)*. Earth System Science Data Discussions (preprint). [https://doi.org/10.5194/essd-2026-481](https://doi.org/10.5194/essd-2026-481)

Centre of Hydrology and Water Resources Research (CHWRR), Water and Energy Commission Secretariat. (2026). *Assessment Report II: Rasuwa–Bhote Koshi Flood Event, 2026 (2083)*. Government of Nepal, Kathmandu (13 September 2026). [https://giwmscdnone.gov.np/media/pdf_upload/1_Situation_Report_Bhotekoshi%20Flood_2026_CHWRR_hnmns6o.pdf](https://giwmscdnone.gov.np/media/pdf_upload/1_Situation_Report_Bhotekoshi%20Flood_2026_CHWRR_hnmns6o.pdf)

Chen, C.-M., Hollingsworth, J., Clark, M. K., Chamlagain, D., Bista, S., Zekkos, D., Siwakoti, A., & West, A. J. (2025). Erosional cascade during the 2021 Melamchi flood. *Nature Geoscience*, *18*(1), 32–36. [https://doi.org/10.1038/s41561-024-01596-x](https://doi.org/10.1038/s41561-024-01596-x)

Cohen, J. (1960). A coefficient of agreement for nominal scales. *Educational and Psychological Measurement*, *20*(1), 37–46. [https://doi.org/10.1177/001316446002000104](https://doi.org/10.1177/001316446002000104)

Cook, K. L., Andermann, C., Gimbert, F., Adhikari, B. R., & Hovius, N. (2018). Glacial lake outburst floods as drivers of fluvial erosion in the Himalaya. *Science*, *362*(6410), 53–57. [https://doi.org/10.1126/science.aat4981](https://doi.org/10.1126/science.aat4981)

Copernicus Emergency Management Service (Copernicus EMS). (2026a). *EMSR927 Flood in Nepal: rapid-mapping activation record (areas of interest, imagery and grading statistics) and vector products*. Copernicus EMS Rapid Mapping (accessed 20 October 2026). [https://rapidmapping.emergency.copernicus.eu/backend/dashboard-api/public-activations/?code=EMSR927](https://rapidmapping.emergency.copernicus.eu/backend/dashboard-api/public-activations/?code=EMSR927)

Copernicus Emergency Management Service (Copernicus EMS). (2026b). *EMSR927: Flood in Nepal - flood and mass movement damage grading, Syapru Besi and Timure, Rasuwa District (27 August 2026)*. Copernicus EMS Rapid Mapping (dataset; re-published with DOI via UNESCO IHP-WINS). [https://doi.org/10.63253/bkdj361r](https://doi.org/10.63253/bkdj361r)

Dietrich, O., Alfredsson, M., Arens, E., Metzger, N., Peters, T., Scheibenreif, L., Wegner, J. D., & Schindler, K. (2026). The potential of Copernicus satellites for disaster response: Retrieving building damage from Sentinel-1 and Sentinel-2. *ISPRS Annals of the Photogrammetry, Remote Sensing and Spatial Information Sciences*, *XI-2-2026*, 831–838. [https://doi.org/10.5194/isprs-annals-XI-2-2026-831-2026](https://doi.org/10.5194/isprs-annals-XI-2-2026-831-2026)

Drusch, M., Del Bello, U., Carlier, S., Colin, O., Fernandez, V., Gascon, F., Hoersch, B., Isola, C., Laberinti, P., Martimort, P., Meygret, A., Spoto, F., Sy, O., Marchese, F., & Bargellini, P. (2012). Sentinel-2: ESA's Optical High-Resolution Mission for GMES Operational Services. *Remote Sensing of Environment*, *120*, 25–36. [https://doi.org/10.1016/j.rse.2011.11.026](https://doi.org/10.1016/j.rse.2011.11.026)

Efron, B., & Tibshirani, R. J. (1993). *An Introduction to the Bootstrap*. Chapman & Hall/CRC. [https://doi.org/10.1201/9780429246593](https://doi.org/10.1201/9780429246593)

Element 84. (2026). *Earth Search STAC API: Sentinel-2 Level-2A cloud-optimised GeoTIFFs (collection sentinel-2-l2a)*. Amazon Web Services Open Data Registry (accessed 19–20 October 2026). [https://earth-search.aws.element84.com/v1](https://earth-search.aws.element84.com/v1)

European Space Agency, & Airbus. (2022). *Copernicus DEM*. ESA (dataset). [https://doi.org/10.5270/ESA-c5d3d65](https://doi.org/10.5270/ESA-c5d3d65)

Fisher, A., Rudin, C., & Dominici, F. (2019). *All models are wrong, but many are useful: Learning a variable's importance by studying an entire class of prediction models simultaneously*. Journal of Machine Learning Research. [https://jmlr.org/papers/v20/18-760.html](https://jmlr.org/papers/v20/18-760.html)

Friedman, J. H. (2001). Greedy function approximation: A gradient boosting machine. *The Annals of Statistics*, *29*(5), 1189–1232. [https://doi.org/10.1214/aos/1013203451](https://doi.org/10.1214/aos/1013203451)

Fuchs, S., Heiss, K., & Hübl, J. (2007). Towards an empirical vulnerability function for use in debris flow risk assessment. *Natural Hazards and Earth System Sciences*, *7*(5), 495–506. [https://doi.org/10.5194/nhess-7-495-2007](https://doi.org/10.5194/nhess-7-495-2007)

Garousi‐Nejad, I., Tarboton, D. G., Aboutalebi, M., & Torres‐Rua, A. F. (2019). Terrain Analysis Enhancements to the Height Above Nearest Drainage Flood Inundation Mapping Method. *Water Resources Research*, *55*(10), 7983–8009. [https://doi.org/10.1029/2019WR024837](https://doi.org/10.1029/2019WR024837)

Gerl, T., Kreibich, H., Franco, G., Marechal, D., & Schröter, K. (2016). A review of flood loss models as basis for harmonization and benchmarking. *PLoS ONE*, *11*(7), e0159791. [https://doi.org/10.1371/journal.pone.0159791](https://doi.org/10.1371/journal.pone.0159791)

Guth, P. L., & Geoffroy, T. M. (2021). LiDAR point cloud and ICESat‐2 evaluation of 1 second global digital elevation models: Copernicus wins. *Transactions in GIS*, *25*(5), 2245–2261. [https://doi.org/10.1111/tgis.12825](https://doi.org/10.1111/tgis.12825)

Haklay, M., & Weber, P. (2008). OpenStreetMap: User-Generated Street Maps. *IEEE Pervasive Computing*, *7*(4), 12–18. [https://doi.org/10.1109/MPRV.2008.80](https://doi.org/10.1109/MPRV.2008.80)

Herfort, B., Lautenbach, S., Porto de Albuquerque, J., Anderson, J., & Zipf, A. (2023). A spatio-temporal analysis investigating completeness and inequalities of global urban building data in OpenStreetMap. *Nature Communications*, *14*(1), 3985. [https://doi.org/10.1038/s41467-023-39698-6](https://doi.org/10.1038/s41467-023-39698-6)

Hock, R., et al. (2019). *High Mountain Areas*. In: Pörtner, H.-O. et al. (eds) IPCC Special Report on the Ocean and Cryosphere in a Changing Climate (Cambridge University Press). [https://doi.org/10.1017/9781009157964.004](https://doi.org/10.1017/9781009157964.004)

Hooker, G., Mentch, L., & Zhou, S. (2021). Unrestricted permutation forces extrapolation: variable importance requires at least one more model, or there is no free variable importance. *Statistics and Computing*, *31*(6), 82. [https://doi.org/10.1007/s11222-021-10057-z](https://doi.org/10.1007/s11222-021-10057-z)

Humanitarian OpenStreetMap Team (HOT). (2026). *Nepal flood building damage inventory and analysed-area polygon (fAIR-assisted labels on OpenStreetMap footprints)*. HOT raw-data API (retrieved 9 September 2026). [https://production-raw-data-api.s3.amazonaws.com/ISO3/NPL/buildings/hot_flood_npl_buildings_damage_overview.html](https://production-raw-data-api.s3.amazonaws.com/ISO3/NPL/buildings/hot_flood_npl_buildings_damage_overview.html)

ICIMOD. (2026). *Understanding the Gyirong–Rasuwa disaster of 26 August 2026: A preliminary synthesis*. ICIMOD report (Kathmandu), ISBN 978-92-9115-983-3. [https://doi.org/10.53055/ICIMOD.1150](https://doi.org/10.53055/ICIMOD.1150)

Jakob, M., Stein, D., & Ulmi, M. (2012). Vulnerability of buildings to debris flow impact. *Natural Hazards*, *60*(2), 241–261. [https://doi.org/10.1007/s11069-011-0007-2](https://doi.org/10.1007/s11069-011-0007-2)

Kang, H.-S., & Kim, Y.-T. (2016). The physical vulnerability of different types of building structure to debris flow events. *Natural Hazards*, *80*(3), 1475–1493. [https://doi.org/10.1007/s11069-015-2032-z](https://doi.org/10.1007/s11069-015-2032-z)

Khadka, N., Pandey, V. P., Watson, C. S., Zheng, G., Wu, T., Sharma, K., Rawlins, L. D., Allen, S., Gouli, M. R., & Shrestha, D. (2026). The 2024 cascading glacial lake outburst flood in the Thame Valley of Everest region, Nepal: process, impacts and implications. *Natural Hazards and Earth System Sciences*, *26*(8), 4131–4152. [https://doi.org/10.5194/nhess-26-4131-2026](https://doi.org/10.5194/nhess-26-4131-2026)

Kirschbaum, D., Watson, C. S., Rounce, D. R., Shugar, D. H., Kargel, J. S., Haritashya, U. K., Amatya, P., Shean, D., Anderson, E. R., & Jo, M. (2019). The State of Remote Sensing Capabilities of Cascading Hazards Over High Mountain Asia. *Frontiers in Earth Science*, *7*, 197. [https://doi.org/10.3389/feart.2019.00197](https://doi.org/10.3389/feart.2019.00197)

Künsch, H. R. (1989). The Jackknife and the Bootstrap for General Stationary Observations. *The Annals of Statistics*, *17*(3), 1217–1241. [https://doi.org/10.1214/aos/1176347265](https://doi.org/10.1214/aos/1176347265)

Li, D., Lu, X., Walling, D. E., Zhang, T., Steiner, J. F., Wasson, R. J., Harrison, S., Nepal, S., Nie, Y., Immerzeel, W. W., Shugar, D. H., Koppes, M., Lane, S., Zeng, Z., Sun, X., Yegorov, A., & Bolch, T. (2022). High Mountain Asia hydropower systems threatened by climate-driven landscape instability. *Nature Geoscience*, *15*(7), 520–530. [https://doi.org/10.1038/s41561-022-00953-y](https://doi.org/10.1038/s41561-022-00953-y)

Li, L., Chang-Richards, A., Boston, M., Elwood, K., & Molina Hutt, C. (2023). Post-disaster functional recovery of the built environment: A systematic review and directions for future research. *International Journal of Disaster Risk Reduction*, *95*, 103899. [https://doi.org/10.1016/j.ijdrr.2023.103899](https://doi.org/10.1016/j.ijdrr.2023.103899)

Li, R. (2026). *When a high-mountain slope failure cascades downstream: physical footprint and evolving exposure of the 2026 Gyirong mixed rock-ice cascade*. arXiv preprint (v2, 7 Sep 2026). [https://doi.org/10.48550/arXiv.2609.04563](https://doi.org/10.48550/arXiv.2609.04563)

Liu, Q., Khatri, A., Lord, A., Ghouli, M., Thapa, N., Steiner, J., Immerzeel, W. W., & Allen, S. (2026). *Rapid Hazard Assessment Report No. NP3: Lirung massif, Lhende catchment, Upper Trishuli watershed (rock-ice avalanche, flood), 26 August 2026*. HiRISK Rapid Hazard Assessment (last update 28 Aug 2026). [https://hirisk.org/wp-content/uploads/2026/08/RHA_NP3_RasuwaFlood.pdf](https://hirisk.org/wp-content/uploads/2026/08/RHA_NP3_RasuwaFlood.pdf)

Luo, H. Y., Zhang, L. M., Zhang, L. L., He, J., & Yin, K. S. (2023). Vulnerability of buildings to landslides: The state of the art and future needs. *Earth-Science Reviews*, *238*, 104329. [https://doi.org/10.1016/j.earscirev.2023.104329](https://doi.org/10.1016/j.earscirev.2023.104329)

Maharjan, S. B., Steiner, J. F., Shrestha, A. B., Maharjan, A., & Nepal, S. (2021). *The Melamchi flood disaster: Cascading hazard and the need for multihazard risk management*. ICIMOD report (Kathmandu: International Centre for Integrated Mountain Development). [https://doi.org/10.53055/ICIMOD.981](https://doi.org/10.53055/ICIMOD.981)

Mani, P., Allen, S., Evans, S. G., Kargel, J. S., Mergili, M., Petrakov, D., & Stoffel, M. (2023). Geomorphic Process Chains in High‐Mountain Regions—A Review and Classification Approach for Natural Hazards Assessment. *Reviews of Geophysics*, *61*(4), e2022RG000791. [https://doi.org/10.1029/2022RG000791](https://doi.org/10.1029/2022RG000791)

McAdoo, B. G., Quak, M., Gnyawali, K. R., Adhikari, B. R., Devkota, S., Rajbhandari, P. L., & Sudmeier-Rieux, K. (2018). Roads and landslides in Nepal: how development affects environmental risk. *Natural Hazards and Earth System Sciences*, *18*(12), 3203–3210. [https://doi.org/10.5194/nhess-18-3203-2018](https://doi.org/10.5194/nhess-18-3203-2018)

Merz, B., Kreibich, H., Schwarze, R., & Thieken, A. (2010). Review article "Assessment of economic flood damage". *Natural Hazards and Earth System Sciences*, *10*(8), 1697–1724. [https://doi.org/10.5194/nhess-10-1697-2010](https://doi.org/10.5194/nhess-10-1697-2010)

Meyer, H., & Pebesma, E. (2022). Machine learning-based global maps of ecological variables and the challenge of assessing them. *Nature Communications*, *13*(1), 2208. [https://doi.org/10.1038/s41467-022-29838-9](https://doi.org/10.1038/s41467-022-29838-9)

National Disaster Risk Reduction and Management Authority (NDRRMA). (2026). *Bhotekoshi–Trishuli Flood: Search, Rescue and Relief Update (26 August–3 October 2026)*. NDRRMA, Government of Nepal, Kathmandu. [https://ndrrma.gov.np/mediafiles/publications/Bhotekoshi-Trishuli_Flood_Update_From_August_26_2026_to_October_3_2026.pdf](https://ndrrma.gov.np/mediafiles/publications/Bhotekoshi-Trishuli_Flood_Update_From_August_26_2026_to_October_3_2026.pdf)

National Disaster Risk Reduction and Management Authority (NDRRMA), & National Planning Commission (NPC), Government of Nepal. (2026). *Rapid Damage and Needs Assessment (RDNA): Rasuwa–Bhotekoshi Flood 2026*. NDRRMA, Kathmandu. [https://ndrrma.gov.np/mediafiles/rasuwa/Rapid_Damage_and_Needs_Assessment_RDNA_Rasuwa-Bhotekoshi_Flood_2026.pdf](https://ndrrma.gov.np/mediafiles/rasuwa/Rapid_Damage_and_Needs_Assessment_RDNA_Rasuwa-Bhotekoshi_Flood_2026.pdf)

Nobre, A. D., Cuartas, L. A., Hodnett, M., Rennó, C. D., Rodrigues, G., Silveira, A., Waterloo, M., & Saleska, S. (2011). Height Above the Nearest Drainage – a hydrologically relevant new terrain model. *Journal of Hydrology*, *404*(1-2), 13–29. [https://doi.org/10.1016/j.jhydrol.2011.03.051](https://doi.org/10.1016/j.jhydrol.2011.03.051)

O'Callaghan, J. F., & Mark, D. M. (1984). The extraction of drainage networks from digital elevation data. *Computer Vision, Graphics, and Image Processing*, *28*(3), 323–344. [https://doi.org/10.1016/S0734-189X(84)80011-0](https://doi.org/10.1016/S0734-189X%2884%2980011-0)

OECD, European Union, & Joint Research Centre - European Commission. (2008). *Handbook on Constructing Composite Indicators: Methodology and User Guide*. OECD Publishing (Paris). [https://doi.org/10.1787/9789264043466-en](https://doi.org/10.1787/9789264043466-en)

Olofsson, P., Foody, G. M., Herold, M., Stehman, S. V., Woodcock, C. E., & Wulder, M. A. (2014). Good practices for estimating area and assessing accuracy of land change. *Remote Sensing of Environment*, *148*, 42–57. [https://doi.org/10.1016/j.rse.2014.02.015](https://doi.org/10.1016/j.rse.2014.02.015)

Overture Maps Foundation. (2026). *Overture Maps buildings theme (open map data release)*. Overture Maps Foundation (dataset). [https://overturemaps.org/](https://overturemaps.org/)

Papathoma-Köhle, M., Gems, B., Sturm, M., & Fuchs, S. (2017). Matrices, curves and indicators: A review of approaches to assess physical vulnerability to debris flows. *Earth-Science Reviews*, *171*, 272–288. [https://doi.org/10.1016/j.earscirev.2017.06.007](https://doi.org/10.1016/j.earscirev.2017.06.007)

Pedregosa, F., et al. (2011). Scikit-learn: machine learning in Python. *Journal of Machine Learning Research*, *12*, 2825–2830. [https://jmlr.org/papers/v12/pedregosa11a.html](https://jmlr.org/papers/v12/pedregosa11a.html)

Pesaresi, M. (2023). *GHS-BUILT-S R2023A - GHS built-up surface grid, derived from Sentinel2 composite and Landsat, multitemporal (1975-2030)*. European Commission, Joint Research Centre (dataset). [https://doi.org/10.2905/9F06F36F-4B11-47EC-ABB0-4F8B7B1D72EA](https://doi.org/10.2905/9F06F36F-4B11-47EC-ABB0-4F8B7B1D72EA)

Pesaresi, M., Schiavina, M., Politis, P., Freire, S., Krasnodębska, K., Uhl, J. H., Carioli, A., Corbane, C., Dijkstra, L., Florio, P., Friedrich, H. K., Gao, J., Leyk, S., Lu, L., Maffenini, L., Mari-Rivero, I., Melchiorri, M., Syrris, V., Van Den Hoek, J., & Kemper, T. (2024). Advances on the Global Human Settlement Layer by joint assessment of Earth Observation and population survey data. *International Journal of Digital Earth*, *17*(1), 2390454. [https://doi.org/10.1080/17538947.2024.2390454](https://doi.org/10.1080/17538947.2024.2390454)

Ploton, P., Mortier, F., Réjou-Méchain, M., Barbier, N., Picard, N., Rossi, V., Dormann, C., Cornu, G., Viennois, G., Bayol, N., Lyapustin, A., Gourlet-Fleury, S., & Pélissier, R. (2020). Spatial validation reveals poor predictive performance of large-scale ecological mapping models. *Nature Communications*, *11*(1), 4540. [https://doi.org/10.1038/s41467-020-18321-y](https://doi.org/10.1038/s41467-020-18321-y)

Prieto, J. A., Journeay, M., Acevedo, A. B., Arbelaez, J. D., & Ulmi, M. (2018). Development of structural debris flow fragility curves (debris flow buildings resistance) using momentum flux rate as a hazard parameter. *Engineering Geology*, *239*, 144–157. [https://doi.org/10.1016/j.enggeo.2018.03.014](https://doi.org/10.1016/j.enggeo.2018.03.014)

Radio Nepal. (2026). *Government to relocate and rebuild Bhotekoshi flood-affected settlements in safer areas*. Radio Nepal Online (21 September 2026). [https://radionepalonline.com/en/2026/09/21/436388.html](https://radionepalonline.com/en/2026/09/21/436388.html)

Rennó, C. D., Nobre, A. D., Cuartas, L. A., Soares, J. V., Hodnett, M. G., Tomasella, J., & Waterloo, M. J. (2008). HAND, a new terrain descriptor using SRTM-DEM: Mapping terra-firme rainforest environments in Amazonia. *Remote Sensing of Environment*, *112*(9), 3469–3481. [https://doi.org/10.1016/j.rse.2008.03.018](https://doi.org/10.1016/j.rse.2008.03.018)

Rentschler, J., Avner, P., Marconcini, M., Su, R., Strano, E., Vousdoukas, M., & Hallegatte, S. (2023). Global evidence of rapid urban growth in flood zones since 1985. *Nature*, *622*(7981), 87–92. [https://doi.org/10.1038/s41586-023-06468-9](https://doi.org/10.1038/s41586-023-06468-9)

Roberts, D. R., Bahn, V., Ciuti, S., Boyce, M. S., Elith, J., Guillera‐Arroita, G., Hauenstein, S., Lahoz‐Monfort, J. J., Schröder, B., Thuiller, W., Warton, D. I., Wintle, B. A., Hartig, F., & Dormann, C. F. (2017). Cross‐validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. *Ecography*, *40*(8), 913–929. [https://doi.org/10.1111/ecog.02881](https://doi.org/10.1111/ecog.02881)

Romali, N. S., Sulong, S., & Kawasaki, A. (2025). A systematic review of flood damage assessment: insight for the data-scarce regions. *Water Resources Management*, *39*(10), 4707–4734. [https://doi.org/10.1007/s11269-025-04265-9](https://doi.org/10.1007/s11269-025-04265-9)

Roy, P., Majumdar, R., Chauhan, P., Jalan, P., Pradhan, G., Srivastava, D., Martha, T. R., Reddy, P. S., Sharma, S. V. S. P., Suresh Babu, A. V., Das, I. C., & Durga Rao, K. H. V. (2026). 26 August 2026 rock–ice avalanche in Nepal: rapid assessment of the cascading disaster using satellite data. *Journal of the Indian Society of Remote Sensing*. [https://doi.org/10.1007/s12524-026-02611-x](https://doi.org/10.1007/s12524-026-02611-x)

Runfola, D., Anderson, A., Baier, H., Crittenden, M., Dowker, E., Fuhrig, S., Goodman, S., Grimsley, G., Layko, R., Melville, G., Mulder, M., Oberman, R., Panganiban, J., Peck, A., Seitz, L., Shea, S., Slevin, H., Youngerman, R., & Hobbs, L. (2020). geoBoundaries: a global database of political administrative boundaries. *PLOS ONE*, *15*(4), e0231866. [https://doi.org/10.1371/journal.pone.0231866](https://doi.org/10.1371/journal.pone.0231866)

Saisana, M., Saltelli, A., & Tarantola, S. (2005). Uncertainty and Sensitivity Analysis Techniques as Tools for the Quality Assessment of Composite Indicators. *Journal of the Royal Statistical Society Series A: Statistics in Society*, *168*(2), 307–323. [https://doi.org/10.1111/j.1467-985X.2005.00350.x](https://doi.org/10.1111/j.1467-985X.2005.00350.x)

Sattar, A., Cook, K. L., Rai, S. K., Berthier, E., Allen, S., Rinzin, S., de Vries, M. V. W., Haeberli, W., Kushwaha, P., Shugar, D. H., Emmer, A., Haritashya, U. K., Frey, H., Rao, P., Gurudin, K. S. K., Rai, P., Rajak, R., Hossain, F., Huggel, C., . . . Bhat, S. Y. (2025). The Sikkim flood of October 2023: Drivers, causes, and impacts of a multihazard cascade. *Science*, *387*(6740), eads2659. [https://doi.org/10.1126/science.ads2659](https://doi.org/10.1126/science.ads2659)

Schwanghart, W., Worni, R., Huggel, C., Stoffel, M., & Korup, O. (2016). Uncertainty in the Himalayan energy–water nexus: estimating regional exposure to glacial lake outburst floods. *Environmental Research Letters*, *11*(7), 074005. [https://doi.org/10.1088/1748-9326/11/7/074005](https://doi.org/10.1088/1748-9326/11/7/074005)

Seabold, S., & Perktold, J. (2010). *Statsmodels: econometric and statistical modeling with Python*. Proceedings of the 9th Python in Science Conference. [https://doi.org/10.25080/Majora-92bf1922-011](https://doi.org/10.25080/Majora-92bf1922-011)

Shugar, D. H., Jacquemart, M., Shean, D., Bhushan, S., Upadhyay, K., Sattar, A., Schwanghart, W., McBride, S., de Vries, M. V. W., Mergili, M., Emmer, A., Deschamps-Berger, C., McDonnell, M., Bhambri, R., Allen, S., Berthier, E., Carrivick, J. L., Clague, J. J., Dokukin, M., . . . Westoby, M. J. (2021). A massive rock and ice avalanche caused the 2021 disaster at Chamoli, Indian Himalaya. *Science*, *373*(6552), 300–306. [https://doi.org/10.1126/science.abh4455](https://doi.org/10.1126/science.abh4455)

Sirko, W., et al. (2021). *Continental-Scale Building Detection from High Resolution Satellite Imagery*. arXiv preprint. [https://doi.org/10.48550/arXiv.2107.12283](https://doi.org/10.48550/arXiv.2107.12283)

Slaughter, S., et al. (2026). *2026 Nepal Debris Avalanche and Flash Flood*. U.S. Geological Survey, Landslide Hazards Program (web page, 27-28 Aug 2026). [https://www.usgs.gov/programs/landslide-hazards/science/2026-nepal-debris-avalanche-and-flash-flood](https://www.usgs.gov/programs/landslide-hazards/science/2026-nepal-debris-avalanche-and-flash-flood)

Stevens, F. R., Gaughan, A. E., Linard, C., & Tatem, A. J. (2015). Disaggregating Census Data for Population Mapping Using Random Forests with Remotely-Sensed and Ancillary Data. *PLOS ONE*, *10*(2), e0107042. [https://doi.org/10.1371/journal.pone.0107042](https://doi.org/10.1371/journal.pone.0107042)

Strobl, C., Boulesteix, A.-L., Zeileis, A., & Hothorn, T. (2007). Bias in random forest variable importance measures: Illustrations, sources and a solution. *BMC Bioinformatics*, *8*(1), 25. [https://doi.org/10.1186/1471-2105-8-25](https://doi.org/10.1186/1471-2105-8-25)

Tate, E. (2012). Social vulnerability indices: a comparative assessment using uncertainty and sensitivity analysis. *Natural Hazards*, *63*(2), 325–347. [https://doi.org/10.1007/s11069-012-0152-2](https://doi.org/10.1007/s11069-012-0152-2)

Taylor, C., Robinson, T. R., Dunning, S., Carr, J. R., & Westoby, M. (2023). Glacial lake outburst floods threaten millions globally. *Nature Communications*, *14*(1), 487. [https://doi.org/10.1038/s41467-023-36033-x](https://doi.org/10.1038/s41467-023-36033-x)

Tellman, B., Sullivan, J. A., Kuhn, C., Kettner, A. J., Doyle, C. S., Brakenridge, G. R., Erickson, T. A., & Slayback, D. A. (2021). Satellite imaging reveals increased proportion of population exposed to floods. *Nature*, *596*(7870), 80–86. [https://doi.org/10.1038/s41586-021-03695-w](https://doi.org/10.1038/s41586-021-03695-w)

United Nations Development Programme (UNDP). (2026). *RAPIDA assessment of the floods in Nepal (StoryMap and feature services for building debris, economic estimate, exposure and affected population)*. UNDP GeoSMART (retrieved 9 September 2026). [https://geosmart.undp.org/arcgis/apps/storymaps/stories/7450cd01c584424f8a10ccfc166b167a](https://geosmart.undp.org/arcgis/apps/storymaps/stories/7450cd01c584424f8a10ccfc166b167a)

UNOSAT (UNITAR). (2026). *Satellite-detected mudflow and rockflow extent in Rasuwa and Nuwakot Districts, Bagmati Province, Nepal (26-27 August 2026)*. UNOSAT products 4257/4258 (dataset; re-published with DOI via UNESCO IHP-WINS). [https://doi.org/10.63253/1y26ihdq](https://doi.org/10.63253/1y26ihdq)

Voigt, S., Giulio-Tonolo, F., Lyons, J., Kučera, J., Jones, B., Schneiderhan, T., Platzeck, G., Kaku, K., Hazarika, M. K., Czaran, L., Li, S., Pedersen, W., James, G. K., Proy, C., Muthike, D. M., Bequignon, J., & Guha-Sapir, D. (2016). Global trends in satellite-based emergency mapping. *Science*, *353*(6296), 247–252. [https://doi.org/10.1126/science.aad8728](https://doi.org/10.1126/science.aad8728)

World Bank, & Global Facility for Disaster Reduction and Recovery (GFDRR). (2026). *Global Rapid Post-Disaster Damage Estimation (GRADE) Report: Rasuwa Flash Flood, Nepal*. World Bank Report No. 215321 (Washington, DC). [http://documents.worldbank.org/curated/en/099217209292624461](http://documents.worldbank.org/curated/en/099217209292624461)

World Health Organization (WHO). (2026). *Nepal: Flash floods and health response*. World Health Organization. [https://www.who.int/nepal/emergencies/2026-rasuwa-flash-floods](https://www.who.int/nepal/emergencies/2026-rasuwa-flash-floods)

WorldPop. (2025). *Global2 constrained population counts, 2015–2030, 100 m (release R2025A): Nepal*. WorldPop, University of Southampton (dataset). [https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/](https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/)

Xu, C. (2026). Warnings must cross borders before disasters do. *npj Natural Hazards (Editorial)*, *3*(1), 73. [https://doi.org/10.1038/s44304-026-00271-y](https://doi.org/10.1038/s44304-026-00271-y)

Xu, Q., Kang, S., Du, W., Wu, W., Hu, Z., He, X., Cao, B., & Xie, B. (2026). *Brief communication: Repeated supraglacial lake drainage from the Purepu Glacier system, central Himalaya*. EGUsphere preprint (Brief communication; in discussion). [https://doi.org/10.5194/egusphere-2026-4065](https://doi.org/10.5194/egusphere-2026-4065)

Zanaga, D., et al. (2022). *ESA WorldCover 10 m 2021 v200*. Zenodo (dataset). [https://doi.org/10.5281/zenodo.7254221](https://doi.org/10.5281/zenodo.7254221)

Zhang, T.-G., Wang, W.-C., Khadka, N., Kougkoulos, I., Cook, S. J., Watson, C. S., Gao, Y., Li, S.-H., Yang, X., Wang, Z.-Y., An, B.-S., & Yao, T.-D. (2026). Transboundary outburst floods from giant supraglacial lakes over the Himalayan China–Nepal border. *Advances in Climate Change Research*, *18*(1), 267–282. [https://doi.org/10.1016/j.accre.2026.06.022](https://doi.org/10.1016/j.accre.2026.06.022)

Zheng, G., Allen, S. K., Bao, A., Ballesteros-Cánovas, J. A., Huss, M., Zhang, G., Li, J., Yuan, Y., Jiang, L., Yu, T., Chen, W., & Stoffel, M. (2021). Increasing risk of glacial lake outburst floods from future Third Pole deglaciation. *Nature Climate Change*, *11*(5), 411–417. [https://doi.org/10.1038/s41558-021-01028-3](https://doi.org/10.1038/s41558-021-01028-3)
