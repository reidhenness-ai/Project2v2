# Project Plan

This plan follows `ASSIGNMENT.md`. Step 0 is setup and plan review; Steps 1-7 are the project work. No implementation is included in this planning document.

## Data split and leakage controls

- Use 2014-2017 as the initial training years and 2018 as the validation year for model and hyperparameter choices.
- After choices are fixed, refit the final preprocessing and models using 2014-2018, then evaluate on the untouched 2019, 2020, and 2021 test years. Report metrics separately for each test year and pooled across those years.
- The validation year may be included in the final training fit only after model choices are fixed. Do not use any test-year rows or labels for fitting, feature selection, scaling, or model selection.
- For periodic-retraining comparisons, the static baseline remains fitted through 2018. The updated model may use labels from 2019 before predicting 2020 and labels through 2020 before predicting 2021. At every evaluation point, the predicted year is strictly later than all years used to fit that model.
- Drift analysis is descriptive. It must not choose features or tune models based on final test-year outcomes. Any learned transformation is fitted using only the training years available at that point.

## Step 1: Prepare the data

- **Approach:** Load every `sampled_<year>_<benign|malware>_api.csv`, derive year and target from the filename, discard `apkname` (the first column), validate the remaining feature schema, and concatenate files by year. Record actual row counts, feature types, missing values, and unexpected values. The observed 2014-2018 files have 9,000 rows each and 2019-2021 files have 1,500 rows each, despite the assignment's uniform 1,500-row description.
- **Planned code:** `src/data.py` will expose filename parsing and loading functions that return per-year feature/target data with consistent feature columns, plus year metadata. No file in `input_data/` is modified.
- **Outputs:** `docs/step1_data_summary.md`; tester adds `tests/test_step1_*.py` and `tests/step1_test_log.md`.
- **Tests:** Verify all 16 files are discovered; labels map malware to 1 and benign to 0; first-column values are absent; feature counts and actual per-file row counts match inspection; schemas align across files; malformed names, missing values, and unexpected values are surfaced clearly.

## Step 2: Handle data drift

- **Approach:** Compare yearly feature distributions using per-feature two-sample Kolmogorov-Smirnov tests, using 2014 as a reference and reporting effect sizes as well as significance. Analyze within each class as well as overall to reduce confusion between changing class mix and feature drift. Correct for multiple feature-wise tests (Benjamini-Hochberg) and identify features/years with the largest supported changes. Interpret these tests as feature-distribution drift, not proof of concept drift.
- **Planned code:** `src/drift.py` will accept prepared per-year data and return a structured table of year comparisons, feature statistics, effect sizes, and adjusted p-values.
- **Outputs:** `docs/step2_drift_analysis.md`; tester adds `tests/test_step2_*.py` and `tests/step2_test_log.md`.
- **Tests:** Check statistic/effect bounds, identical distributions, shifted synthetic features, class-stratified comparisons, and constant or invalid features.

## Step 3: Preprocess for model training

- **Approach:** Establish a year-aware split with training 2014-2017 and validation 2018. Use a scikit-learn pipeline so the scaler is fitted only on its training input and applied without refitting to validation data. After model selection, refit preprocessing on 2014-2018 for the final 2019-2021 evaluation.
- **Planned code:** `src/preprocessing.py` will construct the chronological train/validation/test datasets and preprocessing pipeline while preserving feature order and year labels.
- **Outputs:** `docs/step3_preprocessing.md`; tester adds `tests/test_step3_*.py` and `tests/step3_test_log.md`.
- **Tests:** Assert no year overlap across initial train and validation/test; feature order matches; fitted scaler statistics come only from training data; and later data is transformed, not used to refit.

## Step 4: Apply classifiers

- **Approach:** Implement at least Logistic Regression and Random Forest from scikit-learn. Select any hyperparameters using only the 2018 validation year; then freeze choices and fit final models on 2014-2018. Use reproducible settings (`random_state=42` where supported) and account for class balance where inspection warrants it.
- **Planned code:** `src/models.py` will create, fit, and expose the classifier pipelines using the prepared split.
- **Outputs:** `docs/step4_models.md`; tester adds `tests/test_step4_*.py` and `tests/step4_test_log.md`.
- **Tests:** Fit each classifier on a small synthetic dataset; check prediction shape and labels, deterministic behavior, and that fitting uses only the supplied training years.

## Step 5: Evaluate classifier performance

- **Approach:** Evaluate only on final held-out years. Report accuracy as the primary metric and precision, recall, and F1 with malware (`1`) as the positive class. Include per-year and pooled results so aggregate performance does not obscure temporal changes.
- **Planned code:** `src/evaluation.py` will compute the agreed metrics from true labels and predictions and return results keyed by classifier and test year.
- **Outputs:** `docs/step5_evaluation.md`; tester adds `tests/test_step5_*.py` and `tests/step5_test_log.md`.
- **Tests:** Compare metric output with hand-checked predictions and scikit-learn; verify positive-class semantics and that evaluation inputs are held-out predictions.

## Step 6: Predict on drifted test data

- **Approach:** Apply each final model, fitted through 2018, to each untouched test year (2019-2021). Summarize metrics and prediction counts separately by year, then discuss temporal changes alongside Step 2 drift findings without claiming causation.
- **Planned code:** `src/evaluation.py` will provide per-year prediction/evaluation; `src/main.py` will coordinate the end-to-end run and output reports/results.
- **Outputs:** `docs/step6_test_results.md`; tester adds `tests/test_step6_*.py` and `tests/step6_test_log.md`.
- **Tests:** Require one result per classifier and test year; verify metric bounds, year grouping, and that no model has seen its prediction year during fitting.

## Step 7: Test a sustainable approach

- **Approach:** Compare a never-updated baseline fitted through 2018 with an expanding-window periodic-retraining strategy. Before predicting 2020, the updated model may train on 2019; before predicting 2021, it may train on 2019-2020. Keep each prediction year held out from its own model fit, and use the same test years and metrics for fair comparison. Refit preprocessing within each training window.
- **Planned code:** `src/sustainable.py` will implement the time-forward evaluation protocol and return baseline/updated metrics by year; `src/main.py` will include these results in the project run.
- **Outputs:** `docs/step7_sustainable_approach.md`; tester adds `tests/test_step7_*.py` and `tests/step7_test_log.md`.
- **Tests:** Assert all training years precede the prediction year; updated fits use newly available years; baseline fit years remain fixed; and comparisons use identical years and metrics.

## Step 0 process and shared validation

- Review this plan in a fresh reviewer session using only `ASSIGNMENT.md`, `AGENTS.md`, and `PLAN.md`. Save findings in `reviews/step0_plan_review.md`, record a reasoned decision for every comment, revise the plan for accepted findings, and retain the original and revised plan in Git history before starting Step 1.
- Use separate fresh builder, reviewer, and tester sessions for each required cycle. Save each full transcript under `transcripts/` using the harness naming convention. Do not treat agent-reported outcomes as verified until independently checked.
- For each of Steps 1-7, save a builder report under `docs/`, reviewer report under `reviews/`, tester code and log under `tests/`, and transcripts for all three roles. Complete at least one build-review-test-fix cycle per step, record decisions for every review comment and test failure, and commit completed tasks with role-tagged messages.
- Run focused tests after each change and `python harness.py check` before submission. The builder's planned full-run command is `python -m src.main`; the test commands are `python harness.py test N` and `python harness.py test all`.
