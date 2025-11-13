#!/usr/bin/env python3
import sys
import csv
import numpy as np
import os

def main():
    if len(sys.argv) != 4:
        print("Usage: ./gen_input.py rows_A cols_A_rows_B cols_B")
        sys.exit(1)

    rows_A = int(sys.argv[1])
    cols_A_rows_B = int(sys.argv[2])
    cols_B = int(sys.argv[3])

    # Generate random integer matrices
    np.random.seed(42)  # for reproducibility
    A = np.random.randint(0, 10, size=(rows_A, cols_A_rows_B))
    B = np.random.randint(0, 10, size=(cols_A_rows_B, cols_B))

    # Compute expected result
    C = np.matmul(A, B)

    # Make output directory
    os.makedirs("input", exist_ok=True)

    # Save CSVs
    np.savetxt("input/A.csv", A, fmt="%d", delimiter=",")
    np.savetxt("input/B.csv", B, fmt="%d", delimiter=",")
    np.savetxt("input/Expected.csv", C, fmt="%d", delimiter=",")

    print(f"Generated A.csv ({rows_A}x{cols_A_rows_B}), B.csv ({cols_A_rows_B}x{cols_B}), Expected.csv ({rows_A}x{cols_B}) in ./input/")

if __name__ == "__main__":
    main()
