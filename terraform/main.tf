terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.15.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# Create the S3 bucket
resource "aws_s3_bucket" "my_bucket" {
  bucket = var.bucket_name

  # Forces the bucket to be destroyed even if it has objects inside
  force_destroy = true
}
