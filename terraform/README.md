## General notes & Commands

**Terraform** is an *IaC* (*Infrastructure as Code*) tool. 

It is used to create and manage cloud resources through code using a **declarative language**. 

> You can execute Terraform inside an EC2 instance, if you have the right permissions on the IAM Role attached to the EC2 instance. For example, a policy to create S3 resources.

### Create a main.ts file to configure the provider.

Go to google and search [‘terraform aws provider’](https://registry.terraform.io/providers/hashicorp/aws/latest/docs).

**Copy the code in USE PROVIDER button:**
```
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "6.15.0"
    }
  }
}

provider "aws" {
  # Configuration options
}
```

**Configure the AWS Provider:**
```
provider "aws" {
  region = "us-east-1"
}
```

**Initialize terraform.**

Execute in your terminal:
```bash
terraform init
```

### Create an S3 bucket

Go to google and search [‘terraform aws s3 bucket’](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket.html).

**Add it into main.ts:**
```
# Create the S3 bucket
resource "aws_s3_bucket" "my_bucket" {
  # S3 bucket names are globally unique across all AWS accounts and all regions.
  bucket = "<Your unique bucket name>"

  # Forces the bucket to be destroyed even if it has objects inside
  force_destroy = true
}
```

**Format the file:**

Execute in your terminal:
```bash
terraform fmt
```

**Check the plan:**

Execute in your terminal:
```bash
terraform plan
```

**Apply it to create the bucket:**

Execute in your terminal:
```bash
terraform apply
```

**Destroy the bucket:**

Execute in your terminal:
```bash
terraform destroy
```
