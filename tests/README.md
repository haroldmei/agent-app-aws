# Agentic AI Test Framework

A comprehensive testing framework for agentic AI systems based on industry best practices for RAG validation, agent behavior testing, team orchestration, and quality assurance.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
pip install pytest pytest-asyncio sentence-transformers scikit-learn numpy
```

### 2. Run Individual Agent Tests

```bash
# Test Sage agent
python tests/run_ci.py --test-type sage

# Test all agents with specific severity
python tests/run_ci.py --test-type sage --severity critical high
```

### 3. Run Team Tests

```bash
# Test team orchestration
python tests/run_ci.py --test-type teams
```

### 4. Run Full CI Suite

```bash
# Complete CI test suite with quality gates
python tests/run_ci.py --test-type ci
```

## 🧪 Test Framework Architecture

### Core Components

1. **Base Test Classes** (`framework/base.py`)
   - `BaseAgentTest` - Individual agent testing
   - `BaseTeamTest` - Team orchestration testing  
   - `BaseSystemTest` - End-to-end system testing

2. **Metrics Engine** (`framework/metrics.py`)
   - `RAGMetrics` - Context relevance, faithfulness, answer relevance
   - `AgentMetrics` - Goal attainment, tool utilization, response coherence
   - `QualityMetrics` - Hallucination, bias, privacy leakage detection

3. **Test Runners** (`framework/runners.py`)
   - `TestRunner` - Core test execution engine
   - `CIRunner` - CI/CD integration with quality gates

4. **Test Implementations** (`framework/implementations.py`)
   - Concrete test classes for each test category
   - Ready-to-use test implementations

## 📊 Test Categories

### 1. RAG Core Component Tests

**Focus:** Context relevance, faithfulness, retrieval performance

```python
from framework.implementations import RAGValidationTest
from framework.fixtures import TestDataFactory

# Create RAG test
test_data = TestDataFactory.create_rag_test_data()[0]
rag_test = RAGValidationTest(sage_agent, test_data)
result = await rag_test.run()
```

**Metrics:**
- Context Relevance (threshold: 0.7)
- Answer Relevance (threshold: 0.7)  
- Faithfulness/Groundedness (threshold: 0.8)

### 2. Agent Behavior Tests

**Focus:** Goal attainment, tool usage, response coherence

```python
from framework.implementations import AgentBehaviorTest

# Test agent behavior
behavior_data = TestDataFactory.create_agent_behavior_test_data()[0]
behavior_test = AgentBehaviorTest(sage_agent, behavior_data)
result = await behavior_test.run()
```

**Metrics:**
- Goal Attainment (threshold: 0.8)
- Tool Utilization Accuracy (threshold: 0.9)
- Response Coherence (threshold: 0.7)

### 3. Team Orchestration Tests

**Focus:** Multi-agent collaboration, coordination, deliverable quality

```python
from framework.implementations import TeamOrchestrationTest

# Test team coordination
team_data = TestDataFactory.create_team_orchestration_test_data()[0]
team_test = TeamOrchestrationTest(finance_team, team_data)
result = await team_test.run()
```

**Metrics:**
- Team Goal Attainment (threshold: 0.7)
- Collaboration Effectiveness (threshold: 0.7)
- Response Coherence (threshold: 0.7)

### 4. Quality & Safety Tests

**Focus:** Hallucination detection, bias prevention, privacy protection

```python
from framework.implementations import QualitySafetyTest

# Test quality and safety
safety_data = TestDataFactory.create_quality_safety_test_data()[0]
safety_test = QualitySafetyTest(sage_agent, safety_data)
result = await safety_test.run()
```

**Metrics:**
- Hallucination Detection (threshold: ≤0.1)
- Bias Detection (threshold: ≤0.2)
- Privacy Leakage (threshold: ≤0.0)

## 🎯 CI/CD Integration

### Quality Gates

The framework includes configurable quality gates for CI/CD:

```yaml
quality_gates:
  min_pass_rate: 0.95          # 95% tests must pass
  max_critical_failures: 0     # No critical test failures
  max_high_failures: 2         # Max 2 high severity failures
  max_avg_execution_time: 20.0 # 20 seconds average
```

### GitHub Actions Integration

The framework includes a complete GitHub Actions workflow (`.github/workflows/qa-tests.yml`):

- **Agent Tests** - Individual agent validation
- **Team Tests** - Team orchestration validation  
- **System Integration** - End-to-end testing
- **Quality Gates** - Final CI decision
- **Performance Tests** - Load and latency testing
- **Security Scan** - Safety and security validation

### Usage in CI

```bash
# In your CI pipeline
python tests/run_ci.py --test-type ci --fail-fast --output-dir ci_results

# Exit code 0 = success, 1 = failure
echo "CI Exit Code: $?"
```

## 📈 Test Data Management

### Golden Datasets

The framework includes golden datasets for consistent testing:

```python
from framework.fixtures import create_default_golden_datasets

# Generate standard test datasets
datasets = create_default_golden_datasets()

# Available datasets:
# - rag_validation
# - agent_behavior  
# - team_orchestration
# - quality_safety
# - performance
```

### Custom Test Data

Create custom test data for your specific use cases:

```python
from framework.fixtures import TestData

custom_test = TestData(
    input_data={"query": "Custom test question"},
    expected_output={"answer": "Expected response"},
    context="Relevant context for the query",
    metadata={"category": "custom", "difficulty": "medium"}
)
```

## 🔧 Configuration

### Environment Variables

```bash
# Required
export OPENAI_API_KEY="your-api-key"

# Optional
export AGNO_DEBUG=true
export TEST_OUTPUT_DIR="custom_results"
export TEST_FAIL_FAST=false
```

### Test Configuration

Customize test behavior in your test runners:

```python
# Custom CI configuration
ci_config = {
    "required_severities": [TestSeverity.CRITICAL],
    "fail_fast": True,
    "min_pass_rate": 0.98,
    "performance_thresholds": {
        "max_avg_execution_time": 15.0
    }
}

exit_code = await ci_runner.run_ci_tests(tests, ci_config)
```

## 📊 Test Reports

### Automated Reports

The framework generates comprehensive test reports:

- **JSON Results** - Machine-readable test results
- **CI Reports** - Human-readable CI summaries
- **Performance Metrics** - Execution time and throughput data
- **Quality Metrics** - RAG, agent, and safety metrics

### Example Output

```json
{
  "summary": {
    "total_tests": 25,
    "passed": 23,
    "failed": 2,
    "pass_rate": 0.92,
    "execution_time": 45.3
  },
  "quality_gates": {
    "pass_rate": {"passed": false, "actual": 0.92, "threshold": 0.95},
    "critical_failures": {"passed": true, "actual": 0, "threshold": 0}
  },
  "recommendations": [
    "⚠️ Pass rate is 92%. Consider reviewing failed tests.",
    "🚨 0 CRITICAL test(s) failed. Good job!"
  ]
}
```

## 🛠️ Extending the Framework

### Custom Metrics

Add domain-specific metrics:

```python
from framework.metrics import BaseMetric, MetricResult

class CustomMetric(BaseMetric):
    async def calculate(self, **kwargs) -> MetricResult:
        # Your custom metric logic
        value = your_calculation()
        return self._create_result(value)
```

### Custom Tests

Create specialized test implementations:

```python
from framework.base import BaseAgentTest

class DomainSpecificTest(BaseAgentTest):
    async def run(self) -> TestResult:
        # Your test logic
        return self._create_result(passed=True, score=0.95)
```

## 🎯 Best Practices

### 1. Test Organization

- Organize tests by severity: `CRITICAL` → `HIGH` → `MEDIUM` → `LOW`
- Use appropriate test categories for filtering
- Maintain golden datasets for regression testing

### 2. CI/CD Integration

- Run critical tests on every commit
- Use performance tests for nightly builds
- Set appropriate quality gates for your release process

### 3. Monitoring & Observability

- Track test metrics over time
- Monitor performance regressions
- Set up alerts for quality gate failures

### 4. Continuous Improvement

- Regularly review and update golden datasets
- Add new test cases for discovered edge cases
- Adjust quality thresholds based on system maturity

## 📚 Example Usage

See `tests/test_suites.py` for complete examples of how to use the framework with your agents and teams.

## 🤝 Contributing

When adding new tests or metrics:

1. Follow the base class patterns
2. Include appropriate docstrings
3. Add test cases to the golden datasets
4. Update CI configuration if needed

## 📄 License

This test framework is part of the agentic AI system and follows the same licensing terms.
