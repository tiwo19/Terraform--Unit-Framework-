# Policy Compliance Checker for Terraform IaC
# This module checks Terraform configurations against defined policies

import os
import json
import yaml
import subprocess
import re
from pathlib import Path
from typing import Dict, List, Any

class ComplianceChecker:
    """
    Policy compliance checker for Terraform infrastructure code
    """
    
    def __init__(self, policies_dir: str = "policies"):
        self.policies_dir = policies_dir
        self.policies = self._load_policies()
    
    def _load_policies(self) -> Dict[str, Any]:
        """
        Load policy definitions from the policies directory
        
        Returns:
            Dictionary containing loaded policies
        """
        policies = {}
        
        if not os.path.exists(self.policies_dir):
            print(f"Warning: Policies directory {self.policies_dir} does not exist")
            return policies
        
        try:
            for filename in os.listdir(self.policies_dir):
                if filename.endswith(('.yml', '.yaml')):
                    filepath = os.path.join(self.policies_dir, filename)
                    with open(filepath, 'r', encoding='utf-8') as file:
                        policy_data = yaml.safe_load(file)
                        if policy_data and 'policies' in policy_data:
                            for policy in policy_data['policies']:
                                policy_name = policy.get('name')
                                if policy_name:
                                    policies[policy_name] = policy
                        
                elif filename.endswith('.json'):
                    filepath = os.path.join(self.policies_dir, filename)
                    with open(filepath, 'r', encoding='utf-8') as file:
                        policy_data = json.load(file)
                        if policy_data and 'policies' in policy_data:
                            for policy in policy_data['policies']:
                                policy_name = policy.get('name')
                                if policy_name:
                                    policies[policy_name] = policy
        except Exception as e:
            print(f"Error loading policies: {e}")
        
        return policies
    
    def check_compliance(self, terraform_dir: str) -> Dict[str, Any]:
        """
        Check Terraform configurations against loaded policies
        
        Args:
            terraform_dir: Directory containing Terraform files
            
        Returns:
            Dictionary containing compliance check results
        """
        if not self.policies:
            return {
                "status": "error",
                "error_message": "No policies loaded",
                "results": []
            }
        
        # Parse Terraform files
        terraform_resources = self._parse_terraform_files(terraform_dir)
        
        if not terraform_resources:
            return {
                "status": "error",
                "error_message": "No Terraform resources found",
                "results": []
            }
        
        # Run compliance checks
        compliance_results = []
        
        for policy_name, policy_config in self.policies.items():
            policy_result = self._check_policy_compliance(
                policy_name, policy_config, terraform_resources
            )
            compliance_results.append(policy_result)
        
        # Calculate summary
        passed_policies = sum(1 for result in compliance_results if result["status"] == "PASSED")
        failed_policies = sum(1 for result in compliance_results if result["status"] == "FAILED")
        
        return {
            "status": "success",
            "terraform_directory": terraform_dir,
            "total_policies": len(self.policies),
            "passed_policies": passed_policies,
            "failed_policies": failed_policies,
            "results": compliance_results,
            "summary": {
                "compliance_score": (passed_policies / len(self.policies)) * 100 if self.policies else 0,
                "overall_status": "PASSED" if failed_policies == 0 else "FAILED"
            }
        }
    
    def validate_resource_policies(self, resource_config: Dict[str, Any]) -> List[str]:
        """
        Validate a specific resource configuration against policies
        
        Args:
            resource_config: Configuration of a Terraform resource
            
        Returns:
            List of policy violations
        """
        violations = []
        resource_type = resource_config.get('type')
        
        if not resource_type:
            return violations
        
        # Check each policy
        for policy_name, policy_config in self.policies.items():
            resource_types = policy_config.get('resource_types', [])
            
            # Check if policy applies to this resource type
            if resource_type in resource_types:
                rules = policy_config.get('rules', [])
                
                for rule in rules:
                    violation = self._check_rule_violation(resource_config, rule, policy_name)
                    if violation:
                        violations.append(violation)
        
        return violations
    
    def _parse_terraform_files(self, terraform_dir: str) -> List[Dict[str, Any]]:
        """
        Parse Terraform files to extract resource configurations
        
        Args:
            terraform_dir: Directory containing Terraform files
            
        Returns:
            List of resource configurations
        """
        resources = []
        
        try:
            # Simple parsing of .tf files
            for root, dirs, files in os.walk(terraform_dir):
                for file in files:
                    if file.endswith('.tf'):
                        filepath = os.path.join(root, file)
                        try:
                            with open(filepath, 'r', encoding='utf-8') as f:
                                content = f.read()
                                # Basic regex-based parsing for resource blocks
                                resource_pattern = r'resource\s+"([^"]+)"\s+"([^"]+)"\s*\{'
                                matches = re.findall(resource_pattern, content)
                                
                                for match in matches:
                                    resources.append({
                                        'type': match[0],
                                        'name': match[1],
                                        'file': filepath,
                                        'address': f"{match[0]}.{match[1]}"
                                    })
                        except Exception as e:
                            print(f"Error parsing {filepath}: {e}")
                            
        except Exception as e:
            print(f"Error parsing Terraform files: {e}")
        
        return resources
    
    def _check_policy_compliance(self, policy_name: str, policy_config: Dict[str, Any], 
                               terraform_resources: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Check compliance for a specific policy
        
        Args:
            policy_name: Name of the policy
            policy_config: Policy configuration
            terraform_resources: List of Terraform resources
            
        Returns:
            Policy compliance result
        """
        resource_types = policy_config.get('resource_types', [])
        rules = policy_config.get('rules', [])
        
        # Find relevant resources
        relevant_resources = [
            resource for resource in terraform_resources 
            if resource.get('type') in resource_types
        ]
        
        violations = []
        
        for resource in relevant_resources:
            for rule in rules:
                violation = self._check_rule_violation(resource, rule, policy_name)
                if violation:
                    violations.append(violation)
        
        return {
            "policy_name": policy_name,
            "description": policy_config.get('description', ''),
            "status": "PASSED" if not violations else "FAILED",
            "applicable_resources": len(relevant_resources),
            "violations": violations,
            "violation_count": len(violations)
        }
    
    def _check_rule_violation(self, resource: Dict[str, Any], rule: Dict[str, Any], 
                            policy_name: str) -> Dict[str, Any]:
        """
        Check if a resource violates a specific rule
        
        Args:
            resource: Resource configuration
            rule: Rule configuration
            policy_name: Name of the policy
            
        Returns:
            Violation details if found, None otherwise
        """
        property_name = rule.get('property')
        if not property_name:
            return None
        
        # For simple parsing, we'll check basic properties
        # In a full implementation, this would parse the actual resource configuration
        
        # Check if property is required
        if rule.get('required'):
            return {
                "resource": resource.get('address', resource.get('name')),
                "resource_type": resource.get('type'),
                "rule": f"Property {property_name} is required but not validated in simple parsing",
                "policy": policy_name,
                "severity": "MEDIUM"
            }
        
        return None
    
    def run_opa_check(self, terraform_dir: str, opa_policy_file: str) -> Dict[str, Any]:
        """
        Run Open Policy Agent (OPA) checks on Terraform files
        
        Args:
            terraform_dir: Directory containing Terraform files
            opa_policy_file: Path to OPA policy file
            
        Returns:
            OPA check results
        """
        try:
            # Run OPA eval command
            result = subprocess.run(
                ['opa', 'eval', '-d', opa_policy_file, '-i', terraform_dir, 'data.terraform.deny'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                opa_output = json.loads(result.stdout) if result.stdout else {}
                
                return {
                    "tool": "opa",
                    "status": "success",
                    "results": opa_output,
                    "violations": opa_output.get("result", [])
                }
            else:
                return {
                    "tool": "opa",
                    "status": "error",
                    "error_message": result.stderr,
                    "violations": []
                }
                
        except FileNotFoundError:
            return {
                "tool": "opa",
                "status": "not_found",
                "error_message": "OPA not found. Please install Open Policy Agent.",
                "violations": []
            }
        except Exception as e:
            return {
                "tool": "opa",
                "status": "error",
                "error_message": str(e),
                "violations": []
            }
    
    def get_policies_summary(self) -> Dict[str, Any]:
        """
        Get summary of loaded policies
        
        Returns:
            Summary of policies
        """
        return {
            "total_policies": len(self.policies),
            "policies": [
                {
                    "name": policy_name,
                    "description": policy_config.get('description', ''),
                    "resource_types": policy_config.get('resource_types', []),
                    "rules_count": len(policy_config.get('rules', []))
                }
                for policy_name, policy_config in self.policies.items()
            ]
        }
