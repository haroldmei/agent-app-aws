import pytest
import sys
from pathlib import Path

# Add the parent directory to sys.path to import agents
sys.path.append(str(Path(__file__).parent.parent))

import scenario
from agno.models.openai import OpenAIChat


# Configure scenario framework
scenario.configure(
    default_model="openai/gpt-4o-mini",
    cache_key="agents-test-42",
)


class SageAdapter(scenario.AgentAdapter):
    """Adapter for Sage agent to work with langwatch scenario framework."""
    
    def __init__(self):
        from agents.sage import get_sage

        self.agent_factory = get_sage
    
    async def call(self, input: scenario.AgentInput) -> scenario.AgentReturnTypes:
        # Create agent instance
        agent = self.agent_factory(
            model_id="gpt-4o-mini",
            user_id=input.thread_id,
            session_id=input.thread_id,
            debug_mode=False,
        )
        
        # Get current message count to track new messages
        current_messages = agent.memory.messages if agent.memory else []
        current_messages_count = len(current_messages)
        
        # Run the agent with the user message
        result = await agent.arun(input.last_new_user_message_str())
        
        # Get new messages after the run
        new_messages = agent.memory.messages if agent.memory else []
        new_messages_to_return = new_messages[current_messages_count:]
        
        # Format messages for langwatch
        openai_formatted_messages = []
        for message in new_messages_to_return:
            if hasattr(message, 'role') and hasattr(message, 'content'):
                formatted_msg = {
                    "role": message.role,
                    "content": str(message.content)
                }
                if hasattr(message, 'tools') and message.tools:
                    formatted_msg["tool_calls"] = message.tools
                openai_formatted_messages.append(formatted_msg)
        
        # If no new messages, create one from the result
        if not openai_formatted_messages and result:
            formatted_msg = {
                "role": "assistant",
                "content": str(result.content) if result.content else ""
            }
            if hasattr(result, 'tools') and result.tools:
                formatted_msg["tool_calls"] = result.tools
            openai_formatted_messages.append(formatted_msg)
        
        return openai_formatted_messages


class ScholarAdapter(scenario.AgentAdapter):
    """Adapter for Scholar agent to work with langwatch scenario framework."""
    
    def __init__(self):
        from agents.scholar import get_scholar

        self.agent_factory = get_scholar
    
    async def call(self, input: scenario.AgentInput) -> scenario.AgentReturnTypes:
        # Create agent instance
        agent = self.agent_factory(
            model_id="gpt-4o-mini",
            user_id=input.thread_id,
            session_id=input.thread_id,
            debug_mode=False,
        )
        
        # Get current message count to track new messages
        current_messages = agent.memory.messages if agent.memory else []
        current_messages_count = len(current_messages)
        
        # Run the agent with the user message
        result = await agent.arun(input.last_new_user_message_str())
        
        # Get new messages after the run
        new_messages = agent.memory.messages if agent.memory else []
        new_messages_to_return = new_messages[current_messages_count:]
        
        # Format messages for langwatch
        openai_formatted_messages = []
        for message in new_messages_to_return:
            if hasattr(message, 'role') and hasattr(message, 'content'):
                formatted_msg = {
                    "role": message.role,
                    "content": str(message.content)
                }
                if hasattr(message, 'tools') and message.tools:
                    formatted_msg["tool_calls"] = message.tools
                openai_formatted_messages.append(formatted_msg)
        
        # If no new messages, create one from the result
        if not openai_formatted_messages and result:
            formatted_msg = {
                "role": "assistant",
                "content": str(result.content) if result.content else ""
            }
            if hasattr(result, 'tools') and result.tools:
                formatted_msg["tool_calls"] = result.tools
            openai_formatted_messages.append(formatted_msg)
        
        return openai_formatted_messages


@pytest.fixture
def sage_adapter():
    """Fixture providing Sage agent adapter."""
    return SageAdapter()


@pytest.fixture 
def scholar_adapter():
    """Fixture providing Scholar agent adapter."""
    return ScholarAdapter()
