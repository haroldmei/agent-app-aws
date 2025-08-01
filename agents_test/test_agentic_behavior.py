"""
Agentic Behavior & Orchestration Tests

This module tests the core agentic behaviors including:
- Task completion and goal attainment
- Tool interaction capabilities
- Conversational flow and memory management
"""
import pytest
import asyncio
from typing import List, Dict, Any


class TestTaskCompletionAndGoalAttainment:
    """Test suite for task completion and goal attainment."""

    @pytest.mark.agent_test
    @pytest.mark.asyncio
    async def test_sage_knowledge_retrieval_task(self, sage_agent, mock_judge):
        """Test Sage agent's ability to complete knowledge retrieval tasks."""
        judge = mock_judge([
            "The agent searches the knowledge base for relevant information",
            "The agent provides a comprehensive answer",
            "The agent completes the information retrieval workflow"
        ])
        
        user_query = "What is machine learning and how does it work?"
        
        # Simulate agent interaction
        response = await sage_agent.arun(user_query)
        response_content = str(response.content) if response and response.content else ""
        
        evaluation = await judge.evaluate(response_content)
        
        assert evaluation["success"], f"Task completion failed: {evaluation['criteria_results']}"
        assert evaluation["overall_score"] > 0.7, "Task completion score too low"

    @pytest.mark.agent_test
    @pytest.mark.asyncio
    async def test_scholar_research_task(self, scholar_agent, mock_judge):
        """Test Scholar agent's ability to complete research tasks."""
        judge = mock_judge([
            "The agent searches the web for current information",
            "The agent provides detailed analysis with sources",
            "The agent completes the research workflow"
        ])
        
        user_query = "What are the latest developments in renewable energy technology?"
        
        response = await scholar_agent.arun(user_query)
        response_content = str(response.content) if response and response.content else ""
        
        evaluation = await judge.evaluate(response_content)
        
        assert evaluation["success"], f"Research task failed: {evaluation['criteria_results']}"
        assert "search" in response_content.lower() or len(response_content) > 100

    @pytest.mark.agent_test
    @pytest.mark.asyncio
    async def test_multi_step_information_synthesis(self, sage_agent, mock_judge):
        """Test agent's ability to handle multi-step information synthesis."""
        judge = mock_judge([
            "The agent breaks down complex queries into components",
            "The agent synthesizes information from multiple sources",
            "The agent provides structured, comprehensive responses"
        ])
        
        complex_query = """I need to understand:
        1. The basic principles of artificial intelligence
        2. Current applications in healthcare
        3. Potential future developments
        Please provide a comprehensive overview."""
        
        response = await sage_agent.arun(complex_query)
        response_content = str(response.content) if response and response.content else ""
        
        evaluation = await judge.evaluate(response_content)
        
        assert evaluation["success"], f"Multi-step synthesis failed: {evaluation['criteria_results']}"
        assert len(response_content) > 200, "Response too brief for complex query"

    @pytest.mark.agent_test
    @pytest.mark.asyncio
    async def test_goal_oriented_conversation(self, scholar_agent, mock_judge):
        """Test agent's ability to maintain goal orientation across turns."""
        judge = mock_judge([
            "The agent maintains focus on the stated goal",
            "The agent provides incremental progress toward completion",
            "The agent successfully achieves the conversation objective"
        ])
        
        # Multi-turn conversation with a specific goal
        goal_query = "Help me plan a sustainable energy solution for a small business"
        followup_query = "What about the costs involved?"
        
        # First turn
        response1 = await scholar_agent.arun(goal_query)
        response1_content = str(response1.content) if response1 and response1.content else ""
        
        # Second turn
        response2 = await scholar_agent.arun(followup_query)
        response2_content = str(response2.content) if response2 and response2.content else ""
        
        # Evaluate goal achievement
        combined_response = f"{response1_content} {response2_content}"
        evaluation = await judge.evaluate(combined_response)
        
        assert evaluation["success"], f"Goal-oriented conversation failed: {evaluation['criteria_results']}"
        assert "sustainable" in response1_content.lower()
        assert "cost" in response2_content.lower()


class TestToolInteraction:
    """Test suite for tool interaction capabilities."""

    @pytest.mark.agent_test
    @pytest.mark.asyncio
    async def test_sage_knowledge_base_tool_usage(self, sage_agent, mock_judge):
        """Test Sage agent's proper use of knowledge base tools."""
        judge = mock_judge([
            "The agent correctly identifies when to use knowledge base search",
            "The agent uses appropriate search parameters",
            "The agent integrates knowledge base results effectively"
        ])
        
        knowledge_query = "What information do you have about our company policies?"
        
        response = await sage_agent.arun(knowledge_query)
        response_content = str(response.content) if response and response.content else ""
        
        evaluation = await judge.evaluate(response_content)
        
        # Check if agent attempted to use knowledge base
        assert evaluation["success"] or "search" in response_content.lower(), \
            f"Knowledge base tool usage failed: {evaluation['criteria_results']}"

    @pytest.mark.agent_test
    @pytest.mark.asyncio
    async def test_scholar_web_search_tool_usage(self, scholar_agent, mock_judge):
        """Test Scholar agent's proper use of web search tools."""
        judge = mock_judge([
            "The agent uses DuckDuckGo search tool appropriately",
            "The agent constructs effective search queries",
            "The agent processes and presents search results clearly"
        ])
        
        web_search_query = "What are the current stock market trends today?"
        
        response = await scholar_agent.arun(web_search_query)
        response_content = str(response.content) if response and response.content else ""
        
        evaluation = await judge.evaluate(response_content)
        
        assert evaluation["success"], f"Web search tool usage failed: {evaluation['criteria_results']}"
        # Scholar should always search for current information
        assert len(response_content) > 50, "Response suggests tool usage occurred"

    @pytest.mark.agent_test
    @pytest.mark.asyncio
    async def test_tool_selection_logic(self, sage_agent, mock_judge):
        """Test agent's ability to select appropriate tools for different query types."""
        judge = mock_judge([
            "The agent selects the most appropriate tool for the query type",
            "The agent uses tools in the correct sequence",
            "The agent fallback to alternative tools when needed"
        ])
        
        # Test different query types that should trigger different tool usage
        queries = [
            "Search for recent news about climate change",  # Should use web search
            "What's in our knowledge base about customer service?",  # Should search KB
            "Tell me about Python programming basics"  # Could use either/both
        ]
        
        for query in queries:
            response = await sage_agent.arun(query)
            response_content = str(response.content) if response and response.content else ""
            
            evaluation = await judge.evaluate(response_content)
            assert len(response_content) > 30, f"Tool selection failed for query: {query}"

    @pytest.mark.agent_test
    @pytest.mark.asyncio
    async def test_tool_error_handling(self, scholar_agent, mock_judge):
        """Test agent's handling of tool errors and failures."""
        judge = mock_judge([
            "The agent handles tool failures gracefully",
            "The agent provides alternative responses when tools fail",
            "The agent maintains helpful behavior despite tool issues"
        ])
        
        # Query that might cause tool issues or empty results
        edge_case_query = "Find information about a completely made-up topic: flibbertigibbet technology"
        
        response = await scholar_agent.arun(edge_case_query)
        response_content = str(response.content) if response and response.content else ""
        
        evaluation = await judge.evaluate(response_content)
        
        # Agent should still provide a helpful response even if tools don't find results
        assert len(response_content) > 20, "Agent should handle tool failures gracefully"
        assert evaluation["overall_score"] > 0.5, "Error handling quality insufficient"


class TestConversationalFlowAndMemory:
    """Test suite for conversational flow and memory management."""

    @pytest.mark.agent_test
    @pytest.mark.asyncio
    async def test_conversation_context_maintenance(self, sage_agent, mock_judge):
        """Test agent's ability to maintain context across conversation turns."""
        judge = mock_judge([
            "The agent remembers previous context in follow-up responses",
            "The agent maintains coherent conversation flow",
            "The agent builds upon previous exchanges appropriately"
        ])
        
        # Multi-turn conversation
        turn1 = "I'm interested in learning about artificial intelligence"
        turn2 = "What are the main applications of it?"
        turn3 = "How about in healthcare specifically?"
        
        response1 = await sage_agent.arun(turn1)
        response1_content = str(response1.content) if response1 and response1.content else ""
        
        response2 = await sage_agent.arun(turn2)
        response2_content = str(response2.content) if response2 and response2.content else ""
        
        response3 = await sage_agent.arun(turn3)
        response3_content = str(response3.content) if response3 and response3.content else ""
        
        # Evaluate context maintenance
        evaluation = await judge.evaluate(response3_content, context=response1_content + response2_content)
        
        assert evaluation["success"], f"Context maintenance failed: {evaluation['criteria_results']}"
        # Response 2 should reference "AI" or "artificial intelligence"
        assert "ai" in response2_content.lower() or "artificial" in response2_content.lower()
        # Response 3 should reference "healthcare" and show context understanding
        assert "healthcare" in response3_content.lower()

    @pytest.mark.agent_test
    @pytest.mark.asyncio
    async def test_conversation_history_recall(self, scholar_agent, mock_judge):
        """Test agent's ability to recall information from conversation history."""
        judge = mock_judge([
            "The agent can reference specific details from earlier in conversation",
            "The agent maintains accurate recall of previous statements",
            "The agent uses conversation history to provide better responses"
        ])
        
        # Establish context
        context_establishment = "My name is Alex and I work in renewable energy research"
        
        # Later reference
        history_reference = "Based on what I told you about my work, what topics should I focus on?"
        
        response1 = await scholar_agent.arun(context_establishment)
        response2 = await scholar_agent.arun(history_reference)
        response2_content = str(response2.content) if response2 and response2.content else ""
        
        evaluation = await judge.evaluate(response2_content, context=context_establishment)
        
        assert evaluation["success"], f"History recall failed: {evaluation['criteria_results']}"
        # Should reference renewable energy or related topics
        energy_keywords = ["renewable", "energy", "sustainability", "solar", "wind"]
        assert any(keyword in response2_content.lower() for keyword in energy_keywords)

    @pytest.mark.agent_test
    @pytest.mark.asyncio
    async def test_memory_persistence_across_sessions(self, sage_agent, mock_judge):
        """Test agent's memory persistence capabilities."""
        judge = mock_judge([
            "The agent stores important information for future reference",
            "The agent can retrieve stored information when relevant",
            "The agent maintains user preferences and context"
        ])
        
        # This test would need actual session persistence
        # For now, test within-session memory
        preference_setting = "I prefer technical explanations with detailed examples"
        later_query = "Explain machine learning to me"
        
        response1 = await sage_agent.arun(preference_setting)
        response2 = await sage_agent.arun(later_query)
        response2_content = str(response2.content) if response2 and response2.content else ""
        
        evaluation = await judge.evaluate(response2_content, context=preference_setting)
        
        # Check if response style matches stated preference
        technical_indicators = ["algorithm", "model", "data", "training", "parameters"]
        technical_score = sum(1 for indicator in technical_indicators if indicator in response2_content.lower())
        
        assert technical_score >= 2, "Response should reflect technical preference"
        assert len(response2_content) > 100, "Response should be detailed as preferred"

    @pytest.mark.agent_test
    @pytest.mark.asyncio
    async def test_conversation_flow_coherence(self, operator_agent, mock_judge):
        """Test overall conversation flow coherence and natural progression."""
        judge = mock_judge([
            "The conversation follows logical progression",
            "The agent maintains appropriate tone and style",
            "The agent provides smooth transitions between topics"
        ])
        
        # Simulate natural conversation flow
        conversation_turns = [
            "Hello, I need help with a project",
            "It's about implementing AI in education",
            "What are the key considerations I should think about?",
            "How do I get started with a pilot program?"
        ]
        
        responses = []
        for turn in conversation_turns:
            response = await operator_agent.arun(turn)
            response_content = str(response.content) if response and response.content else ""
            responses.append(response_content)
        
        # Evaluate final response in context of full conversation
        full_context = " ".join(responses[:-1])
        evaluation = await judge.evaluate(responses[-1], context=full_context)
        
        assert evaluation["success"], f"Conversation flow failed: {evaluation['criteria_results']}"
        
        # Check for topic consistency across turns
        education_keywords = ["education", "learning", "student", "teaching", "curriculum"]
        ai_keywords = ["ai", "artificial", "intelligence", "machine", "algorithm"]
        
        final_response = responses[-1].lower()
        assert any(keyword in final_response for keyword in education_keywords)
        assert any(keyword in final_response for keyword in ai_keywords)
