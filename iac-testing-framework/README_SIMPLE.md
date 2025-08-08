# 🚀 IaC Testing Framework

A simple and effective Infrastructure as Code (IaC) testing framework that provides static analysis, policy compliance checking, and dynamic testing for Terraform configurations.

## ✨ Features

- **🔍 Static Analysis**: Terraform syntax validation, security scanning with Checkov, and linting
- **🔐 Policy Compliance**: Custom policy validation with detailed reporting
- **🚀 Dynamic Testing**: Deploy and test infrastructure in LocalStack or real AWS environments
- **📊 Comprehensive Reporting**: Detailed reports with issue breakdowns and compliance scores
- **🌍 Multi-Environment**: Support for safe LocalStack testing and real AWS deployment

## 🏗️ Simple Architecture

```
iac-testing-framework/
├── comprehensive_runner.py    # Main test runner
├── static_analysis/          # Static analysis components
├── policy_compliance/        # Policy checking components  
├── dynamic_provisioning/     # Dynamic testing components
├── aws_config.json          # Environment configuration
├── check_environment.py     # Environment verification tool
└── docker-compose.yml       # LocalStack setup
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Check Your Environment
```bash
python check_environment.py
```

### 3. Run Simple Testing

**Basic Static Analysis:**
```bash
python comprehensive_runner.py static ./static_analysis/examples
```

**Comprehensive Testing with LocalStack (Safe):**
```bash
# Start LocalStack first
docker-compose up -d localstack

# Run comprehensive testing
python comprehensive_runner.py comprehensive ./static_analysis/examples --environment localstack --include-dynamic
```

**Real AWS Testing (Advanced):**
```bash
# Configure AWS credentials first (aws configure)
python comprehensive_runner.py comprehensive ./static_analysis/examples --environment aws --include-dynamic
```

## 📋 Simple Commands

### Quick Commands
```bash
# Just check syntax and security
python comprehensive_runner.py static ./static_analysis/examples

# Check compliance policies
python comprehensive_runner.py policy ./static_analysis/examples

# Test with LocalStack (no real AWS resources)
python comprehensive_runner.py comprehensive ./static_analysis/examples --environment localstack --include-dynamic

# Test with real AWS (be careful - creates real resources!)
python comprehensive_runner.py comprehensive ./static_analysis/examples --environment aws --include-dynamic
```

## 🌍 Environment Setup

### LocalStack (Recommended - Safe & Free)
```bash
# Install Docker
# Start LocalStack
docker-compose up -d localstack

# Use in commands
--environment localstack
```

### Real AWS (Advanced - Costs Money!)
```bash
# Configure AWS credentials
aws configure

# Use in commands (careful!)
--environment aws
```

## 🔧 AWS Credentials (Simple Setup)

Choose the easiest option for you:

1. **AWS CLI (Recommended)**:
   ```bash
   aws configure
   ```

2. **Environment Variables**:
   ```bash
   set AWS_ACCESS_KEY_ID=your_key
   set AWS_SECRET_ACCESS_KEY=your_secret
   ```

## 📊 Understanding Results

The framework gives you simple, clear results:

```
🔍 Static Analysis:
   - Files Analyzed: 3
   - Security Issues: 2
   - Status: ✅ PASSED

🔐 Policy Compliance:
   - Policies Checked: 8
   - Passed: 6
   - Failed: 2
   - Score: 75%

🚀 Dynamic Testing:
   - Deployment: ✅ SUCCESS
   - Tests: 5/5 passed

📈 Overall: ✅ NEEDS_ATTENTION (84.6% success)
```

## 🔧 Troubleshooting

### Common Issues & Simple Fixes

**"No AWS credentials found"**
```bash
# Fix: Configure AWS
aws configure
```

**"LocalStack is not running"**
```bash
# Fix: Start LocalStack
docker-compose up -d localstack
```

**"Terraform command failed"**
```bash
# Fix: Install Terraform
# Download from: https://terraform.io/downloads
```

### Quick Environment Check
```bash
python check_environment.py
```

## 🎯 Simple Use Cases

### For Developers
```bash
# Quick check before committing code
python comprehensive_runner.py static ./my-terraform/
```

### For Testing
```bash
# Safe testing with LocalStack
python comprehensive_runner.py comprehensive ./my-terraform/ --environment localstack --include-dynamic
```

### For Production
```bash
# Final validation before deployment
python comprehensive_runner.py comprehensive ./production-terraform/ --environment aws --include-dynamic
```

## 📈 Why Use This Framework?

- **🚀 Fast**: Get results in minutes, not hours
- **🔒 Safe**: Test with LocalStack before touching real AWS
- **💰 Cost-Effective**: Catch issues before they cost money
- **📋 Simple**: Easy commands, clear results
- **🎯 Comprehensive**: Covers security, compliance, and functionality

## 🤝 Getting Help

1. **Check Environment**: `python check_environment.py`
2. **View Detailed Reports**: Check the generated `detailed_*_report_*.txt` files
3. **Use LocalStack First**: Always test safely before using real AWS

## 📄 License

MIT License - feel free to use and modify!
