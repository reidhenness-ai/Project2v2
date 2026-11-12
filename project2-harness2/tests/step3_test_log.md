# Step 3 Test Log: Preprocess Data for Model Training

- Tester transcript: transcripts/NN_YYYY-MM-DD_tester_stepN.md

## Tests written (tester)

One row per test function.

| Test | What it checks (from the assignment or plan) |
| --- | --- |
| `test_splits_are_chronological_disjoint_and_preserve_feature_order` | Verifies chronological, non-overlapping split metadata, row counts, and feature order. |
| `test_standard_scaler_is_fitted_only_on_training_rows` | Checks the scaler's mean, variance, and sample count against training values and confirms validation uses those learned parameters. |
| `test_changing_later_years_does_not_change_fitted_scaler` | Changes test-year feature values and confirms scaler parameters and scaled training features remain unchanged. |
| `test_rejects_non_chronological_year_groups` | Rejects an invalid ordering of training and validation years. |
| `test_rejects_feature_schema_mismatch` | Rejects feature-name/order inconsistency across years. |
| `test_loader_can_read_selected_years_while_checking_full_inventory` | Checks the staged loader returns only requested years while requiring the complete, schema-consistent file inventory. |
| `test_default_split_uses_planned_years_and_keeps_metadata_out_of_features` | Verifies the planned 2014-2017/2018/2019-2021 split, matching row metadata, labels, and feature columns. |
| `test_scaler_matches_all_training_rows_and_transforms_later_splits_unchanged` | Compares scaler statistics and scaled values with an independent fit over training rows only. |
| `test_perturbing_validation_and_test_rows_does_not_change_training_fit` | Changes later features and labels and confirms the training scaler and transformed training rows remain unchanged. |
| `test_source_frames_are_not_mutated` | Confirms split creation does not modify the supplied yearly DataFrames. |
| `test_rejects_invalid_year_groups` | Rejects overlapping, unsorted, non-chronological, or empty split groups. |
| `test_rejects_missing_or_unassigned_years` | Rejects yearly input with missing required years or years not assigned to a split. |
| `test_rejects_invalid_year_data` | Rejects missing targets, schema mismatch, empty years, missing/non-finite features, and invalid target labels. |
| `test_staged_loader_builds_default_split_and_fits_scaler_from_train_csvs` | Exercises the CSV loader end to end using temporary files and verifies scaler fit counts and year groups. |

## Failures and decisions (student)

One row per failing test. Decision is "Accepted" (the test is right; the builder fixes the code) or "Rejected" (the test is wrong; the tester fixes the test). Add the commit with the fix.

| Test | Cause | Decision | Fixed in commit |
| --- | --- | --- | --- |

## Runs (added by `python harness.py test N`; do not edit)

### Run 1: PASSED

- Time: 2026-11-12T16:18:31+00:00
- Commit: 64305b7
- Result: 5 passed in 1.46s
- Files: test_step3_preprocessing.py

```
============================= test session starts ==============================
platform linux -- Python 3.14.2, pytest-9.2.0, pluggy-1.7.0 -- /home/codespace/.python/current/bin/python
cachedir: .pytest_cache
rootdir: /workspaces/Project2v2/project2-harness2
configfile: pytest.ini
plugins: platformdirs-4.14.0, anyio-4.15.1
collecting ... collected 5 items

tests/test_step3_preprocessing.py::test_splits_are_chronological_disjoint_and_preserve_feature_order PASSED [ 20%]
tests/test_step3_preprocessing.py::test_standard_scaler_is_fitted_only_on_training_rows PASSED [ 40%]
tests/test_step3_preprocessing.py::test_changing_later_years_does_not_change_fitted_scaler PASSED [ 60%]
tests/test_step3_preprocessing.py::test_rejects_non_chronological_year_groups PASSED [ 80%]
tests/test_step3_preprocessing.py::test_rejects_feature_schema_mismatch PASSED [100%]

==================================== PASSES ====================================
=========================== short test summary info ============================
PASSED tests/test_step3_preprocessing.py::test_splits_are_chronological_disjoint_and_preserve_feature_order
PASSED tests/test_step3_preprocessing.py::test_standard_scaler_is_fitted_only_on_training_rows
PASSED tests/test_step3_preprocessing.py::test_changing_later_years_does_not_change_fitted_scaler
PASSED tests/test_step3_preprocessing.py::test_rejects_non_chronological_year_groups
PASSED tests/test_step3_preprocessing.py::test_rejects_feature_schema_mismatch
============================== 5 passed in 1.46s ===============================
```

### Run 2: PASSED

- Time: 2026-11-12T16:20:22+00:00
- Commit: 64305b7
- Result: 6 passed in 1.21s
- Files: test_step3_preprocessing.py

```
============================= test session starts ==============================
platform linux -- Python 3.14.2, pytest-9.2.0, pluggy-1.7.0 -- /home/codespace/.python/current/bin/python
cachedir: .pytest_cache
rootdir: /workspaces/Project2v2/project2-harness2
configfile: pytest.ini
plugins: platformdirs-4.14.0, anyio-4.15.1
collecting ... collected 6 items

tests/test_step3_preprocessing.py::test_splits_are_chronological_disjoint_and_preserve_feature_order PASSED [ 16%]
tests/test_step3_preprocessing.py::test_standard_scaler_is_fitted_only_on_training_rows PASSED [ 33%]
tests/test_step3_preprocessing.py::test_changing_later_years_does_not_change_fitted_scaler PASSED [ 50%]
tests/test_step3_preprocessing.py::test_rejects_non_chronological_year_groups PASSED [ 66%]
tests/test_step3_preprocessing.py::test_rejects_feature_schema_mismatch PASSED [ 83%]
tests/test_step3_preprocessing.py::test_loader_can_read_selected_years_while_checking_full_inventory PASSED [100%]

==================================== PASSES ====================================
=========================== short test summary info ============================
PASSED tests/test_step3_preprocessing.py::test_splits_are_chronological_disjoint_and_preserve_feature_order
PASSED tests/test_step3_preprocessing.py::test_standard_scaler_is_fitted_only_on_training_rows
PASSED tests/test_step3_preprocessing.py::test_changing_later_years_does_not_change_fitted_scaler
PASSED tests/test_step3_preprocessing.py::test_rejects_non_chronological_year_groups
PASSED tests/test_step3_preprocessing.py::test_rejects_feature_schema_mismatch
PASSED tests/test_step3_preprocessing.py::test_loader_can_read_selected_years_while_checking_full_inventory
============================== 6 passed in 1.21s ===============================
```

### Run 3: PASSED

- Time: 2026-11-12T16:28:32+00:00
- Commit: d61083c
- Result: 23 passed in 1.75s
- Files: test_step3_preprocessing.py, test_step3_tester.py

```
============================= test session starts ==============================
platform linux -- Python 3.14.2, pytest-9.2.0, pluggy-1.7.0 -- /home/codespace/.python/current/bin/python
cachedir: .pytest_cache
rootdir: /workspaces/Project2v2/project2-harness2
configfile: pytest.ini
plugins: platformdirs-4.14.0, anyio-4.15.1
collecting ... collected 23 items

tests/test_step3_preprocessing.py::test_splits_are_chronological_disjoint_and_preserve_feature_order PASSED [  4%]
tests/test_step3_preprocessing.py::test_standard_scaler_is_fitted_only_on_training_rows PASSED [  8%]
tests/test_step3_preprocessing.py::test_changing_later_years_does_not_change_fitted_scaler PASSED [ 13%]
tests/test_step3_preprocessing.py::test_rejects_non_chronological_year_groups PASSED [ 17%]
tests/test_step3_preprocessing.py::test_rejects_feature_schema_mismatch PASSED [ 21%]
tests/test_step3_preprocessing.py::test_loader_can_read_selected_years_while_checking_full_inventory PASSED [ 26%]
tests/test_step3_tester.py::test_default_split_uses_planned_years_and_keeps_metadata_out_of_features PASSED [ 30%]
tests/test_step3_tester.py::test_scaler_matches_all_training_rows_and_transforms_later_splits_unchanged PASSED [ 34%]
tests/test_step3_tester.py::test_perturbing_validation_and_test_rows_does_not_change_training_fit PASSED [ 39%]
tests/test_step3_tester.py::test_source_frames_are_not_mutated PASSED    [ 43%]
tests/test_step3_tester.py::test_rejects_invalid_year_groups[train_years0-validation_years0-test_years0-overlap] PASSED [ 47%]
tests/test_step3_tester.py::test_rejects_invalid_year_groups[train_years1-validation_years1-test_years1-ascending order] PASSED [ 52%]
tests/test_step3_tester.py::test_rejects_invalid_year_groups[train_years2-validation_years2-test_years2-ascending order] PASSED [ 56%]
tests/test_step3_tester.py::test_rejects_invalid_year_groups[train_years3-validation_years3-test_years3-precede] PASSED [ 60%]
tests/test_step3_tester.py::test_rejects_invalid_year_groups[train_years4-validation_years4-test_years4-cannot be empty] PASSED [ 65%]
tests/test_step3_tester.py::test_rejects_missing_or_unassigned_years PASSED [ 69%]
tests/test_step3_tester.py::test_rejects_invalid_year_data[2014-replacement0-target] PASSED [ 73%]
tests/test_step3_tester.py::test_rejects_invalid_year_data[2018-replacement1-Feature schema mismatch] PASSED [ 78%]
tests/test_step3_tester.py::test_rejects_invalid_year_data[2019-replacement2-missing feature values] PASSED [ 82%]
tests/test_step3_tester.py::test_rejects_invalid_year_data[2020-replacement3-non-finite] PASSED [ 86%]
tests/test_step3_tester.py::test_rejects_invalid_year_data[2021-replacement4-target values must be 0 or 1] PASSED [ 91%]
tests/test_step3_tester.py::test_rejects_invalid_year_data[2016-replacement5-contains no rows] PASSED [ 95%]
tests/test_step3_tester.py::test_staged_loader_builds_default_split_and_fits_scaler_from_train_csvs PASSED [100%]

==================================== PASSES ====================================
=========================== short test summary info ============================
PASSED tests/test_step3_preprocessing.py::test_splits_are_chronological_disjoint_and_preserve_feature_order
PASSED tests/test_step3_preprocessing.py::test_standard_scaler_is_fitted_only_on_training_rows
PASSED tests/test_step3_preprocessing.py::test_changing_later_years_does_not_change_fitted_scaler
PASSED tests/test_step3_preprocessing.py::test_rejects_non_chronological_year_groups
PASSED tests/test_step3_preprocessing.py::test_rejects_feature_schema_mismatch
PASSED tests/test_step3_preprocessing.py::test_loader_can_read_selected_years_while_checking_full_inventory
PASSED tests/test_step3_tester.py::test_default_split_uses_planned_years_and_keeps_metadata_out_of_features
PASSED tests/test_step3_tester.py::test_scaler_matches_all_training_rows_and_transforms_later_splits_unchanged
PASSED tests/test_step3_tester.py::test_perturbing_validation_and_test_rows_does_not_change_training_fit
PASSED tests/test_step3_tester.py::test_source_frames_are_not_mutated
PASSED tests/test_step3_tester.py::test_rejects_invalid_year_groups[train_years0-validation_years0-test_years0-overlap]
PASSED tests/test_step3_tester.py::test_rejects_invalid_year_groups[train_years1-validation_years1-test_years1-ascending order]
PASSED tests/test_step3_tester.py::test_rejects_invalid_year_groups[train_years2-validation_years2-test_years2-ascending order]
PASSED tests/test_step3_tester.py::test_rejects_invalid_year_groups[train_years3-validation_years3-test_years3-precede]
PASSED tests/test_step3_tester.py::test_rejects_invalid_year_groups[train_years4-validation_years4-test_years4-cannot be empty]
PASSED tests/test_step3_tester.py::test_rejects_missing_or_unassigned_years
PASSED tests/test_step3_tester.py::test_rejects_invalid_year_data[2014-replacement0-target]
PASSED tests/test_step3_tester.py::test_rejects_invalid_year_data[2018-replacement1-Feature schema mismatch]
PASSED tests/test_step3_tester.py::test_rejects_invalid_year_data[2019-replacement2-missing feature values]
PASSED tests/test_step3_tester.py::test_rejects_invalid_year_data[2020-replacement3-non-finite]
PASSED tests/test_step3_tester.py::test_rejects_invalid_year_data[2021-replacement4-target values must be 0 or 1]
PASSED tests/test_step3_tester.py::test_rejects_invalid_year_data[2016-replacement5-contains no rows]
PASSED tests/test_step3_tester.py::test_staged_loader_builds_default_split_and_fits_scaler_from_train_csvs
============================== 23 passed in 1.75s ==============================
```
