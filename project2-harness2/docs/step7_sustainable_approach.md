# Step 7 Report: Sustainable Approach

## Approach

[`src/sustainable.py`](../src/sustainable.py) compares two strategies using
the same classifiers, feature set, scaling method, and held-out test rows:

- **Static baseline:** fit the scaler and both models on 2014-2018, then keep
  them fixed while predicting 2019, 2020, and 2021.
- **Periodic retraining:** use the 2014-2018 fit for 2019, add the now-labeled
  2019 data and refit the scaler and models before predicting 2020, then add
  2020 data and refit before predicting 2021.

Each prediction year is excluded from that prediction's training and scaler
fit. The strategies use identical test rows in each year: 3,000 apps (1,500
goodware and 1,500 malware). Malware (`1`) is the positive class.

Reproduce the comparison from the project directory with:

```bash
python -m src.sustainable
```

## Comparison by test year

Each metric row uses a model trained on the years shown. Precision, recall,
and F1-score treat malware as positive.

| Approach | Classifier | Test year | Training years | Accuracy | Precision | Recall | F1-score |
|---|---|---:|---|---:|---:|---:|---:|
| Static baseline | Logistic Regression | 2019 | 2014-2018 | 0.5637 | 0.5342 | 0.9953 | 0.6952 |
| Periodic retraining | Logistic Regression | 2019 | 2014-2018 | 0.5637 | 0.5342 | 0.9953 | 0.6952 |
| Static baseline | Logistic Regression | 2020 | 2014-2018 | 0.5503 | 0.5268 | 0.9887 | 0.6874 |
| Periodic retraining | Logistic Regression | 2020 | 2014-2019 | 0.8830 | 0.8611 | 0.9133 | 0.8864 |
| Static baseline | Logistic Regression | 2021 | 2014-2018 | 0.5780 | 0.5437 | 0.9700 | 0.6968 |
| Periodic retraining | Logistic Regression | 2021 | 2014-2020 | 0.9003 | 0.8995 | 0.9013 | 0.9004 |
| Static baseline | Random Forest | 2019 | 2014-2018 | 0.5703 | 0.5381 | 0.9927 | 0.6979 |
| Periodic retraining | Random Forest | 2019 | 2014-2018 | 0.5703 | 0.5381 | 0.9927 | 0.6979 |
| Static baseline | Random Forest | 2020 | 2014-2018 | 0.5370 | 0.5193 | 0.9973 | 0.6829 |
| Periodic retraining | Random Forest | 2020 | 2014-2019 | 0.9267 | 0.9307 | 0.9220 | 0.9263 |
| Static baseline | Random Forest | 2021 | 2014-2018 | 0.5177 | 0.5092 | 0.9827 | 0.6708 |
| Periodic retraining | Random Forest | 2021 | 2014-2020 | 0.9417 | 0.9811 | 0.9007 | 0.9392 |

## Conclusions

Both approaches are identical on 2019 because neither can use labels from
2019 before predicting that year. Once newer labels are available, periodic
retraining performs substantially better on the next test year. Compared with
the static baseline, accuracy rises by 0.3327-0.3897 in 2020 and 0.3223-0.4240
in 2021 across the two classifiers. F1-score also improves for both models in
both years.

This is consistent with the Step 2 finding that feature distributions change
over time: overall mean KS distance from 2014 rises from 0.0313 in 2019 to
0.0523 in 2021, with the number of FDR-significant features increasing from
393 to 459. Retraining can incorporate more recent labeled patterns and
re-estimate feature scaling, which may help when the old training distribution
no longer represents current apps.

The comparison supports periodic retraining for this dataset and protocol, but
does not prove that measured feature drift alone caused the performance gap.
Other temporal differences or properties of the sampled data may contribute.
Retraining also requires access to reliable recent labels and should continue
to preserve a future-year holdout for evaluation.
