"""Unmapped product starter: a web app that puts your adapted data in someone's hands.

Try it:   pip install -r requirements.txt
          streamlit run app.py
Make it yours: change the four settings below and replace data.csv with your adapted dataset.
"""
from pathlib import Path

import streamlit as st

from lookup import (apply_filters, filter_choices, load_table, location_columns, number_columns,
                    points_table, search, summarise)

# 1. Change these four settings.
APP_TITLE = "Clinic Finder"
APP_INTRO = "Find a health facility near you and how long people wait there. These are example rows: replace data.csv with your own data."
DATA_FILE = "data.csv"  # your adapted dataset (CSV, Excel or JSON), in this folder
DATA_NOTE = "Data: example rows made up for the Unmapped starter. Replace this line with your source and a link to your data card."

st.set_page_config(page_title=APP_TITLE, layout="wide")


@st.cache_data
def load(path: str):
    return load_table(path)


path = Path(__file__).parent / DATA_FILE
if not path.exists():
    st.error(f"Put your dataset in the same folder as app.py and call it {DATA_FILE}.")
    st.stop()
table = load(str(path))

st.title(APP_TITLE)
st.write(APP_INTRO)

# 2. Search and filter. Every word typed must appear somewhere in a row.
query = st.text_input("Search", placeholder="Type a town, a name or a service")
with st.sidebar:
    st.header("Filter")
    picked = {column: st.multiselect(column, values) for column, values in filter_choices(table).items()}
rows = apply_filters(search(table, query), picked)

st.subheader(f"{len(rows):,} of {len(table):,} rows")

# 3. A map, when the data has latitude and longitude columns.
where = location_columns(table)
if where and len(rows):
    st.map(points_table(rows, where), width="stretch")

st.dataframe(rows, width="stretch", hide_index=True)

# 4. Compare a number across groups, for example average waiting time by town.
numbers = number_columns(table, skip=where or ())
groups = list(filter_choices(table))
if numbers and groups and len(rows):
    st.subheader("Compare")
    left, right = st.columns(2)
    value_column = left.selectbox("Number", numbers)
    group_column = right.selectbox("Grouped by", groups)
    st.bar_chart(summarise(rows, value_column, group_column).head(20), width="stretch")

st.download_button("Download these rows", rows.to_csv(index=False), file_name="results.csv", mime="text/csv")
st.caption(DATA_NOTE)
