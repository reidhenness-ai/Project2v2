# Step 3 Report: Preprocessing

## Scaling

[`src/preprocessing.py`](../src/preprocessing.py) uses scikit-learn's
`StandardScaler` to standardize each API-call feature:

```text
scaled_value = (value - training_mean) / training_standard_deviation
```

The scaler is incrementally fitted (`partial_fit`) on the training rows from
2014-2017 only. Its learned means and scales are then applied unchanged to
training, validation, and test rows. Constant features use scikit-learn's
default scale of 1. The target label and year metadata are not included among
the features. API feature names and order are retained.

## Time-based split

| Split | Years | Rows | API features |
|---|---|---:|---:|
| Training | 2014-2017 | 72,000 | 1,848 |
| Validation | 2018 | 18,000 | 1,848 |
| Test | 2019-2021 | 9,000 | 1,848 |

Each listed row count is the combined malware and goodware count. The actual
inputs contain 18,000 rows per year for 2014-2018 and 3,000 rows per year for
2019-2021.

The split is created by `create_temporal_split()` when prepared yearly
DataFrames are already available. `load_temporal_split()` provides the
memory-bounded path used for the supplied data; it loads, scales, and releases
one split at a time after validating the complete 16-file inventory and feature
schema.

Reproduce the full-data split from the project directory with:

```bash
python -m src.preprocessing
```

The command reports the rows and feature counts in each split, plus the number
of rows used to fit the scaler. For the supplied data, it reports 72,000 fit
rows, 18,000 validation rows, and 9,000 test rows.

## Leakage prevention

- Years are disjoint and strictly chronological: training precedes validation,
  which precedes testing.
- The scaler is fitted only on 2014-2017. Neither validation nor test features
  or labels contribute to its fitted parameters.
- Validation and test feature matrices are transformed using the training
  scaler; there is no call to `fit` or `partial_fit` on either set.
- The test years are kept separate from model-selection data. The plan allows
  refitting final preprocessing on 2014-2018 only after model choices are
  finalized; that later final-fit action is not performed in this step.
