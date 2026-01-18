"""
Tutorial: Ouroboros Observer - Simulating Consciousness Phase Transitions

This notebook demonstrates the core functionality of the Ouroboros Observer toolkit.

Run this cell-by-cell in a Jupyter notebook, or convert with:
    jupyter nbconvert --to notebook --execute tutorial.py
"""

# Cell 1: Imports
print("=" * 60)
print("OUROBOROS OBSERVER TUTORIAL")
print("Simulating Consciousness Phase Transitions")
print("=" * 60)

import numpy as np
import matplotlib.pyplot as plt

from ouroboros_observer import (
    NeuralNetwork,
    NetworkGenerator,
    ConsciousnessMeasure,
    BifurcationDetector,
    SelfReferenceEngine,
    ValidationFramework
)

print("\nâœ“ Imports successful\n")

# Cell 2: Create a Neural Network
print("STEP 1: Creating Neural Network")
print("-" * 60)

N = 100  # neurons
W = NetworkGenerator.scale_free(N, m=4)
print(f"Created scale-free network with {N} neurons")
print(f"Number of connections: {W.nnz}")

# Tune to criticality
W = NetworkGenerator.tune_to_criticality(W, target_branching=1.0)
print(f"Tuned network to critical dynamics (branching â‰ˆ 1.0)")

network = NeuralNetwork(N, W, dt=0.1)
print(f"âœ“ Network initialized\n")

# Cell 3: Run Simulation
print("STEP 2: Running Neural Simulation")
print("-" * 60)

duration = 1000  # ms
I_external = np.random.rand(N) * 2.0  # External input

results = network.run(duration, I_external=I_external, record_V=True)

print(f"Simulation duration: {duration} ms")
print(f"Total spikes: {results['spike_raster'].sum()}")
print(f"Mean firing rate: {results['firing_rates'].mean():.2f} Hz")
print(f"âœ“ Simulation complete\n")

# Cell 4: Calculate Consciousness Measure
print("STEP 3: Calculating C(t)")
print("-" * 60)

measure = ConsciousnessMeasure(lambda_param=2.0, Phi_method='geometric')

# Calculate C at multiple timepoints
C_timeseries = []
time_windows = []

for t_start in range(0, duration-100, 50):
    window = results['spike_raster'][:, t_start:t_start+100]
    activity_mean = window.mean(axis=1)
    
    C_result = measure.calculate_C(activity_mean, W, window)
    C_timeseries.append(C_result)
    time_windows.append(t_start + 50)

C_values = np.array([c['C'] for c in C_timeseries])
Phi_values = np.array([c['Phi'] for c in C_timeseries])
R_values = np.array([c['R'] for c in C_timeseries])
D_values = np.array([c['D'] for c in C_timeseries])

print(f"Mean C(t): {C_values.mean():.2f} Â± {C_values.std():.2f} bits")
print(f"Mean Î¦(t): {Phi_values.mean():.2f} bits")
print(f"Mean R(t): {R_values.mean():.2f}")
print(f"Mean D(t): {D_values.mean():.3f}")

if C_values.mean() > 8.3:
    print(f"\nâœ“ System is CONSCIOUS (C > C_critical = 8.3 bits)")
else:
    print(f"\nâœ— System is UNCONSCIOUS (C < C_critical = 8.3 bits)")

print()

# Cell 5: Detect Phase Transitions
print("STEP 4: Detecting Phase Transitions")
print("-" * 60)

detector = BifurcationDetector(C_critical=8.3)

transitions = detector.detect_transition(C_values, time=np.array(time_windows))

print(f"Total transitions detected: {transitions['total_transitions']}")
print(f"Up transitions: {transitions['n_up_transitions']}")
print(f"Down transitions: {transitions['n_down_transitions']}")

if transitions['total_transitions'] > 0:
    print(f"\nâœ“ Phase transition(s) detected!")
else:
    print(f"\nâ—‹ No transitions (system in stable state)")

print()

# Cell 6: Simulate Self-Reference
print("STEP 5: Simulating Self-Reference Dynamics")
print("-" * 60)

sr_engine = SelfReferenceEngine(state_dim=10)

sr_results = sr_engine.simulate_recursive_collapse(n_steps=100)

print(f"Mean recursive depth: {sr_results['mean_depth']:.2f}")
print(f"Strange loop strength: {sr_results['loop_strength']:.2f}")
print(f"Converged to fixed point: {sr_results['final_convergence']['converged']}")

if sr_results['final_convergence']['converged']:
    print(f"  Convergence time: {sr_results['final_convergence']['convergence_time']}")

print(f"âœ“ Self-reference simulation complete\n")

# Cell 7: Visualization
print("STEP 6: Creating Visualizations")
print("-" * 60)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. C(t) time series
ax = axes[0, 0]
ax.plot(time_windows, C_values, 'b-', linewidth=2, label='C(t)')
ax.axhline(8.3, color='r', linestyle='--', linewidth=2, label='C_critical')
ax.fill_between(time_windows, 7.7, 8.9, alpha=0.2, color='green')
ax.set_xlabel('Time (ms)')
ax.set_ylabel('C (bits)')
ax.set_title('Consciousness Measure C(t)')
ax.legend()
ax.grid(True, alpha=0.3)

# 2. Components
ax = axes[0, 1]
ax.plot(time_windows, Phi_values, 'g-', label='Î¦ (Integration)', linewidth=2)
ax.plot(time_windows, R_values, 'b-', label='R (Recursion)', linewidth=2)
ax.plot(time_windows, D_values * 5, 'r-', label='DÃ—5 (Criticality)', linewidth=2)
ax.set_xlabel('Time (ms)')
ax.set_ylabel('Value')
ax.set_title('C(t) Components')
ax.legend()
ax.grid(True, alpha=0.3)

# 3. Spike raster (sample)
ax = axes[1, 0]
sample = results['spike_raster'][:30, :200]  # First 30 neurons, 200 timesteps
ax.imshow(sample, aspect='auto', cmap='binary', interpolation='nearest')
ax.set_xlabel('Time (ms Ã— 0.1)')
ax.set_ylabel('Neuron')
ax.set_title('Neural Activity Raster (Sample)')

# 4. Self-reference dynamics
ax = axes[1, 1]
ax.plot(sr_results['depths'], 'purple', linewidth=2)
ax.fill_between(range(len(sr_results['depths'])), 
               0, sr_results['depths'], alpha=0.3, color='purple')
ax.set_xlabel('Time Step')
ax.set_ylabel('Recursive Depth')
ax.set_title('Self-Reference Depth Evolution')
ax.grid(True, alpha=0.3)

plt.suptitle('Ouroboros Observer: Neural Dynamics and Consciousness Measure', 
            fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('tutorial_results.png', dpi=150, bbox_inches='tight')
print("âœ“ Visualization saved: tutorial_results.png")
plt.show()

# Cell 8: Run Validation
print("\nSTEP 7: Running Validation Suite")
print("-" * 60)

validator = ValidationFramework(random_seed=42)

# Generate test data
print("Generating synthetic conscious and unconscious states...")
conscious_data = validator.generate_synthetic_conscious(N=80, T=500)
unconscious_data = validator.generate_synthetic_unconscious(N=80, T=500)

print(f"\nConscious data:")
print(f"  Mean C: {conscious_data['C_mean']:.2f} Â± {conscious_data['C_std']:.2f} bits")

print(f"\nUnconscious data:")
print(f"  Mean C: {unconscious_data['C_mean']:.2f} Â± {unconscious_data['C_std']:.2f} bits")

# Test classifier
labels = np.array([1, 0])  # 1=conscious, 0=unconscious
C_test = np.array([conscious_data['C_mean'], unconscious_data['C_mean']])
predictions = (C_test > 8.3).astype(int)

if predictions[0] == 1 and predictions[1] == 0:
    print(f"\nâœ“ Classifier correctly separates conscious/unconscious states")
else:
    print(f"\nâš  Classifier accuracy limited (may need more samples)")

# Cell 9: Summary
print("\n" + "=" * 60)
print("TUTORIAL SUMMARY")
print("=" * 60)

print("\nKey Results:")
print(f"  1. Network activity: {results['firing_rates'].mean():.1f} Hz average")
print(f"  2. Consciousness measure: C = {C_values.mean():.2f} bits")
print(f"  3. State: {'CONSCIOUS' if C_values.mean() > 8.3 else 'UNCONSCIOUS'}")
print(f"  4. Transitions detected: {transitions['total_transitions']}")
print(f"  5. Self-reference depth: {sr_results['mean_depth']:.2f}")

print("\nNext Steps:")
print("  â€¢ Explore parameter_explorer.py for parameter optimization")
print("  â€¢ See experiment_*.py notebooks for specific predictions")
print("  â€¢ Consult README.md for advanced usage")

print("\n" + "=" * 60)
print("TUTORIAL COMPLETE")
print("=" * 60)
