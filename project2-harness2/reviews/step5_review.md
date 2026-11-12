# Step 5 Review: Evaluate Classifier Performance

## Summary

The evaluator calculates accuracy, precision, recall, and F1 with malware
(`1`) explicitly positive. It reports pooled and per-year rows, checks that
training years precede test years, and does not use validation/test labels to
fit models.

This was a code inspection only; I did not run tests or execute the evaluation
command.

## Issues

### 1) Final models are not refitted on the validation year before testing

- **Description:** The plan specifies that after model choices are fixed, final
  preprocessing and models should be refitted using 2014-2018 before evaluation
  on the untouched 2019-2021 test years. However, `evaluation.main()` calls
  `train_from_temporal_split(split)`, which passes only `split.X_train` and
  `split.y_train` to the classifiers; those contain 2014-2017. The report also
  confirms the evaluated models use only 2014-2017. This leaves 2018 out of the
  final fit, contrary to the planned protocol.
- **Severity:** medium
- **File and location:** `src/evaluation.py`, `main()` at the call to
  `train_from_temporal_split(split)`; `src/models.py`, `train_from_temporal_split()`;
  `docs/step5_evaluation.md`, paragraph stating models were trained on
  2014-2017.
- **Recommended fix:** Once model choices are fixed, fit a final scaler and
  both classifiers using 2014-2018, then transform and evaluate 2019-2021
  without refitting on test data. Keep the existing 2014-2017/2018 split for
  model selection, if any, separate from this final-fit path, and update the
  report to state the actual final training years.

## Decision Log

- Comment 1: Accepted — Added a final evaluation data path that refits
  `StandardScaler` and both classifiers on 2014-2018 after model choices were
  fixed, then transforms and evaluates 2019-2021 without fitting on test data.
  Updated the report with the new pooled and per-year metrics. The evaluation
  command completed; tests were left for the tester to rerun.

