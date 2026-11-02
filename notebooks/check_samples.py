"""Load every sample in the notebook through the notebook's own code, to catch broken links or formats.

Run: python notebooks/check_samples.py (needs pandas and nbformat, and an internet connection).
"""
import os
from pathlib import Path

import nbformat

NOTEBOOK = Path(__file__).resolve().parent / "unmapped_starter.ipynb"


def cell_with(notebook, text):
    return next(cell.source for cell in notebook.cells if cell.cell_type == "code" and text in cell.source)


def main():
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    settings = cell_with(notebook, "SAMPLES = ")
    reader = cell_with(notebook, "def read_table")
    loader = cell_with(notebook, "df = read_table(dataset_source")
    os.environ.pop("UNMAPPED_TEST_DATASET", None)
    failures = 0
    namespace = {"display": lambda *args, **kwargs: None, "os": os}
    exec(settings, namespace)
    for area in namespace["SAMPLES"]:
        scope = {"display": lambda *args, **kwargs: None, "os": os}
        try:
            exec(settings.replace('DATA_SOURCE = "upload"', 'DATA_SOURCE = "sample"')
                         .replace('SAMPLE_AREA = "health"', f'SAMPLE_AREA = "{area}"'), scope)
            exec(reader, scope)
            exec(loader, scope)
            df = scope["df"]
            print(f"PASS {area:9} {len(df):>7,} rows {len(df.columns):>3} columns  {list(df.columns)[:5]}")
        except Exception as error:
            failures += 1
            print(f"FAIL {area:9} {type(error).__name__}: {error}")
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()

