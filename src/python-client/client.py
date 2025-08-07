import os
import boto3
from boto3.dynamodb.conditions import Key

class CatalogClient:
    def __init__(self, region_name=None, table_name=None):
        self.region = region_name or os.getenv("AWS_REGION", "us-east-1")
        self.table_name = table_name or os.getenv("DDB_TABLE", "GlobalCatalog")
        session = boto3.Session(region_name=self.region)
        self.dynamodb = session.resource("dynamodb")
        self.table = self.dynamodb.Table(self.table_name)

    def put_item(self, item_id: str, data: dict, category: str):
        item = {"ItemID": item_id, "Category": category, **data}
        return self.table.put_item(Item=item)

    def get_item(self, item_id: str) -> dict:
        resp = self.table.get_item(Key={"ItemID": item_id})
        return resp.get("Item")

    def query_by_category(self, category: str) -> list:
        resp = self.table.query(
            IndexName="ByCategory",
            KeyConditionExpression=Key("Category").eq(category)
        )
        return resp.get("Items", [])

if __name__ == "__main__":
    # simple smoke test
    client = CatalogClient()
    print("Putting test item…")
    client.put_item("test123", {"Name": "Example"}, "Demo")
    print("Fetching test item…", client.get_item("test123"))
    print("Querying category ‘Demo’…", client.query_by_category("Demo"))
