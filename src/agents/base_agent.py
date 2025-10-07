"""
ADAPT-MAD: Base Detection Agent
Core agent implementation with LSTM-based anomaly detection
"""

import numpy as np
import torch
import torch.nn as nn
from typing import Dict, List, Tuple, Optional
from collections import deque
from dataclasses import dataclass
from enum import Enum

class AgentType(Enum):
    LATENCY = "LDA"
    THROUGHPUT = "TMA"
    RESOURCE = "RUA"
    ERROR_RATE = "ERA"
    SLO_COMPLIANCE = "SCA"

@dataclass
class DetectionResult:
    score: float
    is_anomaly: bool
    confidence: float
    timestamp: float
    agent_type: AgentType

class LSTMDetector(nn.Module):
    """LSTM-based anomaly detector"""
    
    def __init__(self, input_dim: int, hidden_dim: int = 64, 
                 num_layers: int = 2, dropout: float = 0.2):
        super(LSTMDetector, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        
        self.lstm = nn.LSTM(
            input_dim, hidden_dim, num_layers, 
            dropout=dropout, batch_first=True
        )
        self.fc = nn.Linear(hidden_dim, input_dim)
        
    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        output = self.fc(lstm_out)
        return output

class DetectionAgent:
    """Base detection agent with adaptive threshold"""
    
    def __init__(self, agent_type: AgentType, feature_dim: int,
                 window_size: int = 50, hidden_dim: int = 64,
                 num_layers: int = 2, dropout: float = 0.2,
                 device: str = 'cpu'):
        self.agent_type = agent_type
        self.feature_dim = feature_dim
        self.window_size = window_size
        self.device = device
        
        self.model = LSTMDetector(
            feature_dim, hidden_dim, num_layers, dropout
        ).to(device)
        
        self.detection_history = deque(maxlen=1000)
        self.performance_metrics = {
            'true_positives': 0, 'false_positives': 0,
            'true_negatives': 0, 'false_negatives': 0
        }
        
        self.alpha = 1.0
        self.recent_fpr = deque(maxlen=100)
        self.recent_fnr = deque(maxlen=100)
        self.weight = 1.0
        self.communication_buffer = []
    
    def extract_features(self, window: np.ndarray) -> np.ndarray:
        """Extract and normalize features"""
        features = window.copy()
        mean = np.mean(features, axis=0)
        std = np.std(features, axis=0) + 1e-8
        normalized = (features - mean) / std
        return normalized
    
    def detect(self, window: np.ndarray) -> DetectionResult:
        """Algorithm 3: Agent Detection Process"""
        features = self.extract_features(window)
        
        with torch.no_grad():
            x = torch.FloatTensor(features).unsqueeze(0).to(self.device)
            y_pred = self.model(x).squeeze(0).cpu().numpy()
        
        y_true = features[-1]
        error = np.abs(y_true - y_pred[-1])
        window_std = np.std(window, axis=0) + 1e-8
        threshold = self.alpha * window_std
        score = np.mean(error / threshold)
        
        self._adapt_threshold()
        
        is_anomaly = score > 1.0
        confidence = min(score / 2.0, 1.0) if is_anomaly else 1.0 - score
        
        result = DetectionResult(
            score=float(score), is_anomaly=bool(is_anomaly),
            confidence=float(confidence), timestamp=0.0,
            agent_type=self.agent_type
        )
        
        self.detection_history.append(result)
        return result
    
    def _adapt_threshold(self):
        """Adapt detection threshold"""
        if len(self.recent_fpr) > 10:
            avg_fpr = np.mean(self.recent_fpr)
            if avg_fpr > 0.15:
                self.alpha = min(self.alpha * 1.1, 2.0)
            elif len(self.recent_fnr) > 10 and np.mean(self.recent_fnr) > 0.10:
                self.alpha = max(self.alpha * 0.9, 0.5)
    
    def update_performance(self, is_correct: bool, was_true_positive: bool = None):
        """Algorithm 6: Performance-Based Weight Update"""
        if was_true_positive is not None:
            if was_true_positive:
                self.performance_metrics['true_positives'] += 1
            else:
                self.performance_metrics['false_positives'] += 1
                self.recent_fpr.append(1)
        
        beta = 0.95
        if is_correct:
            new_weight = min(1.1 * self.weight, 2.0)
        else:
            new_weight = max(0.9 * self.weight, 0.5)
        
        self.weight = beta * self.weight + (1 - beta) * new_weight
    
    def get_metrics(self) -> Dict[str, float]:
        """Calculate performance metrics"""
        tp = self.performance_metrics['true_positives']
        fp = self.performance_metrics['false_positives']
        tn = self.performance_metrics['true_negatives']
        fn = self.performance_metrics['false_negatives']
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
        
        return {
            'precision': precision, 'recall': recall,
            'f1': f1, 'fpr': fpr, 'weight': self.weight
        }
