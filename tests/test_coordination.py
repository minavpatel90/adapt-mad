"""Test coordination layer"""
import pytest
import numpy as np
import sys
sys.path.insert(0, 'src')

from src.agents import LatencyDetectionAgent
from src.coordination import AdaptiveCoordinator, SystemState, CollaborationStrategy

class TestCoordination:
    def test_coordinator_initialization(self):
        agents = [LatencyDetectionAgent(feature_dim=10, window_size=50)]
        coordinator = AdaptiveCoordinator(agents)
        assert coordinator.current_strategy == CollaborationStrategy.HYBRID
    
    def test_strategy_selection(self):
        agents = [LatencyDetectionAgent(feature_dim=10, window_size=50)]
        coordinator = AdaptiveCoordinator(agents, hysteresis=1)
        
        # High load
        state = SystemState(
            workload_intensity=5000.0,
            cpu_utilization=0.85,
            memory_utilization=0.80,
            recent_fpr=0.08,
            recent_fnr=0.05,
            deployment_active=False,
            timestamp=0.0
        )
        
        strategy = coordinator.select_strategy(state)
        assert strategy == CollaborationStrategy.HIERARCHICAL
