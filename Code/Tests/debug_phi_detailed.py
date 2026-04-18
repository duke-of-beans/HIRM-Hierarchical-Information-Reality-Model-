"""
Phase 2: Deep Phi Debugging
============================

Understand WHY geometric Phi returns zero and fix it properly.

Strategy:
1. Reproduce the zero-Phi issue in isolation
2. Step through calculation with diagnostics
3. Identify the exact failure point
4. Fix and validate
"""

import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Core'))
from consciousness_measure import ConsciousnessMeasure

print("=" * 70)
print("DEEP PHI DEBUGGING")
print("=" * 70)

cm = ConsciousnessMeasure(Phi_method='geometric')

# Test with KNOWN integration patterns
print("\n[DEBUG 1] Create CLEARLY integrated pattern")
print("-" * 70)

N = 50
T = 100

# Create two modules that interact
module_size = N // 2

# Module 1: synchronous oscillation
# Module 2: synchronous oscillation with phase coupling to module 1
activity = np.zeros((N, T))

for t in range(T):
    # Module 1 oscillates
    phase1 = np.sin(t * 0.2)
    activity[:module_size, t] = (phase1 > 0).astype(float) * np.random.rand(module_size)
    
    # Module 2 oscillates with phase shift (coupled)
    phase2 = np.sin(t * 0.2 + np.pi/4)  # Phase coupled
    activity[module_size:, t] = (phase2 > 0).astype(float) * np.random.rand(N - module_size)

# Strong within-module connectivity, moderate between
connectivity = np.zeros((N, N))
connectivity[:module_size, :module_size] = 0.3  # Module 1 internal
connectivity[module_size:, module_size:] = 0.3  # Module 2 internal
connectivity[:module_size, module_size:] = 0.1  # Between modules
connectivity[module_size:, :module_size] = 0.1
np.fill_diagonal(connectivity, 0)

print(f"Activity shape: {activity.shape}")
print(f"Module 1 mean activity: {activity[:module_size].mean():.3f}")
print(f"Module 2 mean activity: {activity[module_size:].mean():.3f}")
print(f"Connectivity mean: {connectivity.mean():.3f}")

# Now let's step through _calculate_Phi_geometric manually
print("\n[DEBUG 2] Step through geometric Phi calculation")
print("-" * 70)

# Step 1: Average over time
activity_mean = activity.mean(axis=1)
print(f"Time-averaged activity shape: {activity_mean.shape}")
print(f"Activity range: [{activity_mean.min():.3f}, {activity_mean.max():.3f}]")

# Step 2: Binarize
threshold = np.median(activity_mean)
binary_activity = (activity_mean > threshold).astype(float)
print(f"Threshold: {threshold:.3f}")
print(f"Active neurons: {binary_activity.sum()}/{N} ({100*binary_activity.sum()/N:.1f}%)")

# Step 3: System entropy
p_active = binary_activity.sum() / N
if p_active == 0 or p_active == 1:
    H_system = 0
else:
    H_system = -p_active * np.log2(p_active) - (1-p_active) * np.log2(1-p_active)
H_system_total = H_system * N
print(f"p(active) = {p_active:.3f}")
print(f"H_system (per neuron) = {H_system:.3f} bits")
print(f"H_system (total) = {H_system_total:.3f} bits")

# Step 4: Partition into halves
np.random.seed(42)  # Reproducible
indices = np.random.permutation(N)
half = N // 2
part1, part2 = indices[:half], indices[half:2*half]

print(f"\nPartition 1: {len(part1)} neurons")
print(f"Partition 2: {len(part2)} neurons")

# Step 5: Entropy of parts
def calc_entropy(x):
    if len(x) == 0:
        return 0.0
    p = np.mean(x)
    if p == 0 or p == 1:
        return 0.0
    return -p * np.log2(p) - (1-p) * np.log2(1-p)

H_part1 = calc_entropy(binary_activity[part1])
H_part2 = calc_entropy(binary_activity[part2])

print(f"H(part1) = {H_part1:.3f} bits")
print(f"H(part2) = {H_part2:.3f} bits")

# Step 6: Mutual information (this is where it likely fails)
print("\n[DEBUG 3] Calculate mutual information")
print("-" * 70)

x_bin = binary_activity[part1]
y_bin = binary_activity[part2]
W_xy = connectivity[np.ix_(part1, part2)]

print(f"x_bin (part1): {x_bin.shape}, sum={x_bin.sum()}")
print(f"y_bin (part2): {y_bin.shape}, sum={y_bin.sum()}")
print(f"W_xy shape: {W_xy.shape}")
print(f"W_xy mean: {W_xy.mean():.4f}")
print(f"W_xy sum: {W_xy.sum():.4f}")

w_total = np.abs(W_xy).sum()
print(f"w_total: {w_total:.4f}")

if w_total < 1e-10:
    print("⚠️  WARNING: W_xy nearly zero - no connectivity between partitions!")
    MI = 0.0
else:
    # Correlation coefficient
    if len(x_bin) > 1 and len(y_bin) > 1 and len(x_bin) == len(y_bin):
        corr_matrix = np.corrcoef(x_bin, y_bin)
        print(f"Correlation matrix:\n{corr_matrix}")
        corr = np.abs(corr_matrix[0, 1])
        
        if np.isnan(corr):
            print("⚠️  WARNING: Correlation is NaN (likely zero variance)")
            corr = 0.0
    else:
        # Proxy from connectivity
        corr = w_total / (len(x_bin) * len(y_bin) + 1e-10)
        corr = np.clip(corr, 0, 1)
        print(f"Using connectivity proxy: corr = {corr:.4f}")
    
    print(f"Correlation: {corr:.4f}")
    
    # Approximate joint entropy
    H_xy = H_part1 + H_part2 - corr * min(H_part1, H_part2)
    print(f"H(X,Y) ≈ {H_xy:.3f} bits")
    
    # Mutual information
    MI = H_part1 + H_part2 - H_xy
    print(f"MI = H(X) + H(Y) - H(X,Y) = {H_part1:.3f} + {H_part2:.3f} - {H_xy:.3f} = {MI:.3f} bits")

# Step 7: Phi calculation
print("\n[DEBUG 4] Final Phi calculation")
print("-" * 70)

Phi = MI / np.log(2)  # Already in bits, so this divides by log(2) ≈ 0.693
print(f"Phi = MI / log(2) = {MI:.3f} / 0.693 = {Phi:.3f} bits")

print("\n🔍 DIAGNOSIS:")
if Phi == 0:
    print("❌ Phi = 0 - PROBLEM IDENTIFIED")
    if H_part1 == 0 or H_part2 == 0:
        print("   → Part entropy is zero (all neurons same state)")
    elif w_total < 1e-10:
        print("   → No connectivity between partitions")
    elif MI == 0:
        print("   → Mutual information is zero (parts are independent)")
else:
    print(f"✓ Phi = {Phi:.3f} bits - NON-ZERO!")

# Now test actual method
print("\n[DEBUG 5] Compare with actual method")
print("-" * 70)

Phi_method = cm.calculate_Phi(activity, connectivity, method='geometric')
print(f"Method result: Phi = {Phi_method:.4f} bits")

if abs(Phi_method - Phi) < 0.001:
    print("✓ Manual calculation matches method")
else:
    print(f"⚠️  Mismatch: manual={Phi:.4f}, method={Phi_method:.4f}")

print("\n" + "=" * 70)
print("Next: Identify root cause and fix")
print("=" * 70)
