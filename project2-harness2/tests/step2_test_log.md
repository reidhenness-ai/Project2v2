# Step 2 Test Log: Handle Data Drift

- Tester transcript: transcripts/NN_YYYY-MM-DD_tester_stepN.md

## Tests written (tester)

One row per test function.

| Test | What it checks (from the assignment or plan) |
| --- | --- |
| `test_identical_distributions_have_zero_ks_and_no_significance` | Identical values, including a constant feature, yield zero KS statistics and no significant discoveries. |
| `test_detects_shifted_features_within_each_class` | A synthetic malware-only shift is detected while the unchanged goodware feature remains unchanged. |
| `test_benjamini_hochberg_adjustment_is_monotone_in_rank` | BH-adjusted p-values match expected values and preserve rank monotonicity. |
| `test_underflowed_p_values_are_not_reported_as_exact_zero` | Report formatting identifies p-values that underflow to zero as below a threshold. |
| `test_report_ranks_years_by_mean_ks_and_formats_underflowed_p_values` | Generated report ranking follows mean KS and does not print underflowed values as exact zero. |
| `test_rejects_invalid_p_values` | The adjustment helper rejects out-of-range and non-finite p-values. |
| `test_rejects_feature_schema_mismatch` | Year inputs with inconsistent feature names are rejected. |
| `test_compares_each_feature_to_reference_for_each_later_year_and_scope` | Checks one result per feature, later year, and overall/goodware/malware scope, with bounded statistics and p/q values. |
| `test_ks_statistic_and_p_value_match_two_sided_scipy_test` | Independently compares a returned statistic and p-value with SciPy's two-sided asymptotic KS test. |
| `test_class_stratification_separates_class_mix_change_from_feature_drift` | Verifies pooled drift can reflect a changed class mix while each class-specific feature distribution remains unchanged. |
| `test_bh_adjustment_is_applied_per_scope_and_comparison_year` | Checks adjusted p-values against an independent BH calculation within each class scope. |
| `test_analysis_does_not_mutate_input_frames` | Confirms analysis leaves caller-provided DataFrames unchanged. |
| `test_rejects_alpha_outside_open_unit_interval` | Rejects alpha values at or outside the valid open interval, including NaN. |
| `test_rejects_missing_reference_or_missing_comparison_year` | Rejects unavailable reference years and input containing no comparison year. |
| `test_rejects_invalid_year_frames` | Rejects missing targets, schema mismatch, missing/non-finite features, and invalid target labels. |
| `test_rejects_year_missing_one_of_the_class_labels` | Rejects class-specific comparisons when either year lacks a target class. |
| `test_report_writer_uses_supplied_analysis_data_and_writes_report` | Checks report generation using controlled data and a temporary output path. |

## Failures and decisions (student)

One row per failing test. Decision is "Accepted" (the test is right; the builder fixes the code) or "Rejected" (the test is wrong; the tester fixes the test). Add the commit with the fix.

| Test | Cause | Decision | Fixed in commit |
| --- | --- | --- | --- |

## Runs (added by `python harness.py test N`; do not edit)

### Run 1: PASSED

- Time: 2026-11-12T15:54:11+00:00
- Commit: 3ba5868
- Result: 6 passed in 2.33s
- Files: test_step2_drift.py

```
============================= test session starts ==============================
platform linux -- Python 3.14.2, pytest-9.2.0, pluggy-1.7.0 -- /home/codespace/.python/current/bin/python
cachedir: .pytest_cache
rootdir: /workspaces/Project2v2/project2-harness2
configfile: pytest.ini
plugins: platformdirs-4.14.0, anyio-4.15.1
collecting ... collected 6 items

tests/test_step2_drift.py::test_identical_distributions_have_zero_ks_and_no_significance PASSED [ 16%]
tests/test_step2_drift.py::test_detects_shifted_features_within_each_class PASSED [ 33%]
tests/test_step2_drift.py::test_benjamini_hochberg_adjustment_is_monotone_in_rank PASSED [ 50%]
tests/test_step2_drift.py::test_rejects_invalid_p_values[p_values0] PASSED [ 66%]
tests/test_step2_drift.py::test_rejects_invalid_p_values[p_values1] PASSED [ 83%]
tests/test_step2_drift.py::test_rejects_feature_schema_mismatch PASSED   [100%]

==================================== PASSES ====================================
=========================== short test summary info ============================
PASSED tests/test_step2_drift.py::test_identical_distributions_have_zero_ks_and_no_significance
PASSED tests/test_step2_drift.py::test_detects_shifted_features_within_each_class
PASSED tests/test_step2_drift.py::test_benjamini_hochberg_adjustment_is_monotone_in_rank
PASSED tests/test_step2_drift.py::test_rejects_invalid_p_values[p_values0]
PASSED tests/test_step2_drift.py::test_rejects_invalid_p_values[p_values1]
PASSED tests/test_step2_drift.py::test_rejects_feature_schema_mismatch
============================== 6 passed in 2.33s ===============================
```

### Run 2: PASSED

- Time: 2026-11-12T15:56:05+00:00
- Commit: 3ba5868
- Result: 7 passed in 3.33s
- Files: test_step2_drift.py

```
============================= test session starts ==============================
platform linux -- Python 3.14.2, pytest-9.2.0, pluggy-1.7.0 -- /home/codespace/.python/current/bin/python
cachedir: .pytest_cache
rootdir: /workspaces/Project2v2/project2-harness2
configfile: pytest.ini
plugins: platformdirs-4.14.0, anyio-4.15.1
collecting ... collected 7 items

tests/test_step2_drift.py::test_identical_distributions_have_zero_ks_and_no_significance PASSED [ 14%]
tests/test_step2_drift.py::test_detects_shifted_features_within_each_class PASSED [ 28%]
tests/test_step2_drift.py::test_benjamini_hochberg_adjustment_is_monotone_in_rank PASSED [ 42%]
tests/test_step2_drift.py::test_underflowed_p_values_are_not_reported_as_exact_zero PASSED [ 57%]
tests/test_step2_drift.py::test_rejects_invalid_p_values[p_values0] PASSED [ 71%]
tests/test_step2_drift.py::test_rejects_invalid_p_values[p_values1] PASSED [ 85%]
tests/test_step2_drift.py::test_rejects_feature_schema_mismatch PASSED   [100%]

==================================== PASSES ====================================
=========================== short test summary info ============================
PASSED tests/test_step2_drift.py::test_identical_distributions_have_zero_ks_and_no_significance
PASSED tests/test_step2_drift.py::test_detects_shifted_features_within_each_class
PASSED tests/test_step2_drift.py::test_benjamini_hochberg_adjustment_is_monotone_in_rank
PASSED tests/test_step2_drift.py::test_underflowed_p_values_are_not_reported_as_exact_zero
PASSED tests/test_step2_drift.py::test_rejects_invalid_p_values[p_values0]
PASSED tests/test_step2_drift.py::test_rejects_invalid_p_values[p_values1]
PASSED tests/test_step2_drift.py::test_rejects_feature_schema_mismatch
============================== 7 passed in 3.33s ===============================
```

### Run 3: PASSED

- Time: 2026-11-12T16:00:12+00:00
- Commit: 3ba5868
- Result: 8 passed in 2.40s
- Files: test_step2_drift.py

```
============================= test session starts ==============================
platform linux -- Python 3.14.2, pytest-9.2.0, pluggy-1.7.0 -- /home/codespace/.python/current/bin/python
cachedir: .pytest_cache
rootdir: /workspaces/Project2v2/project2-harness2
configfile: pytest.ini
plugins: platformdirs-4.14.0, anyio-4.15.1
collecting ... collected 8 items

tests/test_step2_drift.py::test_identical_distributions_have_zero_ks_and_no_significance PASSED [ 12%]
tests/test_step2_drift.py::test_detects_shifted_features_within_each_class PASSED [ 25%]
tests/test_step2_drift.py::test_benjamini_hochberg_adjustment_is_monotone_in_rank PASSED [ 37%]
tests/test_step2_drift.py::test_underflowed_p_values_are_not_reported_as_exact_zero PASSED [ 50%]
tests/test_step2_drift.py::test_report_ranks_years_by_mean_ks_and_formats_underflowed_p_values PASSED [ 62%]
tests/test_step2_drift.py::test_rejects_invalid_p_values[p_values0] PASSED [ 75%]
tests/test_step2_drift.py::test_rejects_invalid_p_values[p_values1] PASSED [ 87%]
tests/test_step2_drift.py::test_rejects_feature_schema_mismatch PASSED   [100%]

==================================== PASSES ====================================
=========================== short test summary info ============================
PASSED tests/test_step2_drift.py::test_identical_distributions_have_zero_ks_and_no_significance
PASSED tests/test_step2_drift.py::test_detects_shifted_features_within_each_class
PASSED tests/test_step2_drift.py::test_benjamini_hochberg_adjustment_is_monotone_in_rank
PASSED tests/test_step2_drift.py::test_underflowed_p_values_are_not_reported_as_exact_zero
PASSED tests/test_step2_drift.py::test_report_ranks_years_by_mean_ks_and_formats_underflowed_p_values
PASSED tests/test_step2_drift.py::test_rejects_invalid_p_values[p_values0]
PASSED tests/test_step2_drift.py::test_rejects_invalid_p_values[p_values1]
PASSED tests/test_step2_drift.py::test_rejects_feature_schema_mismatch
============================== 8 passed in 2.40s ===============================
```

### Run 4: PASSED

- Time: 2026-11-12T16:03:05+00:00
- Commit: 64305b7
- Result: 26 passed in 1.50s
- Files: test_step2_drift.py, test_step2_tester.py

```
============================= test session starts ==============================
platform linux -- Python 3.14.2, pytest-9.2.0, pluggy-1.7.0 -- /home/codespace/.python/current/bin/python
cachedir: .pytest_cache
rootdir: /workspaces/Project2v2/project2-harness2
configfile: pytest.ini
plugins: platformdirs-4.14.0, anyio-4.15.1
collecting ... collected 26 items

tests/test_step2_drift.py::test_identical_distributions_have_zero_ks_and_no_significance PASSED [  3%]
tests/test_step2_drift.py::test_detects_shifted_features_within_each_class PASSED [  7%]
tests/test_step2_drift.py::test_benjamini_hochberg_adjustment_is_monotone_in_rank PASSED [ 11%]
tests/test_step2_drift.py::test_underflowed_p_values_are_not_reported_as_exact_zero PASSED [ 15%]
tests/test_step2_drift.py::test_report_ranks_years_by_mean_ks_and_formats_underflowed_p_values PASSED [ 19%]
tests/test_step2_drift.py::test_rejects_invalid_p_values[p_values0] PASSED [ 23%]
tests/test_step2_drift.py::test_rejects_invalid_p_values[p_values1] PASSED [ 26%]
tests/test_step2_drift.py::test_rejects_feature_schema_mismatch PASSED   [ 30%]
tests/test_step2_tester.py::test_compares_each_feature_to_reference_for_each_later_year_and_scope PASSED [ 34%]
tests/test_step2_tester.py::test_ks_statistic_and_p_value_match_two_sided_scipy_test PASSED [ 38%]
tests/test_step2_tester.py::test_class_stratification_separates_class_mix_change_from_feature_drift PASSED [ 42%]
tests/test_step2_tester.py::test_bh_adjustment_is_applied_per_scope_and_comparison_year PASSED [ 46%]
tests/test_step2_tester.py::test_analysis_does_not_mutate_input_frames PASSED [ 50%]
tests/test_step2_tester.py::test_rejects_alpha_outside_open_unit_interval[0] PASSED [ 53%]
tests/test_step2_tester.py::test_rejects_alpha_outside_open_unit_interval[1] PASSED [ 57%]
tests/test_step2_tester.py::test_rejects_alpha_outside_open_unit_interval[-0.1] PASSED [ 61%]
tests/test_step2_tester.py::test_rejects_alpha_outside_open_unit_interval[1.1] PASSED [ 65%]
tests/test_step2_tester.py::test_rejects_alpha_outside_open_unit_interval[nan] PASSED [ 69%]
tests/test_step2_tester.py::test_rejects_missing_reference_or_missing_comparison_year PASSED [ 73%]
tests/test_step2_tester.py::test_rejects_invalid_year_frames[reference0-comparison0-target] PASSED [ 76%]
tests/test_step2_tester.py::test_rejects_invalid_year_frames[reference1-comparison1-Feature schema mismatch] PASSED [ 80%]
tests/test_step2_tester.py::test_rejects_invalid_year_frames[reference2-comparison2-missing feature values] PASSED [ 84%]
tests/test_step2_tester.py::test_rejects_invalid_year_frames[reference3-comparison3-non-finite] PASSED [ 88%]
tests/test_step2_tester.py::test_rejects_invalid_year_frames[reference4-comparison4-target values must be 0 or 1] PASSED [ 92%]
tests/test_step2_tester.py::test_rejects_year_missing_one_of_the_class_labels PASSED [ 96%]
tests/test_step2_tester.py::test_report_writer_uses_supplied_analysis_data_and_writes_report PASSED [100%]

==================================== PASSES ====================================
=========================== short test summary info ============================
PASSED tests/test_step2_drift.py::test_identical_distributions_have_zero_ks_and_no_significance
PASSED tests/test_step2_drift.py::test_detects_shifted_features_within_each_class
PASSED tests/test_step2_drift.py::test_benjamini_hochberg_adjustment_is_monotone_in_rank
PASSED tests/test_step2_drift.py::test_underflowed_p_values_are_not_reported_as_exact_zero
PASSED tests/test_step2_drift.py::test_report_ranks_years_by_mean_ks_and_formats_underflowed_p_values
PASSED tests/test_step2_drift.py::test_rejects_invalid_p_values[p_values0]
PASSED tests/test_step2_drift.py::test_rejects_invalid_p_values[p_values1]
PASSED tests/test_step2_drift.py::test_rejects_feature_schema_mismatch
PASSED tests/test_step2_tester.py::test_compares_each_feature_to_reference_for_each_later_year_and_scope
PASSED tests/test_step2_tester.py::test_ks_statistic_and_p_value_match_two_sided_scipy_test
PASSED tests/test_step2_tester.py::test_class_stratification_separates_class_mix_change_from_feature_drift
PASSED tests/test_step2_tester.py::test_bh_adjustment_is_applied_per_scope_and_comparison_year
PASSED tests/test_step2_tester.py::test_analysis_does_not_mutate_input_frames
PASSED tests/test_step2_tester.py::test_rejects_alpha_outside_open_unit_interval[0]
PASSED tests/test_step2_tester.py::test_rejects_alpha_outside_open_unit_interval[1]
PASSED tests/test_step2_tester.py::test_rejects_alpha_outside_open_unit_interval[-0.1]
PASSED tests/test_step2_tester.py::test_rejects_alpha_outside_open_unit_interval[1.1]
PASSED tests/test_step2_tester.py::test_rejects_alpha_outside_open_unit_interval[nan]
PASSED tests/test_step2_tester.py::test_rejects_missing_reference_or_missing_comparison_year
PASSED tests/test_step2_tester.py::test_rejects_invalid_year_frames[reference0-comparison0-target]
PASSED tests/test_step2_tester.py::test_rejects_invalid_year_frames[reference1-comparison1-Feature schema mismatch]
PASSED tests/test_step2_tester.py::test_rejects_invalid_year_frames[reference2-comparison2-missing feature values]
PASSED tests/test_step2_tester.py::test_rejects_invalid_year_frames[reference3-comparison3-non-finite]
PASSED tests/test_step2_tester.py::test_rejects_invalid_year_frames[reference4-comparison4-target values must be 0 or 1]
PASSED tests/test_step2_tester.py::test_rejects_year_missing_one_of_the_class_labels
PASSED tests/test_step2_tester.py::test_report_writer_uses_supplied_analysis_data_and_writes_report
============================== 26 passed in 1.50s ==============================
```
