#!/usr/bin/env python3
"""Preview and apply batch file renames."""

from __future__ import annotations

import argparse
from pathlib import Path


def unique_destination(destination: Path) -> Path:
    if not destination.exists():
        return destination
    stem, suffix = destination.stem, destination.suffix
    counter = 1
    while True:
        candidate = destination.with_name(f"{stem}_{counter}{suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def rename_files(folder: Path, prefix: str, start: int, dry_run: bool) -> None:
    files = sorted(path for path in folder.iterdir() if path.is_file())
    width = max(3, len(str(start + len(files))))
    planned: list[tuple[Path, Path]] = []

    for index, path in enumerate(files, start=start):
        destination = unique_destination(folder / f"{prefix}_{index:0{width}d}{path.suffix.lower()}")
        planned.append((path, destination))
        print(f"{path.name} -> {destination.name}")

    if dry_run:
        print("Preview only. Re-run without --dry-run to apply changes.")
        return

    for source, destination in planned:
        source.rename(destination)


def main() -> None:
    parser = argparse.ArgumentParser(description="Batch rename files in a folder.")
    parser.add_argument("folder", type=Path, help="Folder containing files to rename")
    parser.add_argument("--prefix", default="file", help="New filename prefix")
    parser.add_argument("--start", type=int, default=1, help="Starting number")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without renaming")
    args = parser.parse_args()

    if not args.folder.is_dir():
        raise SystemExit(f"Not a folder: {args.folder}")
    rename_files(args.folder, args.prefix, args.start, args.dry_run)


if __name__ == "__main__":
    main()
