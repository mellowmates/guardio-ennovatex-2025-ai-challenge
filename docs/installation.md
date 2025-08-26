# Installation Guide

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10, macOS 10.14, or Ubuntu 18.04+
- **Python**: Version 3.8 or higher
- **RAM**: 2GB available memory
- **Storage**: 100MB free space
- **Internet**: Required only for initial package downloads

### Recommended Specifications
- **Operating System**: Latest versions of Windows 11, macOS, or Ubuntu
- **Python**: Version 3.10 or higher
- **RAM**: 4GB or more
- **Storage**: 500MB free space
- **Permissions**: Admin/sudo access for package installation

## Installation Steps

### 1. Clone the Repository

```bash
# Using HTTPS
git clone https://github.com/mellowmates/Guardio.git

# Or using SSH (if configured)
git clone git@github.com:mellowmates/Guardio.git

# Navigate to project directory
cd Guardio
```

### 2. Create Virtual Environment

#### On Windows:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment

venv\Scripts\activate

```

#### On Linux/macOS:
```


# Create virtual environment

python3 -m venv venv

# Activate virtual environment

source venv/bin/activate

```

### 3. Install Dependencies

```


# Upgrade pip (recommended)

python -m pip install --upgrade pip

# Install required packages

pip install customtkinter pynput numpy psutil

# Or install from requirements file (if available)

pip install -r requirements.txt

```

### 4. Verify Installation

```


# Check Python version

python --version

# Verify package installations

python -c "import customtkinter, pynput, numpy, psutil; print('All packages installed successfully')"

```

### 5. Run Guardio

```


# From project root directory

python src/main.py

```

## Package Dependencies

### Core Dependencies
- **customtkinter** (≥5.0.0): Modern UI framework
- **pynput** (≥1.7.0): Keyboard and mouse monitoring
- **numpy** (≥1.21.0): Numerical computations
- **psutil** (≥5.8.0): System and process utilities

### Optional Dependencies
- **pillow** (≥8.0.0): Image processing for enhanced UI
- **matplotlib** (≥3.5.0): Data visualization (future features)

## Platform-Specific Notes

### Windows
- **Permissions**: May require "Run as Administrator" for keyboard monitoring
- **Antivirus**: Add Guardio folder to antivirus exclusions if needed
- **Python Path**: Ensure Python is added to system PATH

### macOS
- **Privacy Settings**: Grant accessibility permissions when prompted
- **Gatekeeper**: May need to allow Guardio in Security & Privacy settings
- **Homebrew**: Consider using Homebrew for Python installation

### Linux
- **X11**: Requires X11 display server (standard on most distributions)
- **Permissions**: May need to add user to input group
- **Package Manager**: Install python3-pip if not available

## Troubleshooting

### Common Installation Issues

#### Python Version Mismatch
```


# Check available Python versions

python --version
python3 --version

# Use specific version if needed

python3.10 -m venv venv

```

#### Permission Denied Errors
```


# On Linux/macOS, use sudo for system-wide installation (not recommended)

# Better: Fix virtual environment permissions

chmod -R 755 venv/

```

#### Package Installation Failures
```


# Clear pip cache

pip cache purge

# Install with verbose output for debugging

pip install -v customtkinter

# Use alternative index if needed

pip install -i https://pypi.org/simple/ customtkinter

```

#### Runtime Errors

1. **"Module not found" errors**:
   - Ensure virtual environment is activated
   - Verify packages installed in correct environment

2. **Permission errors on startup**:
   - Grant necessary system permissions
   - Run with appropriate privileges

3. **Display issues**:
   - Check display server compatibility
   - Verify graphics drivers

### Performance Optimization

#### For Better Performance
```


# Install optimized numpy (if available)

pip install numpy[mkl]

# Use Python 3.10+ for better performance

# Enable hardware acceleration where available

```

#### Memory Usage
- Close unnecessary applications
- Increase virtual memory if needed
- Monitor system resources during initial learning

## Development Setup

### For Contributors
```


# Install development dependencies

pip install pytest black flake8 mypy

# Run tests (if available)

python -m pytest tests/

# Code formatting

black src/

# Type checking

mypy src/

```

### Building from Source
```


# Clone development branch

git clone -b develop https://github.com/mellowmates/Guardio.git

# Install in editable mode

pip install -e .

```

## Uninstallation

### Complete Removal
```


# Deactivate virtual environment

deactivate

# Remove project directory

rm -rf Guardio/  \# Linux/macOS
rmdir /s Guardio  \# Windows

# Remove Python packages (if installed globally)

pip uninstall customtkinter pynput numpy psutil

```

## Support

For installation issues:
1. Check [GitHub Issues](https://github.com/mellowmates/Guardio/issues)
2. Create new issue with system details
3. Include error messages and system configuration

---

**Installation Guide by Vishwajith Chakravarthy**  
**Dev Dream Team - Samsung EnnovateX 2025**
```
