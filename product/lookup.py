"""Shared helpers for the Unmapped product starter.

The web app (app.py) and the Telegram bot (bot.py) both use these functions,
so a fix here fixes both. Each one takes a pandas table and returns a new one.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

LAT_NAMES = ("lat", "latitude")
LON_NAMES = ("lon", "lng", "long", "longitude")
# Map exports such as healthsites.io name the coordinates Y (latitude) and X (longitude).
FALLBACK_NAMES = (("y",), ("x",))


def load_table(path: str | Path) -> pd.DataFrame:
    """Read a CSV, Excel or JSON file into a table."""
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix in (".xlsx", ".xls"):
        return pd.read_excel(path)
    if suffix == ".json":
        return pd.read_json(path)
    return pd.read_csv(path)


def location_columns(df: pd.DataFrame) -> tuple[str, str] | None:
    """Find the latitude and longitude columns, if the table has usable ones."""
    by_name = {str(column).lower().strip(): column for column in df.columns}
    for lat_names, lon_names in ((LAT_NAMES, LON_NAMES), FALLBACK_NAMES):
        lat = next((by_name[name] for name in lat_names if name in by_name), None)
        lon = next((by_name[name] for name in lon_names if name in by_name), None)
        if lat is not None and lon is not None and len(points_table(df, (lat, lon))):
            return lat, lon
    return None


def points_table(df: pd.DataFrame, where: tuple[str, str]) -> pd.DataFrame:
    """Rows with a valid latitude and longitude, as the lat and lon columns a map needs."""
    lat, lon = where
    points = pd.DataFrame({
        "lat": pd.to_numeric(df[lat], errors="coerce"),
        "lon": pd.to_numeric(df[lon], errors="coerce"),
    }).dropna()
    return points[points["lat"].between(-90, 90) & points["lon"].between(-180, 180)]


def text_columns(df: pd.DataFrame) -> list[str]:
    """Columns that hold words, which are the ones worth searching."""
    return [column for column in df.columns if not pd.api.types.is_numeric_dtype(df[column])]


def search(df: pd.DataFrame, query: str) -> pd.DataFrame:
    """Rows where every word of the query appears somewhere in the row's text (any case)."""
    words = [word for word in str(query).lower().split() if word]
    if not words:
        return df
    columns = text_columns(df)
    if not columns:
        return df.iloc[0:0]
    rows = df[columns].fillna("").astype(str).agg(" ".join, axis=1).str.lower()
    keep = pd.Series(True, index=df.index)
    for word in words:
        keep &= rows.str.contains(word, regex=False)
    return df[keep]


def filter_choices(df: pd.DataFrame, max_choices: int = 50) -> dict[str, list[str]]:
    """Text columns with a few repeated values (like town or type), which make good dropdown filters.

    Columns where every value is different, like names or dates, are left out.
    """
    choices = {}
    for column in text_columns(df):
        values = df[column].dropna().astype(str).str.strip()
        values = values[values != ""]
        distinct = sorted(values.unique())
        if 1 < len(distinct) <= max_choices and len(distinct) < len(values):
            choices[column] = distinct
    return choices


def apply_filters(df: pd.DataFrame, selected: dict[str, list[str]]) -> pd.DataFrame:
    """Keep the rows that match every filter the person picked. An empty filter keeps everything."""
    for column, values in selected.items():
        if values:
            df = df[df[column].astype(str).str.strip().isin(values)]
    return df


def number_columns(df: pd.DataFrame, skip: tuple[str, ...] = ()) -> list[str]:
    """Columns that hold numbers, apart from any listed in skip (such as map coordinates)."""
    return [column for column in df.columns if pd.api.types.is_numeric_dtype(df[column]) and column not in skip]


def summarise(df: pd.DataFrame, value_column: str, group_column: str, how: str = "mean") -> pd.Series:
    """The average (or total) of a number column for each group, largest first."""
    values = pd.to_numeric(df[value_column], errors="coerce")
    groups = values.groupby(df[group_column].astype(str).str.strip())
    result = groups.sum() if how == "sum" else groups.mean()
    return result.dropna().sort_values(ascending=False)


def describe_row(row: pd.Series, limit: int = 6) -> str:
    """One row as short "column: value" lines, for chat replies."""
    lines = []
    for column, value in row.items():
        if pd.isna(value) or str(value).strip() == "":
            continue
        lines.append(f"{column}: {value}")
        if len(lines) == limit:
            break
    return "\n".join(lines)
