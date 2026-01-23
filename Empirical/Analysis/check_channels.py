"""
Check available EEG channels in Sleep-EDF dataset
"""
import mne

edf_path = 'D:/Research/HIRM/Empirical/Datasets/Sleep_EDF/SC4001E0-PSG.edf'
raw = mne.io.read_raw_edf(edf_path, preload=False, verbose=False)

print("Available channels:")
print("=" * 60)
for i, ch in enumerate(raw.ch_names):
    ch_type = raw.get_channel_types()[i]
    print(f"{i:2d}. {ch:30s} ({ch_type})")

print("\n" + "=" * 60)
print("EEG channels only:")
eeg_channels = [ch for ch, typ in zip(raw.ch_names, raw.get_channel_types()) if typ == 'eeg']
print(f"Found {len(eeg_channels)} EEG channels:")
for ch in eeg_channels:
    print(f"  - {ch}")
