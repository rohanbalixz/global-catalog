resource "aws_dynamodb_table" "audit_log" {
  name              = "${var.table_name}-audit"
  billing_mode      = "PAY_PER_REQUEST"
  hash_key          = "EventID"
  stream_enabled    = true
  stream_view_type  = "NEW_AND_OLD_IMAGES"

  attribute {
    name = "EventID"
    type = "S"
  }

  attribute {
    name = "ItemID"
    type = "S"
  }

  attribute {
    name = "Timestamp"
    type = "S"
  }

  global_secondary_index {
    name            = "ByItemID"
    hash_key        = "ItemID"
    range_key       = "Timestamp"
    projection_type = "ALL"
  }

  dynamic "replica" {
    for_each = var.replica_regions
    content {
      region_name = replica.value
    }
  }

  tags = {
    Environment = var.environment
    Project     = "global-catalog-audit"
  }
}
