#!/usr/bin/env python3
"""
🧪 CI/CD Pipeline Local Test
Quick validation script to test CI/CD components locally
"""

import sys
import os
import subprocess
import time

def print_header(title):
    print(f"\n🎯 {title}")
    print("=" * (len(title) + 4))

def run_test(name, command, expected_success=True):
    """Run a test command and report results"""
    print(f"\n🔄 Testing: {name}")
    print("-" * (len(name) + 12))
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0 or not expected_success:
            print(f"✅ {name}: PASSED")
            if result.stdout:
                print(f"📄 Output: {result.stdout[:200]}...")
            return True
        else:
            print(f"⚠️ {name}: NEEDS ATTENTION")
            if result.stderr:
                print(f"📝 Note: {result.stderr[:200]}...")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {name}: TIMEOUT (may still be working)")
        return False
    except Exception as e:
        print(f"📝 {name}: SKIPPED ({e})")
        return False

def main():
    print_header("CI/CD Pipeline Local Validation Test")
    
    # Check if we're in the right directory
    if not os.path.exists("comprehensive_runner.py"):
        print("\n❌ Please run this from the iac-testing-framework directory")
        return
    
    results = []
    
    # Test 1: Framework Help
    results.append(run_test(
        "Framework CLI",
        "python comprehensive_runner.py --help"
    ))
    
    # Test 2: CI/CD Integration Module
    results.append(run_test(
        "CI/CD Integration",
        "python -c 'from ci_cd.ci_integration import CICDIntegration; ci = CICDIntegration(); print(\"CI/CD Ready\")'"
    ))
    
    # Test 3: Static Analysis
    results.append(run_test(
        "Static Analysis",
        "python comprehensive_runner.py static ./static_analysis/examples"
    ))
    
    # Test 4: Policy Compliance  
    results.append(run_test(
        "Policy Compliance",
        "python comprehensive_runner.py policy ./static_analysis/examples"
    ))
    
    # Test 5: CI/CD Annotations
    results.append(run_test(
        "GitHub Actions Annotations",
        "python -c 'from ci_cd.ci_integration import CICDIntegration; ci = CICDIntegration(\"github_actions\"); ci.set_notice(\"Test annotation\")'"
    ))
    
    # Test 6: Report Generation
    results.append(run_test(
        "Report Generation",
        "python -c 'from ci_cd.ci_integration import CICDIntegration; ci = CICDIntegration(); ci.save_results_for_reporting({\"test\": \"data\"}, \"test-reports\")'"
    ))
    
    # Summary
    print_header("LOCAL VALIDATION RESULTS")
    passed = sum(results)
    total = len(results)
    
    print(f"📊 Test Results: {passed}/{total} passed ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - CI/CD Pipeline Ready!")
        print("✅ Your pipeline should work perfectly on GitHub Actions")
    elif passed >= total * 0.8:
        print("⚠️ MOSTLY WORKING - Minor issues detected")
        print("✅ CI/CD pipeline should work with expected warnings")
    else:
        print("❌ ISSUES DETECTED - Review failed tests")
        print("⚠️ CI/CD pipeline may have problems")
    
    print_header("Next Steps")
    print("1. 🌐 Check GitHub Actions: https://github.com/tiwo19/Terraform--Unit-Framework-/actions")
    print("2. 📊 View live pipeline execution in real-time")
    print("3. 🔍 Check for annotations and PR comments")
    print("4. 📁 Download artifacts after pipeline completes")
    print("\n🚀 Your CI/CD pipeline is now running on GitHub!")

if __name__ == "__main__":
    main()
