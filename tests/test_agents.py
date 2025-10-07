"""Test detection agents"""
import pytest
import numpy as np
import sys
sys.path.insert(0, 'src')

from src.agents import LatencyDetectionAgent, AgentType

class TestAgents:
    def test_agent_initialization(self):
        agent = LatencyDetectionAgent(feature_dim=10, window_size=50)
        assert agent.agent_type == AgentType.LATENCY
        assert agent.feature_dim == 10
        assert agent.window_size == 50
    
    def test_detection(self):
        agent = LatencyDetectionAgent(feature_dim=10, window_size=50)
        window = np.random.randn(50, 10)
        result = agent.detect(window)
        
        assert result.score >= 0
        assert isinstance(result.is_anomaly, bool)
        assert 0 <= result.confidence <= 1.0
    
    def test_weight_update(self):
        agent = LatencyDetectionAgent(feature_dim=10, window_size=50)
        initial_weight = agent.weight
        
        agent.update_performance(is_correct=True)
        assert agent.weight >= initial_weight
