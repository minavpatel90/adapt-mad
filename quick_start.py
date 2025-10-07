"""ADAPT-MAD Quick Start Example"""
from src.agents import LatencyDetectionAgent, ThroughputMonitoringAgent
from src.coordination import AdaptiveCoordinator, SystemState
import numpy as np
import time

print("ADAPT-MAD Quick Start")
print("=" * 50)

# Create agents
print("\n1. Creating detection agents...")
agents = [
    LatencyDetectionAgent(feature_dim=10, window_size=50),
    ThroughputMonitoringAgent(feature_dim=10, window_size=50),
]
print(f"   Created {len(agents)} agents")

# Create coordinator
print("\n2. Initializing coordinator...")
coordinator = AdaptiveCoordinator(agents)
print("   Coordinator ready")

# Generate sample data
print("\n3. Preparing test data...")
window = np.random.randn(50, 10)
print(f"   Window shape: {window.shape}")

# Define system state
system_state = SystemState(
    workload_intensity=3500.0,
    cpu_utilization=0.65,
    memory_utilization=0.58,
    recent_fpr=0.08,
    recent_fnr=0.05,
    deployment_active=False,
    timestamp=time.time()
)

# Run detection
print("\n4. Running anomaly detection...")
agent_results = [agent.detect(window) for agent in agents]

is_anomaly, confidence, metadata = coordinator.coordinate_detection(
    agent_results, 
    system_state
)

# Display results
print("\n" + "=" * 50)
print("DETECTION RESULTS")
print("=" * 50)
print(f"Anomaly Detected: {is_anomaly}")
print(f"Confidence: {confidence:.3f}")
print(f"Strategy Used: {metadata['strategy']}")
print("=" * 50)

# Show agent metrics
print("\n5. Agent Performance:")
for agent in agents:
    metrics = agent.get_metrics()
    print(f"\n   {agent.agent_type.value}:")
    print(f"     Weight: {metrics['weight']:.3f}")
    print(f"     F1: {metrics['f1']:.3f}")

print("\n✓ Quick start complete!")
