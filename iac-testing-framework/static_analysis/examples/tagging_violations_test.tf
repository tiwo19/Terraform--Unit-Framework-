# DELIBERATELY BROKEN - Resource Tagging Test Case  
# This file contains KNOWN TAGGING VIOLATIONS for testing framework effectiveness
# Expected Tagging Violations: 12 resource tagging policy issues

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-west-2"
  # LocalStack configuration
  s3_use_path_style           = true
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  access_key                  = "test"
  secret_key                  = "test"
  
  endpoints {
    ec2 = "http://localhost:4566"
    s3  = "http://localhost:4566"
  }
}

# TAGGING VIOLATION 1: S3 bucket with no tags at all
resource "aws_s3_bucket" "no_tags_bucket" {
  bucket = "company-no-tags-bucket-123"
  # VIOLATION: Completely missing all required tags
}

# TAGGING VIOLATION 2: S3 bucket with incomplete tags  
resource "aws_s3_bucket" "incomplete_tags_bucket" {
  bucket = "company-incomplete-tags-456"
  
  tags = {
    Name = "IncompleteTagsBucket"
    # VIOLATION: Missing Environment tag
    # VIOLATION: Missing Owner tag  
    # VIOLATION: Missing Project tag
  }
}

# TAGGING VIOLATION 3: EC2 instance with no tags
resource "aws_instance" "no_tags_instance" {
  ami           = "ami-12345678"
  instance_type = "t3.micro"
  # VIOLATION: No tags block at all
}

# TAGGING VIOLATION 4: EC2 instance with partial tags
resource "aws_instance" "partial_tags_instance" {
  ami           = "ami-12345678" 
  instance_type = "t3.micro"
  
  tags = {
    Name = "PartialTagsInstance"
    Environment = "dev"
    # VIOLATION: Missing Owner tag
    # VIOLATION: Missing Project tag
  }
}

# TAGGING VIOLATION 5: Security group with minimal tags
resource "aws_security_group" "minimal_tags_sg" {
  name_prefix = "minimal-"
  description = "Minimal tags security group"
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]
  }
  
  tags = {
    Name = "MinimalTagsSG"
    # VIOLATION: Missing Environment tag
    # VIOLATION: Missing Owner tag
    # VIOLATION: Missing Project tag
  }
}

# TAGGING VIOLATION 6: Another S3 bucket missing tags
resource "aws_s3_bucket" "missing_owner_bucket" {
  bucket = "company-missing-owner-789"
  
  tags = {
    Name = "MissingOwnerBucket"
    Environment = "production"
    Project = "WebApp"
    # VIOLATION: Missing Owner tag
  }
}

# TAGGING VIOLATION 7: EC2 instance missing project tag
resource "aws_instance" "missing_project_instance" {
  ami           = "ami-12345678"
  instance_type = "t3.small"
  
  tags = {
    Name = "MissingProjectInstance"
    Environment = "staging"
    Owner = "devteam"
    # VIOLATION: Missing Project tag
  }
}

# TAGGING VIOLATION 8: Security group missing environment tag
resource "aws_security_group" "missing_env_sg" {
  name_prefix = "missing-env-"
  description = "Missing environment tag security group"
  
  tags = {
    Name = "MissingEnvSG" 
    Owner = "netteam"
    Project = "Infrastructure"
    # VIOLATION: Missing Environment tag
  }
}

# TAGGING VIOLATION 9: S3 bucket with only name tag
resource "aws_s3_bucket" "only_name_bucket" {
  bucket = "company-only-name-000"
  
  tags = {
    Name = "OnlyNameBucket"
    # VIOLATION: Missing Environment tag
    # VIOLATION: Missing Owner tag
    # VIOLATION: Missing Project tag
  }
}

# TAGGING VIOLATION 10-12: Multiple resources with various missing tags
resource "aws_instance" "mixed_missing_tags_1" {
  ami           = "ami-12345678"
  instance_type = "t3.micro"
  
  tags = {
    Name = "MixedMissingTags1"
    Project = "TestApp"
    # VIOLATION: Missing Environment tag
    # VIOLATION: Missing Owner tag
  }
}

resource "aws_instance" "mixed_missing_tags_2" {
  ami           = "ami-12345678"
  instance_type = "t3.micro"
  
  tags = {
    Name = "MixedMissingTags2"
    Environment = "test"
    # VIOLATION: Missing Owner tag
    # VIOLATION: Missing Project tag
  }
}
