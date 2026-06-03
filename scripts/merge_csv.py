#!/usr/bin/env python3
"""Merge CSV files from a folder into one CSV file."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def merge_csv(folder: Path, output: Path, pattern: str, add_source: bool) -> None:
    files = sorted(path for path in folder.glob(pattern) if path.is_file())
    if not files:
        raise SystemExit(f"No files matched {pattern!r} in {folder}")

    all_headers: list[str] = []
    rows: list[dict[str, str]] = []
    for path in files:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                continue
            for header in reader.fieldnames:
                if header not in all_headers:
                    all_headers.append(header)
            for row in reader:
                if add_source:
                    row["source_file"] = path.name
                rows.append(row)

    if add_source and "source_file" not in all_headers:
        all_headers.append("source_file")

    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=all_headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Merged {len(files)} files and {len(rows)} rows into {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge CSV files into one file.")
    parser.add_argument("folder", type=Path, help="Folder containing CSV files")
    parser.add_argument("--output", type=Path, default=Path("merged.csv"), help="Output CSV path")
    parser.add_argument("--pattern", default="*.csv", help="Input filename pattern")
    parser.add_argument("--source", action="store_true", help="Add source_file column")
    args = parser.parse_args()

    if not args.folder.is_dir():
        raise SystemExit(f"Not a folder: {args.folder}")
    merge_csv(args.folder, args.output, args.pattern, args.source)


if __name__ == "__main__":
    main()
