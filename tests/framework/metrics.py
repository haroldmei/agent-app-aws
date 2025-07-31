"""
Metrics calculators for the agentic AI test framework.
Based on QA.md best practices for RAG, Agent behavior, and Quality assurance.
"""

import re
import json
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from abc import ABC, abstractmethod

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class MetricResult:
    """Standard metric result structure"""
    name: str
    value: float
    threshold: float
    passed: bool
    details: Dict[str, Any] = None


class BaseMetric(ABC):
    """Base class for all metrics"""
    
    def __init__(self, name: str, threshold: float = 0.7):
        self.name = name
        self.threshold = threshold
    
    @abstractmethod
    async def calculate(self, **kwargs) -> MetricResult:
        """Calculate the metric value"""
        pass
    
    def _create_result(self, value: float, details: Dict[str, Any] = None) -> MetricResult:
        """Helper to create metric results"""
        return MetricResult(
            name=self.name,
            value=value,
            threshold=self.threshold,
            passed=value >= self.threshold,
            details=details or {}
        )


class RAGMetrics:
    """RAG validation metrics based on QA.md section 2.1"""
    
    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2"):
        self.embedding_model = SentenceTransformer(embedding_model)
    
    async def context_relevance(self, query: str, retrieved_contexts: List[str], 
                              threshold: float = 0.7) -> MetricResult:
        """Measure how pertinent retrieved context is to the user query"""
        if not retrieved_contexts:
            return MetricResult("context_relevance", 0.0, threshold, False, 
                              {"error": "No contexts provided"})
        
        try:
            # Encode query and contexts
            query_embedding = self.embedding_model.encode([query])
            context_embeddings = self.embedding_model.encode(retrieved_contexts)
            
            # Calculate cosine similarities
            similarities = cosine_similarity(query_embedding, context_embeddings)[0]
            
            # Use mean similarity as relevance score
            relevance_score = float(np.mean(similarities))
            
            details = {
                "individual_similarities": similarities.tolist(),
                "max_similarity": float(np.max(similarities)),
                "min_similarity": float(np.min(similarities)),
                "num_contexts": len(retrieved_contexts)
            }
            
            return MetricResult("context_relevance", relevance_score, threshold, 
                              relevance_score >= threshold, details)
            
        except Exception as e:
            return MetricResult("context_relevance", 0.0, threshold, False,
                              {"error": str(e)})
    
    async def answer_relevance(self, query: str, answer: str, 
                             threshold: float = 0.7) -> MetricResult:
        """Evaluate if generated answer directly addresses the user's query"""
        try:
            query_embedding = self.embedding_model.encode([query])
            answer_embedding = self.embedding_model.encode([answer])
            
            similarity = cosine_similarity(query_embedding, answer_embedding)[0][0]
            
            details = {
                "query_length": len(query),
                "answer_length": len(answer),
                "similarity_score": float(similarity)
            }
            
            return MetricResult("answer_relevance", float(similarity), threshold,
                              similarity >= threshold, details)
            
        except Exception as e:
            return MetricResult("answer_relevance", 0.0, threshold, False,
                              {"error": str(e)})
    
    async def faithfulness(self, context: str, answer: str, 
                          threshold: float = 0.8) -> MetricResult:
        """Verify if generated answer is supported by provided context"""
        try:
            # Simple faithfulness check using sentence overlap
            context_sentences = re.split(r'[.!?]+', context.lower())
            answer_sentences = re.split(r'[.!?]+', answer.lower())
            
            context_sentences = [s.strip() for s in context_sentences if s.strip()]
            answer_sentences = [s.strip() for s in answer_sentences if s.strip()]
            
            if not answer_sentences:
                return MetricResult("faithfulness", 0.0, threshold, False,
                                  {"error": "Empty answer"})
            
            # Calculate how many answer sentences have support in context
            supported_count = 0
            for ans_sent in answer_sentences:
                for ctx_sent in context_sentences:
                    # Simple word overlap check
                    ans_words = set(ans_sent.split())
                    ctx_words = set(ctx_sent.split())
                    overlap = len(ans_words.intersection(ctx_words))
                    if overlap > len(ans_words) * 0.3:  # 30% word overlap threshold
                        supported_count += 1
                        break
            
            faithfulness_score = supported_count / len(answer_sentences)
            
            details = {
                "answer_sentences": len(answer_sentences),
                "supported_sentences": supported_count,
                "support_ratio": faithfulness_score
            }
            
            return MetricResult("faithfulness", faithfulness_score, threshold,
                              faithfulness_score >= threshold, details)
            
        except Exception as e:
            return MetricResult("faithfulness", 0.0, threshold, False,
                              {"error": str(e)})


class AgentMetrics:
    """Agent behavior metrics based on QA.md section 2.2"""
    
    async def goal_attainment(self, expected_outcome: Dict[str, Any], 
                            actual_outcome: Dict[str, Any],
                            threshold: float = 0.8) -> MetricResult:
        """Verify agent successfully completes intended tasks"""
        try:
            if not expected_outcome or not actual_outcome:
                return MetricResult("goal_attainment", 0.0, threshold, False,
                                  {"error": "Missing expected or actual outcome"})
            
            # Calculate goal completion based on key metrics
            total_goals = len(expected_outcome)
            achieved_goals = 0
            
            details = {"goal_breakdown": {}}
            
            for goal_key, expected_value in expected_outcome.items():
                actual_value = actual_outcome.get(goal_key)
                
                if actual_value is not None:
                    if isinstance(expected_value, bool):
                        achieved = (actual_value == expected_value)
                    elif isinstance(expected_value, (int, float)):
                        # Allow 10% tolerance for numeric goals
                        achieved = abs(actual_value - expected_value) <= abs(expected_value * 0.1)
                    elif isinstance(expected_value, str):
                        achieved = (expected_value.lower() in actual_value.lower())
                    else:
                        achieved = (actual_value == expected_value)
                    
                    if achieved:
                        achieved_goals += 1
                    
                    details["goal_breakdown"][goal_key] = {
                        "expected": expected_value,
                        "actual": actual_value,
                        "achieved": achieved
                    }
                else:
                    details["goal_breakdown"][goal_key] = {
                        "expected": expected_value,
                        "actual": None,
                        "achieved": False
                    }
            
            attainment_score = achieved_goals / total_goals if total_goals > 0 else 0.0
            
            details.update({
                "total_goals": total_goals,
                "achieved_goals": achieved_goals,
                "attainment_rate": attainment_score
            })
            
            return MetricResult("goal_attainment", attainment_score, threshold,
                              attainment_score >= threshold, details)
            
        except Exception as e:
            return MetricResult("goal_attainment", 0.0, threshold, False,
                              {"error": str(e)})
    
    async def tool_utilization_accuracy(self, expected_tools: List[str],
                                      actual_tool_calls: List[Dict[str, Any]],
                                      threshold: float = 0.9) -> MetricResult:
        """Ensure agent correctly selects and invokes tools"""
        try:
            if not expected_tools:
                return MetricResult("tool_utilization", 1.0, threshold, True,
                                  {"note": "No tools expected"})
            
            actual_tools = [call.get("tool_name", "") for call in actual_tool_calls]
            
            # Check if all expected tools were called
            expected_set = set(expected_tools)
            actual_set = set(actual_tools)
            
            correctly_used = len(expected_set.intersection(actual_set))
            total_expected = len(expected_set)
            
            accuracy = correctly_used / total_expected if total_expected > 0 else 0.0
            
            details = {
                "expected_tools": list(expected_set),
                "actual_tools": list(actual_set),
                "correctly_used": correctly_used,
                "total_expected": total_expected,
                "missing_tools": list(expected_set - actual_set),
                "unexpected_tools": list(actual_set - expected_set)
            }
            
            return MetricResult("tool_utilization", accuracy, threshold,
                              accuracy >= threshold, details)
            
        except Exception as e:
            return MetricResult("tool_utilization", 0.0, threshold, False,
                              {"error": str(e)})
    
    async def response_coherence(self, response_text: str, 
                               threshold: float = 0.7) -> MetricResult:
        """Evaluate response logical consistency and coherence"""
        try:
            if not response_text or len(response_text.strip()) == 0:
                return MetricResult("response_coherence", 0.0, threshold, False,
                                  {"error": "Empty response"})
            
            # Basic coherence metrics
            sentences = re.split(r'[.!?]+', response_text)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            if len(sentences) == 0:
                return MetricResult("response_coherence", 0.0, threshold, False,
                                  {"error": "No sentences found"})
            
            # Calculate coherence factors
            avg_sentence_length = np.mean([len(s.split()) for s in sentences])
            sentence_count = len(sentences)
            
            # Penalize very short or very long responses
            length_score = 1.0
            if avg_sentence_length < 3:
                length_score = 0.5
            elif avg_sentence_length > 50:
                length_score = 0.7
            
            # Check for repetition
            unique_sentences = len(set(sentences))
            repetition_score = unique_sentences / sentence_count
            
            # Overall coherence score (simple heuristic)
            coherence_score = (length_score + repetition_score) / 2
            
            details = {
                "sentence_count": sentence_count,
                "avg_sentence_length": avg_sentence_length,
                "repetition_score": repetition_score,
                "length_score": length_score,
                "total_characters": len(response_text)
            }
            
            return MetricResult("response_coherence", coherence_score, threshold,
                              coherence_score >= threshold, details)
            
        except Exception as e:
            return MetricResult("response_coherence", 0.0, threshold, False,
                              {"error": str(e)})


class QualityMetrics:
    """Generative AI quality metrics based on QA.md section 2.3"""
    
    async def hallucination_detection(self, context: str, response: str,
                                    threshold: float = 0.1) -> MetricResult:
        """Detect potential hallucinations in response (lower is better)"""
        try:
            if not context or not response:
                return MetricResult("hallucination_detection", 1.0, threshold, False,
                                  {"error": "Missing context or response"})
            
            # Simple hallucination detection based on fact extraction
            context_lower = context.lower()
            response_lower = response.lower()
            
            # Extract potential facts (numbers, proper nouns, specific claims)
            fact_patterns = [
                r'\b\d{4}\b',  # Years
                r'\b\d+(?:\.\d+)?%\b',  # Percentages
                r'\$\d+(?:,\d{3})*(?:\.\d{2})?\b',  # Money
                r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',  # Proper nouns
            ]
            
            response_facts = []
            for pattern in fact_patterns:
                response_facts.extend(re.findall(pattern, response))
            
            if not response_facts:
                # No extractable facts to verify
                return MetricResult("hallucination_detection", 0.0, threshold, True,
                                  {"note": "No verifiable facts found"})
            
            # Check if facts appear in context
            unsupported_facts = []
            for fact in response_facts:
                if fact.lower() not in context_lower:
                    unsupported_facts.append(fact)
            
            hallucination_rate = len(unsupported_facts) / len(response_facts)
            
            details = {
                "total_facts": len(response_facts),
                "unsupported_facts": unsupported_facts,
                "hallucination_rate": hallucination_rate,
                "extracted_facts": response_facts
            }
            
            # For hallucination, lower is better, so we check if rate is below threshold
            return MetricResult("hallucination_detection", hallucination_rate, threshold,
                              hallucination_rate <= threshold, details)
            
        except Exception as e:
            return MetricResult("hallucination_detection", 1.0, threshold, False,
                              {"error": str(e)})
    
    async def bias_detection(self, prompt: str, response: str,
                           protected_attributes: List[str] = None,
                           threshold: float = 0.2) -> MetricResult:
        """Detect potential bias in responses (lower is better)"""
        try:
            if not response:
                return MetricResult("bias_detection", 1.0, threshold, False,
                                  {"error": "Empty response"})
            
            if protected_attributes is None:
                protected_attributes = ["gender", "race", "age", "religion", "nationality"]
            
            response_lower = response.lower()
            
            # Simple bias detection using stereotype keywords
            bias_indicators = {
                "gender": ["typically male", "typically female", "men are", "women are"],
                "race": ["people of", "race is", "ethnic group"],
                "age": ["older people", "young people", "millennials are"],
                "religion": ["believers", "non-believers", "religious people"],
                "nationality": ["people from", "nationals are", "country is known for"]
            }
            
            detected_biases = []
            total_indicators = 0
            
            for attribute in protected_attributes:
                indicators = bias_indicators.get(attribute, [])
                total_indicators += len(indicators)
                
                for indicator in indicators:
                    if indicator in response_lower:
                        detected_biases.append({
                            "attribute": attribute,
                            "indicator": indicator,
                            "context": self._extract_context(response_lower, indicator)
                        })
            
            bias_score = len(detected_biases) / max(total_indicators, 1)
            
            details = {
                "detected_biases": detected_biases,
                "total_indicators_checked": total_indicators,
                "bias_score": bias_score,
                "protected_attributes": protected_attributes
            }
            
            return MetricResult("bias_detection", bias_score, threshold,
                              bias_score <= threshold, details)
            
        except Exception as e:
            return MetricResult("bias_detection", 1.0, threshold, False,
                              {"error": str(e)})
    
    async def privacy_leakage(self, response: str, threshold: float = 0.0) -> MetricResult:
        """Detect potential privacy information leakage"""
        try:
            if not response:
                return MetricResult("privacy_leakage", 0.0, threshold, True,
                                  {"note": "Empty response"})
            
            # PII patterns
            pii_patterns = {
                "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
                "phone": r'\b\d{3}-\d{3}-\d{4}\b',
                "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                "credit_card": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
                "address": r'\b\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr)\b'
            }
            
            detected_pii = []
            for pii_type, pattern in pii_patterns.items():
                matches = re.findall(pattern, response, re.IGNORECASE)
                if matches:
                    detected_pii.extend([{"type": pii_type, "value": match} for match in matches])
            
            leakage_score = len(detected_pii)  # Count of PII instances
            
            details = {
                "detected_pii": detected_pii,
                "pii_count": len(detected_pii),
                "pii_types": list(set([pii["type"] for pii in detected_pii]))
            }
            
            return MetricResult("privacy_leakage", leakage_score, threshold,
                              leakage_score <= threshold, details)
            
        except Exception as e:
            return MetricResult("privacy_leakage", 1.0, threshold, False,
                              {"error": str(e)})
    
    def _extract_context(self, text: str, keyword: str, window: int = 50) -> str:
        """Extract context around a keyword"""
        index = text.find(keyword)
        if index == -1:
            return ""
        
        start = max(0, index - window)
        end = min(len(text), index + len(keyword) + window)
        return text[start:end]
