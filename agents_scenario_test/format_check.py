#!/usr/bin/env python3
"""
Format Check Script for Scenario Tests

This script helps validate and fix formatting issues in the scenario test files.
It can be used locally before pushing to ensure CI formatting checks pass.
"""

import subprocess
import sys
from pathlib import Path


def check_formatting() -> bool:
    """Check if files need formatting using ruff."""
    try:
        result = subprocess.run(
            ["python", "-m", "ruff", "format", ".", "--check"],
            capture_output=True,
            text=True,
        )
        
        if result.returncode == 0:
            print("✅ All files are properly formatted!")
            return True
        else:
            print("❌ Some files need formatting:")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except FileNotFoundError:
        print("⚠️ ruff not found. Install with: pip install ruff")
        return False
    except Exception as e:
        print(f"Error checking formatting: {e}")
        return False


def apply_formatting() -> bool:
    """Apply formatting to all files using ruff."""
    try:
        result = subprocess.run(
            ["python", "-m", "ruff", "format", "."],
            capture_output=True,
            text=True,
        )
        
        if result.returncode == 0:
            print("✅ Formatting applied successfully!")
            print(result.stdout)
            return True
        else:
            print("❌ Error applying formatting:")
            print(result.stderr)
            return False
            
    except FileNotFoundError:
        print("⚠️ ruff not found. Install with: pip install ruff")
        return False
    except Exception as e:
        print(f"Error applying formatting: {e}")
        return False


def main():
    """Main function."""
    if len(sys.argv) > 1 and sys.argv[1] == "--fix":
        print("🔧 Applying formatting fixes...")
        success = apply_formatting()
        if success:
            print("🔄 Checking formatting after fixes...")
            check_formatting()
    else:
        print("🔍 Checking file formatting...")
        success = check_formatting()
        if not success:
            print("\n💡 To fix formatting issues, run:")
            print("    python format_check.py --fix")
            print("    # or")
            print("    python -m ruff format .")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
