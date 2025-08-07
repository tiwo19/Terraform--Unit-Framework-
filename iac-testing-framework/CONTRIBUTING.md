# 🤝 Contributing to IaC Testing Framework

Thank you for your interest in contributing! This project welcomes contributions from developers of all skill levels.

## 🚀 Quick Start

1. **Fork** the repository
2. **Clone** your fork locally
3. **Create** a new branch for your changes
4. **Make** your improvements
5. **Test** locally 
6. **Submit** a pull request

For detailed instructions, see our [Pull Request Guide](PULL_REQUEST_GUIDE.md).

## 📋 Ways to Contribute

### 🐛 Bug Reports
Found a bug? Please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment details

### ✨ Feature Requests  
Have an idea? We'd love to hear it! Please include:
- Description of the feature
- Why it would be useful
- How it might work

### 🔧 Code Contributions
Ready to code? Great! Please:
- Follow our coding standards
- Add tests for new features
- Update documentation
- Keep PRs focused and small

### 📚 Documentation
Help others by:
- Fixing typos
- Adding examples
- Improving clarity
- Creating tutorials

## 🧪 Testing Your Changes

Before submitting a PR, please test locally:

```bash
# Check environment setup
python check_environment.py

# Run static analysis
python comprehensive_runner.py static ./static_analysis/examples

# Run policy compliance
python comprehensive_runner.py policy ./static_analysis/examples

# Test CI/CD pipeline
python demo_cicd.py
```

## 📝 Code Standards

- Use clear, descriptive variable names
- Add comments for complex logic
- Follow PEP 8 for Python code
- Test your changes before submitting

## 🔄 Development Workflow

1. **Fork** the repo
2. **Clone** your fork
3. **Create branch**: `git checkout -b feature-name`
4. **Make changes** and test
5. **Commit**: `git commit -m "Clear description"`
6. **Push**: `git push origin feature-name`
7. **Create PR** on GitHub

## 🆘 Getting Help

- 📖 Read the [Pull Request Guide](PULL_REQUEST_GUIDE.md)
- 💬 Ask questions in issues or PR comments
- 🔍 Check existing issues for similar problems
- 📧 Contact maintainers if needed

## 🏆 Recognition

All contributors will be:
- Listed in our contributors section
- Mentioned in release notes
- Thanked publicly for their work

## 📄 License

By contributing, you agree that your contributions will be licensed under the project's MIT License.

---

**Ready to contribute? Check out our [Pull Request Guide](PULL_REQUEST_GUIDE.md) to get started!** 🚀
