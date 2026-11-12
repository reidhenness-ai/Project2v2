# Step 7 Review: Sustainable ML Approach

## Summary

The implementation follows the planned time-forward protocol. The static
baseline remains trained through 2018; the periodic strategy uses that same
fit for 2019, adds 2019 labels before predicting 2020, and adds 2019-2020
labels before predicting 2021. Each window refits its scaler and classifiers
only on the specified training years, and both approaches are scored on the
same respective test year. The report's performance and drift interpretation
is appropriately cautious.

This was a code and artifact inspection only; I did not run tests or execute
the comparison command. I found no Step 7 training-window or data-leakage
defect.

## Issues

### 1) The Step 7 test log still points to a placeholder tester transcript

- **Description:** The test log records tester results, but the transcript
  field remains `transcripts/NN_YYYY-MM-DD_tester_stepN.md`. This does not
  identify the actual tester session transcript required by the project
  workflow.
- **Severity:** low
- **File and location:** `tests/step7_test_log.md:3`.
- **Recommended fix:** Save the tester session transcript under
  `transcripts/` and replace the placeholder with its actual path.

## Decision Log

- Comment 1: [ ] Accepted / [ ] Rejected — Reason: ______________________________________________________

