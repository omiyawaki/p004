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
- [ ] **Chunk 2 — curve evaluation → `ooplh`** (`mk.oo.plh.py`): how BC_all is reconstructed; extrapolation beyond observed SM; handling of failed fits (`bc=None`).
- [ ] **Chunk 3 — decomposition algebra** (`mk.oo.plh.{fixbc,dbc,fixmsm,rddsm,rbcsm}.py`): do the terms partition?
- [ ] **Chunk 4 — inputs** (`rg.p.cond.py`, `rg.p.py`, `rg.m.py`, `mk.csm.py`): hot-day percentile & mean construction.
- [ ] **Chunk 5 — aggregation** (`mmm.p.cond.dsm.py`): finish; resolve the csm subtraction (F1).
- [ ] **Chunk 6 — conventions + figures** (`util.py`, `decomp.*.mmm.lh.py`).
- [ ] **External — `etregimes.bestfit`** (not in repo; see F3): the actual fit engine. Highest offset-relevance; needs the source.

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
