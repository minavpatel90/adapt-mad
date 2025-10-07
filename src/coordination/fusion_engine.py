"""Decision Fusion Engine"""
import numpy as np
from typing import List, Tuple

class DecisionFusionEngine:
    """Tier 3: Decision Fusion Engine"""
    
    def __init__(self, agents: List):
        self.agents = agents
        self.base_threshold = 0.6
        self.epsilon = 1e-8
    
    def fuse_decisions(self, detection_results: List, 
                      system_state) -> Tuple[bool, float]:
        """Algorithm 5: Adaptive Weighted Voting"""
        S = 0.0
        W = 0.0
        
        for result in detection_results:
            agent = self._get_agent_by_type(result.agent_type)
            if agent:
                weight = agent.weight
                score = result.score if result.is_anomaly else 0.0
                S += weight * score
                W += weight
        
        fusion_score = S / max(W, self.epsilon)
        
        delta_fpr = max(0, system_state.recent_fpr - 0.1)
        adaptive_threshold = np.clip(self.base_threshold + delta_fpr, 0.4, 0.8)
        
        is_anomaly = fusion_score > adaptive_threshold
        return is_anomaly, fusion_score
    
    def _get_agent_by_type(self, agent_type):
        for agent in self.agents:
            if agent.agent_type == agent_type:
                return agent
        return None
