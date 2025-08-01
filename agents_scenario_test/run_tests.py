#!/usr/bin/env python3
"""
Test runner script for agent scenario validation tests.
Usage: python run_tests.py [--category=task|tool|flow|hallucination|integration|all] [--agent=sage|scholar|all] [--verbose]
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_tests(category: str = "all", agent_filter: str = "all", verbose: bool = False):
    """Run the agent scenario test suite with specified filters."""
    
    # Build pytest command
    cmd = ["pytest"]
    
    # Set verbosity
    if verbose:
        cmd.extend(["-v", "-s"])
    
    # Add test file based on category
    if category != "all":
        test_file_map = {
            "task": "test_task_completion.py",
            "tool": "test_tool_interaction.py", 
            "flow": "test_conversational_flow.py",
            "hallucination": "test_hallucination_detection.py",
            "integration": "test_integration.py"
        }
        if category in test_file_map:
            cmd.append(test_file_map[category])
    
    # Add agent filter
    if agent_filter != "all":
        cmd.extend(["-k", agent_filter])
    
    # Add markers
    cmd.extend(["-m", "agent_test"])
    
    # Add current directory if no specific files
    if category == "all":
        cmd.append(".")
    
    print(f"Running command: {' '.join(cmd)}")
    print("-" * 60)
    
    # Change to test directory
    test_dir = Path(__file__).parent
    
    # Create test results directory if it doesn't exist
    results_dir = test_dir / "test-results"
    results_dir.mkdir(exist_ok=True)
    
    # Add JUnit XML output for CI
    cmd.extend(["--junitxml", str(results_dir / "junit.xml")])
    
    # Add HTML report if pytest-html is available
    try:
        import pytest_html  # noqa: F401
        cmd.extend(["--html", str(results_dir / "report.html"), "--self-contained-html"])
    except ImportError:
        pass
    
    # Run pytest
    result = subprocess.run(cmd, cwd=test_dir)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="Run agent scenario validation tests")
    parser.add_argument(
        "--category", 
        choices=["task", "tool", "flow", "hallucination", "integration", "all"],
        default="all",
        help="Which test category to run (default: all)"
    )
    parser.add_argument(
        "--agent",
        choices=["sage", "scholar", "all"],
        default="all",
        help="Which agent to test (default: all)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    print(f"Running agent scenario tests:")
    print(f"  Category: {args.category}")
    print(f"  Agent: {args.agent}")
    print(f"  Verbose: {args.verbose}")
    print("=" * 60)
    
    result = run_tests(
        category=args.category,
        agent_filter=args.agent,
        verbose=args.verbose
    )
    
    if result == 0:
        print("\n✅ All tests passed!")
    else:
        print(f"\n❌ Tests failed with exit code: {result}")
    
    return result


if __name__ == "__main__":
    sys.exit(main())
