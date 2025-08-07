import os
import uuid
import time
import boto3
from boto3.dynamodb.conditions import Key

class CatalogClient:
    def __init__(self, region_name=None, table_name=None):
        self.region = region_name or os.getenv("AWS_REGION", "us-east-1")
        self.table_name = table_name or os.getenv("DDB_TABLE", "GlobalCatalog")
        session = boto3.Session(region_name=self.region)
        self.dynamodb = session.resource("dynamodb")
        self.table = self.dynamodb.Table(self.table_name)
        self.audit_table = self.dynamodb.Table(f"{self.table_name}-audit")

    def _prefixed_id(self, item_id: str) -> str:
        return f"{self.region}#{item_id}"

    def _log_event(self, item_id: str, action: str, version: int):
        event = {
            "EventID": str(uuid.uuid4()),
            "ItemID": self._prefixed_id(item_id),
            "Timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            "Action": action,
            "Version": version
        }
        self.audit_table.put_item(Item=event)

    def put_item(self, item_id: str, data: dict, category: str):
        # Fetch current version
        existing = self.get_item(item_id)
        new_version = (existing.get("Version", 0) + 1) if existing else 1

        pref_id = self._prefixed_id(item_id)
        item = {
            "ItemID": pref_id,
            "Category": category,
            "Version": new_version,
            **data
        }
        resp = self.table.put_item(Item=item)
        self._log_event(item_id, "PUT", new_version)
        return resp

    def get_item(self, item_id: str) -> dict:
        pref_id = self._prefixed_id(item_id)
        resp = self.table.get_item(Key={"ItemID": pref_id})
        item = resp.get("Item")
        if item:
            # strip prefix
            item["ItemID"] = item["ItemID"].split('#',1)[1]
        return item

    def query_by_category(self, category: str) -> list:
        resp = self.table.query(
            IndexName="ByCategory",
            KeyConditionExpression=Key("Category").eq(category)
        )
        items = resp.get("Items", [])
        for item in items:
            item["ItemID"] = item["ItemID"].split('#',1)[1]
        return items

if __name__ == "__main__":
    client = CatalogClient()
    # Smoke test version increments
    print("First put…")
    client.put_item("test123", {"Name": "Example1"}, "Demo")
    print("Second put…")
    client.put_item("test123", {"Name": "Example2"}, "Demo")
    item = client.get_item("test123")
    print("Fetched item with version:", item.get("Version"), item)
