"""
HIRM Sleep-EDF Batch Validation Runner
=======================================
Runs the HIRM consciousness measure across ALL Sleep-EDF subjects.
Crash-safe: saves progress after each subject. Resume by re-running.
Pause: Ctrl+C saves progress cleanly. Re-run to continue.

Usage:
  python run_batch.py              # Run/resume all subjects
  python run_batch.py --aggregate  # Aggregate completed results only
  python run_batch.py --status     # Show progress

Output:
  Results/Sleep_EDF_Batch/progress.json     — tracks completion
  Results/Sleep_EDF_Batch/subject_NNN.csv   — per-subject raw results
  Results/Sleep_EDF_Batch/population.csv    — aggregated (after --aggregate)
  Results/Sleep_EDF_Batch/population.png    — population-level plots
"""

import sys
import os
import json
import time
import signal
import traceback
import numpy as np
import pandas as pd
import mne

# Setup paths
HIRM_ROOT = 'D:/Projects/HIRM'
sys.path.insert(0, os.path.join(HIRM_ROOT, 'Code/Core'))
DATASET_PATH = os.path.join(HIRM_ROOT, 'Empirical/Datasets')
BATCH_DIR = os.path.join(HIRM_ROOT, 'Empirical/Results/Sleep_EDF_Batch')
PROGRESS_FILE = os.path.join(BATCH_DIR, 'progress.json')

os.makedirs(BATCH_DIR, exist_ok=True)

# Valid subjects: 0-82 excluding 39, 68, 69, 78, 79
UNAVAILABLE_SUBJECTS = {39, 68, 69, 78, 79}
ALL_SUBJECTS = [s for s in range(83) if s not in UNAVAILABLE_SUBJECTS]

# Recording availability exceptions
NO_REC1 = {36, 52}   # missing recording 1
NO_REC2 = {13}        # missing recording 2

def get_recordings(subject):
    """Return valid recording indices for a subject."""
    recs = []
    if subject not in NO_REC1:
        recs.append(1)
    if subject not in NO_REC2:
        recs.append(2)
    return recs

# --- Progress tracking ---

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {'completed': {}, 'failed': {}, 'started_at': time.strftime('%Y-%m-%d %H:%M:%S')}

def save_progress(progress):
    # Write to temp first, then rename (atomic on Windows NTFS)
    tmp = PROGRESS_FILE + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(progress, f, indent=2)
    if os.path.exists(PROGRESS_FILE):
        os.replace(tmp, PROGRESS_FILE)
    else:
        os.rename(tmp, PROGRESS_FILE)

def get_job_key(subject, recording):
    return f"S{subject:03d}_R{recording}"

# --- Graceful shutdown ---

SHUTDOWN_REQUESTED = False

def handle_signal(signum, frame):
    global SHUTDOWN_REQUESTED
    if SHUTDOWN_REQUESTED:
        print("\n[FORCE QUIT] Exiting immediately.")
        sys.exit(1)
    SHUTDOWN_REQUESTED = True
    print("\n[PAUSING] Will stop after current subject finishes. Press Ctrl+C again to force quit.")

signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)


# --- Core processing ---

def process_subject(subject, recording):
    """Download (if needed) and process one subject/recording. Returns DataFrame or None."""
    from sleep_edf_validation import run_sleep_validation

    key = get_job_key(subject, recording)
    csv_path = os.path.join(BATCH_DIR, f"{key}.csv")

    # Download data
    try:
        paths = mne.datasets.sleep_physionet.age.fetch_data(
            subjects=[subject],
            recording=[recording],
            path=DATASET_PATH,
            verbose='ERROR'
        )
    except Exception as e:
        print(f"  [DOWNLOAD FAILED] {key}: {e}")
        return None

    psg_path = str(paths[0][0])
    hyp_path = str(paths[0][1])

    # Run validation (suppress MNE output)
    mne.set_log_level('ERROR')
    results_df = run_sleep_validation(psg_path, hyp_path, BATCH_DIR)

    if results_df is not None and len(results_df) > 0:
        results_df['subject'] = subject
        results_df['recording'] = recording
        results_df.to_csv(csv_path, index=False)
        return results_df
    return None


# --- Aggregation ---

def aggregate_results():
    """Combine all per-subject CSVs into population-level analysis."""
    print("\n" + "=" * 70)
    print("AGGREGATING POPULATION RESULTS")
    print("=" * 70)

    csvs = [f for f in os.listdir(BATCH_DIR) if f.startswith('S') and f.endswith('.csv')]
    if not csvs:
        print("No results to aggregate.")
        return

    all_dfs = []
    for csv in sorted(csvs):
        try:
            df = pd.read_csv(os.path.join(BATCH_DIR, csv))
            all_dfs.append(df)
        except Exception as e:
            print(f"  Skip {csv}: {e}")

    if not all_dfs:
        print("No valid results.")
        return

    pop = pd.concat(all_dfs, ignore_index=True)
    pop_path = os.path.join(BATCH_DIR, 'population.csv')
    pop.to_csv(pop_path, index=False)
    print(f"\nPopulation CSV: {pop_path}")
    print(f"Total epochs: {len(pop):,}")
    print(f"Subjects: {pop['subject'].nunique()}")
    print(f"Recordings: {len(csvs)}")

    # Stage-level statistics
    print(f"\n{'Stage':<12} {'C_mean':>8} {'C_std':>8} {'C_median':>8} {'n_epochs':>10}")
    print("-" * 52)

    stage_order = ['Sleep stage W', 'Sleep stage 1', 'Sleep stage R',
                   'Sleep stage 2', 'Sleep stage 3', 'Sleep stage 4']
    stage_short = {'Sleep stage W': 'Wake', 'Sleep stage 1': 'S1',
                   'Sleep stage R': 'REM', 'Sleep stage 2': 'S2',
                   'Sleep stage 3': 'S3', 'Sleep stage 4': 'S4'}

    stage_means = {}
    for stage in stage_order:
        mask = pop['stage'] == stage
        if mask.sum() == 0:
            continue
        vals = pop.loc[mask, 'C']
        stage_means[stage] = vals.mean()
        short = stage_short.get(stage, stage)
        print(f"  {short:<10} {vals.mean():>8.2f} {vals.std():>8.2f} {vals.median():>8.2f} {mask.sum():>10,}")

    # Ordering check
    print("\nORDERING CHECK:")
    ordered = sorted(stage_means.items(), key=lambda x: x[1], reverse=True)
    ordering_str = ' > '.join([f"{stage_short.get(s, s)}({v:.1f})" for s, v in ordered])
    print(f"  {ordering_str}")

    expected = ['Sleep stage W', 'Sleep stage 1', 'Sleep stage R',
                'Sleep stage 2', 'Sleep stage 3', 'Sleep stage 4']
    actual = [s for s, v in ordered]
    is_correct = actual == expected
    print(f"  Correct monotonic ordering: {'YES' if is_correct else 'NO'}")

    # Effect size: Wake vs S4
    if 'Sleep stage W' in stage_means and 'Sleep stage 4' in stage_means:
        wake_vals = pop.loc[pop['stage'] == 'Sleep stage W', 'C']
        s4_vals = pop.loc[pop['stage'] == 'Sleep stage 4', 'C']
        pooled_std = np.sqrt((wake_vals.var() + s4_vals.var()) / 2)
        if pooled_std > 0:
            cohens_d = (wake_vals.mean() - s4_vals.mean()) / pooled_std
            print(f"\n  Cohen's d (Wake vs S4): {cohens_d:.2f}")

    # T-test: conscious vs unconscious
    from scipy import stats
    conscious = pop.loc[pop['stage'].isin(['Sleep stage W', 'Sleep stage R']), 'C']
    unconscious = pop.loc[pop['stage'].isin(['Sleep stage 2', 'Sleep stage 3', 'Sleep stage 4']), 'C']
    if len(conscious) > 0 and len(unconscious) > 0:
        t, p = stats.ttest_ind(conscious, unconscious)
        print(f"  T-test conscious vs unconscious: t={t:.2f}, p={p:.2e}")
        print(f"  Conscious mean: {conscious.mean():.2f}, Unconscious mean: {unconscious.mean():.2f}")


    # Population plot
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        fig.suptitle(f'HIRM Sleep-EDF Population Validation (n={pop["subject"].nunique()} subjects)', fontsize=14)

        # Box plot by stage
        stage_data = []
        stage_labels = []
        for stage in stage_order:
            vals = pop.loc[pop['stage'] == stage, 'C'].dropna()
            if len(vals) > 0:
                stage_data.append(vals.values)
                stage_labels.append(stage_short.get(stage, stage))

        bp = axes[0].boxplot(stage_data, labels=stage_labels, patch_artist=True)
        colors = ['#2ecc71', '#f39c12', '#e74c3c', '#9b59b6', '#3498db', '#1abc9c']
        for patch, color in zip(bp['boxes'], colors[:len(stage_data)]):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        axes[0].set_ylabel('C(t) bits')
        axes[0].set_title('C(t) Distribution by Stage')
        axes[0].grid(True, alpha=0.3)

        # Per-subject means
        subj_means = pop.groupby(['subject', 'stage'])['C'].mean().unstack()
        for stage in stage_order:
            col = stage
            if col in subj_means.columns:
                vals = subj_means[col].dropna()
                axes[1].scatter([stage_short.get(stage, stage)] * len(vals), vals,
                              alpha=0.4, s=20, label=stage_short.get(stage, stage))
        axes[1].set_ylabel('C(t) bits (subject mean)')
        axes[1].set_title('Per-Subject Means')
        axes[1].grid(True, alpha=0.3)

        # Component means
        components = ['Phi', 'D_eff']
        comp_means = {}
        for comp in components:
            if comp in pop.columns:
                comp_means[comp] = pop.groupby('stage')[comp].mean()

        x = np.arange(len(stage_order))
        width = 0.35
        for i, comp in enumerate(components):
            if comp in comp_means:
                vals = [comp_means[comp].get(s, 0) for s in stage_order]
                axes[2].bar(x + i * width, vals, width, label=comp, alpha=0.8)
        axes[2].set_xticks(x + width / 2)
        axes[2].set_xticklabels([stage_short.get(s, s) for s in stage_order])
        axes[2].set_title('Component Means by Stage')
        axes[2].legend()
        axes[2].grid(True, alpha=0.3)

        plt.tight_layout()
        plot_path = os.path.join(BATCH_DIR, 'population.png')
        plt.savefig(plot_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"\nPlot saved: {plot_path}")

    except Exception as e:
        print(f"\nPlot error (non-fatal): {e}")

    print("\n" + "=" * 70)
    print("AGGREGATION COMPLETE")
    print("=" * 70)


# --- Main ---

def show_status():
    progress = load_progress()
    completed = progress.get('completed', {})
    failed = progress.get('failed', {})

    total_jobs = sum(len(get_recordings(s)) for s in ALL_SUBJECTS)
    n_done = len(completed)
    n_failed = len(failed)
    n_remaining = total_jobs - n_done - n_failed

    print(f"\n{'=' * 50}")
    print(f"HIRM Sleep-EDF Batch Status")
    print(f"{'=' * 50}")
    print(f"  Total jobs:     {total_jobs}")
    print(f"  Completed:      {n_done}")
    print(f"  Failed:         {n_failed}")
    print(f"  Remaining:      {n_remaining}")
    print(f"  Progress:       {n_done/total_jobs*100:.1f}%")
    if progress.get('started_at'):
        print(f"  Started:        {progress['started_at']}")
    if completed:
        last = max(completed.values(), key=lambda x: x.get('finished_at', ''))
        print(f"  Last completed: {last.get('finished_at', '?')}")
    if failed:
        print(f"\n  Failed subjects:")
        for key, info in sorted(failed.items()):
            print(f"    {key}: {info.get('error', '?')[:80]}")
    print()


def main():
    if '--aggregate' in sys.argv:
        aggregate_results()
        return

    if '--status' in sys.argv:
        show_status()
        return

    global SHUTDOWN_REQUESTED

    progress = load_progress()
    completed = progress.get('completed', {})
    failed = progress.get('failed', {})

    # Build job list
    jobs = []
    for subject in ALL_SUBJECTS:
        for rec in get_recordings(subject):
            key = get_job_key(subject, rec)
            if key not in completed:
                jobs.append((subject, rec, key))

    total_jobs = sum(len(get_recordings(s)) for s in ALL_SUBJECTS)
    n_done = len(completed)

    if not jobs:
        print("All subjects completed! Run with --aggregate to generate population results.")
        return

    print(f"\n{'=' * 70}")
    print(f"HIRM Sleep-EDF Batch Validation")
    print(f"{'=' * 70}")
    print(f"  Total jobs: {total_jobs}")
    print(f"  Already done: {n_done}")
    print(f"  Remaining: {len(jobs)}")
    print(f"  Ctrl+C to pause (saves progress cleanly)")
    print(f"{'=' * 70}\n")

    for i, (subject, rec, key) in enumerate(jobs):
        if SHUTDOWN_REQUESTED:
            print(f"\n[PAUSED] Progress saved. Re-run to continue from {key}.")
            save_progress(progress)
            return

        n_current = n_done + i + 1
        pct = n_current / total_jobs * 100
        print(f"[{n_current}/{total_jobs} {pct:.0f}%] Processing {key}...", end=' ', flush=True)

        start_t = time.time()
        try:
            result_df = process_subject(subject, rec)
            elapsed = time.time() - start_t

            if result_df is not None:
                n_epochs = len(result_df)
                c_mean = result_df['C'].mean()
                progress['completed'][key] = {
                    'finished_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'elapsed_s': round(elapsed, 1),
                    'n_epochs': n_epochs,
                    'c_mean': round(c_mean, 2)
                }
                print(f"OK ({n_epochs} epochs, C_mean={c_mean:.2f}, {elapsed:.0f}s)")
            else:
                progress['failed'][key] = {
                    'finished_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'error': 'No results returned'
                }
                print(f"EMPTY ({elapsed:.0f}s)")

        except Exception as e:
            elapsed = time.time() - start_t
            err_msg = str(e)[:200]
            progress['failed'][key] = {
                'finished_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'error': err_msg
            }
            print(f"FAILED ({elapsed:.0f}s): {err_msg}")
            traceback.print_exc()

        # Save progress after every subject (crash-safe)
        save_progress(progress)

    # All done
    print(f"\n{'=' * 70}")
    print(f"BATCH COMPLETE — {len(progress['completed'])} succeeded, {len(progress['failed'])} failed")
    print(f"{'=' * 70}")
    print(f"\nRun with --aggregate to generate population results.")


if __name__ == '__main__':
    main()
