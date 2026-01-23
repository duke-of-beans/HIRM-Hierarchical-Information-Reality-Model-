"""
Debug C(t) Calculation - Find Why R and D Return Zero
"""
import sys
import numpy as np

sys.path.insert(0, 'D:/Research/HIRM/Code/Core')
from consciousness_measure import ConsciousnessMeasure

# Load one epoch of actual Sleep-EDF data
import mne

edf_path = 'D:/Research/HIRM/Empirical/Datasets/Sleep_EDF/SC4001E0-PSG.edf'
raw = mne.io.read_raw_edf(edf_path, preload=True)
eeg_data = raw.get_data(picks=['EEG Fpz-Cz'])[0]
sfreq = 100.0

# Get first 30-second epoch
epoch = eeg_data[:int(30 * sfreq)]

print("="*70)
print("DIAGNOSTIC: Why R and D return zero")
print("="*70)
print(f"\nEpoch shape: {epoch.shape}")
print(f"Epoch range: [{epoch.min():.6f}, {epoch.max():.6f}]")
print(f"Epoch mean: {epoch.mean():.6f}, std: {epoch.std():.6f}")

# Replicate validation script's activity construction
n_delays = 5
delay = int(sfreq * 0.01)  # 10ms = 1 sample at 100Hz

print(f"\nDelay construction:")
print(f"  n_delays: {n_delays}")
print(f"  delay samples: {delay}")

activity = np.zeros((n_delays, len(epoch)))
for i in range(n_delays):
    shift = i * delay
    if shift < len(epoch):
        activity[i, shift:] = epoch[:-shift] if shift > 0 else epoch

print(f"\nActivity matrix shape: {activity.shape}")
print(f"Activity range: [{activity.min():.6f}, {activity.max():.6f}]")

# Check for variance
print(f"\nRow variances:")
for i in range(n_delays):
    print(f"  Row {i}: mean={activity[i].mean():.6f}, std={activity[i].std():.6f}")

# Check if rows are identical
print(f"\nRow correlation matrix:")
corr = np.corrcoef(activity)
print(corr)

# Create connectivity
connectivity = np.eye(n_delays)
for i in range(n_delays - 1):
    connectivity[i, i+1] = 0.5
    connectivity[i+1, i] = 0.5

print(f"\nConnectivity matrix:")
print(connectivity)

# Initialize calculator
cm = ConsciousnessMeasure(Phi_method='geometric', temporal_window=3000, D_max=8.0)

# Calculate components individually
print("\n" + "="*70)
print("COMPONENT CALCULATIONS")
print("="*70)

# Phi
Phi = cm.calculate_Phi(activity, connectivity)
print(f"\nΦ(t) = {Phi:.6f} bits")

# D_eff
D_eff = cm.calculate_D_eff(activity)
print(f"D_eff(t) = {D_eff:.6f}")

# R with history
R_obs = cm.calculate_R_obs(activity)
print(f"R_obs(t) = {R_obs:.6f}")

R_theory = cm.calculate_R_theory(R_obs)
print(f"R_theory(t) = {R_theory:.6f}")

# Full calculation
results = cm.calculate_C(activity, connectivity, history=activity)
print(f"\nFull C(t) calculation:")
print(f"  C = {results['C']:.6f}")
print(f"  Phi = {results['Phi']:.6f}")
print(f"  R_obs = {results['R_obs']:.6f}")
print(f"  R_theory = {results['R_theory']:.6f}")
print(f"  D_eff = {results['D_eff']:.6f}")

# MANUAL D calculation to debug
print("\n" + "="*70)
print("MANUAL D_eff DEBUGGING")
print("="*70)

N, T = activity.shape
print(f"Activity shape: N={N}, T={T}")

# Center data
activity_centered = activity - activity.mean(axis=1, keepdims=True)
print(f"Centered data range: [{activity_centered.min():.6f}, {activity_centered.max():.6f}]")

# Covariance
cov = (activity_centered @ activity_centered.T) / T
print(f"\nCovariance matrix:")
print(cov)
print(f"Covariance range: [{cov.min():.6f}, {cov.max():.6f}]")

# Eigenvalues
eigenvalues = np.linalg.eigvalsh(cov)
print(f"\nEigenvalues: {eigenvalues}")
eigenvalues_filtered = eigenvalues[eigenvalues > 1e-10]
print(f"Filtered eigenvalues (>1e-10): {eigenvalues_filtered}")

if len(eigenvalues_filtered) > 0:
    sum_eig = np.sum(eigenvalues_filtered)
    sum_eig_sq = np.sum(eigenvalues_filtered**2)
    D_raw = (sum_eig**2) / sum_eig_sq
    D_eff_manual = D_raw / 8.0
    print(f"\nsum(λ) = {sum_eig:.6f}")
    print(f"sum(λ²) = {sum_eig_sq:.6f}")
    print(f"D_raw = {D_raw:.6f}")
    print(f"D_eff = {D_eff_manual:.6f}")
else:
    print("\nNO VALID EIGENVALUES - This is the bug!")

# MANUAL R calculation to debug
print("\n" + "="*70)
print("MANUAL R_obs DEBUGGING")
print("="*70)

T_window = min(3000, activity.shape[1])
recent = activity[:, -T_window:]
print(f"Recent activity shape: {recent.shape}")

# Calculate autocorrelation for first neuron
neuron_activity = recent[0]
neuron_activity_centered = neuron_activity - np.mean(neuron_activity)
c0 = np.dot(neuron_activity_centered, neuron_activity_centered) / len(neuron_activity_centered)
print(f"\nNeuron 0 autocorrelation:")
print(f"  c0 = {c0:.6f}")

if c0 < 1e-10:
    print(f"  c0 too small - autocorrelation will fail!")
else:
    max_lag = min(20, T_window // 2)
    acf = []
    for lag in range(max_lag):
        if lag < len(neuron_activity_centered):
            c_lag = np.dot(neuron_activity_centered[:-lag or None], 
                          neuron_activity_centered[lag:]) / (len(neuron_activity_centered) - lag)
            acf.append(c_lag / c0)
    
    print(f"  ACF (first 5 lags): {acf[:5]}")
    R_proxy = np.sum(np.abs(acf)) / len(acf)
    print(f"  R_proxy = {R_proxy:.6f}")

print("\n" + "="*70)
print("DIAGNOSIS COMPLETE")
print("="*70)
