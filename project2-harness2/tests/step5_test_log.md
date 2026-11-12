# Step 5 Test Log: Evaluate Classifier Performance

- Tester transcript: transcripts/NN_YYYY-MM-DD_tester_stepN.md

## Tests written (tester)

One row per test function.

| Test | What it checks (from the assignment or plan) |
| --- | --- |
| `test_computes_pooled_metrics_with_malware_as_positive_class` | Checks hand-calculated pooled accuracy, precision, recall, and F1 for both classifiers and confirms predictions use only test features. |
| `test_returns_metrics_for_each_test_year_and_for_the_pooled_test_set` | Requires separate 2019, 2020, and 2021 metric rows as well as a pooled row, as specified by the plan. |
| `test_zero_division_is_defined_when_predictions_have_no_malware` | Verifies zero-division handling when both classifiers predict no malware. |
| `test_rejects_training_test_year_overlap_or_nonchronological_fit` | Rejects overlapping years and models trained on years that do not precede the test period. |
| `test_rejects_empty_missing_or_invalid_test_labels` | Rejects empty, missing, or non-binary test labels. |

## Failures and decisions (student)

One row per failing test. Decision is "Accepted" (the test is right; the builder fixes the code) or "Rejected" (the test is wrong; the tester fixes the test). Add the commit with the fix.

| Test | Cause | Decision | Fixed in commit |
| --- | --- | --- | --- |
| `test_returns_metrics_for_each_test_year_and_for_the_pooled_test_set` | `evaluate_test_set` initially returned only two pooled rows, rather than separate metrics for each test year and a pooled result. | Accepted: the plan requires per-year and pooled metrics. The builder added per-year results; the test now passes. | `efa623a` |
| `test_rejects_training_test_year_overlap_or_nonchronological_fit` (Run 1 case) | The test data accidentally had overlap as well as non-chronological years, so the evaluator correctly raised the overlap error first. | Rejected as a test setup issue: adjusted test years to make the groups disjoint and isolate chronology validation. The corrected case passes in Run 2. | N/A — tester test-data correction |
| `test_computes_pooled_metrics_with_malware_as_positive_class` (Run 3 case) | The assertion selected one row per classifier, which became ambiguous after the evaluator started returning separate year rows. | Rejected as a test assertion issue: select the pooled row by its total test-row count; the corrected test passes in Run 4. | N/A — tester assertion correction |

## Runs (added by `python harness.py test N`; do not edit)

### Run 1: FAILED

- Time: 2026-11-12T16:49:43+00:00
- Commit: 8d18adb
- Result: 2 failed, 7 passed in 2.16s
- Files: test_step5_tester.py

```
============================= test session starts ==============================
platform linux -- Python 3.14.2, pytest-9.2.0, pluggy-1.7.0 -- /home/codespace/.python/current/bin/python
cachedir: .pytest_cache
rootdir: /workspaces/Project2v2/project2-harness2
configfile: pytest.ini
plugins: platformdirs-4.14.0, anyio-4.15.1
collecting ... collected 9 items

tests/test_step5_tester.py::test_computes_pooled_metrics_with_malware_as_positive_class PASSED [ 11%]
tests/test_step5_tester.py::test_returns_metrics_for_each_test_year_and_for_the_pooled_test_set FAILED [ 22%]
tests/test_step5_tester.py::test_zero_division_is_defined_when_predictions_have_no_malware PASSED [ 33%]
tests/test_step5_tester.py::test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years0-test_years0-overlap] PASSED [ 44%]
tests/test_step5_tester.py::test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years1-test_years1-precede] FAILED [ 55%]
tests/test_step5_tester.py::test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years2-test_years2-precede] PASSED [ 66%]
tests/test_step5_tester.py::test_rejects_empty_missing_or_invalid_test_labels[labels0-present and non-empty] PASSED [ 77%]
tests/test_step5_tester.py::test_rejects_empty_missing_or_invalid_test_labels[labels1-present and non-empty] PASSED [ 88%]
tests/test_step5_tester.py::test_rejects_empty_missing_or_invalid_test_labels[labels2-encoded as 0 or 1] PASSED [100%]

=================================== FAILURES ===================================
_____ test_returns_metrics_for_each_test_year_and_for_the_pooled_test_set ______

    def test_returns_metrics_for_each_test_year_and_for_the_pooled_test_set():
        results = evaluate_test_set(_trained_models(), _test_split())
    
        assert set(results["classifier"]) == {"Logistic Regression", "Random Forest"}
>       assert len(results) == 2 * 4
E       assert 2 == (2 * 4)
E        +  where 2 = len(            classifier  test_rows  ...    recall  f1_score\n0  Logistic Regression         12  ...  0.714286  0.769231\n1        Random Forest         12  ...  0.000000  0.000000\n\n[2 rows x 8 columns])

tests/test_step5_tester.py:96: AssertionError
_ test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years1-test_years1-precede] _

training_years = (2014, 2020), test_years = (2019, 2020), message = 'precede'

    @pytest.mark.parametrize(
        ("training_years", "test_years", "message"),
        [
            ((2014, 2019), (2019, 2020), "overlap"),
            ((2014, 2020), (2019, 2020), "precede"),
            ((), (2019, 2020), "precede"),
        ],
    )
    def test_rejects_training_test_year_overlap_or_nonchronological_fit(
        training_years, test_years, message
    ):
>       with pytest.raises(ValueError, match=message):
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       AssertionError: Regex pattern did not match.
E         Expected regex: 'precede'
E         Actual message: "A model's training years overlap the held-out test years."

tests/test_step5_tester.py:135: AssertionError
==================================== PASSES ====================================
=========================== short test summary info ============================
PASSED tests/test_step5_tester.py::test_computes_pooled_metrics_with_malware_as_positive_class
PASSED tests/test_step5_tester.py::test_zero_division_is_defined_when_predictions_have_no_malware
PASSED tests/test_step5_tester.py::test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years0-test_years0-overlap]
PASSED tests/test_step5_tester.py::test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years2-test_years2-precede]
PASSED tests/test_step5_tester.py::test_rejects_empty_missing_or_invalid_test_labels[labels0-present and non-empty]
PASSED tests/test_step5_tester.py::test_rejects_empty_missing_or_invalid_test_labels[labels1-present and non-empty]
PASSED tests/test_step5_tester.py::test_rejects_empty_missing_or_invalid_test_labels[labels2-encoded as 0 or 1]
FAILED tests/test_step5_tester.py::test_returns_metrics_for_each_test_year_and_for_the_pooled_test_set
FAILED tests/test_step5_tester.py::test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years1-test_years1-precede]
========================= 2 failed, 7 passed in 2.16s ==========================
```

### Run 2: FAILED

- Time: 2026-11-12T16:50:04+00:00
- Commit: 8d18adb
- Result: 1 failed, 8 passed in 1.95s
- Files: test_step5_tester.py

```
============================= test session starts ==============================
platform linux -- Python 3.14.2, pytest-9.2.0, pluggy-1.7.0 -- /home/codespace/.python/current/bin/python
cachedir: .pytest_cache
rootdir: /workspaces/Project2v2/project2-harness2
configfile: pytest.ini
plugins: platformdirs-4.14.0, anyio-4.15.1
collecting ... collected 9 items

tests/test_step5_tester.py::test_computes_pooled_metrics_with_malware_as_positive_class PASSED [ 11%]
tests/test_step5_tester.py::test_returns_metrics_for_each_test_year_and_for_the_pooled_test_set FAILED [ 22%]
tests/test_step5_tester.py::test_zero_division_is_defined_when_predictions_have_no_malware PASSED [ 33%]
tests/test_step5_tester.py::test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years0-test_years0-overlap] PASSED [ 44%]
tests/test_step5_tester.py::test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years1-test_years1-precede] PASSED [ 55%]
tests/test_step5_tester.py::test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years2-test_years2-precede] PASSED [ 66%]
tests/test_step5_tester.py::test_rejects_empty_missing_or_invalid_test_labels[labels0-present and non-empty] PASSED [ 77%]
tests/test_step5_tester.py::test_rejects_empty_missing_or_invalid_test_labels[labels1-present and non-empty] PASSED [ 88%]
tests/test_step5_tester.py::test_rejects_empty_missing_or_invalid_test_labels[labels2-encoded as 0 or 1] PASSED [100%]

=================================== FAILURES ===================================
_____ test_returns_metrics_for_each_test_year_and_for_the_pooled_test_set ______

    def test_returns_metrics_for_each_test_year_and_for_the_pooled_test_set():
        results = evaluate_test_set(_trained_models(), _test_split())
    
        assert set(results["classifier"]) == {"Logistic Regression", "Random Forest"}
>       assert len(results) == 2 * 4
E       assert 2 == (2 * 4)
E        +  where 2 = len(            classifier  test_rows  ...    recall  f1_score\n0  Logistic Regression         12  ...  0.714286  0.769231\n1        Random Forest         12  ...  0.000000  0.000000\n\n[2 rows x 8 columns])

tests/test_step5_tester.py:96: AssertionError
==================================== PASSES ====================================
=========================== short test summary info ============================
PASSED tests/test_step5_tester.py::test_computes_pooled_metrics_with_malware_as_positive_class
PASSED tests/test_step5_tester.py::test_zero_division_is_defined_when_predictions_have_no_malware
PASSED tests/test_step5_tester.py::test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years0-test_years0-overlap]
PASSED tests/test_step5_tester.py::test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years1-test_years1-precede]
PASSED tests/test_step5_tester.py::test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years2-test_years2-precede]
PASSED tests/test_step5_tester.py::test_rejects_empty_missing_or_invalid_test_labels[labels0-present and non-empty]
PASSED tests/test_step5_tester.py::test_rejects_empty_missing_or_invalid_test_labels[labels1-present and non-empty]
PASSED tests/test_step5_tester.py::test_rejects_empty_missing_or_invalid_test_labels[labels2-encoded as 0 or 1]
FAILED tests/test_step5_tester.py::test_returns_metrics_for_each_test_year_and_for_the_pooled_test_set
========================= 1 failed, 8 passed in 1.95s ==========================
```

### Run 3: FAILED

- Time: 2026-11-12T16:55:41+00:00
- Commit: efa623a
- Result: 1 failed, 8 passed in 1.94s
- Files: test_step5_tester.py

```
============================= test session starts ==============================
platform linux -- Python 3.14.2, pytest-9.2.0, pluggy-1.7.0 -- /home/codespace/.python/current/bin/python
cachedir: .pytest_cache
rootdir: /workspaces/Project2v2/project2-harness2
configfile: pytest.ini
plugins: platformdirs-4.14.0, anyio-4.15.1
collecting ... collected 9 items

tests/test_step5_tester.py::test_computes_pooled_metrics_with_malware_as_positive_class FAILED [ 11%]
tests/test_step5_tester.py::test_returns_metrics_for_each_test_year_and_for_the_pooled_test_set PASSED [ 22%]
tests/test_step5_tester.py::test_zero_division_is_defined_when_predictions_have_no_malware PASSED [ 33%]
tests/test_step5_tester.py::test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years0-test_years0-overlap] PASSED [ 44%]
tests/test_step5_tester.py::test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years1-test_years1-precede] PASSED [ 55%]
tests/test_step5_tester.py::test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years2-test_years2-precede] PASSED [ 66%]
tests/test_step5_tester.py::test_rejects_empty_missing_or_invalid_test_labels[labels0-present and non-empty] PASSED [ 77%]
tests/test_step5_tester.py::test_rejects_empty_missing_or_invalid_test_labels[labels1-present and non-empty] PASSED [ 88%]
tests/test_step5_tester.py::test_rejects_empty_missing_or_invalid_test_labels[labels2-encoded as 0 or 1] PASSED [100%]

=================================== FAILURES ===================================
_________ test_computes_pooled_metrics_with_malware_as_positive_class __________

    def test_computes_pooled_metrics_with_malware_as_positive_class():
        split = _test_split()
        models = _trained_models()
    
        results = evaluate_test_set(models, split).set_index("classifier")
    
        logistic = results.loc["Logistic Regression"]
>       assert logistic["test_rows"] == 12

tests/test_step5_tester.py:74: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = classifier
Logistic Regression     True
Logistic Regression    False
Logistic Regression    False
Logistic Regression    False
Name: test_rows, dtype: bool

    @final
    def __bool__(self) -> NoReturn:
>       raise ValueError(
            f"The truth value of a {type(self).__name__} is ambiguous. "
            "Use a.empty, a.item(), a.any() or a.all()."
        )
E       ValueError: The truth value of a Series is ambiguous. Use a.empty, a.item(), a.any() or a.all().

/usr/local/python/3.14.2/lib/python3.14/site-packages/pandas/core/generic.py:1445: ValueError
==================================== PASSES ====================================
=========================== short test summary info ============================
PASSED tests/test_step5_tester.py::test_returns_metrics_for_each_test_year_and_for_the_pooled_test_set
PASSED tests/test_step5_tester.py::test_zero_division_is_defined_when_predictions_have_no_malware
PASSED tests/test_step5_tester.py::test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years0-test_years0-overlap]
PASSED tests/test_step5_tester.py::test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years1-test_years1-precede]
PASSED tests/test_step5_tester.py::test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years2-test_years2-precede]
PASSED tests/test_step5_tester.py::test_rejects_empty_missing_or_invalid_test_labels[labels0-present and non-empty]
PASSED tests/test_step5_tester.py::test_rejects_empty_missing_or_invalid_test_labels[labels1-present and non-empty]
PASSED tests/test_step5_tester.py::test_rejects_empty_missing_or_invalid_test_labels[labels2-encoded as 0 or 1]
FAILED tests/test_step5_tester.py::test_computes_pooled_metrics_with_malware_as_positive_class
========================= 1 failed, 8 passed in 1.94s ==========================
```

### Run 4: PASSED

- Time: 2026-11-12T16:55:52+00:00
- Commit: efa623a
- Result: 9 passed in 1.83s
- Files: test_step5_tester.py

```
============================= test session starts ==============================
platform linux -- Python 3.14.2, pytest-9.2.0, pluggy-1.7.0 -- /home/codespace/.python/current/bin/python
cachedir: .pytest_cache
rootdir: /workspaces/Project2v2/project2-harness2
configfile: pytest.ini
plugins: platformdirs-4.14.0, anyio-4.15.1
collecting ... collected 9 items

tests/test_step5_tester.py::test_computes_pooled_metrics_with_malware_as_positive_class PASSED [ 11%]
tests/test_step5_tester.py::test_returns_metrics_for_each_test_year_and_for_the_pooled_test_set PASSED [ 22%]
tests/test_step5_tester.py::test_zero_division_is_defined_when_predictions_have_no_malware PASSED [ 33%]
tests/test_step5_tester.py::test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years0-test_years0-overlap] PASSED [ 44%]
tests/test_step5_tester.py::test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years1-test_years1-precede] PASSED [ 55%]
tests/test_step5_tester.py::test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years2-test_years2-precede] PASSED [ 66%]
tests/test_step5_tester.py::test_rejects_empty_missing_or_invalid_test_labels[labels0-present and non-empty] PASSED [ 77%]
tests/test_step5_tester.py::test_rejects_empty_missing_or_invalid_test_labels[labels1-present and non-empty] PASSED [ 88%]
tests/test_step5_tester.py::test_rejects_empty_missing_or_invalid_test_labels[labels2-encoded as 0 or 1] PASSED [100%]

==================================== PASSES ====================================
=========================== short test summary info ============================
PASSED tests/test_step5_tester.py::test_computes_pooled_metrics_with_malware_as_positive_class
PASSED tests/test_step5_tester.py::test_returns_metrics_for_each_test_year_and_for_the_pooled_test_set
PASSED tests/test_step5_tester.py::test_zero_division_is_defined_when_predictions_have_no_malware
PASSED tests/test_step5_tester.py::test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years0-test_years0-overlap]
PASSED tests/test_step5_tester.py::test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years1-test_years1-precede]
PASSED tests/test_step5_tester.py::test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years2-test_years2-precede]
PASSED tests/test_step5_tester.py::test_rejects_empty_missing_or_invalid_test_labels[labels0-present and non-empty]
PASSED tests/test_step5_tester.py::test_rejects_empty_missing_or_invalid_test_labels[labels1-present and non-empty]
PASSED tests/test_step5_tester.py::test_rejects_empty_missing_or_invalid_test_labels[labels2-encoded as 0 or 1]
============================== 9 passed in 1.83s ===============================
```

### Run 5: PASSED

- Time: 2026-11-12T17:02:46+00:00
- Commit: 07c0b66
- Result: 9 passed in 1.62s
- Files: test_step5_tester.py

```
============================= test session starts ==============================
platform linux -- Python 3.14.2, pytest-9.2.0, pluggy-1.7.0 -- /home/codespace/.python/current/bin/python
cachedir: .pytest_cache
rootdir: /workspaces/Project2v2/project2-harness2
configfile: pytest.ini
plugins: platformdirs-4.14.0, anyio-4.15.1
collecting ... collected 9 items

tests/test_step5_tester.py::test_computes_pooled_metrics_with_malware_as_positive_class PASSED [ 11%]
tests/test_step5_tester.py::test_returns_metrics_for_each_test_year_and_for_the_pooled_test_set PASSED [ 22%]
tests/test_step5_tester.py::test_zero_division_is_defined_when_predictions_have_no_malware PASSED [ 33%]
tests/test_step5_tester.py::test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years0-test_years0-overlap] PASSED [ 44%]
tests/test_step5_tester.py::test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years1-test_years1-precede] PASSED [ 55%]
tests/test_step5_tester.py::test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years2-test_years2-precede] PASSED [ 66%]
tests/test_step5_tester.py::test_rejects_empty_missing_or_invalid_test_labels[labels0-present and non-empty] PASSED [ 77%]
tests/test_step5_tester.py::test_rejects_empty_missing_or_invalid_test_labels[labels1-present and non-empty] PASSED [ 88%]
tests/test_step5_tester.py::test_rejects_empty_missing_or_invalid_test_labels[labels2-encoded as 0 or 1] PASSED [100%]

==================================== PASSES ====================================
=========================== short test summary info ============================
PASSED tests/test_step5_tester.py::test_computes_pooled_metrics_with_malware_as_positive_class
PASSED tests/test_step5_tester.py::test_returns_metrics_for_each_test_year_and_for_the_pooled_test_set
PASSED tests/test_step5_tester.py::test_zero_division_is_defined_when_predictions_have_no_malware
PASSED tests/test_step5_tester.py::test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years0-test_years0-overlap]
PASSED tests/test_step5_tester.py::test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years1-test_years1-precede]
PASSED tests/test_step5_tester.py::test_rejects_training_test_year_overlap_or_nonchronological_fit[training_years2-test_years2-precede]
PASSED tests/test_step5_tester.py::test_rejects_empty_missing_or_invalid_test_labels[labels0-present and non-empty]
PASSED tests/test_step5_tester.py::test_rejects_empty_missing_or_invalid_test_labels[labels1-present and non-empty]
PASSED tests/test_step5_tester.py::test_rejects_empty_missing_or_invalid_test_labels[labels2-encoded as 0 or 1]
============================== 9 passed in 1.62s ===============================
```
