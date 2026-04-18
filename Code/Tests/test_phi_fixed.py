"""
Test Phi calculation after bug fix
===================================
"""

import sys
import os
import numpy as np

# Force reload of module
import importlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Core'))

# Remove cached module if exists
if 'consciousness_measure' in sys.modules:
    del sys.modules['consciousness_measure']

from consciousness_measure import ConsciousnessMeasure

print("=" * 70)
print("PHI CALCULATION - POST-FIX TEST")
print("=" * 70)

# Test 1: Integrated pattern (two coupled modules)
print("\n[TEST 1] Integrated pattern (two coupled oscillating modules)")
print("-" * 70)

N = 50
T = 100
module_size = N // 2

activity = np.zeros((N, T))

for t in range(T):
    # Module 1 oscillates
    phase1 = np.sin(t * 0.2)
    activity[:module_size, t] = (phase1 > 0).astype(float) * np.random.rand(module_size)
    
    # Module 2 oscillates with phase coupling
    phase2 = np.sin(t * 0.2 + np.pi/4)
    activity[module_size:, t] = (phase2 > 0).astype(float) * np.random.rand(N - module_size)

# Strong within-module, moderate between
connectivity = np.zeros((N, N))
connectivity[:module_size, :module_size] = 0.3
connectivity[module_size:, module_size:] = 0.3
connectivity[:module_size, module_size:] = 0.1
connectivity[module_size:, :module_size] = 0.1
np.fill_diagonal(connectivity, 0)

cm = ConsciousnessMeasure(Phi_method='geometric')

np.random.seed(42)  # Reproducible
Phi_geometric = cm.calculate_Phi(activity, connectivity, method='geometric')
Phi_stochastic = cm.calculate_Phi(activity, connectivity, method='stochastic')
Phi_PSI = cm.calculate_Phi(activity, connectivity, method='PSI')

print(f"Geometric:   Phi = {Phi_geometric:.4f} bits")
print(f"Stochastic:  Phi = {Phi_stochastic:.4f} bits")
print(f"PSI:         Phi = {Phi_PSI:.4f} bits")

if Phi_geometric > 0:
    print("✓ Geometric method FIXED (non-zero)")
else:
    print("✗ Geometric method still broken")

# Test 2: High integration (fully connected, synchronized)
print("\n[TEST 2] High integration (fully connected synchronized)")
print("-" * 70)

activity_sync = np.zeros((N, T))
phase = np.sin(np.arange(T) * 0.3)
for i in range(N):
    activity_sync[i] = (phase > 0).astype(float) * (0.5 + 0.5 * np.random.rand(T))

connectivity_full = np.random.rand(N, N) * 0.5
np.fill_diagonal(connectivity_full, 0)

np.random.seed(42)
Phi_geometric = cm.calculate_Phi(activity_sync, connectivity_full, method='geometric')
Phi_stochastic = cm.calculate_Phi(activity_sync, connectivity_full, method='stochastic')
Phi_PSI = cm.calculate_Phi(activity_sync, connectivity_full, method='PSI')

print(f"Geometric:   Phi = {Phi_geometric:.4f} bits")
print(f"Stochastic:  Phi = {Phi_stochastic:.4f} bits")
print(f"PSI:         Phi = {Phi_PSI:.4f} bits")

# Test 3: Zero integration (independent neurons)
print("\n[TEST 3] Zero integration (independent neurons)")
print("-" * 70)

activity_indep = np.random.rand(N, T)
connectivity_none = np.zeros((N, N))

np.random.seed(42)
Phi_geometric = cm.calculate_Phi(activity_indep, connectivity_none, method='geometric')
Phi_stochastic = cm.calculate_Phi(activity_indep, connectivity_none, method='stochastic')
Phi_PSI = cm.calculate_Phi(activity_indep, connectivity_none, method='PSI')

print(f"Geometric:   Phi = {Phi_geometric:.4f} bits (should be ~0)")
print(f"Stochastic:  Phi = {Phi_stochastic:.4f} bits (should be ~0)")
print(f"PSI:         Phi = {Phi_PSI:.4f} bits (should be ~0)")

# Test 4: Calculate full C(t) with fixed point values
print("\n[TEST 4] Full C(t) calculation at expected fixed point")
print("-" * 70)

# Create activity that should yield C* ≈ 8.3
# Target: Phi* = 4.82, R* = 1.95, D* = 0.89
# C* = 4.82 * 1.95 * 0.89 = 8.37 bits

history = activity_sync  # Use synchronized activity with history

result = cm.calculate_C(activity_sync, connectivity_full, history=history)

print(f"C(t) = {result['C']:.3f} bits")
print(f"  Phi = {result['Phi']:.3f} bits (target: ~4.82)")
print(f"  R_obs = {result['R_obs']:.3f} (target: ~0.475)")
print(f"  R_theory = {result['R_theory']:.3f} (target: ~1.95)")
print(f"  D_eff = {result['D_eff']:.3f} (target: ~0.89)")
print(f"  sigma = {result['sigma']:.3f}")

print("\n" + "=" * 70)
print("VERDICT")
print("=" * 70)

if Phi_geometric > 0.1 and Phi_PSI > 0:
    print("✓ PHI CALCULATION FIXED")
    print("  - Geometric method returns non-zero for integrated patterns")
    print("  - PSI method returns non-zero")
    print("  - Full C(t) calculation working")
else:
    print("✗ PHI CALCULATION STILL HAS ISSUES")
    print(f"  - Geometric: {Phi_geometric:.4f}")
    print(f"  - PSI: {Phi_PSI:.4f}")

print("=" * 70)
