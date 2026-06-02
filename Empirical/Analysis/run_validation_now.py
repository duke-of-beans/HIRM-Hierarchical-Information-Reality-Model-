"""Download one Sleep-EDF subject using MNE's built-in fetcher, then run HIRM validation."""
import mne
import sys
import os

# Download subject 0 from Sleep-EDF
print("Downloading Sleep-EDF subject 0...")
paths = mne.datasets.sleep_physionet.age.fetch_data(
    subjects=[0], 
    recording=[1],
    path='D:/Projects/HIRM/Empirical/Datasets'
)
print(f"Downloaded: {paths}")

psg_path = paths[0][0]  # PSG file
hyp_path = paths[0][1]  # Hypnogram file
print(f"PSG: {psg_path}")
print(f"Hypnogram: {hyp_path}")

# Fix sys.path for HIRM imports
sys.path.insert(0, 'D:/Projects/HIRM/Code/Core')

# Now run the validation
from sleep_edf_validation import run_sleep_validation, analyze_by_sleep_stage, test_threshold_prediction, plot_results

output_dir = 'D:/Projects/HIRM/Empirical/Results/Sleep_EDF'
os.makedirs(output_dir, exist_ok=True)

results_df = run_sleep_validation(str(psg_path), str(hyp_path), output_dir)
stats = analyze_by_sleep_stage(results_df)
test_results = test_threshold_prediction(results_df)
plot_results(results_df, output_dir)

print("\n" + "=" * 70)
print("DONE. Check results above.")
print("=" * 70)
