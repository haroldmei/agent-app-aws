"""
Test suite configuration and fixtures for agent validation.
"""
import pytest
import asyncio
from typing import Optional
from agents.sage import get_sage
from agents.scholar import get_scholar
from agents.operator import AgentType, get_agent


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def sage_agent():
    """Fixture for Sage agent."""
    return get_sage(
        model_id="gpt-4o-mini",
        user_id="test_user",
        session_id="test_session_sage",
        debug_mode=False
    )


@pytest.fixture
async def scholar_agent():
    """Fixture for Scholar agent."""
    return get_scholar(
        model_id="gpt-4o-mini",
        user_id="test_user",
        session_id="test_session_scholar",
        debug_mode=False
    )


@pytest.fixture
async def operator_agent():
    """Fixture for Operator agent."""
    return get_agent(
        model_id="gpt-4o-mini",
        agent_id=AgentType.SAGE,
        user_id="test_user",
        session_id="test_session_operator",
        debug_mode=False
    )


class MockJudgeAgent:
    """Mock judge agent for evaluation."""
    
    def __init__(self, criteria: list[str]):
        self.criteria = criteria
    
    async def evaluate(self, response: str, context: Optional[str] = None) -> dict:
        """Mock evaluation based on criteria."""
        results = {}
        for criterion in self.criteria:
            # Simple keyword-based evaluation for testing
            if "tool" in criterion.lower():
                results[criterion] = "search" in response.lower() or "duckduckgo" in response.lower()
            elif "factual" in criterion.lower() or "accurate" in criterion.lower():
                results[criterion] = len(response) > 50 and "based on" not in response.lower()
            elif "memory" in criterion.lower() or "context" in criterion.lower():
                results[criterion] = context is not None and len(response) > 30
            elif "hallucination" in criterion.lower():
                # Check for specific hallucination indicators
                hallucination_phrases = ["I'm not sure", "I don't have", "cannot confirm"]
                results[criterion] = any(phrase in response for phrase in hallucination_phrases)
            else:
                results[criterion] = len(response) > 20
        
        return {
            "success": all(results.values()),
            "criteria_results": results,
            "overall_score": sum(results.values()) / len(results) if results else 0
        }


@pytest.fixture
def mock_judge():
    """Fixture for mock judge agent."""
    return MockJudgeAgent
