import time, uuid, random, string
from src.python_client.client import CatalogClient

def random_string(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def benchmark_put(client, n=1000):
    start = time.perf_counter()
    for _ in range(n):
        client.put_item(str(uuid.uuid4()), {"Name": random_string(12)},
                        random.choice(["CatA","CatB","CatC"]))
    dt = time.perf_counter() - start
    print(f"PUT {n} items in {dt:.2f}s — {n/dt:.2f} ops/sec")

def benchmark_query(client, n=1000):
    start = time.perf_counter()
    for _ in range(n):
        client.query_by_category("CatA")
    dt = time.perf_counter() - start
    print(f"QUERY_BY_CATEGORY {n} times in {dt:.2f}s — {n/dt:.2f} ops/sec")

if __name__ == "__main__":
    c = CatalogClient()
    print("Benchmarking Global DynamoDB table:\n")
    benchmark_put(c)
    benchmark_query(c)
