# Duan, McKinnon & Simpson (2024) methodology digest — "Two Perspectives on Amplified Warming over Tropical Land"

Citation: Duan, S. Q., McKinnon, K. A., Simpson, I. R. (2024), *J. Climate* 37, 4743–4755.
doi:10.1175/JCLI-D-22-0955.1. glean: `Duan2024Two`. **McKinnon & Simpson are p004 coauthors.**
Read in full 2026-06-21. Purpose: is there a simple *predictive* land-surface model? (No — see §5.)

## 1. Goal
Compare the two existing explanations of amplified warming over *dry* tropical land:
- **Atmospheric-dynamics perspective** (QE–WTG; Joshi 2013; Byrne & O'Gorman 2013/2018; Byrne 2021):
  free-tropospheric T uniform (WTG), surface connected via a lapse rate closer to dry adiabat over dry
  land ⇒ drier land warms more. Constrains near-surface **MSE** changes ~equal over land/ocean.
- **Surface-flux perspective** (Berg, Donat, Vogel, Duan 2020, Dirmeyer; process-based, local SEB):
  drier soil ⇒ less LH, more SH, hotter near-surface; the **Bowen ratio** controls warming.

## 2. The unified diagnostic framework (their core contribution)
Both perspectives partition a total energy/flux into a temperature part and a humidity part:
- Surface: `Rn − G = SH + LH`; Bowen ratio `B = SH/LH`; `Rn ≈ Ψ·SH`, `Ψ = (B+1)/B = Rn/SH`.  [eq 1]
- Atmospheric: `ME = c_pT + L_vq` (MSE − gz); `b = c_pT/(L_vq)`; `ME = ψ·c_pT`, `ψ = (b+1)/b`.  [eq 2]

Linearize (drop nonlinear cross terms), with `ΔSH = κΔT` (κ ≈ const):
- `ΔMSE ≈ ψ·c_p·ΔT + c_p·T·Δψ`   [eq 3]      →  **`ΔT = (ΔMSE − c_p T Δψ)/(c_p ψ)`**  [eq 6, atmos]
- `ΔRn  ≈ Ψ·κ·ΔT + SH·ΔΨ`        [eq 5]      →  **`ΔT = (ΔRn − SH ΔΨ)/(κ Ψ)`**       [eq 7, surface]

Three pieces of each (Table 1): (i) a **forcing analog** (ΔMSE or ΔRn = change in total energy/flux);
(ii) a **base-climate sensitivity** = inverse partition factor (`1/(c_pψ)` atmos, `1/(κΨ)` surface) —
drier base climate → higher sensitivity → more warming; (iii) a **repartition term** (`−c_pTΔψ` or
`−SHΔΨ`) = change in the partitioning under warming.

## 3. Key result
Across a daily-SM-percentile (temporal) × climatological-aridity-index (spatial) phase space, the
**base-climate sensitivity alone largely explains the warming pattern** (drier → more warming; the
two perspectives' sensitivities correlate r=0.99). The **repartition term** adds the extra
enhancement/damping at **intermediate (transitional) wet↔dry conditions** — where SH/LH repartitioning
(surface) and moistening (atmos) matter most. They link the two views mechanistically via the
lower-tropospheric lapse rate ↔ surface-flux (SH/R) relationship (§5, Fig 6).

## 4. Scope / data (important for our positioning)
- **abrupt 4×CO2** (yrs 121–150) vs historical control (1850–79); only **9 CMIP6 models** that report
  daily SM + surface/radiative fluxes in 4×CO2.
- **Warm season only:** 150 days centered on 15 Jul (NH) / 16 Jan (SH). **Tropical land 30°S–30°N.**
- Analysis is in the **SM×AI dryness phase space**, NOT a seasonal-cycle analysis. So: they restrict to
  the warm season and characterize warming vs *dryness* (spatial + daily-temporal), but **do not
  examine the seasonal cycle** of amplification, and **do not go beyond the tropics**.

## 5. PREDICTIVE vs DIAGNOSTIC — the crux for our project
- **The model is explicitly DIAGNOSTIC.** Summary §6: *"The linearized perturbation model we derive is
  diagnostic … instead of making predictions."* Eqs 6/7 need the *future* ΔMSE/ΔRn and the
  partition-factor change (Δψ/ΔΨ) as inputs from model output — it attributes warming, it does not
  forward-predict it from base-climate-only inputs.
- **Asymmetry (answers Osamu's question):** the **atmospheric side HAS a predictive constraint** —
  Byrne's "ocean-influence model": `ΔT^L = ΔT^O + (1−γ)(L_v/c_p)Δq^O`, `γ = q^L/q^O` (base-climate
  land/ocean humidity ratio) [their eq 8]. The **land/surface side here is a decomposition, with NO
  closed predictive model.**
- **Precedented simple PREDICTIVE land models** exist but are not tested as predictors of amplification:
  - **Surface Flux Equilibrium (SFE)** (McColl et al. 2019; McColl & Rigden 2020): `RH = c_p/(L_v φ B)`,
    `φ = ∂q*/∂T` [their eq 9] — predicts boundary-layer RH from the Bowen ratio (assumes BL heat/moisture
    budgets dominated by surface fluxes at ≥ daily scale).
  - **Idealized Budyko curve** `LH = f(SM)` — what this project has used (precedented but, per our audit,
    SM-only + empirical; the offset is structural).

## 6. Implications for our novelty (sharpened)
Two clean openings, both consistent with Osamu's "test the limits of simple models":
1. **Seasonality is still untested.** Duan et al. use warm-season days in a dryness phase space, not the
   seasonal cycle; Byrne is annual. Whether any of these models explains the **seasonal cycle** of
   amplified hot-day warming is open.
2. **No simple *predictive* land model has been tested for amplification.** Byrne (atmospheric) is a
   tested simple predictive model (annual, tropics); the land side has only diagnostic decompositions
   (Duan) or candidate simple predictors (SFE, idealized BC) that have NOT been tested as predictors of
   the seasonal cycle of amplification.

**Framing:** there is a spectrum — full GCM → diagnostic decomposition (Duan 2024) → simple *predictive*
models (Byrne atmospheric; SFE / idealized BC land). The contribution is to **test how far the simple
*predictive* models go in capturing the SEASONAL CYCLE of amplified hot-day warming, gridpoint and
globally**, and map where they hold vs break (tropics/convective-season → succeed; extratropics/winter →
fail, where Layer 2 advection+snow enters). The failure boundaries are the science.

## 7. Cross-refs
- `notes/byrne2021_methodology.md` — the atmospheric predictive model (the thing to test seasonally).
- `notes/theory_direction.md` — layered plan + novelty check.
- Adjacent coauthor work: `Duan2023Coherent` (the SM/AI phase space), `Duan2025Impact` (soil
  preconditioning of heatwaves).
