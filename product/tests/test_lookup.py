from pathlib import Path

import pandas as pd

import pytest

from lookup import (apply_filters, describe_row, filter_choices, keep_columns, load_table, location_columns,
                    number_columns, points_table, search, summarise)

DATA = Path(__file__).resolve().parents[1] / "data.csv"


def table():
    return load_table(DATA)


def test_loads_the_example_rows_and_finds_the_map_columns():
    df = table()
    assert len(df) == 12
    assert location_columns(df) == ("lat", "lon")
    assert len(points_table(df, ("lat", "lon"))) == 12


def test_every_search_word_must_match_in_any_case():
    df = table()
    assert list(search(df, "KIGALI")["name"]) == ["Example Clinic J", "Example Clinic K"]
    assert list(search(df, "malaria abeokuta")["name"]) == ["Example Clinic B"]
    assert len(search(df, "  ")) == 12
    assert search(df, "no such place").empty


def test_filters_offer_repeated_values_and_skip_unique_ones():
    choices = filter_choices(table())
    assert choices["country"] == ["Kenya", "Nigeria", "Rwanda"]
    assert "town" in choices and "type" in choices
    assert "name" not in choices and "last_checked" not in choices
    assert len(apply_filters(table(), {"country": ["Kenya"], "town": []})) == 4


def test_summarise_ranks_groups_by_their_average():
    df = table()
    waits = summarise(df, "wait_minutes", "country")
    assert list(waits.index) == ["Kenya", "Nigeria", "Rwanda"]
    assert waits["Kenya"] == 68.75
    assert summarise(df, "wait_minutes", "country", how="sum")["Rwanda"] == 150
    assert number_columns(df, skip=("lat", "lon")) == ["wait_minutes"]


def test_bad_coordinates_and_missing_values_are_skipped():
    df = pd.DataFrame({"Latitude": ["1.5", "x", "95"], "Longitude": [30, 31, 32], "note": ["a", None, ""]})
    assert location_columns(df) == ("Latitude", "Longitude")
    assert len(points_table(df, ("Latitude", "Longitude"))) == 1
    assert describe_row(df.iloc[1]) == "Latitude: x\nLongitude: 31"
    assert describe_row(df.iloc[2]) == "Latitude: 95\nLongitude: 32"
    assert location_columns(pd.DataFrame({"lat": ["?"], "lon": ["?"]})) is None


def test_map_exports_with_x_and_y_columns_still_get_a_map():
    healthsites = pd.DataFrame({"X": [30.5577], "Y": [-2.0103], "name": ["Kabarondo Health Centre"]})
    assert location_columns(healthsites) == ("Y", "X")
    assert location_columns(pd.DataFrame({"x": [500.0], "y": [900.0]})) is None


def test_only_the_chosen_columns_are_shown_and_old_excel_files_get_a_clear_message(tmp_path):
    assert list(keep_columns(table(), ["town", "name"]).columns) == ["town", "name"]
    assert len(keep_columns(table(), []).columns) == 10
    with pytest.raises(ValueError, match="not in your data: phone"):
        keep_columns(table(), ["name", "phone"])
    old = tmp_path / "old.xls"
    old.write_bytes(b"not really excel")
    with pytest.raises(ValueError, match="Save the file as .xlsx or .csv"):
        load_table(old)


def test_long_values_are_cut_short_in_chat_replies():
    line = describe_row(pd.Series({"notes": "x" * 500}))
    assert len(line) == len("notes: ") + 200 and line.endswith("…")
