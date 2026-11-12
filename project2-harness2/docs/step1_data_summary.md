# Step 1 Report: Prepare the Data

## Files loaded and combined

The loader in [`src/data.py`](../src/data.py) found all 16 CSV files in
`input_data/`. It removes the first column from each file, derives the year and
target from the filename, then concatenates the two class files into one
DataFrame per year. The returned DataFrames contain 1,848 feature columns and
one `target` column (`malware = 1`, `benign`/goodware = 0).

| Year | Files | Benign file rows | Malware file rows | Combined rows |
|---:|---:|---:|---:|---:|
| 2014 | 2 | 9,000 | 9,000 | 18,000 |
| 2015 | 2 | 9,000 | 9,000 | 18,000 |
| 2016 | 2 | 9,000 | 9,000 | 18,000 |
| 2017 | 2 | 9,000 | 9,000 | 18,000 |
| 2018 | 2 | 9,000 | 9,000 | 18,000 |
| 2019 | 2 | 1,500 | 1,500 | 3,000 |
| 2020 | 2 | 1,500 | 1,500 | 3,000 |
| 2021 | 2 | 1,500 | 1,500 | 3,000 |
| **Total** | **16** | **51,000** | **51,000** | **102,000** |

## Combined data shape

The first (APK-name) column is excluded. Each yearly DataFrame has 1,848 API
feature columns plus the target, for **1,849 columns total**.

| Year | Rows | Feature columns | Target columns | Total columns |
|---:|---:|---:|---:|---:|
| 2014 | 18,000 | 1,848 | 1 | 1,849 |
| 2015 | 18,000 | 1,848 | 1 | 1,849 |
| 2016 | 18,000 | 1,848 | 1 | 1,849 |
| 2017 | 18,000 | 1,848 | 1 | 1,849 |
| 2018 | 18,000 | 1,848 | 1 | 1,849 |
| 2019 | 3,000 | 1,848 | 1 | 1,849 |
| 2020 | 3,000 | 1,848 | 1 | 1,849 |
| 2021 | 3,000 | 1,848 | 1 | 1,849 |

## Class counts

| Year | Malware (1) | Goodware / benign (0) |
|---:|---:|---:|
| 2014 | 9,000 | 9,000 |
| 2015 | 9,000 | 9,000 |
| 2016 | 9,000 | 9,000 |
| 2017 | 9,000 | 9,000 |
| 2018 | 9,000 | 9,000 |
| 2019 | 1,500 | 1,500 |
| 2020 | 1,500 | 1,500 |
| 2021 | 1,500 | 1,500 |

## Data checks and issues

All files have the same ordered set of 1,848 feature columns. Every feature
column was read as an integer (`int64`); the scan found no missing or nonnumeric
values, non-finite values, negative counts, or fractional counts.

The 2014-2018 files contain 9,000 rows each, not the 1,500 rows per file
described in the assignment. The 2019-2021 files contain 1,500 rows each. The
reported counts above are measured from the supplied data.
