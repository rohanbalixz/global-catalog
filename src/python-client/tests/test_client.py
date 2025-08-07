import os
from moto import mock_dynamodb2
import boto3
import pytest

from client import CatalogClient

@mock_dynamodb2
def test_put_get_and_query():
    region = "us-east-1"
    table_name = "GlobalCatalog"
    os.environ["AWS_REGION"] = region
    os.environ["DDB_TABLE"] = table_name

    dynamodb = boto3.client("dynamodb", region_name=region)
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{"AttributeName": "ItemID", "KeyType": "HASH"}],
        AttributeDefinitions=[
            {"AttributeName": "ItemID", "AttributeType": "S"},
            {"AttributeName": "Category", "AttributeType": "S"}
        ],
        BillingMode="PAY_PER_REQUEST",
        GlobalSecondaryIndexes=[{
            "IndexName": "ByCategory",
            "KeySchema": [{"AttributeName": "Category", "KeyType": "HASH"}],
            "Projection": {"ProjectionType": "ALL"}
        }]
    )

    client = CatalogClient()
    client.put_item("i1", {"Name": "Test"}, "CatA")
    item = client.get_item("i1")
    assert item["Name"] == "Test"
    assert item["Category"] == "CatA"
    items = client.query_by_category("CatA")
    assert len(items) == 1
    assert items[0]["ItemID"] == "i1"
