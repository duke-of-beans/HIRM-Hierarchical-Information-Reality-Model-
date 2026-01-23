"""
HIRM Sleep-EDF Empirical Validation Script
==========================================

PURPOSE: Test HIRM's core prediction that C(t) = Φ × R × D crosses the 
         critical threshold C_critical = 8.3 ± 0.6 bits at wake/sleep boundary

DATASET: Sleep-EDF (PhysioNet) - Polysomnography with sleep stage annotations
         https://physionet.org/content/sleep-edfx/1.0.0/

PROTOCOL:
---------
1. Load EEG data (Fpz-Cz channel) + sleep stage annotations
2. Process in 30-second epochs (standard sleep scoring)
3. Calculate C(t) components (Phi, R_theory, D_eff) per epoch
4. Test threshold prediction: Wake/REM > 8.3 > N2/N3
5. Generate plots and statistical validation

EXPECTED PATTERNS (from literature):
------------------------------------
State | Φ    | R    | D    | C (bits) | Status
------|------|------|------|----------|----------
Wake  | 1.00 | 1.00 | 1.00 | 12-15    | Conscious
N1    | 0.85 | 0.75 | 0.80 | 6-8      | Critical
N2    | 0.70 | 0.60 | 0.70 | 4-5      | Unconscious
N3    | 0.30 | 0.30 | 0.40 | 0.5-1    | Deep
REM   | 0.90 | 0.70 | 0.85 | 7-9      | Altered

VERSION: 1.0
CREATED: 2026-01-18 Session 37
STATUS: Ready for data loading
"""

import sys
import numpy as np
import pandas as pd
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Add HIRM code to path
sys.path.insert(0, 'D:/Research/HIRM/Code/Core')

# Import HIRM consciousness measure (Variable Constitution v1.0)
from consciousness_measure import ConsciousnessMeasure

# Configuration
CONFIG = {
    'epoch_duration': 30,  # seconds (standard sleep scoring)
    'overlap': 15,  # seconds (50% overlap)
    'sampling_rate': 100,  # Hz (Sleep-EDF EEG)
    'eeg_channel': 'EEG Fpz-Cz',  # Primary channel
    'bandpass': (0.5, 45),  # Hz (standard EEG filtering)
    'C_critical': 8.3,  # bits (locked constant)
    'C_variance': 0.6,  # bits (uncertainty)
}

print("[OK] Sleep-EDF validation script initialized")
print(f"[OK] Critical threshold: C_critical = {CONFIG['C_critical']} ± {CONFIG['C_variance']} bits")
print("[WIP] Awaiting dataset loading...")


# ==============================================================================
# DATA LOADING FUNCTIONS
# ==============================================================================

def load_sleep_edf_file(edf_path, hypnogram_path):
    """
    Load Sleep-EDF data and annotations.
    
    Parameters
    ----------
    edf_path : str
        Path to .edf file containing EEG data
    hypnogram_path : str
        Path to hypnogram file with sleep stage annotations
        
    Returns
    -------
    eeg_data : np.ndarray
        Multichannel EEG signal (n_channels, samples)
    sleep_stages : pd.DataFrame
        DataFrame with columns: ['onset', 'duration', 'stage']
    sfreq : float
        Sampling frequency (Hz)
    channel_names : list
        Names of EEG channels used
    """
    try:
        import mne
    except ImportError:
        raise ImportError(
            "MNE-Python required for EEG loading. Install: pip install mne"
        )
    
    print(f"[WIP] Loading EEG from: {edf_path}")
    
    # Load EEG data
    raw = mne.io.read_raw_edf(edf_path, preload=True)
    
    # Get all neural channels: 2 EEG + 1 EOG for true multichannel integration
    # EOG is essential - eye movements differentiate wake from sleep
    eeg_channels = ['EEG Fpz-Cz', 'EEG Pz-Oz', 'EOG horizontal']
    eeg_data = raw.get_data(picks=eeg_channels)
    sfreq = raw.info['sfreq']
    
    n_channels, n_samples = eeg_data.shape
    
    print(f"[OK] Neural data loaded: {n_channels} channels × {n_samples} samples at {sfreq} Hz")
    print(f"[OK] Channels: {eeg_channels}")
    print(f"[OK] N={n_channels} ensures non-degenerate Phi calculation (geometric method requires N≥3)")
    print(f"[OK] Duration: {n_samples/sfreq/60:.1f} minutes")
    
    # Load sleep stage annotations
    print(f"[WIP] Loading annotations from: {hypnogram_path}")
    annotations = mne.read_annotations(hypnogram_path)
    
    # Convert to DataFrame
    sleep_stages = pd.DataFrame({
        'onset': annotations.onset,
        'duration': annotations.duration,
        'stage': annotations.description
    })
    
    print(f"[OK] Sleep stages loaded: {len(sleep_stages)} annotations")
    print(f"[OK] Stages present: {sleep_stages['stage'].unique()}")
    
    return eeg_data, sleep_stages, sfreq, eeg_channels


def preprocess_eeg(eeg_data, sfreq, bandpass=(0.5, 45)):
    """
    Preprocess multichannel EEG signal with bandpass filtering.
    
    Parameters
    ----------
    eeg_data : np.ndarray
        Raw EEG signal (n_channels, samples)
    sfreq : float
        Sampling frequency
    bandpass : tuple
        (low_freq, high_freq) in Hz
        
    Returns
    -------
    eeg_filtered : np.ndarray
        Bandpass filtered EEG (n_channels, samples)
    """
    try:
        from scipy.signal import butter, filtfilt
    except ImportError:
        print("[WARN] scipy not available, skipping filtering")
        return eeg_data
    
    print(f"[WIP] Bandpass filtering: {bandpass[0]}-{bandpass[1]} Hz")
    
    # Design butterworth filter
    nyq = sfreq / 2
    low = bandpass[0] / nyq
    high = bandpass[1] / nyq
    
    b, a = butter(4, [low, high], btype='band')
    
    # Apply filter to each channel
    n_channels = eeg_data.shape[0]
    eeg_filtered = np.zeros_like(eeg_data)
    
    for ch in range(n_channels):
        eeg_filtered[ch] = filtfilt(b, a, eeg_data[ch])
    
    print("[OK] Filtering complete")
    
    return eeg_filtered
    low = bandpass[0] / nyq
    high = bandpass[1] / nyq
    
    b, a = butter(4, [low, high], btype='band')
    
    # Apply filter
    eeg_filtered = filtfilt(b, a, eeg_data)
    
    print("[OK] Filtering complete")
    
    return eeg_filtered


# ==============================================================================
# EPOCH PROCESSING AND C(t) CALCULATION
# ==============================================================================

def create_epochs(eeg_data, sfreq, epoch_duration=30, overlap=15):
    """
    Create overlapping epochs from continuous multichannel EEG.
    
    Parameters
    ----------
    eeg_data : np.ndarray
        Continuous EEG signal (n_channels, samples)
    sfreq : float
        Sampling frequency
    epoch_duration : float
        Epoch length in seconds
    overlap : float
        Overlap between epochs in seconds
        
    Returns
    -------
    epochs : np.ndarray
        Array of shape (n_epochs, n_channels, samples_per_epoch)
    epoch_times : np.ndarray
        Start time of each epoch in seconds
    """
    n_channels = eeg_data.shape[0]
    samples_per_epoch = int(epoch_duration * sfreq)
    overlap_samples = int(overlap * sfreq)
    step = samples_per_epoch - overlap_samples
    
    # Calculate number of epochs
    n_samples = eeg_data.shape[1]
    n_epochs = (n_samples - samples_per_epoch) // step + 1
    
    # Create epochs
    epochs = np.zeros((n_epochs, n_channels, samples_per_epoch))
    epoch_times = np.zeros(n_epochs)
    
    for i in range(n_epochs):
        start = i * step
        end = start + samples_per_epoch
        
        if end > n_samples:
            break
            
        epochs[i] = eeg_data[:, start:end]
        epoch_times[i] = start / sfreq
    
    print(f"[OK] Created {n_epochs} epochs ({epoch_duration}s, {overlap}s overlap)")
    print(f"[OK] Epoch shape: ({n_channels} channels, {samples_per_epoch} samples)")
    
    return epochs[:n_epochs], epoch_times[:n_epochs]


def calculate_C_for_epoch(epoch, cm, sfreq):
    """
    Calculate C(t) components for a single multichannel epoch.
    
    PROPER MULTICHANNEL INTEGRATION (3 channels minimum):
    - Uses TRUE neural channels: 2 EEG + 1 EOG
    - EOG critical: eye movements differentiate wake from sleep
    - Connectivity based on cross-correlation between channels
    - N=3 ensures non-degenerate Phi partitions (geometric method)
    
    Parameters
    ----------
    epoch : np.ndarray
        Multichannel EEG data for one epoch (n_channels, samples)
    cm : ConsciousnessMeasure
        Initialized consciousness measure calculator
    sfreq : float
        Sampling frequency
        
    Returns
    -------
    results : dict
        C, Phi, R_obs, R_theory, D_eff, sigma
    """
    # epoch shape: (n_channels, samples)
    n_channels, n_samples = epoch.shape
    
    # Activity matrix: (N, T) where N=3 channels, T=time samples
    # This is TRUE multichannel data: 2 EEG + 1 EOG, not delay-embedding!
    activity = epoch  # Shape: (3, 3000) for 3 channels, 30s at 100 Hz
    
    # Calculate functional connectivity between channels
    # Use cross-correlation as proxy for structural connectivity
    connectivity = np.corrcoef(activity)
    
    # Ensure positive definite and well-conditioned
    connectivity = np.abs(connectivity)
    np.fill_diagonal(connectivity, 1.0)
    
    # Small regularization for numerical stability
    connectivity += 0.1 * np.eye(n_channels)
    
    # Calculate C(t)
    try:
        results = cm.calculate_C(
            activity=activity,
            connectivity=connectivity,
            history=activity  # Use same epoch for R calculation
        )
        return results
    except Exception as e:
        print(f"[WARN] C(t) calculation failed: {e}")
        return None


# ==============================================================================
# MAIN VALIDATION PIPELINE
# ==============================================================================

def run_sleep_validation(edf_path, hypnogram_path, output_dir='Results'):
    """
    Run complete Sleep-EDF validation pipeline.
    
    Parameters
    ----------
    edf_path : str
        Path to EEG .edf file
    hypnogram_path : str
        Path to hypnogram annotations
    output_dir : str
        Directory to save results
        
    Returns
    -------
    results_df : pd.DataFrame
        Epoch-by-epoch results with C(t) and sleep stages
    """
    print("\n" + "="*70)
    print("HIRM SLEEP-EDF EMPIRICAL VALIDATION")
    print("="*70 + "\n")
    
    # 1. Load data
    eeg_data, sleep_stages, sfreq, channel_names = load_sleep_edf_file(edf_path, hypnogram_path)
    
    # 2. Preprocess
    eeg_filtered = preprocess_eeg(eeg_data, sfreq, CONFIG['bandpass'])
    
    # 3. Create epochs
    epochs, epoch_times = create_epochs(
        eeg_filtered, 
        sfreq,
        CONFIG['epoch_duration'],
        CONFIG['overlap']
    )
    
    # 4. Initialize consciousness measure
    print("\n[WIP] Initializing consciousness measure calculator...")
    cm = ConsciousnessMeasure(
        Phi_method='PSI',  # PSI method for low-dimensional systems (N=3)
        temporal_window=int(CONFIG['epoch_duration'] * sfreq),
        D_max=1.5,  # CALIBRATED from empirical data
        Phi_scale=10.0  # CALIBRATED scaling factor
    )
    print("[OK] Calculator ready (Variable Constitution v1.0 - PSI method for N=3)")
    
    # 5. Calculate C(t) for each epoch
    print(f"\n[WIP] Calculating C(t) for {len(epochs)} epochs...")
    results_list = []
    
    for i, (epoch, t) in enumerate(zip(epochs, epoch_times)):
        if i % 10 == 0:
            print(f"[WIP] Processing epoch {i}/{len(epochs)}...")
        
        # Calculate C(t)
        result = calculate_C_for_epoch(epoch, cm, sfreq)
        
        if result is not None:
            # Find corresponding sleep stage
            stage_idx = (sleep_stages['onset'] <= t).sum() - 1
            if 0 <= stage_idx < len(sleep_stages):
                stage = sleep_stages.iloc[stage_idx]['stage']
            else:
                stage = 'Unknown'
            
            results_list.append({
                'time': t,
                'C': result['C'],
                'Phi': result['Phi'],
                'R_obs': result['R_obs'],
                'R_theory': result['R_theory'],
                'D_eff': result['D_eff'],
                'sigma': result['sigma'],
                'stage': stage
            })
    
    # Convert to DataFrame
    results_df = pd.DataFrame(results_list)
    
    print(f"\n[OK] C(t) calculation complete: {len(results_df)} valid epochs")
    
    # 6. Save raw results
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    csv_file = output_path / 'sleep_edf_raw_results.csv'
    results_df.to_csv(csv_file, index=False)
    print(f"[OK] Raw results saved: {csv_file}")
    
    return results_df


# ==============================================================================
# STATISTICAL ANALYSIS AND THRESHOLD TESTING
# ==============================================================================

def analyze_by_sleep_stage(results_df):
    """
    Compute statistics grouped by sleep stage.
    
    Parameters
    ----------
    results_df : pd.DataFrame
        Results from run_sleep_validation()
        
    Returns
    -------
    stats : pd.DataFrame
        Mean ± SD for each component by sleep stage
    """
    print("\n" + "="*70)
    print("SLEEP STAGE ANALYSIS")
    print("="*70 + "\n")
    
    # Group by sleep stage
    components = ['C', 'Phi', 'R_theory', 'D_eff']
    stats = results_df.groupby('stage')[components].agg(['mean', 'std', 'count'])
    
    print(stats)
    
    # Test threshold prediction
    print("\n" + "="*70)
    print("THRESHOLD ANALYSIS")
    print("="*70 + "\n")
    
    C_crit = CONFIG['C_critical']
    
    for stage in stats.index:
        mean_C = stats.loc[stage, ('C', 'mean')]
        std_C = stats.loc[stage, ('C', 'std')]
        count = stats.loc[stage, ('C', 'count')]
        
        above_threshold = mean_C > C_crit
        status = "ABOVE" if above_threshold else "BELOW"
        
        print(f"{stage:8s}: C = {mean_C:6.3f} ± {std_C:5.3f} bits  "
              f"(n={count:3.0f})  [{status} {C_crit} bits]")
    
    return stats


def test_threshold_prediction(results_df):
    """
    Statistical test of threshold crossing prediction.
    
    Tests:
    1. Wake/REM > 8.3 > N2/N3
    2. Component ranges match literature
    3. Multiplicative structure validation
    """
    print("\n" + "="*70)
    print("HYPOTHESIS TESTING")
    print("="*70 + "\n")
    
    C_crit = CONFIG['C_critical']
    
    # Define conscious vs unconscious states
    conscious_states = ['W', 'Wake', 'REM', 'R']  # Possible labels
    unconscious_states = ['N2', 'N3', 'S2', 'S3', 'S4']
    
    # Filter data
    conscious_mask = results_df['stage'].isin(conscious_states)
    unconscious_mask = results_df['stage'].isin(unconscious_states)
    
    C_conscious = results_df.loc[conscious_mask, 'C']
    C_unconscious = results_df.loc[unconscious_mask, 'C']
    
    print(f"Conscious states (Wake/REM): n = {len(C_conscious)}")
    print(f"  Mean C = {C_conscious.mean():.3f} ± {C_conscious.std():.3f} bits")
    print(f"  Predicted: > {C_crit} bits")
    print(f"  Result: {'✓ PASS' if C_conscious.mean() > C_crit else '✗ FAIL'}\n")
    
    print(f"Unconscious states (N2/N3): n = {len(C_unconscious)}")
    print(f"  Mean C = {C_unconscious.mean():.3f} ± {C_unconscious.std():.3f} bits")
    print(f"  Predicted: < {C_crit} bits")
    print(f"  Result: {'✓ PASS' if C_unconscious.mean() < C_crit else '✗ FAIL'}\n")
    
    # T-test
    try:
        from scipy.stats import ttest_ind
        t_stat, p_value = ttest_ind(C_conscious, C_unconscious)
        print(f"T-test: t = {t_stat:.3f}, p = {p_value:.3e}")
        print(f"Result: {'✓ SIGNIFICANT' if p_value < 0.05 else '✗ NOT SIGNIFICANT'}")
    except ImportError:
        print("[WARN] scipy not available for t-test")
    
    return {
        'conscious_mean': C_conscious.mean(),
        'conscious_std': C_conscious.std(),
        'unconscious_mean': C_unconscious.mean(),
        'unconscious_std': C_unconscious.std(),
        'threshold_crossed': C_conscious.mean() > C_crit > C_unconscious.mean()
    }


# ==============================================================================
# VISUALIZATION (OPTIONAL - requires matplotlib)
# ==============================================================================

def plot_results(results_df, output_dir='Results'):
    """
    Create plots of C(t) vs time with sleep stages.
    
    NOTE: Requires matplotlib. If not available, skip plotting.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("[WARN] matplotlib not available, skipping plots")
        return
    
    print("\n[WIP] Generating plots...")
    
    fig, axes = plt.subplots(5, 1, figsize=(14, 10), sharex=True)
    
    time = results_df['time'] / 3600  # Convert to hours
    
    # Plot C(t)
    axes[0].plot(time, results_df['C'], 'b-', alpha=0.7, label='C(t)')
    axes[0].axhline(CONFIG['C_critical'], color='r', linestyle='--', 
                    label=f'C_critical = {CONFIG["C_critical"]} bits')
    axes[0].set_ylabel('C(t) [bits]')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Plot components
    axes[1].plot(time, results_df['Phi'], 'g-', alpha=0.7)
    axes[1].set_ylabel('Φ(t) [bits]')
    axes[1].grid(True, alpha=0.3)
    
    axes[2].plot(time, results_df['R_theory'], 'orange', alpha=0.7)
    axes[2].set_ylabel('R_theory(t)')
    axes[2].grid(True, alpha=0.3)
    
    axes[3].plot(time, results_df['D_eff'], 'purple', alpha=0.7)
    axes[3].set_ylabel('D_eff(t)')
    axes[3].grid(True, alpha=0.3)
    
    axes[4].plot(time, results_df['sigma'], 'brown', alpha=0.7)
    axes[4].set_ylabel('σ(t)')
    axes[4].set_xlabel('Time [hours]')
    axes[4].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    output_path = Path(output_dir)
    fig_file = output_path / 'sleep_edf_timeseries.png'
    plt.savefig(fig_file, dpi=150)
    print(f"[OK] Plot saved: {fig_file}")
    
    plt.close()


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

if __name__ == '__main__':
    """
    Example usage - modify paths as needed.
    """
    print("""
    ========================================================================
    HIRM SLEEP-EDF VALIDATION - INSTRUCTIONS
    ========================================================================
    
    1. Download Sleep-EDF dataset from:
       https://physionet.org/content/sleep-edfx/1.0.0/
    
    2. Extract files to: D:/Research/HIRM/Empirical/Datasets/Sleep_EDF/
    
    3. Modify paths below to point to a specific subject file
    
    4. Run: python sleep_edf_validation.py
    
    ========================================================================
    """)
    
    # Example paths (MODIFY THESE)
    edf_path = 'D:/Research/HIRM/Empirical/Datasets/Sleep_EDF/SC4001E0-PSG.edf'
    hypnogram_path = 'D:/Research/HIRM/Empirical/Datasets/Sleep_EDF/SC4001EC-Hypnogram.edf'
    output_dir = 'D:/Research/HIRM/Empirical/Results/Sleep_EDF'
    
    # Check if files exist
    if not Path(edf_path).exists():
        print(f"[FAIL] EEG file not found: {edf_path}")
        print("[INFO] Please download Sleep-EDF dataset first")
        sys.exit(1)
    
    # Run validation
    results_df = run_sleep_validation(edf_path, hypnogram_path, output_dir)
    
    # Analyze
    stats = analyze_by_sleep_stage(results_df)
    test_results = test_threshold_prediction(results_df)
    
    # Plot (optional)
    plot_results(results_df, output_dir)
    
    print("\n" + "="*70)
    print("VALIDATION COMPLETE")
    print("="*70)
    print(f"\n[OK] Results saved to: {output_dir}")
    print("[OK] Review plots and statistics to assess threshold prediction")
