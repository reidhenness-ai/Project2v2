# Step 2 Review: Handle Data Drift

## Summary

The core analysis follows the plan: it compares each year against 2014 using
two-sided feature-wise KS tests, reports overall and class-specific results, and
applies Benjamini-Hochberg adjustment per year and scope. Validation checks and
the synthetic tests cover important cases. I independently ran
`python -m pytest -q tests/test_step2_drift.py`; all 7 tests passed.

One issue remains in the checked-in report: it no longer reflects the current
report-generation code.

## Issues

### 1) The Step 2 report is stale relative to the current analysis code

- **Description:** `src/drift.py` currently says that yearly comparisons are
  ranked by mean KS statistic and sorts the results by `mean_ks` (lines 164-165,
  194). Its feature-table formatter also renders p-values that underflow to
  zero as `<1e-300` (lines 33 and 234-235). However,
  `docs/step2_drift_analysis.md` says the ranking is by median KS, orders years
  according to the old median-based output, and displays raw and adjusted
  p-values as `0`. For example, the goodware table puts 2019 ahead of 2020,
  although the displayed mean KS for 2020 (0.0632) exceeds 2019 (0.0503).
  Readers cannot reliably determine the ranking or p-value representation from
  the report as it stands.
- **Severity:** medium
- **File and location:** `src/drift.py:161-200,230-235` and
  `docs/step2_drift_analysis.md:7-22,49-93`.
- **Recommended fix:** Regenerate `docs/step2_drift_analysis.md` with
  `python -m src.drift` after the analysis code is finalized. Confirm that the
  written ranking description, table order, and underflowed p-value display
  match the current implementation; add a focused test or verification step
  that catches stale generated output.

## Decision Log

- Comment 1: Accepted — Regenerated `docs/step2_drift_analysis.md` with
  `python -m src.drift`; the output now states and follows the mean-KS ranking,
  and underflowed p-values are displayed as `<1e-300`. Added
  `test_report_ranks_years_by_mean_ks_and_formats_underflowed_p_values` to
  guard the report logic. The final Step 2 test run passed all 8 tests.
