#!/usr/bin/env python3
"""
Test runner script for agent validation tests.
Usage: python test_runner.py [--agent=sage|scholar|all] [--category=behavior|safety|integration|all]
"""

import argparse
import asyncio
import sys
from pathlib import Path

# Add the parent directory to sys.path to import agents
sys.path.append(str(Path(__file__).parent.parent))


def run_tests(agent_filter: str = "all", category_filter: str = "all", verbose: bool = False):
    """Run the agent test suite with specified filters."""
    
    try:
        import pytest
    except ImportError:
        print("pytest is required to run tests. Please install it with: pip install pytest pytest-asyncio")
        return 1
    
    # Build pytest arguments
    pytest_args = []
    
    # Set verbosity
    if verbose:
        pytest_args.extend(["-v", "-s"])
    
    # Add test markers based on filters
    if agent_filter != "all":
        pytest_args.extend(["-k", f"{agent_filter}"])
    
    if category_filter != "all":
        test_file_map = {
            "behavior": "test_agentic_behavior.py",
            "safety": "test_quality_safety.py", 
            "integration": "test_integration.py"
        }
        if category_filter in test_file_map:
            pytest_args.append(test_file_map[category_filter])
    
    # Add the test directory
    test_dir = Path(__file__).parent
    pytest_args.append(str(test_dir))
    
    # Run pytest
    result = pytest.main(pytest_args)
    return result


def main():
    parser = argparse.ArgumentParser(description="Run agent validation tests")
    parser.add_argument(
        "--agent", 
        choices=["sage", "scholar", "all"],
        default="all",
        help="Which agent to test (default: all)"
    )
    parser.add_argument(
        "--category",
        choices=["behavior", "safety", "integration", "all"],
        default="all", 
        help="Which test category to run (default: all)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    print(f"Running agent tests for: {args.agent} agent(s), {args.category} category")
    print("-" * 60)
    
    result = run_tests(
        agent_filter=args.agent,
        category_filter=args.category,
        verbose=args.verbose
    )
    
    if result == 0:
        print("\n✅ All tests passed!")
    else:
        print(f"\n❌ Tests failed with exit code: {result}")
    
    return result


if __name__ == "__main__":
    sys.exit(main())
