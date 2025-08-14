# 🔐 AWS Integration Setup for CI/CD

## ⚠️ **Optional: Real AWS Testing**

### **Step 1: Add AWS Secrets to GitHub**
1. Go to repository **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"**
3. Add these secrets:

```
AWS_ACCESS_KEY_ID: your-access-key
AWS_SECRET_ACCESS_KEY: your-secret-key
AWS_DEFAULT_REGION: us-east-1
```

### **Step 2: Update Workflow for AWS**
Edit `.github/workflows/demo-iac-testing.yml`:

```yaml
- name: 🚀 Run Dynamic Testing (AWS)
  env:
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    AWS_DEFAULT_REGION: ${{ secrets.AWS_DEFAULT_REGION }}
  run: |
    python comprehensive_runner.py dynamic ./static_analysis/examples/sample --environment aws
```

### **🛡️ Security Best Practices:**
- ✅ Use IAM roles with minimal permissions
- ✅ Never commit AWS credentials to code
- ✅ Use GitHub secrets for sensitive data
- ✅ Test with LocalStack first (safer)

### **📊 LocalStack vs AWS:**
| Feature | LocalStack | Real AWS |
|---------|------------|----------|
| **Safety** | ✅ No charges | ⚠️ May incur costs |
| **Speed** | ✅ Fast | ⚠️ Slower |
| **Realism** | ⚠️ Simulated | ✅ Real cloud |
| **CI/CD** | ✅ Perfect for testing | ✅ Production validation |

**💡 Recommendation:** Use LocalStack for CI/CD, Real AWS for final validation
