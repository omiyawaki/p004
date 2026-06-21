# Byrne (2021) methodology digest — "Amplified warming of extreme temperatures over tropical land"

Citation: Byrne, M. P. (2021), *Nature Geoscience* 14, 837–841. doi:10.1038/s41561-021-00828-8.
glean: `Byrne2021Amplified`. (NB: this is the foundational paper — it is **2021**, not 2022; no
separate 2022 hot-extremes theory paper exists in the library.)
Read 2026-06-21. Purpose: understand the theory before implementing the gridpoint/extratropical test.

## 1. Core idea
Over tropical land, **active convection couples near-surface moist static energy (MSE) to
free-tropospheric temperature**, and the **weak temperature gradient (WTG)** approximation makes
free-tropospheric temperature ~horizontally uniform across the tropics. Together these constrain
near-surface MSE changes to be ~uniform across the tropics and therefore **equal over land and ocean**.
Hot land days are *dry* (low q). Because `h = c_p·T + L_v·q`, on dry days the humidity term is small, so
to keep land MSE changes tied to ocean MSE changes (which are set by ocean warming at ~constant ocean
RH), **temperature must rise more on dry/hot days** → amplified hot-day warming. This is the
**"drier get hotter"** mechanism.

## 2. Key quantities
- `h = c_p·T + L_v·q`  (near-surface MSE)  [eq 1]; `c_p=1004.6 J/kg/K`, `L_v=2.5e6 J/kg`.
- `δ` = change between historical (1980–2000) and ssp245 (2080–2100).
- `x` = temperature percentile; quantities with superscript `x` are averaged over days exceeding the
  `x`th percentile of daily-mean near-surface T.
- `T_L^x`, `q_L^x` = land T and specific humidity averaged over land days above the `x`th T percentile.
- `p^x` = the **land MSE percentile** whose value equals the average MSE of days above the `x`th T
  percentile, i.e. `h_L(p^x) = h_L^x` (historical). This is the matching index that links land hot days
  to the ocean reference.
- Pseudo relative humidities: land `r_L^x = q_L^x / q_{L,sat}^x`; ocean `r_O = q_O(p^x)/q_{O,sat}(p^x)`.
  Saturation specific humidities via Bolton (1980). `α` = Clausius–Clapeyron parameter (fractional
  change of `q_sat` per 1 K): `α_L`, `α_O`.

## 3. Derivation (Methods)
**Load-bearing assumption** — equal MSE-percentile changes over land and ocean (from convection+WTG):

    δh_L(p) = δh_O(p)                                            [eq 2 / eq 7]

Change in land MSE of hot days:

    δh_L^x = c_p·δT_L^x + L_v·δq_L^x                             [eq 8]

Using eq 7 and the percentile-matching `p^x`:

    δh_L^x = δh_O(p^x) + Δh                                       [eq 9]
    Δh = h_L^ssp245(p^x + δp^x) − h_L^ssp245(p^x)

`Δh` accounts for hot land days shifting to a **lower** MSE percentile as climate warms (`δp^x < 0`,
Ext Data Figs 1 & 3a) ⇒ **`Δh < 0`**, which *tempers* the warming. Ocean side:

    δh_O(p^x) ≈ c_p·δT_O(p^x) + L_v·δq_O(p^x)                    [eq 10]

Write `δq` via T and pseudo-RH changes (Clausius–Clapeyron):

    δq_L^x = q_{L,sat}^x·δr_L^x + α_L·r_L^x·δT_L^x + α_L·q_{L,sat}^x·δr_L^x·δT_L^x   [eq 12]
    δq_O   = q_{O,sat}·δr_O + α_O·q_O·δT_O                       [eq 13]  (ocean nonlinear term dropped)

Combine (eqs 11–14) → land hot-day temperature response:

    δT_L^x = 1/(1+ε·δr_L^x) · [ γ^{T_O}·δT_O + γ^{r_O}·δr_O − (ε/α_L)·δr_L^x
                                + (1/(c_p+L_v·α_L·q_L^x))·Δh ]    [eq 14]
    ε      = L_v·α_L·q_{L,sat}^x / (c_p + L_v·α_L·q_L^x)
    γ^{T_O} = (c_p + L_v·α_O·q_O) / (c_p + L_v·α_L·q_L^x)         [eq 15]  (sensitivity to ocean T)
    γ^{r_O} = L_v·q_{O,sat} / (c_p + L_v·α_L·q_L^x)              [eq 16]  (sensitivity to ocean RH)

`Δh` is closed as a function of land T and land-RH change (Taylor expansion, eqs 17–24):

    Δh ≈ L_v·( δr_L^x·q_{L,sat}^x − δr̄_L·q̄_{L,sat} )            [eq 24]   (bar = mean-land-day value)

giving the **final theory** with four physically-named components:

    δT_L^x = 1/(1+ε·δr_L^x) · [ γ^{T_O}·δT_O   (δT_O comp: ocean warming)
                              + γ^{r_O}·δr_O   (δr_O comp: ocean RH)
                              + (ε/α_L)·(δr_L^x − δr̄_L·q̄_{L,sat}/q_{L,sat}^x) ]  (Δh comp)
             − 1/(1+ε·δr_L^x)·(ε/α_L)·δr_L^x                     (δr_L comp: land RH)   [eq 25]

**Fixed-RH simplification** (set all `δr = 0`):

    δT_{L,fixRH}^x = γ^{T_O}·δT_O                                 [eq 6]

This *alone* qualitatively reproduces amplification, because **`γ^{T_O}` rises with percentile**
(~1.19 at low `x` → ~1.43 at the 99th; Ext Data Fig 4a): hotter/drier days are more sensitive to ocean
warming. The `Δh` + `δr_L` terms combine into a total land-RH component (eqs 26–27).

## 4. Headline results
- Hottest 5% of land days warm **1.21 ± 0.07×** the mean day; ocean only **1.02 ± 0.04×** (Fig 2b).
- Higher percentile → larger amplification (monotonic).
- Theory vs simulated `δT_L^x`: **r = 0.98**; scaling factor `δT_L^x/δT̄_L`: r = 0.66 (Ext Data Fig 5).
- Fixed-RH (eq 6) explains ~20% of inter-model variance in hot-day warming (the climatological land–ocean
  q contrast).
- Land-RH decline (`δr_L < 0`) adds **+0.38 ± 0.22 K** (mean across percentiles) and its component
  correlates r = 0.93 with simulated hot-day warming ⇒ **RH changes drive the inter-model spread**.

## 5. Data & numerical method
- 18 CMIP6 models; daily-mean near-surface **T and q over BOTH land and ocean**; historical 1980–2000
  vs ssp245 2080–2100.
- Percentiles computed **per latitude**, aggregating over time **and longitude**; then area-weighted
  mean **20°S–20°N**. Land/ocean done separately. (Ext: 26 percentiles 0th–99th, spline-interpolated.)
- **Byrne already checked gridpoint percentile computation** (aggregate over time only, then spatially
  average) and got similar results (Supplementary Fig 6) — so the *percentile diagnostic* is robust
  pointwise; what remains tropical-aggregate is the **theory's ocean coupling**.

## 6. Assumptions — and exactly where they break (this is our opening)
The whole theory rests on **eq 7: `δh_L(p) = δh_O(p)`**, which requires:
1. Active convection coupling the land near-surface to the free troposphere, and
2. WTG making the free troposphere ~uniform so the ocean sets it (land MSE ≈ ocean MSE).

These hold in the **deep tropics** and fail moving poleward (WTG breaks; free troposphere has gradients
set by baroclinic dynamics/advection; boundary layer can be stable/decoupled, esp. winter). That is
**precisely** where this project already found you need the surface energy balance (summer
water-limited) and then advection + snow-melt (extratropical winter).

## 7. Implications for our extension
- **Novelty, sharpened:** gridpoint *percentile* computation is already validated by Byrne. The new
  contributions are (a) applying the **theory** (eqs 25/6) per gridpoint, and (b) extending **beyond
  20°S–20°N**. Both hinge on the ocean/free-troposphere reference.
- **Gridpoint application needs a free-troposphere reference per land point.** In the deep tropics
  (WTG) that reference is the tropical-mean (or zonal) ocean — Byrne's `δh_O(p^x)`. The clean
  generalization is to replace the *ocean MSE* proxy with the **local free-tropospheric temperature
  change** (e.g., T at 500 hPa or the level of neutral buoyancy), since the real physical content is
  surface↔free-troposphere convective coupling. In the tropics local FT ≈ ocean-set; in the
  extratropics it is dynamics-set and varies — so using local FT generalizes the same thermodynamic
  structure.
- **The test → a map of where the convective-thermodynamic theory suffices.** Predicted vs simulated
  `δT_L^x` per gridpoint/season; skill should be high in the convectively-coupled tropics and degrade
  where eq 7 fails. The breakdown map is itself the Layer-0 result, and it tells us where to add
  Layer 1 (SEB/Penman–Monteith) and Layer 2 (advection + snow).
- **Scenario note:** Byrne used ssp245, 2080–2100. Our products use ssp370 at GWL2.0. The theory is
  scenario-independent in form; decide whether to replicate ssp245/2080–2100 for a clean benchmark or
  apply at GWL2.0.

## 8. Inputs to confirm we have (or can compute) per gridpoint
- daily-mean `tas`, `huss` (→ q), over land AND ocean, hist + future. (We have land `tas`/`huss`; need
  the **ocean** counterparts and a free-troposphere temperature, e.g. `ta500`.)
- saturation specific humidity `q_sat(T, p_surface)` via Bolton (1980); Clausius–Clapeyron `α(T)`.
- the percentile-matching machinery for `p^x` (find land MSE percentile whose value = mean MSE of
  days above the `x`th T percentile), then evaluate the reference (ocean / local FT) at `p^x`.

## 9. Open questions before implementation
1. Free-troposphere reference for the gridpoint/extratropical generalization: tropical-mean ocean vs
   zonal ocean vs **local FT temperature** (recommended) — decide and justify physically.
2. Do we reproduce Byrne's tropical-aggregate result first as a validation (sanity check our pipeline
   against r = 0.98 / 1.21×) before going gridpoint/global? (Recommended.)
3. Which warming framing (ssp245/2080–2100 vs GWL2.0).
