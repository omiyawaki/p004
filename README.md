# p004: Seasonal cycle of warming across percentiles

How climate warming reshapes the full distribution of near-surface temperature,
not just the mean. Work spans observations (ERA5, GPCP, CERES) and model
output (CMIP6, CESM2 variants), with emphasis on percentile behavior, seasonal
structure, and regional contrasts in hot extremes.

Lead: Osamu Miyawaki. Coauthors: Isla Simpson, Brian Medeiros, Qinqin Kong,
Karen McKinnon.

## Layout

- `ceres+gpcp/`, `cesm2-cmip/`, `cesm2-le/`, `cesm2-sf/`, `cmip6/`, `era5/`,
  `gpcp/`, `rae/`: per-source data processing and plotting code. Each module
  has `data/` (preprocessing, derived variables) and `plot/` (figure
  generation).
- `paper/`: planning outlines (`outline.md`, `outline_comparison.md`,
  `outline_meetings.md`) plus the draft manuscript under `manuscript/`
  (`main.tex`, `main.pdf`, `references.bib`, `ametsocV6.1.cls`). The
  manuscript is in an early skeleton stage.
- `notes/`: `figure_interpretations.md` and older planning notes converted
  from docx (`outline.md`, `meetings_summary.md`, `references_p004.md`).
- `AGENTS.md`: project conventions (style, commit patterns, data hygiene).

Data and plot products are not in this repository. See
`projects.yaml :: p004 :: locations` for the authoritative paths on CGD
(`an`, `~/scripts/p004/{data,plots}` → `/project/amp/miyawaki/{data,plots}/p004`)
and on Derecho (`de`, `/glade/campaign/cgd/cas/miyawaki/{data,plots,archive}/p004`).

## Status

Planning / early-draft stage. Paper outlines are the most current thinking;
the LaTeX manuscript at `paper/manuscript/main.tex` is a skeleton with
abstract, author list, and one CMIP6 model table populated. Next steps are
tracked in `paper/outline.md`.
