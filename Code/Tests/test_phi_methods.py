"""
Phi Method Comparison Test
===========================

Test all three Phi calculation methods to diagnose where the issue is:
1. Geometric (mutual information)
2. Stochastic (partition sampling)
3. PSI (practical simplicity index)

GOAL: Identify if Phi=0 is method-specific or fundamental
"""

import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Core'))
from consciousness_measure import ConsciousnessMeasure

print("=" * 70)
print("PHI METHOD COMPARISON TEST")
print("=" * 70)

# Create three instances with different methods
cm_geometric = ConsciousnessMeasure(Phi_method='geometric', D_max=8.0)
cm_stochastic = ConsciousnessMeasure(Phi_method='stochastic', D_max=8.0)
cm_psi = ConsciousnessMeasure(Phi_method='PSI', D_max=8.0)

# Test Case 1: Random activity (baseline)
print("\n[TEST 1] Random Activity (50 neurons, 100 timesteps)")
print("-" * 70)

N = 50
T = 100
activity_random = np.random.rand(N, T)
connectivity = np.random.rand(N, N) * 0.1
np.fill_diagonal(connectivity, 0)

phi_geom = cm_geometric.calculate_Phi(activity_random, connectivity, method='geometric')
phi_stoch = cm_stochastic.calculate_Phi(activity_random, connectivity, method='stochastic')
phi_psi = cm_psi.calculate_Phi(activity_random, connectivity, method='PSI')

print(f"Geometric:   Phi = {phi_geom:.4f} bits")
print(f"Stochastic:  Phi = {phi_stoch:.4f} bits")
print(f"PSI:         Phi = {phi_psi:.4f} bits")

# Test Case 2: Synchronized bursts (should have high integration)
print("\n[TEST 2] Synchronized Bursts (high integration)")
print("-" * 70)

activity_sync = np.zeros((N, T))
for t in range(T):
    if t % 20 < 10:  # Half the time in synchronized bursts
        # All neurons active together
        activity_sync[:, t] = np.random.rand(N) * 0.8 + 0.2
    else:
        # Low activity
        activity_sync[:, t] = np.random.rand(N) * 0.2

phi_geom = cm_geometric.calculate_Phi(activity_sync, connectivity, method='geometric')
phi_stoch = cm_stochastic.calculate_Phi(activity_sync, connectivity, method='stochastic')
phi_psi = cm_psi.calculate_Phi(activity_sync, connectivity, method='PSI')

print(f"Geometric:   Phi = {phi_geom:.4f} bits")
print(f"Stochastic:  Phi = {phi_stoch:.4f} bits")
print(f"PSI:         Phi = {phi_psi:.4f} bits")

# Test Case 3: Modular activity (functional modules)
print("\n[TEST 3] Modular Activity (2 functional groups)")
print("-" * 70)

activity_mod = np.zeros((N, T))
# Module 1: First half of neurons
# Module 2: Second half of neurons
for t in range(T):
    # Module 1 has one pattern
    if np.sin(t * 0.1) > 0:
        activity_mod[:N//2, t] = np.random.rand(N//2) * 0.8 + 0.2
    else:
        activity_mod[:N//2, t] = np.random.rand(N//2) * 0.2
    
    # Module 2 has phase-shifted pattern (coupling)
    if np.sin(t * 0.1 + np.pi/4) > 0:
        activity_mod[N//2:, t] = np.random.rand(N//2) * 0.8 + 0.2
    else:
        activity_mod[N//2:, t] = np.random.rand(N//2) * 0.2

# Modular connectivity (strong within modules, weak between)
connectivity_mod = np.random.rand(N, N) * 0.05
connectivity_mod[:N//2, :N//2] *= 4  # Strong within module 1
connectivity_mod[N//2:, N//2:] *= 4  # Strong within module 2
np.fill_diagonal(connectivity_mod, 0)

phi_geom = cm_geometric.calculate_Phi(activity_mod, connectivity_mod, method='geometric')
phi_stoch = cm_stochastic.calculate_Phi(activity_mod, connectivity_mod, method='stochastic')
phi_psi = cm_psi.calculate_Phi(activity_mod, connectivity_mod, method='PSI')

print(f"Geometric:   Phi = {phi_geom:.4f} bits")
print(f"Stochastic:  Phi = {phi_stoch:.4f} bits")
print(f"PSI:         Phi = {phi_psi:.4f} bits")

# Test Case 4: Independent neurons (zero integration)
print("\n[TEST 4] Independent Neurons (zero integration expected)")
print("-" * 70)

activity_indep = np.random.rand(N, T)
connectivity_zero = np.zeros((N, N))  # No connections

phi_geom = cm_geometric.calculate_Phi(activity_indep, connectivity_zero, method='geometric')
phi_stoch = cm_stochastic.calculate_Phi(activity_indep, connectivity_zero, method='stochastic')
phi_psi = cm_psi.calculate_Phi(activity_indep, connectivity_zero, method='PSI')

print(f"Geometric:   Phi = {phi_geom:.4f} bits (should be ~0)")
print(f"Stochastic:  Phi = {phi_stoch:.4f} bits (should be ~0)")
print(f"PSI:         Phi = {phi_psi:.4f} bits (should be ~0)")

# Test Case 5: Strong coupling (maximum integration)
print("\n[TEST 5] Strong Coupling (high integration expected)")
print("-" * 70)

# Create tightly coupled network
connectivity_strong = np.random.rand(N, N) * 0.4
np.fill_diagonal(connectivity_strong, 0)

# Activity driven by network (coupled dynamics)
activity_coupled = np.zeros((N, T))
activity_coupled[:, 0] = np.random.rand(N)
for t in range(1, T):
    # Network dynamics: x(t+1) = tanh(W * x(t) + noise)
    activity_coupled[:, t] = np.tanh(connectivity_strong @ activity_coupled[:, t-1] + 
                                     np.random.randn(N) * 0.1)

phi_geom = cm_geometric.calculate_Phi(activity_coupled, connectivity_strong, method='geometric')
phi_stoch = cm_stochastic.calculate_Phi(activity_coupled, connectivity_strong, method='stochastic')
phi_psi = cm_psi.calculate_Phi(activity_coupled, connectivity_strong, method='PSI')

print(f"Geometric:   Phi = {phi_geom:.4f} bits")
print(f"Stochastic:  Phi = {phi_stoch:.4f} bits")
print(f"PSI:         Phi = {phi_psi:.4f} bits")

# Summary
print("\n" + "=" * 70)
print("DIAGNOSTIC SUMMARY")
print("=" * 70)
print("\nPattern Analysis:")
print("  - If ALL methods return ~0: Activity patterns insufficient")
print("  - If PSI > 0 but Geometric/Stochastic = 0: Implementation issue")
print("  - If Geometric = 0 but others work: Geometric method needs fixing")
print("\nNext Steps:")
print("  → Check which methods produce non-zero values")
print("  → Identify which test cases work")
print("  → Debug the failing method(s)")
print("=" * 70)
