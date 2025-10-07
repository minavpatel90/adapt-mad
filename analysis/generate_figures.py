"""Generate result figures"""
import matplotlib.pyplot as plt
import numpy as np

def main():
    print("Generating Figures")
    print("=" * 60)
    
    # Figure: Performance Comparison
    systems = ['Threshold', 'Iso Forest', 'Single', 'Static MA', 'ADAPT-MAD']
    f1_scores = [0.552, 0.662, 0.682, 0.670, 0.836]
    
    plt.figure(figsize=(10, 6))
    plt.bar(systems, f1_scores, color='steelblue')
    plt.ylabel('F1 Score')
    plt.title('Detection Performance Comparison')
    plt.ylim([0, 1.0])
    plt.grid(axis='y', alpha=0.3)
    
    plt.savefig('results/figures/performance_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: performance_comparison.png")
    
    plt.close()
    print("\n✓ Figures generated!")

if __name__ == "__main__":
    main()
