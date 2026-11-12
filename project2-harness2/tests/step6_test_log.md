# Step 6 Test Log: Test Data Prediction

- Tester transcript: transcripts/NN_YYYY-MM-DD_tester_stepN.md

## Tests written (tester)

One row per test function.

| Test | What it checks (from the assignment or plan) |
| --- | --- |
| `test_outputs_each_classifier_by_year_and_pooled_with_correct_counts_and_metrics` | Checks per-year and pooled results, malware-positive metrics, prediction/actual counts, and that estimators receive only the test matrix. |
| `test_final_loader_fits_on_2014_through_2018_and_keeps_later_years_held_out` | Uses temporary CSVs to verify the final split, training-only scaler fit, labels, row counts, then trains both real classifiers and evaluates all held-out years. |
| `test_rejects_misaligned_or_incomplete_test_year_metadata` | Rejects test-year metadata with a wrong length, missing declared year, or unlisted year. |
| `test_rejects_model_trained_on_a_test_year` | Ensures a model whose training metadata overlaps the held-out years is rejected. |

## Failures and decisions (student)

One row per failing test. Decision is "Accepted" (the test is right; the builder fixes the code) or "Rejected" (the test is wrong; the tester fixes the test). Add the commit with the fix.

| Test | Cause | Decision | Fixed in commit |
| --- | --- | --- | --- |

## Runs (added by `python harness.py test N`; do not edit)

### Run 1: PASSED

- Time: 2026-11-12T17:09:21+00:00
- Commit: d8bfbe3
- Result: 6 passed in 1.60s
- Files: test_step6_tester.py

```
============================= test session starts ==============================
platform linux -- Python 3.14.2, pytest-9.2.0, pluggy-1.7.0 -- /home/codespace/.python/current/bin/python
cachedir: .pytest_cache
rootdir: /workspaces/Project2v2/project2-harness2
configfile: pytest.ini
plugins: platformdirs-4.14.0, anyio-4.15.1
collecting ... collected 6 items

tests/test_step6_tester.py::test_outputs_each_classifier_by_year_and_pooled_with_correct_counts_and_metrics PASSED [ 16%]
tests/test_step6_tester.py::test_final_loader_fits_on_2014_through_2018_and_keeps_later_years_held_out PASSED [ 33%]
tests/test_step6_tester.py::test_rejects_misaligned_or_incomplete_test_year_metadata[year_test0-metadata must align] PASSED [ 50%]
tests/test_step6_tester.py::test_rejects_misaligned_or_incomplete_test_year_metadata[year_test1-exactly the declared test years] PASSED [ 66%]
tests/test_step6_tester.py::test_rejects_misaligned_or_incomplete_test_year_metadata[year_test2-exactly the declared test years] PASSED [ 83%]
tests/test_step6_tester.py::test_rejects_model_trained_on_a_test_year PASSED [100%]

==================================== PASSES ====================================
=========================== short test summary info ============================
PASSED tests/test_step6_tester.py::test_outputs_each_classifier_by_year_and_pooled_with_correct_counts_and_metrics
PASSED tests/test_step6_tester.py::test_final_loader_fits_on_2014_through_2018_and_keeps_later_years_held_out
PASSED tests/test_step6_tester.py::test_rejects_misaligned_or_incomplete_test_year_metadata[year_test0-metadata must align]
PASSED tests/test_step6_tester.py::test_rejects_misaligned_or_incomplete_test_year_metadata[year_test1-exactly the declared test years]
PASSED tests/test_step6_tester.py::test_rejects_misaligned_or_incomplete_test_year_metadata[year_test2-exactly the declared test years]
PASSED tests/test_step6_tester.py::test_rejects_model_trained_on_a_test_year
============================== 6 passed in 1.60s ===============================
```

### Run 2: PASSED

- Time: 2026-11-12T17:09:46+00:00
- Commit: d8bfbe3
- Result: 6 passed in 2.03s
- Files: test_step6_tester.py

```
============================= test session starts ==============================
platform linux -- Python 3.14.2, pytest-9.2.0, pluggy-1.7.0 -- /home/codespace/.python/current/bin/python
cachedir: .pytest_cache
rootdir: /workspaces/Project2v2/project2-harness2
configfile: pytest.ini
plugins: platformdirs-4.14.0, anyio-4.15.1
collecting ... collected 6 items

tests/test_step6_tester.py::test_outputs_each_classifier_by_year_and_pooled_with_correct_counts_and_metrics PASSED [ 16%]
tests/test_step6_tester.py::test_final_loader_fits_on_2014_through_2018_and_keeps_later_years_held_out PASSED [ 33%]
tests/test_step6_tester.py::test_rejects_misaligned_or_incomplete_test_year_metadata[year_test0-metadata must align] PASSED [ 50%]
tests/test_step6_tester.py::test_rejects_misaligned_or_incomplete_test_year_metadata[year_test1-exactly the declared test years] PASSED [ 66%]
tests/test_step6_tester.py::test_rejects_misaligned_or_incomplete_test_year_metadata[year_test2-exactly the declared test years] PASSED [ 83%]
tests/test_step6_tester.py::test_rejects_model_trained_on_a_test_year PASSED [100%]

==================================== PASSES ====================================
=========================== short test summary info ============================
PASSED tests/test_step6_tester.py::test_outputs_each_classifier_by_year_and_pooled_with_correct_counts_and_metrics
PASSED tests/test_step6_tester.py::test_final_loader_fits_on_2014_through_2018_and_keeps_later_years_held_out
PASSED tests/test_step6_tester.py::test_rejects_misaligned_or_incomplete_test_year_metadata[year_test0-metadata must align]
PASSED tests/test_step6_tester.py::test_rejects_misaligned_or_incomplete_test_year_metadata[year_test1-exactly the declared test years]
PASSED tests/test_step6_tester.py::test_rejects_misaligned_or_incomplete_test_year_metadata[year_test2-exactly the declared test years]
PASSED tests/test_step6_tester.py::test_rejects_model_trained_on_a_test_year
============================== 6 passed in 2.03s ===============================
```
