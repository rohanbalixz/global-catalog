terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.primary_region
}

resource "aws_dynamodb_table" "catalog" {
  name              = var.table_name
  billing_mode      = "PAY_PER_REQUEST"
  hash_key          = "ItemID"
  stream_enabled    = true
  stream_view_type  = "NEW_AND_OLD_IMAGES"

  attribute {
    name = "ItemID"
    type = "S"
  }

  attribute {
    name = "Category"
    type = "S"
  }

  global_secondary_index {
    name            = "ByCategory"
    hash_key        = "Category"
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
    Project     = "global-catalog"
  }
}
