#!/usr/bin/env python3
"""
Comprehensive Test Runner for IaC Testing Framework
Integrates all phases: Static Analysis, Policy Compliance, Dynamic Testing, CI/CD, and Evaluation
"""

import argparse
import sys
import json
import os
from pathlib import Path
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from static_analysis.static_checker import StaticChecker
from policy_compliance.compliance_checker import ComplianceChecker
from dynamic_provisioning.dynamic_tester import DynamicTester
from ci_cd.ci_integration import CICDIntegration
from evaluation.evaluator import FrameworkEvaluator

class ComprehensiveTestRunner:
    """
    Main test runner that orchestrates all framework components
    """
    
    def __init__(self):
        """Initialize the test runner"""
        self.static_checker = StaticChecker()
        self.compliance_checker = None
        self.dynamic_tester = DynamicTester()
        self.ci_integration = CICDIntegration()
        self.evaluator = FrameworkEvaluator()
        
    def run_static_analysis(self, terraform_dir: str, output_file: str = None) -> dict:
        """Run static analysis on Terraform files"""
        print("🔍 Running Static Analysis...")
        
        start_time = datetime.now()
        results = self.static_checker.analyze_terraform_files(terraform_dir)
        end_time = datetime.now()
        
        # Add execution time to results
        execution_time = (end_time - start_time).total_seconds()
        results["execution_time"] = execution_time
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"✅ Static analysis results saved to: {output_file}")
        
        return results
    
    def run_policy_compliance(self, terraform_dir: str, policies_dir: str = None, output_file: str = None) -> dict:
        """Run policy compliance checking"""
        print("🔐 Running Policy Compliance Checks...")
        
        start_time = datetime.now()
        
        if not policies_dir:
            policies_dir = str(Path(__file__).parent / "policy_compliance" / "policies")
        
        if not self.compliance_checker:
            self.compliance_checker = ComplianceChecker(policies_dir)
        
        results = self.compliance_checker.check_compliance(terraform_dir)
        
        end_time = datetime.now()
        
        # Add execution time and directory info to results
        execution_time = (end_time - start_time).total_seconds()
        results["execution_time"] = execution_time
        results["terraform_directory"] = terraform_dir
        results["analysis_timestamp"] = start_time.isoformat()
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"✅ Policy compliance results saved to: {output_file}")
        
        return results
    
    def run_dynamic_testing(self, terraform_dir: str, test_environment: str = "localstack", output_file: str = None) -> dict:
        """Run dynamic provisioning and runtime tests"""
        print("🚀 Running Dynamic Testing...")
        
        start_time = datetime.now()
        
        # Initialize dynamic tester with specified environment
        if test_environment != self.dynamic_tester.test_environment:
            self.dynamic_tester = DynamicTester(test_environment=test_environment)
        
        # Deploy infrastructure
        deployment_result = self.dynamic_tester.deploy_infrastructure(terraform_dir)
        
        # Run runtime tests if deployment succeeded
        if deployment_result["status"] == "success":
            runtime_results = self.dynamic_tester.run_runtime_tests(terraform_dir)
            
            # Cleanup infrastructure - COMMENTED OUT TO KEEP AWS RESOURCES
           # cleanup_result = self.dynamic_tester.cleanup_deployment(terraform_dir)
            cleanup_result = {"status": "skipped", "message": "Cleanup disabled to preserve AWS resources"}
            
            results = {
                "deployment": deployment_result,
                "runtime_tests": runtime_results,
                "cleanup": cleanup_result,
                "summary": {
                    "overall_status": runtime_results.get("summary", {}).get("overall_status", "UNKNOWN"),
                    "tests_passed": runtime_results.get("passed_tests", 0),
                    "tests_failed": runtime_results.get("failed_tests", 0),
                    "total_tests": runtime_results.get("total_tests", 0)
                }
            }
        else:
            results = {
                "deployment": deployment_result,
                "runtime_tests": {"status": "skipped", "message": "Deployment failed"},
                "cleanup": {"status": "skipped"},
                "summary": {"overall_status": "FAILED"}
            }
        
        end_time = datetime.now()
        
        # Add execution time and directory info to results
        execution_time = (end_time - start_time).total_seconds()
        results["execution_time"] = execution_time
        results["terraform_directory"] = terraform_dir
        results["analysis_timestamp"] = start_time.isoformat()
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"✅ Dynamic testing results saved to: {output_file}")
        
        return results
    
    def run_comprehensive_analysis(self, terraform_dir: str, policies_dir: str = None, 
                                 include_dynamic: bool = False, test_environment: str = "localstack",
                                 output_file: str = None) -> dict:
        """Run complete analysis including all components"""
        print("🎯 Running Comprehensive Analysis...")
        
        start_time = datetime.now()
        
        # Run static analysis
        static_results = self.run_static_analysis(terraform_dir)
        
        # Run policy compliance
        compliance_results = self.run_policy_compliance(terraform_dir, policies_dir)
        
        # Run dynamic testing if requested
        dynamic_results = None
        if include_dynamic:
            dynamic_results = self.run_dynamic_testing(terraform_dir, test_environment)
        
        # Combine results
        combined_results = {
            "analysis_timestamp": start_time.isoformat(),
            "terraform_directory": terraform_dir,
            "analysis_type": "comprehensive" if include_dynamic else "static_and_compliance",
            "execution_time": (datetime.now() - start_time).total_seconds(),
            "static_analysis": static_results,
            "policy_compliance": compliance_results,
            "summary": self._calculate_overall_summary(static_results, compliance_results, dynamic_results)
        }
        
        if dynamic_results:
            combined_results["dynamic_testing"] = dynamic_results
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(combined_results, f, indent=2)
            print(f"✅ Comprehensive results saved to: {output_file}")
        
        return combined_results
    
    def run_evaluation(self, output_dir: str = "evaluation_results") -> dict:
        """Run framework evaluation and generate reports"""
        print("📊 Running Framework Evaluation...")
        
        evaluation_results = self.evaluator.generate_evaluation_report()
        
        print(f"✅ Evaluation completed. Results in: {output_dir}")
        return evaluation_results
    
    def run_ci_integration(self, results: dict, ci_environment: str = "github_actions") -> None:
        """Process results for CI/CD integration"""
        print(f"🔗 Processing results for {ci_environment}...")
        
        # Initialize CI integration
        ci_integration = CICDIntegration(ci_environment=ci_environment)
        
        # Generate CI-friendly reports
        ci_integration.save_results_for_reporting(results)
        
        # Set CI outputs
        overall_status = results.get("summary", {}).get("overall_status", "UNKNOWN")
        ci_integration.set_output("test_status", overall_status.lower())
        
        if "policy_compliance" in results:
            compliance_score = results["policy_compliance"].get("summary", {}).get("compliance_score", 0)
            ci_integration.set_output("compliance_score", str(int(compliance_score)))
        
        # Check for breaking changes and set exit code
        ci_integration.set_exit_code_based_on_results(results)
    
    def _calculate_overall_summary(self, static_results: dict, compliance_results: dict, dynamic_results: dict = None) -> dict:
        """Calculate overall summary across all analysis types"""
        
        # Count total checks
        static_issues = static_results.get("summary", {}).get("total_issues", 0)
        total_policies = compliance_results.get("total_policies", 0)
        failed_policies = compliance_results.get("failed_policies", 0)
        
        total_checks = total_policies
        if static_issues > 0:
            total_checks += 1  # Count static analysis as one check
        
        passed_checks = compliance_results.get("passed_policies", 0)
        if static_issues == 0:
            passed_checks += 1
        
        failed_checks = failed_policies
        if static_issues > 0:
            failed_checks += 1
        
        # Include dynamic testing if available
        if dynamic_results:
            dynamic_tests = dynamic_results.get("summary", {}).get("total_tests", 0)
            dynamic_passed = dynamic_results.get("summary", {}).get("tests_passed", 0)
            dynamic_failed = dynamic_results.get("summary", {}).get("tests_failed", 0)
            
            total_checks += dynamic_tests
            passed_checks += dynamic_passed
            failed_checks += dynamic_failed
        
        # Determine overall status
        if failed_checks == 0:
            overall_status = "PASSED"
        elif static_results.get("summary", {}).get("validation_passed", True) == False:
            overall_status = "CRITICAL_FAILURE"  # Terraform validation failed
        else:
            overall_status = "NEEDS_ATTENTION"
        
        return {
            "total_checks": total_checks,
            "passed_checks": passed_checks,
            "failed_checks": failed_checks,
            "success_rate": (passed_checks / total_checks * 100) if total_checks > 0 else 0,
            "overall_status": overall_status
        }
    
    def print_summary(self, results: dict) -> None:
        """Print a formatted summary of results"""
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE ANALYSIS SUMMARY")
        print("=" * 80)
        
        # Basic info - handle both nested and direct results
        if 'static_analysis' in results:
            # For static-only calls, extract info from nested structure
            static_data = results['static_analysis']
            terraform_dir = static_data.get('terraform_directory', 'N/A')
            timestamp = static_data.get('analysis_timestamp', 'N/A')
            execution_time = static_data.get('execution_time', 0)
            analysis_type = 'static_analysis'
        elif 'policy_compliance' in results:
            # For policy-only calls, extract info from nested structure
            policy_data = results['policy_compliance']
            terraform_dir = policy_data.get('terraform_directory', 'N/A')
            timestamp = policy_data.get('analysis_timestamp', 'N/A')
            execution_time = policy_data.get('execution_time', 0)
            analysis_type = 'policy_compliance'
        elif 'dynamic_testing' in results:
            # For dynamic-only calls, extract info from nested structure
            dynamic_data = results['dynamic_testing']
            terraform_dir = dynamic_data.get('terraform_directory', 'N/A')
            timestamp = dynamic_data.get('analysis_timestamp', 'N/A')
            execution_time = dynamic_data.get('execution_time', 0)
            analysis_type = 'dynamic_testing'
        else:
            # For comprehensive calls
            terraform_dir = results.get('terraform_directory', 'N/A')
            timestamp = results.get('analysis_timestamp', 'N/A')
            execution_time = results.get('execution_time', 0)
            analysis_type = results.get('analysis_type', 'N/A')
        
        print(f"📁 Directory: {terraform_dir}")
        print(f"🕐 Timestamp: {timestamp}")
        print(f"⏱️  Execution Time: {execution_time:.1f}s")
        print(f"📄 Analysis Type: {analysis_type}")
        
        # Static Analysis
        if 'static_analysis' in results:
            static = results['static_analysis']
            print(f"\n🔍 Static Analysis:")
            print(f"   - Status: {static.get('status', 'unknown')}")
            print(f"   - Files Analyzed: {static.get('terraform_files_found', 0)}")
            
            # Calculate total issues from actual results
            total_issues = 0
            if 'results' in static and 'checkov' in static['results']:
                checkov = static['results']['checkov']
                if checkov.get('status') == 'success':
                    # The failed_checks count is directly in checkov object
                    total_issues = checkov.get('failed_checks', 0)
            
            print(f"   - Total Issues: {total_issues}")
            print(f"   - Validation: {'✅ PASSED' if static.get('summary', {}).get('validation_passed') else '❌ FAILED'}")
            
            # Show detailed breakdown
            if 'results' in static:
                tools_results = static['results']
                total_issues = 0
                failed_count = 0
                passed_count = 0
                
                if 'checkov' in tools_results:
                    checkov = tools_results['checkov']
                    if checkov.get('status') == 'success':
                        # The counts are directly in checkov object
                        failed_count = checkov.get('failed_checks', 0)
                        passed_count = checkov.get('passed_checks', 0)
                        total_issues += failed_count
                        
                        print(f"   - Security Issues: {failed_count} failed, {passed_count} passed")
                        
                        # Show detailed breakdown of issues
                        if 'results' in checkov and failed_count > 0:
                            self._print_detailed_issues(checkov['results'], static.get('terraform_directory', 'static_analysis/examples'))
                    else:
                        print(f"   - Security Issues: Checkov failed to run")
                        
                if 'tflint' in tools_results:
                    tflint = tools_results['tflint']
                    print(f"   - Linting Issues: {tflint.get('total_issues', 0)}")
                    
                if 'terraform_validate' in tools_results:
                    validate = tools_results['terraform_validate']
                    print(f"   - Validation: {'✅ PASSED' if validate.get('valid', False) else '❌ FAILED'}")
                
                # Update the total issues display
                print(f"   - Total Issues: {total_issues}")
            else:
                print(f"   - Total Issues: 0")
        
        # Policy Compliance
        if 'policy_compliance' in results:
            compliance = results['policy_compliance']
            print(f"\n🔐 Policy Compliance:")
            print(f"   - Status: {compliance.get('status', 'unknown')}")
            print(f"   - Total Policies: {compliance.get('total_policies', 0)}")
            print(f"   - Passed: {compliance.get('passed_policies', 0)}")
            print(f"   - Failed: {compliance.get('failed_policies', 0)}")
            print(f"   - Compliance Score: {compliance.get('summary', {}).get('compliance_score', 0):.1f}%")
            
            # Show detailed breakdown of policy results if available
            if compliance.get('failed_policies', 0) > 0 and 'results' in compliance:
                self._print_detailed_policy_results(compliance['results'], 
                                                   compliance.get('terraform_directory', 'N/A'))
        
        # Dynamic Testing
        if 'dynamic_testing' in results:
            dynamic = results['dynamic_testing']
            print(f"\n🚀 Dynamic Testing:")
            print(f"   - Deployment: {dynamic.get('deployment', {}).get('status', 'unknown')}")
            print(f"   - Runtime Tests: {dynamic.get('summary', {}).get('tests_passed', 0)}/{dynamic.get('summary', {}).get('total_tests', 0)} passed")
            print(f"   - Overall Status: {dynamic.get('summary', {}).get('overall_status', 'UNKNOWN')}")
            
            # Show detailed deployment info if failed
            deployment = dynamic.get('deployment', {})
            if deployment.get('status') == 'failed':
                errors = deployment.get('errors', [])
                if errors:
                    # Clean up the first error message for console display
                    error_msg = errors[0]
                    # Remove ANSI color codes for cleaner display
                    import re
                    clean_error = re.sub(r'\x1b\[[0-9;]*m', '', error_msg)
                    # Extract just the core error message
                    if 'Error:' in clean_error:
                        clean_error = clean_error.split('Error:')[1].split('\n')[0].strip()
                    print(f"   - Deployment Error: {clean_error[:100]}{'...' if len(clean_error) > 100 else ''}")
                else:
                    print(f"   - Deployment Error: Unknown deployment error")
                
                # Save detailed error to file
                self._print_detailed_dynamic_results(dynamic, dynamic.get('terraform_directory', 'N/A'))
            else:
                # Save detailed report for successful deployments too
                self._print_detailed_dynamic_results(dynamic, dynamic.get('terraform_directory', 'N/A'))
        
        # Overall Summary
        if 'summary' in results:
            summary = results['summary']
            print(f"\n📈 Overall Summary:")
            print(f"   - Total Checks: {summary.get('total_checks', 0)}")
            print(f"   - Passed: {summary.get('passed_checks', 0)}")
            print(f"   - Failed: {summary.get('failed_checks', 0)}")
            print(f"   - Success Rate: {summary.get('success_rate', 0):.1f}%")
            
            status = summary.get('overall_status', 'UNKNOWN')
            status_emoji = {
                'PASSED': '✅',
                'NEEDS_ATTENTION': '⚠️',
                'CRITICAL_FAILURE': '❌',
                'UNKNOWN': '❓'
            }.get(status, '❓')
            
            print(f"   - Status: {status_emoji} {status}")
        
        print("=" * 80)

    def _print_detailed_issues(self, checkov_results, terraform_dir=""):
        """Print detailed breakdown of failed and passed checks"""
        
        # Create detailed report file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        detailed_file = f"detailed_security_report_{timestamp}.txt"
        
        with open(detailed_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("🔍 DETAILED SECURITY ANALYSIS REPORT\n")
            f.write("=" * 80 + "\n")
            f.write(f"📁 Directory: {terraform_dir}\n")
            f.write(f"🕐 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            # Print failed checks (show only 2 in console, all in file)
            if 'failed' in checkov_results and checkov_results['failed']:
                total_failed = len(checkov_results['failed'])
                print(f"\n   ❌ FAILED CHECKS ({total_failed}):")
                
                # Console output - show only first 2
                for i, issue in enumerate(checkov_results['failed'][:2], 1):
                    check_id = issue.get('check_id', 'Unknown')
                    check_name = issue.get('check_name', 'Unknown check')
                    print(f"      {check_id}: {check_name}")
                
                if total_failed > 2:
                    print(f"      ... and {total_failed - 2} more failed checks")
                
                # File output - show all failed checks
                f.write(f"❌ FAILED CHECKS ({total_failed}):\n")
                f.write("=" * 50 + "\n")
                for i, issue in enumerate(checkov_results['failed'], 1):
                    check_id = issue.get('check_id', 'Unknown')
                    check_name = issue.get('check_name', 'Unknown check')
                    resource = issue.get('resource', 'Unknown resource')
                    file_path = issue.get('file_path', 'Unknown file')
                    
                    f.write(f"{i:2d}. {check_id}: {check_name}\n")
                    f.write(f"    Resource: {resource}\n")
                    f.write(f"    File: {file_path}\n")
                    
                    # Add description if available
                    if 'description' in issue:
                        f.write(f"    Description: {issue['description']}\n")
                    
                    f.write("\n")
        
            # Print sample of passed checks (show only 2 in console, all in file)
            if 'passed' in checkov_results and checkov_results['passed']:
                total_passed = len(checkov_results['passed'])
                print(f"\n   ✅ PASSED CHECKS ({total_passed}):")
                
                # Console output - show only first 2
                for i, check in enumerate(checkov_results['passed'][:2], 1):
                    check_id = check.get('check_id', 'Unknown')
                    check_name = check.get('check_name', 'Unknown check')
                    print(f"      {check_id}: {check_name}")
                
                if total_passed > 2:
                    print(f"      ... and {total_passed - 2} more passed checks")
                
                # File output - show all passed checks
                f.write(f"\n✅ PASSED CHECKS ({total_passed}):\n")
                f.write("=" * 50 + "\n")
                for i, check in enumerate(checkov_results['passed'], 1):
                    check_id = check.get('check_id', 'Unknown')
                    check_name = check.get('check_name', 'Unknown check')
                    resource = check.get('resource', 'Unknown resource')
                    
                    f.write(f"{i:2d}. {check_id}: {check_name}\n")
                    f.write(f"    Resource: {resource}\n")
                    
                    # Add description if available
                    if 'description' in check:
                        f.write(f"    Description: {check['description']}\n")
                    
                    f.write("\n")
        
        print(f"\n   📄 Full detailed report saved to: {detailed_file}")

    def _print_detailed_policy_results(self, policy_results_list, terraform_dir=""):
        """Print detailed breakdown of policy compliance results"""
        
        # Create detailed policy report file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        detailed_file = f"detailed_policy_report_{timestamp}.txt"
        
        failed_policies = []
        passed_policies = []
        
        # Categorize policy results from list
        for policy_result in policy_results_list:
            policy_name = policy_result.get('policy_name', 'Unknown Policy')
            if policy_result.get('status') == 'FAILED':
                failed_policies.append((policy_name, policy_result))
            else:
                passed_policies.append((policy_name, policy_result))
        
        with open(detailed_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("🔐 DETAILED POLICY COMPLIANCE REPORT\n")
            f.write("=" * 80 + "\n")
            f.write(f"📁 Directory: {terraform_dir}\n")
            f.write(f"🕐 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            # Print failed policies (show only 2 in console, all in file)
            if failed_policies:
                total_failed = len(failed_policies)
                print(f"\n   ❌ FAILED POLICIES ({total_failed}):")
                
                # Console output - show only first 2
                for i, (policy_name, policy_result) in enumerate(failed_policies[:2], 1):
                    description = policy_result.get('description', 'No description available')
                    violation_count = policy_result.get('violation_count', 0)
                    print(f"      {policy_name}: {description[:50]}{'...' if len(description) > 50 else ''} ({violation_count} violations)")
                
                if total_failed > 2:
                    print(f"      ... and {total_failed - 2} more failed policies")
                
                # File output - show all failed policies
                f.write(f"❌ FAILED POLICIES ({total_failed}):\n")
                f.write("=" * 50 + "\n")
                for i, (policy_name, policy_result) in enumerate(failed_policies, 1):
                    description = policy_result.get('description', 'No description available')
                    violations = policy_result.get('violations', [])
                    violation_count = policy_result.get('violation_count', 0)
                    applicable_resources = policy_result.get('applicable_resources', 0)
                    
                    f.write(f"{i:2d}. {policy_name}\n")
                    f.write(f"    Description: {description}\n")
                    f.write(f"    Applicable Resources: {applicable_resources}\n")
                    f.write(f"    Violations: {violation_count}\n")
                    
                    if violations:
                        f.write(f"    Violation Details:\n")
                        for j, violation in enumerate(violations[:5], 1):  # Show first 5 violations
                            resource = violation.get('resource', 'Unknown')
                            rule = violation.get('rule', 'Unknown rule')
                            severity = violation.get('severity', 'UNKNOWN')
                            f.write(f"      {j}. Resource: {resource}\n")
                            f.write(f"         Rule: {rule}\n")
                            f.write(f"         Severity: {severity}\n")
                        if len(violations) > 5:
                            f.write(f"      ... and {len(violations) - 5} more violations\n")
                    
                    f.write("\n")
        
            # Print passed policies (show only 2 in console, all in file)
            if passed_policies:
                total_passed = len(passed_policies)
                print(f"\n   ✅ PASSED POLICIES ({total_passed}):")
                
                # Console output - show only first 2
                for i, (policy_name, policy_result) in enumerate(passed_policies[:2], 1):
                    description = policy_result.get('description', 'No description available')
                    applicable_resources = policy_result.get('applicable_resources', 0)
                    print(f"      {policy_name}: {description[:50]}{'...' if len(description) > 50 else ''} ({applicable_resources} resources)")
                
                if total_passed > 2:
                    print(f"      ... and {total_passed - 2} more passed policies")
                
                # File output - show all passed policies
                f.write(f"\n✅ PASSED POLICIES ({total_passed}):\n")
                f.write("=" * 50 + "\n")
                for i, (policy_name, policy_result) in enumerate(passed_policies, 1):
                    description = policy_result.get('description', 'No description available')
                    applicable_resources = policy_result.get('applicable_resources', 0)
                    
                    f.write(f"{i:2d}. {policy_name}\n")
                    f.write(f"    Description: {description}\n")
                    f.write(f"    Applicable Resources: {applicable_resources}\n")
                    f.write("\n")
        
        print(f"\n   📄 Full detailed policy report saved to: {detailed_file}")

    def _print_detailed_dynamic_results(self, dynamic_results, terraform_dir=""):
        """Print detailed breakdown of dynamic testing results"""
        
        # Create detailed dynamic report file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        detailed_file = f"detailed_dynamic_report_{timestamp}.txt"
        
        # Get test results for console display
        runtime_tests = dynamic_results.get('runtime_tests', {})
        deployment = dynamic_results.get('deployment', {})
        
        # Console output with rich details (similar to static analysis)
        print(f"\n📊 DYNAMIC TESTING BREAKDOWN:")
        print("=" * 60)
        
        # Deployment Summary
        deployment_status = deployment.get('status', 'unknown')
        deployment_time = deployment.get('deployment_time', 0)
        environment = deployment.get('environment', 'unknown')
        
        print(f"🏗️  DEPLOYMENT PHASE:")
        print(f"   Status: {'✅ SUCCESS' if deployment_status == 'success' else '❌ FAILED'}")
        print(f"   Environment: {environment.upper()}")
        print(f"   Duration: {deployment_time:.1f} seconds")
        
        if deployment_status == 'failed':
            errors = deployment.get('errors', [])
            if errors:
                print(f"   Errors: {len(errors)} deployment issues found")
                # Show first 2 errors in console
                for i, error in enumerate(errors[:2], 1):
                    import re
                    clean_error = re.sub(r'\x1b\[[0-9;]*m', '', error)
                    # Get first line of error for console
                    error_line = clean_error.split('\n')[0][:80] + "..."
                    print(f"      Error {i}: {error_line}")
                if len(errors) > 2:
                    print(f"      ... and {len(errors) - 2} more errors")
        
        # Runtime Tests Summary
        if runtime_tests.get('status') != 'skipped':
            print(f"\n🧪 RUNTIME TESTING PHASE:")
            
            test_results = runtime_tests.get('test_results', {})
            if isinstance(test_results, dict):
                passed_tests = []
                failed_tests = []
                
                for test_name, test_result in test_results.items():
                    if isinstance(test_result, dict):
                        if test_result.get('status') == 'passed':
                            passed_tests.append((test_name, test_result))
                        else:
                            failed_tests.append((test_name, test_result))
                
                # Show passed tests summary
                if passed_tests:
                    print(f"   ✅ PASSED TESTS ({len(passed_tests)}):")
                    for i, (test_name, test_result) in enumerate(passed_tests[:3], 1):
                        duration = test_result.get('duration', 'unknown')
                        print(f"      {test_name} ({duration})")
                    if len(passed_tests) > 3:
                        print(f"      ... and {len(passed_tests) - 3} more passed tests")
                
                # Show failed tests summary  
                if failed_tests:
                    print(f"   ❌ FAILED TESTS ({len(failed_tests)}):")
                    for i, (test_name, test_result) in enumerate(failed_tests[:3], 1):
                        error = test_result.get('error', 'No error details')
                        error_summary = error.split('\n')[0][:60] + "..."
                        print(f"      {test_name}: {error_summary}")
                    if len(failed_tests) > 3:
                        print(f"      ... and {len(failed_tests) - 3} more failed tests")
            
            # Overall test statistics
            total_tests = runtime_tests.get('total_tests', 0)
            passed_count = runtime_tests.get('passed_tests', 0)
            failed_count = runtime_tests.get('failed_tests', 0)
            
            if total_tests > 0:
                success_rate = (passed_count / total_tests) * 100
                print(f"\n   📈 TEST STATISTICS:")
                print(f"      Total Tests: {total_tests}")
                print(f"      Passed: {passed_count}")
                print(f"      Failed: {failed_count}")
                print(f"      Success Rate: {success_rate:.1f}%")
        
        # Infrastructure Summary
        resources_deployed = deployment.get('resources_deployed', [])
        if resources_deployed:
            print(f"\n🏗️  INFRASTRUCTURE DEPLOYED:")
            for i, resource in enumerate(resources_deployed[:5], 1):
                print(f"      {i}. {resource}")
            if len(resources_deployed) > 5:
                print(f"      ... and {len(resources_deployed) - 5} more resources")
        
        # Cleanup Status
        cleanup = dynamic_results.get('cleanup', {})
        cleanup_status = cleanup.get('status', 'unknown')
        print(f"\n🧹 CLEANUP PHASE:")
        if cleanup_status == 'skipped':
            print(f"   Status: ⏸️  SKIPPED (Resources preserved for demonstration)")
        elif cleanup_status == 'success':
            print(f"   Status: ✅ COMPLETED (All resources cleaned up)")
        else:
            print(f"   Status: ❌ FAILED (Manual cleanup may be required)")
        
        # File output with complete details
        with open(detailed_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("🚀 DETAILED DYNAMIC TESTING REPORT\n")
            f.write("=" * 80 + "\n")
            f.write(f"📁 Directory: {terraform_dir}\n")
            f.write(f"🕐 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            # Deployment details
            f.write("🏗️ DEPLOYMENT DETAILS:\n")
            f.write("=" * 40 + "\n")
            f.write(f"Status: {deployment.get('status', 'unknown')}\n")
            f.write(f"Environment: {deployment.get('environment', 'unknown')}\n")
            f.write(f"Start Time: {deployment.get('deployment_timestamp', 'unknown')}\n")
            f.write(f"Duration: {deployment.get('deployment_time', 0)} seconds\n")
            
            # Add Terraform output details
            terraform_output = deployment.get('terraform_output', '')
            if terraform_output:
                f.write(f"\nTerraform Output:\n{terraform_output}\n")
            
            # Add deployed resources
            if resources_deployed:
                f.write(f"\nDeployed Resources ({len(resources_deployed)}):\n")
                for i, resource in enumerate(resources_deployed, 1):
                    f.write(f"{i:2d}. {resource}\n")
            
            if deployment.get('status') == 'failed':
                errors = deployment.get('errors', [])
                if errors:
                    f.write(f"\nDEPLOYMENT ERRORS ({len(errors)} errors):\n")
                    f.write("=" * 40 + "\n")
                    for i, error in enumerate(errors, 1):
                        # Clean ANSI codes for file output
                        import re
                        clean_error = re.sub(r'\x1b\[[0-9;]*m', '', error)
                        f.write(f"\nError {i}:\n{clean_error}\n")
                        f.write("-" * 40 + "\n")
                else:
                    f.write(f"\nError Details:\nNo specific error details available\n")
            
            # Runtime tests details
            if runtime_tests.get('status') != 'skipped':
                f.write(f"\n🧪 RUNTIME TESTS DETAILED RESULTS:\n")
                f.write("=" * 40 + "\n")
                f.write(f"Overall Status: {runtime_tests.get('status', 'unknown')}\n")
                f.write(f"Total Tests: {runtime_tests.get('total_tests', 0)}\n")
                f.write(f"Passed: {runtime_tests.get('passed_tests', 0)}\n")
                f.write(f"Failed: {runtime_tests.get('failed_tests', 0)}\n")
                
                if total_tests > 0:
                    success_rate = (runtime_tests.get('passed_tests', 0) / total_tests) * 100
                    f.write(f"Success Rate: {success_rate:.1f}%\n")
                
                f.write(f"\nINDIVIDUAL TEST RESULTS:\n")
                f.write("-" * 40 + "\n")
                
                if 'test_results' in runtime_tests:
                    test_results = runtime_tests['test_results']
                    if isinstance(test_results, list):
                        for i, test_result in enumerate(test_results, 1):
                            test_name = test_result.get('test_name', f'Test {i}')
                            f.write(f"\n{i:2d}. Test: {test_name}\n")
                            f.write(f"    Status: {test_result.get('status', 'unknown')}\n")
                            f.write(f"    Duration: {test_result.get('duration', 'unknown')}\n")
                            if 'error' in test_result:
                                f.write(f"    Error: {test_result['error']}\n")
                            if 'details' in test_result:
                                f.write(f"    Details: {test_result['details']}\n")
                    else:
                        # Handle as dictionary (legacy support)
                        for i, (test_name, test_result) in enumerate(test_results.items(), 1):
                            f.write(f"\n{i:2d}. Test: {test_name}\n")
                            if isinstance(test_result, dict):
                                f.write(f"    Status: {test_result.get('status', 'unknown')}\n")
                                f.write(f"    Duration: {test_result.get('duration', 'unknown')}\n")
                                if 'error' in test_result:
                                    f.write(f"    Error: {test_result['error']}\n")
                                if 'details' in test_result:
                                    f.write(f"    Details: {test_result['details']}\n")
                            else:
                                f.write(f"    Result: {test_result}\n")
            
            # Cleanup details
            f.write(f"\n🧹 CLEANUP DETAILS:\n")
            f.write("=" * 40 + "\n")
            f.write(f"Status: {cleanup.get('status', 'unknown')}\n")
            if 'message' in cleanup:
                f.write(f"Message: {cleanup['message']}\n")
            if 'cleanup_time' in cleanup:
                f.write(f"Duration: {cleanup['cleanup_time']} seconds\n")
            
            # Add AWS resource summary if available
            aws_resources = runtime_tests.get('aws_resources_found', {})
            if aws_resources:
                f.write(f"\n☁️  AWS RESOURCES DISCOVERED:\n")
                f.write("=" * 40 + "\n")
                for resource_type, resources in aws_resources.items():
                    f.write(f"\n{resource_type.upper()}:\n")
                    if isinstance(resources, list):
                        for resource in resources:
                            f.write(f"  - {resource}\n")
                    else:
                        f.write(f"  - {resources}\n")
        
        print(f"\n   📄 Full detailed dynamic report saved to: {detailed_file}")

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description="IaC Testing Framework - Comprehensive Test Runner")
    
    # Add subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Static analysis command
    static_parser = subparsers.add_parser('static', help='Run static analysis only')
    static_parser.add_argument('terraform_dir', help='Directory containing Terraform files')
    static_parser.add_argument('--output', '-o', help='Output file for results')
    
    # Policy compliance command
    policy_parser = subparsers.add_parser('policy', help='Run policy compliance checks only')
    policy_parser.add_argument('terraform_dir', help='Directory containing Terraform files')
    policy_parser.add_argument('--policies', '-p', help='Directory containing policy files')
    policy_parser.add_argument('--output', '-o', help='Output file for results')
    
    # Dynamic testing command
    dynamic_parser = subparsers.add_parser('dynamic', help='Run dynamic testing only')
    dynamic_parser.add_argument('terraform_dir', help='Directory containing Terraform files')
    dynamic_parser.add_argument('--environment', '-e', choices=['localstack', 'aws'], 
                               default='localstack', help='Test environment')
    dynamic_parser.add_argument('--output', '-o', help='Output file for results')
    
    # Comprehensive analysis command
    comprehensive_parser = subparsers.add_parser('comprehensive', help='Run complete analysis')
    comprehensive_parser.add_argument('terraform_dir', help='Directory containing Terraform files')
    comprehensive_parser.add_argument('--policies', '-p', help='Directory containing policy files')
    comprehensive_parser.add_argument('--include-dynamic', action='store_true', 
                                    help='Include dynamic testing')
    comprehensive_parser.add_argument('--environment', '-e', choices=['localstack', 'aws'],
                                    default='localstack', help='Test environment for dynamic testing')
    comprehensive_parser.add_argument('--output', '-o', help='Output file for results')
    comprehensive_parser.add_argument('--ci', choices=['github_actions', 'jenkins', 'gitlab_ci'],
                                    help='Process results for CI/CD integration')
    
    # Evaluation command
    eval_parser = subparsers.add_parser('evaluate', help='Run framework evaluation')
    eval_parser.add_argument('--output-dir', default='evaluation_results',
                           help='Directory for evaluation results')
    
    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Run demonstration')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize test runner
    runner = ComprehensiveTestRunner()
    
    try:
        if args.command == 'static':
            results = runner.run_static_analysis(args.terraform_dir, args.output)
            runner.print_summary({"static_analysis": results})
            
        elif args.command == 'policy':
            results = runner.run_policy_compliance(args.terraform_dir, args.policies, args.output)
            runner.print_summary({"policy_compliance": results})
            
        elif args.command == 'dynamic':
            results = runner.run_dynamic_testing(args.terraform_dir, args.environment, args.output)
            runner.print_summary({"dynamic_testing": results})
            
        elif args.command == 'comprehensive':
            results = runner.run_comprehensive_analysis(
                args.terraform_dir, args.policies, args.include_dynamic, 
                args.environment, args.output
            )
            runner.print_summary(results)
            
            # CI/CD integration if requested
            if args.ci:
                runner.run_ci_integration(results, args.ci)
            
        elif args.command == 'evaluate':
            runner.run_evaluation(args.output_dir)
            
        elif args.command == 'demo':
            # Import and run demo
            from demo_phase2 import main as demo_main
            demo_main()
            
    except KeyboardInterrupt:
        print("\n⚠️ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
