"""
Test runners and CI/CD integration for the agentic AI test framework.
"""

import asyncio
import json
import time
from typing import List, Dict, Any, Optional, Type
from pathlib import Path
from dataclasses import asdict
import logging

from .base import BaseTest, TestResult, TestSeverity, TestCategory
from .metrics import MetricResult


class TestRunner:
    """Main test runner for executing agentic AI tests"""
    
    def __init__(self, output_dir: str = "test_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(__name__)
    
    async def run_tests(self, tests: List[BaseTest], 
                       filter_severity: Optional[List[TestSeverity]] = None,
                       filter_category: Optional[List[TestCategory]] = None,
                       fail_fast: bool = False) -> Dict[str, Any]:
        """Run a collection of tests with optional filtering"""
        
        # Filter tests based on criteria
        filtered_tests = self._filter_tests(tests, filter_severity, filter_category)
        
        results = {
            "summary": {
                "total_tests": len(filtered_tests),
                "passed": 0,
                "failed": 0,
                "execution_time": 0.0
            },
            "test_results": [],
            "metrics": {},
            "errors": []
        }
        
        start_time = time.time()
        
        for test in filtered_tests:
            try:
                self.logger.info(f"Running test: {test.name}")
                
                # Setup test
                test.setup()
                
                # Run test
                test_result = await test.run()
                results["test_results"].append(asdict(test_result))
                
                if test_result.passed:
                    results["summary"]["passed"] += 1
                else:
                    results["summary"]["failed"] += 1
                    if fail_fast:
                        self.logger.error(f"Test failed (fail_fast enabled): {test.name}")
                        break
                
                # Teardown test
                test.teardown()
                
                self.logger.info(f"Test {test.name}: {'PASSED' if test_result.passed else 'FAILED'}")
                
            except Exception as e:
                error_msg = f"Test {test.name} encountered an error: {str(e)}"
                self.logger.error(error_msg)
                results["errors"].append(error_msg)
                results["summary"]["failed"] += 1
                
                if fail_fast:
                    break
        
        results["summary"]["execution_time"] = time.time() - start_time
        
        # Generate aggregated metrics
        results["metrics"] = self._generate_aggregate_metrics(results["test_results"])
        
        # Save results
        await self._save_results(results)
        
        return results
    
    def _filter_tests(self, tests: List[BaseTest], 
                     filter_severity: Optional[List[TestSeverity]] = None,
                     filter_category: Optional[List[TestCategory]] = None) -> List[BaseTest]:
        """Filter tests based on severity and category"""
        filtered = tests
        
        if filter_severity:
            filtered = [t for t in filtered if t.severity in filter_severity]
        
        if filter_category:
            filtered = [t for t in filtered if t.category in filter_category]
        
        return filtered
    
    def _generate_aggregate_metrics(self, test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate aggregate metrics across all tests"""
        metrics = {
            "by_category": {},
            "by_severity": {},
            "performance": {
                "avg_execution_time": 0.0,
                "total_execution_time": 0.0
            }
        }
        
        # Aggregate by category
        for result in test_results:
            category = result["category"]
            if category not in metrics["by_category"]:
                metrics["by_category"][category] = {"passed": 0, "failed": 0, "total": 0}
            
            metrics["by_category"][category]["total"] += 1
            if result["passed"]:
                metrics["by_category"][category]["passed"] += 1
            else:
                metrics["by_category"][category]["failed"] += 1
        
        # Aggregate by severity
        for result in test_results:
            severity = result["severity"]
            if severity not in metrics["by_severity"]:
                metrics["by_severity"][severity] = {"passed": 0, "failed": 0, "total": 0}
            
            metrics["by_severity"][severity]["total"] += 1
            if result["passed"]:
                metrics["by_severity"][severity]["passed"] += 1
            else:
                metrics["by_severity"][severity]["failed"] += 1
        
        # Performance metrics
        execution_times = [r["execution_time"] for r in test_results]
        if execution_times:
            metrics["performance"]["avg_execution_time"] = sum(execution_times) / len(execution_times)
            metrics["performance"]["total_execution_time"] = sum(execution_times)
        
        return metrics
    
    async def _save_results(self, results: Dict[str, Any]) -> None:
        """Save test results to file"""
        timestamp = int(time.time())
        filename = f"test_results_{timestamp}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        # Also save as latest
        latest_path = self.output_dir / "latest_results.json"
        with open(latest_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)


class CIRunner:
    """CI/CD specific test runner with exit codes and reporting"""
    
    def __init__(self, test_runner: TestRunner):
        self.test_runner = test_runner
        self.logger = logging.getLogger(__name__)
    
    async def run_ci_tests(self, tests: List[BaseTest], 
                          ci_config: Dict[str, Any] = None) -> int:
        """Run tests in CI/CD mode with appropriate exit codes"""
        
        if ci_config is None:
            ci_config = self._default_ci_config()
        
        # Run tests with CI configuration
        results = await self.test_runner.run_tests(
            tests=tests,
            filter_severity=ci_config.get("required_severities"),
            filter_category=ci_config.get("required_categories"),
            fail_fast=ci_config.get("fail_fast", False)
        )
        
        # Generate CI report
        await self._generate_ci_report(results, ci_config)
        
        # Determine exit code based on results and CI requirements
        exit_code = self._determine_exit_code(results, ci_config)
        
        return exit_code
    
    def _default_ci_config(self) -> Dict[str, Any]:
        """Default CI configuration"""
        return {
            "required_severities": [TestSeverity.CRITICAL, TestSeverity.HIGH],
            "required_categories": None,  # All categories
            "fail_fast": False,
            "min_pass_rate": 0.95,  # 95% pass rate required
            "max_critical_failures": 0,  # No critical test failures allowed
            "max_high_failures": 2,  # Maximum 2 high severity failures
            "performance_thresholds": {
                "max_avg_execution_time": 30.0,  # 30 seconds average
                "max_total_execution_time": 300.0  # 5 minutes total
            }
        }
    
    async def _generate_ci_report(self, results: Dict[str, Any], 
                                 ci_config: Dict[str, Any]) -> None:
        """Generate CI-specific report"""
        report = {
            "ci_summary": {
                "build_status": "PENDING",
                "total_tests": results["summary"]["total_tests"],
                "passed": results["summary"]["passed"],
                "failed": results["summary"]["failed"],
                "pass_rate": results["summary"]["passed"] / max(results["summary"]["total_tests"], 1),
                "execution_time": results["summary"]["execution_time"]
            },
            "quality_gates": {},
            "recommendations": []
        }
        
        # Check quality gates
        report["quality_gates"] = self._check_quality_gates(results, ci_config)
        
        # Generate recommendations
        report["recommendations"] = self._generate_recommendations(results, ci_config)
        
        # Determine overall build status
        if all(gate["passed"] for gate in report["quality_gates"].values()):
            report["ci_summary"]["build_status"] = "PASSED"
        else:
            report["ci_summary"]["build_status"] = "FAILED"
        
        # Save CI report
        ci_report_path = self.test_runner.output_dir / "ci_report.json"
        with open(ci_report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        # Print CI summary to console
        self._print_ci_summary(report)
    
    def _check_quality_gates(self, results: Dict[str, Any], 
                           ci_config: Dict[str, Any]) -> Dict[str, Any]:
        """Check CI quality gates"""
        gates = {}
        
        # Pass rate gate
        pass_rate = results["summary"]["passed"] / max(results["summary"]["total_tests"], 1)
        min_pass_rate = ci_config.get("min_pass_rate", 0.95)
        gates["pass_rate"] = {
            "name": "Minimum Pass Rate",
            "actual": pass_rate,
            "threshold": min_pass_rate,
            "passed": pass_rate >= min_pass_rate
        }
        
        # Critical failures gate
        critical_failures = results["metrics"]["by_severity"].get("critical", {}).get("failed", 0)
        max_critical = ci_config.get("max_critical_failures", 0)
        gates["critical_failures"] = {
            "name": "Maximum Critical Failures",
            "actual": critical_failures,
            "threshold": max_critical,
            "passed": critical_failures <= max_critical
        }
        
        # High severity failures gate
        high_failures = results["metrics"]["by_severity"].get("high", {}).get("failed", 0)
        max_high = ci_config.get("max_high_failures", 2)
        gates["high_failures"] = {
            "name": "Maximum High Severity Failures",
            "actual": high_failures,
            "threshold": max_high,
            "passed": high_failures <= max_high
        }
        
        # Performance gates
        perf_thresholds = ci_config.get("performance_thresholds", {})
        avg_time = results["metrics"]["performance"]["avg_execution_time"]
        max_avg_time = perf_thresholds.get("max_avg_execution_time", 30.0)
        gates["avg_execution_time"] = {
            "name": "Average Execution Time",
            "actual": avg_time,
            "threshold": max_avg_time,
            "passed": avg_time <= max_avg_time
        }
        
        return gates
    
    def _generate_recommendations(self, results: Dict[str, Any], 
                                ci_config: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        # Check for failed critical tests
        critical_failures = results["metrics"]["by_severity"].get("critical", {}).get("failed", 0)
        if critical_failures > 0:
            recommendations.append(
                f"🚨 {critical_failures} CRITICAL test(s) failed. Address immediately before release."
            )
        
        # Check for high failure rate
        pass_rate = results["summary"]["passed"] / max(results["summary"]["total_tests"], 1)
        if pass_rate < 0.9:
            recommendations.append(
                f"⚠️ Pass rate is {pass_rate:.1%}. Consider reviewing failed tests and improving quality."
            )
        
        # Check for performance issues
        avg_time = results["metrics"]["performance"]["avg_execution_time"]
        if avg_time > 15.0:
            recommendations.append(
                f"🐌 Average test execution time is {avg_time:.1f}s. Consider optimizing slow tests."
            )
        
        # Check category-specific issues
        for category, stats in results["metrics"]["by_category"].items():
            if stats["failed"] > 0:
                failure_rate = stats["failed"] / stats["total"]
                if failure_rate > 0.2:  # More than 20% failure rate
                    recommendations.append(
                        f"📊 {category} category has {failure_rate:.1%} failure rate. Focus on improving {category} tests."
                    )
        
        return recommendations
    
    def _determine_exit_code(self, results: Dict[str, Any], 
                           ci_config: Dict[str, Any]) -> int:
        """Determine appropriate exit code for CI/CD"""
        
        # Check critical failures
        critical_failures = results["metrics"]["by_severity"].get("critical", {}).get("failed", 0)
        if critical_failures > ci_config.get("max_critical_failures", 0):
            return 1  # Exit with error
        
        # Check pass rate
        pass_rate = results["summary"]["passed"] / max(results["summary"]["total_tests"], 1)
        if pass_rate < ci_config.get("min_pass_rate", 0.95):
            return 1  # Exit with error
        
        # Check high severity failures
        high_failures = results["metrics"]["by_severity"].get("high", {}).get("failed", 0)
        if high_failures > ci_config.get("max_high_failures", 2):
            return 1  # Exit with error
        
        return 0  # Success
    
    def _print_ci_summary(self, report: Dict[str, Any]) -> None:
        """Print CI summary to console"""
        summary = report["ci_summary"]
        
        print("\n" + "="*60)
        print("🤖 AGENTIC AI TEST RESULTS")
        print("="*60)
        print(f"Build Status: {summary['build_status']}")
        print(f"Tests Run: {summary['total_tests']}")
        print(f"Passed: {summary['passed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Pass Rate: {summary['pass_rate']:.1%}")
        print(f"Execution Time: {summary['execution_time']:.2f}s")
        
        print("\n📊 QUALITY GATES")
        print("-"*40)
        for gate_name, gate_info in report["quality_gates"].items():
            status = "✅ PASS" if gate_info["passed"] else "❌ FAIL"
            print(f"{gate_info['name']}: {status}")
            print(f"  Actual: {gate_info['actual']}, Threshold: {gate_info['threshold']}")
        
        if report["recommendations"]:
            print("\n💡 RECOMMENDATIONS")
            print("-"*40)
            for rec in report["recommendations"]:
                print(f"  {rec}")
        
        print("\n" + "="*60)
