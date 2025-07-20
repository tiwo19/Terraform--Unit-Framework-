#!/usr/bin/env python3
"""
Test Runner for IaC Testing Framework
This script provides a command-line interface to run the framework components
"""

import argparse
import sys
import json
from pathlib import Path
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from static_analysis.static_checker import StaticChecker
from policy_compliance.compliance_checker import ComplianceChecker

def run_static_analysis(terraform_dir: str, output_file: str = None):
    """Run static analysis on Terraform files"""
    print("🔍 Running Static Analysis...")
    
    checker = StaticChecker()
    results = checker.analyze_terraform_files(terraform_dir)
    
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"✅ Results saved to: {output_file}")
    
    return results

def run_policy_compliance(terraform_dir: str, policies_dir: str = None, output_file: str = None):
    """Run policy compliance checking"""
    print("🔐 Running Policy Compliance Checks...")
    
    if not policies_dir:
        policies_dir = str(Path(__file__).parent / "policy_compliance" / "policies")
    
    checker = ComplianceChecker(policies_dir)
    results = checker.check_compliance(terraform_dir)
    
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"✅ Results saved to: {output_file}")
    
    return results

def run_combined_analysis(terraform_dir: str, policies_dir: str = None, output_file: str = None):
    """Run both static analysis and policy compliance"""
    print("🚀 Running Combined Analysis...")
    
    # Run static analysis
    static_results = run_static_analysis(terraform_dir)
    
    # Run policy compliance
    compliance_results = run_policy_compliance(terraform_dir, policies_dir)
    
    # Combine results
    combined_results = {
        "analysis_timestamp": datetime.now().isoformat(),
        "terraform_directory": terraform_dir,
        "analysis_type": "combined",
        "static_analysis": static_results,
        "policy_compliance": compliance_results,
        "summary": {
            "total_checks": (
                static_results.get('summary', {}).get('total_issues', 0) + 
                compliance_results.get('total_policies', 0)
            ),
            "passed_checks": compliance_results.get('passed_policies', 0),
            "failed_checks": (
                static_results.get('summary', {}).get('total_issues', 0) + 
                compliance_results.get('failed_policies', 0)
            ),
            "overall_status": "NEEDS_ATTENTION" if (
                static_results.get('summary', {}).get('total_issues', 0) > 0 or
                compliance_results.get('failed_policies', 0) > 0
            ) else "PASSED"
        }
    }
    
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(combined_results, f, indent=2)
        print(f"✅ Combined results saved to: {output_file}")
    
    return combined_results

def print_summary(results: dict):
    """Print a summary of the results"""
    print("\n" + "=" * 60)
    print("📊 ANALYSIS SUMMARY")
    print("=" * 60)
    
    if 'static_analysis' in results:
        # Combined results
        static = results['static_analysis']
        compliance = results['policy_compliance']
        
        print(f"📁 Directory: {results.get('terraform_directory')}")
        print(f"🕐 Timestamp: {results.get('analysis_timestamp')}")
        print(f"📄 Analysis Type: {results.get('analysis_type')}")
        
        print(f"\n🔍 Static Analysis:")
        print(f"   - Status: {static.get('status')}")
        print(f"   - Total Issues: {static.get('summary', {}).get('total_issues', 0)}")
        print(f"   - Validation: {'✅ PASSED' if static.get('summary', {}).get('validation_passed') else '❌ FAILED'}")
        
        print(f"\n🔐 Policy Compliance:")
        print(f"   - Status: {compliance.get('status')}")
        print(f"   - Total Policies: {compliance.get('total_policies')}")
        print(f"   - Passed: {compliance.get('passed_policies')}")
        print(f"   - Failed: {compliance.get('failed_policies')}")
        print(f"   - Score: {compliance.get('summary', {}).get('compliance_score', 0):.1f}%")
        
        print(f"\n📈 Overall Status: {results.get('summary', {}).get('overall_status')}")
        
    else:
        # Single analysis results
        print(f"📁 Directory: {results.get('terraform_directory')}")
        print(f"📄 Status: {results.get('status')}")
        
        if 'summary' in results:
            summary = results['summary']
            print(f"📊 Total Issues: {summary.get('total_issues', 0)}")
            print(f"📈 Overall Status: {summary.get('overall_status')}")

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description="IaC Testing Framework - Phase 2")
    
    # Add subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Static analysis command
    static_parser = subparsers.add_parser('static', help='Run static analysis')
    static_parser.add_argument('terraform_dir', help='Directory containing Terraform files')
    static_parser.add_argument('--output', '-o', help='Output file for results')
    
    # Policy compliance command
    policy_parser = subparsers.add_parser('policy', help='Check policy compliance')
    policy_parser.add_argument('terraform_dir', help='Directory containing Terraform files')
    policy_parser.add_argument('--policies', '-p', help='Directory containing policy files')
    policy_parser.add_argument('--output', '-o', help='Output file for results')
    
    # Combined analysis command
    combined_parser = subparsers.add_parser('combined', help='Run complete analysis')
    combined_parser.add_argument('terraform_dir', help='Directory containing Terraform files')
    combined_parser.add_argument('--policies', '-p', help='Directory containing policy files')
    combined_parser.add_argument('--output', '-o', help='Output file for results')
    
    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Run demonstration')
    
    args = parser.parse_args()
    
    if args.command == 'static':
        results = run_static_analysis(args.terraform_dir, args.output)
        print_summary(results)
        
    elif args.command == 'policy':
        results = run_policy_compliance(args.terraform_dir, args.policies, args.output)
        print_summary(results)
        
    elif args.command == 'combined':
        results = run_combined_analysis(args.terraform_dir, args.policies, args.output)
        print_summary(results)
        
    elif args.command == 'demo':
        # Import and run demo
        from demo_phase2 import main as demo_main
        demo_main()
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
