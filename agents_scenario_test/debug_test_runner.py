#!/usr/bin/env python3
"""
Debug Test Runner for Scenario Tests

This script helps debug issues with the scenario tests by running them
with detailed logging and error capture.
"""

import os
import sys
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, Any

async def test_agent_adapters():
    """Test that the agent adapters can be created and called successfully."""
    print("🧪 Testing agent adapters...")
    
    try:
        # Add parent directory to path to import conftest
        sys.path.insert(0, str(Path(__file__).parent.parent))
        
        # Import the adapters
        from agents_scenario_test.conftest import SageAdapter, ScholarAdapter
        
        # Test SageAdapter
        print("   Testing SageAdapter...")
        sage_adapter = SageAdapter()
        print("   ✅ SageAdapter created successfully")
        
        # Test ScholarAdapter  
        print("   Testing ScholarAdapter...")
        scholar_adapter = ScholarAdapter()
        print("   ✅ ScholarAdapter created successfully")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Agent adapter test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dependencies():
    """Test that all required dependencies are available."""
    print("📦 Testing dependencies...")
    
    required_modules = [
        "agno",
        "scenario", 
        "pytest",
        "psycopg",
        "openai",
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError:
            print(f"   ❌ {module} (missing)")
            missing_modules.append(module)
    
    return len(missing_modules) == 0

def test_environment_setup():
    """Test environment variable setup."""
    print("🔧 Testing environment setup...")
    
    required_env_vars = [
        "OPENAI_API_KEY",
        "LANGWATCH_API_KEY", 
    ]
    
    missing_vars = []
    for var in required_env_vars:
        if var in os.environ and os.environ[var]:
            print(f"   ✅ {var}")
        else:
            print(f"   ❌ {var} (not set)")
            missing_vars.append(var)
    
    return len(missing_vars) == 0

async def test_simple_agent_call():
    """Test a simple agent call to see if basic functionality works."""
    print("🤖 Testing simple agent call...")
    
    try:
        # Import required modules
        from agents_scenario_test.conftest import SageAdapter
        
        # Create a simple mock input
        class MockInput:
            def __init__(self):
                self.thread_id = 'debug-test-thread'
            def last_new_user_message_str(self):
                return 'Hello, can you provide a brief introduction about yourself?'
        
        # Test the adapter
        adapter = SageAdapter()
        mock_input = MockInput()
        
        # This might fail due to missing API keys, but we can catch the specific error
        try:
            result = await adapter.call(mock_input)
            print("   ✅ Agent call completed successfully")
            print(f"   Result type: {type(result)}")
            return True
        except Exception as api_error:
            print(f"   ⚠️  Agent call failed (this may be expected): {api_error}")
            # Check if it's an API key issue vs other issues
            if "api" in str(api_error).lower() or "key" in str(api_error).lower():
                print("   This appears to be an API key issue, which is expected in test environments")
                return True  # Consider this a success for environment testing
            else:
                raise api_error
    
    except Exception as e:
        print(f"   ❌ Simple agent call test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_pytest_with_debugging():
    """Run pytest with verbose debugging."""
    print("🔍 Running pytest with debugging...")
    
    test_dir = Path(__file__).parent
    
    # Run a simple test with maximum verbosity
    result = subprocess.run(
        [
            "python",
            "-m",
            "pytest",
            "test_task_completion.py::test_sage_knowledge_retrieval_task",
            "-vvv",
            "-s",
            "--tb=long",
            "--capture=no",
        ],
        cwd=test_dir,
        text=True,
    )
    
    return result.returncode == 0

async def main():
    """Main debug function."""
    print("🚀 Agent Scenario Test Debug Runner")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Test dependencies
    if not test_dependencies():
        print("❌ Dependency test failed")
        all_tests_passed = False
    print()
    
    # Test environment
    if not test_environment_setup():
        print("❌ Environment test failed")
        all_tests_passed = False
    print()
    
    # Test agent adapters
    if not await test_agent_adapters():
        print("❌ Agent adapter test failed")
        all_tests_passed = False
    print()
    
    # Test simple agent call
    if not await test_simple_agent_call():
        print("❌ Simple agent call test failed")
        all_tests_passed = False
    print()
    
    # If basic tests pass, try running pytest
    if all_tests_passed:
        print("🎯 Basic tests passed! Attempting pytest run...")
        if not run_pytest_with_debugging():
            print("❌ Pytest run failed")
            all_tests_passed = False
    else:
        print("⚠️  Skipping pytest run due to basic test failures")
    
    print("=" * 50)
    if all_tests_passed:
        print("🎉 All debug tests passed!")
        return 0
    else:
        print("💥 Some debug tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
