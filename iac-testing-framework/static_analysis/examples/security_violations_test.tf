# DELIBERATELY BROKEN - Security Policy Violations Test Case
# This file contains KNOWN POLICY VIOLATIONS for testing framework effectiveness
# Expected Policy Violations: 25 security policy issues

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

# SECURITY VIOLATION 1-4: Multiple S3 buckets without encryption
resource "aws_s3_bucket" "data_bucket" {
  bucket = "company-sensitive-data-123"
  # VIOLATION: No encryption configuration
  
  tags = {
    Name = "DataBucket"
    # VIOLATION: Missing required Environment, Owner, Project tags
  }
}

resource "aws_s3_bucket" "backup_bucket" {
  bucket = "company-backups-456"
  # VIOLATION: No encryption configuration
  
  tags = {
    Name = "BackupBucket"
    # VIOLATION: Missing required tags
  }
}

resource "aws_s3_bucket" "logs_bucket" {
  bucket = "company-logs-789"
  # VIOLATION: No encryption configuration
  
  # VIOLATION: No tags at all
}

# SECURITY VIOLATION 5-8: Overly permissive security groups
resource "aws_security_group" "web_dmz" {
  name_prefix = "web-dmz-"
  description = "DMZ security group"
  
  # VIOLATION: SSH open to world
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  # VIOLATION: RDP open to world
  ingress {
    from_port   = 3389
    to_port     = 3389
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  # VIOLATION: Database port open to world
  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  # VIOLATION: All outbound traffic allowed
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "WebDMZ"
    # VIOLATION: Missing required tags
  }
}

resource "aws_security_group" "database_sg" {
  name_prefix = "db-"
  description = "Database security group"
  
  # VIOLATION: Database accessible from anywhere
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "DatabaseSG"
    # VIOLATION: Missing required tags
  }
}

# SECURITY VIOLATION 9-12: EC2 instances with security issues
resource "aws_instance" "web_server_1" {
  ami           = "ami-12345678"
  instance_type = "t3.xlarge"  # VIOLATION: Oversized for policy requirements
  
  vpc_security_group_ids = [aws_security_group.web_dmz.id]
  
  # VIOLATION: No detailed monitoring
  monitoring = false
  
  # VIOLATION: Root volume not encrypted
  root_block_device {
    volume_type = "gp3"
    volume_size = 100
    encrypted   = false
  }
  
  # VIOLATION: Missing required tags
  tags = {
    Name = "WebServer1"
  }
}

resource "aws_instance" "web_server_2" {
  ami           = "ami-12345678"
  instance_type = "m5.large"   # VIOLATION: Not in approved instance types
  
  vpc_security_group_ids = [aws_security_group.web_dmz.id]
  
  # VIOLATION: No monitoring
  monitoring = false
  
  # VIOLATION: Root volume not encrypted
  root_block_device {
    encrypted = false
  }
  
  # VIOLATION: No tags at all - complete policy violation
}

resource "aws_instance" "database_server" {
  ami           = "ami-12345678"
  instance_type = "r5.2xlarge"  # VIOLATION: Oversized and not approved
  
  vpc_security_group_ids = [aws_security_group.database_sg.id]
  
  # VIOLATION: No monitoring
  monitoring = false
  
  # VIOLATION: Root volume not encrypted
  root_block_device {
    encrypted = false
  }
  
  tags = {
    Name = "DatabaseServer"
    # VIOLATION: Missing Environment, Owner, Project
  }
}

# SECURITY VIOLATION 13-16: Additional S3 buckets with issues
resource "aws_s3_bucket" "public_website" {
  bucket = "company-public-site-000"
  # VIOLATION: No encryption even for public content
  
  tags = {
    Name = "PublicWebsite"
    # VIOLATION: Missing required tags
  }
}

# SECURITY VIOLATION 17-20: IAM and access issues
resource "aws_s3_bucket_public_access_block" "public_website" {
  bucket = aws_s3_bucket.public_website.id
  
  # VIOLATION: Public access enabled (against security policy)
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_public_access_block" "data_bucket" {
  bucket = aws_s3_bucket.data_bucket.id
  
  # VIOLATION: Sensitive data bucket allowing some public access
  block_public_acls       = true
  block_public_policy     = false  # VIOLATION: Should block all public access
  ignore_public_acls      = false  # VIOLATION: Should ignore public ACLs
  restrict_public_buckets = false  # VIOLATION: Should restrict public buckets
}

# SECURITY VIOLATION 21-25: Network and additional security groups
resource "aws_security_group" "management_sg" {
  name_prefix = "mgmt-"
  description = "Management security group"
  
  # VIOLATION: Management interfaces open to world
  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  # VIOLATION: SNMP open to world
  ingress {
    from_port   = 161
    to_port     = 161
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "ManagementSG"
    # VIOLATION: Missing required tags
  }
}

# Additional resources without proper configuration for comprehensive testing
