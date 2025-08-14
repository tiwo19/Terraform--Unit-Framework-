# 🏢 Jenkins CI/CD Integration

## 🎯 **Enterprise Jenkins Setup**

### **Step 1: Create Jenkins Pipeline**

Create a `Jenkinsfile` in your repository root:

```groovy
pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.9'
    }
    
    stages {
        stage('Setup') {
            steps {
                echo '🐍 Setting up Python environment'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pip install checkov
                '''
            }
        }
        
        stage('Static Analysis') {
            steps {
                echo '🔍 Running static analysis'
                sh '''
                    . venv/bin/activate
                    python comprehensive_runner.py static ./static_analysis/examples
                '''
            }
        }
        
        stage('Policy Compliance') {
            steps {
                echo '🔐 Checking policy compliance'
                sh '''
                    . venv/bin/activate
                    python comprehensive_runner.py policy ./static_analysis/examples
                '''
            }
        }
        
        stage('Dynamic Testing') {
            steps {
                echo '🚀 Running dynamic tests'
                sh '''
                    . venv/bin/activate
                    # Start LocalStack
                    docker run -d -p 4566:4566 localstack/localstack
                    sleep 30
                    
                    # Run dynamic tests
                    python comprehensive_runner.py dynamic ./static_analysis/examples/sample --environment localstack
                '''
            }
        }
        
        stage('Generate Reports') {
            steps {
                echo '📊 Generating CI/CD reports'
                sh '''
                    . venv/bin/activate
                    python -c "
                    from ci_cd.ci_integration import CICDIntegration
                    ci = CICDIntegration('jenkins')
                    results = {'summary': {'overall_status': 'PASSED'}}
                    ci.save_results_for_reporting(results, 'jenkins-reports')
                    "
                '''
            }
        }
    }
    
    post {
        always {
            echo '📤 Archiving artifacts'
            archiveArtifacts artifacts: 'jenkins-reports/**', fingerprint: true
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'jenkins-reports',
                reportFiles: 'summary.html',
                reportName: 'IaC Testing Report'
            ])
        }
        
        success {
            echo '✅ Pipeline completed successfully'
        }
        
        failure {
            echo '❌ Pipeline failed'
            emailext (
                to: 'team@company.com',
                subject: 'IaC Testing Pipeline Failed',
                body: 'The infrastructure testing pipeline has failed. Please check the logs.'
            )
        }
    }
}
```

### **Step 2: Configure Jenkins Job**

1. **Create New Pipeline Job:**
   - Jenkins Dashboard → New Item → Pipeline
   - Name: "IaC-Testing-Framework"

2. **Configure Source:**
   - Pipeline → Definition: "Pipeline script from SCM"
   - SCM: Git
   - Repository URL: `https://github.com/tiwo19/Terraform--Unit-Framework-.git`

3. **Set Triggers:**
   - ✅ GitHub hook trigger for GITScm polling
   - ✅ Poll SCM: `H/5 * * * *` (every 5 minutes)

### **Step 3: Required Jenkins Plugins**

Install these plugins:
```
- Pipeline
- Git
- HTML Publisher
- Email Extension
- Docker Pipeline
- Workspace Cleanup
```

### **Step 4: Environment Variables**

Set in Jenkins → Manage Jenkins → Configure System:
```
DOCKER_HOST=unix:///var/run/docker.sock
LOCALSTACK_ENDPOINT=http://localhost:4566
```

## 🎯 **Jenkins vs GitHub Actions**

| Feature | Jenkins | GitHub Actions |
|---------|---------|----------------|
| **Setup** | ⚠️ Complex | ✅ Simple |
| **Enterprise** | ✅ Advanced | ⚠️ Basic |
| **Customization** | ✅ Unlimited | ⚠️ Limited |
| **Maintenance** | ⚠️ Self-managed | ✅ Hosted |
| **Integration** | ✅ Extensive | ✅ GitHub-native |

**💡 Recommendation:** Start with GitHub Actions, upgrade to Jenkins for enterprise needs
