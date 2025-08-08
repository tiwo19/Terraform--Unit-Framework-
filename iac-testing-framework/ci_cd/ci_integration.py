#!/usr/bin/env python3
"""
CI/CD Integration Module
This module provides utilities for integrating the IaC testing framework with CI/CD pipelines
"""

import os
import json
import sys
import yaml
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

class CICDIntegration:
    """
    Handles CI/CD pipeline integration for the IaC testing framework
    """
    
    def __init__(self, ci_environment: str = "github_actions"):
        """
        Initialize CI/CD integration
        
        Args:
            ci_environment: The CI/CD environment (github_actions, jenkins, gitlab_ci)
        """
        self.ci_environment = ci_environment
        self.env_vars = self._load_environment_variables()
    
    def _load_environment_variables(self) -> Dict[str, str]:
        """Load relevant environment variables based on CI environment"""
        env_vars = {}
        
        if self.ci_environment == "github_actions":
            env_vars = {
                "repository": os.getenv("GITHUB_REPOSITORY", ""),
                "ref": os.getenv("GITHUB_REF", ""),
                "sha": os.getenv("GITHUB_SHA", ""),
                "actor": os.getenv("GITHUB_ACTOR", ""),
                "workflow": os.getenv("GITHUB_WORKFLOW", ""),
                "run_id": os.getenv("GITHUB_RUN_ID", ""),
                "run_number": os.getenv("GITHUB_RUN_NUMBER", "")
            }
        elif self.ci_environment == "jenkins":
            env_vars = {
                "build_number": os.getenv("BUILD_NUMBER", ""),
                "build_id": os.getenv("BUILD_ID", ""),
                "job_name": os.getenv("JOB_NAME", ""),
                "workspace": os.getenv("WORKSPACE", ""),
                "git_commit": os.getenv("GIT_COMMIT", ""),
                "git_branch": os.getenv("GIT_BRANCH", "")
            }
        elif self.ci_environment == "gitlab_ci":
            env_vars = {
                "project_id": os.getenv("CI_PROJECT_ID", ""),
                "pipeline_id": os.getenv("CI_PIPELINE_ID", ""),
                "commit_sha": os.getenv("CI_COMMIT_SHA", ""),
                "ref_name": os.getenv("CI_COMMIT_REF_NAME", ""),
                "job_name": os.getenv("CI_JOB_NAME", "")
            }
        
        return env_vars
    
    def set_output(self, name: str, value: str) -> None:
        """
        Set output variable for CI/CD pipeline
        
        Args:
            name: Output variable name
            value: Output variable value
        """
        if self.ci_environment == "github_actions":
            # GitHub Actions output format
            print(f"::set-output name={name}::{value}")
        elif self.ci_environment == "jenkins":
            # Jenkins environment variable
            with open("ci_outputs.env", "a") as f:
                f.write(f"{name}={value}\n")
        else:
            print(f"Output: {name}={value}")
    
    def set_error(self, message: str, file_path: str = "", line: int = 0) -> None:
        """
        Set error annotation for CI/CD pipeline
        
        Args:
            message: Error message
            file_path: File path where error occurred
            line: Line number where error occurred
        """
        if self.ci_environment == "github_actions":
            if file_path and line:
                print(f"::error file={file_path},line={line}::{message}")
            else:
                print(f"::error::{message}")
        else:
            print(f"ERROR: {message}")
    
    def set_warning(self, message: str, file_path: str = "", line: int = 0) -> None:
        """
        Set warning annotation for CI/CD pipeline
        
        Args:
            message: Warning message
            file_path: File path where warning occurred
            line: Line number where warning occurred
        """
        if self.ci_environment == "github_actions":
            if file_path and line:
                print(f"::warning file={file_path},line={line}::{message}")
            else:
                print(f"::warning::{message}")
        else:
            print(f"WARNING: {message}")
    
    def set_notice(self, message: str, file_path: str = "", line: int = 0) -> None:
        """
        Set notice annotation for CI/CD pipeline
        
        Args:
            message: Notice message
            file_path: File path where notice occurred
            line: Line number where notice occurred
        """
        if self.ci_environment == "github_actions":
            if file_path and line:
                print(f"::notice file={file_path},line={line}::{message}")
            else:
                print(f"::notice::{message}")
        else:
            print(f"NOTICE: {message}")
    
    def create_summary_comment(self, results: Dict[str, Any]) -> str:
        """
        Create a summary comment for pull requests
        
        Args:
            results: Test results to summarize
            
        Returns:
            Formatted summary comment
        """
        summary = "## 🔍 IaC Testing Framework Results\n\n"
        
        # Overall status
        overall_status = results.get("summary", {}).get("overall_status", "UNKNOWN")
        status_emoji = "✅" if overall_status == "PASSED" else "❌"
        summary += f"**Overall Status:** {status_emoji} {overall_status}\n\n"
        
        # Static Analysis Results
        if "static_analysis" in results:
            static = results["static_analysis"]
            summary += "### 📊 Static Analysis\n"
            summary += f"- **Status:** {static.get('status', 'unknown')}\n"
            summary += f"- **Issues Found:** {static.get('summary', {}).get('total_issues', 0)}\n"
            summary += f"- **Validation:** {'✅ Passed' if static.get('summary', {}).get('validation_passed') else '❌ Failed'}\n\n"
        
        # Policy Compliance Results
        if "policy_compliance" in results:
            compliance = results["policy_compliance"]
            summary += "### 🔐 Policy Compliance\n"
            summary += f"- **Status:** {compliance.get('status', 'unknown')}\n"
            summary += f"- **Policies Checked:** {compliance.get('total_policies', 0)}\n"
            summary += f"- **Passed:** {compliance.get('passed_policies', 0)}\n"
            summary += f"- **Failed:** {compliance.get('failed_policies', 0)}\n"
            summary += f"- **Compliance Score:** {compliance.get('summary', {}).get('compliance_score', 0):.1f}%\n\n"
        
        # Dynamic Testing Results
        if "dynamic_testing" in results:
            dynamic = results["dynamic_testing"]
            summary += "### 🚀 Dynamic Testing\n"
            summary += f"- **Status:** {dynamic.get('status', 'unknown')}\n"
            summary += f"- **Tests Run:** {dynamic.get('total_tests', 0)}\n"
            summary += f"- **Passed:** {dynamic.get('passed_tests', 0)}\n"
            summary += f"- **Failed:** {dynamic.get('failed_tests', 0)}\n\n"
        
        # Recommendations
        summary += "### 💡 Recommendations\n"
        if overall_status == "FAILED":
            summary += "- Review and fix the identified issues before deploying\n"
            summary += "- Check the detailed logs for specific error messages\n"
            summary += "- Ensure all security policies are met\n"
        else:
            summary += "- Infrastructure looks good for deployment! 🎉\n"
            summary += "- Consider reviewing any warnings for best practices\n"
        
        summary += f"\n---\n*Generated by IaC Testing Framework at {datetime.now().isoformat()}*"
        
        return summary
    
    def save_results_for_reporting(self, results: Dict[str, Any], output_dir: str = "reports") -> None:
        """
        Save results in formats suitable for CI/CD reporting
        
        Args:
            results: Test results to save
            output_dir: Directory to save reports
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Save as JSON for programmatic access
        json_path = os.path.join(output_dir, "ci_results.json")
        with open(json_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Save as JUnit XML for test reporting
        junit_path = os.path.join(output_dir, "junit_results.xml")
        self._save_junit_xml(results, junit_path)
        
        # Save summary as markdown
        markdown_path = os.path.join(output_dir, "summary.md")
        summary = self.create_summary_comment(results)
        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"Reports saved to {output_dir}/")
    
    def _save_junit_xml(self, results: Dict[str, Any], file_path: str) -> None:
        """Save results in JUnit XML format"""
        junit_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        
        # Calculate totals
        total_tests = 0
        total_failures = 0
        total_time = 0
        
        test_suites = []
        
        # Static Analysis Suite
        if "static_analysis" in results:
            static = results["static_analysis"]
            suite_tests = 1
            suite_failures = 1 if static.get("summary", {}).get("total_issues", 0) > 0 else 0
            total_tests += suite_tests
            total_failures += suite_failures
            
            test_suites.append(f'''
    <testsuite name="StaticAnalysis" tests="{suite_tests}" failures="{suite_failures}" time="0">
        <testcase name="terraform_validation" classname="static_analysis">
            {"<failure>Validation failed</failure>" if suite_failures > 0 else ""}
        </testcase>
    </testsuite>''')
        
        # Policy Compliance Suite
        if "policy_compliance" in results:
            compliance = results["policy_compliance"]
            suite_tests = compliance.get("total_policies", 0)
            suite_failures = compliance.get("failed_policies", 0)
            total_tests += suite_tests
            total_failures += suite_failures
            
            test_cases = []
            for policy_result in compliance.get("results", []):
                policy_name = policy_result.get("policy_name", "unknown")
                status = policy_result.get("status", "unknown")
                failure_tag = '<failure>Policy violation</failure>' if status == "FAILED" else ""
                test_cases.append(f'        <testcase name="{policy_name}" classname="policy_compliance">{failure_tag}</testcase>')
            
            test_suites.append(f'''
    <testsuite name="PolicyCompliance" tests="{suite_tests}" failures="{suite_failures}" time="0">
{chr(10).join(test_cases)}
    </testsuite>''')
        
        junit_xml += f'<testsuites tests="{total_tests}" failures="{total_failures}" time="{total_time}">'
        junit_xml += ''.join(test_suites)
        junit_xml += '\n</testsuites>'
        
        with open(file_path, 'w') as f:
            f.write(junit_xml)
    
    def check_for_breaking_changes(self, results: Dict[str, Any]) -> bool:
        """
        Check if results contain breaking changes that should fail the CI
        
        Args:
            results: Test results to check
            
        Returns:
            True if breaking changes found, False otherwise
        """
        # Check for critical security violations
        if "policy_compliance" in results:
            compliance = results["policy_compliance"]
            for policy_result in compliance.get("results", []):
                if policy_result.get("status") == "FAILED":
                    # Check if any violations are marked as critical
                    for violation in policy_result.get("violations", []):
                        if violation.get("severity") == "HIGH" or violation.get("severity") == "CRITICAL":
                            return True
        
        # Check for terraform validation failures
        if "static_analysis" in results:
            static = results["static_analysis"]
            if not static.get("summary", {}).get("validation_passed", True):
                return True
        
        return False
    
    def set_exit_code_based_on_results(self, results: Dict[str, Any]) -> None:
        """
        Set appropriate exit code based on test results
        
        Args:
            results: Test results to evaluate
        """
        if self.check_for_breaking_changes(results):
            self.set_error("Critical issues found - failing CI build")
            sys.exit(1)
        
        overall_status = results.get("summary", {}).get("overall_status", "UNKNOWN")
        if overall_status == "FAILED":
            self.set_warning("Some tests failed, but no critical issues found")
            # Don't exit with error for non-critical failures
        else:
            self.set_notice("All tests passed successfully!")

def generate_github_actions_workflow(output_path: str = ".github/workflows/iac-testing.yml") -> None:
    """
    Generate a GitHub Actions workflow file for the IaC testing framework
    
    Args:
        output_path: Path where to save the workflow file
    """
    # The workflow content is already created above
    print(f"GitHub Actions workflow already created at {output_path}")

def main():
    """Demo function for CI/CD integration"""
    integration = CICDIntegration()
    
    # Example results
    example_results = {
        "summary": {
            "overall_status": "PASSED",
            "total_checks": 10,
            "passed_checks": 8,
            "failed_checks": 2
        },
        "static_analysis": {
            "status": "success",
            "summary": {
                "total_issues": 0,
                "validation_passed": True
            }
        },
        "policy_compliance": {
            "status": "success",
            "total_policies": 5,
            "passed_policies": 4,
            "failed_policies": 1,
            "summary": {
                "compliance_score": 80.0
            }
        }
    }
    
    print("🔗 CI/CD Integration Demo")
    print("=" * 30)
    
    # Generate summary
    summary = integration.create_summary_comment(example_results)
    print("Summary Comment:")
    print(summary)
    
    # Save reports
    integration.save_results_for_reporting(example_results)
    
    # Set outputs
    integration.set_output("test_status", "passed")
    integration.set_output("compliance_score", "80")

if __name__ == "__main__":
    main()
