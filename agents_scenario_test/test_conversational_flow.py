import pytest
import scenario


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_sage_conversation_context_maintenance(sage_adapter):
    """Test Sage agent's ability to maintain context across conversation turns."""
    result = await scenario.run(
        name="conversation context maintenance",
        description="""
            User has a multi-turn conversation about artificial intelligence,
            starting with basic concepts, then asking follow-up questions about
            specific applications and implementations. The agent should maintain
            context and build upon previous exchanges.
        """,
        agents=[
            sage_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "The agent remembers previous context in follow-up responses",
                    "The agent maintains coherent conversation flow across multiple turns",
                    "The agent builds upon previous exchanges appropriately",
                    "The agent references earlier parts of the conversation when relevant",
                ],
            ),
        ],
    )
    assert result.success


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_scholar_conversation_history_recall(scholar_adapter):
    """Test Scholar agent's ability to recall information from conversation history."""
    result = await scenario.run(
        name="conversation history recall",
        description="""
            User establishes context early in the conversation (mentions their profession,
            interests, or specific needs), then later asks questions that should reference
            this earlier context. The agent should demonstrate accurate recall.
        """,
        agents=[
            scholar_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "The agent accurately recalls specific details from earlier in the conversation",
                    "The agent uses conversation history to provide more relevant and personalized responses",
                    "The agent maintains accurate recall of user-provided information",
                    "The agent demonstrates understanding of conversational context over time",
                ],
            ),
        ],
    )
    assert result.success


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_sage_conversation_flow_coherence(sage_adapter):
    """Test Sage agent's overall conversation flow coherence and natural progression."""
    result = await scenario.run(
        name="conversation flow coherence",
        description="""
            User engages in a natural conversation flow about a complex topic,
            with topic transitions, digressions, and returns to previous points.
            The agent should maintain coherent flow and handle transitions smoothly.
        """,
        agents=[
            sage_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "The conversation follows logical progression with smooth transitions",
                    "The agent maintains appropriate tone and style throughout the conversation",
                    "The agent handles topic transitions and digressions naturally",
                    "The agent can return to previous topics when the user redirects",
                ],
            ),
        ],
    )
    assert result.success


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_scholar_memory_persistence_in_session(scholar_adapter):
    """Test Scholar agent's memory persistence capabilities within a session."""
    result = await scenario.run(
        name="memory persistence in session",
        description="""
            User sets preferences or provides personal information early in the session,
            then continues the conversation with requests that should reflect those
            preferences. The agent should consistently apply learned preferences.
        """,
        agents=[
            scholar_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "The agent stores and applies user preferences consistently",
                    "The agent maintains context about user needs throughout the session",
                    "The agent personalizes responses based on earlier conversation",
                    "The agent demonstrates long-term memory within the conversation session",
                ],
            ),
        ],
    )
    assert result.success


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_sage_contextual_question_handling(sage_adapter):
    """Test Sage agent's handling of contextual questions that require conversation awareness."""
    result = await scenario.run(
        name="contextual question handling",
        description="""
            User asks questions using pronouns, references, and contextual cues that
            require understanding of the conversation history (e.g., "tell me more about that",
            "what did you mean earlier", "how does this relate to what we discussed").
        """,
        agents=[
            sage_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "The agent correctly interprets contextual references and pronouns",
                    "The agent understands what 'that', 'this', 'earlier' refer to in context",
                    "The agent provides relevant responses to context-dependent questions",
                    "The agent maintains conversation awareness for ambiguous references",
                ],
            ),
        ],
    )
    assert result.success


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_scholar_conversation_state_management(scholar_adapter):
    """Test Scholar agent's management of conversation state and topic tracking."""
    result = await scenario.run(
        name="conversation state management",
        description="""
            User engages in a conversation that involves multiple topics, sub-topics,
            and levels of detail. The agent should track where they are in the
            conversation and manage topic state effectively.
        """,
        agents=[
            scholar_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "The agent tracks current topic and subtopic accurately",
                    "The agent manages conversation depth and breadth appropriately",
                    "The agent knows when to dive deeper vs. when to broaden the discussion",
                    "The agent maintains clear sense of where the conversation stands",
                ],
            ),
        ],
    )
    assert result.success


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_sage_interruption_and_resumption_handling(sage_adapter):
    """Test Sage agent's handling of conversation interruptions and resumptions."""
    result = await scenario.run(
        name="interruption and resumption handling",
        description="""
            User starts a topic, gets interrupted or distracted by another question,
            then wants to return to the original topic. The agent should handle
            these interruptions gracefully and resume appropriately.
        """,
        agents=[
            sage_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "The agent handles topic interruptions gracefully",
                    "The agent can resume previous topics when the user requests",
                    "The agent maintains awareness of multiple concurrent conversation threads",
                    "The agent provides smooth transitions between interrupted and resumed topics",
                ],
            ),
        ],
    )
    assert result.success


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_scholar_conversational_learning_adaptation(scholar_adapter):
    """Test Scholar agent's ability to adapt based on conversational learning."""
    result = await scenario.run(
        name="conversational learning and adaptation",
        description="""
            User provides feedback about their preferred communication style,
            level of detail, or specific interests. The agent should adapt its
            communication approach based on this feedback during the conversation.
        """,
        agents=[
            scholar_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "The agent adapts communication style based on user feedback",
                    "The agent learns user preferences and applies them consistently",
                    "The agent demonstrates improved responses after receiving guidance",
                    "The agent shows conversational learning and behavioral adaptation",
                ],
            ),
        ],
    )
    assert result.success
