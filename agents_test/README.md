# Agent Testing Suite

This test suite provides comprehensive validation for the agents defined in the `agents` folder, implementing test cases for:

## Test Categories

### 1. Agentic Behavior & Orchestration Tests (`test_agentic_behavior.py`)
- **Task Completion & Goal Attainment Tests**: Validates agents' ability to complete assigned tasks and achieve stated goals
- **Tool Interaction Tests**: Ensures proper use of available tools (knowledge base search, web search, etc.)
- **Conversational Flow & Memory Tests**: Tests context maintenance, conversation coherence, and memory management

### 2. Generative AI Quality & Safety Tests (`test_quality_safety.py`)
- **Hallucination Detection Tests**: Validates factual grounding, uncertainty acknowledgment, and prevents fabrication
- **Safety Measures Tests**: Ensures appropriate boundaries and safe response generation

### 3. Integration Tests (`test_integration.py`)
- **End-to-End Workflows**: Tests complete agent workflows combining multiple capabilities
- **Error Recovery**: Validates graceful handling of failures and edge cases
- **Cross-Agent Consistency**: Ensures quality standards across different agent types
- **Performance Tests**: Validates response times and scalability

## Agents Tested

The test suite covers all agents defined in the `agents` folder:

### Sage Agent
- **Capabilities**: Knowledge base access, web search, comprehensive information synthesis
- **Tools**: DuckDuckGo search, vector database knowledge base
- **Focus**: Accurate, context-rich responses with knowledge grounding

### Scholar Agent
- **Capabilities**: Real-time web research, up-to-date information retrieval
- **Tools**: DuckDuckGo search for current information
- **Focus**: Precise, engaging responses with current data

### Operator Agent
- **Capabilities**: Agent orchestration and routing
- **Focus**: Proper agent selection and workflow management

## Usage

### Prerequisites
```bash
# Install required dependencies
pip install pytest pytest-asyncio

# Ensure environment variables are set
export OPENAI_API_KEY="your-api-key"
export DB_HOST="localhost"  # or your database host
export DB_PORT="5432"
export DB_USER="ai"
export DB_PASS="ai"
export DB_DATABASE="ai"
```

### Running All Tests
```bash
cd agents_test
python test_runner.py
```

### Running Specific Agent Tests
```bash
# Test only Sage agent
python test_runner.py --agent=sage

# Test only Scholar agent  
python test_runner.py --agent=scholar
```

### Running Specific Test Categories
```bash
# Test only behavior/orchestration
python test_runner.py --category=behavior

# Test only safety/quality
python test_runner.py --category=safety

# Test only integration
python test_runner.py --category=integration
```

### Running with Pytest Directly
```bash
# Run all tests with verbose output
pytest -v

# Run specific test file
pytest test_agentic_behavior.py -v

# Run specific test class
pytest test_agentic_behavior.py::TestTaskCompletionAndGoalAttainment -v

# Run specific test method
pytest test_agentic_behavior.py::TestTaskCompletionAndGoalAttainment::test_sage_knowledge_retrieval_task -v
```

## Test Structure

### Fixtures (`conftest.py`)
- `sage_agent`: Provides configured Sage agent instance
- `scholar_agent`: Provides configured Scholar agent instance  
- `operator_agent`: Provides configured Operator agent instance
- `mock_judge`: Mock evaluation agent for test assessment

### Test Files
- `test_agentic_behavior.py`: Behavior and orchestration tests
- `test_quality_safety.py`: Quality and safety validation tests
- `test_integration.py`: Integration and end-to-end tests

## Implementation Notes

### Mock Judge Agent
The test suite uses a `MockJudgeAgent` that evaluates responses based on configurable criteria. This allows for:
- Flexible evaluation logic based on test requirements
- Consistent assessment across different test scenarios
- Easy modification of evaluation criteria

### Test Patterns
Tests follow a structured pattern:
1. Define evaluation criteria using `MockJudgeAgent`
2. Execute agent interactions
3. Evaluate responses against criteria
4. Assert success conditions and specific quality measures

### Environment Requirements
- Valid OpenAI API key for agent operations
- PostgreSQL database for agent session management
- Agents configured with appropriate model settings

## Test Configuration

### Agent Configuration
Tests use `gpt-4o-mini` model by default for cost efficiency while maintaining quality. Agents are configured with:
- Debug mode disabled for cleaner test output
- Unique session IDs to prevent test interference
- Standard user ID for consistency

### Evaluation Criteria
Each test defines specific criteria for evaluation:
- Task completion validation
- Tool usage verification  
- Response quality assessment
- Safety and factual accuracy checks

## Expected Test Coverage

### Task Completion Tests
- ✅ Knowledge retrieval and synthesis
- ✅ Web research and information gathering
- ✅ Multi-step task breakdown and execution
- ✅ Goal-oriented conversation management

### Tool Interaction Tests
- ✅ Knowledge base search functionality
- ✅ Web search tool usage
- ✅ Tool selection logic
- ✅ Error handling and recovery

### Conversational Tests
- ✅ Context maintenance across turns
- ✅ Memory and history recall
- ✅ Conversation flow coherence
- ✅ Multi-turn dialogue management

### Quality & Safety Tests
- ✅ Factual grounding validation
- ✅ Uncertainty acknowledgment
- ✅ Source attribution accuracy
- ✅ Consistency across similar queries
- ✅ Knowledge gap handling
- ✅ Safety and bias prevention

### Integration Tests
- ✅ Complex workflow execution
- ✅ Cross-agent consistency
- ✅ Error recovery mechanisms
- ✅ Performance benchmarks

## Extending the Test Suite

### Adding New Tests
1. Create test methods following existing patterns
2. Define appropriate evaluation criteria
3. Use existing fixtures or create new ones as needed
4. Add to appropriate test category file

### Custom Evaluation Logic
Extend `MockJudgeAgent` or create specialized evaluation functions for:
- Domain-specific quality measures
- Complex multi-turn conversation assessment
- Tool-specific validation logic
- Safety-specific checks

### Integration with CI/CD
Tests can be integrated into continuous integration:
```bash
# In CI pipeline
python test_runner.py --category=behavior
python test_runner.py --category=safety
python test_runner.py --category=integration
```

## Common Issues and Solutions

### Database Connection Issues
```bash
# Ensure database is running
docker ps | grep postgres

# Check connection settings
echo $DB_HOST $DB_PORT $DB_USER
```

### OpenAI API Issues
```bash
# Verify API key is set
echo $OPENAI_API_KEY

# Check API quota and rate limits
```

### Test Timeouts
- Increase timeout values for slow network connections
- Use lighter models for faster testing (gpt-4o-mini)
- Mock external services for consistent testing

## Test Results Interpretation

### Successful Tests Indicate:
- Agents complete tasks as designed
- Tools are used appropriately and effectively
- Conversational flow and memory work correctly
- Responses are factually grounded and safe
- Error handling is graceful and helpful

### Common Failure Modes:
- Tool usage failures (search not working, incorrect parameters)
- Memory/context issues (not maintaining conversation state)
- Hallucination or factual errors
- Poor error recovery or unhelpful responses
- Performance degradation under load

This comprehensive test suite ensures the quality, safety, and reliability of all agents in the system, providing confidence in their deployment and operation.
