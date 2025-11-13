#!/usr/bin/env bash

# Usage: ./test_matrix.sh N m k n
# Example: ./test_matrix.sh 5 10 12 13

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 N m k n"
    exit 1
fi

N=$1
m=$2
k=$3
n=$4

success_count=0
fail_count=0

for i in $(seq 1 $N); do
    echo "==============================="
    echo "Trial $i/$N"
    
    # Step 1: regenerate input
    echo "Generating input..."
    make input m=$m k=$k n=$n
    if [ $? -ne 0 ]; then
        echo "❌ Failed to generate input."
        fail_count=$((fail_count+1))
        continue
    fi

    # Step 2: run PySpark
    echo "Running PySpark matrix multiplication..."
    make run
    if [ $? -ne 0 ]; then
        echo "❌ PySpark run failed."
        fail_count=$((fail_count+1))
        continue
    fi

    # Step 3: check result
    echo "Checking result..."
    make check
    if [ $? -eq 0 ]; then
        echo "✅ Trial $i: Success!"
        success_count=$((success_count+1))
    else
        echo "❌ Trial $i: Failed!"
        fail_count=$((fail_count+1))
    fi
done

echo "==============================="
echo "Finished $N trials"
echo "Successes: $success_count"
echo "Failures:  $fail_count"
