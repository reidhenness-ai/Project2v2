# Step 5 Report: Evaluation

## Metrics

[`src/evaluation.py`](../src/evaluation.py) evaluates both Step 4 classifiers
on the held-out Step 3 test set, pooling the available years 2019-2021. The
test set contains 9,000 rows (4,500 goodware and 4,500 malware). Models were
refitted on 2014-2018 (90,000 rows) after the classifier choices were fixed.
The final scaler was also fitted on 2014-2018 only. Test rows were used only
for prediction and metric calculation.

Malware (`target = 1`) is the positive class for precision, recall, and
F1-score. Accuracy is the primary metric. Values are rounded to four decimal
places.

| Classifier | Test data | Rows | Accuracy | Precision (positive=malware) | Recall (positive=malware) | F1-score (positive=malware) |
|---|---|---:|---:|---:|---:|---:|
| Logistic Regression | 2019 | 3,000 | 0.5637 | 0.5342 | 0.9953 | 0.6952 |
| Logistic Regression | 2020 | 3,000 | 0.5503 | 0.5268 | 0.9887 | 0.6874 |
| Logistic Regression | 2021 | 3,000 | 0.5780 | 0.5437 | 0.9700 | 0.6968 |
| Logistic Regression | Pooled 2019-2021 | 9,000 | 0.5640 | 0.5348 | 0.9847 | 0.6931 |
| Random Forest | 2019 | 3,000 | 0.5703 | 0.5381 | 0.9927 | 0.6979 |
| Random Forest | 2020 | 3,000 | 0.5370 | 0.5193 | 0.9973 | 0.6829 |
| Random Forest | 2021 | 3,000 | 0.5177 | 0.5092 | 0.9827 | 0.6708 |
| Random Forest | Pooled 2019-2021 | 9,000 | 0.5417 | 0.5219 | 0.9909 | 0.6837 |

Reproduce the training and evaluation run from the project directory with:

```bash
python -m src.evaluation
```

## Observations

Both classifiers have high malware recall in every test year. On the pooled
set, Logistic Regression has higher accuracy, precision, and F1-score, while
Random Forest has higher recall. The per-year rows are provided alongside the
pooled results so changes in one year are not hidden by the aggregate. No
further drift analysis is performed in this step.
