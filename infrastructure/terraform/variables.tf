variable "primary_region" {
  type    = string
  default = "us-east-1"
}

variable "replica_regions" {
  type    = list(string)
  default = ["us-west-2", "eu-central-1"]
}

variable "table_name" {
  type    = string
  default = "GlobalCatalog"
}

variable "environment" {
  type    = string
  default = "dev"
}
