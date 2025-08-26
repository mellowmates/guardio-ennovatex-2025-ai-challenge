# Contributing Guidelines

Welcome to the Guardio project! We appreciate your interest in contributing to our adaptive anomaly detection system.

## Development Team

- **Omprakash Panda** - AI/ML Development & Project Lead
- **Sindhu B L** - UI Development & Design  
- **Vittal G B** - Backend Integration & Threading
- **Vishwajith Chakravarthy** - Testing, Documentation & Presentation

## Getting Started

### Development Setup

1. **Fork the Repository**
```bash
# Click "Fork" on GitHub, then clone your fork
git clone https://github.com/yourusername/Guardio.git
cd Guardio
```

2. **Set Up Development Environment**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install development tools
pip install pytest black flake8 mypy
```

3. **Create Feature Branch**
```bash
git checkout -b feature/your-feature-name
```

## Code Standards

### Python Style Guide
- Follow **PEP 8** style guidelines
- Use **4 spaces** for indentation
- Maximum **line length: 88 characters** (Black formatter standard)
- Use **descriptive variable names**

### Code Formatting
```bash
# Format code with Black
black src/

# Check style with flake8
flake8 src/

# Type checking with mypy
mypy src/
```

### Documentation Standards
- Add **docstrings** to all public functions and classes
- Use **Google-style docstrings**
- Update **API documentation** for new features
- Include **inline comments** for complex logic

### Example Function Documentation
```python
def update_risk_score(self, risk_score: int) -> None:
    """Update the security risk score display.

    Args:
        risk_score: Integer risk score value between 0 and 15.
        
    Returns:
        None
        
    Raises:
        ValueError: If risk_score is outside valid range.
    """
```

## Areas for Contribution

### 🔧 Core Development
- **New Detection Agents**: Implement additional behavioral monitoring
- **Algorithm Improvements**: Enhance statistical analysis methods
- **Performance Optimization**: Improve system efficiency
- **Cross-platform Support**: Expand OS compatibility

### 🎨 UI/UX Enhancements
- **Samsung One UI Features**: Additional design elements
- **Accessibility**: Improve interface accessibility
- **Data Visualization**: Enhanced metrics display
- **User Experience**: Interface usability improvements

### 📊 Analytics & Insights
- **Advanced Metrics**: Additional statistical measures
- **Reporting Features**: Generate usage reports
- **Data Export**: Export monitoring data
- **Trend Analysis**: Long-term pattern analysis

### 🧪 Testing & Quality
- **Unit Tests**: Expand test coverage
- **Integration Tests**: Test component interactions
- **Performance Tests**: Benchmark system performance
- **Security Testing**: Validate privacy protection

### 📚 Documentation
- **User Guides**: Improve user documentation
- **API Documentation**: Expand technical documentation
- **Tutorials**: Create usage tutorials
- **Translation**: Multi-language support

## Contribution Process

### 1. Issue Discussion
- **Check existing issues** before creating new ones
- **Propose new features** through issue discussion
- **Get consensus** on implementation approach
- **Assign yourself** to issues you plan to work on

### 2. Development Workflow
```bash
# Keep your fork updated
git remote add upstream https://github.com/devdreamteam/Guardio.git
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature

# Make your changes
# ... develop and test ...

# Commit changes
git add .
git commit -m "feat: add new detection agent for network behavior"

# Push to your fork
git push origin feature/your-feature
```

### 3. Commit Message Convention
Use **conventional commits** format:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code formatting
- `refactor:` Code restructuring
- `test:` Test additions
- `chore:` Maintenance tasks

### 4. Pull Request Guidelines
- **Clear title** describing the change
- **Detailed description** of what and why
- **Link related issues** using "Fixes #123"
- **Include tests** for new functionality
- **Update documentation** as needed
- **Ensure CI passes** all checks

## Testing Requirements

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=src tests/

# Run specific test file
python -m pytest tests/test_agents.py
```

### Writing Tests
- **Unit tests** for individual functions
- **Integration tests** for component interactions
- **Mock external dependencies** (keyboard, mouse)
- **Test edge cases** and error conditions

### Test Structure
```python
import pytest
from src.agents.typing_agent import TypingAgent

class TestTypingAgent:
    def setup_method(self):
        """Set up test fixtures."""
        self.agent = TypingAgent(None, None)

    def test_initialization(self):
        """Test agent initialization."""
        assert self.agent.sensitivity == 3.0
        assert self.agent.cooldown == 3.0
```

## Code Review Process

### For Contributors
- **Self-review** code before submitting
- **Respond promptly** to review feedback
- **Make requested changes** in same branch
- **Resolve conflicts** with main branch

### Review Criteria
- **Functionality**: Does it work as intended?
- **Code Quality**: Clean, readable, maintainable?
- **Performance**: Efficient implementation?
- **Security**: No privacy or security issues?
- **Documentation**: Adequately documented?

## Community Guidelines

### Communication
- **Be respectful** and professional
- **Provide constructive feedback**
- **Ask questions** when unclear
- **Help others** learn and improve

### Issue Reporting
Include the following information:
- **Operating System** and version
- **Python version** and environment
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Error messages** and logs

### Feature Requests
- **Describe the use case** clearly
- **Explain the benefits** to users
- **Consider implementation complexity**
- **Discuss alternatives** if applicable

## Recognition

Contributors will be recognized in:
- **README.md** contributor section
- **Release notes** for significant contributions
- **GitHub contributors** page
- **Documentation credits**

## Getting Help

- **GitHub Issues**: Technical questions and bug reports
- **Documentation**: Comprehensive guides in `/docs`
- **Code Examples**: Reference existing implementations
- **Team Contact**: Reach out to maintainers for guidance

## License

By contributing to Guardio, you agree that your contributions will be licensed under the same MIT License that covers the project.

---

**Thank you for contributing to Guardio!**

**Dev Dream Team - Samsung EnnovateX 2025**

