# DELIBERATELY BROKEN - Compliance Requirements Test Case
# This file contains KNOWN COMPLIANCE VIOLATIONS for testing framework effectiveness
# Expected Compliance Violations: 17 compliance requirement issues

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

# COMPLIANCE VIOLATION 1-4: Financial data storage without compliance
resource "aws_s3_bucket" "financial_records" {
  bucket = "company-financial-data-2024"
  # VIOLATION: No encryption for financial data (SOX compliance)
  
  tags = {
    Name = "FinancialRecords"
    # VIOLATION: Missing DataClassification tag required for compliance
    # VIOLATION: Missing RetentionPeriod tag required for compliance  
    # VIOLATION: Missing ComplianceLevel tag
  }
}

# COMPLIANCE VIOLATION 5-7: Healthcare data without HIPAA compliance
resource "aws_s3_bucket" "patient_data" {
  bucket = "company-patient-records-2024"
  # VIOLATION: No encryption for HIPAA data
  
  tags = {
    Name = "PatientData"
    # VIOLATION: Missing HIPAA compliance tags
    # VIOLATION: Missing data retention policies
  }
}

# COMPLIANCE VIOLATION 8-10: Production resources without proper governance
resource "aws_instance" "production_web" {
  ami           = "ami-12345678"
  instance_type = "t3.small"
  
  # VIOLATION: Production instance without backup configuration
  # VIOLATION: No disaster recovery plan referenced
  # VIOLATION: Missing compliance monitoring
  
  tags = {
    Name = "ProductionWeb"
    Environment = "production"
    # VIOLATION: Missing ChangeControl tag required for production
    # VIOLATION: Missing BackupPolicy tag
    # VIOLATION: Missing DisasterRecovery tag
  }
}

# COMPLIANCE VIOLATION 11-13: Audit and logging requirements
resource "aws_instance" "audit_server" {
  ami           = "ami-12345678"  
  instance_type = "t3.medium"
  
  # VIOLATION: Audit server without enhanced monitoring
  monitoring = false
  
  # VIOLATION: No audit trail configuration
  # VIOLATION: Missing log retention policies
  
  tags = {
    Name = "AuditServer"
    Environment = "production"
    # VIOLATION: Missing AuditLevel tag
    # VIOLATION: Missing LogRetention tag
  }
}

# COMPLIANCE VIOLATION 14-15: Network compliance issues
resource "aws_security_group" "compliance_sg" {
  name_prefix = "compliance-"
  description = "Compliance security group"
  
  # VIOLATION: Missing network segmentation for compliance
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # VIOLATION: Should be restricted for compliance
  }
  
  tags = {
    Name = "ComplianceSG"
    # VIOLATION: Missing NetworkZone tag for compliance
    # VIOLATION: Missing ComplianceLevel tag
  }
}

# COMPLIANCE VIOLATION 16-17: Data governance violations
resource "aws_s3_bucket" "customer_data" {
  bucket = "company-customer-pii-2024"
  # VIOLATION: PII data without encryption (GDPR compliance)
  
  tags = {
    Name = "CustomerData"
    # VIOLATION: Missing GDPR compliance tags
    # VIOLATION: Missing data sovereignty tags
  }
}
