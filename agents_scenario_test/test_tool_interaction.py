import pytest
import scenario


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_sage_knowledge_base_tool_usage(sage_adapter):
    """Test Sage agent's proper use of knowledge base search tools."""
    result = await scenario.run(
        name="knowledge base tool usage",
        description="""
            User asks about company policies or internal information that should be
            available in the knowledge base. The agent should use knowledge base
            search tools appropriately and integrate the results effectively.
        """,
        agents=[
            sage_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "The agent correctly identifies when to use knowledge base search",
                    "The agent uses appropriate search parameters and queries",
                    "The agent integrates knowledge base results into a coherent response",
                    "The agent handles cases where information is not found gracefully",
                ],
            ),
        ],
    )
    assert result.success


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_scholar_web_search_tool_usage(scholar_adapter):
    """Test Scholar agent's proper use of DuckDuckGo web search tools."""
    result = await scenario.run(
        name="web search tool usage",
        description="""
            User asks about current events or recent developments that require
            web searching. The agent should use DuckDuckGo search tools effectively
            and present the information clearly.
        """,
        agents=[
            scholar_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "The agent uses DuckDuckGo search tool when appropriate for current information",
                    "The agent constructs effective search queries for the user's request",
                    "The agent processes and presents search results clearly and accurately",
                    "The agent distinguishes between search results and its own analysis",
                ],
            ),
        ],
    )
    assert result.success


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_sage_tool_selection_logic(sage_adapter):
    """Test Sage agent's ability to select appropriate tools for different query types."""
    result = await scenario.run(
        name="tool selection logic",
        description="""
            User asks different types of questions that should trigger different tool usage:
            some requiring knowledge base search, others web search, and some general knowledge.
            The agent should select the most appropriate tool for each query type.
        """,
        agents=[
            sage_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "The agent selects the most appropriate tool for each query type",
                    "The agent demonstrates logic in tool selection decisions",
                    "The agent uses tools in the correct sequence when multiple tools are needed",
                    "The agent explains its tool usage decisions when relevant",
                ],
            ),
        ],
    )
    assert result.success


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_scholar_tool_parameter_accuracy(scholar_adapter):
    """Test Scholar agent's accuracy in tool parameter configuration."""
    result = await scenario.run(
        name="tool parameter accuracy",
        description="""
            User asks specific questions that require precise search parameters.
            The agent should configure search tools with appropriate keywords,
            filters, and parameters to get relevant results.
        """,
        agents=[
            scholar_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "The agent configures search tools with relevant and specific parameters",
                    "The agent uses appropriate keywords derived from user queries",
                    "The agent adjusts search parameters based on initial results if needed",
                    "The agent demonstrates understanding of tool capabilities and limitations",
                ],
            ),
        ],
    )
    assert result.success


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_sage_tool_error_handling(sage_adapter):
    """Test Sage agent's handling of tool errors and failures."""
    result = await scenario.run(
        name="tool error handling",
        description="""
            User makes requests that might cause tool issues: network problems,
            empty search results, or malformed queries. The agent should handle
            these gracefully and provide alternative solutions.
        """,
        agents=[
            sage_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "The agent handles tool failures gracefully without crashing",
                    "The agent provides alternative responses when tools fail or return empty results",
                    "The agent maintains helpful behavior despite technical difficulties",
                    "The agent explains limitations and suggests alternative approaches when appropriate",
                ],
            ),
        ],
    )
    assert result.success


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_scholar_multi_tool_workflow(scholar_adapter):
    """Test Scholar agent's ability to coordinate multiple tools in a single response."""
    result = await scenario.run(
        name="multi-tool workflow",
        description="""
            User asks a complex question that requires using multiple search strategies
            or different types of information gathering. The agent should coordinate
            multiple tool uses effectively to provide a comprehensive answer.
        """,
        agents=[
            scholar_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "The agent uses multiple tools in a logical sequence",
                    "The agent synthesizes information from different tool outputs",
                    "The agent coordinates tool usage to build a comprehensive response",
                    "The agent manages tool interactions efficiently without redundancy",
                ],
            ),
        ],
    )
    assert result.success


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_sage_tool_result_integration(sage_adapter):
    """Test Sage agent's ability to integrate tool results with its own knowledge."""
    result = await scenario.run(
        name="tool result integration",
        description="""
            User asks questions where the agent should combine information from
            tool searches with its own knowledge to provide enhanced responses.
            The agent should seamlessly blend different information sources.
        """,
        agents=[
            sage_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "The agent seamlessly integrates tool results with its own knowledge",
                    "The agent provides enhanced responses by combining multiple information sources",
                    "The agent clearly distinguishes between different sources when appropriate",
                    "The agent creates coherent narratives from diverse information sources",
                ],
            ),
        ],
    )
    assert result.success
