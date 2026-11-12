"""Compare fixed and periodically retrained models on future test years."""

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

from src.data import load_yearly_data
from src.evaluation import binary_metrics
from src.models import TrainedClassifiers, train_classifiers
from src.preprocessing import FINAL_TRAIN_YEARS, TEST_YEARS


@dataclass
class FittedWindow:
    """A model pair and scaler fitted on one chronological training window."""

    models: TrainedClassifiers
    scaler: StandardScaler
    feature_columns: tuple[str, ...]


def _fit_window(data_dir: str | Path, training_years: tuple[int, ...]) -> FittedWindow:
    """Fit the scaler and both models using only the requested years."""
    data_by_year = load_yearly_data(data_dir, years=training_years)
    first_frame = data_by_year[training_years[0]]
    feature_columns = tuple(column for column in first_frame if column != "target")
    if not feature_columns:
        raise ValueError("At least one API feature is required.")

    scaler = StandardScaler()
    for year in training_years:
        frame = data_by_year[year]
        if tuple(column for column in frame if column != "target") != feature_columns:
            raise ValueError(f"Feature schema mismatch in year {year}.")
        scaler.partial_fit(frame.loc[:, feature_columns])

    row_count = sum(len(data_by_year[year]) for year in training_years)
    X_values = np.empty((row_count, len(feature_columns)), dtype=np.float64)
    y_values = np.empty(row_count, dtype=np.int8)
    start = 0
    for year in training_years:
        frame = data_by_year[year]
        end = start + len(frame)
        X_values[start:end] = scaler.transform(frame.loc[:, feature_columns])
        y_values[start:end] = frame["target"].to_numpy(dtype=np.int8)
        start = end

    del data_by_year
    models = train_classifiers(
        pd.DataFrame(X_values, columns=feature_columns, copy=False),
        pd.Series(y_values, name="target"),
        training_years=training_years,
    )
    return FittedWindow(models, scaler, feature_columns)


def _predict_year(
    fitted: FittedWindow, data_dir: str | Path, test_year: int, approach: str
) -> list[dict[str, object]]:
    """Predict and score one later year without fitting on its rows."""
    test_data = load_yearly_data(data_dir, years=(test_year,))
    frame = test_data[test_year]
    feature_columns = tuple(column for column in frame if column != "target")
    if feature_columns != fitted.feature_columns:
        raise ValueError(f"Feature schema mismatch in test year {test_year}.")

    X_test = pd.DataFrame(
        fitted.scaler.transform(frame.loc[:, feature_columns]),
        columns=feature_columns,
    )
    y_test = frame["target"].reset_index(drop=True)
    rows = []
    for model_name, model in (
        ("Logistic Regression", fitted.models.logistic_regression),
        ("Random Forest", fitted.models.random_forest),
    ):
        predictions = model.predict(X_test)
        rows.append(
            {
                "approach": approach,
                "classifier": model_name,
                "test_year": test_year,
                "training_years": fitted.models.training_years,
                "training_rows": fitted.models.training_rows,
                "test_rows": len(y_test),
                "predicted_goodware": int((predictions == 0).sum()),
                "predicted_malware": int((predictions == 1).sum()),
                "positive_class": 1,
                **binary_metrics(y_test, predictions),
            }
        )
    return rows


def compare_retraining_strategies(data_dir: str | Path) -> pd.DataFrame:
    """Evaluate fixed and expanding-window strategies on identical test years.

    The fixed baseline is trained once through 2018. The periodically retrained
    strategy uses that same fit for 2019, then adds 2019 labels before the 2020
    prediction and 2019-2020 labels before the 2021 prediction.
    """
    fixed_fit = _fit_window(data_dir, FINAL_TRAIN_YEARS)
    fixed_rows = [
        row
        for year in TEST_YEARS
        for row in _predict_year(fixed_fit, data_dir, year, "Static baseline")
    ]

    periodic_rows = [
        {**row, "approach": "Periodic retraining"}
        for row in fixed_rows
        if row["test_year"] == TEST_YEARS[0]
    ]
    del fixed_fit

    for year in TEST_YEARS[1:]:
        training_years = FINAL_TRAIN_YEARS + tuple(
            prior_year for prior_year in TEST_YEARS if prior_year < year
        )
        updated_fit = _fit_window(data_dir, training_years)
        periodic_rows.extend(
            _predict_year(updated_fit, data_dir, year, "Periodic retraining")
        )
        del updated_fit

    return pd.DataFrame(fixed_rows + periodic_rows)


def main() -> None:
    """Run and print the sustainable static-versus-retraining comparison."""
    project_root = Path(__file__).resolve().parents[1]
    results = compare_retraining_strategies(project_root / "input_data")
    print("Positive class: malware (1)")
    print(
        results[
            [
                "approach",
                "classifier",
                "test_year",
                "training_years",
                "accuracy",
                "precision",
                "recall",
                "f1_score",
            ]
        ].to_string(index=False, float_format=lambda value: f"{value:.4f}")
    )


if __name__ == "__main__":
    main()
