"""
ADAPT-MAD: Adaptive Coordination Layer
"""
import numpy as np
from typing import List, Dict, Tuple
from enum import Enum
from collections import deque
from dataclasses import dataclass
import time

class CollaborationStrategy(Enum):
    PEER_TO_PEER = "P2P"
    HIERARCHICAL = "HIER"
    HYBRID = "HYBRID"

@dataclass
class SystemState:
    workload_intensity: float
    cpu_utilization: float
    memory_utilization: float
    recent_fpr: float
    recent_fnr: float
    deployment_active: bool
    timestamp: float

class AdaptiveCoordinator:
    """Tier 2: Adaptive Coordination Layer"""
    
    def __init__(self, agents: List, threshold_high_load: float = 4000.0,
                 threshold_low_load: float = 1000.0, threshold_fpr: float = 0.15,
                 threshold_fnr: float = 0.10, hysteresis: int = 2):
        self.agents = agents
        self.T_high = threshold_high_load
        self.T_low = threshold_low_load
        self.T_FPR = threshold_fpr
        self.T_FNR = threshold_fnr
        self.hysteresis = hysteresis
        
        self.current_strategy = CollaborationStrategy.HYBRID
        self.strategy_triggers = deque(maxlen=hysteresis)
        self.recent_detections = deque(maxlen=1000)
        self.workload_history = deque(maxlen=100)
        self.deployment_mode_until = 0
        self.lenient_mode_duration = 30 * 60
        
        self.strategy_stats = {
            CollaborationStrategy.PEER_TO_PEER: {'time': 0, 'detections': 0},
            CollaborationStrategy.HIERARCHICAL: {'time': 0, 'detections': 0},
            CollaborationStrategy.HYBRID: {'time': 0, 'detections': 0}
        }
        self.strategy_start_time = time.time()
    
    def select_strategy(self, system_state: SystemState) -> CollaborationStrategy:
        """Algorithm 1 & 4: Strategy Selection"""
        workload = system_state.workload_intensity
        
        if workload > self.T_high:
            target_strategy = CollaborationStrategy.HIERARCHICAL
        elif workload < self.T_low:
            target_strategy = CollaborationStrategy.PEER_TO_PEER
        else:
            target_strategy = CollaborationStrategy.HYBRID
        
        if system_state.recent_fnr > self.T_FNR:
            for agent in self.agents:
                agent.alpha = max(agent.alpha * 0.9, 0.5)
        
        if system_state.deployment_active:
            self.enable_lenient_mode()
        
        self.strategy_triggers.append(target_strategy)
        
        if len(self.strategy_triggers) == self.hysteresis:
            if all(s == target_strategy for s in self.strategy_triggers):
                if self.current_strategy != target_strategy:
                    elapsed = time.time() - self.strategy_start_time
                    self.strategy_stats[self.current_strategy]['time'] += elapsed
                    self.strategy_start_time = time.time()
                    self.current_strategy = target_strategy
        
        return self.current_strategy
    
    def enable_lenient_mode(self):
        """Enable lenient thresholds during deployments"""
        self.deployment_mode_until = time.time() + self.lenient_mode_duration
        for agent in self.agents:
            agent.alpha = min(agent.alpha * 1.3, 2.0)
    
    def is_lenient_mode(self) -> bool:
        return time.time() < self.deployment_mode_until
    
    def coordinate_detection(self, detection_results: List, 
                           system_state: SystemState) -> Tuple[bool, float, Dict]:
        """Coordinate detection results"""
        strategy = self.select_strategy(system_state)
        
        if strategy == CollaborationStrategy.PEER_TO_PEER:
            return self._peer_to_peer_coordination(detection_results, system_state)
        elif strategy == CollaborationStrategy.HIERARCHICAL:
            return self._hierarchical_coordination(detection_results, system_state)
        else:
            return self._hybrid_coordination(detection_results, system_state)
    
    def _peer_to_peer_coordination(self, results, state):
        anomaly_votes = sum(1 for r in results if r.is_anomaly)
        is_anomaly = anomaly_votes > len(results) / 2
        avg_confidence = np.mean([r.confidence for r in results])
        metadata = {'strategy': 'P2P', 'votes': anomaly_votes}
        return is_anomaly, avg_confidence, metadata
    
    def _hierarchical_coordination(self, results, state):
        sorted_results = sorted(results, 
            key=lambda r: self._get_agent_by_type(r.agent_type).weight, reverse=True)
        leader_result = sorted_results[0]
        metadata = {'strategy': 'HIERARCHICAL', 
                   'leader': leader_result.agent_type.value}
        return leader_result.is_anomaly, leader_result.confidence, metadata
    
    def _hybrid_coordination(self, results, state):
        from .fusion_engine import DecisionFusionEngine
        fusion = DecisionFusionEngine(self.agents)
        is_anomaly, score = fusion.fuse_decisions(results, state)
        metadata = {'strategy': 'HYBRID', 'fusion_score': score}
        return is_anomaly, score, metadata
    
    def _get_agent_by_type(self, agent_type):
        for agent in self.agents:
            if agent.agent_type == agent_type:
                return agent
        return None
    
    def get_statistics(self) -> Dict:
        elapsed = time.time() - self.strategy_start_time
        self.strategy_stats[self.current_strategy]['time'] += elapsed
        self.strategy_start_time = time.time()
        
        total_time = sum(s['time'] for s in self.strategy_stats.values())
        
        return {
            'current_strategy': self.current_strategy.value,
            'strategy_distribution': {
                k.value: {
                    'time_percent': (v['time'] / total_time * 100) if total_time > 0 else 0,
                    'detections': v['detections']
                }
                for k, v in self.strategy_stats.items()
            },
            'lenient_mode': self.is_lenient_mode()
        }
