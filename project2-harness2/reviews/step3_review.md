# Step 3 Review: Preprocess Data for Model Training

## Summary

The preprocessing implementation matches the Step 3 plan. It creates
chronological, disjoint training (2014-2017), validation (2018), and test
(2019-2021) sets; excludes the target and year metadata from features; and fits
`StandardScaler` only on training rows. The staged loader validates the full
file inventory and schemas while loading feature rows a split at a time.

Code inspection found no Step 3 data-leakage or scaling correctness issue.
Process note: I also ran tests and the preprocessing command before receiving
the instruction to keep reviewer work to code review; that was outside the
requested reviewer role and is not part of this review's findings.

## Issues

### 1) The required independent tester session is not recorded

- **Description:** The Step 3 test log still contains a placeholder tester
  transcript path (`NN_YYYY-MM-DD_tester_stepN.md`), and the Step 3 commit
  includes the tests and test log under the builder role. The provided
  StepThreeTranscript records the builder running tests, but does not show the
  required separate tester session or its transcript. This does not invalidate
  the passing tests, but it does not demonstrate the independent tester
  workflow required by the assignment.
- **Severity:** medium
- **File and location:** `tests/step3_test_log.md:3`; Step 3 test artifacts in
  commit `d61083c` (`tests/test_step3_preprocessing.py`,
  `tests/step3_test_log.md`); `transcripts/StepThreeTranscript.txt`.
- **Recommended fix:** Have a fresh tester session, without the builder's
  conversation, independently review the assignment, `AGENTS.md`, and
  `PLAN.md`, write/run its Step 3 tests, save the actual tester transcript, and
  replace the placeholder with that transcript's path. Record any test failures
  and their dispositions in the log.

## Decision Log

- Comment 1: [ ] Accepted / [ ] Rejected — Reason: ______________________________________________________

