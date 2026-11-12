"""Load and validate the yearly malware/goodware API-call datasets."""

from collections.abc import Iterable
from pathlib import Path
import re

import numpy as np
import pandas as pd


_FILENAME_PATTERN = re.compile(
    r"^sampled_(?P<year>\d{4})_(?P<class>benign|malware)_api\.csv$"
)
_LABELS = {"benign": 0, "malware": 1}
_EXPECTED_YEARS = range(2014, 2022)
_EXPECTED_CLASSES = ("benign", "malware")


def _expected_filenames() -> set[str]:
    return {
        f"sampled_{year}_{class_name}_api.csv"
        for year in _EXPECTED_YEARS
        for class_name in _EXPECTED_CLASSES
    }


def parse_filename(filename: str | Path) -> tuple[int, int]:
    """Return the year and binary target encoded in a dataset filename."""
    name = Path(filename).name
    match = _FILENAME_PATTERN.fullmatch(name)
    if match is None:
        raise ValueError(
            f"Unexpected dataset filename {name!r}; expected "
            "'sampled_<year>_<benign|malware>_api.csv'."
        )

    return int(match.group("year")), _LABELS[match.group("class")]


def load_yearly_data(
    data_dir: str | Path, years: Iterable[int] | None = None
) -> dict[int, pd.DataFrame]:
    """Load CSVs, drop their first column, append encoded targets, and group by year.

    The returned DataFrames contain the shared API feature columns followed by
    a ``target`` column (malware=1, benign/goodware=0). If ``years`` is given,
    only those years' rows are loaded, but the complete inventory and all file
    schemas are still validated.
    """
    directory = Path(data_dir)
    files = sorted(directory.glob("*.csv"))
    expected_files = _expected_filenames()
    actual_files = {path.name for path in files}
    missing_files = sorted(expected_files - actual_files)
    unexpected_files = sorted(actual_files - expected_files)
    if missing_files or unexpected_files:
        details = []
        if missing_files:
            details.append(f"missing files: {missing_files}")
        if unexpected_files:
            details.append(f"unexpected files: {unexpected_files}")
        raise ValueError(
            f"Dataset inventory in {directory} is invalid; " + "; ".join(details)
        )

    selected_years = set(_EXPECTED_YEARS) if years is None else set(years)
    if not selected_years:
        raise ValueError("At least one year must be selected.")
    invalid_years = sorted(selected_years - set(_EXPECTED_YEARS))
    if invalid_years:
        raise ValueError(f"Unsupported dataset years requested: {invalid_years}.")

    feature_columns: list[str] | None = None
    file_metadata = []
    for path in files:
        year, target = parse_filename(path)
        header = pd.read_csv(path, nrows=0)
        feature_index = header.columns[1:]
        columns = feature_index.tolist()
        if not columns:
            raise ValueError(f"{path.name} must contain at least one feature column.")
        if feature_index.has_duplicates:
            duplicates = feature_index[feature_index.duplicated()].tolist()
            raise ValueError(f"{path.name} has duplicate feature columns: {duplicates}.")
        if feature_columns is None:
            feature_columns = columns
        elif columns != feature_columns:
            raise ValueError(
                f"Feature schema mismatch in {path.name}; feature names and order "
                "must match the first loaded file."
            )
        file_metadata.append((path, year, target))

    yearly_frames: dict[int, list[pd.DataFrame]] = {}
    for path, year, target in file_metadata:
        if year not in selected_years:
            continue
        frame = pd.read_csv(path)
        if frame.shape[1] < 2:
            raise ValueError(f"{path.name} must contain an ID column and features.")

        features = frame.iloc[:, 1:].copy()
        missing_count = int(features.isna().sum().sum())
        if missing_count:
            raise ValueError(
                f"{path.name} contains {missing_count} missing feature values."
            )

        try:
            features = features.apply(pd.to_numeric, errors="raise")
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"{path.name} contains non-numeric feature values."
            ) from exc

        values = features.to_numpy(dtype=np.float64)
        if not np.isfinite(values).all():
            raise ValueError(f"{path.name} contains non-finite feature values.")
        if (values < 0).any():
            raise ValueError(f"{path.name} contains negative API-call counts.")
        if not np.equal(values, np.floor(values)).all():
            raise ValueError(f"{path.name} contains non-integer API-call counts.")

        features["target"] = target
        yearly_frames.setdefault(year, []).append(features)

    return {
        year: pd.concat(frames, ignore_index=True)
        for year, frames in sorted(yearly_frames.items())
    }
