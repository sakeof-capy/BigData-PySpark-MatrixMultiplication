# Matrix Multiplication using Apache Spark (MapReduce)

## 1. Overview

This project implements **matrix multiplication** using the **MapReduce paradigm** in **Apache Spark (PySpark)**.  
It demonstrates how large matrix operations can be distributed across multiple nodes using Spark’s **RDD (Resilient Distributed Dataset)** abstraction.

The implementation avoids collecting large intermediate results to the driver, ensuring scalability for large datasets.  
Input matrices are generated automatically, processed in parallel by Spark, and verified against an expected output.


## 2. Project Structure

```bash
.
├── check_result.py # Compares Spark output with expected result
├── gen_input.py # Generates random matrices and expected result
├── input
│ ├── A.csv # Matrix A
│ ├── B.csv # Matrix B
│ └── Expected.csv # Expected result (A × B)
├── Makefile # Automates input generation, Spark run, and validation
├── matrix_multiplication.py # Main PySpark MapReduce implementation
├── output
│ └── result.csv # Final merged Spark output
├── README.md # Project report
└── test_algorithm.sh # Script for automated testing
```

## 3. Implementation Details

### a. Input Generation (`gen_input.py`)

- Generates random integer matrices **A (m × k)** and **B (k × n)**.
- Computes their expected product **C (m × n)** using NumPy.
- Saves all matrices as CSV files in the `input/` directory.

### b. Matrix Multiplication (`matrix_multiplication.py`)

Uses **Spark RDD transformations** to simulate **MapReduce**:

1. **Map**: Each element of A and B is converted into key-value pairs based on shared dimension `k`.  
2. **Join**: Pairs are joined by their common key `k`.  
3. **Multiply & Reduce**: Each partial product is multiplied and summed by `(i, j)` key to form each element of the result.  
4. **Output**: The result is written in partitioned form (`part-*` files), then merged into a single `result.csv`.

### c. Result Validation (`check_result.py`)

- Compares Spark-generated `result.csv` with `Expected.csv`.
- Verifies both shape and values.
- Reports **success** or detailed **failure diagnostics**.

---

## 4. Execution Workflow

The workflow is fully automated through the `Makefile`.

### Basic Commands

```bash
# 1. Generate input matrices (A, B, Expected)
make input m=3 k=4 n=2

# 2. Run Spark job inside Docker
make run

# 3. Validate Spark result
make check

# 4. Run multiple randomized tests
make test N=5 m=3 k=4 n=2
```

## 5. Result of multiplication

The result is stored in the following file:
```
output/result.csv
```

## 6. Conclusion

This project successfully demonstrates distributed matrix multiplication using Apache Spark’s RDD-based MapReduce model.
It highlights how large-scale matrix operations can be parallelized efficiently, making it suitable for big data computation.

The combination of PySpark, Docker, and automated validation scripts ensures a reproducible, scalable, and reliable setup for testing distributed algorithms.