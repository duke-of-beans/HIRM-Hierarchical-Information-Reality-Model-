#!/usr/bin/env python3
"""
Quick Demo: Consciousness Transition Simulation

Demonstrates the Ouroboros Observer framework by simulating
a neural network transitioning from unconscious to conscious state.
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '.')

from ouroboros_observer import (
    NeuralNetwork,
    ConsciousnessMeasure,
    BifurcationDetector
)
from ouroboros_observer.visualization import plots


def main():
    print("=" * 70)
    print("OUROBOROS OBSERVER: CONSCIOUSNESS TRANSITION DEMO")
    print("=" * 70)
    print()
    
    # Configuration
    N_neurons = 100
    duration = 10000.0  # 10 seconds
    dt = 0.1
    
    print(f"Configuration:")
    print(f"  - Network size: {N_neurons} neurons")
    print(f"  - Simulation duration: {duration/1000:.1f} seconds")
    print(f"  - Time step: {dt} ms")
    print()
    
    # Step 1: Create network
    print("[1/5] Creating neural network...")
    network = NeuralNetwork(
        N_neurons=N_neurons,
        dt=dt,
        seed=42
    )
    print(f"  ✓ Network created with {network.W.sum():.0f} synapses")
    print()
    
    # Step 2: Initialize measurement tools
    print("[2/5] Initializing measurement tools...")
    measure = ConsciousnessMeasure(lambda_param=5.0, Phi_method='geometric')
    detector = BifurcationDetector(C_critical=8.3)
    print("  ✓ Consciousness measure initialized")
    print("  ✓ Phase transition detector initialized")
    print()
    
    # Step 3: Run simulation with increasing input
    print("[3/5] Running simulation...")
    print("  Simulating gradual increase in external input...")
    
    n_steps = int(duration / dt)
    C_timeseries = []
    Phi_timeseries = []
    R_timeseries = []
    D_timeseries = []
    time_points = []
    
    sample_interval = 100  # Sample every 100 steps
    
    for step in range(n_steps):
        # Gradually increase input strength
        input_strength = 1.0 + 9.0 * (step / n_steps)
        I_ext = np.random.randn(N_neurons) * 1.0 + input_strength
        
        network.step(I_ext)
        
        # Sample C(t) periodically
        if step % sample_interval == 0 and len(network.spike_history) > 50:
            activity = network.get_activity()
            history = np.array(network.spike_history[-50:])
            
            C, components = measure.calculate_C(
                activity=activity,
                connectivity=network.W,
                activity_history=history
            )
            
            C_timeseries.append(C)
            Phi_timeseries.append(components['Phi'])
            R_timeseries.append(components['R'])
            D_timeseries.append(components['D'])
            time_points.append(network.time)
        
        if step % 10000 == 0:
            progress = 100 * step / n_steps
            print(f"    Progress: {progress:.1f}% (t = {network.time:.0f} ms)")
    
    C_timeseries = np.array(C_timeseries)
    time_points = np.array(time_points)
    
    print(f"  ✓ Simulation complete")
    print()
    
    # Step 4: Detect transitions
    print("[4/5] Analyzing phase transitions...")
    transitions = detector.detect_transitions(C_timeseries, time_points)
    
    if transitions:
        print(f"  ✓ Detected {len(transitions)} transition(s):")
        for i, trans in enumerate(transitions):
            print(f"    {i+1}. At t={trans.time:.0f} ms:")
            print(f"       C: {trans.C_before:.2f} → {trans.C_after:.2f} bits")
            print(f"       Type: {trans.transition_type}")
    else:
        print("  ✗ No transitions detected")
    print()
    
    # Step 5: Results summary
    print("[5/5] Results Summary:")
    print(f"  Mean C(t): {C_timeseries.mean():.2f} ± {C_timeseries.std():.2f} bits")
    print(f"  Max C(t): {C_timeseries.max():.2f} bits")
    print(f"  Min C(t): {C_timeseries.min():.2f} bits")
    
    if transitions:
        trans_C = [t.C_after for t in transitions if t.transition_type == 'subcritical_to_supercritical']
        if trans_C:
            print(f"  C_critical (measured): {np.mean(trans_C):.2f} ± {np.std(trans_C):.2f} bits")
            print(f"  C_critical (theoretical): 8.3 bits")
            print(f"  Deviation: {abs(np.mean(trans_C) - 8.3):.2f} bits")
    
    final_state = "CONSCIOUS" if C_timeseries[-1] > 8.3 else "UNCONSCIOUS"
    print(f"  Final state: {final_state}")
    print()
    
    # Visualize
    print("Generating visualization...")
    
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    
    # Plot C(t)
    axes[0].plot(time_points/1000, C_timeseries, 'b-', linewidth=2, label='C(t)')
    axes[0].axhline(8.3, color='r', linestyle='--', linewidth=2, label='C_critical = 8.3 bits')
    
    # Mark transitions
    for trans in transitions:
        axes[0].axvline(trans.time/1000, color='orange', linestyle=':', alpha=0.7)
        axes[0].plot(trans.time/1000, trans.C_after, 'ro', markersize=10)
    
    axes[0].set_ylabel('C(t) [bits]', fontsize=12)
    axes[0].set_title('Consciousness Measure During Transition', fontsize=14, fontweight='bold')
    axes[0].legend(fontsize=10)
    axes[0].grid(True, alpha=0.3)
    
    # Plot components
    axes[1].plot(time_points/1000, Phi_timeseries, 'b-', alpha=0.7, label='Φ (Integration)')
    axes[1].plot(time_points/1000, R_timeseries, 'g-', alpha=0.7, label='R (Recursion)')
    axes[1].plot(time_points/1000, D_timeseries, 'orange', alpha=0.7, label='D (Criticality)')
    
    axes[1].set_xlabel('Time [s]', fontsize=12)
    axes[1].set_ylabel('Component Value', fontsize=12)
    axes[1].set_title('C(t) Components', fontsize=14, fontweight='bold')
    axes[1].legend(fontsize=10)
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('consciousness_transition_demo.png', dpi=300, bbox_inches='tight')
    print("  ✓ Saved figure: consciousness_transition_demo.png")
    
    plt.show()
    
    print()
    print("=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)


if __name__ == '__main__':
    main()
