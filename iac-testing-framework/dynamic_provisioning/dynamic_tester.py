#!/usr/bin/env python3
"""
Dynamic Provisioning and Runtime Testing Module
This module deploys Terraform infrastructure to test environments and validates runtime behavior
"""

import os
import json
import subprocess
import time
import boto3
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

class DynamicTester:
    """
    Handles dynamic provisioning and runtime testing of Terraform infrastructure
    """
    
    def __init__(self, test_environment: str = "localstack", aws_region: str = "us-east-1"):
        """
        Initialize the dynamic tester
        
        Args:
            test_environment: Either 'localstack' for local testing or 'aws' for real AWS
            aws_region: AWS region to use for testing
        """
        self.test_environment = test_environment
        self.aws_region = aws_region
        self.logger = self._setup_logging()
        
        # Initialize AWS clients based on environment
        if test_environment == "localstack":
            self.aws_clients = self._init_localstack_clients()
        else:
            self.aws_clients = self._init_aws_clients()
    
    def _setup_logging(self) -> logging.Logger:
        """Set up logging for the dynamic tester"""
        logger = logging.getLogger("DynamicTester")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _init_localstack_clients(self) -> Dict[str, Any]:
        """Initialize LocalStack clients for local testing"""
        endpoint_url = "http://localhost:4566"
        
        clients = {
            'ec2': boto3.client('ec2', region_name=self.aws_region, endpoint_url=endpoint_url),
            's3': boto3.client('s3', region_name=self.aws_region, endpoint_url=endpoint_url),
            'iam': boto3.client('iam', region_name=self.aws_region, endpoint_url=endpoint_url),
            'vpc': boto3.client('ec2', region_name=self.aws_region, endpoint_url=endpoint_url)
        }
        
        return clients
    
    def _init_aws_clients(self) -> Dict[str, Any]:
        """Initialize real AWS clients"""
        clients = {
            'ec2': boto3.client('ec2', region_name=self.aws_region),
            's3': boto3.client('s3', region_name=self.aws_region),
            'iam': boto3.client('iam', region_name=self.aws_region),
            'vpc': boto3.client('ec2', region_name=self.aws_region)
        }
        
        return clients
    
    def deploy_infrastructure(self, terraform_dir: str) -> Dict[str, Any]:
        """
        Deploy Terraform infrastructure to test environment
        
        Args:
            terraform_dir: Directory containing Terraform files
            
        Returns:
            Deployment results and metadata
        """
        self.logger.info(f"Starting infrastructure deployment in {terraform_dir}")
        
        result = {
            "status": "unknown",
            "terraform_directory": terraform_dir,
            "deployment_timestamp": datetime.now().isoformat(),
            "environment": self.test_environment,
            "deployment_time": 0,
            "resources_created": [],
            "errors": []
        }
        
        start_time = time.time()
        
        try:
            # Change to terraform directory
            original_dir = os.getcwd()
            os.chdir(terraform_dir)
            
            # Initialize Terraform
            init_result = self._run_terraform_command(["terraform", "init"])
            if init_result["returncode"] != 0:
                result["status"] = "failed"
                result["errors"].append(f"Terraform init failed: {init_result['stderr']}")
                return result
            
            # Plan deployment
            plan_result = self._run_terraform_command(["terraform", "plan", "-out=tfplan"])
            if plan_result["returncode"] != 0:
                result["status"] = "failed"
                result["errors"].append(f"Terraform plan failed: {plan_result['stderr']}")
                return result
            
            # Apply deployment
            apply_result = self._run_terraform_command(["terraform", "apply", "-auto-approve", "tfplan"])
            if apply_result["returncode"] != 0:
                result["status"] = "failed"
                result["errors"].append(f"Terraform apply failed: {apply_result['stderr']}")
                return result
            
            # Get terraform state to extract created resources
            state_result = self._run_terraform_command(["terraform", "show", "-json"])
            if state_result["returncode"] == 0:
                try:
                    state_data = json.loads(state_result["stdout"])
                    result["resources_created"] = self._extract_resources_from_state(state_data)
                except json.JSONDecodeError:
                    self.logger.warning("Could not parse terraform state JSON")
            
            result["status"] = "success"
            result["deployment_time"] = time.time() - start_time
            
        except Exception as e:
            result["status"] = "error"
            result["errors"].append(f"Deployment error: {str(e)}")
            
        finally:
            os.chdir(original_dir)
        
        return result
    
    def run_runtime_tests(self, terraform_dir: str) -> Dict[str, Any]:
        """
        Run runtime tests on deployed infrastructure
        
        Args:
            terraform_dir: Directory containing Terraform files
            
        Returns:
            Runtime test results
        """
        self.logger.info("Starting runtime tests")
        
        result = {
            "status": "unknown",
            "test_timestamp": datetime.now().isoformat(),
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "test_results": [],
            "summary": {}
        }
        
        try:
            # Get deployed resources
            deployment_info = self._get_deployment_info(terraform_dir)
            
            if not deployment_info:
                result["status"] = "error"
                result["test_results"].append({
                    "test_name": "deployment_check",
                    "status": "failed",
                    "message": "No deployed infrastructure found"
                })
                return result
            
            # Run tests for each resource type
            test_functions = [
                self._test_vpc_configuration,
                self._test_ec2_instances,
                self._test_s3_buckets,
                self._test_security_groups,
                self._test_connectivity
            ]
            
            for test_func in test_functions:
                test_result = test_func(deployment_info)
                result["test_results"].extend(test_result)
            
            # Calculate summary
            result["total_tests"] = len(result["test_results"])
            result["passed_tests"] = len([t for t in result["test_results"] if t["status"] == "passed"])
            result["failed_tests"] = len([t for t in result["test_results"] if t["status"] == "failed"])
            
            result["status"] = "success" if result["failed_tests"] == 0 else "partial_failure"
            
            result["summary"] = {
                "overall_status": "PASSED" if result["failed_tests"] == 0 else "FAILED",
                "success_rate": (result["passed_tests"] / result["total_tests"] * 100) if result["total_tests"] > 0 else 0
            }
            
        except Exception as e:
            result["status"] = "error"
            result["test_results"].append({
                "test_name": "runtime_tests",
                "status": "error",
                "message": f"Runtime test error: {str(e)}"
            })
        
        return result
    
    def _test_vpc_configuration(self, deployment_info: Dict) -> List[Dict]:
        """Test VPC configuration"""
        tests = []
        
        try:
            vpcs = self.aws_clients['vpc'].describe_vpcs()['Vpcs']
            
            if vpcs:
                vpc = vpcs[0]  # Assuming first VPC for testing
                
                # Test VPC exists
                tests.append({
                    "test_name": "vpc_exists",
                    "status": "passed",
                    "message": f"VPC {vpc['VpcId']} found",
                    "details": {"vpc_id": vpc['VpcId'], "cidr": vpc['CidrBlock']}
                })
                
                # Test CIDR block
                if vpc['CidrBlock']:
                    tests.append({
                        "test_name": "vpc_cidr_configured",
                        "status": "passed",
                        "message": f"VPC CIDR configured: {vpc['CidrBlock']}"
                    })
                
            else:
                tests.append({
                    "test_name": "vpc_exists",
                    "status": "failed",
                    "message": "No VPC found"
                })
                
        except Exception as e:
            tests.append({
                "test_name": "vpc_configuration",
                "status": "error",
                "message": f"VPC test error: {str(e)}"
            })
        
        return tests
    
    def _test_ec2_instances(self, deployment_info: Dict) -> List[Dict]:
        """Test EC2 instances"""
        tests = []
        
        try:
            instances = self.aws_clients['ec2'].describe_instances()
            
            running_instances = []
            for reservation in instances['Reservations']:
                for instance in reservation['Instances']:
                    if instance['State']['Name'] == 'running':
                        running_instances.append(instance)
            
            if running_instances:
                tests.append({
                    "test_name": "ec2_instances_running",
                    "status": "passed",
                    "message": f"Found {len(running_instances)} running instances",
                    "details": {"instance_count": len(running_instances)}
                })
                
                # Test each instance
                for i, instance in enumerate(running_instances):
                    tests.append({
                        "test_name": f"ec2_instance_{i}_state",
                        "status": "passed",
                        "message": f"Instance {instance['InstanceId']} is running"
                    })
            else:
                tests.append({
                    "test_name": "ec2_instances_running",
                    "status": "failed",
                    "message": "No running EC2 instances found"
                })
                
        except Exception as e:
            tests.append({
                "test_name": "ec2_instances",
                "status": "error",
                "message": f"EC2 test error: {str(e)}"
            })
        
        return tests
    
    def _test_s3_buckets(self, deployment_info: Dict) -> List[Dict]:
        """Test S3 buckets"""
        tests = []
        
        try:
            buckets = self.aws_clients['s3'].list_buckets()['Buckets']
            
            if buckets:
                tests.append({
                    "test_name": "s3_buckets_exist",
                    "status": "passed",
                    "message": f"Found {len(buckets)} S3 buckets",
                    "details": {"bucket_count": len(buckets)}
                })
                
                # Test bucket accessibility
                for bucket in buckets:
                    try:
                        self.aws_clients['s3'].head_bucket(Bucket=bucket['Name'])
                        tests.append({
                            "test_name": f"s3_bucket_{bucket['Name']}_accessible",
                            "status": "passed",
                            "message": f"Bucket {bucket['Name']} is accessible"
                        })
                    except Exception:
                        tests.append({
                            "test_name": f"s3_bucket_{bucket['Name']}_accessible",
                            "status": "failed",
                            "message": f"Bucket {bucket['Name']} is not accessible"
                        })
            else:
                tests.append({
                    "test_name": "s3_buckets_exist",
                    "status": "warning",
                    "message": "No S3 buckets found"
                })
                
        except Exception as e:
            tests.append({
                "test_name": "s3_buckets",
                "status": "error",
                "message": f"S3 test error: {str(e)}"
            })
        
        return tests
    
    def _test_security_groups(self, deployment_info: Dict) -> List[Dict]:
        """Test security groups"""
        tests = []
        
        try:
            security_groups = self.aws_clients['ec2'].describe_security_groups()['SecurityGroups']
            
            for sg in security_groups:
                if sg['GroupName'] != 'default':  # Skip default security group
                    
                    # Test for overly permissive rules
                    has_open_ssh = False
                    has_open_http = False
                    
                    for rule in sg['IpPermissions']:
                        for ip_range in rule.get('IpRanges', []):
                            if ip_range.get('CidrIp') == '0.0.0.0/0':
                                if rule.get('FromPort') == 22:
                                    has_open_ssh = True
                                if rule.get('FromPort') == 80:
                                    has_open_http = True
                    
                    tests.append({
                        "test_name": f"sg_{sg['GroupId']}_ssh_not_open",
                        "status": "failed" if has_open_ssh else "passed",
                        "message": f"SSH access {'is' if has_open_ssh else 'is not'} open to 0.0.0.0/0"
                    })
                    
                    tests.append({
                        "test_name": f"sg_{sg['GroupId']}_configured",
                        "status": "passed",
                        "message": f"Security group {sg['GroupId']} configured"
                    })
                    
        except Exception as e:
            tests.append({
                "test_name": "security_groups",
                "status": "error",
                "message": f"Security group test error: {str(e)}"
            })
        
        return tests
    
    def _test_connectivity(self, deployment_info: Dict) -> List[Dict]:
        """Test network connectivity"""
        tests = []
        
        # This is a placeholder for connectivity tests
        # In a real implementation, you might:
        # - Test HTTP endpoints
        # - Test database connections
        # - Test service discovery
        
        tests.append({
            "test_name": "connectivity_placeholder",
            "status": "passed",
            "message": "Connectivity tests placeholder - implement based on infrastructure"
        })
        
        return tests
    
    def cleanup_deployment(self, terraform_dir: str) -> Dict[str, Any]:
        """
        Clean up deployed infrastructure
        
        Args:
            terraform_dir: Directory containing Terraform files
            
        Returns:
            Cleanup results
        """
        self.logger.info("Starting infrastructure cleanup")
        
        result = {
            "status": "unknown",
            "cleanup_timestamp": datetime.now().isoformat(),
            "errors": []
        }
        
        try:
            original_dir = os.getcwd()
            os.chdir(terraform_dir)
            
            # Destroy infrastructure
            destroy_result = self._run_terraform_command(["terraform", "destroy", "-auto-approve"])
            
            if destroy_result["returncode"] == 0:
                result["status"] = "success"
                self.logger.info("Infrastructure cleanup completed successfully")
            else:
                result["status"] = "failed"
                result["errors"].append(f"Terraform destroy failed: {destroy_result['stderr']}")
                
        except Exception as e:
            result["status"] = "error"
            result["errors"].append(f"Cleanup error: {str(e)}")
            
        finally:
            os.chdir(original_dir)
        
        return result
    
    def _run_terraform_command(self, command: List[str]) -> Dict[str, Any]:
        """Run a terraform command and return results"""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            return {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
            
        except subprocess.TimeoutExpired:
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": "Command timed out"
            }
        except Exception as e:
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": str(e)
            }
    
    def _extract_resources_from_state(self, state_data: Dict) -> List[Dict]:
        """Extract resource information from terraform state"""
        resources = []
        
        if 'values' in state_data and 'root_module' in state_data['values']:
            root_module = state_data['values']['root_module']
            
            if 'resources' in root_module:
                for resource in root_module['resources']:
                    resources.append({
                        "type": resource.get('type'),
                        "name": resource.get('name'),
                        "address": resource.get('address'),
                        "values": resource.get('values', {})
                    })
        
        return resources
    
    def _get_deployment_info(self, terraform_dir: str) -> Optional[Dict]:
        """Get information about deployed infrastructure"""
        try:
            original_dir = os.getcwd()
            os.chdir(terraform_dir)
            
            state_result = self._run_terraform_command(["terraform", "show", "-json"])
            
            if state_result["returncode"] == 0:
                return json.loads(state_result["stdout"])
            
        except Exception as e:
            self.logger.error(f"Error getting deployment info: {e}")
        finally:
            os.chdir(original_dir)
        
        return None

def main():
    """Demo function for dynamic testing"""
    tester = DynamicTester(test_environment="localstack")
    
    # Example usage
    terraform_dir = "../static_analysis/examples"
    
    print("🚀 Dynamic Provisioning & Runtime Testing Demo")
    print("=" * 50)
    
    # Deploy infrastructure
    print("1. Deploying infrastructure...")
    deployment_result = tester.deploy_infrastructure(terraform_dir)
    print(f"Deployment status: {deployment_result['status']}")
    
    if deployment_result['status'] == 'success':
        # Run runtime tests
        print("\n2. Running runtime tests...")
        test_result = tester.run_runtime_tests(terraform_dir)
        print(f"Test status: {test_result['status']}")
        print(f"Tests passed: {test_result['passed_tests']}/{test_result['total_tests']}")
        
        # Cleanup
        #print("\n3. Cleaning up...")
       # cleanup_result = tester.cleanup_deployment(terraform_dir)
       # print(f"Cleanup status: {cleanup_result['status']}")

if __name__ == "__main__":
    main()
