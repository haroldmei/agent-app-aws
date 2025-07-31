"""
Base test classes for the agentic AI test framework.
"""

import asyncio
import time
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum

import pytest

# Type definitions for when agno is not available
try:
    from agno.agent import Agent
    from agno.team import Team
    from agno.models.response import RunResponse, RunResponseEvent
except ImportError:
    # Fallback for when agno is not available or has different imports
    from typing import Any as Agent, Any as Team, Any as RunResponse, Any as RunResponseEvent


class TestSeverity(Enum):
    """Test severity levels for CI/CD filtering"""
    CRITICAL = "critical"  # Must pass for release
    HIGH = "high"        # Should pass for release
    MEDIUM = "medium"    # Can be addressed post-release
    LOW = "low"         # Nice to have


class TestCategory(Enum):
    """Test categories based on QA.md framework"""
    RAG_CORE = "rag_core"
    AGENT_BEHAVIOR = "agent_behavior"
    TEAM_ORCHESTRATION = "team_orchestration"
    QUALITY_SAFETY = "quality_safety"
    PERFORMANCE = "performance"


@dataclass
class TestResult:
    """Standardized test result structure"""
    test_name: str
    category: TestCategory
    severity: TestSeverity
    passed: bool
    score: Optional[float]
    threshold: Optional[float]
    metrics: Dict[str, Any]
    execution_time: float
    error_message: Optional[str] = None
    artifacts: Dict[str, Any] = None


class BaseTest(ABC):
    """Base class for all agentic AI tests"""
    
    def __init__(self, name: str, category: TestCategory, severity: TestSeverity):
        self.name = name
        self.category = category
        self.severity = severity
        self.results: List[TestResult] = []
    
    def setup(self):
        """Setup method called before each test"""
        pass
    
    def teardown(self):
        """Teardown method called after each test"""
        pass
    
    @abstractmethod
    async def run(self) -> TestResult:
        """Execute the test and return results"""
        pass
    
    def _create_result(self, passed: bool, score: Optional[float] = None, 
                      threshold: Optional[float] = None, metrics: Dict[str, Any] = None,
                      execution_time: float = 0.0, error_message: Optional[str] = None,
                      artifacts: Dict[str, Any] = None) -> TestResult:
        """Helper to create standardized test results"""
        return TestResult(
            test_name=self.name,
            category=self.category,
            severity=self.severity,
            passed=passed,
            score=score,
            threshold=threshold,
            metrics=metrics or {},
            execution_time=execution_time,
            error_message=error_message,
            artifacts=artifacts or {}
        )


class BaseAgentTest(BaseTest):
    """Base class for individual agent tests"""
    
    def __init__(self, name: str, agent: Agent, category: TestCategory, 
                 severity: TestSeverity = TestSeverity.HIGH):
        super().__init__(name, category, severity)
        self.agent = agent
    
    async def run_agent(self, message: str, **kwargs) -> RunResponse:
        """Run agent with standardized error handling"""
        try:
            start_time = time.time()
            response = await self.agent.arun(message, **kwargs)
            execution_time = time.time() - start_time
            return response, execution_time
        except Exception as e:
            execution_time = time.time() - start_time
            raise Exception(f"Agent execution failed after {execution_time:.2f}s: {str(e)}")


class BaseTeamTest(BaseTest):
    """Base class for team tests"""
    
    def __init__(self, name: str, team: Team, category: TestCategory,
                 severity: TestSeverity = TestSeverity.HIGH):
        super().__init__(name, category, severity)
        self.team = team
    
    async def run_team(self, message: str, **kwargs) -> RunResponse:
        """Run team with standardized error handling"""
        try:
            start_time = time.time()
            response = await self.team.arun(message, **kwargs)
            execution_time = time.time() - start_time
            return response, execution_time
        except Exception as e:
            execution_time = time.time() - start_time
            raise Exception(f"Team execution failed after {execution_time:.2f}s: {str(e)}")


class BaseSystemTest(BaseTest):
    """Base class for end-to-end system tests"""
    
    def __init__(self, name: str, agents: List[Agent], teams: List[Team],
                 category: TestCategory, severity: TestSeverity = TestSeverity.CRITICAL):
        super().__init__(name, category, severity)
        self.agents = agents
        self.teams = teams
    
    async def run_system_scenario(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Run a complex system scenario"""
        results = {}
        start_time = time.time()
        
        try:
            # Execute scenario steps
            for step in scenario.get("steps", []):
                step_type = step.get("type")
                if step_type == "agent":
                    agent_name = step.get("agent")
                    agent = next((a for a in self.agents if a.name == agent_name), None)
                    if agent:
                        response, exec_time = await self.run_agent_step(agent, step)
                        results[f"agent_{agent_name}"] = {"response": response, "time": exec_time}
                
                elif step_type == "team":
                    team_name = step.get("team")
                    team = next((t for t in self.teams if t.name == team_name), None)
                    if team:
                        response, exec_time = await self.run_team_step(team, step)
                        results[f"team_{team_name}"] = {"response": response, "time": exec_time}
            
            total_time = time.time() - start_time
            results["total_execution_time"] = total_time
            return results
            
        except Exception as e:
            total_time = time.time() - start_time
            raise Exception(f"System scenario failed after {total_time:.2f}s: {str(e)}")
    
    async def run_agent_step(self, agent: Agent, step: Dict[str, Any]) -> Tuple[RunResponse, float]:
        """Execute an agent step in the system scenario"""
        start_time = time.time()
        message = step.get("message", "")
        kwargs = step.get("kwargs", {})
        response = await agent.arun(message, **kwargs)
        execution_time = time.time() - start_time
        return response, execution_time
    
    async def run_team_step(self, team: Team, step: Dict[str, Any]) -> Tuple[RunResponse, float]:
        """Execute a team step in the system scenario"""
        start_time = time.time()
        message = step.get("message", "")
        kwargs = step.get("kwargs", {})
        response = await team.arun(message, **kwargs)
        execution_time = time.time() - start_time
        return response, execution_time
