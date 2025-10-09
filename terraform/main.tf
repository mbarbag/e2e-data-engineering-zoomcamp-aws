terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.15.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# Create the S3 bucket
resource "aws_s3_bucket" "my_bucket" {
  # S3 bucket names are globally unique across all AWS accounts and all regions.
  bucket = "my-terraform-bucket-203918861455"

  # Forces the bucket to be destroyed even if it has objects inside
  force_destroy = true
}
