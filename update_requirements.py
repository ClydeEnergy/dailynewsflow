#!/usr/bin/env python3
"""
Requirements Update Script for Daily News Flow
Helps maintain up-to-date and secure dependencies
"""

import subprocess
import sys
import os

def run_command(command):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_pip_tools():
    """Check if pip-tools is installed."""
    success, _, _ = run_command("pip show pip-tools")
    if not success:
        print("Installing pip-tools...")
        success, _, _ = run_command("pip install pip-tools")
        if not success:
            print("Failed to install pip-tools")
            return False
    return True

def update_requirements():
    """Update all requirements files."""
    print("🔄 Updating Daily News Flow Requirements...")
    
    # Check current environment
    success, output, _ = run_command("pip list --outdated")
    if success and output:
        print("📦 Outdated packages found:")
        print(output)
    else:
        print("✅ All packages are up to date!")
    
    # Run security check if pip-audit is available
    success, _, _ = run_command("pip show pip-audit")
    if success:
        print("\n🔒 Running security audit...")
        success, output, error = run_command("pip-audit")
        if success:
            print("✅ No security vulnerabilities found!")
        else:
            print("⚠️  Security issues found:")
            print(error)
    
    # Check for dependency conflicts
    print("\n🔍 Checking for dependency conflicts...")
    success, output, error = run_command("pip check")
    if success:
        print("✅ No dependency conflicts found!")
    else:
        print("⚠️  Dependency conflicts found:")
        print(error)
    
    print("\n✨ Requirements check complete!")
    print("\n💡 To update packages:")
    print("   1. Update version numbers in requirements files")
    print("   2. Test thoroughly in development")
    print("   3. Run this script again to verify")

if __name__ == "__main__":
    print("Daily News Flow - Requirements Manager")
    print("=" * 40)
    
    # Verify we're in the right directory
    if not os.path.exists("requirements.txt"):
        print("❌ Error: requirements.txt not found!")
        print("   Please run this script from the project root directory.")
        sys.exit(1)
    
    update_requirements()
