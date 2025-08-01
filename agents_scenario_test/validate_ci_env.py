#!/usr/bin/env python3
"""
CI Validation Script for Scenario-Based QA Tests

This script validates that the scenario test environment is properly configured
for CI/CD execution, similar to what happens in the GitHub Actions workflow.
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List


def check_environment_variables() -> Dict[str, bool]:
    """Check if required environment variables are set."""
    required_vars = [
        "OPENAI_API_KEY",
        "LANGWATCH_API_KEY",
        "DB_HOST",
        "DB_PORT", 
        "DB_USER",
        "DB_PASS",
        "DB_DATABASE"
    ]
    
    results = {}
    for var in required_vars:
        results[var] = var in os.environ and bool(os.environ[var])
    
    return results


def check_python_version() -> bool:
    """Check if Python version is compatible."""
    version = sys.version_info
    # Require Python 3.12+ (CI uses 3.13)
    return version.major >= 3 and version.minor >= 12


def check_dependencies() -> bool:
    """Check if required dependencies are installed."""
    try:
        import agno
        import scenario
        import pytest
        import psycopg
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        return False


def check_database_connection() -> bool:
    """Check if database connection works."""
    try:
        import psycopg
        
        # Get connection details from environment
        host = os.environ.get("DB_HOST", "localhost")
        port = os.environ.get("DB_PORT", "5432")
        user = os.environ.get("DB_USER", "ai")
        password = os.environ.get("DB_PASS", "ai")
        database = os.environ.get("DB_DATABASE", "ai")
        
        # Test connection
        conn_str = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        conn = psycopg.connect(conn_str)
        conn.close()
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False


def run_sample_test() -> bool:
    """Run a simple test to validate the setup."""
    try:
        # Change to the test directory
        test_dir = Path(__file__).parent
        
        # Run a single test to validate setup
        result = subprocess.run([
            "python", "-m", "pytest", 
            "test_task_completion.py::test_sage_knowledge_retrieval_task",
            "-v", "--tb=short"
        ], cwd=test_dir, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Sample test passed!")
            return True
        else:
            print("❌ Sample test failed:")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"Failed to run sample test: {e}")
        return False


def main():
    """Main validation function."""
    print("🔍 Validating CI Environment for Scenario-Based QA Tests")
    print("=" * 60)
    
    all_checks_passed = True
    
    # Check Python version
    print("🐍 Checking Python version...")
    if check_python_version():
        print(f"✅ Python {sys.version} is compatible")
    else:
        print(f"❌ Python {sys.version} is not compatible (requires 3.12+)")
        all_checks_passed = False
    
    print()
    
    # Check environment variables
    print("🔧 Checking environment variables...")
    env_results = check_environment_variables()
    for var, is_set in env_results.items():
        status = "✅" if is_set else "❌"
        print(f"{status} {var}: {'Set' if is_set else 'Not set'}")
        if not is_set:
            all_checks_passed = False
    
    print()
    
    # Check dependencies
    print("📦 Checking dependencies...")
    if check_dependencies():
        print("✅ All required dependencies are installed")
    else:
        print("❌ Missing required dependencies")
        all_checks_passed = False
    
    print()
    
    # Check database connection (only if env vars are set)
    if all(env_results[var] for var in ["DB_HOST", "DB_PORT", "DB_USER", "DB_PASS", "DB_DATABASE"]):
        print("🗄️ Checking database connection...")
        if check_database_connection():
            print("✅ Database connection successful")
        else:
            print("❌ Database connection failed")
            all_checks_passed = False
    else:
        print("⚠️ Skipping database check (missing environment variables)")
    
    print()
    
    # Run sample test (only if all other checks pass)
    if all_checks_passed:
        print("🧪 Running sample test...")
        if run_sample_test():
            print("✅ Sample test validation successful")
        else:
            print("❌ Sample test validation failed")
            all_checks_passed = False
    else:
        print("⚠️ Skipping sample test (prerequisite checks failed)")
    
    print()
    print("=" * 60)
    
    if all_checks_passed:
        print("🎉 All validations passed! Environment is ready for CI.")
        return 0
    else:
        print("💥 Some validations failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
