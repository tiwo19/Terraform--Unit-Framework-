# Example Terraform configuration for static analysis testing
# This file demonstrates common Terraform patterns that can be analyzed

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
  s3_use_path_style           = true
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  
  
  access_key                  = "test"
  secret_key                  = "test"
 



   endpoints {
     ec2            = "http://localhost:4566"
     s3             = "http://s3.localhost.localstack.cloud:4566"

  }


}



# Example S3 bucket with encryption
resource "aws_s3_bucket" "example" {
  bucket = "my-terraform-test-bucket-${random_string.bucket_suffix.result}"
  
  tags = {
    Name        = "example-bucket"
    Environment = "dev"
    Owner       = "terraform-team"
  }
}

# Random suffix for unique bucket names
resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
}

resource "aws_s3_bucket_server_side_encryption_configuration" "example" {
  bucket = aws_s3_bucket.example.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Example security group
resource "aws_security_group" "web" {
  name        = "web-security-group"
  description = "Security group for web server"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "web-sg"
    Environment = "dev"
    Owner       = "terraform-team"
  }
}

# Example EC2 instance (LocalStack compatible)
resource "aws_instance" "web" {
  ami           = "ami-12345678"  # LocalStack test AMI
  instance_type = "t2.micro"
  
  vpc_security_group_ids = [aws_security_group.web.id]
  
  tags = {
    Name        = "web-server"
    Environment = "dev" 
    Owner       = "terraform-team"
  }
}

# Variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}
