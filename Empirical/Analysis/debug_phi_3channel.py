"""
Diagnose why Phi = 0 with 3-channel data
"""
import numpy as np
import sys
sys.path.append('D:/Research/HIRM/Code/Core')
from consciousness_measure import ConsciousnessMeasure

# Load a single epoch from the validation results
import pandas as pd
import mne

print("Loading single epoch for diagnosis...")
edf_path = 'D:/Research/HIRM/Empirical/Datasets/Sleep_EDF/SC4001E0-PSG.edf'
raw = mne.io.read_raw_edf(edf_path, preload=True, verbose=False)

# Get 3 channels
channels = ['EEG Fpz-Cz', 'EEG Pz-Oz', 'EOG horizontal']
data = raw.get_data(picks=channels)
sfreq = raw.info['sfreq']

# Take first 30 seconds
epoch = data[:, :int(30*sfreq)]

print(f"\nEpoch shape: {epoch.shape}")
print(f"Channels: {len(channels)}")
print(f"Samples per channel: {epoch.shape[1]}")

# Create connectivity
connectivity = np.corrcoef(epoch)
connectivity = np.abs(connectivity)
np.fill_diagonal(connectivity, 1.0)
connectivity += 0.1 * np.eye(len(channels))

print(f"\nConnectivity matrix:")
print(connectivity)

# Initialize measure
cm = ConsciousnessMeasure(
    Phi_method='geometric',
    temporal_window=int(30 * sfreq),
    D_max=1.5,
    Phi_scale=10.0
)

print("\n" + "="*60)
print("Testing Phi calculation...")
print("="*60)

try:
    Phi = cm.calculate_Phi(epoch, connectivity)
    print(f"✓ Phi = {Phi:.6f} bits")
except Exception as e:
    print(f"✗ Phi calculation failed: {e}")
    import traceback
    traceback.print_exc()

# Try manual geometric calculation
print("\n" + "="*60)
print("Manual geometric Phi calculation:")
print("="*60)

# Binarize activity
activity_binary = (epoch > np.median(epoch, axis=1, keepdims=True)).astype(float)
print(f"Activity binarized: {activity_binary.shape}")
print(f"Mean activation: {activity_binary.mean():.3f}")

# Calculate geometric integration
from scipy.spatial.distance import hamming

n_channels = epoch.shape[0]
n_samples = epoch.shape[1]

# Whole system entropy
whole_entropy = 0
for t in range(n_samples):
    state = tuple(activity_binary[:, t])
    whole_entropy -= np.log2(1/n_samples + 1e-10)  # Rough approximation

# Partition entropy
partition_entropy = 0
for ch in range(n_channels):
    for t in range(n_samples):
        partition_entropy -= np.log2(1/n_samples + 1e-10)

# Geometric Phi (very simplified)
Phi_manual = max(0, (whole_entropy - partition_entropy) / n_channels)
print(f"Manual Phi (geometric approximation): {Phi_manual:.6f}")

print("\nDEBUGGING INFO:")
print(f"Data range: [{epoch.min():.2e}, {epoch.max():.2e}]")
print(f"Data mean: {epoch.mean():.2e}")
print(f"Data std: {epoch.std():.2e}")
print(f"Binary mean by channel: {activity_binary.mean(axis=1)}")
