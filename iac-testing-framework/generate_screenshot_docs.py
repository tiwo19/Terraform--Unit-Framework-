#!/usr/bin/env python3
"""
Screenshot Documentation Generator
This script generates text-based documentation for the screenshots that would be included in the MSc report
"""

import json
from pathlib import Path
from datetime import datetime

def generate_screenshot_documentation():
    """Generate documentation for all screenshots needed for the MSc report"""
    
    screenshots_dir = Path(__file__).parent / "screenshots"
    
    # Create screenshot documentation
    screenshot_docs = {
        "tflint_run": {
            "filename": "tflint_run.png",
            "description": "TFLint Static Analysis Execution",
            "content": {
                "command": "tflint --format=json --chdir ./static_analysis/examples",
                "output": {
                    "issues": [
                        {
                            "rule": "terraform_required_version",
                            "severity": "warning",
                            "message": "terraform_required_version is required",
                            "filename": "main.tf",
                            "line": 1
                        }
                    ],
                    "total_issues": 1
                }
            },
            "msc_caption": "Figure X.X: TFLint execution showing static analysis results with one warning about missing terraform_required_version"
        },
        
        "checkov_scan": {
            "filename": "checkov_scan.png",
            "description": "Checkov Security Analysis Execution",
            "content": {
                "command": "checkov --directory ./static_analysis/examples --output json",
                "output": {
                    "passed_checks": 15,
                    "failed_checks": 3,
                    "skipped_checks": 2,
                    "parsing_errors": 0,
                    "results": [
                        {
                            "check_id": "CKV_AWS_23",
                            "check_name": "Ensure Security group does not have an unrestricted inbound rule",
                            "check_result": "FAILED",
                            "file_path": "main.tf",
                            "file_line_range": [10, 15],
                            "resource": "aws_security_group.web",
                            "severity": "HIGH"
                        }
                    ]
                }
            },
            "msc_caption": "Figure X.X: Checkov security scan results showing 3 failed checks including unrestricted security group rule"
        },
        
        "json_output": {
            "filename": "json_output.png",
            "description": "Framework JSON Report Output",
            "content": {
                "report_structure": {
                    "analysis_timestamp": "2025-07-17T10:30:00Z",
                    "terraform_directory": "./static_analysis/examples",
                    "analysis_type": "combined",
                    "static_analysis": {
                        "status": "success",
                        "terraform_files_found": 1,
                        "summary": {
                            "total_issues": 4,
                            "validation_passed": True,
                            "overall_status": "NEEDS_ATTENTION"
                        }
                    },
                    "policy_compliance": {
                        "status": "success",
                        "total_policies": 4,
                        "passed_policies": 2,
                        "failed_policies": 2,
                        "summary": {
                            "compliance_score": 50.0,
                            "overall_status": "FAILED"
                        }
                    },
                    "summary": {
                        "total_checks": 8,
                        "overall_status": "NEEDS_ATTENTION"
                    }
                }
            },
            "msc_caption": "Figure X.X: Complete framework JSON output showing combined static analysis and policy compliance results"
        },
        
        "cli_execution": {
            "filename": "cli_execution.png",
            "description": "Command Line Interface Execution",
            "content": {
                "command": "python test_runner.py combined ./static_analysis/examples",
                "output": {
                    "console_output": [
                        "🚀 Running Combined Analysis...",
                        "🔍 Running Static Analysis...",
                        "🔐 Running Policy Compliance Checks...",
                        "✅ Combined results saved to: results.json",
                        "",
                        "============================================================",
                        "📊 ANALYSIS SUMMARY",
                        "============================================================",
                        "📁 Directory: ./static_analysis/examples",
                        "🕐 Timestamp: 2025-07-17T10:30:00.123456",
                        "📄 Analysis Type: combined",
                        "",
                        "🔍 Static Analysis:",
                        "   - Status: success",
                        "   - Total Issues: 4",
                        "   - Validation: ✅ PASSED",
                        "",
                        "🔐 Policy Compliance:",
                        "   - Status: success",
                        "   - Total Policies: 4",
                        "   - Passed: 2",
                        "   - Failed: 2",
                        "   - Score: 50.0%",
                        "",
                        "📈 Overall Status: NEEDS_ATTENTION"
                    ]
                }
            },
            "msc_caption": "Figure X.X: Command-line execution of the framework showing combined analysis results"
        },
        
        "terraform_validate": {
            "filename": "terraform_validate.png",
            "description": "Terraform Validate Execution",
            "content": {
                "command": "terraform validate -json",
                "output": {
                    "format_version": "1.0",
                    "valid": True,
                    "error_count": 0,
                    "warning_count": 0,
                    "diagnostics": []
                }
            },
            "msc_caption": "Figure X.X: Terraform validate command showing successful syntax validation"
        },
        
        "policy_compliance_demo": {
            "filename": "policy_compliance_demo.png",
            "description": "Policy Compliance Check Results",
            "content": {
                "policies_loaded": 4,
                "results": [
                    {
                        "policy_name": "require_encryption",
                        "status": "FAILED",
                        "violations": 2,
                        "description": "All storage resources must be encrypted"
                    },
                    {
                        "policy_name": "tag_compliance",
                        "status": "FAILED",
                        "violations": 3,
                        "description": "All resources must have required tags"
                    },
                    {
                        "policy_name": "security_group_rules",
                        "status": "PASSED",
                        "violations": 0,
                        "description": "Security groups must not allow unrestricted access"
                    },
                    {
                        "policy_name": "instance_type_compliance",
                        "status": "PASSED",
                        "violations": 0,
                        "description": "Only approved instance types are allowed"
                    }
                ],
                "compliance_score": 50.0
            },
            "msc_caption": "Figure X.X: Policy compliance check results showing 50% compliance score with detailed violation breakdown"
        }
    }
    
    # Generate documentation file
    documentation = {
        "title": "IaC Testing Framework - Phase 2 Screenshots Documentation",
        "description": "This document describes the screenshots to be included in the MSc report",
        "generated_on": datetime.now().isoformat(),
        "screenshots": screenshot_docs,
        "instructions": {
            "for_msc_report": [
                "1. Take actual screenshots of the described commands and outputs",
                "2. Include clear, readable terminal/console output",
                "3. Use the provided captions for the MSc report",
                "4. Ensure screenshots show the framework's capabilities clearly",
                "5. Include both successful and failed test cases for completeness"
            ],
            "technical_requirements": [
                "Resolution: At least 1920x1080 for clarity",
                "Format: PNG for text clarity",
                "Font: Use a clear monospace font in terminal",
                "Annotations: Add arrows or highlights if needed for clarity"
            ]
        }
    }
    
    # Save documentation
    doc_path = screenshots_dir / "screenshot_documentation.json"
    with open(doc_path, 'w') as f:
        json.dump(documentation, f, indent=2)
    
    print(f"📸 Screenshot documentation generated: {doc_path}")
    
    # Generate individual placeholder files for each screenshot
    for screenshot_name, screenshot_info in screenshot_docs.items():
        placeholder_path = screenshots_dir / f"{screenshot_info['filename']}.placeholder"
        with open(placeholder_path, 'w') as f:
            f.write(f"# {screenshot_info['description']}\n")
            f.write(f"# This is a placeholder for {screenshot_info['filename']}\n")
            f.write(f"# MSc Caption: {screenshot_info['msc_caption']}\n\n")
            f.write(f"# Expected Content:\n")
            f.write(f"# {json.dumps(screenshot_info['content'], indent=2)}\n")
    
    print(f"📄 Generated {len(screenshot_docs)} screenshot placeholder files")
    
    return documentation

if __name__ == "__main__":
    generate_screenshot_documentation()
