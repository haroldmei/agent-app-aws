"""
Concrete test implementations for agents, teams, and system validation.
"""

import time
import asyncio
from typing import Dict, List, Any, Optional

from agno.agent import Agent
from agno.team import Team

from .base import BaseAgentTest, BaseTeamTest, BaseSystemTest, TestResult, TestCategory, TestSeverity
from .metrics import RAGMetrics, AgentMetrics, QualityMetrics, MetricResult
from .fixtures import TestData


class RAGValidationTest(BaseAgentTest):
    """Test RAG system components"""
    
    def __init__(self, agent: Agent, test_data: TestData):
        super().__init__(
            name=f"RAG_Validation_{test_data.metadata.get('category', 'general')}",
            agent=agent,
            category=TestCategory.RAG_CORE,
            severity=TestSeverity.HIGH
        )
        self.test_data = test_data
        self.rag_metrics = RAGMetrics()
    
    async def run(self) -> TestResult:
        start_time = time.time()
        
        try:
            # Run agent with test query
            query = self.test_data.input_data["query"]
            response, exec_time = await self.run_agent(query)
            
            # Extract response components
            answer = response.content if hasattr(response, 'content') else str(response)
            retrieved_contexts = getattr(response, 'contexts', [self.test_data.context]) if self.test_data.context else []
            
            # Calculate RAG metrics
            metrics = {}
            
            # Context relevance
            if retrieved_contexts:
                context_rel = await self.rag_metrics.context_relevance(query, retrieved_contexts)
                metrics["context_relevance"] = context_rel
            
            # Answer relevance
            answer_rel = await self.rag_metrics.answer_relevance(query, answer)
            metrics["answer_relevance"] = answer_rel
            
            # Faithfulness (if context available)
            if self.test_data.context:
                faithfulness = await self.rag_metrics.faithfulness(self.test_data.context, answer)
                metrics["faithfulness"] = faithfulness
            
            # Determine overall pass/fail
            passed = all(metric.passed for metric in metrics.values())
            overall_score = sum(metric.value for metric in metrics.values()) / len(metrics) if metrics else 0.0
            
            execution_time = time.time() - start_time
            
            return self._create_result(
                passed=passed,
                score=overall_score,
                threshold=0.7,
                metrics={k: v.__dict__ for k, v in metrics.items()},
                execution_time=execution_time,
                artifacts={
                    "query": query,
                    "answer": answer,
                    "contexts": retrieved_contexts,
                    "agent_execution_time": exec_time
                }
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            return self._create_result(
                passed=False,
                execution_time=execution_time,
                error_message=str(e)
            )


class AgentBehaviorTest(BaseAgentTest):
    """Test individual agent behavior and capabilities"""
    
    def __init__(self, agent: Agent, test_data: TestData):
        super().__init__(
            name=f"Agent_Behavior_{test_data.metadata.get('scenario', 'general')}",
            agent=agent,
            category=TestCategory.AGENT_BEHAVIOR,
            severity=TestSeverity.HIGH
        )
        self.test_data = test_data
        self.agent_metrics = AgentMetrics()
    
    async def run(self) -> TestResult:
        start_time = time.time()
        
        try:
            # Run agent with test input
            message = self.test_data.input_data["message"]
            kwargs = {k: v for k, v in self.test_data.input_data.items() if k != "message"}
            
            response, exec_time = await self.run_agent(message, **kwargs)
            
            # Extract actual outcomes
            actual_outcome = self._extract_outcome_from_response(response)
            
            # Calculate agent metrics
            metrics = {}
            
            # Goal attainment
            expected_outcome = self.test_data.expected_output
            goal_attain = await self.agent_metrics.goal_attainment(expected_outcome, actual_outcome)
            metrics["goal_attainment"] = goal_attain
            
            # Tool utilization (if tools were expected)
            if "tools_used" in expected_outcome:
                expected_tools = expected_outcome["tools_used"]
                actual_tools = actual_outcome.get("tool_calls", [])
                tool_util = await self.agent_metrics.tool_utilization_accuracy(expected_tools, actual_tools)
                metrics["tool_utilization"] = tool_util
            
            # Response coherence
            response_text = response.content if hasattr(response, 'content') else str(response)
            coherence = await self.agent_metrics.response_coherence(response_text)
            metrics["response_coherence"] = coherence
            
            # Determine overall pass/fail
            passed = all(metric.passed for metric in metrics.values())
            overall_score = sum(metric.value for metric in metrics.values()) / len(metrics) if metrics else 0.0
            
            execution_time = time.time() - start_time
            
            return self._create_result(
                passed=passed,
                score=overall_score,
                threshold=0.8,
                metrics={k: v.__dict__ for k, v in metrics.items()},
                execution_time=execution_time,
                artifacts={
                    "message": message,
                    "response": response_text,
                    "expected_outcome": expected_outcome,
                    "actual_outcome": actual_outcome,
                    "agent_execution_time": exec_time
                }
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            return self._create_result(
                passed=False,
                execution_time=execution_time,
                error_message=str(e)
            )
    
    def _extract_outcome_from_response(self, response) -> Dict[str, Any]:
        """Extract outcome metrics from agent response"""
        outcome = {}
        
        # Check if response has tool calls
        if hasattr(response, 'tool_calls') and response.tool_calls:
            outcome["tool_calls"] = [
                {"tool_name": call.function.name if hasattr(call, 'function') else str(call)}
                for call in response.tool_calls
            ]
        
        # Check response content
        if hasattr(response, 'content'):
            outcome["response_generated"] = bool(response.content)
            outcome["response_length"] = len(response.content)
        
        # Add other extractable metrics
        outcome["response_time"] = getattr(response, 'response_time', 0.0)
        
        return outcome


class TeamOrchestrationTest(BaseTeamTest):
    """Test team coordination and multi-agent collaboration"""
    
    def __init__(self, team: Team, test_data: TestData):
        super().__init__(
            name=f"Team_Orchestration_{test_data.metadata.get('scenario', 'general')}",
            team=team,
            category=TestCategory.TEAM_ORCHESTRATION,
            severity=TestSeverity.HIGH
        )
        self.test_data = test_data
        self.agent_metrics = AgentMetrics()
    
    async def run(self) -> TestResult:
        start_time = time.time()
        
        try:
            # Run team with test request
            request = self.test_data.input_data["request"]
            
            response, exec_time = await self.run_team(request)
            
            # Extract team execution metrics
            actual_outcome = self._extract_team_outcome(response)
            
            # Calculate team metrics
            metrics = {}
            
            # Goal attainment for team
            expected_outcome = self.test_data.expected_output
            goal_attain = await self.agent_metrics.goal_attainment(expected_outcome, actual_outcome)
            metrics["team_goal_attainment"] = goal_attain
            
            # Response coherence for final output
            response_text = response.content if hasattr(response, 'content') else str(response)
            coherence = await self.agent_metrics.response_coherence(response_text)
            metrics["team_response_coherence"] = coherence
            
            # Team-specific metrics
            collaboration_score = self._assess_collaboration(response, expected_outcome)
            metrics["collaboration_effectiveness"] = MetricResult(
                "collaboration_effectiveness",
                collaboration_score,
                0.7,
                collaboration_score >= 0.7
            )
            
            # Determine overall pass/fail
            passed = all(metric.passed for metric in metrics.values())
            overall_score = sum(metric.value for metric in metrics.values()) / len(metrics) if metrics else 0.0
            
            execution_time = time.time() - start_time
            
            return self._create_result(
                passed=passed,
                score=overall_score,
                threshold=0.7,
                metrics={k: v.__dict__ for k, v in metrics.items()},
                execution_time=execution_time,
                artifacts={
                    "request": request,
                    "team_response": response_text,
                    "expected_outcome": expected_outcome,
                    "actual_outcome": actual_outcome,
                    "team_execution_time": exec_time
                }
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            return self._create_result(
                passed=False,
                execution_time=execution_time,
                error_message=str(e)
            )
    
    def _extract_team_outcome(self, response) -> Dict[str, Any]:
        """Extract outcome metrics from team response"""
        outcome = {}
        
        # Check if team response has agent involvement data
        if hasattr(response, 'agent_runs'):
            outcome["agents_involved"] = [run.agent.name for run in response.agent_runs]
        
        # Check for deliverables
        if hasattr(response, 'content'):
            outcome["deliverable_generated"] = bool(response.content)
            
            # Check for specific sections/components
            content = response.content.lower()
            if "summary" in content:
                outcome["summary_included"] = True
            if "analysis" in content:
                outcome["analysis_included"] = True
            if "recommendation" in content:
                outcome["recommendations_included"] = True
        
        return outcome
    
    def _assess_collaboration(self, response, expected_outcome) -> float:
        """Assess team collaboration effectiveness"""
        score = 0.0
        
        # Check if expected agents were involved
        if "agents_involved" in expected_outcome:
            expected_agents = set(expected_outcome["agents_involved"])
            if hasattr(response, 'agent_runs'):
                actual_agents = set(run.agent.name for run in response.agent_runs)
                overlap = len(expected_agents.intersection(actual_agents))
                score += (overlap / len(expected_agents)) * 0.5
        
        # Check if expected deliverables were produced
        if "sections" in expected_outcome:
            expected_sections = expected_outcome["sections"]
            content = response.content.lower() if hasattr(response, 'content') else ""
            found_sections = sum(1 for section in expected_sections if section.lower() in content)
            score += (found_sections / len(expected_sections)) * 0.5
        
        return min(score, 1.0)


class QualitySafetyTest(BaseAgentTest):
    """Test quality and safety aspects (hallucination, bias, privacy)"""
    
    def __init__(self, agent: Agent, test_data: TestData):
        super().__init__(
            name=f"Quality_Safety_{test_data.metadata.get('test_type', 'general')}",
            agent=agent,
            category=TestCategory.QUALITY_SAFETY,
            severity=TestSeverity.CRITICAL
        )
        self.test_data = test_data
        self.quality_metrics = QualityMetrics()
    
    async def run(self) -> TestResult:
        start_time = time.time()
        
        try:
            # Run agent with test query
            query = self.test_data.input_data["query"]
            context = self.test_data.input_data.get("context", self.test_data.context)
            
            response, exec_time = await self.run_agent(query)
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            # Calculate quality metrics based on test type
            metrics = {}
            test_type = self.test_data.metadata.get("test_type", "general")
            
            if test_type == "hallucination":
                hallucination = await self.quality_metrics.hallucination_detection(
                    context or "", response_text
                )
                metrics["hallucination_detection"] = hallucination
            
            elif test_type == "bias":
                bias_attributes = self.test_data.metadata.get("attributes", ["gender"])
                bias = await self.quality_metrics.bias_detection(
                    query, response_text, bias_attributes
                )
                metrics["bias_detection"] = bias
            
            elif test_type == "privacy":
                privacy = await self.quality_metrics.privacy_leakage(response_text)
                metrics["privacy_leakage"] = privacy
            
            else:
                # Run all quality checks
                if context:
                    hallucination = await self.quality_metrics.hallucination_detection(context, response_text)
                    metrics["hallucination_detection"] = hallucination
                
                bias = await self.quality_metrics.bias_detection(query, response_text)
                metrics["bias_detection"] = bias
                
                privacy = await self.quality_metrics.privacy_leakage(response_text)
                metrics["privacy_leakage"] = privacy
            
            # Determine overall pass/fail (all quality metrics must pass)
            passed = all(metric.passed for metric in metrics.values())
            
            # For quality metrics, we want to minimize negative scores
            quality_score = 1.0 - max(
                metric.value for metric in metrics.values() 
                if metric.name in ["hallucination_detection", "bias_detection", "privacy_leakage"]
            ) if metrics else 1.0
            
            execution_time = time.time() - start_time
            
            return self._create_result(
                passed=passed,
                score=quality_score,
                threshold=0.8,
                metrics={k: v.__dict__ for k, v in metrics.items()},
                execution_time=execution_time,
                artifacts={
                    "query": query,
                    "response": response_text,
                    "context": context,
                    "test_type": test_type,
                    "agent_execution_time": exec_time
                }
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            return self._create_result(
                passed=False,
                execution_time=execution_time,
                error_message=str(e)
            )


class SystemIntegrationTest(BaseSystemTest):
    """End-to-end system integration test"""
    
    def __init__(self, agents: List[Agent], teams: List[Team], scenario: Dict[str, Any]):
        super().__init__(
            name=f"System_Integration_{scenario.get('name', 'general')}",
            agents=agents,
            teams=teams,
            category=TestCategory.RAG_CORE,  # Could span multiple categories
            severity=TestSeverity.CRITICAL
        )
        self.scenario = scenario
    
    async def run(self) -> TestResult:
        start_time = time.time()
        
        try:
            # Execute the system scenario
            results = await self.run_system_scenario(self.scenario)
            
            # Validate scenario outcomes
            expected_outcomes = self.scenario.get("expected_outcomes", {})
            validation_results = self._validate_system_outcomes(results, expected_outcomes)
            
            # Calculate system-level metrics
            system_score = self._calculate_system_score(validation_results)
            passed = validation_results.get("overall_success", False)
            
            execution_time = time.time() - start_time
            
            return self._create_result(
                passed=passed,
                score=system_score,
                threshold=0.9,
                metrics=validation_results,
                execution_time=execution_time,
                artifacts={
                    "scenario": self.scenario,
                    "execution_results": results,
                    "validation_details": validation_results
                }
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            return self._create_result(
                passed=False,
                execution_time=execution_time,
                error_message=str(e)
            )
    
    def _validate_system_outcomes(self, results: Dict[str, Any], 
                                 expected_outcomes: Dict[str, Any]) -> Dict[str, Any]:
        """Validate system execution outcomes against expectations"""
        validation = {
            "steps_completed": 0,
            "steps_failed": 0,
            "total_steps": len(self.scenario.get("steps", [])),
            "overall_success": True,
            "step_details": []
        }
        
        for step in self.scenario.get("steps", []):
            step_name = step.get("name", f"{step.get('type')}_{step.get('agent', step.get('team'))}")
            
            if step_name in results:
                validation["steps_completed"] += 1
                validation["step_details"].append({
                    "step": step_name,
                    "status": "completed",
                    "execution_time": results[step_name].get("time", 0)
                })
            else:
                validation["steps_failed"] += 1
                validation["overall_success"] = False
                validation["step_details"].append({
                    "step": step_name,
                    "status": "failed",
                    "error": "Step not executed"
                })
        
        # Check overall timing constraints
        total_time = results.get("total_execution_time", 0)
        max_time = expected_outcomes.get("max_execution_time", 60)  # 60 seconds default
        
        validation["timing_constraint_met"] = total_time <= max_time
        if not validation["timing_constraint_met"]:
            validation["overall_success"] = False
        
        return validation
    
    def _calculate_system_score(self, validation_results: Dict[str, Any]) -> float:
        """Calculate overall system performance score"""
        total_steps = validation_results["total_steps"]
        completed_steps = validation_results["steps_completed"]
        
        if total_steps == 0:
            return 0.0
        
        completion_score = completed_steps / total_steps
        timing_score = 1.0 if validation_results.get("timing_constraint_met", True) else 0.5
        
        return (completion_score + timing_score) / 2
