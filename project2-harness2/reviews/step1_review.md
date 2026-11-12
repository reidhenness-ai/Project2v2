# Step 1 Review

## Summary

The current Step 1 implementation is largely correct for the supplied dataset: it removes the first column, extracts year and target from the filename, encodes malware as `1` and benign as `0`, and concatenates rows by year. I did not find a correctness bug in the current `input_data/` contents, but I did identify two issues that should be fixed to align the implementation with the project requirements and make it robust to incomplete or malformed datasets.

## Issues

### 1) Missing validation that the full expected dataset inventory is present

- Description: `load_yearly_data()` loads every CSV found in `input_data/` but never verifies that the directory contains the exact expected inventory: 16 files covering years 2014-2021 with both `benign` and `malware` files for each year. Because it uses `directory.glob("*.csv")` and then iterates over whatever matches, a missing file, extra file, or renamed file would be silently ignored. This can mask data loss or a bad environment without producing a clear error.
- Severity: medium
- File and location: `src/data.py`, `load_yearly_data()` (`src/data.py:35-89`); the discovery step is `files = sorted(directory.glob("*.csv"))` and there is no comparison against the expected set.
- Recommended fix: After discovering the CSVs, build the expected set of file names for 2014-2021 and each class (`benign`, `malware`), compare it to the actual list, and raise a `ValueError` or `FileNotFoundError` if any expected file is missing or if unexpected files are present. That keeps the loader aligned with the project requirement to validate the dataset inventory rather than assuming success.

### 2) Step 1 verification artifacts are missing even though the project plan requires them

- Description: The project plan and instructions require Step 1 to include both a data-loading test file and a test log, but no Step 1 pytest file or log exists in `tests/`. The only file currently present is shared setup fixture code (`tests/conftest.py`), which does not exercise the Step 1 loader or verify that the first column is removed, labels are extracted correctly, or the row/column counts match the data. This makes it easy for a silent data issue to slip through without a failing test.
- Severity: medium
- File and location: `tests/` (no Step 1 tests exist); the current relevant file is `tests/conftest.py` (`tests/conftest.py:1-19`), which sets up the path but does not contain Step 1 assertions.
- Recommended fix: Add tests such as `tests/test_step1_data_loading.py` that assert the expected 16-file discovery, exact per-year counts, first-column removal, label mapping (`malware=1`, `benign=0`), and consistent feature schema. Also save the Step 1 test output in `tests/step1_test_log.md` as described in the plan.

## Decision Log

- Comment 1: Accepted
______________________________________________________
- Comment 2: Accepted  
______________________________________________________

