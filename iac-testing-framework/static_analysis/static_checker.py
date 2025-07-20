# Static Analysis Checker for Terraform IaC
# This module provides static analysis capabilities for Terraform files

import os
import json
import subprocess
from datetime import datetime
from typing import Dict, List, Any

class StaticChecker:
    """
    Static analysis checker for Terraform infrastructure code
    """
    
    def __init__(self):
        self.results = []
    
    def run_tflint(self, terraform_dir: str) -> Dict[str, Any]:
        """
        Run TFLint static analysis on Terraform files
        
        Args:
            terraform_dir: Directory containing Terraform files
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            # Run TFLint with JSON output
            result = subprocess.run(
                ['tflint', '--format=json', '--chdir', terraform_dir],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                # Parse JSON output
                if result.stdout:
                    tflint_output = json.loads(result.stdout)
                else:
                    tflint_output = {"issues": []}
                
                # Format results
                formatted_results = {
                    "tool": "tflint",
                    "status": "success",
                    "issues": tflint_output.get("issues", []),
                    "total_issues": len(tflint_output.get("issues", [])),
                    "execution_time": None  # Can be added with timing
                }
                
                return formatted_results
            else:
                return {
                    "tool": "tflint",
                    "status": "error",
                    "error_message": result.stderr,
                    "issues": [],
                    "total_issues": 0
                }
                
        except subprocess.TimeoutExpired:
            return {
                "tool": "tflint",
                "status": "timeout",
                "error_message": "TFLint execution timed out",
                "issues": [],
                "total_issues": 0
            }
        except FileNotFoundError:
            return {
                "tool": "tflint",
                "status": "not_found",
                "error_message": "TFLint not found. Please install TFLint.",
                "issues": [],
                "total_issues": 0
            }
        except Exception as e:
            return {
                "tool": "tflint",
                "status": "error",
                "error_message": str(e),
                "issues": [],
                "total_issues": 0
            }
    
    def run_checkov(self, terraform_dir: str) -> Dict[str, Any]:
        """
        Run Checkov security analysis on Terraform files
        
        Args:
            terraform_dir: Directory containing Terraform files
            
        Returns:
            Dictionary containing security analysis results
        """
        try:
            # Run Checkov with JSON output
            result = subprocess.run(
                ['checkov', '--directory', terraform_dir, '--output', 'json', '--quiet'],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            # Checkov returns non-zero exit code when issues are found
            if result.stdout:
                checkov_output = json.loads(result.stdout)
            else:
                checkov_output = {"results": {"failed_checks": [], "passed_checks": []}}
            
            # Extract results
            failed_checks = checkov_output.get("results", {}).get("failed_checks", [])
            passed_checks = checkov_output.get("results", {}).get("passed_checks", [])
            
            # Format results
            formatted_results = {
                "tool": "checkov",
                "status": "success",
                "failed_checks": len(failed_checks),
                "passed_checks": len(passed_checks),
                "total_checks": len(failed_checks) + len(passed_checks),
                "results": {
                    "failed": failed_checks,
                    "passed": passed_checks
                },
                "summary": {
                    "critical": len([check for check in failed_checks if check.get("severity") == "CRITICAL"]),
                    "high": len([check for check in failed_checks if check.get("severity") == "HIGH"]),
                    "medium": len([check for check in failed_checks if check.get("severity") == "MEDIUM"]),
                    "low": len([check for check in failed_checks if check.get("severity") == "LOW"])
                }
            }
            
            return formatted_results
            
        except subprocess.TimeoutExpired:
            return {
                "tool": "checkov",
                "status": "timeout",
                "error_message": "Checkov execution timed out",
                "failed_checks": 0,
                "passed_checks": 0,
                "total_checks": 0
            }
        except FileNotFoundError:
            return {
                "tool": "checkov",
                "status": "not_found",
                "error_message": "Checkov not found. Please install Checkov.",
                "failed_checks": 0,
                "passed_checks": 0,
                "total_checks": 0
            }
        except json.JSONDecodeError:
            return {
                "tool": "checkov",
                "status": "parse_error",
                "error_message": "Failed to parse Checkov JSON output",
                "failed_checks": 0,
                "passed_checks": 0,
                "total_checks": 0
            }
        except Exception as e:
            return {
                "tool": "checkov",
                "status": "error",
                "error_message": str(e),
                "failed_checks": 0,
                "passed_checks": 0,
                "total_checks": 0
            }
    
    def _run_terraform_validate(self, terraform_dir: str) -> Dict[str, Any]:
        """
        Run terraform validate to check syntax and configuration
        
        Args:
            terraform_dir: Directory containing Terraform files
            
        Returns:
            Dictionary containing validation results
        """
        try:
            # First, initialize terraform if needed
            init_result = subprocess.run(
                ['terraform', 'init', '-backend=false'],
                cwd=terraform_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Run terraform validate
            validate_result = subprocess.run(
                ['terraform', 'validate', '-json'],
                cwd=terraform_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if validate_result.returncode == 0:
                if validate_result.stdout:
                    validate_output = json.loads(validate_result.stdout)
                else:
                    validate_output = {"valid": True}
                
                return {
                    "tool": "terraform_validate",
                    "status": "success",
                    "valid": validate_output.get("valid", True),
                    "diagnostics": validate_output.get("diagnostics", []),
                    "error_count": validate_output.get("error_count", 0),
                    "warning_count": validate_output.get("warning_count", 0)
                }
            else:
                return {
                    "tool": "terraform_validate",
                    "status": "error",
                    "valid": False,
                    "error_message": validate_result.stderr,
                    "diagnostics": [],
                    "error_count": 1,
                    "warning_count": 0
                }
                
        except subprocess.TimeoutExpired:
            return {
                "tool": "terraform_validate",
                "status": "timeout",
                "valid": False,
                "error_message": "Terraform validate timed out",
                "diagnostics": [],
                "error_count": 1,
                "warning_count": 0
            }
        except FileNotFoundError:
            return {
                "tool": "terraform_validate",
                "status": "not_found",
                "valid": False,
                "error_message": "Terraform not found. Please install Terraform.",
                "diagnostics": [],
                "error_count": 1,
                "warning_count": 0
            }
        except Exception as e:
            return {
                "tool": "terraform_validate",
                "status": "error",
                "valid": False,
                "error_message": str(e),
                "diagnostics": [],
                "error_count": 1,
                "warning_count": 0
            }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _determine_overall_status(self, validate_result: Dict[str, Any], 
                                 tflint_result: Dict[str, Any], 
                                 checkov_result: Dict[str, Any]) -> str:
        """
        Determine overall status based on all tool results
        
        Args:
            validate_result: Terraform validate results
            tflint_result: TFLint results
            checkov_result: Checkov results
            
        Returns:
            Overall status string
        """
        # Check if any tool failed to run
        if (validate_result.get("status") not in ["success"] or
            tflint_result.get("status") not in ["success"] or
            checkov_result.get("status") not in ["success"]):
            return "TOOL_ERROR"
        
        # Check validation status
        if not validate_result.get("valid", False):
            return "VALIDATION_FAILED"
        
        # Count critical issues
        critical_issues = (
            validate_result.get("error_count", 0) +
            tflint_result.get("total_issues", 0) +
            checkov_result.get("summary", {}).get("critical", 0) +
            checkov_result.get("summary", {}).get("high", 0)
        )
        
        if critical_issues > 0:
            return "CRITICAL_ISSUES"
        
        # Count medium/low issues
        medium_issues = (
            validate_result.get("warning_count", 0) +
            checkov_result.get("summary", {}).get("medium", 0) +
            checkov_result.get("summary", {}).get("low", 0)
        )
        
        if medium_issues > 0:
            return "NEEDS_ATTENTION"
        
        return "PASSED"
    
    def analyze_terraform_files(self, terraform_dir: str) -> Dict[str, Any]:
        """
        Perform comprehensive static analysis on Terraform files
        
        Args:
            terraform_dir: Directory containing Terraform files
            
        Returns:
            Combined analysis results
        """
        if not os.path.exists(terraform_dir):
            return {
                "status": "error",
                "error_message": f"Directory {terraform_dir} does not exist",
                "results": {}
            }
        
        # Check if directory contains Terraform files
        terraform_files = []
        for root, dirs, files in os.walk(terraform_dir):
            for file in files:
                if file.endswith('.tf'):
                    terraform_files.append(os.path.join(root, file))
        
        if not terraform_files:
            return {
                "status": "error",
                "error_message": f"No Terraform files found in {terraform_dir}",
                "results": {}
            }
        
        # Run terraform validate first
        validate_result = self._run_terraform_validate(terraform_dir)
        
        # Run TFLint
        tflint_result = self.run_tflint(terraform_dir)
        
        # Run Checkov
        checkov_result = self.run_checkov(terraform_dir)
        
        # Combine results
        combined_results = {
            "status": "success",
            "terraform_directory": terraform_dir,
            "terraform_files_found": len(terraform_files),
            "analysis_timestamp": self._get_timestamp(),
            "results": {
                "terraform_validate": validate_result,
                "tflint": tflint_result,
                "checkov": checkov_result
            },
            "summary": {
                "total_issues": (
                    tflint_result.get("total_issues", 0) + 
                    checkov_result.get("failed_checks", 0)
                ),
                "validation_passed": validate_result.get("status") == "success",
                "linting_issues": tflint_result.get("total_issues", 0),
                "security_issues": checkov_result.get("failed_checks", 0),
                "overall_status": self._determine_overall_status(
                    validate_result, tflint_result, checkov_result
                )
            }
        }
        
        # Store results for later use
        self.results.append(combined_results)
        
        return combined_results
    
    def get_results_summary(self) -> Dict[str, Any]:
        """
        Get summary of all analysis results
        
        Returns:
            Summary dictionary
        """
        if not self.results:
            return {"message": "No analysis results available"}
        
        latest_result = self.results[-1]
        return {
            "total_analyses": len(self.results),
            "latest_analysis": {
                "timestamp": latest_result.get("analysis_timestamp"),
                "status": latest_result.get("summary", {}).get("overall_status"),
                "total_issues": latest_result.get("summary", {}).get("total_issues", 0),
                "validation_passed": latest_result.get("summary", {}).get("validation_passed", False)
            }
        }
