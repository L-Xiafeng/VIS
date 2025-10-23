#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按列/键统计缺失值数量（支持 CSV/TSV/JSON）。把常见的空表示当作缺失：空字符串, NA, N/A, null, None。
用法:
  python count_missing.py data.csv
  python count_missing.py data.json --format json
  python count_missing.py data.tsv --sep '\t'
"""
import argparse
import csv
import json
import sys
from collections import defaultdict

DEFAULT_MISSING = {"", "na", "n/a", "null", "none"}

def use_pandas():
    try:
        import pandas as pd  # type: ignore
        return pd
    except Exception:
        return None

def report_counts(counts, total_rows):
    print(f"总行数: {total_rows}")
    print("列/键, 缺失数, 缺失率")
    for k, v in counts.items():
        rate = (v / total_rows * 100) if total_rows > 0 else 0.0
        print(f"{k}, {v}, {rate:.2f}%")

def csv_with_stdlib(path, sep, missing_set):
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=sep)
        try:
            header = next(reader)
        except StopIteration:
            return {}, 0
        counts = defaultdict(int)
        ncols = len(header)
        total = 0
        for row in reader:
            total += 1
            # pad shorter rows with empty strings
            for i in range(ncols):
                val = row[i].strip() if i < len(row) else ""
                if val.lower() in missing_set:
                    counts[header[i]] += 1
        return counts, total

def json_with_stdlib(path, missing_set):
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data, dict):
        # assume dict of arrays -> convert to list of records if possible
        # fallback: not supported
        raise SystemExit("JSON root is object; expected list of records (array of objects).")
    if not isinstance(data, list):
        raise SystemExit("Unsupported JSON structure; expected array of objects.")
    total = len(data)
    keys = set()
    for item in data:
        if isinstance(item, dict):
            keys.update(item.keys())
    counts = defaultdict(int)
    for item in data:
        for k in keys:
            v = item.get(k, None)
            if v is None or (isinstance(v, str) and v.strip().lower() in missing_set):
                counts[k] += 1
    return counts, total

def pandas_handler(path, fmt, sep, missing_set):
    pd = use_pandas()
    if pd is None:
        return None
    na_vals = list(missing_set)
    if fmt == "json":
        df = pd.read_json(path)
    else:
        df = pd.read_csv(path, sep=sep, dtype=str, na_values=na_vals, keep_default_na=True)
    total = len(df)
    counts = df.isna().sum().to_dict()
    # ensure ints
    counts = {str(k): int(v) for k, v in counts.items()}
    return counts, total

def main():
    p = argparse.ArgumentParser(description="统计每列/每键的缺失值数量")
    p.add_argument("path", help="输入文件路径 (csv/json/tsv 等)")
    p.add_argument("--format", choices=["csv", "json"], help="强制文件格式")
    p.add_argument("--sep", default=",", help="CSV 分隔符（默认 ,；TSV 用 '\\t'）")
    args = p.parse_args()

    path = args.path
    fmt = args.format
    sep = args.sep

    if fmt is None:
        if path.lower().endswith(".json"):
            fmt = "json"
        else:
            fmt = "csv"

    missing_set = DEFAULT_MISSING

    # try pandas first
    if fmt in ("csv",) and use_pandas() is not None or fmt == "json" and use_pandas() is not None:
        out = pandas_handler(path, fmt, sep, missing_set)
        if out:
            counts, total = out
            report_counts(counts, total)
            return

    # fallback implementations
    if fmt == "csv":
        counts, total = csv_with_stdlib(path, sep, missing_set)
        report_counts(counts, total)
        return
    if fmt == "json":
        counts, total = json_with_stdlib(path, missing_set)
        report_counts(counts, total)
        return

if __name__ == "__main__":
    main()
