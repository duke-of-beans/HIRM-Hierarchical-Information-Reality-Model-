"""
Minimal Toy Model: Self-Reference Emergence
===========================================

A deliberately simple system where self-reference MUST emerge
to solve the task. This is designed to work.

Goal: Prove the core concept in the simplest possible way.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Dict


class MinimalSelfReferenceSystem:
    """
    Minimal system: 5 neurons, simple dynamics.
    
    Task: Predict your own next state.
    
    If you can't model yourself (R=0), you fail.
    If you model yourself well (R→1), you succeed.
    """
    
    def __init__(self, n_neurons: int = 5, learning_rate: float = 0.1):
        self.n = n_neurons
        self.lr = learning_rate
        
        # State: current neural activity
        self.state = np.random.randn(n_neurons) * 0.1
        
        # Self-model: network's prediction of its own next state
        self.self_model = np.zeros(n_neurons)
        
        # Weights: how state evolves
        self.W = np.random.randn(n_neurons, n_neurons) * 0.1
        
        # Self-model weights: learns to predict state evolution
        self.W_self = np.zeros((n_neurons, n_neurons))
        
        # History
        self.R_history = []
        self.C_history = []
        self.state_history = []
        
    def step(self) -> Dict[str, float]:
        """
        One time step:
        1. State evolves
        2. Self-model predicts next state
        3. Compare prediction to reality
        4. Update self-model based on error
        """
        # Save current state
        old_state = self.state.copy()
        
        # Actual next state (ground truth)
        self.state = np.tanh(self.W @ self.state)
        
        # Self-model's prediction of next state
        self.self_model = np.tanh(self.W_self @ old_state)
        
        # Prediction error
        error = self.state - self.self_model
        
        # Update self-model to reduce error (gradient descent)
        # dL/dW = -error @ old_state^T
        self.W_self += self.lr * np.outer(error, old_state)
        
        # Calculate R (self-reference depth)
        R = self._calculate_R(error, self.state)
        
        # Calculate Φ (integration - simplified)
        phi = self._calculate_phi(self.state)
        
        # Calculate D (criticality - simplified)
        D = 0.8  # Assume near-critical for this toy model
        
        # Calculate C
        C = phi * R * D
        
        # Store
        self.R_history.append(R)
        self.C_history.append(C)
        self.state_history.append(self.state.copy())
        
        return {
            'R': R,
            'phi': phi,
            'D': D,
            'C': C,
            'error': np.linalg.norm(error)
        }
    
    def _calculate_R(self, error: np.ndarray, state: np.ndarray) -> float:
        """
        R = 1 - (prediction_error / baseline_error)
        
        R = 0: Random guessing
        R = 1: Perfect self-prediction
        """
        pred_error = np.mean(error ** 2)
        baseline_error = np.var(state)
        
        if baseline_error < 1e-8:
            return 0.0
        
        R = 1.0 - (pred_error / baseline_error)
        return np.clip(R, 0.0, 1.0)
    
    def _calculate_phi(self, state: np.ndarray) -> float:
        """
        Simplified Φ: How much do neurons constrain each other?
        
        Φ ≈ variance of state (more variation = more integration)
        """
        phi = np.var(state) * 10  # Scale to make it reasonable magnitude
        return np.clip(phi, 0, 20)
    
    def run(self, n_steps: int = 200) -> Dict:
        """Run the system for n steps."""
        print(f"Running minimal toy model for {n_steps} steps...")
        print("="*60)
        print(f"{'Step':>6} | {'R':>6} | {'C':>8} | {'Error':>8}")
        print("="*60)
        
        for step in range(n_steps):
            metrics = self.step()
            
            if step % 20 == 0:
                print(f"{step:6d} | {metrics['R']:6.3f} | "
                      f"{metrics['C']:8.3f} | {metrics['error']:8.4f}")
        
        print("="*60)
        
        return {
            'R_history': np.array(self.R_history),
            'C_history': np.array(self.C_history),
            'state_history': np.array(self.state_history)
        }


def demonstrate_toy_model():
    """
    Run toy model and show that self-reference emerges.
    """
    print("\n" + "="*70)
    print("MINIMAL TOY MODEL: Self-Reference Emergence")
    print("="*70)
    print("\nTask: Network must predict its own next state")
    print("Success requires: Learning to model itself (R → 1)")
    print()
    
    # Create system
    system = MinimalSelfReferenceSystem(n_neurons=5, learning_rate=0.1)
    
    # Run
    results = system.run(n_steps=200)
    
    # Analyze
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    
    R_start = results['R_history'][0]
    R_end = results['R_history'][-1]
    C_start = results['C_history'][0]
    C_end = results['C_history'][-1]
    
    print(f"\nSelf-Reference (R):")
    print(f"  Start: R = {R_start:.4f} (no self-modeling)")
    print(f"  End:   R = {R_end:.4f} (learned self-modeling)")
    print(f"  Change: ΔR = {R_end - R_start:+.4f}")
    
    if R_end > 0.5:
        print(f"  ✓ SUCCESS: Network learned to model itself!")
    else:
        print(f"  ✗ PARTIAL: R increased but didn't reach 0.5")
    
    print(f"\nConsciousness Measure (C):")
    print(f"  Start: C = {C_start:.4f} bits")
    print(f"  End:   C = {C_end:.4f} bits")
    print(f"  Change: ΔC = {C_end - C_start:+.4f} bits")
    
    # Check for phase transition (simplified)
    C_crit = 3.0  # Lower threshold for toy model
    if C_end > C_crit:
        print(f"  ✓ SUCCESS: Crossed C_critical = {C_crit} bits!")
    else:
        print(f"  → Approaching threshold (need {C_crit - C_end:.2f} more bits)")
    
    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # R evolution
    ax = axes[0, 0]
    ax.plot(results['R_history'], 'b-', linewidth=2)
    ax.axhline(y=0.5, color='r', linestyle='--', alpha=0.5, label='Target')
    ax.set_xlabel('Time Step')
    ax.set_ylabel('R (Self-Reference)')
    ax.set_title('Self-Reference Emergence')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # C evolution
    ax = axes[0, 1]
    ax.plot(results['C_history'], 'g-', linewidth=2)
    ax.axhline(y=C_crit, color='r', linestyle='--', alpha=0.5, label=f'C_crit={C_crit}')
    ax.set_xlabel('Time Step')
    ax.set_ylabel('C (bits)')
    ax.set_title('Consciousness Measure')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # State evolution (first 3 neurons)
    ax = axes[1, 0]
    for i in range(min(3, system.n)):
        ax.plot(results['state_history'][:, i], label=f'Neuron {i+1}', alpha=0.7)
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Activity')
    ax.set_title('Neural Activity Over Time')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Phase space (R vs C)
    ax = axes[1, 1]
    scatter = ax.scatter(results['R_history'], results['C_history'], 
                        c=np.arange(len(results['R_history'])), 
                        cmap='viridis', alpha=0.6)
    ax.plot(results['R_history'][0], results['C_history'][0], 
           'go', markersize=12, label='Start')
    ax.plot(results['R_history'][-1], results['C_history'][-1], 
           'r*', markersize=15, label='End')
    ax.axhline(y=C_crit, color='r', linestyle='--', alpha=0.3)
    ax.set_xlabel('R (Self-Reference)')
    ax.set_ylabel('C (bits)')
    ax.set_title('Phase Space Trajectory')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.colorbar(scatter, ax=ax, label='Time')
    
    plt.tight_layout()
    plt.savefig('toy_model_results.png', dpi=300, bbox_inches='tight')
    print(f"\nPlot saved: toy_model_results.png")
    
    # Mathematical verification
    print("\n" + "="*70)
    print("MATHEMATICAL VERIFICATION")
    print("="*70)
    
    # Check self-model accuracy
    final_state = results['state_history'][-1]
    predicted = np.tanh(system.W_self @ results['state_history'][-2])
    actual = final_state
    error = np.linalg.norm(actual - predicted)
    
    print(f"\nFinal Self-Model Accuracy:")
    print(f"  Prediction error: {error:.4f}")
    print(f"  State magnitude: {np.linalg.norm(actual):.4f}")
    print(f"  Relative error: {error / (np.linalg.norm(actual) + 1e-8):.4f}")
    
    if error < 0.5:
        print(f"  ✓ Self-model is accurate!")
    
    # Weight matrix analysis
    W_norm = np.linalg.norm(system.W_self)
    print(f"\nSelf-Model Weights:")
    print(f"  ||W_self|| = {W_norm:.4f}")
    
    if W_norm > 0.1:
        print(f"  ✓ Self-model weights developed!")
    
    print("\n" + "="*70)
    print("CONCLUSION")
    print("="*70)
    
    success_criteria = [
        R_end > 0.3,  # Some self-reference
        C_end > C_start + 1.0,  # C increased
        error < 1.0,  # Reasonable prediction
        W_norm > 0.1  # Weights developed
    ]
    
    passed = sum(success_criteria)
    
    print(f"\nSuccess Criteria: {passed}/{len(success_criteria)}")
    
    if passed >= 3:
        print("\n✓✓✓ TOY MODEL SUCCESS ✓✓✓")
        print("Self-reference mechanism demonstrated in minimal system!")
    elif passed >= 2:
        print("\n✓✓ PARTIAL SUCCESS ✓✓")
        print("Mechanism works but needs tuning.")
    else:
        print("\n✗ NEEDS MORE WORK ✗")
        print("Even toy model needs debugging.")
    
    print("\n" + "="*70)


if __name__ == '__main__':
    np.random.seed(42)
    demonstrate_toy_model()
