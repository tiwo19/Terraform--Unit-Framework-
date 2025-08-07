#!/usr/bin/env python3
"""
AWS Environment Checker
Simple utility to verify AWS credentials and environment setup
"""

import boto3
import json
import os
from pathlib import Path

def check_aws_credentials():
    """Check if AWS credentials are properly configured"""
    print("🔍 Checking AWS Credentials...")
    
    try:
        # Try to create a session
        session = boto3.Session()
        credentials = session.get_credentials()
        
        if credentials is None:
            print("❌ No AWS credentials found")
            print("💡 Configure credentials using:")
            print("   - aws configure")
            print("   - Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables")
            return False
        
        # Try to make a simple API call
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        
        print("✅ AWS credentials are valid")
        print(f"   Account: {identity.get('Account', 'Unknown')}")
        print(f"   User/Role: {identity.get('Arn', 'Unknown')}")
        return True
        
    except Exception as e:
        print(f"❌ AWS credential error: {str(e)}")
        return False

def check_localstack():
    """Check if LocalStack is running"""
    print("\n🐳 Checking LocalStack...")
    
    try:
        import requests
        response = requests.get("http://localhost:4566/_localstack/health", timeout=5)
        
        if response.status_code == 200:
            print("✅ LocalStack is running")
            health = response.json()
            print("   Services:", ", ".join([s for s, status in health.get('services', {}).items() if status == 'running']))
            return True
        else:
            print("❌ LocalStack is not responding properly")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ LocalStack is not running")
        print("💡 Start LocalStack with: docker-compose up -d localstack")
        return False
    except Exception as e:
        print(f"❌ LocalStack check error: {str(e)}")
        return False

def show_config_help():
    """Show configuration help"""
    config_file = Path(__file__).parent / "aws_config.json"
    
    if config_file.exists():
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        print("\n📋 Environment Configuration:")
        print("=" * 50)
        
        for env_name, env_config in config['environments'].items():
            print(f"\n🌍 {env_name.upper()}:")
            print(f"   Description: {env_config['description']}")
            if 'cost_warning' in env_config:
                print(f"   ⚠️  Warning: {env_config['cost_warning']}")
        
        print(f"\n💡 AWS Credentials Help:")
        for method in config['aws_credentials']['methods']:
            print(f"   {method}")

def main():
    """Main function"""
    print("🚀 IaC Testing Framework - Environment Checker")
    print("=" * 60)
    
    # Check AWS credentials
    aws_ok = check_aws_credentials()
    
    # Check LocalStack
    localstack_ok = check_localstack()
    
    # Show configuration help
    show_config_help()
    
    print("\n" + "=" * 60)
    print("📊 Environment Summary:")
    print(f"   AWS Ready: {'✅ Yes' if aws_ok else '❌ No'}")
    print(f"   LocalStack Ready: {'✅ Yes' if localstack_ok else '❌ No'}")
    
    if aws_ok:
        print("\n✅ You can use: --environment aws")
    if localstack_ok:
        print("✅ You can use: --environment localstack")
    if not aws_ok and not localstack_ok:
        print("\n⚠️  No testing environments available. Please configure AWS or start LocalStack.")
    
    print("\n🔧 Usage examples:")
    print("   python comprehensive_runner.py comprehensive ./static_analysis/examples --environment localstack --include-dynamic")
    if aws_ok:
        print("   python comprehensive_runner.py comprehensive ./static_analysis/examples --environment aws --include-dynamic")

if __name__ == "__main__":
    main()
