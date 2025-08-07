#!/usr/bin/env python3
"""
Simple CI/CD Demo Script
This script simulates what happens in your CI/CD pipeline
"""

import subprocess
import sys
import time
import os
from datetime import datetime

def run_command(command, description):
    """Run a command and show the results"""
    print(f"\n{'='*60}")
    print(f"🚀 STEP: {description}")
    print(f"📝 COMMAND: {command}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=300
        )
        
        if result.returncode == 0:
            print(f"✅ SUCCESS: {description}")
            if result.stdout:
                print("📄 OUTPUT:")
                print(result.stdout[:500] + "..." if len(result.stdout) > 500 else result.stdout)
        else:
            print(f"❌ FAILED: {description}")
            if result.stderr:
                print("⚠️ ERROR:")
                print(result.stderr[:500] + "..." if len(result.stderr) > 500 else result.stderr)
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print(f"⏰ TIMEOUT: {description} took too long")
        return False
    except Exception as e:
        print(f"💥 ERROR: {str(e)}")
        return False

def demo_cicd_pipeline():
    """Demo the CI/CD pipeline locally"""
    print("🎯 IaC Testing Framework - CI/CD Demo")
    print("=" * 60)
    print("This simulates what happens when you push code to GitHub")
    print("=" * 60)
    
    # Track results
    results = []
    
    # Step 1: Check environment
    success = run_command(
        "python check_environment.py",
        "Check Environment Setup"
    )
    results.append(("Environment Check", success))
    
    # Step 2: Static Analysis
    success = run_command(
        "python comprehensive_runner.py static ./static_analysis/examples",
        "Static Analysis (Security & Syntax)"
    )
    results.append(("Static Analysis", success))
    
    # Step 3: Policy Compliance
    success = run_command(
        "python comprehensive_runner.py policy ./static_analysis/examples",
        "Policy Compliance Check"
    )
    results.append(("Policy Compliance", success))
    
    # Step 4: Ask user about LocalStack
    print(f"\n{'='*60}")
    print("🐳 LOCALSTACK TESTING")
    print("=" * 60)
    print("CI/CD would normally test with LocalStack for safety.")
    
    user_input = input("Do you want to start LocalStack and run dynamic testing? (y/n): ").lower()
    
    if user_input == 'y':
        # Start LocalStack
        print("🚀 Starting LocalStack...")
        success = run_command(
            "docker-compose up -d localstack",
            "Start LocalStack"
        )
        
        if success:
            print("⏰ Waiting 30 seconds for LocalStack to be ready...")
            time.sleep(30)
            
            # Run comprehensive testing
            success = run_command(
                "python comprehensive_runner.py comprehensive ./static_analysis/examples --environment localstack --include-dynamic",
                "Comprehensive Testing with LocalStack"
            )
            results.append(("Dynamic Testing", success))
        else:
            results.append(("Dynamic Testing", False))
    else:
        print("⏭️ Skipping LocalStack testing")
        results.append(("Dynamic Testing", "Skipped"))
    
    # Show final results
    show_cicd_results(results)

def show_cicd_results(results):
    """Show the final CI/CD results"""
    print(f"\n{'='*60}")
    print("📊 CI/CD PIPELINE RESULTS")
    print("=" * 60)
    
    passed = 0
    failed = 0
    skipped = 0
    
    for step_name, result in results:
        if result is True:
            print(f"✅ {step_name}: PASSED")
            passed += 1
        elif result is False:
            print(f"❌ {step_name}: FAILED")
            failed += 1
        else:
            print(f"⏭️ {step_name}: SKIPPED")
            skipped += 1
    
    print("=" * 60)
    print(f"📈 SUMMARY:")
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Failed: {failed}")
    print(f"   ⏭️ Skipped: {skipped}")
    
    if failed == 0:
        print(f"   🎉 OVERALL: SUCCESS - Ready to deploy!")
    else:
        print(f"   ⚠️ OVERALL: FAILED - Fix issues before deploying")
    
    print("=" * 60)
    
    # Show what happens next
    print("\n🔄 WHAT HAPPENS IN REAL CI/CD:")
    print("✅ If tests pass → Code can be merged/deployed")
    print("❌ If tests fail → Block merge, developer must fix")
    print("📧 Notifications sent to team")
    print("📊 Results stored for reporting")

def show_cicd_explanation():
    """Explain what CI/CD does"""
    print("🎓 UNDERSTANDING CI/CD")
    print("=" * 60)
    print("CI/CD automatically tests your code when you:")
    print("📤 Push code to GitHub")
    print("📬 Create a pull request")
    print("🔀 Merge code to main branch")
    print()
    print("🔄 The pipeline runs these steps:")
    print("1. 📥 Download your code")
    print("2. 🐍 Setup Python environment")
    print("3. 📦 Install dependencies") 
    print("4. 🔍 Run static analysis")
    print("5. 🔐 Check policy compliance")
    print("6. 🧪 Test with LocalStack (safe)")
    print("7. ✅/❌ Pass or fail the build")
    print()
    print("💡 Benefits:")
    print("🚀 Catch bugs early")
    print("🔒 Ensure security standards")
    print("👥 Prevent bad code from reaching production")
    print("⏰ Save time with automation")

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--explain":
        show_cicd_explanation()
        return
    
    print("🎯 Welcome to CI/CD Demo!")
    print("Choose an option:")
    print("1. Run CI/CD simulation")
    print("2. Explain what CI/CD does")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ")
    
    if choice == "1":
        demo_cicd_pipeline()
    elif choice == "2":
        show_cicd_explanation()
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
