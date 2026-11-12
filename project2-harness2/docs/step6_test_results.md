# Step 6 Report: Test Data Prediction

## Prediction setup

The final Logistic Regression and Random Forest models were fit on 2014-2018
(90,000 rows), using a `StandardScaler` fit on those same years. Both models
then predicted the untouched 2019, 2020, and 2021 test rows. Each test year
contains 3,000 apps: 1,500 goodware and 1,500 malware. Malware (`1`) is the
positive class for precision, recall, and F1-score.

The per-year prediction and evaluation code is in
[`src/evaluation.py`](../src/evaluation.py). Reproduce the final fit and
predictions from the project directory with:

```bash
python -m src.evaluation
```

## Per-year results

| Classifier | Year | Actual goodware | Actual malware | Predicted goodware | Predicted malware | Accuracy | Precision | Recall | F1-score |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 2019 | 1,500 | 1,500 | 205 | 2,795 | 0.5637 | 0.5342 | 0.9953 | 0.6952 |
| Logistic Regression | 2020 | 1,500 | 1,500 | 185 | 2,815 | 0.5503 | 0.5268 | 0.9887 | 0.6874 |
| Logistic Regression | 2021 | 1,500 | 1,500 | 324 | 2,676 | 0.5780 | 0.5437 | 0.9700 | 0.6968 |
| Random Forest | 2019 | 1,500 | 1,500 | 233 | 2,767 | 0.5703 | 0.5381 | 0.9927 | 0.6979 |
| Random Forest | 2020 | 1,500 | 1,500 | 119 | 2,881 | 0.5370 | 0.5193 | 0.9973 | 0.6829 |
| Random Forest | 2021 | 1,500 | 1,500 | 105 | 2,895 | 0.5177 | 0.5092 | 0.9827 | 0.6708 |

## Performance over time

Random Forest accuracy declines across the test years, from 0.5703 in 2019 to
0.5177 in 2021; its F1-score also decreases from 0.6979 to 0.6708. Logistic
Regression dips in 2020 (accuracy 0.5503, F1 0.6874) and rebounds in 2021
(accuracy 0.5780, F1 0.6968). Malware recall remains high for both classifiers
in every year, while precision is lower. The prediction counts show that both
models classify most apps as malware, despite the balanced actual test classes.

## Relationship to measured data drift

Step 2 compared each year with 2014. The overall mean feature-wise KS statistic
increased from 0.0313 in 2019 to 0.0373 in 2020 and 0.0523 in 2021; the number
of FDR-significant overall features rose from 393 to 433 to 459 out of 1,848.
Within malware, mean KS also increased over these years (0.0550, 0.0572,
0.0615). Goodware drift was highest in 2020 (0.0632) and remained similar in
2021 (0.0626).

The increasing overall and malware drift coincides with declining Random
Forest performance. Logistic Regression does not follow the same monotonic
pattern, and both models retain high malware recall. These results are
consistent with drift being a possible contributor to changing model behavior,
but do not establish that drift caused the observed performance changes.
Feature-distribution drift is not itself proof of concept drift; differences
in the sampled data or model limitations may also contribute.
