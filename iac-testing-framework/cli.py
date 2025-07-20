#!/usr/bin/env python3
"""
Command Line Interface for IaC Testing Framework
This CLI provides access to static analysis and policy compliance checking
"""

import argparse
import sys
import os
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from static_analysis.static_checker import StaticChecker
from policy_compliance.compliance_checker import ComplianceChecker

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="IaC Testing Framework")
    
    # Add subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Static analysis command
    static_parser = subparsers.add_parser('static', help='Run static analysis')
    static_parser.add_argument('terraform_dir', help='Directory containing Terraform files')
    static_parser.add_argument('--output', '-o', help='Output file for results')
    static_parser.add_argument('--format', choices=['json', 'yaml'], default='json',
                               help='Output format')
    
    # Policy compliance command
    policy_parser = subparsers.add_parser('policy', help='Check policy compliance')
    policy_parser.add_argument('terraform_dir', help='Directory containing Terraform files')
    policy_parser.add_argument('--policies', '-p', help='Directory containing policy files')
    policy_parser.add_argument('--output', '-o', help='Output file for results')
    policy_parser.add_argument('--format', choices=['json', 'yaml'], default='json',
                               help='Output format')
    
    # Combined analysis command
    combined_parser = subparsers.add_parser('analyze', help='Run complete analysis')
    combined_parser.add_argument('terraform_dir', help='Directory containing Terraform files')
    combined_parser.add_argument('--policies', '-p', help='Directory containing policy files')
    combined_parser.add_argument('--output', '-o', help='Output file for results')
    combined_parser.add_argument('--format', choices=['json', 'yaml'], default='json',
                                 help='Output format')
    
    args = parser.parse_args()
    
    if args.command == 'static':
        run_static_analysis(args)
    elif args.command == 'policy':
        run_policy_compliance(args)
    elif args.command == 'analyze':
        run_combined_analysis(args)
    else:
        parser.print_help()

def run_static_analysis(args):
    """Run static analysis on Terraform files"""
    checker = StaticChecker()
    results = checker.analyze_terraform_files(args.terraform_dir)
    
    if args.output:
        with open(args.output, 'w') as f:
            if args.format == 'json':
                import json
                json.dump(results, f, indent=2)
            else:
                import yaml
                yaml.dump(results, f)
    else:
        print(f"Static analysis results for {args.terraform_dir}:")
        print(results)

def run_policy_compliance(args):
    """Run policy compliance checking on Terraform files"""
    policies_dir = args.policies or "policy_compliance/policies"
    checker = ComplianceChecker(policies_dir)
    results = checker.check_compliance(args.terraform_dir)
    
    if args.output:
        with open(args.output, 'w') as f:
            if args.format == 'json':
                import json
                json.dump(results, f, indent=2)
            else:
                import yaml
                yaml.dump(results, f)
    else:
        print(f"Policy compliance results for {args.terraform_dir}:")
        print(results)

def run_combined_analysis(args):
    """Run both static analysis and policy compliance checking"""
    # Static analysis
    static_checker = StaticChecker()
    static_results = static_checker.analyze_terraform_files(args.terraform_dir)
    
    # Policy compliance
    policies_dir = args.policies or "policy_compliance/policies"
    policy_checker = ComplianceChecker(policies_dir)
    policy_results = policy_checker.check_compliance(args.terraform_dir)
    
    # Combine results
    combined_results = {
        'static_analysis': static_results,
        'policy_compliance': policy_results
    }
    
    if args.output:
        with open(args.output, 'w') as f:
            if args.format == 'json':
                import json
                json.dump(combined_results, f, indent=2)
            else:
                import yaml
                yaml.dump(combined_results, f)
    else:
        print(f"Combined analysis results for {args.terraform_dir}:")
        print(combined_results)

if __name__ == '__main__':
    main()
