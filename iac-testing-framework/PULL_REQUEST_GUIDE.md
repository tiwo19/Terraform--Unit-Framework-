# 🤝 Pull Request Guide - How to Contribute

Welcome! This guide shows you how to contribute to the IaC Testing Framework by creating a pull request (PR).

## 🎯 What is a Pull Request?

A **Pull Request** is like saying: *"Hey, I made some improvements to your code. Can you review and add them to the main project?"*

It's a safe way to:
- ✅ Suggest changes without breaking the main code
- 🔍 Get your changes reviewed before they're added
- 🤝 Collaborate with the team

## 🚀 Quick Start (5 Steps)

### Step 1: Fork the Repository
1. Go to: https://github.com/tiwo19/Terraform--Unit-Framework-
2. Click the **"Fork"** button (top right)
3. This creates your own copy of the project

### Step 2: Clone Your Fork
```bash
# Replace "YOUR-USERNAME" with your GitHub username
git clone https://github.com/YOUR-USERNAME/Terraform--Unit-Framework-.git
cd Terraform--Unit-Framework-/iac-testing-framework
```

### Step 3: Create a New Branch
```bash
# Create and switch to a new branch for your changes
git checkout -b my-awesome-feature

# Examples of good branch names:
# git checkout -b fix-policy-bug
# git checkout -b add-new-terraform-example
# git checkout -b improve-documentation
```

### Step 4: Make Your Changes
```bash
# Edit files, add features, fix bugs, etc.
# Test your changes locally:
python check_environment.py
python comprehensive_runner.py static ./static_analysis/examples
```

### Step 5: Create Pull Request
```bash
# Add and commit your changes
git add .
git commit -m "Add awesome new feature that does X"

# Push to your fork
git push origin my-awesome-feature
```

Then go to GitHub and click **"Create Pull Request"**!

## 📋 Detailed Guide

### 🔧 Setting Up Your Environment

1. **Install Prerequisites**:
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Install Terraform (if not already installed)
   # Download from: https://terraform.io/downloads
   ```

2. **Verify Setup**:
   ```bash
   # Check if everything works
   python check_environment.py
   ```

### 💡 What Can You Contribute?

#### 🆕 New Features
- Add new Terraform examples
- Create new policy rules
- Add support for new cloud providers
- Improve error handling

#### 🐛 Bug Fixes
- Fix CI/CD issues
- Resolve policy validation bugs
- Improve error messages
- Fix documentation typos

#### 📚 Documentation
- Improve README files
- Add more examples
- Create tutorials
- Fix spelling/grammar

#### 🧪 Testing
- Add new test cases
- Improve existing tests
- Add edge case scenarios

### ✅ Before Creating Your Pull Request

#### Test Your Changes Locally:
```bash
# 1. Run static analysis
python comprehensive_runner.py static ./static_analysis/examples

# 2. Run policy compliance
python comprehensive_runner.py policy ./static_analysis/examples

# 3. Test with LocalStack (if you have Docker)
docker-compose up -d localstack
python comprehensive_runner.py comprehensive ./static_analysis/examples --environment localstack --include-dynamic

# 4. Run CI/CD demo
python demo_cicd.py
```

#### Check Your Code Quality:
```bash
# Make sure your code follows standards
python -m flake8 your-new-file.py
python -m black your-new-file.py
```

### 📝 Writing a Good Pull Request

#### 1. Choose a Clear Title
```
❌ Bad: "Fixed stuff"
❌ Bad: "Update code"
✅ Good: "Add new AWS S3 security policy"
✅ Good: "Fix terraform validation timeout issue"
✅ Good: "Improve documentation for LocalStack setup"
```

#### 2. Write a Clear Description
```markdown
## What does this PR do?
- Adds new security policy for S3 bucket encryption
- Updates documentation with examples
- Fixes bug in policy validation

## How to test?
1. Run: python comprehensive_runner.py policy ./static_analysis/examples
2. Check that new S3 encryption policy is enforced
3. Verify documentation is clear

## Related Issues
- Fixes #123
- Related to #456
```

#### 3. Include Examples (if applicable)
```terraform
# Example Terraform code that your changes affect
resource "aws_s3_bucket" "example" {
  bucket = "my-secure-bucket"
  
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}
```

### 🔄 The Review Process

#### What Happens After You Submit:
1. **🤖 Automatic Tests**: CI/CD runs automatically
2. **👀 Code Review**: Maintainers review your changes
3. **💬 Feedback**: You might get suggestions for improvements
4. **✅ Approval**: Once approved, your changes are merged!

#### If Tests Fail:
```bash
# Fix the issues locally
git add .
git commit -m "Fix test failures"
git push origin my-awesome-feature
```
The PR will automatically update!

### 📊 Understanding CI/CD Results

When you create a PR, GitHub Actions will automatically run:

#### ✅ Success (All Green):
```
✅ Static Analysis: PASSED
✅ Policy Compliance: PASSED  
✅ Dynamic Testing: PASSED
🎉 Ready to merge!
```

#### ❌ Failure (Red X):
```
❌ Static Analysis: FAILED
   - Fix security issues in your code
✅ Policy Compliance: PASSED
❌ Dynamic Testing: FAILED
   - Check Terraform syntax
```

### 🎯 Common Contribution Examples

#### Example 1: Add New Terraform Example
```bash
# 1. Create new directory
mkdir static_analysis/examples/web-app-secure

# 2. Add Terraform files
# Create main.tf, variables.tf, outputs.tf

# 3. Test locally
python comprehensive_runner.py static ./static_analysis/examples/web-app-secure

# 4. Commit and push
git add .
git commit -m "Add secure web application Terraform example"
git push origin add-web-app-example
```

#### Example 2: Fix Documentation
```bash
# 1. Edit README files or documentation
# 2. Test that examples still work
# 3. Commit changes
git add .
git commit -m "Improve LocalStack setup documentation"
git push origin improve-docs
```

#### Example 3: Add New Policy
```bash
# 1. Create new policy file
# policy_compliance/policies/new_security_policy.yaml

# 2. Test the policy
python comprehensive_runner.py policy ./static_analysis/examples

# 3. Update documentation if needed
# 4. Commit and push
git add .
git commit -m "Add new security policy for database encryption"
git push origin add-db-encryption-policy
```

### 🆘 Need Help?

#### Getting Stuck?
- 💬 **Ask Questions**: Create an issue or comment on your PR
- 📚 **Check Documentation**: Read README files and guides
- 🧪 **Test Locally**: Use `python demo_cicd.py` to simulate CI/CD

#### Common Issues:
```bash
# Problem: Tests failing locally
# Solution: Check environment
python check_environment.py

# Problem: Merge conflicts
# Solution: Update your branch
git checkout main
git pull upstream main
git checkout your-branch
git merge main

# Problem: CI/CD failing
# Solution: Check the Actions tab in GitHub for detailed logs
```

### 🏆 Best Practices

#### ✅ Do:
- Test your changes locally first
- Write clear commit messages
- Keep changes focused (one feature per PR)
- Update documentation when needed
- Be responsive to feedback

#### ❌ Don't:
- Make huge PRs with many unrelated changes
- Break existing functionality
- Ignore test failures
- Skip testing locally
- Be rude in comments

### 🎉 After Your PR is Merged

#### What Happens:
1. **🎊 Celebration**: Your code is now part of the project!
2. **📄 Credit**: You're listed as a contributor
3. **🔄 Cleanup**: You can delete your branch
4. **🚀 Deploy**: Your changes go live for everyone

#### Clean Up:
```bash
# Delete your local branch (after merge)
git checkout main
git pull origin main
git branch -d my-awesome-feature

# Delete remote branch
git push origin --delete my-awesome-feature
```

## 🎯 Quick Reference

### Essential Commands:
```bash
# Start contributing
git clone https://github.com/YOUR-USERNAME/Terraform--Unit-Framework-.git
git checkout -b new-feature

# Test locally
python check_environment.py
python comprehensive_runner.py static ./static_analysis/examples

# Submit PR
git add .
git commit -m "Descriptive message"
git push origin new-feature
```

### Key Files to Know:
- `comprehensive_runner.py` - Main test runner
- `static_analysis/examples/` - Terraform examples
- `policy_compliance/policies/` - Policy definitions
- `requirements.txt` - Python dependencies
- `.github/workflows/simple-cicd.yml` - CI/CD configuration

## 🤝 Thank You!

Your contributions make this project better for everyone. Whether it's:
- 🐛 Fixing a small bug
- ✨ Adding a cool new feature  
- 📚 Improving documentation
- 🧪 Adding test cases

**Every contribution matters!** 🙏

Ready to contribute? **Fork the repo and start coding!** 🚀
