"""
Debug Phi calculation with 3-channel data
"""
import numpy as np
import sys
sys.path.append('D:/Research/HIRM/Code/Core')
from consciousness_measure import ConsciousnessMeasure

# Load single epoch from validation results
import mne
raw = mne.io.read_raw_edf('D:/Research/HIRM/Empirical/Datasets/Sleep_EDF/SC4001E0-PSG.edf', preload=True, verbose=False)

# Get 3 channels
eeg_channels = ['EEG Fpz-Cz', 'EEG Pz-Oz', 'EOG horizontal']
data_3ch = raw.get_data(picks=eeg_channels)

# Extract single 30s epoch
sfreq = raw.info['sfreq']
epoch_samples = int(30 * sfreq)  # 3000 samples
epoch = data_3ch[:, :epoch_samples]

print("=" * 60)
print("3-CHANNEL PHI DIAGNOSTIC")
print("=" * 60)
print(f"\nEpoch shape: {epoch.shape}")
print(f"Channels: {eeg_channels}")

# Create connectivity (cross-correlation)
connectivity = np.corrcoef(epoch)
connectivity = np.abs(connectivity)
np.fill_diagonal(connectivity, 1.0)
connectivity += 0.1 * np.eye(3)

print(f"\nConnectivity matrix:")
print(connectivity)

# Initialize consciousness measure
cm = ConsciousnessMeasure(Phi_method='geometric', D_max=1.5, Phi_scale=10.0)

# Calculate Phi with detailed output
print(f"\n" + "=" * 60)
print("CALCULATING PHI (GEOMETRIC METHOD)")
print("=" * 60)

# Access private method for debugging
try:
    Phi_raw = cm._calculate_Phi_geometric(epoch, connectivity)
    Phi_scaled = Phi_raw * cm.Phi_scale
    
    print(f"\nPhi_raw (before scaling): {Phi_raw:.6f}")
    print(f"Phi_scale: {cm.Phi_scale}")
    print(f"Phi_final (after scaling): {Phi_scaled:.6f}")
    
    # Check binarization
    activity_mean = epoch.mean(axis=1, keepdims=True)
    activity_binary = (epoch > activity_mean).astype(int)
    
    print(f"\nBinarization check:")
    print(f"Activity mean per channel: {activity_mean.flatten()}")
    print(f"Binary states per channel:")
    for i, ch in enumerate(eeg_channels):
        n_zeros = (activity_binary[i] == 0).sum()
        n_ones = (activity_binary[i] == 1).sum()
        print(f"  {ch}: {n_zeros} zeros, {n_ones} ones")
    
    # Check unique states
    unique_states = np.unique(activity_binary.T, axis=0)
    print(f"\nUnique binary states: {len(unique_states)} out of 8 possible (2^3)")
    
except Exception as e:
    print(f"ERROR in Phi calculation: {e}")
    import traceback
    traceback.print_exc()
