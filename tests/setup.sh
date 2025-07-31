#!/bin/bash

# Agentic AI Test Framework Setup Script

echo "🤖 Setting up Agentic AI Test Framework..."

# Check if Python 3.12+ is available
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.12"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $required_version or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install test framework dependencies
echo "📚 Installing test framework dependencies..."
pip install -r tests/requirements.txt

# Install main project dependencies
echo "📚 Installing project dependencies..."
pip install -r requirements.txt

# Install project in editable mode
echo "🔧 Installing project in editable mode..."
pip install -e .

# Generate default golden datasets
echo "📊 Generating default golden datasets..."
python -c "
from tests.framework.fixtures import save_default_datasets
save_default_datasets('tests/data')
print('✅ Golden datasets generated in tests/data/')
"

# Create test output directories
echo "📁 Creating test output directories..."
mkdir -p test_results/{agents,teams,system,ci,performance}

# Run a quick smoke test
echo "🧪 Running smoke test..."
python -c "
import asyncio
from agents.sage import get_sage
from tests.framework.fixtures import TestDataFactory
from tests.framework.implementations import RAGValidationTest

async def smoke_test():
    try:
        agent = get_sage(debug_mode=True)
        test_data = TestDataFactory.create_rag_test_data()[0]
        test = RAGValidationTest(agent, test_data)
        print('✅ Framework setup successful - ready for testing!')
        return True
    except Exception as e:
        print(f'❌ Smoke test failed: {e}')
        return False

result = asyncio.run(smoke_test())
"

echo ""
echo "🎉 Agentic AI Test Framework setup complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Activate virtual environment: source .venv/bin/activate"
echo "   2. Set environment variables: export OPENAI_API_KEY='your-key'"
echo "   3. Run tests: python tests/run_ci.py --test-type sage"
echo ""
echo "📚 Documentation: tests/README.md"
echo "🧪 Example tests: tests/test_suites.py"
