#!/usr/bin/env python3
"""Recheck every page, licence and direct data URL in datasets.json."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
CATALOG = ROOT / "datasets.json"


def curl_status(url: str) -> int:
    result = subprocess.run(
        ["curl", "-L", "--max-time", "60", "--retry", "2", "-sS", "-o", "/dev/null", "-w", "%{http_code}", url],
        text=True,
        capture_output=True,
        check=False,
    )
    try:
        return int(result.stdout[-3:])
    except ValueError:
        return 0


def curl_download(url: str, destination: str) -> tuple[int, str, int]:
    result = subprocess.run(
        [
            "curl", "-L", "--max-time", "180", "--retry", "2", "-sS",
            "-o", destination, "-w", "%{http_code}\n%{content_type}\n%{size_download}", url,
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    parts = result.stdout.strip().splitlines()
    if result.returncode or len(parts) < 3:
        return 0, "", 0
    return int(parts[-3]), parts[-2], int(float(parts[-1]))


def safe_first_bytes(raw: bytes) -> str:
    return raw.decode("utf-8", errors="replace").replace("\r", "\\r").replace("\n", "\\n")


def main() -> int:
    catalog = json.loads(CATALOG.read_text())
    today = date.today().isoformat()
    results = []
    status_cache = {}

    def cached_status(url: str) -> int:
        if url not in status_cache:
            status_cache[url] = curl_status(url)
        return status_cache[url]

    for area_key, area in catalog.items():
        for dataset in area["datasets"]:
            with tempfile.NamedTemporaryFile(suffix=".csv") as temp:
                http, content_type, size = curl_download(dataset["direct_url"], temp.name)
                page_http = cached_status(dataset["page_url"])
                license_http = cached_status(dataset["license"]["url"])
                parse_ok = False
                error = ""
                rows = 0
                columns = []
                first_bytes = ""
                try:
                    with open(temp.name, "rb") as handle:
                        first_bytes = safe_first_bytes(handle.read(80))
                    frame = pd.read_csv(temp.name, **dataset.get("read_kwargs", {}))
                    rows = len(frame)
                    columns = list(frame.columns)
                    parse_ok = rows > 0 and len(columns) > 0
                except Exception as exc:  # reported in the table and JSON
                    error = f"{type(exc).__name__}: {exc}"

                passed = (
                    http == 200
                    and content_type.lower().startswith(("text/csv", "application/csv", "application/octet-stream"))
                    and parse_ok
                )
                # Some sites refuse scripted visits to their web pages; a browser still opens them, so warn only.
                warnings = [f"{label} link {code}" for label, code in (("page", page_http), ("licence", license_http))
                            if not 200 <= code < 400]
                dataset["verification"] = {
                    "date": today,
                    "result": "pass" if passed else "fail",
                    "http_status": http,
                    "page_http_status": page_http,
                    "license_http_status": license_http,
                    "content_type": content_type,
                    "first_bytes": first_bytes,
                    "downloaded_bytes": size,
                    "parse_ok": parse_ok,
                    "rows": rows,
                    "columns": columns,
                    "error": error,
                }
                results.append((area["title"], dataset["name"], http, rows, "PASS" if passed else "FAIL", ", ".join(warnings)))

        sample = area["sample"]
        try:
            reader = getattr(pd, sample["reader"])
            frame = reader(sample["url"], **sample.get("read_kwargs", {}))
            sample["rows"] = len(frame)
            sample["columns"] = list(frame.columns)
            sample["direct_load_verified"] = True
            sample["verified_date"] = today
        except Exception as exc:
            sample["direct_load_verified"] = False
            sample["verified_date"] = today
            sample["error"] = f"{type(exc).__name__}: {exc}"

    if "--update" in sys.argv:  # record today's results in datasets.json
        CATALOG.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n")

    print("Area             Dataset                                      HTTP   Rows     Result  Warnings")
    print("---------------- -------------------------------------------- ------ -------- ------  --------")
    for area, name, http, rows, result, warning in results:
        print(f"{area[:16]:16} {name[:44]:44} {http:6} {rows:8} {result:>6}  {warning}")
    passed = sum(row[4] == "PASS" for row in results)
    samples = [area["sample"] for area in catalog.values()]
    loaded = sum(bool(sample.get("direct_load_verified")) for sample in samples)
    print(f"\n{passed}/{len(results)} datasets passed; {loaded}/{len(samples)} samples loaded directly with pandas.")
    return 0 if passed == len(results) and loaded == len(samples) else 1


if __name__ == "__main__":
    raise SystemExit(main())
