# Benchmarking

Measures throughput of CatalogClient against your Global DynamoDB table.

## Run

```bash
python3 -m venv .venv-bench
source .venv-bench/bin/activate
pip install boto3
python benchmark/benchmark.py
