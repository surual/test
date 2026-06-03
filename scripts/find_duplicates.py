#!/usr/bin/env python3
"""Find duplicate files by SHA-256 hash."""

from __future__ import annotations

import argparse
import hashlib
from collections import defaultdict
from pathlib import Path


def file_hash(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def find_duplicates(folder: Path) -> dict[str, list[Path]]:
    by_size: dict[int, list[Path]] = defaultdict(list)
    for path in folder.rglob("*"):
        if path.is_file():
            by_size[path.stat().st_size].append(path)

    by_hash: dict[str, list[Path]] = defaultdict(list)
    for paths in by_size.values():
        if len(paths) < 2:
            continue
        for path in paths:
            by_hash[file_hash(path)].append(path)
    return {digest: paths for digest, paths in by_hash.items() if len(paths) > 1}


def main() -> None:
    parser = argparse.ArgumentParser(description="Find duplicate files in a folder.")
    parser.add_argument("folder", type=Path, help="Folder to scan")
    args = parser.parse_args()

    if not args.folder.is_dir():
        raise SystemExit(f"Not a folder: {args.folder}")

    duplicates = find_duplicates(args.folder)
    if not duplicates:
        print("No duplicates found.")
        return

    for index, paths in enumerate(duplicates.values(), start=1):
        print(f"\nDuplicate group {index}:")
        for path in paths:
            print(f"  {path}")


if __name__ == "__main__":
    main()
