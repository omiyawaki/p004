# Repository Guidelines

## Project Purpose
This project analyzes how climate warming changes the full distribution of near-surface temperature and related hydroclimate variables, not only mean change. Work spans observations (ERA5, GPCP, CERES) and model output (CMIP6, CESM2 variants), with emphasis on percentile behavior, seasonal structure, and regional contrasts in hot extremes.

## Project Structure & Module Organization
Top-level module dirs are data sources/experiments: `cmip6/`, `era5/`, `cesm2-le/`, `cesm2-sf/`, `cesm2-cmip/`, `gpcp/`, `ceres+gpcp/`, and `rae/`. On CGD these sit inside `~/scripts/p004/scripts/` and are the git repo root; on Derecho/local they are the top-level of the clone.

Inside each module, common layout is:
- `data/` for preprocessing and derived variables
- `plot/` for figure generation
- optional `tests/` or `test_*.py` scripts

On CGD, `~/scripts/p004/data` and `~/scripts/p004/plots` are symlinks to `/project/amp/miyawaki/data/p004` and `/project/amp/miyawaki/plots/p004`. On Derecho, the equivalents live under `/glade/campaign/cgd/cas/miyawaki/{data,plots}/p004`. Local checkout carries only code, paper, and notes. Data and plots are remote-only.

## Build, Test, and Development Commands
There is no central build tool; run scripts directly from the repo root.

- `python cmip6/data/distribution/hist_hotdays.py` (compute percentile products)
- `python cmip6/plot/hist_hotdays.py` (plot warming and percentile ratios)
- `python rae/test_tf.py` (run a representative diagnostic test)
- `python -m py_compile cmip6/data/util.py` (quick syntax check after edits)

## Coding Style & Naming Conventions
Use Python with 4-space indentation and `snake_case`. Keep imports grouped (stdlib, third-party, local). Match existing filename conventions, including dot-delimited workflow names like `mk.oo.plh.py`.

Keep path and configuration variables near the top of each script.

## Testing Guidelines
Testing is script-level and analysis-driven rather than a centralized unit-test suite. Add a small runnable validation script near modified code and record expected artifacts (e.g., `*.pickle`, `*.nc`, `*.pdf`).

## Commit & Pull Request Guidelines
Recent history favors short messages (`update`, dated updates, module names). Prefer concise, scoped commits such as `cmip6: fix percentile loop bounds`.

PRs should include changed paths, scientific/technical rationale, commands run, and representative output locations.

## Data & Output Hygiene
Do not commit generated artifacts or HPC logs (`*.nc`, `*.pickle`, `*.pdf`, `*.png`, `*.o*`, `*.e*`). Keep large products in `/project/...` paths referenced by scripts.
