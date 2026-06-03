#!/usr/bin/env python3
"""Organize files in a folder by type, extension, or modified date."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from datetime import datetime

TYPE_GROUPS = {
    "images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg"},
    "documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".ppt", ".pptx"},
    "spreadsheets": {".csv", ".tsv", ".xls", ".xlsx"},
    "archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "code": {".py", ".js", ".ts", ".html", ".css", ".json", ".yaml", ".yml"},
    "media": {".mp3", ".wav", ".mp4", ".mov", ".avi", ".mkv"},
}


def target_folder(path: Path, mode: str) -> str:
    suffix = path.suffix.lower()
    if mode == "extension":
        return suffix[1:] or "no-extension"
    if mode == "date":
        return datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m")
    for group, suffixes in TYPE_GROUPS.items():
        if suffix in suffixes:
            return group
    return "other"


def unique_destination(destination: Path) -> Path:
    if not destination.exists():
        return destination
    stem, suffix = destination.stem, destination.suffix
    parent = destination.parent
    counter = 1
    while True:
        candidate = parent / f"{stem} ({counter}){suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def organize(folder: Path, mode: str, dry_run: bool) -> None:
    for item in folder.iterdir():
        if not item.is_file():
            continue
        group = target_folder(item, mode)
        destination_dir = folder / group
        destination = unique_destination(destination_dir / item.name)
        print(f"{item.name} -> {group}/{destination.name}")
        if not dry_run:
            destination_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(destination))


def main() -> None:
    parser = argparse.ArgumentParser(description="Organize files in a folder.")
    parser.add_argument("folder", type=Path, help="Folder to organize")
    parser.add_argument("--mode", choices=["type", "extension", "date"], default="type")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without moving files")
    args = parser.parse_args()

    if not args.folder.is_dir():
        raise SystemExit(f"Not a folder: {args.folder}")
    organize(args.folder, args.mode, args.dry_run)


if __name__ == "__main__":
    main()
