"""Headless test for unmapped_starter.ipynb with a fake Adaption SDK that mirrors adaption 0.17.1; it makes no API call.

Run: python notebooks/test_notebook.py (needs pandas, nbformat, nbclient and ipykernel)."""

from __future__ import annotations

import inspect
import json
import os
import sys
import tempfile
import textwrap
from pathlib import Path

import nbformat
import pandas as pd
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parent
NOTEBOOK = ROOT / "unmapped_starter.ipynb"

FAKE_MODULE = r'''
from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from types import SimpleNamespace

import pandas as pd

not_given = object()
omit = object()


def _log(method, **details):
    path = Path(os.environ["UNMAPPED_FAKE_CALL_LOG"])
    calls = json.loads(path.read_text()) if path.exists() else []
    calls.append({"method": method, **details})
    path.write_text(json.dumps(calls, indent=2))


class BinaryAPIResponse:
    def __init__(self, source):
        self.source = Path(source)

    def read(self):
        return self.source.read_bytes()

    def text(self):
        return self.source.read_text(encoding="utf-8")

    def write_to_file(self, path):
        shutil.copyfile(self.source, path)


class DatasetsResource:
    def __init__(self):
        self.input_path = None
        self.output_path = None
        self.dataset_id = "dataset_test_001"

    def upload_file(
        self,
        path,
        *,
        name=None,
        processing_mode=None,
        column_mapping=None,
    ):
        self.input_path = Path(path).resolve()
        _log(
            "upload_file",
            path=str(path),
            name=name,
            processing_mode=processing_mode,
            column_mapping=column_mapping,
        )
        return SimpleNamespace(dataset_id=self.dataset_id, status="awaiting_input")

    def get_status(
        self,
        dataset_id,
        *,
        extra_headers=None,
        extra_query=None,
        extra_body=None,
        timeout=not_given,
    ):
        rows = len(pd.read_csv(self.input_path))
        _log("get_status", dataset_id=dataset_id)
        return SimpleNamespace(
            dataset_id=dataset_id,
            status="awaiting_input",
            row_count=rows,
            progress=None,
            error_data=None,
        )

    def adapt(
        self,
        dataset_id,
        *,
        column_mapping=omit,
        recipe_specification=omit,
        job_specification=omit,
        brand_controls=omit,
        training_type=omit,
        estimate=omit,
        language_expansion=omit,
        extra_headers=None,
        extra_query=None,
        extra_body=None,
        timeout=not_given,
    ):
        is_estimate = estimate is True
        _log(
            "adapt",
            dataset_id=dataset_id,
            estimate=is_estimate,
            column_mapping=column_mapping,
            job_specification=job_specification,
        )
        if not is_estimate:
            adapted = pd.read_csv(self.input_path).drop_duplicates().copy()
            adapted = adapted.fillna("filled_by_fake_adaption")
            adapted["adaption_status"] = "adapted"
            self.output_path = Path.cwd() / "fake_adapted_source.csv"
            adapted.to_csv(self.output_path, index=False)
        return SimpleNamespace(
            run_id=None if is_estimate else "run_test_001",
            estimated_minutes=1.5,
            estimated_credits_consumed=2.0,
            estimate=is_estimate,
            multimodal_pricing_applied=False,
            credit_multiplier=None,
        )

    def wait_for_completion(
        self,
        dataset_id,
        *,
        initial_interval=2.0,
        max_interval=30.0,
        backoff_factor=2.0,
        timeout=3600.0,
    ):
        _log("wait_for_completion", dataset_id=dataset_id, timeout=timeout)
        rows = len(pd.read_csv(self.output_path))
        return SimpleNamespace(
            dataset_id=dataset_id,
            status="succeeded",
            row_count=rows,
            progress=SimpleNamespace(percent=100, processed_rows=rows, total_rows=rows),
            error_data=None,
        )

    def download(
        self,
        dataset_id,
        *,
        file_format=omit,
        extra_headers=None,
        extra_query=None,
        extra_body=None,
        timeout=not_given,
    ):
        _log("download", dataset_id=dataset_id, file_format=file_format)
        if file_format != "csv":
            raise AssertionError("The starter notebook must request CSV in this test.")
        return BinaryAPIResponse(self.output_path)


class Adaption:
    def __init__(
        self,
        *,
        api_key=None,
        base_url=None,
        timeout=not_given,
        max_retries=2,
        default_headers=None,
        default_query=None,
        http_client=None,
        _strict_response_validation=False,
    ):
        if not api_key:
            api_key = os.environ.get("ADAPTION_API_KEY")
        if not api_key:
            raise ValueError("api_key is required")
        self.api_key = api_key
        self.datasets = DatasetsResource()
'''


def output_text(notebook):
    pieces = []
    for cell in notebook.cells:
        for output in cell.get("outputs", []):
            if output.output_type == "stream":
                pieces.append(output.get("text", ""))
            elif output.output_type in {"execute_result", "display_data"}:
                pieces.append(output.get("data", {}).get("text/plain", ""))
            elif output.output_type == "error":
                pieces.extend(output.get("traceback", []))
    return "\n".join(pieces)


def source_for_tag(notebook, tag):
    for cell in notebook.cells:
        if tag in cell.get("metadata", {}).get("tags", []):
            return cell.source
    raise AssertionError(f"Missing notebook cell tagged {tag!r}")


def assert_fake_signatures(fake_dir):
    sys.path.insert(0, str(fake_dir))
    try:
        import adaption

        assert list(inspect.signature(adaption.Adaption).parameters) == [
            "api_key", "base_url", "timeout", "max_retries", "default_headers",
            "default_query", "http_client", "_strict_response_validation",
        ]
        resource = adaption.DatasetsResource
        assert list(inspect.signature(resource.upload_file).parameters) == [
            "self", "path", "name", "processing_mode", "column_mapping",
        ]
        assert list(inspect.signature(resource.adapt).parameters) == [
            "self", "dataset_id", "column_mapping", "recipe_specification",
            "job_specification", "brand_controls", "training_type", "estimate",
            "language_expansion", "extra_headers", "extra_query", "extra_body", "timeout",
        ]
        assert list(inspect.signature(resource.wait_for_completion).parameters) == [
            "self", "dataset_id", "initial_interval", "max_interval",
            "backoff_factor", "timeout",
        ]
        assert list(inspect.signature(resource.download).parameters) == [
            "self", "dataset_id", "file_format", "extra_headers", "extra_query",
            "extra_body", "timeout",
        ]
    finally:
        sys.path.pop(0)
        sys.modules.pop("adaption", None)


def flip(notebook, tag, old, new):
    cell = next(cell for cell in notebook.cells if tag in cell.get("metadata", {}).get("tags", []))
    assert old in cell.source, f"{tag} cell should start with {old!r}"
    cell.source = cell.source.replace(old, new)


def execute(notebook, work, dataset, fake_dir, allow_errors=False):
    call_log = work / "fake_calls.json"
    call_log.unlink(missing_ok=True)
    old_env = os.environ.copy()
    os.environ.update({
        "UNMAPPED_NOTEBOOK_TEST": "1",
        "UNMAPPED_TEST_DATASET": str(dataset),
        "UNMAPPED_FAKE_CALL_LOG": str(call_log),
        "ADAPTION_API_KEY": "fake-secret-key-never-print",
        "PYTHONPATH": str(fake_dir) + os.pathsep + old_env.get("PYTHONPATH", ""),
    })
    try:
        client = NotebookClient(notebook, timeout=120, kernel_name="python3", allow_errors=allow_errors,
                                resources={"metadata": {"path": str(work)}})
        executed = client.execute()
    finally:
        os.environ.clear()
        os.environ.update(old_env)
    calls = json.loads(call_log.read_text()) if call_log.exists() else []
    return executed, calls


def main():
    original = nbformat.read(NOTEBOOK, as_version=4)
    code_cells = [cell for cell in original.cells if cell.cell_type == "code"]
    for index, cell in enumerate(original.cells):
        if cell.cell_type == "code":
            assert index > 0 and original.cells[index - 1].cell_type == "markdown"
            assert original.cells[index - 1].source.strip()
    assert all(not cell.get("outputs") for cell in code_cells), "Ship the notebook without outputs."

    with tempfile.TemporaryDirectory(prefix="unmapped-notebook-test-") as temporary:
        work = Path(temporary)
        fake_dir = work / "fake_sdk"
        package = fake_dir / "adaption"
        package.mkdir(parents=True)
        (package / "__init__.py").write_text(textwrap.dedent(FAKE_MODULE), encoding="utf-8")
        assert_fake_signatures(fake_dir)

        sample = work / "sample.csv"
        pd.DataFrame({
            "place": ["Kigali", "Nairobi", "Nairobi", "Lagos"],
            "indicator": ["clinic access", "rainfall", "rainfall", "school attendance"],
            "value": [72.0, None, None, 81.0],
        }).to_csv(sample, index=False)

        # 1. As shipped, the personal-data switch is off, so nothing is uploaded.
        guarded, calls = execute(nbformat.read(NOTEBOOK, as_version=4), work, sample, fake_dir, allow_errors=True)
        assert "Check your data for personal details first" in output_text(guarded)
        assert not any(call["method"] == "upload_file" for call in calls)

        # 2. The scan flags columns that hold contact details.
        personal = work / "personal.csv"
        pd.DataFrame({"town": ["Ikeja", "Huye"], "contact": ["ada@example.com", "+234 803 555 0199"]}).to_csv(personal, index=False)
        scanned, _ = execute(nbformat.read(NOTEBOOK, as_version=4), work, personal, fake_dir, allow_errors=True)
        scan = output_text(scanned)
        assert "email addresses" in scan and "possible phone numbers" in scan

        # 3. With both switches on, the whole notebook runs and spends only after the estimate.
        notebook = nbformat.read(NOTEBOOK, as_version=4)
        flip(notebook, "privacy-flag", "I_CHECKED_FOR_PERSONAL_DATA = False", "I_CHECKED_FOR_PERSONAL_DATA = True")
        flip(notebook, "run-flag", "RUN_FOR_REAL = False", "RUN_FOR_REAL = True")
        executed, calls = execute(notebook, work, sample, fake_dir)

        text = output_text(executed)
        assert all(cell.get("execution_count") is not None for cell in executed.cells if cell.cell_type == "code")
        assert "duplicate rows" in text and "blank values" in text
        assert "Estimated credits: 2.0" in text and "Nothing has been spent yet." in text
        assert "Saved adapted.csv" in text
        assert "fake-secret-key-never-print" not in text

        adapt_calls = [call for call in calls if call["method"] == "adapt"]
        assert [call["estimate"] for call in adapt_calls] == [True, False]
        assert all(call["job_specification"] == {"max_rows": 4} for call in adapt_calls)
        mapping = adapt_calls[0]["column_mapping"]
        assert mapping["universal_prompt"].startswith("Using only the details in this row")
        assert mapping["context"] == ["place", "indicator", "value"]
        assert [call["method"] for call in calls][:1] == ["upload_file"]
        assert any(call["method"] == "wait_for_completion" for call in calls)
        assert any(call["method"] == "download" for call in calls)

        adapted = pd.read_csv(work / "adapted.csv")
        assert len(adapted) == 3 and "adaption_status" in adapted.columns

        card = (work / "DATA_CARD.md").read_text(encoding="utf-8")
        for heading in ("## In one line", "## Sources and permissions", "## What I changed", "## What it covers",
                        "## What is still missing or biased", "## Personal data check", "## How to cite"):
            assert heading in card, heading
        assert "Result: succeeded" in card and "Rows after Adaptive Data: 3" in card
        assert "value (50.0% blank)" in card

    print(f"PASS: executed {len(code_cells)} code cells with the fake adaption SDK.")
    print("PASS: the upload waits for the personal-data check, and the scan flags emails and phone numbers.")
    print("PASS: estimate before spending, guarded run, adapted CSV, comparison and DATA_CARD.md verified.")


if __name__ == "__main__":
    main()

