# Quick Start

## Organize files

Preview first:

```bash
python scripts/organize_files.py "C:/Users/you/Downloads" --mode type --dry-run
```

Apply changes:

```bash
python scripts/organize_files.py "C:/Users/you/Downloads" --mode type
```

Other modes:

```bash
python scripts/organize_files.py "C:/Users/you/Downloads" --mode extension --dry-run
python scripts/organize_files.py "C:/Users/you/Downloads" --mode date --dry-run
```

## Find duplicate files

```bash
python scripts/find_duplicates.py "C:/Users/you/Documents"
```

## Merge CSV files

```bash
python scripts/merge_csv.py "C:/Users/you/Desktop/csv" --output merged.csv --source
```

## Clean a CSV file

```bash
python scripts/clean_csv.py raw.csv --output clean.csv
```

## Batch rename files

Preview first:

```bash
python scripts/batch_rename.py "C:/Users/you/Pictures" --prefix photo --dry-run
```

Apply changes:

```bash
python scripts/batch_rename.py "C:/Users/you/Pictures" --prefix photo
```
