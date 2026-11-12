# Step 4 Report: Models

## Classifiers

[`src/models.py`](../src/models.py) defines and fits two scikit-learn
classifiers:

- **Logistic Regression** is a regularized linear baseline. It is relatively
  efficient for the 1,848-feature dataset and provides a useful comparison to a
  nonlinear model.
- **Random Forest** can model nonlinear relationships and feature
  interactions. Random feature subsets and limits on tree depth and leaf size
  constrain tree complexity.

The supplied training split is balanced: 36,000 goodware rows (label `0`) and
36,000 malware rows (label `1`). Therefore, neither estimator uses class
weighting.

## Hyperparameters

| Classifier | Parameters | Rationale |
|---|---|---|
| Logistic Regression | `C=1.0`, L2 penalty (scikit-learn default), `solver="lbfgs"`, `max_iter=500`, `tol=0.001`, `random_state=42` | L2 regularization is a general-purpose baseline; the iteration limit allows convergence on the large feature set. |
| Random Forest | `n_estimators=100`, `criterion="gini"`, `max_depth=20`, `min_samples_leaf=2`, `max_features="sqrt"`, `class_weight=None`, `n_jobs=-1`, `random_state=42` | 100 trees provide an ensemble baseline; random feature subsets and bounded depth/leaf size manage complexity and training cost. |

These are fixed baseline settings, not the result of a hyperparameter search.
No validation or test rows were used for fitting or parameter selection in this
step.

## Training run

Run from the project directory:

```bash
python -m src.models
```

The command obtains Step 3's training partition and fits both models using
**2014-2017 only**. The completed run used 72,000 rows, 1,848 scaled features,
and both encoded classes `[0, 1]`.

| Classifier | Fit result | Elapsed time |
|---|---|---:|
| Logistic Regression | Fitted | 5.46 seconds |
| Random Forest | Fitted | 19.81 seconds |

Elapsed times are specific to this environment. This step does not calculate
predictive performance metrics or access validation/test labels; evaluation is
left for the later evaluation step. The models are trained in memory and are
not serialized to disk.
