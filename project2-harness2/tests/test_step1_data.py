import csv
import hashlib
from pathlib import Path

import pandas as pd
import pytest

from data import load_yearly_data, parse_filename


def _write_dataset(path: Path, rows: list[tuple[str, int, int]]) -> None:
    pd.DataFrame(rows, columns=["apkname", "api_a", "api_b"]).to_csv(
        path, index=False
    )


def _write_complete_dataset(directory: Path) -> None:
    for year in range(2014, 2022):
        for kind in ("benign", "malware"):
            _write_dataset(
                directory / f"sampled_{year}_{kind}_api.csv",
                [],
            )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def test_step1_loads_synthetic_files_drops_ids_encodes_labels_and_combines_years(
    tmp_path,
):
    _write_complete_dataset(tmp_path)
    _write_dataset(
        tmp_path / "sampled_2014_benign_api.csv",
        [("benign-1", 1, 0), ("benign-2", 2, 1)],
    )
    _write_dataset(
        tmp_path / "sampled_2014_malware_api.csv", [("malware-1", 9, 8)]
    )
    _write_dataset(
        tmp_path / "sampled_2015_benign_api.csv", [("benign-3", 3, 2)]
    )
    _write_dataset(
        tmp_path / "sampled_2015_malware_api.csv",
        [("malware-2", 4, 3), ("malware-3", 5, 4)],
    )

    yearly = load_yearly_data(tmp_path)

    assert set(yearly) == set(range(2014, 2022))
    pd.testing.assert_frame_equal(
        yearly[2014],
        pd.DataFrame(
            {
                "api_a": [1, 2, 9],
                "api_b": [0, 1, 8],
                "target": [0, 0, 1],
            }
        ),
    )
    pd.testing.assert_frame_equal(
        yearly[2015],
        pd.DataFrame(
            {
                "api_a": [3, 4, 5],
                "api_b": [2, 3, 4],
                "target": [0, 1, 1],
            }
        ),
    )
    for year in range(2016, 2022):
        assert yearly[year].empty


@pytest.mark.parametrize(
    ("filename", "expected"),
    [
        ("sampled_2014_benign_api.csv", (2014, 0)),
        ("sampled_2021_malware_api.csv", (2021, 1)),
    ],
)
def test_step1_extracts_year_and_label_from_filename(filename, expected):
    assert parse_filename(filename) == expected


def test_step1_rejects_unrecognized_dataset_filename():
    with pytest.raises(ValueError, match="Unexpected dataset filename"):
        parse_filename("sampled_2014_goodware_api.csv")


@pytest.mark.parametrize(
    ("bad_feature", "error"),
    [
        (None, "missing feature values"),
        ("not-a-count", "non-numeric feature values"),
        (-1, "negative API-call counts"),
        (1.5, "non-integer API-call counts"),
    ],
)
def test_step1_surfaces_missing_or_unexpected_feature_values(
    tmp_path, bad_feature, error
):
    _write_complete_dataset(tmp_path)
    _write_dataset(
        tmp_path / "sampled_2014_benign_api.csv",
        [("app-1", 1, bad_feature)],
    )

    with pytest.raises(ValueError, match=error):
        load_yearly_data(tmp_path)


def test_step1_rejects_missing_expected_file(tmp_path):
    _write_complete_dataset(tmp_path)
    missing = tmp_path / "sampled_2017_malware_api.csv"
    missing.unlink()

    with pytest.raises(ValueError, match=missing.name):
        load_yearly_data(tmp_path)


def test_step1_rejects_unexpected_csv(tmp_path):
    _write_complete_dataset(tmp_path)
    _write_dataset(tmp_path / "sampled_2022_malware_api.csv", [])

    with pytest.raises(ValueError, match="unexpected files"):
        load_yearly_data(tmp_path)


@pytest.mark.parametrize(
    "filename",
    [
        f"sampled_{year}_{kind}_api.csv"
        for year in range(2014, 2022)
        for kind in ("benign", "malware")
    ],
)
def test_step1_each_original_file_has_expected_rows_and_columns(
    real_data_dir, filename
):
    path = real_data_dir / filename
    assert path.is_file(), f"Expected dataset file is missing: {filename}"

    with path.open(newline="", encoding="utf-8") as source:
        header = next(csv.reader(source))
    assert len(header) == 1849

    with path.open(newline="", encoding="utf-8") as source:
        row_count = sum(1 for _ in csv.reader(source)) - 1
    year, _ = parse_filename(filename)
    assert row_count == (9000 if year <= 2018 else 1500)


def test_step1_combines_every_real_file_with_expected_shapes_labels_and_no_input_changes(
    real_data_dir,
):
    paths = sorted(real_data_dir.glob("*.csv"))
    assert len(paths) == 16
    assert {path.name for path in paths} == {
        f"sampled_{year}_{kind}_api.csv"
        for year in range(2014, 2022)
        for kind in ("benign", "malware")
    }

    hashes_before = {path.name: _sha256(path) for path in paths}
    yearly = load_yearly_data(real_data_dir)

    assert set(yearly) == set(range(2014, 2022))
    expected_rows_per_file = {
        year: 9000 if year <= 2018 else 1500 for year in range(2014, 2022)
    }

    for year, frame in yearly.items():
        expected_file_rows = expected_rows_per_file[year]
        assert frame.shape == (2 * expected_file_rows, 1849)
        assert len([column for column in frame.columns if column != "target"]) == 1848
        assert frame.columns[-1] == "target"
        assert "apkname" not in frame.columns
        assert set(frame["target"].unique()) == {0, 1}
        assert frame["target"].value_counts().to_dict() == {
            0: expected_file_rows,
            1: expected_file_rows,
        }

        row_offset = 0
        for kind, label in (("benign", 0), ("malware", 1)):
            path = real_data_dir / f"sampled_{year}_{kind}_api.csv"
            source_header = pd.read_csv(path, nrows=0).columns.tolist()
            assert source_header[0] == "apkname"
            assert frame.columns[:-1].tolist() == source_header[1:]

            samples = pd.read_csv(path, usecols=source_header[:4])
            first_feature = source_header[1]
            assert frame.iloc[row_offset]["target"] == label
            assert (
                frame.iloc[row_offset][first_feature] == samples.iloc[0][first_feature]
            )
            last_output_row = row_offset + expected_file_rows - 1
            assert frame.iloc[last_output_row]["target"] == label
            assert (
                frame.iloc[last_output_row][first_feature]
                == samples.iloc[-1][first_feature]
            )
            row_offset += expected_file_rows

    assert {path.name: _sha256(path) for path in paths} == hashes_before
