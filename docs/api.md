# API Reference

## Detection Agents

### LatencyDetectionAgent

```python
agent = LatencyDetectionAgent(
    feature_dim=10,      # Number of features
    window_size=50,      # Time window size
    hidden_dim=64,       # LSTM hidden dimension
    num_layers=2,        # LSTM layers
    dropout=0.2          # Dropout rate
)

result = agent.detect(window)  # Returns DetectionResult
```

### DetectionResult

```python
@dataclass
class DetectionResult:
    score: float          # Anomaly score
    is_anomaly: bool      # Binary decision
    confidence: float     # Confidence [0, 1]
    timestamp: float      # Detection time
    agent_type: AgentType # Agent identifier
```

## Coordination

### AdaptiveCoordinator

```python
coordinator = AdaptiveCoordinator(
    agents=agents,
    threshold_high_load=4000,
    threshold_low_load=1000,
    threshold_fpr=0.15,
    threshold_fnr=0.10,
    hysteresis=2
)

is_anomaly, confidence, metadata = coordinator.coordinate_detection(
    detection_results, 
    system_state
)
```

### SystemState

```python
@dataclass
class SystemState:
    workload_intensity: float    # RPS
    cpu_utilization: float       # [0, 1]
    memory_utilization: float    # [0, 1]
    recent_fpr: float           # False positive rate
    recent_fnr: float           # False negative rate
    deployment_active: bool     # Deployment flag
    timestamp: float            # Current time
```
