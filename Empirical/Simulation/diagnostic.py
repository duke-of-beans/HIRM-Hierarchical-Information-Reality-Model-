"""
Diagnostic: Why are C values too low?
"""
import numpy as np
import pickle

# Load results
with open('D:/Research/HIRM/Empirical/Simulation/simulation_results.pkl', 'rb') as f:
    conditions = pickle.load(f)

print("Component Breakdown Analysis")
print("=" * 70)

for cond in conditions:
    print(f"\n{cond['name']}:")
    print(f"  Phi = {cond['Phi']:.3f} bits (should vary 1-10 with coupling)")
    print(f"  R = {cond['R']:.3f} (should vary 1-3 with recurrence)")
    print(f"  D = {cond['D']:.3f} (varying correctly: 0-1 range)")
    print(f"  C = Phi × R × D = {cond['Phi']} × {cond['R']} × {cond['D']} = {cond['C']:.3f}")
    
    # Check activity properties
    act = cond['activity']
    print(f"  Activity stats:")
    print(f"    Shape: {act.shape}")
    print(f"    Mean: {act.mean():.3e}")
    print(f"    Std: {act.std():.3e}")
    print(f"    Range: [{act.min():.2f}, {act.max():.2f}]")
    
    # Check connectivity
    conn = np.corrcoef(act)
    print(f"  Connectivity:")
    print(f"    Mean correlation: {conn.mean():.3f}")
    print(f"    Std correlation: {conn.std():.3f}")

print("\n" + "=" * 70)
print("DIAGNOSIS:")
print("=" * 70)
print("1. Phi constant ~5.6 bits - PSI method not sensitive to coupling?")
print("2. R = 1.0 everywhere - Not detecting recurrent structure")
print("3. D varying correctly - Eigenvalue spectrum responding to omega_std")
print("\nConclusion: Need to:")
print("  - Pass activity history for R calculation")
print("  - Check why Phi doesn't vary with coupling")
print("  - Potentially adjust D_max scaling")
