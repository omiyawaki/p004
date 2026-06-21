# p004 — Physical / first-principles direction (working notes)

Date started: 2026-06-21
Status: living direction document. Supersedes the "tune the Budyko fit" framing. Build on this.

## 1. Motivation — move from empirical fit toward grounded structure

Audit verdict (see `notes/audit/bc_framework_audit.md`): the Budyko-curve (BC) offset is
**structural, not a bug**. The all-day, soil-moisture-only curve is the intended design (amplification
is `ΔδLH = ΔLH_hot − ΔLH_mean`, so one general curve must predict both hot and mean days), and its
explanatory ceiling is real — the residual is the share of amplification a general SM-only model
cannot reproduce.

Osamu's methodological concern (the reason the project dragged): the BC approach leans empirical. The
two-regime shape is grounded only at the limits; the body is parameterized.
- **Saturation / flat regime — grounded.** Energy/demand-limited: once soil is wet enough that supply
  is not the bottleneck, LH proceeds at the potential rate set by available energy and atmospheric
  demand, so more soil water does not change LH → flat in `θ`. Caveat: "flat in `θ`" still hides
  day-to-day variation in potential evaporation (Rn, VPD, wind) → that real demand variability becomes
  vertical scatter around the flat line.
- **Dry-regime linearity — NOT first-principles.** It is essentially the Manabe (1969) bucket model
  `β = min(1, θ/θ_crit)`. The bulk aerodynamic formula `E_pot = ρ·C_E·U·(q*(T_s) − q_a)` contains
  **no soil moisture at all** — it is the demand/transport side. Soil moisture enters only via `β` or a
  surface resistance `r_s(θ)`, and the *form* of that down-regulation is the parameterized part. Soil
  physics gives a strongly nonlinear supply limitation (hydraulic conductivity `K(θ) ∝ θ^(2b+3)`,
  Campbell; van Genuchten similar), so a *linear* dry branch is a bulk approximation, not a law.
- `θ_crit` (the water→energy transition) is physically meaningful even though the piecewise shape is not.
- **Name clarification.** The *classical* Budyko curve (long-term `E/P` vs `Ep/P`) is asymptotically
  grounded (`E ≤ P`, `E ≤ Ep`), with only the interpolation parameterized (Fu / Mezentsev one-parameter
  forms). The *daily* LH-vs-SM object fit here borrows the name but is a more empirical creature.

## 2. A more grounded surface-energy-balance (SEB) framing  — expansion layer

Lead with the perturbation surface energy balance on a hot day rather than an LH–SM curve:

    δRn = δH + δLH + δG

Close δLH with Penman–Monteith:

    LH = [ Δ·A + ρ·c_p·D / r_a ] / [ Δ + γ·(1 + r_s/r_a) ],   A = Rn − G,  D = VPD,  r_a ∝ 1/U

Amplification statement: `δT_s ≈ δF / λ_s`, where `λ_s` is the total surface restoring
(sensible `≈ ρc_p/r_a`, radiative `≈ 4εσT_s³`, and the **evaporative feedback** `dLH/dT_s`). Under
water limitation (large `r_s`) the evaporative feedback collapses → `λ_s` shrinks → the same energy
anomaly produces a larger `δT_s` → **amplified hot-day warming = failure of evaporative cooling to keep
up.**

Epistemic upgrade over "add VPD/wind as predictors": here VPD, Rn, and wind appear because the energy
balance *requires* them, not because they improve R². The empiricism collapses to one
physically-interpretable function `r_s(θ)` (boundable/groundable further with soil hydraulics). This
also reframes the BC offset: the residual = the omitted SEB terms (VPD / aerodynamic / energy), which
are nameable and individually testable rather than "stuff orthogonal to SM."

## 3. Proposed research arc — start from Byrne, expand where it breaks

Rationale: the project originated from Byrne. His theory is more first-principles
(convective-thermodynamic), picks up recent literature, but was derived for a **tropical-land spatial
aggregate** and applied only to the tropics. Test it **grid-point-wise** and **beyond the tropics**;
expand the hypothesis where it fails.

**Layer 0 — thermodynamic baseline (Byrne).** Land hot-day near-surface temperature is convectively
coupled to the free troposphere (set by tropical-ocean warming, moist-adiabatic), modified by the
decline in land near-surface relative humidity; the RH decline amplifies hot-day warming.
*(Exact governing equations + assumptions + required inputs to be pulled from the paper before building
the test — see §4. Do not build on recollection.)*
- Test: apply Byrne's predicted `ΔδT` gridpoint-wise across CMIP6 and compare to simulated `ΔδT`
  (we already have the percentile-warming products: `warming_t50`, `warming_t95`, the `ΔδT` maps).
  Per gridpoint, per season: predicted vs simulated, skill maps.
- Expectation: works in the tropics / WTG / convectively-coupled regions; breaks where BL–FT convective
  coupling fails (extratropics, baroclinic/advective regions, winter). The **breakdown map is itself a
  result.**
- Caveats: theory is locally formulated, so pointwise application is legitimate but noisier than the
  aggregate; the free-tropospheric reference is inherently non-local — confirm input availability.

**Layer 1 — SEB / Penman–Monteith correction (water-limited surface).** Where Byrne under-predicts in
summer / water-limited regions, add the evaporative-feedback term (§2). This is where the current
project's SM↔LH work plugs in — now as a *physically-motivated correction to a thermodynamic baseline*,
not a standalone empirical fit.

**Layer 2 — extratropical winter.** Temperature advection / atmospheric energy-flux divergence +
snow/ice-melt near freezing. Already partly established in the project: snow-melt explains the
freezing-point suppression (solid); advection was the leading-but-unclosed explanation for the rest
(see `notes/meetings_summary.md`).

Why this ordering is good: starts from a published first-principles baseline (clear literature
positioning + a definite test); each layer is added only where the simpler one fails (parsimonious,
interpretable); failure maps are results; replaces "fit a curve" with "test a theory, then add physics
where it is insufficient."

## 4. Immediate next steps

1. **Retrieve Byrne** (the foundational one I know is Byrne 2021, *Nature Geoscience*, "Amplified
   warming of extreme temperatures over tropical land"; confirm whether Osamu means a specific 2022
   paper / follow-up). Extract: exact governing equation(s), assumptions, and the list of required
   input variables. Likely already in the `glean` library.
2. **Inventory inputs** vs what we already have as products (T percentiles ✓; near-surface q / RH;
   free-tropospheric T e.g. T500 / moist-adiabat reference; ocean / tropical-mean warming reference).
3. **Draft the gridpoint test methodology** (predicted vs simulated `ΔδT` per gridpoint/season; skill maps;
   tropics-first then global).
4. **Derive the perturbation-SEB amplification expression** explicitly (the `dLH/dT_s` term and which
   part of the BC offset it corresponds to) for Layer 1.

## Cross-references
- `notes/audit/bc_framework_audit.md` — audit verdict (offset structural; keep all-day curve; residual meaningful).
- `notes/meetings_summary.md` — existing extratropical findings (snow solid; advection unclosed).
- `paper/outline_meetings.md` — Introduction already positions against Byrne (2021), Duan et al., Hsu & Dirmeyer.
