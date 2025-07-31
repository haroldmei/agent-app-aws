"""
Example test suites using the agentic AI test framework.
"""

import asyncio
from typing import List

from agents.sage import get_sage
from agents.scholar import get_scholar
from teams.finance_researcher import get_finance_researcher_team
from teams.multi_language import get_multi_language_team

from framework.implementations import (
    RAGValidationTest, 
    AgentBehaviorTest, 
    TeamOrchestrationTest,
    QualitySafetyTest,
    SystemIntegrationTest
)
from framework.fixtures import TestDataFactory, create_default_golden_datasets
from framework.runners import TestRunner, CIRunner
from framework.base import TestSeverity, TestCategory


async def run_sage_agent_tests():
    """Run comprehensive tests for Sage agent"""
    print("🧙‍♂️ Running Sage Agent Tests...")
    
    # Get sage agent
    sage = get_sage(debug_mode=True)
    
    # Create test data
    rag_test_data = TestDataFactory.create_rag_test_data()
    behavior_test_data = TestDataFactory.create_agent_behavior_test_data()
    safety_test_data = TestDataFactory.create_quality_safety_test_data()
    
    # Create tests
    tests = []
    
    # RAG validation tests
    for test_data in rag_test_data:
        tests.append(RAGValidationTest(sage, test_data))
    
    # Agent behavior tests
    for test_data in behavior_test_data:
        tests.append(AgentBehaviorTest(sage, test_data))
    
    # Quality & safety tests
    for test_data in safety_test_data:
        tests.append(QualitySafetyTest(sage, test_data))
    
    # Run tests
    runner = TestRunner(output_dir="test_results/sage")
    results = await runner.run_tests(tests)
    
    print(f"✅ Sage tests completed: {results['summary']['passed']}/{results['summary']['total_tests']} passed")
    return results


async def run_team_tests():
    """Run comprehensive tests for teams"""
    print("👥 Running Team Tests...")
    
    # Get teams
    finance_team = get_finance_researcher_team(debug_mode=True)
    language_team = get_multi_language_team(debug_mode=True)
    
    # Create test data
    team_test_data = TestDataFactory.create_team_orchestration_test_data()
    
    tests = []
    
    # Finance team tests
    finance_data = [data for data in team_test_data if data.metadata.get("domain") == "finance"]
    for test_data in finance_data:
        tests.append(TeamOrchestrationTest(finance_team, test_data))
    
    # Language team tests
    language_data = [data for data in team_test_data if data.metadata.get("domain") == "language"]
    for test_data in language_data:
        tests.append(TeamOrchestrationTest(language_team, test_data))
    
    # Run tests
    runner = TestRunner(output_dir="test_results/teams")
    results = await runner.run_tests(tests)
    
    print(f"✅ Team tests completed: {results['summary']['passed']}/{results['summary']['total_tests']} passed")
    return results


async def run_system_integration_tests():
    """Run end-to-end system integration tests"""
    print("🔗 Running System Integration Tests...")
    
    # Get all agents and teams
    agents = [
        get_sage(debug_mode=True),
        get_scholar(debug_mode=True)
    ]
    
    teams = [
        get_finance_researcher_team(debug_mode=True),
        get_multi_language_team(debug_mode=True)
    ]
    
    # Define integration scenarios
    scenarios = [
        {
            "name": "research_and_report",
            "description": "Research a topic and generate a comprehensive report",
            "steps": [
                {
                    "type": "agent",
                    "agent": "Sage",
                    "message": "Research the latest developments in artificial intelligence",
                    "name": "research_step"
                },
                {
                    "type": "team",
                    "team": "finance_researcher",
                    "message": "Generate a financial impact analysis of AI developments",
                    "name": "analysis_step"
                }
            ],
            "expected_outcomes": {
                "max_execution_time": 120,
                "deliverables": ["research_summary", "financial_analysis"]
            }
        },
        {
            "name": "multilingual_processing",
            "description": "Process content in multiple languages",
            "steps": [
                {
                    "type": "agent",
                    "agent": "Scholar",
                    "message": "Analyze this text for key insights: [sample text]",
                    "name": "analysis_step"
                },
                {
                    "type": "team",
                    "team": "multi_language",
                    "message": "Translate the analysis to Spanish and French",
                    "name": "translation_step"
                }
            ],
            "expected_outcomes": {
                "max_execution_time": 90,
                "deliverables": ["analysis", "spanish_translation", "french_translation"]
            }
        }
    ]
    
    tests = []
    for scenario in scenarios:
        tests.append(SystemIntegrationTest(agents, teams, scenario))
    
    # Run tests
    runner = TestRunner(output_dir="test_results/system")
    results = await runner.run_tests(tests)
    
    print(f"✅ System integration tests completed: {results['summary']['passed']}/{results['summary']['total_tests']} passed")
    return results


async def run_ci_test_suite():
    """Run the full CI test suite"""
    print("🚀 Running CI Test Suite...")
    
    # Get all agents and teams
    sage = get_sage(debug_mode=True)
    scholar = get_scholar(debug_mode=True)
    finance_team = get_finance_researcher_team(debug_mode=True)
    language_team = get_multi_language_team(debug_mode=True)
    
    # Create comprehensive test suite
    all_tests = []
    
    # Critical tests (must pass for release)
    golden_datasets = create_default_golden_datasets()
    
    # RAG validation (critical)
    for test_data in golden_datasets["rag_validation"].test_cases:
        test = RAGValidationTest(sage, test_data)
        test.severity = TestSeverity.CRITICAL
        all_tests.append(test)
    
    # Quality & safety (critical)
    for test_data in golden_datasets["quality_safety"].test_cases:
        test = QualitySafetyTest(sage, test_data)
        test.severity = TestSeverity.CRITICAL
        all_tests.append(test)
    
    # Agent behavior (high priority)
    for test_data in golden_datasets["agent_behavior"].test_cases:
        all_tests.append(AgentBehaviorTest(sage, test_data))
        all_tests.append(AgentBehaviorTest(scholar, test_data))
    
    # Team orchestration (high priority)
    for test_data in golden_datasets["team_orchestration"].test_cases:
        if test_data.metadata.get("domain") == "finance":
            all_tests.append(TeamOrchestrationTest(finance_team, test_data))
        elif test_data.metadata.get("domain") == "language":
            all_tests.append(TeamOrchestrationTest(language_team, test_data))
    
    # System integration (critical)
    integration_scenario = {
        "name": "core_functionality",
        "description": "Test core system functionality",
        "steps": [
            {
                "type": "agent",
                "agent": "Sage",
                "message": "What is machine learning?",
                "name": "knowledge_query"
            }
        ],
        "expected_outcomes": {
            "max_execution_time": 30
        }
    }
    all_tests.append(SystemIntegrationTest([sage, scholar], [finance_team, language_team], integration_scenario))
    
    # CI configuration
    ci_config = {
        "required_severities": [TestSeverity.CRITICAL, TestSeverity.HIGH],
        "fail_fast": False,
        "min_pass_rate": 0.95,
        "max_critical_failures": 0,
        "max_high_failures": 2,
        "performance_thresholds": {
            "max_avg_execution_time": 20.0,
            "max_total_execution_time": 300.0
        }
    }
    
    # Run CI tests
    runner = TestRunner(output_dir="test_results/ci")
    ci_runner = CIRunner(runner)
    
    exit_code = await ci_runner.run_ci_tests(all_tests, ci_config)
    
    if exit_code == 0:
        print("🎉 CI Test Suite PASSED - Ready for deployment!")
    else:
        print("❌ CI Test Suite FAILED - Review issues before deployment")
    
    return exit_code


async def run_performance_tests():
    """Run performance and load tests"""
    print("⚡ Running Performance Tests...")
    
    sage = get_sage(debug_mode=True)
    
    # Performance test data
    perf_tests = []
    
    # Latency tests
    for i in range(5):
        test_data = TestDataFactory.create_performance_test_data()[0]  # Latency test
        test_data.input_data["query"] = f"Performance test query {i+1}"
        perf_tests.append(RAGValidationTest(sage, test_data))
    
    # Run performance tests
    runner = TestRunner(output_dir="test_results/performance")
    results = await runner.run_tests(
        perf_tests,
        filter_category=[TestCategory.PERFORMANCE]
    )
    
    # Calculate performance metrics
    avg_time = results["metrics"]["performance"]["avg_execution_time"]
    total_time = results["metrics"]["performance"]["total_execution_time"]
    
    print(f"⚡ Performance Results:")
    print(f"   Average Execution Time: {avg_time:.2f}s")
    print(f"   Total Execution Time: {total_time:.2f}s")
    print(f"   Tests Passed: {results['summary']['passed']}/{results['summary']['total_tests']}")
    
    return results


if __name__ == "__main__":
    import sys
    
    async def main():
        if len(sys.argv) > 1:
            test_type = sys.argv[1].lower()
            
            if test_type == "sage":
                await run_sage_agent_tests()
            elif test_type == "teams":
                await run_team_tests()
            elif test_type == "system":
                await run_system_integration_tests()
            elif test_type == "ci":
                exit_code = await run_ci_test_suite()
                sys.exit(exit_code)
            elif test_type == "performance":
                await run_performance_tests()
            else:
                print("Unknown test type. Available: sage, teams, system, ci, performance")
        else:
            # Run all tests
            print("🧪 Running All Test Suites...")
            await run_sage_agent_tests()
            await run_team_tests()
            await run_system_integration_tests()
            await run_performance_tests()
            
            print("\n🏁 All test suites completed!")
    
    asyncio.run(main())
