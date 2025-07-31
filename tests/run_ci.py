#!/usr/bin/env python3
"""
CI/CD entry point for agentic AI testing.
This script is designed to be called from GitHub Actions, Jenkins, or other CI systems.
"""

import asyncio
import sys
import os
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tests.test_suites import (
    run_ci_test_suite,
    run_sage_agent_tests,
    run_team_tests,
    run_system_integration_tests,
    run_performance_tests
)


def setup_logging():
    """Setup logging for CI environment"""
    import logging
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('test_execution.log')
        ]
    )


async def main():
    """Main CI entry point"""
    parser = argparse.ArgumentParser(description='Agentic AI Test Framework CI Runner')
    parser.add_argument(
        '--test-type',
        choices=['ci', 'sage', 'teams', 'system', 'performance', 'all'],
        default='ci',
        help='Type of tests to run'
    )
    parser.add_argument(
        '--severity',
        choices=['critical', 'high', 'medium', 'low'],
        nargs='*',
        help='Filter tests by severity'
    )
    parser.add_argument(
        '--fail-fast',
        action='store_true',
        help='Stop on first test failure'
    )
    parser.add_argument(
        '--output-dir',
        default='test_results',
        help='Directory to save test results'
    )
    parser.add_argument(
        '--generate-datasets',
        action='store_true',
        help='Generate default golden datasets before testing'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    
    print("🤖 Agentic AI Test Framework - CI Runner")
    print("=" * 50)
    print(f"Test Type: {args.test_type}")
    print(f"Output Directory: {args.output_dir}")
    print(f"Fail Fast: {args.fail_fast}")
    
    # Generate datasets if requested
    if args.generate_datasets:
        print("📊 Generating golden datasets...")
        from tests.framework.fixtures import save_default_datasets
        save_default_datasets(f"{args.output_dir}/datasets")
        print("✅ Golden datasets generated")
    
    # Set environment variables for test configuration
    os.environ['TEST_OUTPUT_DIR'] = args.output_dir
    os.environ['TEST_FAIL_FAST'] = str(args.fail_fast)
    
    try:
        exit_code = 0
        
        if args.test_type == 'ci':
            exit_code = await run_ci_test_suite()
        
        elif args.test_type == 'sage':
            results = await run_sage_agent_tests()
            exit_code = 0 if results['summary']['failed'] == 0 else 1
        
        elif args.test_type == 'teams':
            results = await run_team_tests()
            exit_code = 0 if results['summary']['failed'] == 0 else 1
        
        elif args.test_type == 'system':
            results = await run_system_integration_tests()
            exit_code = 0 if results['summary']['failed'] == 0 else 1
        
        elif args.test_type == 'performance':
            results = await run_performance_tests()
            exit_code = 0 if results['summary']['failed'] == 0 else 1
        
        elif args.test_type == 'all':
            print("🧪 Running all test suites...")
            
            sage_results = await run_sage_agent_tests()
            team_results = await run_team_tests()
            system_results = await run_system_integration_tests()
            perf_results = await run_performance_tests()
            
            total_failed = (
                sage_results['summary']['failed'] +
                team_results['summary']['failed'] +
                system_results['summary']['failed'] +
                perf_results['summary']['failed']
            )
            
            exit_code = 0 if total_failed == 0 else 1
        
        print(f"\n{'✅' if exit_code == 0 else '❌'} Tests completed with exit code: {exit_code}")
        return exit_code
        
    except Exception as e:
        print(f"❌ Test execution failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
