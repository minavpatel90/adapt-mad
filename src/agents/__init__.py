"""ADAPT-MAD Detection Agents"""
from .base_agent import DetectionAgent, AgentType, DetectionResult, LSTMDetector
from .latency_agent import LatencyDetectionAgent
from .throughput_agent import ThroughputAgent
from .resource_agent import ResourceAgent
from .error_rate_agent import Error_rateAgent
from .slo_agent import SloAgent

# Aliases
ThroughputMonitoringAgent = ThroughputAgent
ResourceUtilizationAgent = ResourceAgent
ErrorRateAgent = Error_rateAgent
SLOComplianceAgent = SloAgent

__all__ = [
    'DetectionAgent', 'AgentType', 'DetectionResult', 'LSTMDetector',
    'LatencyDetectionAgent', 'ThroughputMonitoringAgent',
    'ResourceUtilizationAgent', 'ErrorRateAgent', 'SLOComplianceAgent'
]
