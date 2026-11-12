"""Chronological data splitting and leakage-safe API-feature scaling."""

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

from src.data import load_yearly_data


TRAIN_YEARS = (2014, 2015, 2016, 2017)
VALIDATION_YEARS = (2018,)
TEST_YEARS = (2019, 2020, 2021)
FINAL_TRAIN_YEARS = TRAIN_YEARS + VALIDATION_YEARS


@dataclass
class TemporalDataSplit:
    """Scaled feature matrices, labels, and year metadata for each time split."""

    X_train: pd.DataFrame
    y_train: pd.Series
    year_train: pd.Series
    X_validation: pd.DataFrame
    y_validation: pd.Series
    year_validation: pd.Series
    X_test: pd.DataFrame
    y_test: pd.Series
    year_test: pd.Series
    scaler: StandardScaler
    feature_columns: tuple[str, ...]
    train_years: tuple[int, ...]
    validation_years: tuple[int, ...]
    test_years: tuple[int, ...]


@dataclass
class FinalEvaluationSplit:
    """Final-fit training data through 2018 and untouched test data from 2019+."""

    X_train: pd.DataFrame
    y_train: pd.Series
    year_train: pd.Series
    X_test: pd.DataFrame
    y_test: pd.Series
    year_test: pd.Series
    scaler: StandardScaler
    feature_columns: tuple[str, ...]
    train_years: tuple[int, ...]
    test_years: tuple[int, ...]


def _validate_split_years(
    train_years: tuple[int, ...],
    validation_years: tuple[int, ...],
    test_years: tuple[int, ...],
) -> None:
    groups = {
        "training": train_years,
        "validation": validation_years,
        "test": test_years,
    }
    for name, years in groups.items():
        if not years:
            raise ValueError(f"The {name} year group cannot be empty.")
        if len(set(years)) != len(years):
            raise ValueError(f"The {name} years contain duplicates.")
        if tuple(sorted(years)) != years:
            raise ValueError(f"The {name} years must be in ascending order.")

    if set(train_years) & set(validation_years):
        raise ValueError("Training and validation years must not overlap.")
    if set(train_years) & set(test_years):
        raise ValueError("Training and test years must not overlap.")
    if set(validation_years) & set(test_years):
        raise ValueError("Validation and test years must not overlap.")
    if max(train_years) >= min(validation_years):
        raise ValueError("Training years must precede validation years.")
    if max(validation_years) >= min(test_years):
        raise ValueError("Validation years must precede test years.")


def _validate_yearly_data(
    data_by_year: dict[int, pd.DataFrame], required_years: set[int]
) -> tuple[str, ...]:
    missing_years = sorted(required_years - set(data_by_year))
    extra_years = sorted(set(data_by_year) - required_years)
    if missing_years or extra_years:
        details = []
        if missing_years:
            details.append(f"missing years: {missing_years}")
        if extra_years:
            details.append(f"unassigned years: {extra_years}")
        raise ValueError("Year split does not match the data; " + "; ".join(details))

    first_year = min(required_years)
    first_frame = data_by_year[first_year]
    if "target" not in first_frame.columns:
        raise ValueError(f"Year {first_year} data must contain a 'target' column.")
    feature_columns = tuple(column for column in first_frame if column != "target")
    if not feature_columns:
        raise ValueError("At least one API feature is required.")

    for year in sorted(required_years):
        frame = data_by_year[year]
        if "target" not in frame.columns:
            raise ValueError(f"Year {year} data must contain a 'target' column.")
        if tuple(column for column in frame if column != "target") != feature_columns:
            raise ValueError(f"Feature schema mismatch in year {year}.")
        if frame.empty:
            raise ValueError(f"Year {year} contains no rows.")
        if frame["target"].isna().any() or not frame["target"].isin([0, 1]).all():
            raise ValueError(f"Year {year} target values must be 0 or 1.")

        features = frame.loc[:, feature_columns]
        if features.isna().any().any():
            raise ValueError(f"Year {year} contains missing feature values.")
        try:
            values = features.to_numpy(dtype=np.float64)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Year {year} contains non-numeric features.") from exc
        if not np.isfinite(values).all():
            raise ValueError(f"Year {year} contains non-finite features.")

    return feature_columns


def _scale_year_group(
    data_by_year: dict[int, pd.DataFrame],
    years: tuple[int, ...],
    feature_columns: tuple[str, ...],
    scaler: StandardScaler,
) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    row_count = sum(len(data_by_year[year]) for year in years)
    scaled_values = np.empty(
        (row_count, len(feature_columns)), dtype=np.float64
    )
    labels = np.empty(row_count, dtype=np.int8)
    row_years = np.empty(row_count, dtype=np.int16)

    start = 0
    for year in years:
        frame = data_by_year[year]
        end = start + len(frame)
        scaled_values[start:end] = scaler.transform(frame.loc[:, feature_columns])
        labels[start:end] = frame["target"].to_numpy(dtype=np.int8)
        row_years[start:end] = year
        start = end

    return (
        pd.DataFrame(scaled_values, columns=feature_columns, copy=False),
        pd.Series(labels, name="target"),
        pd.Series(row_years, name="year"),
    )


def _fit_scaler(
    data_by_year: dict[int, pd.DataFrame],
    years: tuple[int, ...],
    feature_columns: tuple[str, ...],
) -> StandardScaler:
    scaler = StandardScaler()
    for year in years:
        scaler.partial_fit(data_by_year[year].loc[:, feature_columns])
    return scaler


def create_temporal_split(
    data_by_year: dict[int, pd.DataFrame],
    train_years: tuple[int, ...] = TRAIN_YEARS,
    validation_years: tuple[int, ...] = VALIDATION_YEARS,
    test_years: tuple[int, ...] = TEST_YEARS,
) -> TemporalDataSplit:
    """Create chronological splits and fit StandardScaler on training rows only.

    The scaler's learned mean and scale are applied unchanged to validation and
    test features. Year columns are retained separately as metadata, never as
    model features.
    """
    _validate_split_years(train_years, validation_years, test_years)
    required_years = set(train_years) | set(validation_years) | set(test_years)
    feature_columns = _validate_yearly_data(data_by_year, required_years)

    scaler = _fit_scaler(data_by_year, train_years, feature_columns)
    scaled_train, y_train, year_train = _scale_year_group(
        data_by_year, train_years, feature_columns, scaler
    )
    scaled_validation, y_validation, year_validation = _scale_year_group(
        data_by_year, validation_years, feature_columns, scaler
    )
    scaled_test, y_test, year_test = _scale_year_group(
        data_by_year, test_years, feature_columns, scaler
    )

    return TemporalDataSplit(
        X_train=scaled_train,
        y_train=y_train,
        year_train=year_train,
        X_validation=scaled_validation,
        y_validation=y_validation,
        year_validation=year_validation,
        X_test=scaled_test,
        y_test=y_test,
        year_test=year_test,
        scaler=scaler,
        feature_columns=feature_columns,
        train_years=train_years,
        validation_years=validation_years,
        test_years=test_years,
    )


def load_temporal_split(data_dir: str | Path) -> TemporalDataSplit:
    """Load, scale, and split years sequentially to bound peak memory usage."""
    training_data = load_yearly_data(data_dir, years=TRAIN_YEARS)
    feature_columns = _validate_yearly_data(training_data, set(TRAIN_YEARS))
    scaler = _fit_scaler(training_data, TRAIN_YEARS, feature_columns)
    X_train, y_train, year_train = _scale_year_group(
        training_data, TRAIN_YEARS, feature_columns, scaler
    )
    del training_data

    validation_data = load_yearly_data(data_dir, years=VALIDATION_YEARS)
    _validate_yearly_data(validation_data, set(VALIDATION_YEARS))
    X_validation, y_validation, year_validation = _scale_year_group(
        validation_data, VALIDATION_YEARS, feature_columns, scaler
    )
    del validation_data

    test_data = load_yearly_data(data_dir, years=TEST_YEARS)
    _validate_yearly_data(test_data, set(TEST_YEARS))
    X_test, y_test, year_test = _scale_year_group(
        test_data, TEST_YEARS, feature_columns, scaler
    )

    return TemporalDataSplit(
        X_train=X_train,
        y_train=y_train,
        year_train=year_train,
        X_validation=X_validation,
        y_validation=y_validation,
        year_validation=year_validation,
        X_test=X_test,
        y_test=y_test,
        year_test=year_test,
        scaler=scaler,
        feature_columns=feature_columns,
        train_years=TRAIN_YEARS,
        validation_years=VALIDATION_YEARS,
        test_years=TEST_YEARS,
    )


def load_final_evaluation_split(data_dir: str | Path) -> FinalEvaluationSplit:
    """Refit preprocessing on 2014-2018, then transform untouched 2019-2021."""
    training_data = load_yearly_data(data_dir, years=FINAL_TRAIN_YEARS)
    feature_columns = _validate_yearly_data(
        training_data, set(FINAL_TRAIN_YEARS)
    )
    scaler = _fit_scaler(training_data, FINAL_TRAIN_YEARS, feature_columns)
    X_train, y_train, year_train = _scale_year_group(
        training_data, FINAL_TRAIN_YEARS, feature_columns, scaler
    )
    del training_data

    test_data = load_yearly_data(data_dir, years=TEST_YEARS)
    _validate_yearly_data(test_data, set(TEST_YEARS))
    X_test, y_test, year_test = _scale_year_group(
        test_data, TEST_YEARS, feature_columns, scaler
    )

    return FinalEvaluationSplit(
        X_train=X_train,
        y_train=y_train,
        year_train=year_train,
        X_test=X_test,
        y_test=y_test,
        year_test=year_test,
        scaler=scaler,
        feature_columns=feature_columns,
        train_years=FINAL_TRAIN_YEARS,
        test_years=TEST_YEARS,
    )


def main() -> None:
    """Load the project data, create the initial split, and print its shapes."""
    project_root = Path(__file__).resolve().parents[1]
    split = load_temporal_split(project_root / "input_data")
    for name, features, labels, years in (
        ("train", split.X_train, split.y_train, split.year_train),
        (
            "validation",
            split.X_validation,
            split.y_validation,
            split.year_validation,
        ),
        ("test", split.X_test, split.y_test, split.year_test),
    ):
        print(
            f"{name}: years={sorted(years.unique().tolist())}, "
            f"rows={len(features):,}, features={features.shape[1]:,}, "
            f"labels={len(labels):,}"
        )
    print(
        f"Scaler fit rows: {split.scaler.n_samples_seen_:,}; "
        f"scaler fit years: {list(split.train_years)}"
    )


if __name__ == "__main__":
    main()
