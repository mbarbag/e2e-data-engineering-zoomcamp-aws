variable "region" {
  description = "Region"
  default     = "us-east-1"
}

variable "bucket_name" {
  description = "Storage unique name"
  # S3 bucket names are globally unique across all AWS accounts and all regions.
  default = "<my-globally-unique-bucket-name>"
}
