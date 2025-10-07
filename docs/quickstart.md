# Quick Start Tutorial

## 5-Minute Example

```python
from src.agents import LatencyDetectionAgent
from src.coordination import AdaptiveCoordinator, SystemState
import numpy as np

# Create agents
agents = [LatencyDetectionAgent(feature_dim=10, window_size=50)]
coordinator = AdaptiveCoordinator(agents)

# Prepare data
window = np.random.randn(50, 10)
system_state = SystemState(
    workload_intensity=3500.0,
    cpu_utilization=0.65,
    memory_utilization=0.58,
    recent_fpr=0.08,
    recent_fnr=0.05,
    deployment_active=False,
    timestamp=0.0
)

# Detect anomalies
agent_results = [agent.detect(window) for agent in agents]
is_anomaly, confidence, metadata = coordinator.coordinate_detection(
    agent_results, system_state
)

print(f"Anomaly: {is_anomaly}, Confidence: {confidence:.3f}")
```

## Run Experiments

```bash
# Single dataset
python experiments/run_single_dataset.py --dataset train_ticket

# Generate results
python analysis/generate_tables.py
```
