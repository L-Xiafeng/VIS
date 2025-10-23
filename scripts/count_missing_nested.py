#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
递归统计 JSON 数据中所有字段（包括嵌套字段）的缺失值数量。
用法:
  python count_missing_nested.py data.json
"""
import argparse
import json
from collections import defaultdict

DEFAULT_MISSING = {"", "na", "n/a", "null", "none"}

def is_missing(value):
    """判断值是否为缺失值"""
    if value is None:
        return True
    if isinstance(value, str) and value.strip().lower() in DEFAULT_MISSING:
        return True
    return False

def flatten_dict(d, parent_key='', sep='.'):
    """递归展平嵌套字典"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def analyze_json_structure(data):
    """分析 JSON 数据结构并统计缺失值"""
    if not isinstance(data, list):
        raise SystemExit("JSON root must be an array of objects.")
    
    total_records = len(data)
    all_keys = set()
    
    # 收集所有可能的键（包括嵌套键）
    for item in data:
        if isinstance(item, dict):
            flat_item = flatten_dict(item)
            all_keys.update(flat_item.keys())
    
    # 统计每个键的缺失情况
    missing_counts = defaultdict(int)
    
    for item in data:
        if isinstance(item, dict):
            flat_item = flatten_dict(item)
            for key in all_keys:
                value = flat_item.get(key, None)
                if is_missing(value):
                    missing_counts[key] += 1
    
    return missing_counts, total_records, all_keys

def report_counts(missing_counts, total_records, all_keys):
    """输出统计报告"""
    print(f"总记录数: {total_records}")
    print(f"总字段数: {len(all_keys)}")
    print("\n" + "="*80)
    print(f"{'字段名':<50} {'缺失数':>10} {'缺失率':>10}")
    print("="*80)
    
    # 按字段名排序输出
    for key in sorted(all_keys):
        count = missing_counts[key]
        rate = (count / total_records * 100) if total_records > 0 else 0.0
        print(f"{key:<50} {count:>10} {rate:>9.2f}%")
    
    # 汇总统计
    print("\n" + "="*80)
    print("汇总统计:")
    total_missing = sum(missing_counts.values())
    total_cells = len(all_keys) * total_records
    overall_rate = (total_missing / total_cells * 100) if total_cells > 0 else 0.0
    print(f"  总单元格数: {total_cells}")
    print(f"  总缺失数: {total_missing}")
    print(f"  总体缺失率: {overall_rate:.2f}%")
    
    # 完全缺失的字段
    completely_missing = [k for k in all_keys if missing_counts[k] == total_records]
    if completely_missing:
        print(f"\n完全缺失的字段 ({len(completely_missing)} 个):")
        for key in sorted(completely_missing):
            print(f"  - {key}")
    
    # 部分缺失的字段
    partially_missing = [k for k in all_keys if 0 < missing_counts[k] < total_records]
    if partially_missing:
        print(f"\n部分缺失的字段 ({len(partially_missing)} 个):")
        for key in sorted(partially_missing):
            count = missing_counts[key]
            rate = (count / total_records * 100)
            print(f"  - {key}: {count}/{total_records} ({rate:.2f}%)")
    
    # 无缺失的字段
    no_missing = [k for k in all_keys if missing_counts[k] == 0]
    if no_missing:
        print(f"\n无缺失的字段 ({len(no_missing)} 个):")
        for key in sorted(no_missing):
            print(f"  - {key}")

def main():
    parser = argparse.ArgumentParser(description="递归统计JSON数据中所有字段的缺失值")
    parser.add_argument("path", help="输入JSON文件路径")
    args = parser.parse_args()
    
    with open(args.path, encoding='utf-8') as f:
        data = json.load(f)
    
    missing_counts, total_records, all_keys = analyze_json_structure(data)
    report_counts(missing_counts, total_records, all_keys)

if __name__ == "__main__":
    main()
