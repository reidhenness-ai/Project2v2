# Step 7 Test Log: Sustainable ML Approach

- Tester transcript: transcripts/NN_YYYY-MM-DD_tester_stepN.md

## Tests written (tester)

One row per test function.

| Test | What it checks (from the assignment or plan) |
| --- | --- |
| `test_comparison_uses_expanding_training_windows_and_matching_test_years` | Checks static and periodic training windows, no future-year leakage, matching test rows, prediction counts, and bounded metrics for both classifiers. |
| `test_first_year_baseline_and_retraining_results_are_identical` | Confirms both strategies use the same fitted models and produce identical results for 2019, before new labels are available. |

## Failures and decisions (student)

One row per failing test. Decision is "Accepted" (the test is right; the builder fixes the code) or "Rejected" (the test is wrong; the tester fixes the test). Add the commit with the fix.

| Test | Cause | Decision | Fixed in commit |
| --- | --- | --- | --- |
| `test_comparison_uses_expanding_training_windows_and_matching_test_years` (Run 1) | The test expected `actual_goodware` and `actual_malware` fields that Step 7 does not return and the plan does not require. | Rejected as an over-specified test: removed the assertions; retained checks for reported prediction counts and metrics. | N/A — tester assertion correction |
| `test_first_year_baseline_and_retraining_results_are_identical` (Run 1) | The comparison failed only because pandas Series names differed by row index (0 vs 6); values matched. | Rejected as a test artifact: compare the row values without requiring identical Series names. | N/A — tester assertion correction |

## Runs (added by `python harness.py test N`; do not edit)

### Run 1: FAILED

- Time: 2026-11-12T17:21:41+00:00
- Commit: 96d81d2
- Result: 2 failed in 4.10s
- Files: test_step7_tester.py

```
============================= test session starts ==============================
platform linux -- Python 3.14.2, pytest-9.2.0, pluggy-1.7.0 -- /home/codespace/.python/current/bin/python
cachedir: .pytest_cache
rootdir: /workspaces/Project2v2/project2-harness2
configfile: pytest.ini
plugins: platformdirs-4.14.0, anyio-4.15.1
collecting ... collected 2 items

tests/test_step7_tester.py::test_comparison_uses_expanding_training_windows_and_matching_test_years FAILED [ 50%]
tests/test_step7_tester.py::test_first_year_baseline_and_retraining_results_are_identical FAILED [100%]

=================================== FAILURES ===================================
___ test_comparison_uses_expanding_training_windows_and_matching_test_years ____

tmp_path = PosixPath('/tmp/pytest-of-codespace/pytest-11/test_comparison_uses_expanding0')

    def test_comparison_uses_expanding_training_windows_and_matching_test_years(tmp_path):
        _write_dataset(tmp_path)
    
        results = compare_retraining_strategies(tmp_path)
    
        assert len(results) == 12
        assert set(results["approach"]) == {"Static baseline", "Periodic retraining"}
        assert set(results["classifier"]) == {"Logistic Regression", "Random Forest"}
        assert set(results["test_year"]) == {2019, 2020, 2021}
        assert len(results.groupby(["approach", "classifier", "test_year"])) == 12
    
        expected_training_years = {
            ("Static baseline", 2019): (2014, 2015, 2016, 2017, 2018),
            ("Static baseline", 2020): (2014, 2015, 2016, 2017, 2018),
            ("Static baseline", 2021): (2014, 2015, 2016, 2017, 2018),
            ("Periodic retraining", 2019): (2014, 2015, 2016, 2017, 2018),
            ("Periodic retraining", 2020): (2014, 2015, 2016, 2017, 2018, 2019),
            (
                "Periodic retraining",
                2021,
            ): (2014, 2015, 2016, 2017, 2018, 2019, 2020),
        }
        expected_training_rows = {
            (2014, 2015, 2016, 2017, 2018): 40,
            (2014, 2015, 2016, 2017, 2018, 2019): 48,
            (2014, 2015, 2016, 2017, 2018, 2019, 2020): 56,
        }
    
        for row in results.itertuples(index=False):
            expected_years = expected_training_years[(row.approach, row.test_year)]
            assert row.training_years == expected_years
            assert max(row.training_years) < row.test_year
            assert row.training_rows == expected_training_rows[expected_years]
            assert row.test_rows == 8
            assert row.positive_class == 1
>           assert row.actual_goodware == 4
                   ^^^^^^^^^^^^^^^^^^^
E           AttributeError: 'Pandas' object has no attribute 'actual_goodware'

tests/test_step7_tester.py:56: AttributeError
________ test_first_year_baseline_and_retraining_results_are_identical _________

tmp_path = PosixPath('/tmp/pytest-of-codespace/pytest-11/test_first_year_baseline_and_r0')

    def test_first_year_baseline_and_retraining_results_are_identical(tmp_path):
        _write_dataset(tmp_path)
    
        results = compare_retraining_strategies(tmp_path)
        for classifier in ("Logistic Regression", "Random Forest"):
            rows = results.loc[
                (results["classifier"] == classifier) & (results["test_year"] == 2019)
            ]
            baseline = rows.loc[rows["approach"] == "Static baseline"].drop(
                columns="approach"
            ).iloc[0]
            retrained = rows.loc[rows["approach"] == "Periodic retraining"].drop(
                columns="approach"
            ).iloc[0]
>           pd.testing.assert_series_equal(
                baseline,
                retrained,
            )
E           AssertionError: Series are different
E           
E           Attribute "name" are different
E           [left]:  0
E           [right]: 6

tests/test_step7_tester.py:79: AssertionError
=========================== short test summary info ============================
FAILED tests/test_step7_tester.py::test_comparison_uses_expanding_training_windows_and_matching_test_years
FAILED tests/test_step7_tester.py::test_first_year_baseline_and_retraining_results_are_identical
============================== 2 failed in 4.10s ===============================
```

### Run 2: PASSED

- Time: 2026-11-12T17:21:59+00:00
- Commit: 96d81d2
- Result: 2 passed in 3.71s
- Files: test_step7_tester.py

```
============================= test session starts ==============================
platform linux -- Python 3.14.2, pytest-9.2.0, pluggy-1.7.0 -- /home/codespace/.python/current/bin/python
cachedir: .pytest_cache
rootdir: /workspaces/Project2v2/project2-harness2
configfile: pytest.ini
plugins: platformdirs-4.14.0, anyio-4.15.1
collecting ... collected 2 items

tests/test_step7_tester.py::test_comparison_uses_expanding_training_windows_and_matching_test_years PASSED [ 50%]
tests/test_step7_tester.py::test_first_year_baseline_and_retraining_results_are_identical PASSED [100%]

==================================== PASSES ====================================
=========================== short test summary info ============================
PASSED tests/test_step7_tester.py::test_comparison_uses_expanding_training_windows_and_matching_test_years
PASSED tests/test_step7_tester.py::test_first_year_baseline_and_retraining_results_are_identical
============================== 2 passed in 3.71s ===============================
```
