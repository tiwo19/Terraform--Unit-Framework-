# IaC Testing Framework - Phase 2

## 📋 Overview
This is the Phase 2 implementation of the IaC Testing Framework for the MSc project: **"Design and Development of a Testing Automation Framework for Infrastructure as Code (IaC) in Scalable Cloud Deployments"**.

Phase 2 focuses on implementing **Static Analysis** and **Policy Compliance** modules that automatically validate Terraform infrastructure code.

## 🏗️ Architecture

```
IaC Testing Framework
├── Static Analysis Module
│   ├── terraform validate (syntax validation)
│   ├── TFLint (best practices & linting)
│   └── Checkov (security scanning)
├── Policy Compliance Module
│   ├── Custom policy engine
│   ├── YAML/JSON policy definitions
│   └── Open Policy Agent (OPA) integration
├── CLI Interface
│   ├── Individual module execution
│   ├── Combined analysis
│   └── Report generation
└── Reporting
    ├── JSON output
    ├── Summary reports
    └── Pass/fail status
```

## 🚀 Features

### ✅ Static Analysis
- **Terraform Validate**: Syntax and configuration validation
- **TFLint**: Linting and best practices enforcement
- **Checkov**: Security and compliance scanning
- **Comprehensive reporting**: JSON output with detailed results

### ✅ Policy Compliance
- **Custom policies**: Define organizational policies in YAML/JSON
- **Resource validation**: Check Terraform resources against policies
- **Compliance scoring**: Calculate compliance percentages
- **Violation tracking**: Detailed violation reports

### ✅ CLI Interface
- **Modular execution**: Run individual or combined analysis
- **Flexible output**: Console output or JSON file export
- **Demo mode**: Built-in demonstration capabilities

## 📁 Project Structure

```
iac-testing-framework/
├── static_analysis/
│   ├── static_checker.py          # Static analysis implementation
│   └── examples/
│       └── main.tf                # Example Terraform configuration
├── policy_compliance/
│   ├── compliance_checker.py      # Policy compliance implementation
│   └── policies/
│       └── sample_policy.yaml     # Sample policy definitions
├── reports/
│   ├── sample_report.json         # Sample output report
│   └── phase2_demo_report.json    # Demo execution report
├── cli.py                         # Original CLI interface
├── test_runner.py                 # Enhanced test runner with CLI
├── demo_phase2.py                 # Phase 2 demonstration script
├── requirements.txt               # Python dependencies
└── README.md                      # This documentation
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Terraform
- TFLint (optional, for enhanced static analysis)
- Checkov (optional, for security scanning)

### Setup
1. Clone the repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Install additional tools:
   ```bash
   # Install TFLint
   curl -s https://raw.githubusercontent.com/terraform-linters/tflint/master/install_linux.sh | bash
   
   # Install Checkov
   pip install checkov
   ```

## 🎯 Usage

### Command Line Interface

#### Run Static Analysis Only
```bash
python test_runner.py static ./terraform_directory
```

#### Run Policy Compliance Only
```bash
python test_runner.py policy ./terraform_directory --policies ./policy_directory
```

#### Run Combined Analysis
```bash
python test_runner.py combined ./terraform_directory --output results.json
```

#### Run Phase 2 Demonstration
```bash
python test_runner.py demo
```

### Programmatic Usage

```python
from static_analysis.static_checker import StaticChecker
from policy_compliance.compliance_checker import ComplianceChecker

# Static Analysis
checker = StaticChecker()
results = checker.analyze_terraform_files("./terraform_directory")

# Policy Compliance
compliance = ComplianceChecker("./policies")
compliance_results = compliance.check_compliance("./terraform_directory")
```

## 📊 Sample Output

### Static Analysis Results
```json
{
  "status": "success",
  "terraform_directory": "./static_analysis/examples",
  "terraform_files_found": 1,
  "analysis_timestamp": "2025-07-17T10:30:00.123456",
  "results": {
    "terraform_validate": {
      "tool": "terraform_validate",
      "status": "success",
      "valid": true,
      "error_count": 0,
      "warning_count": 0
    },
    "tflint": {
      "tool": "tflint",
      "status": "success",
      "total_issues": 2,
      "issues": [...]
    },
    "checkov": {
      "tool": "checkov",
      "status": "success",
      "failed_checks": 3,
      "passed_checks": 15,
      "total_checks": 18
    }
  },
  "summary": {
    "total_issues": 5,
    "validation_passed": true,
    "overall_status": "NEEDS_ATTENTION"
  }
}
```

### Policy Compliance Results
```json
{
  "status": "success",
  "terraform_directory": "./static_analysis/examples",
  "total_policies": 4,
  "passed_policies": 3,
  "failed_policies": 1,
  "results": [
    {
      "policy_name": "require_encryption",
      "description": "All storage resources must be encrypted",
      "status": "PASSED",
      "applicable_resources": 2,
      "violations": [],
      "violation_count": 0
    }
  ],
  "summary": {
    "compliance_score": 75.0,
    "overall_status": "NEEDS_ATTENTION"
  }
}
```

## 🔧 Configuration

### Policy Definitions
Create custom policies in YAML format:

```yaml
policies:
  - name: "require_encryption"
    description: "All storage resources must be encrypted"
    resource_types:
      - "aws_s3_bucket"
      - "aws_ebs_volume"
    rules:
      - property: "encryption"
        required: true
      - property: "encrypted"
        required: true
        value: true

  - name: "tag_compliance"
    description: "All resources must have required tags"
    resource_types:
      - "aws_instance"
      - "aws_s3_bucket"
    rules:
      - property: "tags"
        required: true
        required_keys:
          - "Environment"
          - "Owner"
```

## 🧪 Testing

### Run Demo
```bash
python demo_phase2.py
```

### Test with Sample Data
```bash
python test_runner.py combined ./static_analysis/examples --output test_results.json
```

## 📈 Phase 2 Evaluation Metrics

- **Detection Accuracy**: Ability to identify misconfigurations
- **False Positive Rate**: Minimizing incorrect flagging
- **Execution Time**: Performance benchmarks
- **Policy Coverage**: Percentage of resources covered by policies
- **Compliance Score**: Overall infrastructure compliance percentage

## 🔮 Next Steps (Phase 3)

- **Dynamic Provisioning**: Deploy infrastructure in sandbox environments
- **Runtime Validation**: Verify deployed resources against expectations
- **Integration Testing**: Test resource interactions and dependencies
- **LocalStack Integration**: Safe local cloud simulation
- **Terratest Integration**: Go-based infrastructure testing

## 🤝 Contributing

This is an MSc project focusing on academic research and demonstration. The framework is designed to be modular and extensible for future enhancements.

## 📄 License

This project is part of an MSc thesis and is intended for academic and research purposes.

---

**MSc Project**: Design and Development of a Testing Automation Framework for Infrastructure as Code (IaC) in Scalable Cloud Deployments  
**Phase**: 2 - Static Analysis & Policy Compliance  
**Status**: ✅ Completed  
**Next Phase**: Dynamic Provisioning & Runtime Validation

