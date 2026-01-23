"""
Ultimate Phi Debug - Trace Through _calculate_mutual_information
=================================================================
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Core'))

# Remove cached module
if 'consciousness_measure' in sys.modules:
    del sys.modules['consciousness_measure']

from consciousness_measure import ConsciousnessMeasure

print("=" * 70)
print("ULTIMATE PHI DEBUG - TRACE MI CALCULATION")
print("=" * 70)

# Create integrated pattern
N = 50
T = 100
module_size = N // 2

activity = np.zeros((N, T))

for t in range(T):
    phase1 = np.sin(t * 0.2)
    activity[:module_size, t] = (phase1 > 0).astype(float) * np.random.rand(module_size)
    
    phase2 = np.sin(t * 0.2 + np.pi/4)
    activity[module_size:, t] = (phase2 > 0).astype(float) * np.random.rand(N - module_size)

connectivity = np.zeros((N, N))
connectivity[:module_size, :module_size] = 0.3
connectivity[module_size:, module_size:] = 0.3
connectivity[:module_size, module_size:] = 0.1
connectivity[module_size:, :module_size] = 0.1
np.fill_diagonal(connectivity, 0)

print("\n[SETUP]")
print(f"Activity shape: {activity.shape}")
print(f"Connectivity shape: {connectivity.shape}")
print(f"Connectivity mean: {connectivity.mean():.4f}")

# Manually step through _calculate_Phi_geometric
activity_mean = activity.mean(axis=1)
threshold = np.median(activity_mean)
binary_activity = (activity_mean > threshold).astype(float)

np.random.seed(42)
indices = np.random.permutation(N)
half = N // 2
part1, part2 = indices[:half], indices[half:2*half]

W = connectivity
W_xy = W[np.ix_(part1, part2)]

print(f"\nPartition 1: {len(part1)} neurons")
print(f"Partition 2: {len(part2)} neurons")
print(f"W_xy shape: {W_xy.shape}")
print(f"W_xy mean: {W_xy.mean():.4f}")
print(f"W_xy sum: {W_xy.sum():.4f}")

# Now manually step through _calculate_mutual_information
x = binary_activity[part1]
y = binary_activity[part2]

print("\n[TRACE _calculate_mutual_information]")
print("-" * 70)

# Step 1: Binarize (AGAIN?)
print("\nStep 1: Binarize")
x_bin = (x > np.median(x)).astype(int)
y_bin = (y > np.median(y)).astype(int)
print(f"x input: {x}")
print(f"  median: {np.median(x)}")
print(f"  x_bin: {x_bin}")
print(f"y input: {y}")
print(f"  median: {np.median(y)}")
print(f"  y_bin: {y_bin}")

# Step 2: Individual entropies
print("\nStep 2: Calculate H(X) and H(Y)")

def calc_entropy(x):
    if len(x) == 0:
        return 0.0
    p = np.mean(x)
    if p == 0 or p == 1:
        return 0.0
    return -p * np.log2(p) - (1-p) * np.log2(1-p)

H_x = calc_entropy(x_bin)
H_y = calc_entropy(y_bin)

print(f"H(X) = {H_x:.4f} bits")
print(f"H(Y) = {H_y:.4f} bits")

# Step 3: Check connectivity
print("\nStep 3: Check connectivity between partitions")
w_total = np.abs(W_xy).sum()
print(f"w_total = {w_total:.4f}")

if w_total < 1e-10:
    print("⚠️  w_total < 1e-10, returning 0.0")
    print("THIS IS THE BUG - NO CONNECTIVITY BETWEEN RANDOM PARTITIONS!")
    MI = 0.0
else:
    # Step 4: Correlation
    print("\nStep 4: Calculate correlation")
    if len(x_bin) > 1 and len(y_bin) > 1 and len(x_bin) == len(y_bin):
        corr_matrix = np.corrcoef(x_bin, y_bin)
        print(f"Correlation matrix:\n{corr_matrix}")
        corr = np.abs(corr_matrix[0, 1])
    else:
        corr = w_total / (len(x_bin) * len(y_bin) + 1e-10)
        corr = np.clip(corr, 0, 1)
        print(f"Using connectivity proxy: {corr:.4f}")
    
    if np.isnan(corr):
        print("⚠️  Correlation is NaN")
        corr = 0.0
    
    print(f"Final corr = {corr:.4f}")
    
    # Step 5: Joint entropy
    print("\nStep 5: Approximate joint entropy")
    H_xy = H_x + H_y - corr * min(H_x, H_y)
    print(f"H(X,Y) = {H_x:.4f} + {H_y:.4f} - {corr:.4f} * {min(H_x, H_y):.4f}")
    print(f"H(X,Y) = {H_xy:.4f} bits")
    
    # Step 6: MI
    print("\nStep 6: Calculate MI")
    MI = H_x + H_y - H_xy
    print(f"MI = {H_x:.4f} + {H_y:.4f} - {H_xy:.4f} = {MI:.4f} bits")

print("\n" + "=" * 70)
print("DIAGNOSIS")
print("=" * 70)

if MI > 0:
    print(f"✓ MI = {MI:.4f} bits (non-zero)")
else:
    print("✗ MI = 0 - PROBLEM IDENTIFIED")
    if w_total < 1e-10:
        print("  → Random partition has ZERO connectivity between parts")
        print("  → Need to check if connectivity is actually being passed")
    elif H_x == 0 or H_y == 0:
        print("  → One partition has zero entropy (all same)")

# Now test with ACTUAL method
print("\n[TEST WITH ACTUAL METHOD]")
print("-" * 70)

cm = ConsciousnessMeasure(Phi_method='geometric')
np.random.seed(42)
Phi_result = cm.calculate_Phi(activity, connectivity, method='geometric')

print(f"Method result: Phi = {Phi_result:.4f} bits")
print(f"Manual MI = {MI:.4f} bits")

if abs(Phi_result - MI) < 0.001:
    print("✓ Results match")
else:
    print(f"✗ Mismatch! Method={Phi_result:.4f}, Manual={MI:.4f}")

print("=" * 70)
