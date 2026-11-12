import numpy as np
import pandas as pd
import pytest
from sklearn.preprocessing import StandardScaler

from src.preprocessing import create_temporal_split, load_temporal_split


def _yearly_data():
    values = {
        2014: ([0, 2], [10, 14]),
        2015: ([4, 6], [18, 22]),
        2016: ([8, 10], [26, 30]),
        2017: ([12, 14], [34, 38]),
        2018: ([1000, 2000], [3000, 4000]),
        2019: ([5000, 6000], [7000, 8000]),
        2020: ([9000, 10000], [11000, 12000]),
        2021: ([13000, 14000], [15000, 16000]),
    }
    return {
        year: pd.DataFrame(
            {
                "api_a": features_a,
                "api_b": features_b,
                "target": [0, 1],
            }
        )
        for year, (features_a, features_b) in values.items()
    }


def test_default_split_uses_planned_years_and_keeps_metadata_out_of_features():
    split = create_temporal_split(_yearly_data())

    assert split.train_years == (2014, 2015, 2016, 2017)
    assert split.validation_years == (2018,)
    assert split.test_years == (2019, 2020, 2021)
    assert split.feature_columns == ("api_a", "api_b")
    assert list(split.X_train.columns) == ["api_a", "api_b"]
    assert list(split.X_validation.columns) == ["api_a", "api_b"]
    assert list(split.X_test.columns) == ["api_a", "api_b"]
    assert len(split.X_train) == len(split.y_train) == len(split.year_train) == 8
    assert len(split.X_validation) == len(split.y_validation) == len(split.year_validation) == 2
    assert len(split.X_test) == len(split.y_test) == len(split.year_test) == 6
    assert set(split.year_train) == {2014, 2015, 2016, 2017}
    assert set(split.year_validation) == {2018}
    assert set(split.year_test) == {2019, 2020, 2021}
    assert split.y_train.tolist() == [0, 1] * 4
    assert split.y_validation.tolist() == [0, 1]
    assert split.y_test.tolist() == [0, 1] * 3


def test_scaler_matches_all_training_rows_and_transforms_later_splits_unchanged():
    data = _yearly_data()
    split = create_temporal_split(data)
    training = pd.concat([data[year][["api_a", "api_b"]] for year in range(2014, 2018)])
    expected_scaler = StandardScaler().fit(training)

    np.testing.assert_allclose(split.scaler.mean_, expected_scaler.mean_)
    np.testing.assert_allclose(split.scaler.var_, expected_scaler.var_)
    assert split.scaler.n_samples_seen_ == len(training)
    np.testing.assert_allclose(
        split.X_train.to_numpy(), expected_scaler.transform(training)
    )
    validation = data[2018][["api_a", "api_b"]]
    np.testing.assert_allclose(
        split.X_validation.to_numpy(), expected_scaler.transform(validation)
    )


def test_perturbing_validation_and_test_rows_does_not_change_training_fit():
    original = _yearly_data()
    changed = _yearly_data()
    for year in (2018, 2019, 2020, 2021):
        changed[year].loc[:, ["api_a", "api_b"]] = 1_000_000 + year
        changed[year].loc[:, "target"] = [1, 0]

    baseline_split = create_temporal_split(original)
    changed_split = create_temporal_split(changed)

    np.testing.assert_array_equal(
        baseline_split.scaler.mean_, changed_split.scaler.mean_
    )
    np.testing.assert_array_equal(
        baseline_split.scaler.var_, changed_split.scaler.var_
    )
    pd.testing.assert_frame_equal(baseline_split.X_train, changed_split.X_train)
    pd.testing.assert_series_equal(baseline_split.y_train, changed_split.y_train)
    assert not np.array_equal(
        baseline_split.X_validation.to_numpy(),
        changed_split.X_validation.to_numpy(),
    )


def test_source_frames_are_not_mutated():
    data = _yearly_data()
    original = {year: frame.copy(deep=True) for year, frame in data.items()}

    create_temporal_split(data)

    for year in data:
        pd.testing.assert_frame_equal(data[year], original[year])


@pytest.mark.parametrize(
    ("train_years", "validation_years", "test_years", "error"),
    [
        ((2014, 2015), (2015,), (2016, 2017, 2018, 2019, 2020, 2021), "overlap"),
        ((2015, 2014), (2016,), (2017, 2018, 2019, 2020, 2021), "ascending order"),
        ((2014, 2015), (2016,), (2018, 2017, 2019, 2020, 2021), "ascending order"),
        ((2016, 2017), (2015,), (2018, 2019, 2020, 2021), "precede"),
        ((2014, 2015), (2016,), (), "cannot be empty"),
    ],
)
def test_rejects_invalid_year_groups(
    train_years, validation_years, test_years, error
):
    with pytest.raises(ValueError, match=error):
        create_temporal_split(
            _yearly_data(),
            train_years=train_years,
            validation_years=validation_years,
            test_years=test_years,
        )


def test_rejects_missing_or_unassigned_years():
    missing_year = _yearly_data()
    del missing_year[2017]
    with pytest.raises(ValueError, match="missing years"):
        create_temporal_split(missing_year)

    extra_year = _yearly_data()
    extra_year[2022] = extra_year[2021].copy()
    with pytest.raises(ValueError, match="unassigned years"):
        create_temporal_split(extra_year)


@pytest.mark.parametrize(
    ("year", "replacement", "error"),
    [
        (2014, pd.DataFrame({"api_a": [1], "api_b": [2]}), "target"),
        (
            2018,
            pd.DataFrame({"other": [1, 2], "api_b": [3, 4], "target": [0, 1]}),
            "Feature schema mismatch",
        ),
        (
            2019,
            pd.DataFrame(
                {"api_a": [1, np.nan], "api_b": [2, 3], "target": [0, 1]}
            ),
            "missing feature values",
        ),
        (
            2020,
            pd.DataFrame(
                {"api_a": [1, np.inf], "api_b": [2, 3], "target": [0, 1]}
            ),
            "non-finite",
        ),
        (
            2021,
            pd.DataFrame(
                {"api_a": [1, 2], "api_b": [2, 3], "target": [0, 2]}
            ),
            "target values must be 0 or 1",
        ),
        (
            2016,
            pd.DataFrame(columns=["api_a", "api_b", "target"]),
            "contains no rows",
        ),
    ],
)
def test_rejects_invalid_year_data(year, replacement, error):
    data = _yearly_data()
    data[year] = replacement

    with pytest.raises(ValueError, match=error):
        create_temporal_split(data)


def test_staged_loader_builds_default_split_and_fits_scaler_from_train_csvs(tmp_path):
    for year in range(2014, 2022):
        for class_name, label in (("benign", 0), ("malware", 1)):
            path = tmp_path / f"sampled_{year}_{class_name}_api.csv"
            pd.DataFrame(
                {
                    "apkname": [f"{year}-{class_name}-a", f"{year}-{class_name}-b"],
                    "api_a": [year, year + 1],
                    "api_b": [label * 2, label * 2 + 1],
                }
            ).to_csv(path, index=False)

    split = load_temporal_split(tmp_path)

    assert split.train_years == (2014, 2015, 2016, 2017)
    assert split.validation_years == (2018,)
    assert split.test_years == (2019, 2020, 2021)
    assert split.X_train.shape == (16, 2)
    assert split.X_validation.shape == (4, 2)
    assert split.X_test.shape == (12, 2)
    assert split.scaler.n_samples_seen_ == 16
    np.testing.assert_allclose(split.scaler.mean_, [2016.0, 1.5])
    assert set(split.year_train) == {2014, 2015, 2016, 2017}
    assert set(split.year_validation) == {2018}
    assert set(split.year_test) == {2019, 2020, 2021}
