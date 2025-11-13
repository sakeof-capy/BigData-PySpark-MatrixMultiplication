#!/usr/bin/env python3
import sys
import csv

def load_csv(path):
    """Load CSV into a 2D list of integers"""
    with open(path, newline="") as f:
        reader = csv.reader(f)
        return [[int(x) for x in row] for row in reader]

def compare_matrices(expected_path, result_path):
    expected = load_csv(expected_path)
    result = load_csv(result_path)

    if len(expected) != len(result):
        return False, f"Number of rows differ: expected={len(expected)}, result={len(result)}"

    for i, (row_e, row_r) in enumerate(zip(expected, result)):
        if len(row_e) != len(row_r):
            return False, f"Row {i} length differs: expected={len(row_e)}, result={len(row_r)}"
        for j, (v_e, v_r) in enumerate(zip(row_e, row_r)):
            if v_e != v_r:
                return False, f"Value differs at position ({i},{j}): expected={v_e}, result={v_r}"

    return True, "All values match!"

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 check_result.py Expected.csv result.csv")
        sys.exit(1)

    expected_file = sys.argv[1]
    result_file = sys.argv[2]

    ok, msg = compare_matrices(expected_file, result_file)
    if ok:
        print("✅ Matrices are identical!")
        sys.exit(0)
    else:
        print("❌ Matrices differ!")
        print(msg)
        sys.exit(1)
