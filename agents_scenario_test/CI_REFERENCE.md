# CI/CD Quick Reference for Scenario-Based QA Tests

## Overview
The scenario-based QA tests are automatically run through GitHub Actions to ensure agent quality and reliability.

## Workflow File
- **Location**: `.github/workflows/scenario-qa-tests.yml`
- **Name**: "Scenario-Based Quality Assurance Tests"

## Triggers

### Automatic Triggers
1. **Push to main/develop**: When scenario test files or agent files change
2. **Pull Request to main**: For validation before merge
3. **Scheduled**: Nightly at 3 AM UTC for regression detection

### Manual Trigger
- **Workflow Dispatch**: On-demand testing with options:
  - Test category: all, task, tool, flow, hallucination, integration
  - Agent filter: all, sage, scholar
  - Verbose output: true/false

## Test Jobs

### 1. Individual Category Tests (`scenario-tests`)
- **Purpose**: Run each test category separately for focused validation
- **Matrix Strategy**: Runs 5 parallel jobs (one per category)
- **Timeout**: 60 minutes per job
- **Artifacts**: Test results and logs per category (7-day retention)

### 2. Comprehensive All Tests (`scenario-tests-all`)
- **Purpose**: Run all tests together for full validation
- **Condition**: Only when testing "all" categories
- **Timeout**: 90 minutes
- **Artifacts**: Comprehensive results and logs (14-day retention)

### 3. Results Notification (`notify-results`)
- **Purpose**: Summarize test results and create summary
- **Depends On**: Both test jobs
- **Outputs**: GitHub step summary with status and coverage

## Environment Setup

### Services
- **PostgreSQL**: `agnohq/pgvector:16` with health checks
- **Database**: `ai` database with `ai` user

### Dependencies
- **Python**: 3.13 (latest stable)
- **Package Manager**: `uv` for fast dependency installation
- **Caching**: Pip and uv caches for faster builds

### Environment Variables
```bash
RUNTIME_ENV=test
DB_HOST=localhost
DB_PORT=5432
DB_USER=ai
DB_PASS=ai
DB_DATABASE=ai
OPENAI_API_KEY=${{ secrets.OPENAI_API_KEY }}
LANGWATCH_API_KEY=${{ secrets.LANGWATCH_API_KEY }}
```

## Local Development

### Prerequisites
```bash
# Required environment variables
export OPENAI_API_KEY="your-openai-key"
export LANGWATCH_API_KEY="your-langwatch-key"
export RUNTIME_ENV="test"

# Database (if testing locally)
export DB_HOST="localhost"
export DB_PORT="5432"
export DB_USER="ai"
export DB_PASS="ai"
export DB_DATABASE="ai"
```

### Running Tests Locally
```bash
# Navigate to test directory
cd agents_scenario_test

# Install dependencies
pip install -r requirements.txt
pip install -r ../requirements.txt

# Run all tests
python run_tests.py --category=all --verbose

# Run specific category
python run_tests.py --category=hallucination --agent=sage

# Direct pytest
pytest test_task_completion.py -v
```

### Validation Script
```bash
# Validate CI environment setup
python validate_ci_env.py
```

## Monitoring and Debugging

### GitHub Actions UI
1. Go to repository → Actions → "Scenario-Based Quality Assurance Tests"
2. View workflow runs and detailed logs
3. Download artifacts for local debugging

### Test Artifacts
- **JUnit XML**: `test-results/junit.xml` for test reporting
- **HTML Report**: `test-results/report.html` for visual results (if available)
- **Logs**: Detailed pytest output and error traces

### Common Issues
1. **API Key Issues**: Check secrets configuration in repository settings
2. **Database Connection**: Verify PostgreSQL service health
3. **Dependency Issues**: Check requirements.txt and uv.lock consistency
4. **Test Timeouts**: Individual tests may need optimization

## Status Monitoring

### Badges
- **Main README**: Displays current test status
- **Test Directory**: Shows scenario-specific test status

### Notifications
- **Step Summary**: Automatic summary in GitHub Actions
- **Email**: Configure in repository settings for failure notifications

## Contributing

### Adding Tests
1. Create new test functions following existing patterns
2. Use `@pytest.mark.agent_test` marker
3. Include descriptive scenario descriptions
4. Define specific evaluation criteria

### Modifying Workflow
1. Edit `.github/workflows/scenario-qa-tests.yml`
2. Test changes in feature branch
3. Monitor workflow runs for issues
4. Update documentation as needed

### Performance Considerations
- **Parallel Execution**: Categories run in parallel for speed
- **Caching**: Dependencies cached for faster builds
- **Timeouts**: Set appropriately for test complexity
- **Resource Limits**: Consider GitHub Actions limits

## Security

### Secrets Management
- **OPENAI_API_KEY**: Stored in repository secrets
- **LANGWATCH_API_KEY**: Stored in repository secrets
- **Access Control**: Limited to repository collaborators

### Best Practices
- Never commit API keys to repository
- Use environment-specific configurations
- Regularly rotate API keys
- Monitor usage and costs
