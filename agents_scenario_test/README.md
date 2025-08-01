# Agent Scenario Test Suite

[![Scenario QA Tests](https://github.com/haroldmei/agent-app-aws/actions/workflows/scenario-qa-tests.yml/badge.svg)](https://github.com/haroldmei/agent-app-aws/actions/workflows/scenario-qa-tests.yml)

This test suite provides comprehensive validation for the agents defined in the `agents` folder using the langwatch scenario framework, following the pattern established in the `agno_example` folder.

## Test Categories

### 1. Agentic Behavior & Orchestration Tests

#### Task Completion & Goal Attainment Tests (`test_task_completion.py`)
- **Sage Knowledge Retrieval**: Tests Sage agent's ability to complete knowledge-based tasks
- **Scholar Research Tasks**: Tests Scholar agent's research and analysis capabilities  
- **Multi-step Information Synthesis**: Tests complex information processing and synthesis
- **Goal-oriented Conversations**: Tests maintaining focus on objectives across conversation turns
- **Complex Planning Tasks**: Tests breakdown of complex goals into actionable steps

#### Tool Interaction Tests (`test_tool_interaction.py`)
- **Knowledge Base Tool Usage**: Tests Sage agent's use of knowledge base search
- **Web Search Tool Usage**: Tests Scholar agent's use of DuckDuckGo search tools
- **Tool Selection Logic**: Tests appropriate tool selection for different query types
- **Tool Parameter Accuracy**: Tests precise configuration of tool parameters
- **Tool Error Handling**: Tests graceful handling of tool failures
- **Multi-tool Workflows**: Tests coordination of multiple tools in single responses
- **Tool Result Integration**: Tests blending of tool results with agent knowledge

#### Conversational Flow & Memory Tests (`test_conversational_flow.py`)
- **Context Maintenance**: Tests conversation context across multiple turns
- **History Recall**: Tests accurate recall of earlier conversation details
- **Flow Coherence**: Tests natural conversation progression and transitions
- **Memory Persistence**: Tests maintaining context within conversation sessions
- **Contextual Question Handling**: Tests understanding of contextual references
- **State Management**: Tests tracking of conversation topics and depth
- **Interruption Handling**: Tests managing conversation interruptions and resumptions
- **Learning Adaptation**: Tests adaptation based on user feedback

### 2. Generative AI Quality & Safety Tests

#### Hallucination Detection Tests (`test_hallucination_detection.py`)
- **Factual Grounding**: Tests responses are based on verifiable information
- **Uncertainty Acknowledgment**: Tests appropriate handling of uncertain information
- **Consistency Across Queries**: Tests consistency in responses to similar questions
- **Source Attribution**: Tests accurate citation and source handling
- **Knowledge Gap Handling**: Tests behavior when facing information gaps
- **Temporal Accuracy**: Tests awareness of time-sensitive information
- **Numerical Accuracy**: Tests careful handling of statistics and quantitative data
- **Domain Boundaries**: Tests recognition of specialized knowledge boundaries

### 3. Integration Tests (`test_integration.py`)
- **End-to-End Research Workflows**: Tests complete research processes
- **Error Recovery**: Tests adaptation and recovery from various issues
- **Cross-Agent Consistency**: Tests quality standards across different agents
- **Comprehensive Safety**: Tests safety measures and appropriate boundaries
- **Knowledge Synthesis**: Tests complex information integration over time
- **Real-World Scenarios**: Tests performance in realistic use cases

## Usage

### Prerequisites
1. Ensure the database is running for agent session management
2. Set required environment variables (e.g., `OPENAI_API_KEY`)
3. Install dependencies: `uv sync` or `pip install -r requirements.txt`

### Running Tests

#### All Tests
```bash
cd agents_scenario_test
pytest
```

#### Specific Test Categories
```bash
# Task completion tests
pytest test_task_completion.py -v

# Tool interaction tests  
pytest test_tool_interaction.py -v

# Conversational flow tests
pytest test_conversational_flow.py -v

# Hallucination detection tests
pytest test_hallucination_detection.py -v

# Integration tests
pytest test_integration.py -v
```

#### Specific Agent Tests
```bash
# Tests involving Sage agent
pytest -k "sage" -v

# Tests involving Scholar agent
pytest -k "scholar" -v
```

#### Test Markers
```bash
# Run only agent tests
pytest -m "agent_test" -v

# Run only integration tests
pytest -m "integration" -v

# Run slow tests
pytest -m "slow" -v
```

### Verbose Output
```bash
# Run with detailed output
pytest -v -s

# Run specific test with output
pytest test_task_completion.py::test_sage_knowledge_retrieval_task_completion -v -s
```

## Test Framework Structure

### Configuration (`conftest.py`)
- **Scenario Configuration**: Sets up langwatch scenario framework with appropriate models
- **Agent Adapters**: Provides `SageAdapter` and `ScholarAdapter` classes that interface agents with the scenario framework
- **Fixtures**: Provides `sage_adapter` and `scholar_adapter` fixtures for test use

### Test Pattern
Each test follows the langwatch scenario pattern:

```python
@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_example(sage_adapter):
    result = await scenario.run(
        name="test name",
        description="Detailed scenario description...",
        agents=[
            sage_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "Specific evaluation criterion 1",
                    "Specific evaluation criterion 2",
                    # ...
                ]
            ),
        ],
    )
    assert result.success
```

### Agent Adapters
The adapters handle the interface between agno agents and the langwatch scenario framework:

- **Message Formatting**: Converts agent messages to langwatch-compatible format
- **Session Management**: Manages agent sessions and memory
- **Tool Integration**: Handles tool calls and responses
- **Error Handling**: Manages failures gracefully

## Test Configuration

### Agent Settings
- **Model**: `gpt-4o-mini` for cost efficiency while maintaining quality
- **Debug Mode**: Disabled for cleaner test output
- **Session Management**: Each test uses unique session IDs to prevent interference

### Evaluation Criteria
Tests use specific, measurable criteria for evaluation:
- **Functional Requirements**: Task completion, tool usage, conversation management
- **Quality Standards**: Accuracy, coherence, appropriateness
- **Safety Measures**: Boundary recognition, uncertainty handling, source attribution

## Expected Outcomes

### Successful Tests Indicate:
- Agents complete assigned tasks effectively
- Tools are used appropriately and efficiently  
- Conversation flow is natural and context-aware
- Responses are factually grounded and safe
- Error handling is graceful and helpful
- Quality is consistent across different agents

### Common Failure Patterns:
- **Tool Usage Issues**: Incorrect tool selection or parameter configuration
- **Memory Problems**: Loss of conversation context or history
- **Hallucination**: Fabricated information or unsupported claims
- **Inconsistency**: Contradictory responses to similar queries
- **Poor Error Recovery**: Unhelpful responses when facing difficulties

## Integration with CI/CD

Tests can be integrated into continuous integration pipelines:

```bash
# Basic test run
pytest agents_scenario_test/ --tb=short

# With specific markers
pytest agents_scenario_test/ -m "agent_test and not slow" --tb=short

# With coverage (if configured)
pytest agents_scenario_test/ --cov=agents --cov-report=term-missing
```

## CI/CD Integration

### Automated Testing
The scenario test suite is integrated with GitHub Actions through the `scenario-qa-tests.yml` workflow:

#### Triggers
- **Push/Pull Request**: Tests run on main and develop branches when scenario test files change
- **Scheduled**: Nightly tests at 3 AM UTC to catch regressions
- **Manual**: On-demand testing with customizable parameters via workflow dispatch

#### Test Matrix
The CI runs tests in multiple configurations:
- **Individual Categories**: Each test category (task, tool, flow, hallucination, integration) runs separately
- **Comprehensive Suite**: All tests run together for complete validation
- **Agent-Specific**: Tests can be filtered by agent (sage, scholar, or all)

#### Environment Setup
- **Python 3.13**: Latest Python version for optimal performance
- **PostgreSQL**: Full database setup with pgvector extension
- **Dependencies**: Automated installation of all required packages via uv
- **Environment Variables**: Secure handling of API keys and database credentials

#### Test Artifacts
- Test results and logs are uploaded as artifacts for debugging
- Results retained for 7-14 days depending on test scope
- Comprehensive reporting with status summaries

### Running Tests Locally

#### Development Setup
```bash
# Install dependencies
pip install -r requirements.txt
pip install -r ../requirements.txt

# Set up environment variables
export OPENAI_API_KEY="your-api-key"
export LANGWATCH_API_KEY="your-langwatch-key"
export RUNTIME_ENV="test"

# Run tests with the test runner
python run_tests.py --category=all --verbose

# Check code formatting (recommended before commit)
python format_check.py
```

#### Code Formatting
```bash
# Check formatting
python -m ruff format . --check

# Apply formatting fixes
python -m ruff format .

# Or use the helper script
python format_check.py --fix
```

#### Production Environment
```bash
# With coverage (if configured)
pytest agents_scenario_test/ --cov=agents --cov-report=term-missing
```

## Extension and Customization

### Adding New Tests
1. Follow existing test patterns in appropriate test files
2. Use descriptive scenario descriptions that clearly explain expected behavior
3. Define specific, measurable evaluation criteria
4. Include appropriate test markers

### Custom Evaluation Logic
The langwatch scenario framework allows for sophisticated evaluation:
- **Multi-agent Scenarios**: Test interactions between different agents
- **Complex Workflows**: Test multi-step processes and decision trees
- **Dynamic Criteria**: Adjust evaluation based on scenario context

### Performance Monitoring
Consider adding performance-focused tests:
- **Response Time**: Monitor agent response latency
- **Tool Efficiency**: Track tool usage patterns and success rates
- **Memory Usage**: Monitor conversation memory efficiency
- **Quality Metrics**: Track consistency and accuracy over time

This test suite ensures comprehensive validation of agent capabilities while maintaining the flexibility and power of the langwatch scenario framework.
