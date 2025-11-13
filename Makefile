SPARK_IMAGE := apache/spark:latest
PROJECT_LOCAL_DIR := $(shell pwd)
PROJECT_CONTAINER_DIR := /app
SCRIPT := matrix_multiplication.py
LOCAL_PY := python3.10

m ?= 2
k ?= 2
n ?= 2
N ?= 1 

.PHONY: run
run:
	docker run -it --rm \
		-v $(PROJECT_LOCAL_DIR):$(PROJECT_CONTAINER_DIR) \
		$(SPARK_IMAGE) \
		/opt/spark/bin/spark-submit $(PROJECT_CONTAINER_DIR)/$(SCRIPT)

.PHONY: input
input:
	$(LOCAL_PY) ./gen_input.py $(m) $(k) $(n)

.PHONE: check
check:
	$(LOCAL_PY) ./check_result.py ./input/Expected.csv ./output/result.csv

.PHONY: test
test:
	./test_algorithm.sh $(N) $(m) $(k) $(n)