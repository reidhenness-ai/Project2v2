"""Classifier definitions and training for the chronological data split."""

from dataclasses import dataclass
from pathlib import Path
from time import perf_counter

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from src.preprocessing import TemporalDataSplit, load_temporal_split


@dataclass
class TrainedClassifiers:
    """Fitted estimators and the training metadata needed by later steps."""

    logistic_regression: LogisticRegression
    random_forest: RandomForestClassifier
    training_years: tuple[int, ...]
    training_rows: int
    feature_count: int
    classes: tuple[int, ...]
    fit_seconds: dict[str, float]


def create_classifiers(random_state: int = 42) -> dict[
    str, LogisticRegression | RandomForestClassifier
]:
    """Create the project's fixed Logistic Regression and Random Forest models."""
    return {
        "logistic_regression": LogisticRegression(
            C=1.0,
            solver="lbfgs",
            max_iter=500,
            tol=1e-3,
            random_state=random_state,
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=100,
            criterion="gini",
            max_depth=20,
            min_samples_leaf=2,
            max_features="sqrt",
            class_weight=None,
            n_jobs=-1,
            random_state=random_state,
        ),
    }


def train_classifiers(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    training_years: tuple[int, ...],
    random_state: int = 42,
) -> TrainedClassifiers:
    """Fit both classifiers exclusively on the supplied training split."""
    if X_train.empty or y_train.empty:
        raise ValueError("Training features and labels must not be empty.")
    if len(X_train) != len(y_train):
        raise ValueError("Training features and labels must have equal row counts.")
    if y_train.isna().any() or not y_train.isin([0, 1]).all():
        raise ValueError("Training labels must be encoded as 0 or 1.")

    models = create_classifiers(random_state=random_state)
    fit_seconds = {}
    for name, model in models.items():
        start = perf_counter()
        model.fit(X_train, y_train)
        fit_seconds[name] = perf_counter() - start

    return TrainedClassifiers(
        logistic_regression=models["logistic_regression"],
        random_forest=models["random_forest"],
        training_years=training_years,
        training_rows=len(y_train),
        feature_count=X_train.shape[1],
        classes=tuple(int(label) for label in models["logistic_regression"].classes_),
        fit_seconds=fit_seconds,
    )


def train_from_temporal_split(split: TemporalDataSplit) -> TrainedClassifiers:
    """Train from the training partition only; validation and test stay unused."""
    return train_classifiers(
        split.X_train,
        split.y_train,
        training_years=split.train_years,
    )


def main() -> None:
    """Train both models on Step 3's training years and print fit summaries."""
    project_root = Path(__file__).resolve().parents[1]
    split = load_temporal_split(project_root / "input_data")

    X_train = split.X_train
    y_train = split.y_train
    training_years = split.train_years
    del split

    result = train_classifiers(X_train, y_train, training_years)
    print(
        f"Training data: years={list(result.training_years)}, "
        f"rows={result.training_rows:,}, features={result.feature_count:,}, "
        f"classes={list(result.classes)}"
    )
    for model_name, elapsed in result.fit_seconds.items():
        print(f"{model_name}: fitted in {elapsed:.2f} seconds")


if __name__ == "__main__":
    main()
