import numpy as np
import pandas as pd
import pytest

from src.data import load_yearly_data
from src.preprocessing import create_temporal_split


def _yearly_data():
    return {
        2014: pd.DataFrame(
            {"api_a": [0, 2], "api_b": [4, 8], "target": [0, 1]}
        ),
        2015: pd.DataFrame(
            {"api_a": [4, 6], "api_b": [12, 16], "target": [0, 1]}
        ),
        2016: pd.DataFrame(
            {"api_a": [100, 200], "api_b": [300, 400], "target": [0, 1]}
        ),
        2017: pd.DataFrame(
            {"api_a": [1000, 2000], "api_b": [3000, 4000], "target": [0, 1]}
        ),
        2018: pd.DataFrame(
            {"api_a": [5000, 6000], "api_b": [7000, 8000], "target": [0, 1]}
        ),
        2019: pd.DataFrame(
            {"api_a": [9000, 10000], "api_b": [11000, 12000], "target": [0, 1]}
        ),
    }


def _split(data_by_year):
    return create_temporal_split(
        data_by_year,
        train_years=(2014, 2015),
        validation_years=(2016,),
        test_years=(2017, 2018, 2019),
    )


def test_splits_are_chronological_disjoint_and_preserve_feature_order():
    split = _split(_yearly_data())

    assert split.train_years == (2014, 2015)
    assert split.validation_years == (2016,)
    assert split.test_years == (2017, 2018, 2019)
    assert set(split.year_train).isdisjoint(split.year_validation)
    assert set(split.year_train).isdisjoint(split.year_test)
    assert set(split.year_validation).isdisjoint(split.year_test)
    assert split.X_train.columns.tolist() == ["api_a", "api_b"]
    assert split.X_validation.columns.tolist() == ["api_a", "api_b"]
    assert split.X_test.columns.tolist() == ["api_a", "api_b"]
    assert split.X_train.shape == (4, 2)
    assert split.X_validation.shape == (2, 2)
    assert split.X_test.shape == (6, 2)


def test_standard_scaler_is_fitted_only_on_training_rows():
    split = _split(_yearly_data())

    np.testing.assert_allclose(split.scaler.mean_, [3.0, 10.0])
    np.testing.assert_allclose(split.scaler.var_, [5.0, 20.0])
    assert split.scaler.n_samples_seen_ == 4
    np.testing.assert_allclose(split.X_train.mean().to_numpy(), [0.0, 0.0])
    np.testing.assert_allclose(
        split.X_validation.iloc[0].to_numpy(),
        (np.array([100.0, 300.0]) - np.array([3.0, 10.0]))
        / np.sqrt([5.0, 20.0]),
    )


def test_changing_later_years_does_not_change_fitted_scaler():
    original = _yearly_data()
    changed = _yearly_data()
    changed[2019].loc[:, ["api_a", "api_b"]] = 1_000_000

    original_split = _split(original)
    changed_split = _split(changed)

    np.testing.assert_array_equal(
        original_split.scaler.mean_, changed_split.scaler.mean_
    )
    np.testing.assert_array_equal(
        original_split.scaler.scale_, changed_split.scaler.scale_
    )
    pd.testing.assert_frame_equal(
        original_split.X_train, changed_split.X_train
    )


def test_rejects_non_chronological_year_groups():
    data = _yearly_data()

    with pytest.raises(ValueError, match="must precede validation"):
        create_temporal_split(
            data,
            train_years=(2016,),
            validation_years=(2015,),
            test_years=(2017, 2018, 2019),
        )


def test_rejects_feature_schema_mismatch():
    data = _yearly_data()
    data[2016] = data[2016].rename(columns={"api_a": "other_api"})

    with pytest.raises(ValueError, match="Feature schema mismatch"):
        _split(data)


def test_loader_can_read_selected_years_while_checking_full_inventory(tmp_path):
    for year in range(2014, 2022):
        for class_name in ("benign", "malware"):
            path = tmp_path / f"sampled_{year}_{class_name}_api.csv"
            pd.DataFrame(
                {"apkname": ["app"], "api_a": [1], "api_b": [2]}
            ).to_csv(path, index=False)

    selected = load_yearly_data(tmp_path, years=(2014, 2015))

    assert list(selected) == [2014, 2015]
    assert all(frame.shape == (2, 3) for frame in selected.values())
