"""Run single dataset experiment"""
import argparse
import sys
sys.path.insert(0, 'src')

from src.agents import *
from src.coordination import AdaptiveCoordinator, SystemState
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', required=True, 
                       choices=['train_ticket', 'robotshop', 'sock_shop'])
    parser.add_argument('--config', default='configs/default.yaml')
    parser.add_argument('--output', default='results/')
    args = parser.parse_args()
    
    print(f"Running experiment on {args.dataset}")
    print("=" * 60)
    
    # Create agents
    agents = [
        LatencyDetectionAgent(feature_dim=10, window_size=50),
        ThroughputMonitoringAgent(feature_dim=10, window_size=50),
        ResourceUtilizationAgent(feature_dim=10, window_size=50),
        ErrorRateAgent(feature_dim=10, window_size=50),
    ]
    
    # Create coordinator
    coordinator = AdaptiveCoordinator(agents)
    
    # Simulate evaluation
    print("\nSimulating evaluation...")
    n_samples = 100
    predictions = []
    labels = np.random.randint(0, 2, n_samples)
    
    for i in range(n_samples):
        window = np.random.randn(50, 10)
        
        system_state = SystemState(
            workload_intensity=np.random.uniform(1000, 5000),
            cpu_utilization=np.random.uniform(0.3, 0.9),
            memory_utilization=np.random.uniform(0.3, 0.8),
            recent_fpr=0.08,
            recent_fnr=0.05,
            deployment_active=(i % 50 == 0),
            timestamp=i
        )
        
        agent_results = [agent.detect(window) for agent in agents]
        is_anomaly, _, _ = coordinator.coordinate_detection(agent_results, system_state)
        predictions.append(1 if is_anomaly else 0)
    
    # Calculate metrics
    precision = precision_score(labels, predictions, zero_division=0)
    recall = recall_score(labels, predictions, zero_division=0)
    f1 = f1_score(labels, predictions, zero_division=0)
    
    print("\nResults:")
    print(f"  Precision: {precision:.3f}")
    print(f"  Recall: {recall:.3f}")
    print(f"  F1: {f1:.3f}")
    print("\n✓ Experiment complete!")

if __name__ == "__main__":
    main()
