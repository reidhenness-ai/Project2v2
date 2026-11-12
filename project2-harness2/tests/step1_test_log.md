# Step 1 Test Log: Prepare the Data

- Tester transcript: transcripts/NN_YYYY-MM-DD_tester_step1.md

## Tests written (tester)

| Test | What it checks (from the assignment or plan) |
| --- | --- |
| `test_step1_loads_synthetic_files_drops_ids_encodes_labels_and_combines_years` | Uses controlled input data to check file loading, first-column removal, malware/goodware encoding, and per-year concatenation and row order. |
| `test_step1_extracts_year_and_label_from_filename` | Checks filename-derived years and benign=0/malware=1 labels. |
| `test_step1_rejects_unrecognized_dataset_filename` | Checks that an unsupported filename is reported instead of silently labeled. |
| `test_step1_surfaces_missing_or_unexpected_feature_values` | Checks that missing, non-numeric, negative, and non-integer feature values are surfaced. |
| `test_step1_each_original_file_has_1500_rows` | Checks each of the 16 original files against the assignment's stated 1,500-row requirement and confirms its original 1,849-column schema. |
| `test_step1_combines_every_real_file_with_expected_shapes_labels_and_no_input_changes` | Loads and checks all 16 real inputs, per-year row/column and class counts, feature alignment and sample values, and SHA-256 preservation of inputs. |

## Commands used

- `python harness.py test 1` from the workspace root: did not start because `harness.py` is in `project2-harness2/`.
- `cd project2-harness2 && python harness.py test 1`: initially could not start because pytest was not installed.
- `python -m pip install -r project2-harness2/requirements.txt`: installed the declared test/runtime dependencies.
- `cd project2-harness2 && python harness.py test 1`: ran the test suite and appended the output below.
- `cd project2-harness2 && python harness.py test 1` (asynchronous rerun): completed the full-data check after the preceding harness process was terminated while that check was running.

## Failures and decisions (student)

One row per failing test. Decision is "Accepted" (the test is right; the builder fixes the code) or "Rejected" (the test is wrong; the tester fixes the test). Add the commit with the fix.

| Test | Cause | Decision | Fixed in commit |
| --- | --- | --- | --- |
| `test_step1_each_original_file_has_1500_rows[sampled_2014_benign_api.csv]` | This input contains 9,000 data rows; the assignment says 1,500. | Accepted: the asserted assignment requirement is not met by the supplied file; report the discrepancy without changing input data. | N/A — input/assignment discrepancy |
| `test_step1_each_original_file_has_1500_rows[sampled_2014_malware_api.csv]` | This input contains 9,000 data rows; the assignment says 1,500. | Accepted: the asserted assignment requirement is not met by the supplied file; report the discrepancy without changing input data. | N/A — input/assignment discrepancy |
| `test_step1_each_original_file_has_1500_rows[sampled_2015_benign_api.csv]` | This input contains 9,000 data rows; the assignment says 1,500. | Accepted: the asserted assignment requirement is not met by the supplied file; report the discrepancy without changing input data. | N/A — input/assignment discrepancy |
| `test_step1_each_original_file_has_1500_rows[sampled_2015_malware_api.csv]` | This input contains 9,000 data rows; the assignment says 1,500. | Accepted: the asserted assignment requirement is not met by the supplied file; report the discrepancy without changing input data. | N/A — input/assignment discrepancy |
| `test_step1_each_original_file_has_1500_rows[sampled_2016_benign_api.csv]` | This input contains 9,000 data rows; the assignment says 1,500. | Accepted: the asserted assignment requirement is not met by the supplied file; report the discrepancy without changing input data. | N/A — input/assignment discrepancy |
| `test_step1_each_original_file_has_1500_rows[sampled_2016_malware_api.csv]` | This input contains 9,000 data rows; the assignment says 1,500. | Accepted: the asserted assignment requirement is not met by the supplied file; report the discrepancy without changing input data. | N/A — input/assignment discrepancy |
| `test_step1_each_original_file_has_1500_rows[sampled_2017_benign_api.csv]` | This input contains 9,000 data rows; the assignment says 1,500. | Accepted: the asserted assignment requirement is not met by the supplied file; report the discrepancy without changing input data. | N/A — input/assignment discrepancy |
| `test_step1_each_original_file_has_1500_rows[sampled_2017_malware_api.csv]` | This input contains 9,000 data rows; the assignment says 1,500. | Accepted: the asserted assignment requirement is not met by the supplied file; report the discrepancy without changing input data. | N/A — input/assignment discrepancy |
| `test_step1_each_original_file_has_1500_rows[sampled_2018_benign_api.csv]` | This input contains 9,000 data rows; the assignment says 1,500. | Accepted: the asserted assignment requirement is not met by the supplied file; report the discrepancy without changing input data. | N/A — input/assignment discrepancy |
| `test_step1_each_original_file_has_1500_rows[sampled_2018_malware_api.csv]` | This input contains 9,000 data rows; the assignment says 1,500. | Accepted: the asserted assignment requirement is not met by the supplied file; report the discrepancy without changing input data. | N/A — input/assignment discrepancy |
| Harness Run 4 (execution interruption, not an assertion failure) | The process was terminated while `test_step1_combines_every_real_file_with_expected_shapes_labels_and_no_input_changes` was running; the captured output contains no test failure or traceback. | Reran the same suite asynchronously; Run 5 completed with all 27 tests passing. | N/A — runner interruption |

## Runs (added by `python harness.py test 1`; do not edit)

### Run 1: FAILED

- Time: 2026-11-04T16:38:33+00:00
- Commit: 3264736
- Result: 10 failed, 15 passed in 25.25s
- Files: test_step1_data.py

```
... (213 earlier lines omitted)
    
        with path.open(newline="", encoding="utf-8") as source:
            header = next(csv.reader(source))
        assert len(header) == 1849
    
        with path.open(newline="", encoding="utf-8") as source:
            row_count = sum(1 for _ in csv.reader(source)) - 1
>       assert row_count == 1500
E       assert 9000 == 1500

tests/test_step1_data.py:123: AssertionError
__ test_step1_each_original_file_has_1500_rows[sampled_2017_malware_api.csv] ___

real_data_dir = PosixPath('/workspaces/Project2v2/project2-harness2/input_data')
filename = 'sampled_2017_malware_api.csv'

    @pytest.mark.parametrize(
        "filename",
        [
            f"sampled_{year}_{kind}_api.csv"
            for year in range(2014, 2022)
            for kind in ("benign", "malware")
        ],
    )
    def test_step1_each_original_file_has_1500_rows(real_data_dir, filename):
        path = real_data_dir / filename
        assert path.is_file(), f"Expected dataset file is missing: {filename}"
    
        with path.open(newline="", encoding="utf-8") as source:
            header = next(csv.reader(source))
        assert len(header) == 1849
    
        with path.open(newline="", encoding="utf-8") as source:
            row_count = sum(1 for _ in csv.reader(source)) - 1
>       assert row_count == 1500
E       assert 9000 == 1500

tests/test_step1_data.py:123: AssertionError
___ test_step1_each_original_file_has_1500_rows[sampled_2018_benign_api.csv] ___

real_data_dir = PosixPath('/workspaces/Project2v2/project2-harness2/input_data')
filename = 'sampled_2018_benign_api.csv'

    @pytest.mark.parametrize(
        "filename",
        [
            f"sampled_{year}_{kind}_api.csv"
            for year in range(2014, 2022)
            for kind in ("benign", "malware")
        ],
    )
    def test_step1_each_original_file_has_1500_rows(real_data_dir, filename):
        path = real_data_dir / filename
        assert path.is_file(), f"Expected dataset file is missing: {filename}"
    
        with path.open(newline="", encoding="utf-8") as source:
            header = next(csv.reader(source))
        assert len(header) == 1849
    
        with path.open(newline="", encoding="utf-8") as source:
            row_count = sum(1 for _ in csv.reader(source)) - 1
>       assert row_count == 1500
E       assert 9000 == 1500

tests/test_step1_data.py:123: AssertionError
__ test_step1_each_original_file_has_1500_rows[sampled_2018_malware_api.csv] ___

real_data_dir = PosixPath('/workspaces/Project2v2/project2-harness2/input_data')
filename = 'sampled_2018_malware_api.csv'

    @pytest.mark.parametrize(
        "filename",
        [
            f"sampled_{year}_{kind}_api.csv"
            for year in range(2014, 2022)
            for kind in ("benign", "malware")
        ],
    )
    def test_step1_each_original_file_has_1500_rows(real_data_dir, filename):
        path = real_data_dir / filename
        assert path.is_file(), f"Expected dataset file is missing: {filename}"
    
        with path.open(newline="", encoding="utf-8") as source:
            header = next(csv.reader(source))
        assert len(header) == 1849
    
        with path.open(newline="", encoding="utf-8") as source:
            row_count = sum(1 for _ in csv.reader(source)) - 1
>       assert row_count == 1500
E       assert 9000 == 1500

tests/test_step1_data.py:123: AssertionError
==================================== PASSES ====================================
=========================== short test summary info ============================
PASSED tests/test_step1_data.py::test_step1_loads_synthetic_files_drops_ids_encodes_labels_and_combines_years
PASSED tests/test_step1_data.py::test_step1_extracts_year_and_label_from_filename[sampled_2014_benign_api.csv-expected0]
PASSED tests/test_step1_data.py::test_step1_extracts_year_and_label_from_filename[sampled_2021_malware_api.csv-expected1]
PASSED tests/test_step1_data.py::test_step1_rejects_unrecognized_dataset_filename
PASSED tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[None-missing feature values]
PASSED tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[not-a-count-non-numeric feature values]
PASSED tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[-1-negative API-call counts]
PASSED tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[1.5-non-integer API-call counts]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_1500_rows[sampled_2019_benign_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_1500_rows[sampled_2019_malware_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_1500_rows[sampled_2020_benign_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_1500_rows[sampled_2020_malware_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_1500_rows[sampled_2021_benign_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_1500_rows[sampled_2021_malware_api.csv]
PASSED tests/test_step1_data.py::test_step1_combines_every_real_file_with_expected_shapes_labels_and_no_input_changes
FAILED tests/test_step1_data.py::test_step1_each_original_file_has_1500_rows[sampled_2014_benign_api.csv]
FAILED tests/test_step1_data.py::test_step1_each_original_file_has_1500_rows[sampled_2014_malware_api.csv]
FAILED tests/test_step1_data.py::test_step1_each_original_file_has_1500_rows[sampled_2015_benign_api.csv]
FAILED tests/test_step1_data.py::test_step1_each_original_file_has_1500_rows[sampled_2015_malware_api.csv]
FAILED tests/test_step1_data.py::test_step1_each_original_file_has_1500_rows[sampled_2016_benign_api.csv]
FAILED tests/test_step1_data.py::test_step1_each_original_file_has_1500_rows[sampled_2016_malware_api.csv]
FAILED tests/test_step1_data.py::test_step1_each_original_file_has_1500_rows[sampled_2017_benign_api.csv]
FAILED tests/test_step1_data.py::test_step1_each_original_file_has_1500_rows[sampled_2017_malware_api.csv]
FAILED tests/test_step1_data.py::test_step1_each_original_file_has_1500_rows[sampled_2018_benign_api.csv]
FAILED tests/test_step1_data.py::test_step1_each_original_file_has_1500_rows[sampled_2018_malware_api.csv]
======================== 10 failed, 15 passed in 25.25s ========================
```

### Run 2: PASSED

- Time: 2026-11-04T17:01:47+00:00
- Commit: d3789ee
- Result: 27 passed in 32.37s
- Files: test_step1_data.py

```
============================= test session starts ==============================
platform linux -- Python 3.14.2, pytest-9.2.0, pluggy-1.7.0 -- /home/codespace/.python/current/bin/python
cachedir: .pytest_cache
rootdir: /workspaces/Project2v2/project2-harness2
configfile: pytest.ini
plugins: platformdirs-4.14.0, anyio-4.15.1
collecting ... collected 27 items

tests/test_step1_data.py::test_step1_loads_synthetic_files_drops_ids_encodes_labels_and_combines_years PASSED [  3%]
tests/test_step1_data.py::test_step1_extracts_year_and_label_from_filename[sampled_2014_benign_api.csv-expected0] PASSED [  7%]
tests/test_step1_data.py::test_step1_extracts_year_and_label_from_filename[sampled_2021_malware_api.csv-expected1] PASSED [ 11%]
tests/test_step1_data.py::test_step1_rejects_unrecognized_dataset_filename PASSED [ 14%]
tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[None-missing feature values] PASSED [ 18%]
tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[not-a-count-non-numeric feature values] PASSED [ 22%]
tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[-1-negative API-call counts] PASSED [ 25%]
tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[1.5-non-integer API-call counts] PASSED [ 29%]
tests/test_step1_data.py::test_step1_rejects_missing_expected_file PASSED [ 33%]
tests/test_step1_data.py::test_step1_rejects_unexpected_csv PASSED       [ 37%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2014_benign_api.csv] PASSED [ 40%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2014_malware_api.csv] PASSED [ 44%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2015_benign_api.csv] PASSED [ 48%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2015_malware_api.csv] PASSED [ 51%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2016_benign_api.csv] PASSED [ 55%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2016_malware_api.csv] PASSED [ 59%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2017_benign_api.csv] PASSED [ 62%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2017_malware_api.csv] PASSED [ 66%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2018_benign_api.csv] PASSED [ 70%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2018_malware_api.csv] PASSED [ 74%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2019_benign_api.csv] PASSED [ 77%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2019_malware_api.csv] PASSED [ 81%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2020_benign_api.csv] PASSED [ 85%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2020_malware_api.csv] PASSED [ 88%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2021_benign_api.csv] PASSED [ 92%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2021_malware_api.csv] PASSED [ 96%]
tests/test_step1_data.py::test_step1_combines_every_real_file_with_expected_shapes_labels_and_no_input_changes PASSED [100%]

==================================== PASSES ====================================
=========================== short test summary info ============================
PASSED tests/test_step1_data.py::test_step1_loads_synthetic_files_drops_ids_encodes_labels_and_combines_years
PASSED tests/test_step1_data.py::test_step1_extracts_year_and_label_from_filename[sampled_2014_benign_api.csv-expected0]
PASSED tests/test_step1_data.py::test_step1_extracts_year_and_label_from_filename[sampled_2021_malware_api.csv-expected1]
PASSED tests/test_step1_data.py::test_step1_rejects_unrecognized_dataset_filename
PASSED tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[None-missing feature values]
PASSED tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[not-a-count-non-numeric feature values]
PASSED tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[-1-negative API-call counts]
PASSED tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[1.5-non-integer API-call counts]
PASSED tests/test_step1_data.py::test_step1_rejects_missing_expected_file
PASSED tests/test_step1_data.py::test_step1_rejects_unexpected_csv
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2014_benign_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2014_malware_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2015_benign_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2015_malware_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2016_benign_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2016_malware_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2017_benign_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2017_malware_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2018_benign_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2018_malware_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2019_benign_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2019_malware_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2020_benign_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2020_malware_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2021_benign_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2021_malware_api.csv]
PASSED tests/test_step1_data.py::test_step1_combines_every_real_file_with_expected_shapes_labels_and_no_input_changes
============================= 27 passed in 32.37s ==============================
```

### Run 3: PASSED

- Time: 2026-11-04T17:04:23+00:00
- Commit: bdbeff7
- Result: 27 passed in 30.23s
- Files: test_step1_data.py

```
============================= test session starts ==============================
platform linux -- Python 3.14.2, pytest-9.2.0, pluggy-1.7.0 -- /home/codespace/.python/current/bin/python
cachedir: .pytest_cache
rootdir: /workspaces/Project2v2/project2-harness2
configfile: pytest.ini
plugins: platformdirs-4.14.0, anyio-4.15.1
collecting ... collected 27 items

tests/test_step1_data.py::test_step1_loads_synthetic_files_drops_ids_encodes_labels_and_combines_years PASSED [  3%]
tests/test_step1_data.py::test_step1_extracts_year_and_label_from_filename[sampled_2014_benign_api.csv-expected0] PASSED [  7%]
tests/test_step1_data.py::test_step1_extracts_year_and_label_from_filename[sampled_2021_malware_api.csv-expected1] PASSED [ 11%]
tests/test_step1_data.py::test_step1_rejects_unrecognized_dataset_filename PASSED [ 14%]
tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[None-missing feature values] PASSED [ 18%]
tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[not-a-count-non-numeric feature values] PASSED [ 22%]
tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[-1-negative API-call counts] PASSED [ 25%]
tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[1.5-non-integer API-call counts] PASSED [ 29%]
tests/test_step1_data.py::test_step1_rejects_missing_expected_file PASSED [ 33%]
tests/test_step1_data.py::test_step1_rejects_unexpected_csv PASSED       [ 37%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2014_benign_api.csv] PASSED [ 40%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2014_malware_api.csv] PASSED [ 44%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2015_benign_api.csv] PASSED [ 48%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2015_malware_api.csv] PASSED [ 51%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2016_benign_api.csv] PASSED [ 55%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2016_malware_api.csv] PASSED [ 59%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2017_benign_api.csv] PASSED [ 62%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2017_malware_api.csv] PASSED [ 66%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2018_benign_api.csv] PASSED [ 70%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2018_malware_api.csv] PASSED [ 74%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2019_benign_api.csv] PASSED [ 77%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2019_malware_api.csv] PASSED [ 81%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2020_benign_api.csv] PASSED [ 85%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2020_malware_api.csv] PASSED [ 88%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2021_benign_api.csv] PASSED [ 92%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2021_malware_api.csv] PASSED [ 96%]
tests/test_step1_data.py::test_step1_combines_every_real_file_with_expected_shapes_labels_and_no_input_changes PASSED [100%]

==================================== PASSES ====================================
=========================== short test summary info ============================
PASSED tests/test_step1_data.py::test_step1_loads_synthetic_files_drops_ids_encodes_labels_and_combines_years
PASSED tests/test_step1_data.py::test_step1_extracts_year_and_label_from_filename[sampled_2014_benign_api.csv-expected0]
PASSED tests/test_step1_data.py::test_step1_extracts_year_and_label_from_filename[sampled_2021_malware_api.csv-expected1]
PASSED tests/test_step1_data.py::test_step1_rejects_unrecognized_dataset_filename
PASSED tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[None-missing feature values]
PASSED tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[not-a-count-non-numeric feature values]
PASSED tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[-1-negative API-call counts]
PASSED tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[1.5-non-integer API-call counts]
PASSED tests/test_step1_data.py::test_step1_rejects_missing_expected_file
PASSED tests/test_step1_data.py::test_step1_rejects_unexpected_csv
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2014_benign_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2014_malware_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2015_benign_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2015_malware_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2016_benign_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2016_malware_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2017_benign_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2017_malware_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2018_benign_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2018_malware_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2019_benign_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2019_malware_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2020_benign_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2020_malware_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2021_benign_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2021_malware_api.csv]
PASSED tests/test_step1_data.py::test_step1_combines_every_real_file_with_expected_shapes_labels_and_no_input_changes
============================= 27 passed in 30.23s ==============================
```

### Run 4: FAILED

- Time: 2026-11-12T15:51:29+00:00
- Commit: 3ba5868
- Result: test session starts
- Files: test_step1_data.py

```
============================= test session starts ==============================
platform linux -- Python 3.14.2, pytest-9.2.0, pluggy-1.7.0 -- /home/codespace/.python/current/bin/python
cachedir: .pytest_cache
rootdir: /workspaces/Project2v2/project2-harness2
configfile: pytest.ini
plugins: platformdirs-4.14.0, anyio-4.15.1
collecting ... collected 27 items

tests/test_step1_data.py::test_step1_loads_synthetic_files_drops_ids_encodes_labels_and_combines_years PASSED [  3%]
tests/test_step1_data.py::test_step1_extracts_year_and_label_from_filename[sampled_2014_benign_api.csv-expected0] PASSED [  7%]
tests/test_step1_data.py::test_step1_extracts_year_and_label_from_filename[sampled_2021_malware_api.csv-expected1] PASSED [ 11%]
tests/test_step1_data.py::test_step1_rejects_unrecognized_dataset_filename PASSED [ 14%]
tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[None-missing feature values] PASSED [ 18%]
tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[not-a-count-non-numeric feature values] PASSED [ 22%]
tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[-1-negative API-call counts] PASSED [ 25%]
tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[1.5-non-integer API-call counts] PASSED [ 29%]
tests/test_step1_data.py::test_step1_rejects_missing_expected_file PASSED [ 33%]
tests/test_step1_data.py::test_step1_rejects_unexpected_csv PASSED       [ 37%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2014_benign_api.csv] PASSED [ 40%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2014_malware_api.csv] PASSED [ 44%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2015_benign_api.csv] PASSED [ 48%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2015_malware_api.csv] PASSED [ 51%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2016_benign_api.csv] PASSED [ 55%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2016_malware_api.csv] PASSED [ 59%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2017_benign_api.csv] PASSED [ 62%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2017_malware_api.csv] PASSED [ 66%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2018_benign_api.csv] PASSED [ 70%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2018_malware_api.csv] PASSED [ 74%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2019_benign_api.csv] PASSED [ 77%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2019_malware_api.csv] PASSED [ 81%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2020_benign_api.csv] PASSED [ 85%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2020_malware_api.csv] PASSED [ 88%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2021_benign_api.csv] PASSED [ 92%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2021_malware_api.csv] PASSED [ 96%]
tests/test_step1_data.py::test_step1_combines_every_real_file_with_expected_shapes_labels_and_no_input_changes
```

### Run 5: PASSED

- Time: 2026-11-12T15:53:10+00:00
- Commit: 3ba5868
- Result: 27 passed in 20.16s
- Files: test_step1_data.py

```
============================= test session starts ==============================
platform linux -- Python 3.14.2, pytest-9.2.0, pluggy-1.7.0 -- /home/codespace/.python/current/bin/python
cachedir: .pytest_cache
rootdir: /workspaces/Project2v2/project2-harness2
configfile: pytest.ini
plugins: platformdirs-4.14.0, anyio-4.15.1
collecting ... collected 27 items

tests/test_step1_data.py::test_step1_loads_synthetic_files_drops_ids_encodes_labels_and_combines_years PASSED [  3%]
tests/test_step1_data.py::test_step1_extracts_year_and_label_from_filename[sampled_2014_benign_api.csv-expected0] PASSED [  7%]
tests/test_step1_data.py::test_step1_extracts_year_and_label_from_filename[sampled_2021_malware_api.csv-expected1] PASSED [ 11%]
tests/test_step1_data.py::test_step1_rejects_unrecognized_dataset_filename PASSED [ 14%]
tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[None-missing feature values] PASSED [ 18%]
tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[not-a-count-non-numeric feature values] PASSED [ 22%]
tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[-1-negative API-call counts] PASSED [ 25%]
tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[1.5-non-integer API-call counts] PASSED [ 29%]
tests/test_step1_data.py::test_step1_rejects_missing_expected_file PASSED [ 33%]
tests/test_step1_data.py::test_step1_rejects_unexpected_csv PASSED       [ 37%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2014_benign_api.csv] PASSED [ 40%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2014_malware_api.csv] PASSED [ 44%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2015_benign_api.csv] PASSED [ 48%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2015_malware_api.csv] PASSED [ 51%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2016_benign_api.csv] PASSED [ 55%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2016_malware_api.csv] PASSED [ 59%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2017_benign_api.csv] PASSED [ 62%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2017_malware_api.csv] PASSED [ 66%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2018_benign_api.csv] PASSED [ 70%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2018_malware_api.csv] PASSED [ 74%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2019_benign_api.csv] PASSED [ 77%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2019_malware_api.csv] PASSED [ 81%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2020_benign_api.csv] PASSED [ 85%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2020_malware_api.csv] PASSED [ 88%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2021_benign_api.csv] PASSED [ 92%]
tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2021_malware_api.csv] PASSED [ 96%]
tests/test_step1_data.py::test_step1_combines_every_real_file_with_expected_shapes_labels_and_no_input_changes PASSED [100%]

==================================== PASSES ====================================
=========================== short test summary info ============================
PASSED tests/test_step1_data.py::test_step1_loads_synthetic_files_drops_ids_encodes_labels_and_combines_years
PASSED tests/test_step1_data.py::test_step1_extracts_year_and_label_from_filename[sampled_2014_benign_api.csv-expected0]
PASSED tests/test_step1_data.py::test_step1_extracts_year_and_label_from_filename[sampled_2021_malware_api.csv-expected1]
PASSED tests/test_step1_data.py::test_step1_rejects_unrecognized_dataset_filename
PASSED tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[None-missing feature values]
PASSED tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[not-a-count-non-numeric feature values]
PASSED tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[-1-negative API-call counts]
PASSED tests/test_step1_data.py::test_step1_surfaces_missing_or_unexpected_feature_values[1.5-non-integer API-call counts]
PASSED tests/test_step1_data.py::test_step1_rejects_missing_expected_file
PASSED tests/test_step1_data.py::test_step1_rejects_unexpected_csv
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2014_benign_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2014_malware_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2015_benign_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2015_malware_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2016_benign_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2016_malware_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2017_benign_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2017_malware_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2018_benign_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2018_malware_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2019_benign_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2019_malware_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2020_benign_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2020_malware_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2021_benign_api.csv]
PASSED tests/test_step1_data.py::test_step1_each_original_file_has_expected_rows_and_columns[sampled_2021_malware_api.csv]
PASSED tests/test_step1_data.py::test_step1_combines_every_real_file_with_expected_shapes_labels_and_no_input_changes
============================= 27 passed in 20.16s ==============================
```
