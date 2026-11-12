# Step 4 Test Log: Apply Machine Learning Classifiers

- Tester transcript: transcripts/NN_YYYY-MM-DD_tester_stepN.md

## Tests written (tester)

One row per test function.

| Test | What it checks (from the assignment or plan) |
| --- | --- |
| `test_factory_returns_the_two_planned_classifiers_with_fixed_seed` | Confirms factory output contains Logistic Regression and Random Forest with the planned fixed random seed. |
| `test_train_fits_both_models_and_returns_consistent_metadata` | Fits both models and checks predictions, classes, feature counts, training metadata, and fit timings. |
| `test_repeated_fits_are_reproducible` | Fits each classifier twice on the same controlled data and compares predictions, coefficients, and probabilities. |
| `test_temporal_training_uses_only_training_partition` | Changes validation/test inputs and labels, then checks that `train_from_temporal_split` produces unchanged models. |
| `test_rejects_empty_or_inconsistent_training_input` | Rejects empty inputs, mismatched row counts, invalid labels, and missing labels. |
| `test_single_class_training_failure_is_surfaced` | Confirms fitting with only one label raises a clear error instead of returning an unusable model. |

## Failures and decisions (student)

One row per failing test. Decision is "Accepted" (the test is right; the builder fixes the code) or "Rejected" (the test is wrong; the tester fixes the test). Add the commit with the fix.

| Test | Cause | Decision | Fixed in commit |
| --- | --- | --- | --- |
| `test_repeated_fits_are_reproducible` (Run 1) | Exact probability-array equality failed on a single element differing by approximately `2.8e-17`; predictions and model coefficients matched. | Rejected as a test assertion issue: floating-point probability results should be compared with tolerance. Changed to `assert_allclose`; no implementation defect. | N/A — tester assertion correction |
| `test_temporal_training_uses_only_training_partition` (Run 2) | Exact probability-array equality failed on values differing by approximately `1.4e-17`; predictions matched. | Rejected as a test assertion issue: changed to `assert_allclose` to allow floating-point rounding; no implementation defect. | N/A — tester assertion correction |

## Runs (added by `python harness.py test N`; do not edit)

### Run 1: FAILED

- Time: 2026-11-12T16:41:25+00:00
- Commit: 47fdf33
- Result: 1 failed, 8 passed in 2.95s
- Files: test_step4_tester.py

```
============================= test session starts ==============================
platform linux -- Python 3.14.2, pytest-9.2.0, pluggy-1.7.0 -- /home/codespace/.python/current/bin/python
cachedir: .pytest_cache
rootdir: /workspaces/Project2v2/project2-harness2
configfile: pytest.ini
plugins: platformdirs-4.14.0, anyio-4.15.1
collecting ... collected 9 items

tests/test_step4_tester.py::test_factory_returns_the_two_planned_classifiers_with_fixed_seed PASSED [ 11%]
tests/test_step4_tester.py::test_train_fits_both_models_and_returns_consistent_metadata PASSED [ 22%]
tests/test_step4_tester.py::test_repeated_fits_are_reproducible FAILED   [ 33%]
tests/test_step4_tester.py::test_temporal_training_uses_only_training_partition PASSED [ 44%]
tests/test_step4_tester.py::test_rejects_empty_or_inconsistent_training_input[features0-labels0-must not be empty] PASSED [ 55%]
tests/test_step4_tester.py::test_rejects_empty_or_inconsistent_training_input[features1-labels1-equal row counts] PASSED [ 66%]
tests/test_step4_tester.py::test_rejects_empty_or_inconsistent_training_input[features2-labels2-encoded as 0 or 1] PASSED [ 77%]
tests/test_step4_tester.py::test_rejects_empty_or_inconsistent_training_input[features3-labels3-encoded as 0 or 1] PASSED [ 88%]
tests/test_step4_tester.py::test_single_class_training_failure_is_surfaced PASSED [100%]

=================================== FAILURES ===================================
_____________________ test_repeated_fits_are_reproducible ______________________

    def test_repeated_fits_are_reproducible():
        features, labels = _training_data()
        first = train_classifiers(features, labels, training_years=(2014, 2015))
        second = train_classifiers(features, labels, training_years=(2014, 2015))
    
        np.testing.assert_array_equal(
            first.logistic_regression.predict(features),
            second.logistic_regression.predict(features),
        )
        np.testing.assert_allclose(
            first.logistic_regression.coef_, second.logistic_regression.coef_
        )
        np.testing.assert_array_equal(
            first.random_forest.predict(features), second.random_forest.predict(features)
        )
>       np.testing.assert_array_equal(
            first.random_forest.predict_proba(features),
            second.random_forest.predict_proba(features),
        )
E       AssertionError: 
E       Arrays are not equal
E       
E       Mismatched elements: 1 / 16 (6.25%)
E       Mismatch at index:
E        [4, 1]: 0.22983333333333333 (ACTUAL), 0.2298333333333333 (DESIRED)
E       Max absolute difference among violations: 2.77555756e-17
E       Max relative difference among violations: 1.20763926e-16
E        ACTUAL: array([[0.755667, 0.244333],
E              [0.752833, 0.247167],
E              [0.298333, 0.701667],...
E        DESIRED: array([[0.755667, 0.244333],
E              [0.752833, 0.247167],
E              [0.298333, 0.701667],...

tests/test_step4_tester.py:85: AssertionError
==================================== PASSES ====================================
=========================== short test summary info ============================
PASSED tests/test_step4_tester.py::test_factory_returns_the_two_planned_classifiers_with_fixed_seed
PASSED tests/test_step4_tester.py::test_train_fits_both_models_and_returns_consistent_metadata
PASSED tests/test_step4_tester.py::test_temporal_training_uses_only_training_partition
PASSED tests/test_step4_tester.py::test_rejects_empty_or_inconsistent_training_input[features0-labels0-must not be empty]
PASSED tests/test_step4_tester.py::test_rejects_empty_or_inconsistent_training_input[features1-labels1-equal row counts]
PASSED tests/test_step4_tester.py::test_rejects_empty_or_inconsistent_training_input[features2-labels2-encoded as 0 or 1]
PASSED tests/test_step4_tester.py::test_rejects_empty_or_inconsistent_training_input[features3-labels3-encoded as 0 or 1]
PASSED tests/test_step4_tester.py::test_single_class_training_failure_is_surfaced
FAILED tests/test_step4_tester.py::test_repeated_fits_are_reproducible - Asse...
========================= 1 failed, 8 passed in 2.95s ==========================
```

### Run 2: FAILED

- Time: 2026-11-12T16:41:36+00:00
- Commit: 47fdf33
- Result: 1 failed, 8 passed in 2.87s
- Files: test_step4_tester.py

```
============================= test session starts ==============================
platform linux -- Python 3.14.2, pytest-9.2.0, pluggy-1.7.0 -- /home/codespace/.python/current/bin/python
cachedir: .pytest_cache
rootdir: /workspaces/Project2v2/project2-harness2
configfile: pytest.ini
plugins: platformdirs-4.14.0, anyio-4.15.1
collecting ... collected 9 items

tests/test_step4_tester.py::test_factory_returns_the_two_planned_classifiers_with_fixed_seed PASSED [ 11%]
tests/test_step4_tester.py::test_train_fits_both_models_and_returns_consistent_metadata PASSED [ 22%]
tests/test_step4_tester.py::test_repeated_fits_are_reproducible PASSED   [ 33%]
tests/test_step4_tester.py::test_temporal_training_uses_only_training_partition FAILED [ 44%]
tests/test_step4_tester.py::test_rejects_empty_or_inconsistent_training_input[features0-labels0-must not be empty] PASSED [ 55%]
tests/test_step4_tester.py::test_rejects_empty_or_inconsistent_training_input[features1-labels1-equal row counts] PASSED [ 66%]
tests/test_step4_tester.py::test_rejects_empty_or_inconsistent_training_input[features2-labels2-encoded as 0 or 1] PASSED [ 77%]
tests/test_step4_tester.py::test_rejects_empty_or_inconsistent_training_input[features3-labels3-encoded as 0 or 1] PASSED [ 88%]
tests/test_step4_tester.py::test_single_class_training_failure_is_surfaced PASSED [100%]

=================================== FAILURES ===================================
_____________ test_temporal_training_uses_only_training_partition ______________

    def test_temporal_training_uses_only_training_partition():
        first_split = create_temporal_split(_yearly_data())
        altered_holdout_split = replace(
            first_split,
            X_validation=first_split.X_validation + 100_000,
            y_validation=1 - first_split.y_validation,
            X_test=first_split.X_test - 100_000,
            y_test=1 - first_split.y_test,
        )
    
        first = train_from_temporal_split(first_split)
        altered = train_from_temporal_split(altered_holdout_split)
        probe = first_split.X_train
    
        assert first.training_years == (2014, 2015, 2016, 2017)
        assert first.training_rows == len(first_split.y_train)
        for name in ("logistic_regression", "random_forest"):
            first_model = getattr(first, name)
            altered_model = getattr(altered, name)
            np.testing.assert_array_equal(
                first_model.predict(probe), altered_model.predict(probe)
            )
>           np.testing.assert_array_equal(
                first_model.predict_proba(probe), altered_model.predict_proba(probe)
            )
E           AssertionError: 
E           Arrays are not equal
E           
E           Mismatched elements: 4 / 32 (12.5%)
E           Mismatch at indices:
E            [3, 0]: 0.04335714285714285 (ACTUAL), 0.043357142857142865 (DESIRED)
E            [7, 0]: 0.04335714285714285 (ACTUAL), 0.043357142857142865 (DESIRED)
E            [11, 0]: 0.04335714285714285 (ACTUAL), 0.043357142857142865 (DESIRED)
E            [15, 0]: 0.04335714285714285 (ACTUAL), 0.043357142857142865 (DESIRED)
E           Max absolute difference among violations: 1.38777878e-17
E           Max relative difference among violations: 3.20080773e-16
E            ACTUAL: array([[0.947183, 0.052817],
E                  [0.913357, 0.086643],
E                  [0.047183, 0.952817],...
E            DESIRED: array([[0.947183, 0.052817],
E                  [0.913357, 0.086643],
E                  [0.047183, 0.952817],...

tests/test_step4_tester.py:113: AssertionError
==================================== PASSES ====================================
=========================== short test summary info ============================
PASSED tests/test_step4_tester.py::test_factory_returns_the_two_planned_classifiers_with_fixed_seed
PASSED tests/test_step4_tester.py::test_train_fits_both_models_and_returns_consistent_metadata
PASSED tests/test_step4_tester.py::test_repeated_fits_are_reproducible
PASSED tests/test_step4_tester.py::test_rejects_empty_or_inconsistent_training_input[features0-labels0-must not be empty]
PASSED tests/test_step4_tester.py::test_rejects_empty_or_inconsistent_training_input[features1-labels1-equal row counts]
PASSED tests/test_step4_tester.py::test_rejects_empty_or_inconsistent_training_input[features2-labels2-encoded as 0 or 1]
PASSED tests/test_step4_tester.py::test_rejects_empty_or_inconsistent_training_input[features3-labels3-encoded as 0 or 1]
PASSED tests/test_step4_tester.py::test_single_class_training_failure_is_surfaced
FAILED tests/test_step4_tester.py::test_temporal_training_uses_only_training_partition
========================= 1 failed, 8 passed in 2.87s ==========================
```

### Run 3: PASSED

- Time: 2026-11-12T16:41:48+00:00
- Commit: 47fdf33
- Result: 9 passed in 2.71s
- Files: test_step4_tester.py

```
============================= test session starts ==============================
platform linux -- Python 3.14.2, pytest-9.2.0, pluggy-1.7.0 -- /home/codespace/.python/current/bin/python
cachedir: .pytest_cache
rootdir: /workspaces/Project2v2/project2-harness2
configfile: pytest.ini
plugins: platformdirs-4.14.0, anyio-4.15.1
collecting ... collected 9 items

tests/test_step4_tester.py::test_factory_returns_the_two_planned_classifiers_with_fixed_seed PASSED [ 11%]
tests/test_step4_tester.py::test_train_fits_both_models_and_returns_consistent_metadata PASSED [ 22%]
tests/test_step4_tester.py::test_repeated_fits_are_reproducible PASSED   [ 33%]
tests/test_step4_tester.py::test_temporal_training_uses_only_training_partition PASSED [ 44%]
tests/test_step4_tester.py::test_rejects_empty_or_inconsistent_training_input[features0-labels0-must not be empty] PASSED [ 55%]
tests/test_step4_tester.py::test_rejects_empty_or_inconsistent_training_input[features1-labels1-equal row counts] PASSED [ 66%]
tests/test_step4_tester.py::test_rejects_empty_or_inconsistent_training_input[features2-labels2-encoded as 0 or 1] PASSED [ 77%]
tests/test_step4_tester.py::test_rejects_empty_or_inconsistent_training_input[features3-labels3-encoded as 0 or 1] PASSED [ 88%]
tests/test_step4_tester.py::test_single_class_training_failure_is_surfaced PASSED [100%]

==================================== PASSES ====================================
=========================== short test summary info ============================
PASSED tests/test_step4_tester.py::test_factory_returns_the_two_planned_classifiers_with_fixed_seed
PASSED tests/test_step4_tester.py::test_train_fits_both_models_and_returns_consistent_metadata
PASSED tests/test_step4_tester.py::test_repeated_fits_are_reproducible
PASSED tests/test_step4_tester.py::test_temporal_training_uses_only_training_partition
PASSED tests/test_step4_tester.py::test_rejects_empty_or_inconsistent_training_input[features0-labels0-must not be empty]
PASSED tests/test_step4_tester.py::test_rejects_empty_or_inconsistent_training_input[features1-labels1-equal row counts]
PASSED tests/test_step4_tester.py::test_rejects_empty_or_inconsistent_training_input[features2-labels2-encoded as 0 or 1]
PASSED tests/test_step4_tester.py::test_rejects_empty_or_inconsistent_training_input[features3-labels3-encoded as 0 or 1]
PASSED tests/test_step4_tester.py::test_single_class_training_failure_is_surfaced
============================== 9 passed in 2.71s ===============================
```
