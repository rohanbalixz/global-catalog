import os
import boto3
import random

class CatalogRouter:
    def __init__(self, regions=None):
        # List of regions to failover across
        self.regions = regions or os.getenv("DDB_REGIONS", "us-east-1,us-west-2").split(",")
        # Initialize a boto3 session per region
        self.sessions = {r: boto3.Session(region_name=r) for r in self.regions}

    def get_table(self, table_name):
        # Pick primary region first, else random
        primary = self.regions[0]
        try:
            return self.sessions[primary].resource("dynamodb").Table(table_name)
        except Exception:
            # On failure, pick a random secondary region
            fallback = random.choice(self.regions[1:])
            return self.sessions[fallback].resource("dynamodb").Table(table_name)

# Example usage
if __name__ == "__main__":
    router = CatalogRouter()
    table = router.get_table("GlobalCatalog")
    print(f"Using DynamoDB table in region: {table.meta.client.meta.region_name}")
