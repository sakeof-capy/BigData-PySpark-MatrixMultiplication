from pyspark.sql import SparkSession
import os
import shutil
import glob

spark = SparkSession.builder.appName("MatrixMultiplicationMR").getOrCreate()
sc = spark.sparkContext

A_path = "/app/input/A.csv"
B_path = "/app/input/B.csv"
final_dir = "/app/output/result" 
final_csv = "/app/output/result.csv"

def load_matrix(path):
    rows = sc.textFile(path).map(lambda line: [int(x) for x in line.strip().split(",")])
    return rows.zipWithIndex().map(lambda x: (x[1], x[0]))  # (row_index, row_values)

A = load_matrix(A_path)
B = load_matrix(B_path)

# A[i][k] -> (k, (i, value))
A_mapped = A.flatMap(lambda x: [(k, (x[0], val)) for k, val in enumerate(x[1])])

# B[k][j] -> (k, (j, value))
B_mapped = B.flatMap(lambda x: [(x[0], (j, val)) for j, val in enumerate(x[1])])

# (k, (i, value)) + (k, (j, value)) -> (k, [(i, value), (j, value)])
joined = A_mapped.join(B_mapped)

# (k, [(i, value1), (j, value2)]) -> ([i, j], value1*value2)
products = joined.map(lambda x: ((x[1][0][0], x[1][1][0]), x[1][0][1] * x[1][1][1]))
final_result = products.reduceByKey(lambda x, y: x + y)

# ([i, j], product) -> (i, (j, product))
final_rows = final_result.map(lambda x: (x[0][0], (x[0][1], x[1])))
rows_grouped = final_rows.groupByKey().mapValues(lambda vals: [v for j,v in sorted(vals)])
csv_lines = rows_grouped.sortByKey().map(lambda x: ",".join(map(str, x[1])))

if os.path.exists(final_dir):
    shutil.rmtree(final_dir)

csv_lines.saveAsTextFile(final_dir)

with open(final_csv, "w") as outfile:
    for part_file in sorted(glob.glob(f"{final_dir}/part-*")):
        with open(part_file) as infile:
            for line in infile:
                outfile.write(line)

shutil.rmtree(final_dir)
