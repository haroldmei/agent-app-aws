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
        if agent.memory and hasattr(agent.memory, 'get_messages_from_last_n_runs'):
            # Memory v2 approach
            current_messages = agent.memory.get_messages_from_last_n_runs(input.thread_id)
        elif agent.memory and hasattr(agent.memory, 'messages'):
            # Legacy AgentMemory approach
            current_messages = agent.memory.messages
        else:
            current_messages = []
        current_messages_count = len(current_messages)
        
        # Run the agent with the user message
        result = await agent.arun(input.last_new_user_message_str())
        
        # Get new messages after the run
        if agent.memory and hasattr(agent.memory, 'get_messages_from_last_n_runs'):
            # Memory v2 approach
            new_messages = agent.memory.get_messages_from_last_n_runs(input.thread_id)
        elif agent.memory and hasattr(agent.memory, 'messages'):
            # Legacy AgentMemory approach
            new_messages = agent.memory.messages
        else:
            new_messages = []
        new_messages_to_return = new_messages[current_messages_count:]
        
        # Format messages for langwatch
        openai_formatted_messages = []
        for message in new_messages_to_return:
            if hasattr(message, 'role') and hasattr(message, 'content'):
                formatted_msg = {
                    "role": message.role,
                    "content": str(message.content) if message.content is not None else ""
                }
                
                # Handle tool calls properly for assistant messages
                if message.role == "assistant" and hasattr(message, 'tool_calls') and message.tool_calls:
                    formatted_msg["tool_calls"] = message.tool_calls
                
                # Handle tool messages properly  
                elif message.role == "tool" and hasattr(message, 'tool_call_id') and message.tool_call_id:
                    formatted_msg["tool_call_id"] = message.tool_call_id
                
                # Only include messages with valid content or proper tool structure
                if (formatted_msg["content"] or 
                    (message.role == "assistant" and formatted_msg.get("tool_calls")) or
                    (message.role == "tool" and formatted_msg.get("tool_call_id"))):
                    openai_formatted_messages.append(formatted_msg)
        
        # If no valid new messages, create one from the result
        if not openai_formatted_messages and result:
            formatted_msg = {
                "role": "assistant",
                "content": str(result.content) if hasattr(result, 'content') and result.content else str(result)
            }
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
        if agent.memory and hasattr(agent.memory, 'get_messages_from_last_n_runs'):
            # Memory v2 approach
            current_messages = agent.memory.get_messages_from_last_n_runs(input.thread_id)
        elif agent.memory and hasattr(agent.memory, 'messages'):
            # Legacy AgentMemory approach
            current_messages = agent.memory.messages
        else:
            current_messages = []
        current_messages_count = len(current_messages)
        
        # Run the agent with the user message
        result = await agent.arun(input.last_new_user_message_str())
        
        # Get new messages after the run
        if agent.memory and hasattr(agent.memory, 'get_messages_from_last_n_runs'):
            # Memory v2 approach
            new_messages = agent.memory.get_messages_from_last_n_runs(input.thread_id)
        elif agent.memory and hasattr(agent.memory, 'messages'):
            # Legacy AgentMemory approach
            new_messages = agent.memory.messages
        else:
            new_messages = []
        new_messages_to_return = new_messages[current_messages_count:]
        
        # Format messages for langwatch
        openai_formatted_messages = []
        for message in new_messages_to_return:
            if hasattr(message, 'role') and hasattr(message, 'content'):
                formatted_msg = {
                    "role": message.role,
                    "content": str(message.content) if message.content is not None else ""
                }
                
                # Handle tool calls properly for assistant messages
                if message.role == "assistant" and hasattr(message, 'tool_calls') and message.tool_calls:
                    formatted_msg["tool_calls"] = message.tool_calls
                
                # Handle tool messages properly  
                elif message.role == "tool" and hasattr(message, 'tool_call_id') and message.tool_call_id:
                    formatted_msg["tool_call_id"] = message.tool_call_id
                
                # Only include messages with valid content or proper tool structure
                if (formatted_msg["content"] or 
                    (message.role == "assistant" and formatted_msg.get("tool_calls")) or
                    (message.role == "tool" and formatted_msg.get("tool_call_id"))):
                    openai_formatted_messages.append(formatted_msg)
        
        # If no valid new messages, create one from the result
        if not openai_formatted_messages and result:
            formatted_msg = {
                "role": "assistant",
                "content": str(result.content) if hasattr(result, 'content') and result.content else str(result)
            }
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
