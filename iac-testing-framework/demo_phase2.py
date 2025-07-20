#!/usr/bin/env python3
"""
Demonstration script for the IaC Testing Framework
This script shows how to use the Static Analysis and Policy Compliance modules
"""

import os
import sys
import json
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from static_analysis.static_checker import StaticChecker
from policy_compliance.compliance_checker import ComplianceChecker

def main():
    """Main demonstration function"""
    
    print("🔥 IaC Testing Framework - Phase 2 Demonstration")
    print("=" * 60)
    
    # Set up paths
    current_dir = Path(__file__).parent
    terraform_example_dir = current_dir / "static_analysis" / "examples"
    policies_dir = current_dir / "policy_compliance" / "policies"
    
    print(f"📁 Terraform examples directory: {terraform_example_dir}")
    print(f"📁 Policies directory: {policies_dir}")
    print()
    
    # Initialize modules
    print("🏗️  Initializing Static Analysis module...")
    static_checker = StaticChecker()
    
    print("🔐 Initializing Policy Compliance module...")
    compliance_checker = ComplianceChecker(str(policies_dir))
    
    print()
    print("=" * 60)
    print("📊 PHASE 2 TESTING RESULTS")
    print("=" * 60)
    
    # Run Static Analysis
    print("\n1️⃣ STATIC ANALYSIS RESULTS:")
    print("-" * 40)
    
    try:
        static_results = static_checker.analyze_terraform_files(str(terraform_example_dir))
        print(f"✅ Status: {static_results.get('status')}")
        print(f"📁 Directory: {static_results.get('terraform_directory')}")
        print(f"📄 Terraform files found: {static_results.get('terraform_files_found')}")
        print(f"🔍 Total issues found: {static_results.get('summary', {}).get('total_issues', 0)}")
        print(f"📈 Overall status: {static_results.get('summary', {}).get('overall_status')}")
        
        # Show detailed results
        results = static_results.get('results', {})
        
        # Terraform validate results
        validate_results = results.get('terraform_validate', {})
        print(f"\n   Terraform Validate:")
        print(f"   - Status: {validate_results.get('status')}")
        print(f"   - Valid: {validate_results.get('valid')}")
        print(f"   - Errors: {validate_results.get('error_count', 0)}")
        print(f"   - Warnings: {validate_results.get('warning_count', 0)}")
        
        # TFLint results
        tflint_results = results.get('tflint', {})
        print(f"\n   TFLint:")
        print(f"   - Status: {tflint_results.get('status')}")
        print(f"   - Issues: {tflint_results.get('total_issues', 0)}")
        
        # Checkov results
        checkov_results = results.get('checkov', {})
        print(f"\n   Checkov:")
        print(f"   - Status: {checkov_results.get('status')}")
        print(f"   - Failed checks: {checkov_results.get('failed_checks', 0)}")
        print(f"   - Passed checks: {checkov_results.get('passed_checks', 0)}")
        
        # Show security summary
        security_summary = checkov_results.get('summary', {})
        if security_summary:
            print(f"   - Critical: {security_summary.get('critical', 0)}")
            print(f"   - High: {security_summary.get('high', 0)}")
            print(f"   - Medium: {security_summary.get('medium', 0)}")
            print(f"   - Low: {security_summary.get('low', 0)}")
            
    except Exception as e:
        print(f"❌ Error running static analysis: {e}")
    
    # Run Policy Compliance
    print("\n2️⃣ POLICY COMPLIANCE RESULTS:")
    print("-" * 40)
    
    try:
        compliance_results = compliance_checker.check_compliance(str(terraform_example_dir))
        print(f"✅ Status: {compliance_results.get('status')}")
        print(f"📁 Directory: {compliance_results.get('terraform_directory')}")
        print(f"📋 Total policies: {compliance_results.get('total_policies')}")
        print(f"✅ Passed policies: {compliance_results.get('passed_policies')}")
        print(f"❌ Failed policies: {compliance_results.get('failed_policies')}")
        
        # Show compliance score
        summary = compliance_results.get('summary', {})
        print(f"📊 Compliance score: {summary.get('compliance_score', 0):.1f}%")
        print(f"📈 Overall status: {summary.get('overall_status')}")
        
        # Show policy results
        policy_results = compliance_results.get('results', [])
        if policy_results:
            print(f"\n   Policy Details:")
            for policy in policy_results:
                status_icon = "✅" if policy.get('status') == 'PASSED' else "❌"
                print(f"   {status_icon} {policy.get('policy_name')}: {policy.get('status')}")
                print(f"      - Description: {policy.get('description')}")
                print(f"      - Applicable resources: {policy.get('applicable_resources')}")
                print(f"      - Violations: {policy.get('violation_count')}")
                
    except Exception as e:
        print(f"❌ Error running policy compliance: {e}")
    
    # Show policies summary
    print("\n3️⃣ LOADED POLICIES SUMMARY:")
    print("-" * 40)
    
    try:
        policies_summary = compliance_checker.get_policies_summary()
        print(f"📋 Total policies loaded: {policies_summary.get('total_policies')}")
        
        for policy in policies_summary.get('policies', []):
            print(f"\n   📄 {policy.get('name')}")
            print(f"      - Description: {policy.get('description')}")
            print(f"      - Resource types: {', '.join(policy.get('resource_types', []))}")
            print(f"      - Rules: {policy.get('rules_count')}")
            
    except Exception as e:
        print(f"❌ Error getting policies summary: {e}")
    
    # Generate sample report
    print("\n4️⃣ SAMPLE REPORT GENERATION:")
    print("-" * 40)
    
    try:
        # Combine results for report
        combined_report = {
            "analysis_timestamp": static_results.get('analysis_timestamp', ''),
            "terraform_directory": str(terraform_example_dir),
            "analysis_type": "static_and_compliance",
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
        
        # Save report
        report_path = current_dir / "reports" / "phase2_demo_report.json"
        with open(report_path, 'w') as f:
            json.dump(combined_report, f, indent=2)
        
        print(f"✅ Report saved to: {report_path}")
        print(f"📊 Overall framework status: {combined_report['summary']['overall_status']}")
        
    except Exception as e:
        print(f"❌ Error generating report: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Phase 2 Demonstration Complete!")
    print("=" * 60)
    print("\n📝 Next Steps:")
    print("   - Phase 3: Add Dynamic Provisioning & Runtime Tests")
    print("   - Phase 4: CI/CD Integration")
    print("   - Phase 5: Evaluation & Documentation")

if __name__ == "__main__":
    main()
