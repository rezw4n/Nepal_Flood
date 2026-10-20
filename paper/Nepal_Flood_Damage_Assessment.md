# What height is safe? An analysis of building destruction along the 207-km path of Nepal's 2026 flood

**Rezwan Ahmed^1^, Nusrat Zahan Jarin^2^, Obaidur Rahman^3^**

^1^Department of Geography and Environment, University of Dhaka, Dhaka, Bangladesh. ^2^Department of Geography, University of California, Santa Barbara, CA, USA. ^3^Department of Geography, Oklahoma State University, Stillwater, OK, USA.

ORCID iD, Rezwan Ahmed: [https://orcid.org/0009-0002-8003-099X](https://orcid.org/0009-0002-8003-099X)

ORCID iD, Nusrat Zahan Jarin: [https://orcid.org/0000-0003-2657-8559](https://orcid.org/0000-0003-2657-8559)

Correspondence to be confirmed by the authors.

## Abstract

On 26 August 2026, a rock–ice avalanche from Langtang Lirung, Nepal, generated a flood that travelled 207 km down the Bhote Koshi–Trishuli valley, leaving 1,455 dead and 5,285 missing. Reconciling five satellite and official damage inventories, we find 5,781 damaged buildings, 4,530 of them destroyed. Height above the pre-event channel dominated a spatially cross-validated model of destruction (AUC 0.95). The height at which destruction became more likely than not fell from about 60 m in the gorge to about 7 m 110 km downstream, tracking independently mapped flow margins (Spearman ρ = 0.97). Built-up area less than 10 m above the channel had grown 17-fold since 1975. An automatic seismic alert could have given at least 30 minutes of warning for 73% of destroyed buildings, against 24% under the SMS actually issued. Damage-calibrated heights offer an objective basis for danger zoning and warning in Himalayan valleys.

## Introduction

Cascading hazards that begin with a slope or glacier failure high in a mountain range and end as a flood far downstream are among the deadliest processes in High Mountain Asia ^1,2^. Recent examples include the 2021 Chamoli rock–ice avalanche in India ^3^, the 2021 Melamchi flood ^4,5^ and 2024 Thame outburst ^6^ in Nepal, and the 2023 South Lhonak cascade in Sikkim ^7^. Each overwhelmed settlements and hydropower assets that had been built in narrow valley floors, many tens of kilometres from the source. Glacier and permafrost change is altering the likelihood of such failures ^8–10^, while the population and infrastructure exposed to glacial floods and riverine hazards continue to grow ^11–15^.

At 08:37 Nepal Time (NPT) on 26 August 2026, bedrock and part of a hanging glacier failed on the north face of Langtang Lirung at about 5,200 m above sea level ^16–18^. Estimates of the failed volume range from 99 ± 10 × 10^6^ m^3^ (ref. 18) to about 132 × 10^6^ m^3^ (ref. 17). The mass struck the Lhende glacier, briefly dammed the Lhende Khola and released a debris-laden flood that reached the Nepal–China border at Rasuwagadhi within about seven minutes and the confluence with the Kali Gandaki at Devghat, 207 km from the source, in the afternoon ^19,20^. By 3 October, Nepal's National Disaster Risk Reduction and Management Authority (NDRRMA) had recorded 1,455 deaths and 5,285 people missing (Fig. 1d); Chinese authorities reported 43 deaths and 519 missing at Gyirong (Kyirong) port ^17,20^. The government's Rapid Damage and Needs Assessment (RDNA) estimated US$1.81 billion of physical damage, US$2.70 billion of total effects (6.7% of gross domestic product) and US$4.77 billion of recovery needs ^21^. The event followed a supraglacial-lake outburst in July 2025 that had already damaged the same border crossing and hydropower plants ^22,23^.

Within days, the disaster had been mapped by several independent systems: the Copernicus Emergency Management Service (CEMS) ^24,25^, the United Nations Satellite Centre (UNOSAT) ^26^, the Humanitarian OpenStreetMap Team (HOT) ^27^, the United Nations Development Programme (UNDP) ^28^ and the World Bank ^29^, alongside the government's RDNA. Such rapid products are indispensable when valleys are cut off ^30^, but they differ in imagery, coverage, damage scales and purpose, and their reported totals for this event ranged from fewer than 1,000 to more than 12,000 buildings depending on what was counted ^16,21,31^. They are rarely reconciled, and even more rarely used to ask why particular buildings were destroyed while neighbours survived. That question now matters for recovery. The government has announced that settlements in high-risk parts of the corridor will be relocated ^32^, but no event-calibrated, physically grounded basis yet exists for deciding where reconstruction is unsafe, and the warning of 26 August reached many riverside communities only after the flood had passed ^17,33,34^.

Here we reconcile the building-damage records of four mapping products and the RDNA into a single corridor-scale inventory, and relate it to the pre-event terrain, to Sentinel-2 surface change, to the documented propagation of the flood wave and to five decades of settlement growth (Supplementary Fig. 1 and Supplementary Table 1). We show that height above the pre-event river channel explains most of where buildings were destroyed; that the height reached by destruction declined systematically downstream, in step with independently mapped flow margins and the decay of the wave front; that settlement had expanded fastest into exactly this destructive zone; and that warning time was available for most destroyed buildings but was not used. We translate these results into municipality-level priorities for inspection, debris clearance, danger-zone mapping and early warning.

## Results

### A 207-km cascade recorded by inconsistent damage products

The flood wave decelerated sharply as it travelled down the corridor (Fig. 1a,b). Using the failure time recorded seismically (08:37:10 NPT) ^18^, the reported arrival at Rasuwagadhi and the times at which river gauges stopped transmitting or crossed warning levels ^19^, the front averaged 57 m s^−1^ over the first 23 km, 36 m s^−1^ to Syaphrubesi and 19 m s^−1^ to Betrawati, before slowing to 6–9 m s^−1^ along the Trishuli and 4 m s^−1^ above Devghat (Supplementary Table 2). Peak discharge was reconstructed at about 17,000 m^3^ s^−1^ at Galchhi ^17^ and measured at 5,850 m^3^ s^−1^ at Devghat ^19^. Damaged buildings were concentrated in two reaches: the confined gorge between Rasuwagadhi and Syaphrubesi (21–41 km from the source), and the wider Trishuli valley between Betrawati and Galchhi (64–114 km) (Fig. 1c).

The products that recorded this damage overlapped only partly (Fig. 2a). The CEMS photo-interpreted 17,299 buildings in four areas of interest using 0.3–1 m imagery acquired between 27 August and 5 September and graded 4,685 of them as affected (3,571 destroyed) ^25^. The HOT inventory graded 1,053 buildings in the upper corridor with an artificial-intelligence-assisted workflow ^27^, and the UNDP RAPIDA service re-published 3,043 damaged footprints attributed to CEMS, SERTIT and UNOSAT ^28^. After one-to-one matching of points and footprints to a common stock of 115,048 buildings (Methods), the products together recorded **5,781 damaged buildings, of which 4,530 were destroyed**; 1,912 buildings were classed as destroyed by at least two products (Fig. 2b). This harmonized total is 2.5 times the 2,359 records available to the first UNDP assessment, because later CEMS monitoring products extended grading to Kispang, Belkotgadhi and Galchhi (Supplementary Table 3).

Where two products graded the same buildings, they agreed on destruction but not on lesser damage. Among 867 buildings graded by both HOT and CEMS, 97% of buildings that CEMS classed as destroyed were also destroyed in HOT, and 65% of HOT-destroyed buildings were destroyed in CEMS (Cohen's κ = 0.49) ^35^, whereas the two products disagreed on most minor and major damage (Fig. 2c and Supplementary Table 4). Only 34% of the 367 UNOSAT-attributed 'destroyed' records that fell inside CEMS areas were also destroyed in CEMS, indicating that records of unknown provenance should not be merged without checking. Sentinel-2 composites from the same season before and after the event, which no product used for building grading, independently corroborated the destruction labels. The loss of vegetation signal at building locations, consistent with sediment covering roofs, gardens and fields, separated destroyed from undamaged buildings with an area under the receiver-operating-characteristic curve (AUC) of 0.95 across all graded areas and 0.94 against HOT's labels (normalized difference vegetation index, NDVI; visible brightness gave 0.94). In the CEMS grading, the median NDVI change was +0.02 for buildings without damage, −0.03 for possibly damaged, −0.18 for damaged and −0.41 for destroyed buildings (Fig. 2e,f, Supplementary Fig. 2 and Supplementary Table 5).

The satellite-graded counts matched the government's RDNA in the graded reaches (median ratio 1.16; Fig. 2d), but not elsewhere. In local levels without satellite grading, most of them below Galchhi, the RDNA reported 1,797 affected buildings, including 1,037 in Benighat Rorang ^21^. Yet only 33 buildings in Benighat Rorang lie within 10 m of the channel's elevation, and stage rises of about 9 m were recorded or reconstructed in this reach ^17,19^. The RDNA counts there therefore probably include buildings affected by proximity, erosion of slopes and roads, or service loss rather than direct flooding, and they are the clearest target for field verification.

### Height above the channel governed destruction

Within the HOT inventory, the share of destroyed buildings fell from 95% for buildings less than 20 m above the channel to 7% for buildings more than 80 m above it, while the shares of minor damage and no damage rose (Fig. 3c). Height above the pre-event channel — the relative elevation of each building above the traced flow path, similar to height above nearest drainage ^36,37^ — discriminated destroyed from surviving buildings with an AUC of 0.92; each additional 10 m of height halved the odds of destruction (odds ratio 0.50). Distance from the channel was a weaker discriminator (AUC 0.83). In an ordinal model of the four HOT damage classes with errors clustered by 1-km reach, height (odds ratio 0.85 per 10 m), distance, distance downstream and hillslope gradient were all associated with less severe damage, and buildings on the outer banks of bends had 1.5 times the odds of more severe damage (odds ratio 1.53, 95% confidence interval 1.07–2.17; Supplementary Table 6) — consistent with superelevation and erosion where flows impinge on the outside of bends.

Across the 23,453 buildings in all graded areas, a gradient-boosted classifier ^38,39^ trained on terrain and building attributes predicted destruction with an AUC of 0.95 under spatial block cross-validation ^40,41^ (precision–recall AUC 0.76 at a prevalence of 18%; Fig. 3e and Supplementary Table 7). Height above the channel was by far the most important predictor: permuting it reduced the AUC by 0.20, against 0.045 for distance from the channel and 0.036 for distance downstream (Fig. 3f and Supplementary Fig. 3) ^42^. The result did not depend on which product supplied the labels: a model using CEMS labels alone achieved an AUC of 0.95, and a model trained outside the HOT reach predicted HOT's independent labels with an AUC of 0.89. Height alone retained an AUC of 0.86, but its effect differed strongly between reaches (Fig. 3d), which motivated a reach-specific analysis.

The two zoomed maps in Fig. 3 illustrate the contrast. At Timure, in the gorge, buildings were destroyed up to the upper limit of the valley floor, tens of metres above the river. At Trishuli Bazar–Bidur, destroyed buildings were confined to the lower river terraces, below about 20 m, while the town on the higher terrace survived almost intact (Fig. 3a,b).

### A damage-calibrated destructive height attenuated downstream

We estimated, for each graded reach, the height above the channel at which the probability of destruction reached 50% (Methods). This damage-calibrated height was 55–60 m in the gorge (all gorge buildings pooled: 62 (95% CI 56–88) m), declined from 33 to 15 m between Betrawati and Bidur (pooled: 21 (95% CI 19–24) m) and was 7–12 m below Bidur (pooled: 9 (95% CI 7–11) m) (Fig. 4a and Supplementary Table 8). It closely matched an independent measure — the height of the outer edge of the UNOSAT flow extent, mapped from imagery rather than from buildings — across all 11 reaches (Spearman ρ = 0.97; Fig. 4d). Downstream of the last graded reach, stage rises recorded or reconstructed at Galchhi (about 9 m), Kali Khola (about 9 m) and Devghat (about 2.6 m) ^17,19^ were consistent with the lowest damage-calibrated heights.

The downstream decline in destructive height paralleled the deceleration of the wave front from more than 50 m s^−1^ to less than 10 m s^−1^ and the widening of the valley floor from about 100 m in the gorge to more than 250 m below Betrawati (Fig. 4b,c and Supplementary Fig. 4). In the gorge, destruction extended well beyond plausible water depths: only 16% of destroyed buildings lay less than 20 m above the channel, compared with 61% in the middle valley and 87% in the lower reach (Fig. 4e). This pattern implicates the high momentum of a sediment-laden surge confined in a narrow valley, superelevation in bends and the collapse of undercut terraces, rather than inundation alone ^43–45^. It also means that a single setback distance or flood-mark height cannot define safe ground along the whole corridor (Supplementary Table 9).

### Settlement had grown fastest in the destructive zone

Built-up surface on the valley floor had expanded far faster than on higher ground (Fig. 5a). Within 1 km of the channel in the graded corridor, built-up area less than 10 m above the channel grew 17-fold between 1975 and 2020, and that 10–20 m above the channel 13-fold, compared with 7.7-fold for land more than 80 m above it (Supplementary Table 10) ^46,47^. Inside the area later mapped as flow extent, built-up surface increased from 3.5 ha to 43.7 ha (consistent with an independent estimate ^31^). At Trishuli Bazar–Bidur, much of the riverside building destroyed in 2026 had appeared since 2005 (Fig. 5b). The pattern mirrors the faster growth of settlements in flood zones observed worldwide ^15,48^ and in Nepal's road and hydropower corridors ^13,49^.

Applying the damage-calibrated height to the whole corridor identifies the ground that the 2026 event showed to be most hazardous. The core zone — below the 50%-destruction height and within 500 m of the channel — contained 4,868 buildings, of which 1,541 survived, and an estimated 6,100 residents in 2026 ^50^. It captured 73% of all destroyed buildings. An outer zone, below the height that bounded 90% of destroyed buildings, contained 7,415 buildings (3,377 surviving) and about 9,600 residents and captured 89% of destroyed buildings (Fig. 6c). These zones are an evidence base, not a regulatory map, but they indicate the scale of the relocation and reconstruction decisions now facing local and national government ^32^.

### Warning time was available for most destroyed buildings

The propagation record shows that warning time was short only in the uppermost reach (Fig. 5c). The first official warnings were telephoned from Rasuwa between 08:46 and 08:54, requesting evacuation of residents up to 200 m above the riverbank, and the Department of Hydrology and Meteorology sent 679,295 SMS warnings at 09:15 ^20^. By then the wave had passed Syaphrubesi and was approaching Betrawati. Interpolating arrival times along the channel, 29% of destroyed buildings were reached before the SMS was sent, and only 24% received it at least 30 minutes ahead of the flood (Fig. 5d). Had an alert been issued automatically two minutes after the seismic signal, which exceeded magnitude 5 ^18,51^, no destroyed building would have been reached before the alert, and 73% would have had at least 30 minutes (median 41 min). Even so, the median warning in Gosaikunda would have been only 6 min, compared with 54 min in Bidur (Supplementary Table 11).

Mortality cannot yet be located — 57% of the bodies were recovered beyond the corridor, in Chitwan and Nawalparasi ^20^, and the reported totals were still being revised in late September (Supplementary Table 12) — but the distribution of the missing is consistent with the warning gradient. Rasuwa district, where the flood arrived within minutes of the failure, recorded 3,514 missing people (2.6 per destroyed building in its local levels), whereas Nuwakot, reached 30–90 minutes after the failure, recorded 1,247 (0.4 per destroyed building). The difference also reflects the many travellers, pilgrims, customs officers and hydropower workers present at the border on the day of the disaster ^20^.

### Recovery priorities

We combined satellite-recorded destruction, RDNA-affected buildings, government-reported affected people, modelled building debris and the buildings and population in the core danger zone into a composite index, and propagated uncertainty in weighting, normalization and aggregation by Monte Carlo simulation ^52,53^ (Methods). Bidur and Gosaikunda ranked first and second in almost every simulation (probability of a top-three rank 1.00 and 0.99), followed by Kispang (0.77) (Fig. 6a,b and Supplementary Fig. 5c). Benighat Rorang ranked sixth on average but with the widest interval, reflecting the absence of satellite grading and the large RDNA count (Table 2).

Building debris, modelled with the coefficients used by UNDP for the harmonized inventory, amounted to 1.04 million tonnes (90% range 0.44–1.22 million tonnes under uncertain material coefficients and settlement factors; Fig. 6e and Supplementary Fig. 5a,b), roughly 1.9 times the first UNDP estimate ^28^. Bidur accounted for 60% of this tonnage, but only 44% if the threefold multiplier applied to urban buildings is removed, so that clearance planning in Bidur depends strongly on an untested assumption. In its four areas of interest, CEMS also graded 73 km of road and 44 of 54 affected bridges as destroyed (Supplementary Table 13). The available monetary estimates differ by more than an order of magnitude because they measure different things (Fig. 6d and Supplementary Table 14): modelled direct building damage (US$0.17 billion) ^28^, private housing and household assets (US$0.42 billion), all physical damage (US$1.66–1.81 billion) ^21,29^, total effects (US$2.70 billion) and recovery needs (US$4.77 billion) ^21^. Energy alone accounted for US$0.89 billion of damage, with 13 hydropower projects (759 MW) affected and about 431 MW of generation, roughly a tenth of national capacity, interrupted ^21^. Before the event, the land later covered by the flow included 3.4 km^2^ of cropland, 98% of it in the Trishuli valley, 1.0 km^2^ of built-up land and 12.3 km^2^ of tree cover (Supplementary Table 15) ^54^.

## Discussion

The 2026 cascade shows that a single, easily measured terrain variable — height above the pre-event channel — explains most of the observed building destruction along a 207-km corridor, and that the height reached by destruction declined systematically downstream. Height above the channel integrates the factors that empirical vulnerability models express through flow depth, velocity and impact pressure ^43,55–58^, which are not observable for most buildings after an event of this kind. Because the damage-calibrated height agreed closely with the independently mapped flow margins (ρ = 0.97), with gauged stage rises and with the deceleration of the wave, it captures the physical envelope of the flow rather than artefacts of any one product. The approach needs only a pre-event elevation model, a traced flow path and the damage grading that is now routinely produced within days of a disaster ^30^.

Three implications follow for recovery in the Bhote Koshi–Trishuli corridor. First, danger zones should be defined by reach-specific heights above the channel rather than by a uniform flood mark or setback distance: a criterion appropriate to the lower Trishuli, where the destructive height was 7–12 m, would leave out most of the gorge, where destruction reached about 60 m above the river. Second, 1,541 buildings that survived within the core zone, and 3,377 within the outer zone, require structural inspection and a decision on whether they can be safely reoccupied; reconstruction in these zones would recreate the exposure that grew fastest before 2026 (Fig. 5a). Third, the largest debris and housing burdens lie in Bidur and Gosaikunda, but the uncertain urban debris multiplier and the unexplained RDNA counts below Galchhi should be resolved by field survey before large clearance contracts or compensation are committed.

The warning analysis points to an achievable improvement. Telephone warnings and SMS messages were issued 9 and 38 minutes after the failure but were overtaken by a flood moving at more than 50 m s^−1^ in the upper reach ^17,33^. Downstream of Betrawati, however, the flood took between 45 minutes and nearly seven hours to arrive. An automated chain that converts a strong seismic signal from a known high-hazard slope into immediate, location-specific alerts — combined with transboundary data sharing, which was absent on 26 August ^16,34^ — would have provided at least 30 minutes for most of the buildings that were destroyed. Whether such warning saves lives also depends on how quickly people can reach safe ground; travel-time models of the kind used to assess access to cyclone shelters in coastal Bangladesh ^59^ could map evacuation times to ground above the damage-calibrated height. The same principle applies to the many Himalayan valleys where hydropower development has drawn settlements and workers onto valley floors below glacial and periglacial sources ^13,14,60^.

The analysis has limitations. The 30-m Copernicus elevation model ^61,62^ is a surface model built from data acquired before 2015; vegetation, buildings and later changes in the channel, including deposition by the 2025 outburst ^22^, affect heights by several metres, more in narrow gorges. Height above the channel is not water depth: in the gorge it also captures run-up, erosion and terrace collapse. Damage labels were not validated in the field, the building stock is drawn from open footprints whose completeness varies ^63^ and some destroyed buildings had been deleted from OpenStreetMap after the event; we therefore restricted inference to graded areas and corroborated labels with independent Sentinel-2 change. Arrival times between gauges were interpolated, and gauge-loss times approximate arrival only to within several minutes. Casualty figures remain provisional and cannot yet be assigned to locations. Finally, the composite ranking reflects the indicators chosen; we report its sensitivity rather than a single order.

Disaster mapping has become fast and plentiful, but its outputs are rarely reconciled or used to learn how the hazard interacted with the built environment. In this event, a reconciled inventory and a pre-event elevation model were sufficient to recover the destructive envelope of the flood along 207 km, to show that recent development had moved into it, and to quantify the warning time that went unused. Building such analyses into post-disaster needs assessments would give reconstruction an objective, event-calibrated basis and help to prevent the next cascade from destroying what is rebuilt.

## Methods

### Study design and data

We assembled every openly accessible building-damage record for the event, together with official reports, terrain, imagery, settlement and population data (Supplementary Table 1 and Supplementary Note 1). All sources were retrieved between 9 September and 20 October 2026 and archived with retrieval logs and SHA-256 checksums. Damage records comprised (i) the HOT inventory of 1,053 OpenStreetMap footprints graded as no damage, minor, major or destroyed, with an analysed-area polygon ^27^; (ii) the latest CEMS grading products for the four areas of interest that were graded (AOI01 Syapru Besi, AOI02 Timure, AOI03 Bidur and AOI05 Phosretar), comprising 4,685 building points graded as possibly damaged, damaged or destroyed, with area-of-interest polygons, not-analysed areas, imagery metadata and per-area statistics from the CEMS rapid-mapping service ^24,25^; and (iii) the UNDP RAPIDA building-debris service, which re-published 3,043 footprints attributed to CEMS (2,311), SERTIT (48) and UNOSAT (684) ^28^. The UNOSAT flow-extent polygon (37.35 km^2^ within a 363 km^2^ analysed area) was used as an independent observation of the flood footprint ^26^. Official information came from the NDRRMA situation reports and consolidated update to 3 October 2026 ^20^, the RDNA ^21^ and the propagation timeline of the Centre of Hydrology and Water Resources Research ^19^.

The building stock was taken from the Overture Maps release 2026-09-23.1 ^64^, which conflates OpenStreetMap ^65^, Google Open Buildings ^66^ and Microsoft footprints; we retained 113,533 footprints within 2 km of the channel. Terrain came from the Copernicus GLO-30 digital elevation model ^61^, settlement history from GHS-BUILT-S R2023A (1975–2020, 100 m) ^46,47^, population from WorldPop Global2 R2025A constrained counts for 2015, 2020 and 2026 ^50,67^, infrastructure from Overture transportation and base themes, administrative boundaries from geoBoundaries ^68^ and imagery from Sentinel-2 Level-2A ^69,70^.

### Terrain processing and the traced flow path

The four GLO-30 tiles covering 84.3–85.7° E and 27.6–28.5° N were mosaicked and reprojected by bilinear interpolation to a 30-m grid in WGS 84 / UTM zone 45N. The elevation model was hydrologically conditioned with the Priority-Flood+ε algorithm ^71^, which guarantees that every cell drains to the grid edge, and D8 flow directions ^72^ and flow accumulation were computed. The flow path was traced downstream from the source coordinates reported by HiRISK (28.2887° N, 85.5282° E) ^16^ to the Trishuli–Kali Gandaki confluence at Devghat, a distance of 206.8 km. The path passed within 0.6 km of every reference settlement and its flow accumulation increased at the confluences of the Budhi Gandaki and Marsyangdi, confirming that it followed the main channel. Channel elevations along the path were made non-increasing downstream by a cumulative minimum, smoothed with an 11-cell running mean and constrained again, which removes artefacts from bridges and vegetation in the surface model.

Height above the channel (relative elevation) was computed for every cell within 6 km of the path as the cell elevation minus the inverse-distance-weighted (power 2) mean of the 16 nearest channel elevations ^36,37,73^. For each building we also computed distance to the channel, distance downstream (chainage), the bank side and whether the building lay on the outer bank of a bend (from the signed curvature of the smoothed path over ±300 m), the local hillslope gradient, the channel gradient over a 2-km window and the width of the valley floor below 20 m relative elevation along a transect perpendicular to the path. The same transects, spaced every 90 m, were intersected with the UNOSAT flow extent to obtain the height of its outer edge on each bank.

### Harmonization of damage records

All records were matched to the common building stock. Each UNDP footprint was assigned to the stock polygon with which it shared the largest overlap; each HOT footprint was matched greedily by decreasing overlap, with at most one HOT footprint per stock polygon; and each CEMS point was matched greedily by increasing distance (zero inside a footprint, maximum 10 m) with at most one point per footprint. Records without a match — 521 UNDP footprints, 363 HOT footprints and 631 CEMS points, many of them destroyed buildings deleted from OpenStreetMap after the event — were added to the stock as separate buildings, so that no damage record was lost; the common stock comprised 115,048 buildings. Damage grades were mapped to a common ordinal scale (none; minor or possibly damaged; major or damaged; destroyed), and each building took the most severe grade recorded by any product. Inter-product agreement was measured with Cohen's κ ^35^ on the 867 buildings graded by both HOT and CEMS (CEMS AOI01 and AOI02). Because CEMS and UNDP list only damaged buildings, a building was treated as graded-undamaged only if it lay inside a CEMS area of interest and outside its not-analysed areas, or if it carried a HOT label; statistical models were restricted to this graded domain (23,453 buildings within 1 km of the channel). HOT confidence scores and a 5-m translation of all HOT footprints were used to check the sensitivity of the local labels and of their overlap with the flow extent (Supplementary Fig. 6 and Supplementary Note 2).

### Statistical models

For the HOT inventory, the probability of destruction was modelled by logistic regression on height above the channel, and 95% confidence bands and the height at 50% probability were obtained from 1,000 bootstrap resamples of 1-km reaches, which preserves spatial dependence ^74,75^. A multivariable logistic model and a proportional-odds ordinal model of the four HOT classes ^76^ included height (per 10 m), log distance, chainage, valley-floor width, outer-bank position, hillslope gradient, log footprint area and building density, with standard errors clustered by 1-km reach.

For the graded domain, we fitted histogram-based gradient-boosted trees (400 iterations, learning rate 0.05, 31 leaves, minimum 40 samples per leaf, L2 regularization 1) ^38,39^ to predict destruction from nine terrain and building attributes. Performance was estimated by six-fold cross-validation grouped by 5-km reaches, so that test buildings were spatially separated from training buildings ^40,41,77^, and compared with logistic models using all attributes or height alone. Variable importance was the mean decrease in test-fold AUC over ten permutations ^42,78,79^. Two further tests examined dependence on the labels: a model trained and cross-validated on CEMS labels alone within CEMS areas, and a model trained on all labels outside the HOT reach (21.4–41.5 km) and evaluated against HOT's independent labels (Supplementary Note 3).

The damage-calibrated destructive height was estimated separately for 12 reaches of 5–7 km within the graded areas, as the height at which a logistic model of destruction on height above the channel reached 50% probability, with 500 block-bootstrap resamples of 0.5-km reaches. Where the bootstrap interval exceeded 60 m, we used the smaller of this estimate and the 90th percentile height of destroyed buildings. Reach estimates were smoothed with a three-reach running median within each contiguous graded segment to suppress single-reach outliers caused by a few up-slope records; an outer envelope used the 90th percentile height of destroyed buildings smoothed in the same way. Downstream of the last graded reach, the envelope was interpolated linearly between the stage rises recorded or reconstructed at Galchhi (8.9 m) ^17^, Kali Khola (12.3 m maximum against a normal level of about 3.2 m) and Devghat (6.57 m against about 4 m) ^19^. Agreement with the UNOSAT flow-edge height (median of both banks within each reach) was measured by Spearman's rank correlation (Supplementary Note 4).

### Sentinel-2 corroboration

Clear-sky median composites were built at 20 m from all Sentinel-2 Level-2A scenes with less than 70% cloud cover acquired in October 2025 (pre-event, after the July 2025 flood; 14 scenes) and between 21 September and 18 October 2026 (post-event; 19 scenes), keeping only pixels classed as vegetation, bare soil, water or unclassified in the scene classification layer ^69,70^. Reflectance was computed with each scene's scale factor; the processing-baseline offset listed in the metadata was applied only where the archive had not already removed it, and reflectance was clipped at 10^−4^ before computing visible brightness, the normalized difference vegetation index, the bare soil index and the normalized difference water index. Where an acquisition had been processed twice, only the later processing was used (Supplementary Note 5). Composites were built per MGRS tile and mosaicked by the larger number of clear observations. Post-minus-pre differences were averaged over a 3 × 3-pixel window around each building, and their ability to separate destroyed from undamaged buildings was measured by the AUC.

### Exposure, infrastructure and warning time

GHS-BUILT-S and WorldPop grids were interpolated to the 30-m grid by assigning each fine cell the density of its source cell, which preserves totals. Combining multi-temporal settlement and population layers in this way follows GIS and remote-sensing approaches for tracking how flood exposure changes over time ^48,80^. Built-up surface and population were summed within the UNOSAT flow extent and within bands of height above the channel within 1 km of the path. Pre-event land cover inside the flow extent was taken from ESA WorldCover 2021 (10 m) ^54^. Roads, bridges and power assets inside the flow extent were taken from Overture; damaged road lengths and bridge counts graded by CEMS are reported separately (Supplementary Table 13) because they are observations rather than exposure.

Arrival times of the wave front were assembled from the seismic failure time and the CHWRR timeline (Supplementary Table 2) and interpolated linearly along the channel. Gauge-loss times are upper bounds on arrival. Lead time for each destroyed building was the interpolated arrival time minus the alert time under three scenarios: the mass SMS (09:15), the first telephone warnings (08:50, the midpoint of 08:46–08:54) and a counterfactual automatic alert two minutes after the seismic signal (08:39:10) (Supplementary Note 6).

### Municipal priorities, debris and economic estimates

Indicators were assigned to local levels using geoBoundaries ^68^ with spelling harmonized to the RDNA. The composite index combined six indicators: satellite-recorded destroyed buildings, RDNA-affected buildings, government-reported affected people ^28^, modelled building debris and buildings and population in the core danger zone. In each of 20,000 Monte Carlo draws, weights were sampled from a flat Dirichlet distribution, indicators were normalized by min–max scaling, percentile ranks or logistic-transformed z-scores, and aggregated arithmetically or geometrically; we report the median rank, its 5–95% interval and the probability of a top-three rank ^52,53,81^.

Building debris was estimated for the harmonized inventory with the UNDP model: floor area (footprint area × number of floors) × a grade coefficient (1.0, 0.5 and 0.05 t m^−2^ for destroyed, damaged and possibly damaged buildings) × a settlement factor (3, 2 and 1 for urban, peri-urban and rural buildings) ^28^. Floors and settlement type were taken from UNDP records where available; otherwise floors were set to the mean for the settlement type and buildings with at least 40 neighbours within 100 m were treated as urban, a threshold calibrated on UNDP's classification. Uncertainty was explored with 5,000 draws in which grade coefficients were scaled by a common factor between 0.6 and 1.4 and the urban factor varied between 1 and 3. The resulting distributions are shown in Supplementary Fig. 5. Monetary estimates were not recomputed; we compare published estimates and state their scope.

### Reproducibility

All analyses were run in Python 3.14 with NumPy, pandas, Shapely, rasterio, statsmodels ^76^ and scikit-learn ^39^. The scripts, a one-command rebuild, retrieval logs and checksums accompany this manuscript. Random seeds were fixed (20260826). No field survey was conducted, no new satellite classifier was trained and no hydraulic simulation was performed.

## Data availability

All input data are publicly accessible from the sources listed in Supplementary Table 1; the scripts in the code repository retrieve them, and their retrieval dates, URLs and SHA-256 checksums are recorded in the repository. Aggregated results, the height-above-channel raster, the traced flow path and the source data of every figure and table are available at [https://github.com/rezw4n/Nepal_Flood](https://github.com/rezw4n/Nepal_Flood). Building-level damage records from HOT, UNDP and UNOSAT are not redistributed because their redistribution terms have not been confirmed; they are available from the original providers. Gauge records of the Department of Hydrology and Meteorology could not be accessed through its public interface without an application key.

## Code availability

The Python code that reproduces every number, table and figure, with a one-command rebuild and pinned dependencies, is available at [https://github.com/rezw4n/Nepal_Flood](https://github.com/rezw4n/Nepal_Flood).

## References

1. Mani, P. et al. Geomorphic Process Chains in High‐Mountain Regions—A Review and Classification Approach for Natural Hazards Assessment. *Reviews of Geophysics* **61**, e2022RG000791 (2023). [https://doi.org/10.1029/2022RG000791](https://doi.org/10.1029/2022RG000791)

2. Kirschbaum, D. et al. The State of Remote Sensing Capabilities of Cascading Hazards Over High Mountain Asia. *Frontiers in Earth Science* **7**, 197 (2019). [https://doi.org/10.3389/feart.2019.00197](https://doi.org/10.3389/feart.2019.00197)

3. Shugar, D. H. et al. A massive rock and ice avalanche caused the 2021 disaster at Chamoli, Indian Himalaya. *Science* **373**, 300–306 (2021). [https://doi.org/10.1126/science.abh4455](https://doi.org/10.1126/science.abh4455)

4. Chen, C.-M. et al. Erosional cascade during the 2021 Melamchi flood. *Nature Geoscience* **18**, 32–36 (2025). [https://doi.org/10.1038/s41561-024-01596-x](https://doi.org/10.1038/s41561-024-01596-x)

5. Maharjan, S. B., Steiner, J. F., Shrestha, A. B., Maharjan, A. & Nepal, S. The Melamchi flood disaster: Cascading hazard and the need for multihazard risk management. ICIMOD report (Kathmandu: International Centre for Integrated Mountain Development) (2021). [https://doi.org/10.53055/ICIMOD.981](https://doi.org/10.53055/ICIMOD.981)

6. Khadka, N. et al. The 2024 cascading glacial lake outburst flood in the Thame Valley of Everest region, Nepal: process, impacts and implications. *Natural Hazards and Earth System Sciences* **26**, 4131–4152 (2026). [https://doi.org/10.5194/nhess-26-4131-2026](https://doi.org/10.5194/nhess-26-4131-2026)

7. Sattar, A. et al. The Sikkim flood of October 2023: Drivers, causes, and impacts of a multihazard cascade. *Science* **387**, eads2659 (2025). [https://doi.org/10.1126/science.ads2659](https://doi.org/10.1126/science.ads2659)

8. Hock, R. et al. High Mountain Areas. In: Pörtner, H.-O. et al. (eds) IPCC Special Report on the Ocean and Cryosphere in a Changing Climate (Cambridge University Press) (2019). [https://doi.org/10.1017/9781009157964.004](https://doi.org/10.1017/9781009157964.004)

9. Ahmed, R., Bhardwaj, A., Sam, L. & Van Tricht, L. Ice-rock avalanches in a warming Himalaya indicate pathways toward effective preparedness. *Communications Earth & Environment* **7**, 217 (2026). [https://doi.org/10.1038/s43247-026-03352-y](https://doi.org/10.1038/s43247-026-03352-y)

10. Bashkova, E., Rupper, S. B., Shugar, D. H. & Forster, R. R. Global database of glacier failures (1900–2025). Earth System Science Data Discussions (preprint) (2026). [https://doi.org/10.5194/essd-2026-481](https://doi.org/10.5194/essd-2026-481)

11. Taylor, C., Robinson, T. R., Dunning, S., Carr, J. R. & Westoby, M. Glacial lake outburst floods threaten millions globally. *Nature Communications* **14**, 487 (2023). [https://doi.org/10.1038/s41467-023-36033-x](https://doi.org/10.1038/s41467-023-36033-x)

12. Zheng, G. et al. Increasing risk of glacial lake outburst floods from future Third Pole deglaciation. *Nature Climate Change* **11**, 411–417 (2021). [https://doi.org/10.1038/s41558-021-01028-3](https://doi.org/10.1038/s41558-021-01028-3)

13. Schwanghart, W., Worni, R., Huggel, C., Stoffel, M. & Korup, O. Uncertainty in the Himalayan energy–water nexus: estimating regional exposure to glacial lake outburst floods. *Environmental Research Letters* **11**, 074005 (2016). [https://doi.org/10.1088/1748-9326/11/7/074005](https://doi.org/10.1088/1748-9326/11/7/074005)

14. Li, D. et al. High Mountain Asia hydropower systems threatened by climate-driven landscape instability. *Nature Geoscience* **15**, 520–530 (2022). [https://doi.org/10.1038/s41561-022-00953-y](https://doi.org/10.1038/s41561-022-00953-y)

15. Rentschler, J. et al. Global evidence of rapid urban growth in flood zones since 1985. *Nature* **622**, 87–92 (2023). [https://doi.org/10.1038/s41586-023-06468-9](https://doi.org/10.1038/s41586-023-06468-9)

16. Liu, Q. et al. Rapid Hazard Assessment Report No. NP3: Lirung massif, Lhende catchment, Upper Trishuli watershed (rock-ice avalanche, flood), 26 August 2026. HiRISK Rapid Hazard Assessment (last update 28 Aug 2026) (2026). [https://hirisk.org/wp-content/uploads/2026/08/RHA_NP3_RasuwaFlood.pdf](https://hirisk.org/wp-content/uploads/2026/08/RHA_NP3_RasuwaFlood.pdf)

17. ICIMOD. Understanding the Gyirong–Rasuwa disaster of 26 August 2026: A preliminary synthesis. ICIMOD report (Kathmandu), ISBN 978-92-9115-983-3 (2026). [https://doi.org/10.53055/ICIMOD.1150](https://doi.org/10.53055/ICIMOD.1150)

18. Roy, P. et al. 26 August 2026 rock–ice avalanche in Nepal: rapid assessment of the cascading disaster using satellite data. *Journal of the Indian Society of Remote Sensing* (2026). [https://doi.org/10.1007/s12524-026-02611-x](https://doi.org/10.1007/s12524-026-02611-x)

19. Centre of Hydrology and Water Resources Research (CHWRR), Water and Energy Commission Secretariat. Assessment Report II: Rasuwa–Bhote Koshi Flood Event, 2026 (2083). Government of Nepal, Kathmandu (13 September 2026) (2026). [https://giwmscdnone.gov.np/media/pdf_upload/1_Situation_Report_Bhotekoshi%20Flood_2026_CHWRR_hnmns6o.pdf](https://giwmscdnone.gov.np/media/pdf_upload/1_Situation_Report_Bhotekoshi%20Flood_2026_CHWRR_hnmns6o.pdf)

20. National Disaster Risk Reduction and Management Authority (NDRRMA). Bhotekoshi–Trishuli Flood: Search, Rescue and Relief Update (26 August–3 October 2026). NDRRMA, Government of Nepal, Kathmandu (2026). [https://ndrrma.gov.np/mediafiles/publications/Bhotekoshi-Trishuli_Flood_Update_From_August_26_2026_to_October_3_2026.pdf](https://ndrrma.gov.np/mediafiles/publications/Bhotekoshi-Trishuli_Flood_Update_From_August_26_2026_to_October_3_2026.pdf)

21. Government of Nepal, National Disaster Risk Reduction and Management Authority & National Planning Commission. Rapid Damage and Needs Assessment (RDNA): Rasuwa–Bhotekoshi Flood 2026. NDRRMA, Kathmandu (2026). [https://ndrrma.gov.np/mediafiles/rasuwa/Rapid_Damage_and_Needs_Assessment_RDNA_Rasuwa-Bhotekoshi_Flood_2026.pdf](https://ndrrma.gov.np/mediafiles/rasuwa/Rapid_Damage_and_Needs_Assessment_RDNA_Rasuwa-Bhotekoshi_Flood_2026.pdf)

22. Xu, Q. et al. Brief communication: Repeated supraglacial lake drainage from the Purepu Glacier system, central Himalaya. EGUsphere preprint (Brief communication; in discussion) (2026). [https://doi.org/10.5194/egusphere-2026-4065](https://doi.org/10.5194/egusphere-2026-4065)

23. Zhang, T.-G. et al. Transboundary outburst floods from giant supraglacial lakes over the Himalayan China–Nepal border. *Advances in Climate Change Research* **18**, 267–282 (2026). [https://doi.org/10.1016/j.accre.2026.06.022](https://doi.org/10.1016/j.accre.2026.06.022)

24. Copernicus Emergency Management Service (European Commission JRC). EMSR927: Flood in Nepal - flood and mass movement damage grading, Syapru Besi and Timure, Rasuwa District (27 August 2026). Copernicus EMS Rapid Mapping (dataset; re-published with DOI via UNESCO IHP-WINS) (2026). [https://doi.org/10.63253/bkdj361r](https://doi.org/10.63253/bkdj361r)

25. Copernicus Emergency Management Service. EMSR927 Flood in Nepal: rapid-mapping activation record (areas of interest, imagery and grading statistics) and vector products. Copernicus EMS Rapid Mapping (accessed 20 October 2026) (2026). [https://rapidmapping.emergency.copernicus.eu/backend/dashboard-api/public-activations/?code=EMSR927](https://rapidmapping.emergency.copernicus.eu/backend/dashboard-api/public-activations/?code=EMSR927)

26. UNOSAT (UNITAR). Satellite-detected mudflow and rockflow extent in Rasuwa and Nuwakot Districts, Bagmati Province, Nepal (26-27 August 2026). UNOSAT products 4257/4258 (dataset; re-published with DOI via UNESCO IHP-WINS) (2026). [https://doi.org/10.63253/1y26ihdq](https://doi.org/10.63253/1y26ihdq)

27. Humanitarian OpenStreetMap Team (HOT). Nepal flood building damage inventory and analysed-area polygon (fAIR-assisted labels on OpenStreetMap footprints). HOT raw-data API (retrieved 9 September 2026) (2026). [https://production-raw-data-api.s3.amazonaws.com/ISO3/NPL/buildings/hot_flood_npl_buildings_damage_overview.html](https://production-raw-data-api.s3.amazonaws.com/ISO3/NPL/buildings/hot_flood_npl_buildings_damage_overview.html)

28. United Nations Development Programme (UNDP). RAPIDA assessment of the floods in Nepal (StoryMap and feature services for building debris, economic estimate, exposure and affected population). UNDP GeoSMART (retrieved 9 September 2026) (2026). [https://geosmart.undp.org/arcgis/apps/storymaps/stories/7450cd01c584424f8a10ccfc166b167a](https://geosmart.undp.org/arcgis/apps/storymaps/stories/7450cd01c584424f8a10ccfc166b167a)

29. World Bank & Global Facility for Disaster Reduction and Recovery (GFDRR). Global Rapid Post-Disaster Damage Estimation (GRADE) Report: Rasuwa Flash Flood, Nepal. World Bank Report No. 215321 (Washington, DC) (2026). [http://documents.worldbank.org/curated/en/099217209292624461](http://documents.worldbank.org/curated/en/099217209292624461)

30. Voigt, S. et al. Global trends in satellite-based emergency mapping. *Science* **353**, 247–252 (2016). [https://doi.org/10.1126/science.aad8728](https://doi.org/10.1126/science.aad8728)

31. Li, R. When a high-mountain slope failure cascades downstream: physical footprint and evolving exposure of the 2026 Gyirong mixed rock-ice cascade. arXiv preprint (v2, 7 Sep 2026) (2026). [https://doi.org/10.48550/arXiv.2609.04563](https://doi.org/10.48550/arXiv.2609.04563)

32. Radio Nepal. Government to relocate and rebuild Bhotekoshi flood-affected settlements in safer areas. Radio Nepal Online (21 September 2026) (2026). [https://radionepalonline.com/en/2026/09/21/436388.html](https://radionepalonline.com/en/2026/09/21/436388.html)

33. Acharya, S. The Bhote Koshi–Trishuli flash flood of 26 August 2026, Rasuwa, Nepal: warning latency exceeded flood travel time. EarthArXiv preprint (2026). [https://doi.org/10.31223/X5HN5H](https://doi.org/10.31223/X5HN5H)

34. Xu, C. Warnings must cross borders before disasters do. *npj Natural Hazards (Editorial)* **3**, 73 (2026). [https://doi.org/10.1038/s44304-026-00271-y](https://doi.org/10.1038/s44304-026-00271-y)

35. Cohen, J. A coefficient of agreement for nominal scales. *Educational and Psychological Measurement* **20**, 37–46 (1960). [https://doi.org/10.1177/001316446002000104](https://doi.org/10.1177/001316446002000104)

36. Rennó, C. D. et al. HAND, a new terrain descriptor using SRTM-DEM: Mapping terra-firme rainforest environments in Amazonia. *Remote Sensing of Environment* **112**, 3469–3481 (2008). [https://doi.org/10.1016/j.rse.2008.03.018](https://doi.org/10.1016/j.rse.2008.03.018)

37. Nobre, A. D. et al. Height Above the Nearest Drainage – a hydrologically relevant new terrain model. *Journal of Hydrology* **404**, 13–29 (2011). [https://doi.org/10.1016/j.jhydrol.2011.03.051](https://doi.org/10.1016/j.jhydrol.2011.03.051)

38. Friedman, J. H. Greedy function approximation: A gradient boosting machine. *The Annals of Statistics* **29**, 1189–1232 (2001). [https://doi.org/10.1214/aos/1013203451](https://doi.org/10.1214/aos/1013203451)

39. Pedregosa, F. et al. Scikit-learn: machine learning in Python. *Journal of Machine Learning Research* **12**, 2825–2830 (2011). [https://jmlr.org/papers/v12/pedregosa11a.html](https://jmlr.org/papers/v12/pedregosa11a.html)

40. Roberts, D. R. et al. Cross‐validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. *Ecography* **40**, 913–929 (2017). [https://doi.org/10.1111/ecog.02881](https://doi.org/10.1111/ecog.02881)

41. Ploton, P. et al. Spatial validation reveals poor predictive performance of large-scale ecological mapping models. *Nature Communications* **11**, 4540 (2020). [https://doi.org/10.1038/s41467-020-18321-y](https://doi.org/10.1038/s41467-020-18321-y)

42. Fisher, A., Rudin, C. & Dominici, F. All models are wrong, but many are useful: Learning a variable's importance by studying an entire class of prediction models simultaneously. Journal of Machine Learning Research (2019). [https://jmlr.org/papers/v20/18-760.html](https://jmlr.org/papers/v20/18-760.html)

43. Jakob, M., Stein, D. & Ulmi, M. Vulnerability of buildings to debris flow impact. *Natural Hazards* **60**, 241–261 (2012). [https://doi.org/10.1007/s11069-011-0007-2](https://doi.org/10.1007/s11069-011-0007-2)

44. Papathoma-Köhle, M., Gems, B., Sturm, M. & Fuchs, S. Matrices, curves and indicators: A review of approaches to assess physical vulnerability to debris flows. *Earth-Science Reviews* **171**, 272–288 (2017). [https://doi.org/10.1016/j.earscirev.2017.06.007](https://doi.org/10.1016/j.earscirev.2017.06.007)

45. Cook, K. L., Andermann, C., Gimbert, F., Adhikari, B. R. & Hovius, N. Glacial lake outburst floods as drivers of fluvial erosion in the Himalaya. *Science* **362**, 53–57 (2018). [https://doi.org/10.1126/science.aat4981](https://doi.org/10.1126/science.aat4981)

46. Pesaresi, M. et al. Advances on the Global Human Settlement Layer by joint assessment of Earth Observation and population survey data. *International Journal of Digital Earth* **17**, 2390454 (2024). [https://doi.org/10.1080/17538947.2024.2390454](https://doi.org/10.1080/17538947.2024.2390454)

47. Pesaresi, M. GHS-BUILT-S R2023A - GHS built-up surface grid, derived from Sentinel2 composite and Landsat, multitemporal (1975-2030). European Commission, Joint Research Centre (dataset) (2023). [https://doi.org/10.2905/9F06F36F-4B11-47EC-ABB0-4F8B7B1D72EA](https://doi.org/10.2905/9F06F36F-4B11-47EC-ABB0-4F8B7B1D72EA)

48. Tellman, B. et al. Satellite imaging reveals increased proportion of population exposed to floods. *Nature* **596**, 80–86 (2021). [https://doi.org/10.1038/s41586-021-03695-w](https://doi.org/10.1038/s41586-021-03695-w)

49. McAdoo, B. G. et al. Roads and landslides in Nepal: how development affects environmental risk. *Natural Hazards and Earth System Sciences* **18**, 3203–3210 (2018). [https://doi.org/10.5194/nhess-18-3203-2018](https://doi.org/10.5194/nhess-18-3203-2018)

50. WorldPop. Global2 constrained population counts, 2015–2030, 100 m (release R2025A): Nepal. WorldPop, University of Southampton (dataset) (2025). [https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/](https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/)

51. Slaughter, S. et al. 2026 Nepal Debris Avalanche and Flash Flood. U.S. Geological Survey, Landslide Hazards Program (web page, 27-28 Aug 2026) (2026). [https://www.usgs.gov/programs/landslide-hazards/science/2026-nepal-debris-avalanche-and-flash-flood](https://www.usgs.gov/programs/landslide-hazards/science/2026-nepal-debris-avalanche-and-flash-flood)

52. Saisana, M., Saltelli, A. & Tarantola, S. Uncertainty and Sensitivity Analysis Techniques as Tools for the Quality Assessment of Composite Indicators. *Journal of the Royal Statistical Society Series A: Statistics in Society* **168**, 307–323 (2005). [https://doi.org/10.1111/j.1467-985X.2005.00350.x](https://doi.org/10.1111/j.1467-985X.2005.00350.x)

53. OECD, European Union & Joint Research Centre - European Commission. Handbook on Constructing Composite Indicators: Methodology and User Guide. OECD Publishing (Paris) (2008). [https://doi.org/10.1787/9789264043466-en](https://doi.org/10.1787/9789264043466-en)

54. Zanaga, D. et al. ESA WorldCover 10 m 2021 v200. Zenodo (dataset) (2022). [https://doi.org/10.5281/zenodo.7254221](https://doi.org/10.5281/zenodo.7254221)

55. Fuchs, S., Heiss, K. & Hübl, J. Towards an empirical vulnerability function for use in debris flow risk assessment. *Natural Hazards and Earth System Sciences* **7**, 495–506 (2007). [https://doi.org/10.5194/nhess-7-495-2007](https://doi.org/10.5194/nhess-7-495-2007)

56. Kang, H.-S. & Kim, Y.-T. The physical vulnerability of different types of building structure to debris flow events. *Natural Hazards* **80**, 1475–1493 (2016). [https://doi.org/10.1007/s11069-015-2032-z](https://doi.org/10.1007/s11069-015-2032-z)

57. Prieto, J. A., Journeay, M., Acevedo, A. B., Arbelaez, J. D. & Ulmi, M. Development of structural debris flow fragility curves (debris flow buildings resistance) using momentum flux rate as a hazard parameter. *Engineering Geology* **239**, 144–157 (2018). [https://doi.org/10.1016/j.enggeo.2018.03.014](https://doi.org/10.1016/j.enggeo.2018.03.014)

58. Luo, H. Y., Zhang, L. M., Zhang, L. L., He, J. & Yin, K. S. Vulnerability of buildings to landslides: The state of the art and future needs. *Earth-Science Reviews* **238**, 104329 (2023). [https://doi.org/10.1016/j.earscirev.2023.104329](https://doi.org/10.1016/j.earscirev.2023.104329)

59. Ahmed, A., Ferdous, Z., Kabir, M. H., Rahman, O., Ahmed, R. & Ryhan, M. A. Assessment of physical accessibility to cyclone shelters in the exposed coastal area of Bangladesh by using geospatial approach. *The Dhaka University Journal of Earth and Environmental Sciences* **13**, 63–75 (2024). [https://doi.org/10.3329/dujees.v13i2.79455](https://doi.org/10.3329/dujees.v13i2.79455)

60. Allen, S. K. et al. Glacial lake outburst flood hazard under current and future conditions: worst-case scenarios in a transboundary Himalayan basin. *Natural Hazards and Earth System Sciences* **22**, 3765–3785 (2022). [https://doi.org/10.5194/nhess-22-3765-2022](https://doi.org/10.5194/nhess-22-3765-2022)

61. European Space Agency & Airbus. Copernicus DEM. ESA (dataset) (2022). [https://doi.org/10.5270/ESA-c5d3d65](https://doi.org/10.5270/ESA-c5d3d65)

62. Guth, P. L. & Geoffroy, T. M. LiDAR point cloud and ICESat‐2 evaluation of 1 second global digital elevation models: Copernicus wins. *Transactions in GIS* **25**, 2245–2261 (2021). [https://doi.org/10.1111/tgis.12825](https://doi.org/10.1111/tgis.12825)

63. Herfort, B., Lautenbach, S., Porto de Albuquerque, J., Anderson, J. & Zipf, A. A spatio-temporal analysis investigating completeness and inequalities of global urban building data in OpenStreetMap. *Nature Communications* **14**, 3985 (2023). [https://doi.org/10.1038/s41467-023-39698-6](https://doi.org/10.1038/s41467-023-39698-6)

64. Overture Maps Foundation. Overture Maps buildings theme (open map data release). Overture Maps Foundation (dataset) (2026). [https://overturemaps.org/](https://overturemaps.org/)

65. Haklay, M. & Weber, P. OpenStreetMap: User-Generated Street Maps. *IEEE Pervasive Computing* **7**, 12–18 (2008). [https://doi.org/10.1109/MPRV.2008.80](https://doi.org/10.1109/MPRV.2008.80)

66. Sirko, W. et al. Continental-Scale Building Detection from High Resolution Satellite Imagery. arXiv preprint (2021). [https://doi.org/10.48550/arXiv.2107.12283](https://doi.org/10.48550/arXiv.2107.12283)

67. Stevens, F. R., Gaughan, A. E., Linard, C. & Tatem, A. J. Disaggregating Census Data for Population Mapping Using Random Forests with Remotely-Sensed and Ancillary Data. *PLOS ONE* **10**, e0107042 (2015). [https://doi.org/10.1371/journal.pone.0107042](https://doi.org/10.1371/journal.pone.0107042)

68. Runfola, D. et al. geoBoundaries: a global database of political administrative boundaries. *PLOS ONE* **15**, e0231866 (2020). [https://doi.org/10.1371/journal.pone.0231866](https://doi.org/10.1371/journal.pone.0231866)

69. Drusch, M. et al. Sentinel-2: ESA's Optical High-Resolution Mission for GMES Operational Services. *Remote Sensing of Environment* **120**, 25–36 (2012). [https://doi.org/10.1016/j.rse.2011.11.026](https://doi.org/10.1016/j.rse.2011.11.026)

70. Element 84. Earth Search STAC API: Sentinel-2 Level-2A cloud-optimised GeoTIFFs (collection sentinel-2-l2a). Amazon Web Services Open Data Registry (accessed 19–20 October 2026) (2026). [https://earth-search.aws.element84.com/v1](https://earth-search.aws.element84.com/v1)

71. Barnes, R., Lehman, C. & Mulla, D. Priority-flood: an optimal depression-filling and watershed-labeling algorithm for digital elevation models. *Computers & Geosciences* **62**, 117–127 (2014). [https://doi.org/10.1016/j.cageo.2013.04.024](https://doi.org/10.1016/j.cageo.2013.04.024)

72. O'Callaghan, J. F. & Mark, D. M. The extraction of drainage networks from digital elevation data. *Computer Vision, Graphics, and Image Processing* **28**, 323–344 (1984). [https://doi.org/10.1016/S0734-189X(84)80011-0](https://doi.org/10.1016/S0734-189X%2884%2980011-0)

73. Garousi‐Nejad, I., Tarboton, D. G., Aboutalebi, M. & Torres‐Rua, A. F. Terrain Analysis Enhancements to the Height Above Nearest Drainage Flood Inundation Mapping Method. *Water Resources Research* **55**, 7983–8009 (2019). [https://doi.org/10.1029/2019WR024837](https://doi.org/10.1029/2019WR024837)

74. Efron, B. & Tibshirani, R. J. An Introduction to the Bootstrap. Chapman & Hall/CRC (1993). [https://doi.org/10.1201/9780429246593](https://doi.org/10.1201/9780429246593)

75. Künsch, H. R. The Jackknife and the Bootstrap for General Stationary Observations. *The Annals of Statistics* **17**, 1217–1241 (1989). [https://doi.org/10.1214/aos/1176347265](https://doi.org/10.1214/aos/1176347265)

76. Seabold, S. & Perktold, J. Statsmodels: econometric and statistical modeling with Python. Proceedings of the 9th Python in Science Conference (2010). [https://doi.org/10.25080/Majora-92bf1922-011](https://doi.org/10.25080/Majora-92bf1922-011)

77. Meyer, H. & Pebesma, E. Machine learning-based global maps of ecological variables and the challenge of assessing them. *Nature Communications* **13**, 2208 (2022). [https://doi.org/10.1038/s41467-022-29838-9](https://doi.org/10.1038/s41467-022-29838-9)

78. Strobl, C., Boulesteix, A.-L., Zeileis, A. & Hothorn, T. Bias in random forest variable importance measures: Illustrations, sources and a solution. *BMC Bioinformatics* **8**, 25 (2007). [https://doi.org/10.1186/1471-2105-8-25](https://doi.org/10.1186/1471-2105-8-25)

79. Hooker, G., Mentch, L. & Zhou, S. Unrestricted permutation forces extrapolation: variable importance requires at least one more model, or there is no free variable importance. *Statistics and Computing* **31**, 82 (2021). [https://doi.org/10.1007/s11222-021-10057-z](https://doi.org/10.1007/s11222-021-10057-z)

80. Ahmed, R., Jarin, N. Z. & Rahman, O. Spatiotemporal dynamics of flood exposure in Bangladesh: a GIS and remote sensing based approach. In *Flood Risk Management: Assessment and Strategy* (eds Biswas, B. & Ghute, B. B.) 1–22 (Springer Nature Singapore, 2024). [https://doi.org/10.1007/978-981-97-2688-2_1](https://doi.org/10.1007/978-981-97-2688-2_1)

81. Tate, E. Social vulnerability indices: a comparative assessment using uncertainty and sensitivity analysis. *Natural Hazards* **63**, 325–347 (2012). [https://doi.org/10.1007/s11069-012-0152-2](https://doi.org/10.1007/s11069-012-0152-2)

## Acknowledgements

We thank the agencies and volunteers who produced and openly shared the damage, imagery and official data used here.

## Funding

No funding was received for this study.

\pagebreak

## Figures

![Figure 1](figures/figure_1_overview.png)

**Fig. 1 | The 26 August 2026 cascade and its 207-km impact corridor.** **a**, Shaded-relief map of the corridor from the failure on the north face of Langtang Lirung to the Trishuli–Kali Gandaki confluence at Devghat, showing the D8 flow path traced from the reported source, the UNOSAT flow extent mapped from imagery of 26–27 August, and buildings recorded as destroyed or damaged by at least one product. Distances are along the traced path. **b**, Elevation of the channel along the path. **c**, Damaged and destroyed buildings per 2 km of path; shading marks reaches graded by satellite products. **d**, Deaths and missing people in Nepal reported by NDRRMA between 26 August and 3 October 2026. Map projection: WGS 84 / UTM zone 45N. Data: Copernicus DEM; UNOSAT; HOT; CEMS EMSR927; UNDP RAPIDA; NDRRMA.

![Figure 2](figures/figure_2_inventories.png)

**Fig. 2 | Reconciling the damage record.** **a**, Reaches graded by each product along the corridor and the local levels reported in the RDNA; ticks show individual UNOSAT-attributed records. **b**, Buildings recorded as damaged by each product, by the harmonized union and by the RDNA. **c**, Agreement between HOT and CEMS for the 867 buildings graded by both, as row percentages with counts. **d**, Satellite-graded damaged buildings against RDNA-affected buildings by local level; local levels without satellite grading are plotted at the axis floor. **e**, Sentinel-2 true-colour images from the clearest pre-event (October 2025) and post-event (September–October 2026) scenes at Syaphrubesi (top) and Trishuli Bazar (bottom), with acquisition dates and the same reflectance stretch for all images. **f**, Post-minus-pre change in NDVI at building locations by HOT grade and by CEMS/UNDP grade (boxes, interquartile range; whiskers, 10th–90th percentiles; numbers, buildings), with the AUC for separating destroyed from undamaged buildings within each set. Contains modified Copernicus Sentinel data (2025, 2026).

![Figure 3](figures/figure_3_height_controls.png)

**Fig. 3 | Height above the channel governed destruction.** **a**,**b**, Height above the pre-event channel (shading and white contours), the UNOSAT flow-extent edge and building footprints coloured by the most severe grade recorded, at Timure in the gorge (**a**) and Trishuli Bazar–Bidur in the valley (**b**). **c**, Composition of HOT damage classes by height above the channel; numbers at right give buildings per band (Supplementary Table 6). **d**, Probability of destruction against height above the channel for the three graded reach groups, with 95% block-bootstrap bands; dots mark the height at 50% probability. **e**, Receiver-operating-characteristic curves for gradient-boosted trees under spatial cross-validation, for height alone, and for the model transferred to HOT labels. **f**, Permutation importance (mean loss of AUC ± s.d. across folds).

![Figure 4](figures/figure_4_height_envelope.png)

**Fig. 4 | The destructive height attenuated downstream.** **a**, Damage-calibrated destructive height (height at 50% probability of destruction, with 95% intervals), 90th-percentile height of destroyed buildings, height of the UNOSAT flow-extent edge (median and interquartile range) and stage rises gauged or reconstructed downstream, with the core and outer envelopes used for the danger zones. **b**, Mean celerity of the wave front between timed locations, with times (NPT). **c**, Width of the valley floor less than 20 m above the channel and width of the mapped flow extent (running medians). **d**, Damage-calibrated height against flow-extent edge height for the 11 graded reaches. **e**, Shares of destroyed buildings below 20 m and the number of undamaged buildings below 20 m.

![Figure 5](figures/figure_5_exposure_warning.png)

**Fig. 5 | Exposure growth into the destructive zone and warning time.** **a**, Built-up surface within 1 km of the channel in the graded corridor, relative to 1975, by band of height above the channel (GHS-BUILT-S R2023A). **b**, Epoch in which each 30-m cell first exceeded 10% built-up surface at Trishuli Bazar–Bidur, with the flow extent and destroyed buildings. **c**, Arrival time of the wave front after the failure (log scale) along the corridor and the times of the counterfactual seismic-triggered alert, the first telephone warnings and the mass SMS; the lower panel shows destroyed buildings per 3 km. **d**, Time between alert and wave arrival for the 4,530 destroyed buildings under the three alert scenarios.

![Figure 6](figures/figure_6_priorities.png)

**Fig. 6 | Recovery priorities.** **a**, Indicators by local level, shaded by their log-scaled magnitude (lead-time columns are shaded so that shorter warning is darker). **b**, Median rank and 5–95% interval of the composite index over 20,000 Monte Carlo draws of weights, normalization and aggregation, with the probability of a top-three rank. **c**, Buildings below the damage-calibrated height within 500 m of the channel: destroyed and surviving in the core zone, and additional surviving buildings in the outer zone. **d**, Published monetary estimates by scope (log scale). **e**, Building debris estimated by UNDP and in this study (5–95% Monte Carlo range).

\pagebreak

## Tables

**Table 1 | Damage evidence reconciled in this study.**

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

**Table 2 | Recovery indicators and priorities for the most affected local levels.**

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

*Note:* Destroyed and damaged counts are from the harmonized satellite inventory; RDNA counts are affected private buildings ^21^. Danger-zone counts are buildings within 500 m of the channel below the core damage-calibrated height. Lead times are medians for destroyed buildings under the actual SMS (09:15). Ranks are medians (5–95% interval) of the Monte Carlo composite index.
