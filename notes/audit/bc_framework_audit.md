# BC-framework correctness audit — Phase 1 (INCOMPLETE)

Date: 2026-06-19
Scope: the canonical Budyko-curve (BC) latent-heat decomposition chain that produces the
plotted `ddpc.ooplh*` products (figures `cmip6/plot/spcc/decomp.{dbc,dsm}.mmm.lh.py`).
Method: static read-only audit (data/plots are remote; nothing was run).
Status: **incomplete** — the multi-agent workflow was cut off mid-run by the monthly
API spend limit. Treat this as a partial result, not a clean bill of health.

## Why this is incomplete (read before trusting any "0 bugs" impression)

The workflow reported `confirmed: 0 / refuted: 40`. That headline is an **artifact of the
spend-limit failure**, not a finding:
- The Trace phase completed.
- ~17 per-file audit agents ran and raised **40 candidate findings**.
- Then the monthly spend limit was hit. **Every verification agent, all four
  cross-cutting checks (algebra-closure, variant-diff, units-signs, fit-correctness),
  and the synthesis step failed.** The verdict logic counted "no votes received" as
  "refuted", so all 40 candidates were mislabeled refuted.
- Net: the 40 candidates are **unverified and parked** (recoverable from the workflow
  agent transcripts). The two cross-cutting checks most likely to bear on the offset —
  **algebra-closure** and **fit-correctness** — never ran.

## Confirmed finding (verified by direct reading, not the workflow)

### F1 — `mmm.p.cond.dsm.py`: undefined `csm1`/`csm2` in the climatology-anomaly step
- File: `cmip6/data/mmm/mmm.p.cond.dsm.py` (the MMM aggregator that writes the plotted
  `ddpc.<var>_1980-2000_gwl2.0.sc.nc` products).
- Lines 56, 58: climatology loaded into `cvn1` / `cvn2`.
- Lines 96–99: anomalies computed as `mvn1-csm1`, `mvn2-csm2`, `pvn1-csm1`, `pvn2-csm2`,
  but `csm1` / `csm2` are **never assigned anywhere in the file** (confirmed by grep).
  The sibling `cmip6/data/mmm/mmm.anom.p.cond.py` does the same step consistently
  (loads into `csm1`/`csm2`, subtracts `csm1`/`csm2`).
- Also: `idir0` (the dedicated csm directory, line 47) is defined but unused; csm is
  instead read from `idir1` (the varn0 data dir, line 55).
- Provenance: both blocks originate in commit `3ea2e29` (2024-03-06); single-commit file.

**Impact (my own analysis — the part the killed verification stage would have done):**
- As written the references are undefined → either a `NameError` on a clean run, or
  silent use of a stale `csm1`/`csm2` leaked as a global from a prior script in the same
  interpreter session.
- **For the plotted Δδ (`ddpc`) decomposition, csm cancels algebraically:**
  `ddpvn = dpvn − dvn = (pc2−pc1) − (m2−m1)`; the `(csm2−csm1)` baseline cancels because
  the same csm is subtracted from both percentile and mean within each forcing. So this
  bug **most likely does NOT explain the Actual-vs-BC offset** — both the actual-LH and
  BC-LH Δδ products are equally insensitive to csm.
- It **does** matter for: (a) standalone reproducibility (the script can't run as
  committed); (b) any downstream use of the saved non-Δδ products (`dpc`, `d`, `pc`, `m`),
  which retain a non-cancelling — and here wrong/stale — csm baseline.
- Proposed fix (pending Osamu's confirmation of provenance — do NOT apply blind):
  rename `cvn1`/`cvn2` → `csm1`/`csm2` at lines 56–60 (and read csm from `idir0`, not
  `idir1`), matching `mmm.anom.p.cond.py`. First confirm whether the current figures were
  actually produced by this script vs. an earlier/leaked-global state.

### F2 — decomposition plot scripts: dead `int == str` branch (cosmetic)
- Files: `cmip6/plot/spcc/decomp.dbc.mmm.lh.py:129`, `decomp.dsm.mmm.lh.py:129`.
- `if m==6 and v=='ooplh_rbcsm':` (resp. `'ooplh_rddsm'`) compares the integer loop index
  `v` (0–3, from `range(4)`) to a string → always False, so the intended month-7 contour
  special-casing never executes. Plus a redundant in-loop `savefig` and an inconsistent
  `/project/amp02` vs `/project/amp` mount. Cosmetic (plotting only); no numeric impact.

## Genuinely useful completed output: canonical-vs-off-path map

The Trace phase cleanly separated the **17-file canonical chain** from **69 off-path
files** — this tames the ~150-file variant sprawl. The canonical decomposition is, per
forcing: raw model fields → `rg.p.cond.py`/`rg.p.py`/`rg.m.py` (per-gpi hot-day percentile
& mean) → `mk.bc.dsm.py` (per-model Budyko curve) + `rgr.lh.sm.wgtlogi.one.py` (weighted
logistic LH–SM fit) → `mk.oo.plh{,.fixbc,.dbc,.fixmsm,.rddsm,.rbcsm}.py` (the 6
reconstruction terms) → `mk.csm.py` → `mmm.p.cond.dsm.py` (Δδ + MMM) → `decomp.*.mmm.lh.py`.

Off-path families (safe to ignore when auditing the plotted decomposition):
- `old/` dirs, `*.test.py`, `*.TEMP.py`, `*.BACKUP.py`, `mk.bc.py.old` — superseded/scratch.
- `pef/` — the evaporative-fraction analogue of the whole pipeline (feeds the separate
  `oopef` figures, not the LH decomposition).
- depth-sweep family: `*plhx*`, `*bcx*`, `*mlhx*` (multi-soil-layer, not surface mrsos).
- mean-day-LH family: `mk.oo.mlh*`, `mk.oo.mdlh*` (vs the `plh` hot-day family).
- `*qcesm*` — alternate (CESM-quantile) percentile basis.
- pooled-MMM-curve family: `mk.mmm.bc*`, `mk.oo.plh.mmmbc/mmmsm` (canonical uses per-model
  curves).
- alternative decomposition terms not plotted by these two figures: `mk.oo.plh.{mtr,rdbc,
  rnl,fixasm,msm,orig}`.
- alternative MMM aggregators: `mmm.p.cond.md.py` (median baseline → `ddpc.md.*`),
  `mmm.anom.p.cond.py` (→ `anom.ddpc.*`), `mmm.p.cond.convtas*` (tas-converted).
- legacy gridded percentile route: `cmip6/data/percentile/pct_*.py`.
- single-location fit prototypes: `regress/rgr.{ef,tas,cpe,cpr}.sm.wgtlogi.one.py`.

(Full 69-entry list with per-file reasons is in the workflow output:
`tasks/w8v3phg4h.output`.)

## Chunk plan & progress (incremental, done by hand in the main loop)

The mega-workflow blew the monthly budget in one phase. Switched to small inline chunks.

- [x] **Chunk 1 — LH–SM curve fit** (`mk.bc.dsm.py`, `rgr.lh.sm.wgtlogi.one.py`) — see F3/F4 below.
- [x] **Chunk 2 — curve evaluation → `ooplh`** (`mk.oo.plh.py`): F5 confirmed; F10 (np.interp clamping).
- [x] **Chunk 3 — decomposition algebra** (`mk.oo.plh.{fixbc,dbc,fixmsm,rddsm,rbcsm}.py`): terms partition EXACTLY (closure passes).
- [x] **Chunk 4 — inputs** (`rg.p.cond.py`, `rg.p.py`, `rg.m.py`, `mk.csm.py`): percentile/composite CLEAN; `mk.csm.py` → F12.
- [x] **Chunk 5 — aggregation** (`mmm.p.cond.dsm.py`): F1 (csm cancels in Δδ); chain understood end-to-end.
- [x] **Chunk 6 — conventions + figures** (`util.py` clean; `decomp.*.mmm.lh.py` → F2).

**Phase 1 (BC crux) is COMPLETE — full canonical chain audited by hand. Verdict below.**
- [x] **External — `etregimes.bestfit`** (retrieved from Derecho 2026-06-20; see F5–F9): the segmented-regression fit engine — AUDITED.

## Chunk 1 findings (2026-06-20)

### F3 — the production Budyko-curve fit (`etregimes.bestfit`) is NOT in this repo [HIGH / scope-blocking]
- `mk.bc.dsm.py:17` does `from etregimes import bestfit`; the per-(month,gpi) curve is fit by
  `bestfit(nvn2, nvn1)` at line 84, returning the curve (`line`), the critical SM (`xc`→saved as
  `csm`), and the slope (`mt`→saved as `mtr`).
- `etregimes` lives in `/home/miyawaki/scripts/common` (not in the checkout); **60+ scripts** across
  `plh/`, `pef/`, `smbasis/` import `bestfit`. So the single most offset-relevant code — the fit form,
  the water/energy-limited breakpoint detection, the slope, and extrapolation behavior — **cannot be
  audited locally.** A bug in `bestfit` (e.g., wrong breakpoint, biased slope, bad extrapolation) would
  produce a systematic Actual-vs-BC offset and would be invisible from this repo.
- Other shared modules also absent (lesser blind spots): `glade_utils`, `cmip6util`, `util`, `utils`,
  `constants`, `regions`.
- **Action:** copy `etregimes.py` (and ideally the other `common/` modules) into the repo or share it,
  so `bestfit` can be audited. This is now the highest-priority next step for the offset question.

### F4 — `rgr.lh.sm.wgtlogi.one.py` is a broken, off-path prototype [LOW]
- It is a single hardcoded-location diagnostic (`iloc=[110,85]`), NOT the production fit (production =
  `etregimes.bestfit`). The tracer mis-listed it as canonical.
- It cannot run: `cl` is used at lines 54, 60, 61, 72 but never assigned → `NameError`.
- Ambiguous weighting: primary fit uses `sigma=pdf**(1/3)` (down-weights dense points); the fallback
  uses `sigma=pdf**(-1)` (opposite). Worth confirming intended direction IF this prototype is ever
  revived — but it is off the production path, so low priority.

### Chunk-1 notes (not bugs; confirm intent later)
- SM anomaly fed to the curve is `mrsos − mean(mrsos)` over the **annual** historical period
  (`mk.bc.dsm.py:67`), not the per-month climatology (the monthly version is commented out at line 66).
  Combined with per-month fitting, the SM seasonal cycle is retained in the "anomaly." Internally
  consistent across hist/future (future uses the historical annual mean), but a methodological choice.
- `csm` = critical soil moisture (the Budyko breakpoint `xc`), saved per (month, gpi). This is the same
  `csm` the aggregator subtracts (F1); subtracting a critical-SM from an LH field (`ooplh`) is
  dimensionally odd — revisit in Chunk 5 (recall it cancels in the plotted Δδ).
- Failed fits → `bc=None`, `csm/mtr=NaN` (`mk.bc.dsm.py:88-89`); check how `mk.oo.plh.py` handles
  `None` curves in Chunk 2.

## External fit-engine findings — `etregimes.bestfit` (2026-06-20)

Source: `derecho:/glade/u/home/miyawaki/scripts/common/etregimes.py` (16 KB, dated 2024-03-06;
"Based on Qin Kong's modified ET regime script, Hsu's method"). Snapshot pulled to `/tmp` for this
session; line numbers below are 1-based on the source. `mk.bc.dsm.py:84` calls
`f1,f2=bestfit(SM_anom, LH)` and keeps **`f2` = the BIC-selected** model (`bc=f2['line']`,
`csm=f2['xc']`, `mtr=f2['mt']`).

How it works: `bestfit` fits 9 candidate segmented-linear shapes (`fit1111…fit0001`) to the
(SM-anomaly, LH) points via `scipy.optimize.curve_fit`, then picks the min-AIC and min-BIC model.
Each shape yields a critical SM (`xc`, the water→energy transition) and a transitional slope (`mt`).

### F5 — the curve is fit UNWEIGHTED to ALL days of the month, not to hot days [HIGH — likely bears on the offset]
- `curve_fit` in every `fitNNNN` uses ordinary (unweighted) least squares; there is **no density or
  percentile weighting** anywhere in `bestfit`. `mk.bc.dsm.py:bcmon` feeds it *all* daily
  (SM-anom, LH) pairs for that month.
- The BC reconstruction (`ooplh`) then evaluates this all-day curve at the hot-day SM to predict
  hot-day LH (evaluation step to be confirmed in Chunk 2). So BC assumes the hot-day LH–SM relation
  is the same curve as the all-day relation. If the hot/dry tail departs from the bulk relation
  (hysteresis, VPD, depleted SM), BC will **systematically miss hot-day LH → a structural source of
  the Actual-vs-BC offset.** This is a framework-design limitation, not a coding bug, and is the
  leading candidate for "why BC under-explains." (Tellingly, the abandoned prototype
  `rgr.lh.sm.wgtlogi.one.py` *did* weight by density — weighting was considered and dropped.)
- Implication for the project decision: if confirmed, the offset is partly inherent to fitting an
  all-day curve. A hot-day-conditioned or density/tail-weighted fit is the natural "iterate" path
  before concluding the BC framework itself is inadequate.

### F6 — one failing sub-model discards the whole gridpoint [MEDIUM, robustness]
- `bestfit:399` fits all 9 shapes in a single list comprehension with no per-model try/except. If any
  one `curve_fit` raises (non-convergence, degenerate bounds), the exception propagates out of
  `bestfit`, and `mk.bc.dsm.py:88` catches it with a bare `except: bc.append(None)` — discarding the
  **entire** gridpoint's BC even when other shapes fit fine. This can systematically drop
  hard-to-fit (often dry/hot) gridpoints, biasing coverage of the BC maps. Fix: wrap each `runfit`
  so a single shape's failure is skipped, not fatal.

### F7 — `fit0110` mislabels its type as `'1100'` [COSMETIC]
- `etregimes.py:116` returns `'type':'1100'` inside `fit0110` (copy-paste). The `type` field is unused
  downstream (selection is by AIC/BIC; `mk.bc` reads only `xc`/`mt`/`line`), so no numeric impact —
  but it corrupts any per-shape bookkeeping/diagnostics keyed on `type`.

### F8 — the "x0<x1" breakpoint-ordering issue is only partly handled [LOW/EDGE]
- Header comment (line 8) flags it; 3- and 4-segment fits sort the node arrays before `np.interp`
  (`Xnew=...argsort`). But `curve_fit` can still return breakpoints out of order, in which case the
  AIC/BIC is computed on a sorted-node interpolation that differs from the actual fitted piecewise
  function. Affects a minority of gridpoints; worth a guard.

### F9 — outlier removal is disabled [LOW, confirm intent]
- `runfit:389` has `# sm,lf=remove_outlier(sm,lf)` commented out, so Kong's LH-jump>50 outlier filter
  never runs. May be deliberate; flag to confirm whether high-LH outliers should be trimmed before
  fitting.

**Net on the offset:** no single coding bug here forces the offset, but **F5 is a strong structural
explanation** — the BC curve is an all-day, unweighted fit applied to hot days. Confirm the
evaluation in Chunk 2, then this becomes the central "iterate the method" lever.

## Chunk 2 findings — `mk.oo.plh.py` (ooplh = BC_all) (2026-06-20)

### F5 CONFIRMED — BC reconstructs hot-day LH from the all-day curve at hot-day SM
- `eval_bc(sm,bc)=np.interp(sm,bc[0],bc[1])` (line 70-71); `calc_plh` loads hot-day percentile SM
  (`pc.mrsos`), de-means it (`sm-sm0.mean('time')`, line 94), and evaluates the per-(month,gpi)
  curve at it. So `ooplh = curve(hot-day SM)`. The curve is the all-day, unweighted fit (F5). The
  offset `Actual − ooplh` is whatever hot-day LH variation is **not a function of SM** — confirmed
  structural, as argued in F5.

### F10 — `np.interp` CLAMPS beyond the historical SM range (no extrapolation) [HIGH, offset-relevant]
- The curve nodes `bc[0]` span the *historical* all-day SM range (`SM.min()..SM.max()` from
  `mk.bc.dsm.py`). `np.interp` returns the endpoint value for inputs outside `[xp[0],xp[-1]]`.
- Under warming/drying, future hot-day SM anomaly often falls **below** the historical `SM.min()`,
  so BC **clamps** hot-day LH to the driest-historical value rather than continuing the curve down.
  This biases BC systematically in the dry/hot tail — precisely where the offset is largest. It is a
  defensible "don't extrapolate" choice, but it has real, asymmetric consequences for the future hot
  tail and is a concrete contributor to the Actual-vs-BC offset (distinct from, and on top of, F5).

## Chunk 3 findings — decomposition algebra (`fixbc/dbc/fixmsm/rddsm/rbcsm`) (2026-06-20)

### Algebra closure — PASSES (the prime offset suspect is cleared)
Verified each term's construction from the scripts, then summed by hand:
- `ooplh` (BC_all)       = `curve_fo(sm_fo)`              (run for hist and fut)
- `ooplh_fixbc` (BC_hist)= `curve_hist(sm_fut)`           (hist curve, future SM) — `get_bc(md,fo0,byr0)`
- `ooplh_dbc` (ΔBC)      = `curve_fut(sm_hist)`           (future curve, hist SM) — loads `mrsos(fo0)`
- `ooplh_rbcsm` (Resid)  = `2·lh0 + lhf − lhfbc − lhfsm`  (lhfsm here = `ooplh_dbc`)
Then **Δfixbc + Δdbc + Δrbcsm = curve_fut(sm_fut) − curve_hist(sm_hist) = Δooplh, exactly.** The
second figure's split (`fixmsm`/`rddsm`) likewise closes: `Δrddsm = Δfixbc − Δfixmsm` (the
hot-day-specific ΔδSM effect), with `fixmsm = curve_hist(sm_hist + Δmean_SM)`.
**Conclusion: the offset is not a decomposition-closure bug.** The terms are exact by construction
(`rbcsm` is literally defined as the interaction residual). The offset lives in `Actual − BC_all`.

### F11 — misleading variable name in `mk.oo.plh.rbcsm.py` [COSMETIC]
- Line 63 loads `ooplh_dbc` into a variable named `lhfsm` (suggesting "fixed sm"); the arithmetic is
  correct, but the name invites misreading. Rename to `lhdbc`.

## Chunk 4/5/6 spot-findings (2026-06-20)

### F12 — `mk.csm.py` fits on RAW soil moisture; `mk.bc.dsm.py` fits on the SM ANOMALY [MEDIUM, confirm]
- `mk.csm.py:70-73` has the SM-anomaly step **commented out**, so `bestfit` runs on raw `mrsos` and
  the saved critical SM (`csm=f2['xc']`) is in **raw-SM** units. `mk.bc.dsm.py` fits on `mrsos −
  mean` and its `xc` is in **anomaly** units. Two `csm` products in different coordinates. If the
  aggregator's `csm` subtraction (F1) ever used the raw-units one against anomaly-based fields, it
  would be inconsistent — though recall it cancels in the plotted Δδ (F1). Confirm which `csm`
  feeds which consumer.

### `util.py` — clean
- `mods('historical')` returns exactly the 15 models in the manuscript table (incl. CESM2
  `r11i1p1f1`, UKESM1-0-LL `r9i1p1f2` via `emem`). No correctness issue; only a duplicated docstring
  line in `simu` (cosmetic).

## Chunk 4 findings — inputs (`rg.p.py`, `rg.p.cond.py`, `rg.m.py`) — CLEAN (2026-06-20)
- `rg.p.py`: tas percentile thresholds via `np.nanpercentile` per month/gpi over the year window. Correct.
- `rg.p.cond.py`: the hot-day composite. tas-percentile edges `[0,5,…,95,100]` → 20 bin-center
  outputs `[2.5,…,97.5]`; `bin_below`/`bin_betwn`/`bin_above` fill all 20 bins with no off-by-one and
  no double-fill (checked the `ip==0` / `ip==len-1` branches). `pc.mrsos` = mean SM on days whose tas
  falls in each bin; the hottest bin (≥p95) is the hot-day SM that feeds BC. Correct.
- `rg.m.py`: monthly-mean climatology (`groupby('time.month').mean`). Correct (cosmetic typo
  "colldsect" line 19). Year window `>=byr[0]` & `<byr[1]` matches `rg.p.py`/`rg.p.cond.py` (so
  "1980-2000" = 1980–1999, applied consistently everywhere).
- **Net: the hot-day definition and the SM-on-hot-days composite are correct.** The offset is not an
  input/binning artifact.

---

## AUDIT VERDICT — Phase 1 / BC crux (2026-06-20)

**Question:** is the BC framework's weak explanatory power (the Actual-vs-BC `ΔδLH` offset) a genuine
limitation, or an implementation bug?

**Answer: it is NOT an implementation bug. The offset is structural, from two design choices in the
method itself.** Every load-bearing computational step is correct: the hot-day percentile/composite
inputs (Chunk 4), the per-(month,gpi) segmented fit engine `etregimes.bestfit` (sound; AIC/BIC form
correct), the curve evaluation (Chunk 2), and the decomposition algebra, which **closes exactly**
— `Δfixbc + Δdbc + Δrbcsm = Δooplh` by construction (Chunk 3). The one undefined-variable bug in the
aggregator (F1) cancels in the plotted Δδ.

**The two structural sources of the offset:**
1. **F5 — BC predicts LH from soil moisture alone, via a curve fit to ALL days unweighted.** Any
   hot-day LH signal orthogonal to SM (VPD, net radiation, SM-hysteresis on hot days) is
   unrepresentable. This is the explanatory-power ceiling.
2. **F10 — `np.interp` clamps beyond the historical SM range.** Future hot/dry days below the
   historical `SM.min()` get a flat (clamped) LH instead of an extrapolated one, biasing the future
   dry tail where the offset is largest.

**Real but non-causal bugs to fix (do not explain the offset):**
- **F6** [med]: in `bestfit`, one sub-model's non-convergence throws and `mk.bc.dsm.py`'s bare
  `except` discards the whole gridpoint (`bc=None`) → coverage gaps biased toward hard-to-fit
  dry/hot cells. Fix: per-model try/except.
- **F12** [med]: `mk.csm.py` fits raw SM, `mk.bc.dsm.py` fits SM-anomaly → two `csm` products in
  different coordinates; confirm which feeds which consumer.
- **F1** [low]: `mmm.p.cond.dsm.py` undefined `csm1`/`csm2` (cancels in Δδ; corrupts non-Δδ products).
- **F7/F11** [cosmetic]: `fit0110` mislabels `type='1100'`; `rbcsm` names the dbc term `lhfsm`.

**Decision support — rethink vs. iterate:** there is a concrete ITERATE path to try before concluding
the framework is inadequate:
1. Weight the fit toward the hot/dry tail, or fit a hot-day-conditioned curve (the abandoned
   `wgtlogi` prototype already weighted by density).
2. Replace the `np.interp` clamp with a controlled extrapolation in the water-limited regime (F10).
3. Fix F6 so dry/hot gridpoints are not silently dropped.
If a tail-weighted, properly-extrapolated SM-only curve still leaves a large offset, the limitation
is fundamental (hot-day LH is not a function of SM alone) → add a second predictor (VPD/Rn) or change
framework. That is the clean RETHINK signal.

## Phase 2 — ERA5 observational pipeline (Figure 1 benchmark) — CLEAN (2026-06-20)
Audited `era5/data/tseries/pct.py`, `tseries/trend.py`, `distribution/pct_t2m.py`. The
trend(T50)/trend(T95)/ratio chain is correct: per-year percentiles via `np.percentile` (linear interp,
matches CMIP6), then per-gridpoint OLS (`scipy.stats.linregress`) of each percentile vs. year.
- **E1** [low]: `pct.py:23` uses `lyr=list(set(vn['time.year']))` — arbitrary (hash) order. NOT a
  correctness bug because the `year` coordinate is stored alongside the data and `linregress` is
  order-independent, but fragile; prefer `sorted(set(...))`.
- **E2** [note]: DJF is grouped by calendar year (Dec(Y) with Jan/Feb(Y), not the meteorological
  winter). Standard simplification; affects only DJF/seasonal-spanning, not the JJA+annual main text.
- **E3** [dedup]: `distribution/pct_t2m.py` is a legacy gridded route writing to a different path
  (`hist_hotdays/era5`) than the `era5/ts/tas` consumed by `trend.py`; likely superseded by
  `tseries/pct.py`.

## Phase 2 — CESM2-SF forcing attribution (Figure 4) — CLEAN (2026-06-20)
Audited `cesm2-sf/data/climate_change/diff_hotdays.py`, `sfutil.py`. Per-member percentile warming
`dt2m = ht2m1 − ht2m0`, then correct ensemble stats (mean/median/IQR/range) per percentile. One file
per percentile (`diff_<pc>.pickle`); the ratio is formed in the plot layer. Notes (not bugs): the
`fut=='2000-2014'` branch loads both periods from the `his` directory because 2000-2014 is inside the
historical LENS run; `emem` gives 15 members for ghg/aaer, 50 for lens, 3 for xaaer; the triple-nested
ensemble loop is slow but correct.

### Phase 2 remaining (not yet audited)
cesm2-le, cesm2-cmip, gpcp (precip percentiles), the rest of `cmip6/data/` (other conditioned
variables, kde/smbasis/correlation), and all plot scripts (mostly visualization; main offset-relevant
plotting already covered via the decomp figures, F2).

## Phase 2 — CERES+GPCP hydroclimate regimes (Figure 5) — one bug (2026-06-20)
Audited `ceres+gpcp/data/masks/ai1_regimes.py`, `climatology/clmean_ai1.py`. Aridity-index time-mean
is correct; the 7-regime classification (Takeshima et al. 2020) partitions the AI axis cleanly with no
overlap/gap, and the `pr*86400` mm/d conversion is right.
- **G1** [low-med]: `ai1_regimes.py:30` `hr=np.empty_like(ai)` is uninitialized; NaN/ocean cells match
  none of the `np.where` regime masks, so they keep garbage values rather than NaN. Fix:
  `hr=np.full_like(ai, np.nan)`. Low impact if ocean is masked downstream, but a real latent bug.

## Coverage summary (2026-06-20)
Audited by hand, all main-figure pipelines:
- **Fig 1 (ERA5 obs trend):** clean (E1–E3 minor).
- **Fig 2 (CMIP6 warming/ratio):** percentile/composite/MMM machinery audited via the BC chain (clean;
  the BC-specific `ddpc` is Phase 1).
- **Fig 3 (process-space / BC mechanism):** Phase 1 — offset is structural (F5/F10), plus F6/F12/F1/F7/F11.
- **Fig 4 (CESM2-SF attribution):** clean.
- **Fig 5 (hydroclimate regimes):** clean except G1.
Not yet audited (lower stakes): cesm2-le, cesm2-cmip, gpcp precip percentiles, other `cmip6/data`
conditioned variables (kde/smbasis/correlation), and the ~490 plot scripts.

## Resume plan

1. Raise the monthly limit (claude.ai/settings/usage) or wait for the reset.
2. Resume the same workflow — completed agents (Trace + the ~17 audits) return cached;
   only the failed verify/cross-cut/synth agents re-run:
   `Workflow({scriptPath: ".../workflows/scripts/p004-bc-audit-wf_228d5def-e1d.js",
   resumeFromRunId: "wf_228d5def-e1d"})`.
3. Before resuming, fix the script's verdict logic so a failed (null-vote) verification is
   recorded as "unverified", never "refuted".
4. Prioritize the **algebra-closure** and **fit-correctness** cross-cuts — they target the
   offset most directly and never ran.
5. Then Phase 2+: the rest of cmip6 data/, era5, cesm2-*, gpcp, and the plot scripts.
