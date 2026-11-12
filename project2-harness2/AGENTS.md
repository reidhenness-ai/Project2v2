# AGENTS.md: Project 2 context for all agents

Every builder, reviewer, and tester session reads this file first. The assignment and the seven-step plan are in `ASSIGNMENT.md` and `PLAN.md`.

## Project goal

Classify Android apps as malware or goodware from API-call features, measure how feature distributions change over 2014-2021, and compare a periodically updated classifier with a model that is not updated.

## Dataset and labels

- CSV files are in `input_data/`; this directory is excluded from Git. Do not edit the supplied data.
- There are 16 files named `sampled_<year>_<class>_api.csv`, with years 2014 through 2021 and one file each for `benign` and `malware` per year.
- The first column is `apkname` and must be discarded. The remaining 1,848 columns are API-call features.
- All files have 1,849 columns including the first column. The supplied 2014-2018 files each contain 9,000 data rows; the 2019-2021 files each contain 1,500 data rows. This differs from the assignment's stated 1,500 rows per file. Validate counts from the files and report this discrepancy rather than assuming equal row counts.
- Derive the target from the filename: `malware` is `1` and `benign` (goodware) is `0`. Malware is the positive class for precision, recall, and F1.
- Inspect data types, missing values, and feature values during data preparation; report unexpected values instead of silently discarding data. Do not assume the full dataset's values based on a sample.

## Folder layout

- `input_data/`: supplied CSV data; excluded from Git.
- `src/`: project implementation, written by the builder.
- `tests/`: `test_stepN_*.py` and `stepN_test_log.md`; tests/logs are produced by the tester and harness, with student decisions recorded where required.
- `docs/`: one builder report for each of Steps 1-7.
- `reviews/`: reviewer reports and the student's decision logs.
- `transcripts/`: full session transcripts saved by the harness or exported from the agent tool; do not edit transcripts except to remove secrets or personal information.
- `harness/`, `harness.py`, `hooks/`, `roles/`, and `templates/`: provided project workflow tools and prompts.
- `ASSIGNMENT.md`: authoritative requirements; `PLAN.md`: implementation and validation plan; `README.md`: run instructions and agent/model record; `REPORT.md` and `REFLECTION.md`: student-written submission materials.

## Coding conventions

- Use Python 3 and the dependencies in `requirements.txt` (pandas, numpy, scikit-learn, scipy, pytest). Ask before adding dependencies.
- Use clear names, function docstrings, and comments for major processing steps. Keep code organized in focused modules under `src/`.
- Use `random_state=42` wherever randomness is involved. Avoid absolute paths; resolve paths relative to the project root.
- Validate schemas, labels, missing values, and unexpected feature values. Never silently discard data.
- Split by year. Fit scalers, feature selection, and models only on years available to that training stage, then apply them unchanged to later validation/test years. Never train or tune on final test years.
- Keep malware encoded as `1` and goodware as `0` throughout metrics and reports.

## How to run

- From this directory, the planned full-project command is `python -m src.main` (available after the builder implements it).
- Run one test step with `python harness.py test N`, or all tests with `python harness.py test all`.
- Run the relevant tests after each major code change and record results in the matching test log. All project commands should work from this directory.

## Agent and Git workflow

- Use separate fresh sessions for builder, reviewer, and tester as required by `ASSIGNMENT.md`; reviewer/tester sessions must not receive the builder's conversation.
- The builder writes implementation and step reports; reviewer writes review findings; tester writes tests and test logs. The student records decisions and owns `README.md`, `REPORT.md`, and `REFLECTION.md`.
- Commit each completed task with a message beginning with `[builder]`, `[reviewer]`, `[tester]`, or `[student]`. Do not squash or rewrite history.