# Figure interpretations (working notes)

Date: 2026-02-28
Scope: quick visual audit of representative outputs across ERA5, CMIP6, CESM2-SF, and CERES+GPCP/GPCP.

## 1) ERA5 JJA median trend map
Figure: /project/amp/miyawaki/plots/p004/era5/jja/trend_t50.jja.pdf
Interpretation:
- Broad positive warming trend nearly everywhere, with strongest warming over high-latitude land and parts of the Southern Ocean fringe.
- Pattern is smooth and large-scale, suitable as the baseline "mean warming" reference.
Paper use:
- Establishes that the baseline median warming pattern is spatially structured before discussing distribution-tail behavior.

## 2) ERA5 JJA hot-tail trend map
Figure: /project/amp/miyawaki/plots/p004/era5/jja/trend_t95.jja.pdf
Interpretation:
- Similar large-scale warming structure to T50, but with notable regional departures in intensity.
- Highlights where upper-tail warming tracks or diverges from the median.
Paper use:
- Natural pair with T50 map to motivate tail-vs-median diagnostics.

## 3) ERA5 annual ratio map (T95 trend / T50 trend)
Figure: /project/amp/miyawaki/plots/p004/era5/ann/ratioT50_t95.ann.pdf
Interpretation:
- Strongly heterogeneous ratio field with both amplification (>1) and suppression (<1) regions.
- Spatial complexity suggests local controls, not a globally uniform shift of the full distribution.
Paper use:
- Primary map for the central claim that distributional warming is region dependent.

## 4) ERA5 JJA difference-trend map (T95 - T50)
Figure: /project/amp/miyawaki/plots/p004/era5/jja/t2m/diffT50_t95.jja.trend.pdf
Interpretation:
- Positive and negative regions are both present, reinforcing that hot-tail acceleration is not universal.
- Difference metric is intuitive for physical magnitude (K/decade) compared with dimensionless ratio.
Paper use:
- Companion diagnostic to ratio metric; useful for robustness and interpretability.

## 5) CMIP6 MMM annual warming at T50 (SSP245 future-historical)
Figure: /project/amp/miyawaki/plots/p004/cmip6/ann/fut-his/ssp245/mmm/warming_t50.ssp245.ann.pdf
Interpretation:
- Global warming with strongest magnitude over Arctic/high northern latitudes.
- Provides modeled baseline warming field for comparison with T95 and ratio.
Paper use:
- Opens the projection section and anchors the model story.

## 6) CMIP6 MMM annual warming at T95 (SSP245 future-historical)
Figure: /project/amp/miyawaki/plots/p004/cmip6/ann/fut-his/ssp245/mmm/warming_t95.ssp245.ann.pdf
Interpretation:
- Similar geography to T50 but with distinct regional intensity changes, including stronger warming in select land regions.
- Suggests meaningful distribution-shape change beyond mean warming.
Paper use:
- Direct comparison panel with T50 in projection results.

## 7) CMIP6 MMM annual ratio map (dT95/dT50)
Figure: /project/amp/miyawaki/plots/p004/cmip6/ann/fut-his/ssp245/mmm/ratioT50_t95.ssp245.ann.pdf
Interpretation:
- Clear amplified and suppressed regions, broadly echoing heterogeneity seen in ERA5.
- Distinct high-latitude and continental structures imply robust large-scale organization.
Paper use:
- Key bridge figure connecting observed and projected distributional change patterns.

## 8) CESM2-SF JJA GHG ratio map
Figure: /project/amp/miyawaki/plots/p004/cesm2-sf/jja/fut-his/ghg/ratioT50_t95.ghg.jja.pdf
Interpretation:
- GHG forcing shows coherent regions of amplification and suppression, including strong high-latitude signatures.
- Indicates that forcing-specific fingerprints can alter tail-vs-median response patterns.
Paper use:
- Attribution panel showing how greenhouse gas forcing shapes amplification geography.

## 9) CESM2-SF JJA AAER ratio map
Figure: /project/amp/miyawaki/plots/p004/cesm2-sf/jja/fut-his/aaer/ratioT50_t95.aaer.jja.pdf
Interpretation:
- Aerosol-related pattern is patchier and regionally contrasting relative to GHG case.
- Suggests aerosol forcing may modulate or counteract amplification in specific regions.
Paper use:
- Paired with GHG map to support forcing attribution narrative.

## 10) Regional process-space scatter (SWUS example)
Figure: /project/amp/miyawaki/plots/p004/cmip6/sc/historical+ssp370/CESM2/hfls+mrsos/regions/pct/swus/hfls+mrsos_1980-2000+gwl2.0.sc.swus.7.pct.bc.png
Interpretation:
- Historical and future clouds/curves shift in both soil moisture anomaly and latent heat dimensions.
- Visual evidence of state-dependent coupling behavior across temperature percentiles.
Paper use:
- Mechanistic panel supporting why tail amplification varies by region/hydroclimate state.

## 11) Process summary curve (all-region style)
Figure: /project/amp/miyawaki/plots/p004/cmip6/sc/historical+ssp370/CESM2/bc/bc.500.spagh.png
Interpretation:
- Curve shape suggests regime-like transitions in LH response with drying/wetting states.
- Spread among faint lines indicates regional variability around a shared nonlinear structure.
Paper use:
- Candidate overview panel for process behavior before region-specific examples.

## 12) Regional spagh examples (SA, SEA, SHL)
Figures:
- /project/amp/miyawaki/plots/p004/cmip6/sc/historical+ssp370/CESM2/bc/bc.spagh.sa.png
- /project/amp/miyawaki/plots/p004/cmip6/sc/historical+ssp370/CESM2/bc/bc.spagh.sea.png
- /project/amp/miyawaki/plots/p004/cmip6/sc/historical+ssp370/CESM2/bc/bc.spagh.shl.png
Interpretation:
- Different regions show distinct curve geometry and end-state behavior.
- Supports the argument that coupling and amplification responses are regime and region dependent.
Paper use:
- Select 2-3 contrast regions for a compact mechanism figure.

## 13) Hydroclimate regime classification map (CERES+GPCP)
Figure: /project/amp/miyawaki/plots/p004/ceres+gpcp/jja/hr/clima.2000-2022.jja.pdf
Interpretation:
- Land regions are cleanly partitioned into multiple hydroclimate classes (CH, TH, H, SH, SA, A, HA).
- Useful for objectively grouping regional mechanisms and comparing amplification behavior by regime.
Paper use:
- Context figure or supplementary anchor for regime-based interpretation.

## 14) Aridity proxy map (Rnet/LP)
Figure: /project/amp/miyawaki/plots/p004/ceres+gpcp/jja/ai1/clima.2000-2022.jja.pdf
Interpretation:
- Provides continuous hydroclimate background underlying the discrete regime classes.
- Shows physically interpretable gradients from humid to arid zones across continents.
Paper use:
- Optional support for regime definition and process interpretation.

## 15) GPCP high-percentile precipitation map
Figure: /project/amp/miyawaki/plots/p004/gpcp/jja/pr/clima_p95.jja.pdf
Interpretation:
- Strong tropical and monsoonal maxima; useful hydroclimate context for regions with strong tail behavior.
Paper use:
- Supplementary context panel for precipitation intensity background.

## 16) GPCP width-like diagnostic (P95 - P50)
Figure: /project/amp/miyawaki/plots/p004/gpcp/jja/pr/diffP50_clima_p95.jja.pdf
Interpretation:
- Highlights where precipitation distribution upper-tail spread is largest.
- Potential analog framing to temperature-distribution width/shape diagnostics.
Paper use:
- Could be used carefully as cross-variable context, likely supplementary unless tightly integrated.

## cross-cutting takeaways from this audit
- The strongest paper axis is not "does warming happen" but "how distribution shape changes vary by region and forcing".
- Ratio and difference diagnostics are both useful: ratio emphasizes relative amplification, difference emphasizes physical magnitude.
- Mechanistic process figures are compelling but currently stylistically inconsistent; publication-quality panel harmonization will be important.
