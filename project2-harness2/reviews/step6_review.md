# Step 6 Review: Test Data Prediction

## Summary

The Step 6 path uses the final evaluation split: the scaler and both
classifiers are fitted on 2014-2018, and the 2019-2021 data is held out for
prediction and reporting. The evaluator reports accuracy, precision, recall,
and F1 by test year, identifies malware (`1`) as the positive class, and
includes actual and predicted class counts. The drift discussion is cautious
and does not claim that drift caused performance changes.

This was a code and artifact inspection only; I did not run tests or execute
the prediction command. I found no Step 6 prediction or data-leakage defect.

## Issues

### 1) The Step 6 test log still points to a placeholder tester transcript

- **Description:** The test log records tester results, but its transcript
  field remains `transcripts/NN_YYYY-MM-DD_tester_stepN.md`. The project
  requires the tester session transcript to be saved and identified; the
  placeholder does not identify a usable transcript.
- **Severity:** low
- **File and location:** `tests/step6_test_log.md:3`.
- **Recommended fix:** Save the actual tester session transcript under
  `transcripts/` and replace the placeholder with its path.

## Decision Log

- Comment 1: [ ] Accepted / [ ] Rejected — Reason: ______________________________________________________

