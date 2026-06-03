#!/usr/bin/env python3
"""Clean CSV headers, trim cell spaces, and remove empty rows."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


def clean_header(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"\s+", "_", value)
    value = re.sub(r"[^a-z0-9_]+", "", value)
    return value or "column"


def clean_csv(input_path: Path, output_path: Path) -> None:
    with input_path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.reader(source)
        try:
            headers = next(reader)
        except StopIteration:
            raise SystemExit("Input CSV is empty")

        cleaned_headers = []
        seen: dict[str, int] = {}
        for header in headers:
            cleaned = clean_header(header)
            seen[cleaned] = seen.get(cleaned, 0) + 1
            if seen[cleaned] > 1:
                cleaned = f"{cleaned}_{seen[cleaned]}"
            cleaned_headers.append(cleaned)

        cleaned_rows = []
        for row in reader:
            cleaned_row = [cell.strip() for cell in row]
            if any(cleaned_row):
                cleaned_rows.append(cleaned_row)

    with output_path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.writer(target)
        writer.writerow(cleaned_headers)
        writer.writerows(cleaned_rows)

    print(f"Wrote {len(cleaned_rows)} rows to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean a CSV file.")
    parser.add_argument("input", type=Path, help="Input CSV file")
    parser.add_argument("--output", type=Path, help="Output CSV file")
    args = parser.parse_args()

    if not args.input.is_file():
        raise SystemExit(f"Not a file: {args.input}")
    output = args.output or args.input.with_name(f"{args.input.stem}_clean.csv")
    clean_csv(args.input, output)


if __name__ == "__main__":
    main()
