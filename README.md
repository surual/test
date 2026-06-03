# Useful Tools

A small collection of practical scripts for daily file, data, and project workflows.

## Tools

- `scripts/organize_files.py`: Organize files by extension, date, or file type.
- `scripts/find_duplicates.py`: Find duplicate files by content hash.
- `scripts/merge_csv.py`: Merge many CSV files into one file.
- `scripts/clean_csv.py`: Clean CSV headers, trim spaces, and remove empty rows.
- `scripts/batch_rename.py`: Preview and apply batch file renames safely.
- `docs/quick-start.md`: Simple usage examples.

## Requirements

- Python 3.9 or newer
- No third-party packages required

## Quick Start

```bash
python scripts/organize_files.py "C:/path/to/folder" --mode type --dry-run
python scripts/find_duplicates.py "C:/path/to/folder"
python scripts/merge_csv.py "C:/path/to/csv-folder" --output merged.csv
```

Run any script with `--help` to see all options.

## Safety

Most tools support preview mode, such as `--dry-run`. Use preview first when moving, deleting, or renaming files.
