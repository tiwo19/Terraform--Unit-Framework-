# DELIBERATELY BROKEN Simple Web Application for Testing Framework Effectiveness
# This file contains KNOWN SECURITY ISSUES for testing purposes
# Expected Detection: 6 known issues

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
  # LocalStack configuration for safe testing
  s3_use_path_style           = true
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  access_key                  = "test"
  secret_key                  = "test"
  
  endpoints {
    ec2 = "http://localhost:4566"
    s3  = "http://localhost:4566"
    iam = "http://localhost:4566"
  }
}

# ISSUE 1: S3 Bucket without encryption (SECURITY RISK)
resource "aws_s3_bucket" "web_assets" {
  bucket = "my-public-web-assets-123"
  # Missing: No encryption configuration
  
  tags = {
    Name = "WebAssets"
    # Missing: No Environment or Owner tags (POLICY VIOLATION)
  }
}

# ISSUE 2: S3 Bucket with public read access (SECURITY RISK)
resource "aws_s3_bucket_public_access_block" "web_assets" {
  bucket = aws_s3_bucket.web_assets.id
  
  # DELIBERATELY INSECURE: Allowing public access
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# ISSUE 3: Security Group with overly permissive SSH access (SECURITY RISK)
resource "aws_security_group" "web_sg" {
  name_prefix = "web-app-"
  description = "Security group for web application"
  
  # ISSUE: SSH open to the world
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # SECURITY RISK: Should be restricted
    description = "SSH access"
  }
  
  # ISSUE: HTTP access (should use HTTPS)
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTP access"
  }
  
  # Overly permissive outbound
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "WebSecurityGroup"
    # Missing required tags
  }
}

# ISSUE 4: EC2 Instance without proper monitoring/logging (COMPLIANCE ISSUE)
resource "aws_instance" "web_server" {
  ami           = "ami-12345678"
  instance_type = "t3.large"  # ISSUE: Oversized instance for simple web app
  
  vpc_security_group_ids = [aws_security_group.web_sg.id]
  
  # ISSUE 5: No detailed monitoring enabled
  monitoring = false
  
  # ISSUE 6: Root volume not encrypted
  root_block_device {
    volume_type = "gp3"
    volume_size = 20
    encrypted   = false  # SECURITY RISK: Should be encrypted
  }
  
  # Missing IAM instance profile for proper access management
  
  tags = {
    Name = "WebServer"
    # Missing Environment and Owner tags (POLICY VIOLATIONS)
  }
}

# Missing: No backup configuration
# Missing: No logging configuration  
# Missing: No monitoring/alerting setup

# Output for testing
output "web_server_ip" {
  description = "Public IP of the web server"
  value       = aws_instance.web_server.public_ip
  # ISSUE: Potentially exposing sensitive information
}

output "s3_bucket_name" {
  description = "Name of the S3 bucket"
  value       = aws_s3_bucket.web_assets.bucket
}
