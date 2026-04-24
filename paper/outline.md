# p004 paper planning draft

## Working title options
- Beyond mean warming: observed and simulated shifts in the full near-surface temperature distribution
- Regional amplification of hot-tail warming and hydroclimate controls in observations and CMIP6

## Core research questions
1. Are upper-tail temperatures (T95/T99) warming faster than median temperatures (T50), and where is this robust?
2. Is tail amplification seasonally and regionally structured rather than globally uniform?
3. Do CMIP6 models reproduce observed spatial patterns of distributional change (ERA5), including regions of suppression (ratio < 1)?
4. Which hydroclimate states/processes (soil moisture, latent heat, precipitation/energy-limited regimes) organize where amplification occurs?
5. How much of the amplification pattern is attributable to GHG forcing versus aerosol forcing (CESM2-SF)?

## Central claim scaffold
- Temperature distribution change is strongly pattern-dependent: many land regions show amplified hot-tail warming, but not universally.
- Amplification co-locates with hydroclimate transition zones and land-atmosphere coupling metrics.
- Regional process-space diagnostics (e.g., LH vs dSM behavior) provide an interpretable mechanism for why some regions amplify while others do not.
- Single-forcing experiments suggest a dominant anthropogenic forcing imprint with contrasting aerosol influences.

## Proposed paper flow
1. Observational benchmark (ERA5): map trend(T50), trend(T95), ratio trend(T95)/trend(T50), and difference trend(T95-T50).
2. Future projection (CMIP6 MMM, SSP245): map dT50, dT95, ratio dT95/dT50.
3. Model-observation bridge: compare large-scale amplification motifs between ERA5 and CMIP6.
4. Mechanism layer: regional process-space figures (LH vs dSM and related variables by percentile/season).
5. Attribution layer: CESM2-SF ratio maps (GHG vs AAER) to separate forcing fingerprints.
6. Synthesis: conceptual diagram linking hydroclimate regime, coupling state, and tail amplification sign.

## Candidate main figures (v1)

### Figure 1: Observed distributional warming pattern (ERA5)
- /project/amp/miyawaki/plots/p004/era5/jja/trend_t50.jja.pdf
- /project/amp/miyawaki/plots/p004/era5/jja/trend_t95.jja.pdf
- /project/amp/miyawaki/plots/p004/era5/ann/ratioT50_t95.ann.pdf
- /project/amp/miyawaki/plots/p004/era5/jja/t2m/diffT50_t95.jja.trend.pdf

### Figure 2: CMIP6 projected amplification (MMM SSP245)
- /project/amp/miyawaki/plots/p004/cmip6/ann/fut-his/ssp245/mmm/warming_t50.ssp245.ann.pdf
- /project/amp/miyawaki/plots/p004/cmip6/ann/fut-his/ssp245/mmm/warming_t95.ssp245.ann.pdf
- /project/amp/miyawaki/plots/p004/cmip6/ann/fut-his/ssp245/mmm/ratioT50_t95.ssp245.ann.pdf

### Figure 3: Process-space mechanism (regional examples)
- /project/amp/miyawaki/plots/p004/cmip6/sc/historical+ssp370/CESM2/hfls+mrsos/regions/pct/swus/hfls+mrsos_1980-2000+gwl2.0.sc.swus.7.pct.bc.png
- /project/amp/miyawaki/plots/p004/cmip6/sc/historical+ssp370/CESM2/bc/bc.500.spagh.png
- /project/amp/miyawaki/plots/p004/cmip6/sc/historical+ssp370/CESM2/bc/bc.spagh.sa.png
- /project/amp/miyawaki/plots/p004/cmip6/sc/historical+ssp370/CESM2/bc/bc.spagh.sea.png

### Figure 4: Forcing attribution (CESM2-SF)
- /project/amp/miyawaki/plots/p004/cesm2-sf/jja/fut-his/ghg/ratioT50_t95.ghg.jja.pdf
- /project/amp/miyawaki/plots/p004/cesm2-sf/jja/fut-his/aaer/ratioT50_t95.aaer.jja.pdf

### Figure 5: Hydroclimate context (optional main or early supplement)
- /project/amp/miyawaki/plots/p004/ceres+gpcp/jja/hr/clima.2000-2022.jja.pdf
- /project/amp/miyawaki/plots/p004/ceres+gpcp/jja/ai1/clima.2000-2022.jja.pdf
- /project/amp/miyawaki/plots/p004/gpcp/jja/pr/clima_p95.jja.pdf

## Supplement candidates
- Full seasonal ERA5 map set (ann, djf, mam, jja, son) for trend/ratio/difference.
- CMIP6 individual-model ratio/warming maps (model spread and robustness).
- Additional percentile levels (1, 5, 99).
- Extra regional process panels and alternative process variables (qvegt, qsoil, EF variants).

## Immediate next steps for manuscript assembly
1. Lock one canonical season for main text maps (likely JJA + annual contrast).
2. Define one primary amplification metric in text (ratio and/or difference) and keep the other secondary.
3. Pick 3-5 core regions for mechanism figures using objective criteria (e.g., strongest positive/negative amplification and contrasting hydroclimate regime).
4. Build one master table listing each candidate figure, key message, and keep/drop decision.
5. Draft Results section headers directly from the figure sequence above.

## Notes from quick visual audit
- ERA5 already shows coherent, non-uniform amplification structure with both >1 and <1 regions.
- CMIP6 MMM reproduces broad amplification motifs, especially strong high-latitude behavior.
- Regional process-space plots are scientifically rich but currently stylistically heterogeneous; they will need consistent labeling and panel design for publication.
