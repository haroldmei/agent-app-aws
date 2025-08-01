import pytest
import scenario


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_sage_knowledge_retrieval_task_completion(sage_adapter):
    """Test Sage agent's ability to complete knowledge retrieval tasks."""
    result = await scenario.run(
        name="knowledge retrieval task",
        description="""
            User asks for information about artificial intelligence and machine learning concepts.
            The agent should provide comprehensive, accurate information using its knowledge base
            and web search capabilities when needed.
        """,
        agents=[
            sage_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "The agent provides comprehensive information about the requested topic",
                    "The agent uses appropriate tools (knowledge base search or web search) to gather information",
                    "The agent completes the information retrieval workflow successfully",
                    "The agent's response demonstrates understanding of the query context",
                ],
            ),
        ],
    )
    assert result.success


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_scholar_research_task_completion(scholar_adapter):
    """Test Scholar agent's ability to complete research tasks."""
    result = await scenario.run(
        name="research task completion",
        description="""
            User requests current information about renewable energy developments.
            The agent should search for up-to-date information and provide a detailed analysis.
        """,
        agents=[
            scholar_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "The agent attempts to search for current information or acknowledges information limitations",
                    "The agent provides detailed analysis with relevant context",
                    "The agent completes the research workflow from query to comprehensive response", 
                    "The agent demonstrates understanding of the research request",
                ],
            ),
        ],
    )
    assert result.success


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_sage_multi_step_information_synthesis(sage_adapter):
    """Test Sage agent's ability to handle complex multi-step information requests."""
    result = await scenario.run(
        name="multi-step synthesis task",
        description="""
            User asks for a comprehensive overview that requires multiple information sources:
            understanding AI principles, current applications in healthcare, and future developments.
            The agent should break down the query and provide structured responses.
        """,
        agents=[
            sage_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "The agent addresses all components of the multi-part query",
                    "The agent structures the response logically with clear sections",
                    "The agent demonstrates knowledge synthesis or acknowledges information limitations",
                    "The agent completes the complex task with comprehensive coverage",
                ],
            ),
        ],
    )
    assert result.success


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_scholar_goal_oriented_conversation(scholar_adapter):
    """Test Scholar agent's ability to maintain goal orientation across conversation turns."""
    result = await scenario.run(
        name="goal-oriented conversation",
        description="""
            User wants to plan a sustainable energy solution for a small business.
            This is a multi-turn conversation where the user asks follow-up questions
            about costs, implementation, and benefits. The agent should maintain focus
            on the stated goal throughout the conversation.
        """,
        agents=[
            scholar_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "The agent maintains focus on the sustainable energy goal throughout",
                    "The agent provides practical, actionable advice for small business context",
                    "The agent addresses follow-up questions while staying on topic",
                    "The agent successfully guides the conversation toward goal achievement",
                ],
            ),
        ],
    )
    assert result.success


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_sage_complex_planning_task(sage_adapter):
    """Test Sage agent's planning and task breakdown capabilities."""
    result = await scenario.run(
        name="complex planning task",
        description="""
            User needs help creating a learning plan for data science over 6 months.
            The agent should break down this complex goal into structured phases,
            recommend resources, and provide a timeline.
        """,
        agents=[
            sage_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "The agent breaks down the complex goal into manageable phases",
                    "The agent provides a structured timeline and milestones",
                    "The agent recommends specific resources and learning materials",
                    "The agent completes the planning task with actionable outcomes",
                ],
            ),
        ],
    )
    assert result.success
