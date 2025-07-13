# Requirements Management

This project uses multiple requirements files for different environments:

## Files Overview

### `requirements.txt` - Base Requirements
- Core dependencies needed for the application to run
- Suitable for development and testing
- Includes Django, database drivers, and essential packages

### `requirements-dev.txt` - Development Requirements  
- Includes all base requirements plus development tools
- Testing frameworks, code quality tools, debugging utilities
- Install with: `pip install -r requirements-dev.txt`

### `requirements-prod.txt` - Production Requirements
- Optimized for production deployment
- Includes performance and security enhancements
- Excludes development-only tools

## Installation Instructions

### For Development:
```bash
pip install -r requirements-dev.txt
```

### For Production:
```bash
pip install -r requirements-prod.txt
```

### For Basic Setup:
```bash
pip install -r requirements.txt
```

## Package Versions

All packages are pinned to specific versions for reproducible builds. 
Versions are updated regularly and tested for compatibility.

### Key Dependencies:
- **Django 5.1.6**: Latest stable Django framework
- **mysqlclient 2.2.7**: MySQL database adapter
- **djangorestframework 3.16.0**: REST API framework
- **Pillow 11.0.0**: Image processing library
- **requests 2.32.3**: HTTP library for API calls

## Updating Requirements

1. Install new packages in your virtual environment
2. Update the appropriate requirements file(s)
3. Test thoroughly before committing
4. Run `pip check` to verify no conflicts exist

## Security

- All packages are kept up-to-date with latest security patches
- Use `pip-audit` to check for known vulnerabilities
- Review package changelogs before updating major versions
