#!/usr/bin/env python3
"""
Unit tests for IaC Testing Framework
"""

import unittest
import json
import tempfile
import os
from pathlib import Path
import sys

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from static_analysis.static_checker import StaticChecker
from policy_compliance.compliance_checker import ComplianceChecker

class TestStaticChecker(unittest.TestCase):
    """Test cases for Static Analysis module"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.checker = StaticChecker()
        self.test_dir = Path(__file__).parent / "static_analysis" / "examples"
    
    def test_initialization(self):
        """Test StaticChecker initialization"""
        self.assertIsInstance(self.checker, StaticChecker)
        self.assertEqual(self.checker.results, [])
    
    def test_analyze_terraform_files_existing_directory(self):
        """Test analyzing an existing directory with Terraform files"""
        if self.test_dir.exists():
            results = self.checker.analyze_terraform_files(str(self.test_dir))
            
            # Check basic structure
            self.assertIn('status', results)
            self.assertIn('terraform_directory', results)
            self.assertIn('terraform_files_found', results)
            self.assertIn('analysis_timestamp', results)
            self.assertIn('results', results)
            self.assertIn('summary', results)
            
            # Check results structure
            results_data = results['results']
            self.assertIn('terraform_validate', results_data)
            self.assertIn('tflint', results_data)
            self.assertIn('checkov', results_data)
    
    def test_analyze_terraform_files_nonexistent_directory(self):
        """Test analyzing a non-existent directory"""
        results = self.checker.analyze_terraform_files("/nonexistent/path")
        
        self.assertEqual(results['status'], 'error')
        self.assertIn('error_message', results)
        self.assertIn('does not exist', results['error_message'])
    
    def test_analyze_terraform_files_empty_directory(self):
        """Test analyzing an empty directory"""
        with tempfile.TemporaryDirectory() as temp_dir:
            results = self.checker.analyze_terraform_files(temp_dir)
            
            self.assertEqual(results['status'], 'error')
            self.assertIn('error_message', results)
            self.assertIn('No Terraform files found', results['error_message'])
    
    def test_get_results_summary_no_results(self):
        """Test getting summary when no results exist"""
        summary = self.checker.get_results_summary()
        
        self.assertIn('message', summary)
        self.assertEqual(summary['message'], 'No analysis results available')
    
    def test_get_results_summary_with_results(self):
        """Test getting summary after running analysis"""
        if self.test_dir.exists():
            # Run analysis first
            self.checker.analyze_terraform_files(str(self.test_dir))
            
            # Get summary
            summary = self.checker.get_results_summary()
            
            self.assertIn('total_analyses', summary)
            self.assertIn('latest_analysis', summary)
            self.assertGreater(summary['total_analyses'], 0)

class TestComplianceChecker(unittest.TestCase):
    """Test cases for Policy Compliance module"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.policies_dir = Path(__file__).parent / "policy_compliance" / "policies"
        self.checker = ComplianceChecker(str(self.policies_dir))
        self.test_dir = Path(__file__).parent / "static_analysis" / "examples"
    
    def test_initialization(self):
        """Test ComplianceChecker initialization"""
        self.assertIsInstance(self.checker, ComplianceChecker)
        self.assertEqual(self.checker.policies_dir, str(self.policies_dir))
    
    def test_load_policies(self):
        """Test loading policies from directory"""
        # Check if policies were loaded
        self.assertIsInstance(self.checker.policies, dict)
        
        # If policies directory exists, check policy structure
        if self.policies_dir.exists():
            for policy_name, policy_config in self.checker.policies.items():
                self.assertIsInstance(policy_name, str)
                self.assertIsInstance(policy_config, dict)
                self.assertIn('name', policy_config)
                self.assertIn('resource_types', policy_config)
                self.assertIn('rules', policy_config)
    
    def test_get_policies_summary(self):
        """Test getting policies summary"""
        summary = self.checker.get_policies_summary()
        
        self.assertIn('total_policies', summary)
        self.assertIn('policies', summary)
        self.assertIsInstance(summary['policies'], list)
        
        # Check policy summary structure
        for policy in summary['policies']:
            self.assertIn('name', policy)
            self.assertIn('description', policy)
            self.assertIn('resource_types', policy)
            self.assertIn('rules_count', policy)
    
    def test_check_compliance_existing_directory(self):
        """Test compliance checking on existing directory"""
        if self.test_dir.exists() and self.checker.policies:
            results = self.checker.check_compliance(str(self.test_dir))
            
            # Check basic structure
            self.assertIn('status', results)
            self.assertIn('terraform_directory', results)
            self.assertIn('total_policies', results)
            self.assertIn('passed_policies', results)
            self.assertIn('failed_policies', results)
            self.assertIn('results', results)
            self.assertIn('summary', results)
            
            # Check summary structure
            summary = results['summary']
            self.assertIn('compliance_score', summary)
            self.assertIn('overall_status', summary)
            self.assertIn(summary['overall_status'], ['PASSED', 'FAILED'])
    
    def test_check_compliance_no_policies(self):
        """Test compliance checking with no policies loaded"""
        empty_checker = ComplianceChecker("/nonexistent/policies")
        results = empty_checker.check_compliance(str(self.test_dir))
        
        self.assertEqual(results['status'], 'error')
        self.assertIn('No policies loaded', results['error_message'])
    
    def test_validate_resource_policies(self):
        """Test validating a single resource against policies"""
        if self.checker.policies:
            # Create a test resource configuration
            test_resource = {
                'type': 'aws_instance',
                'name': 'test_instance',
                'address': 'aws_instance.test_instance'
            }
            
            violations = self.checker.validate_resource_policies(test_resource)
            
            self.assertIsInstance(violations, list)
            # Each violation should be a string or dictionary
            for violation in violations:
                self.assertIsInstance(violation, (str, dict))

class TestIntegration(unittest.TestCase):
    """Integration tests for the complete framework"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = Path(__file__).parent / "static_analysis" / "examples"
        self.policies_dir = Path(__file__).parent / "policy_compliance" / "policies"
        self.static_checker = StaticChecker()
        self.compliance_checker = ComplianceChecker(str(self.policies_dir))
    
    def test_combined_analysis(self):
        """Test running both static analysis and policy compliance"""
        if self.test_dir.exists():
            # Run static analysis
            static_results = self.static_checker.analyze_terraform_files(str(self.test_dir))
            
            # Run policy compliance
            compliance_results = self.compliance_checker.check_compliance(str(self.test_dir))
            
            # Verify both have results
            self.assertIn('status', static_results)
            self.assertIn('status', compliance_results)
            
            # Create combined report
            combined_report = {
                "static_analysis": static_results,
                "policy_compliance": compliance_results,
                "summary": {
                    "total_checks": (
                        static_results.get('summary', {}).get('total_issues', 0) + 
                        compliance_results.get('total_policies', 0)
                    ),
                    "overall_status": "NEEDS_ATTENTION" if (
                        static_results.get('summary', {}).get('total_issues', 0) > 0 or
                        compliance_results.get('failed_policies', 0) > 0
                    ) else "PASSED"
                }
            }
            
            # Verify combined report structure
            self.assertIn('static_analysis', combined_report)
            self.assertIn('policy_compliance', combined_report)
            self.assertIn('summary', combined_report)
            self.assertIn('overall_status', combined_report['summary'])
    
    def test_report_generation(self):
        """Test generating JSON reports"""
        if self.test_dir.exists():
            # Run combined analysis
            static_results = self.static_checker.analyze_terraform_files(str(self.test_dir))
            compliance_results = self.compliance_checker.check_compliance(str(self.test_dir))
            
            # Create report
            report = {
                "timestamp": "2025-07-17T10:30:00Z",
                "terraform_directory": str(self.test_dir),
                "static_analysis": static_results,
                "policy_compliance": compliance_results
            }
            
            # Test JSON serialization
            json_str = json.dumps(report, indent=2)
            self.assertIsInstance(json_str, str)
            
            # Test JSON deserialization
            parsed_report = json.loads(json_str)
            self.assertEqual(parsed_report['terraform_directory'], str(self.test_dir))

if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
