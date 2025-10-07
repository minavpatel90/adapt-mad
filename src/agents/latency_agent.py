"""Latency Detection Agent"""
from .base_agent import DetectionAgent, AgentType
import numpy as np

class LatencyDetectionAgent(DetectionAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(AgentType.LATENCY, *args, **kwargs)
    
    def extract_features(self, window: np.ndarray) -> np.ndarray:
        features = super().extract_features(window)
        # Add percentile features
        p50 = np.percentile(window, 50, axis=0)
        p95 = np.percentile(window, 95, axis=0)
        p99 = np.percentile(window, 99, axis=0)
        enhanced = np.vstack([features, p50, p95, p99])
        return enhanced[:self.window_size]
