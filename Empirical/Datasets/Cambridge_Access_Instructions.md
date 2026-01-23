# Cambridge Propofol Dataset - Access Instructions
# Created: 2026-01-18
# Status: READY FOR DOWNLOAD

## Dataset Specifications

**Perfect Match for HIRM Validation:**
- ✅ **20 participants** (excellent sample size)
- ✅ **91-channel EEG** (exceeds 64 minimum)
- ✅ **4 consciousness states**: Baseline, mild sedation, moderate sedation, recovery
- ✅ **~7 minutes per state** (~100K samples at 250 Hz)
- ✅ **Behavioral markers**: Reaction time + hit rate at each level
- ✅ **Propofol concentrations** measured in blood plasma
- ✅ **Preprocessed and artifact-free**
- ✅ **EEGLAB format** (MATLAB compatible)

## Direct Download

**URL**: https://www.repository.cam.ac.uk/bitstreams/e94a6722-da5b-4e53-8673-5e8ec106e0f7/download

**File**: sedation-restingstate.zip (3.44 GB)

**License**: CC BY 2.0 UK
- Can use for research
- Can modify and redistribute
- Must credit: Chennu et al. (2016) PLOS Computational Biology

## Data Structure

**Metadata File**: datainfo.mat
- Dataset name
- Sedation level (1=baseline, 2=mild, 3=moderate, 4=recovery)
- Propofol concentration (μg/L)
- Reaction time (ms)
- Hit rate (correct/40)

**EEG Files**: EEGLAB .set format
- 91 channels (scalp only, neck/cheeks/forehead excluded)
- 250 Hz sampling
- 0.5-45 Hz bandpass filter
- 10-second epochs
- Average-referenced
- Artifact-rejected

## Expected Directory Structure After Download

```
sedation-restingstate/
├── datainfo.mat
├── sub001_baseline.set
├── sub001_baseline.fdt
├── sub001_mild.set
├── sub001_mild.fdt
├── sub001_moderate.set
├── sub001_moderate.fdt
├── sub001_recovery.set
├── sub001_recovery.fdt
├── sub002_baseline.set
... (20 subjects × 4 conditions = 80 files)
```

## Validation Pipeline Adaptation

### Step 1: Download and Extract (10 minutes)
```bash
# Download
wget https://www.repository.cam.ac.uk/bitstreams/e94a6722-da5b-4e53-8673-5e8ec106e0f7/download -O sedation-restingstate.zip

# Extract to datasets directory
unzip sedation-restingstate.zip -d D:/Research/HIRM/Empirical/Datasets/Cambridge_Propofol/
```

### Step 2: Load EEGLAB Data in Python (30 minutes)
```python
import mne
from scipy.io import loadmat

# Load metadata
datainfo = loadmat('datainfo.mat')

# Load single EEG file
raw = mne.io.read_raw_eeglab('sub001_baseline.set', preload=True)

# Extract data: (91 channels, ~105,000 timepoints)
data = raw.get_data()  # (91, T)
sfreq = raw.info['sfreq']  # 250 Hz
ch_names = raw.ch_names  # Channel labels
```

### Step 3: Apply HIRM (30 minutes)
```python
from consciousness_measure import ConsciousnessMeasure

# Initialize
cm = ConsciousnessMeasure(
    Phi_method='PSI',
    temporal_window=2500,  # 10 seconds at 250 Hz
    D_max=91 * 0.8,  # Scale with channels
    Phi_scale=1.0
)

# Compute connectivity
connectivity = np.corrcoef(data)
connectivity = np.abs(connectivity)
np.fill_diagonal(connectivity, 1.0)

# Calculate C
result = cm.calculate_C(data, connectivity)
```

### Step 4: Compare Across States (30 minutes)
```python
results = {}
for state in ['baseline', 'mild', 'moderate', 'recovery']:
    # Load data
    raw = mne.io.read_raw_eeglab(f'sub001_{state}.set')
    data = raw.get_data()
    
    # Measure C
    conn = np.corrcoef(data)
    result = cm.calculate_C(data, conn)
    
    # Store
    results[state] = result['C']

# Expected: C decreases baseline → mild → moderate
# Expected: C increases moderate → recovery
```

## Expected Results

### Hypothesis
**C(t) ordering**: Baseline > Recovery > Mild > Moderate

**Rationale**:
- Baseline: Awake, conscious (high C)
- Mild: Sedated but responsive (moderate C)
- Moderate: Near LOC (low C)
- Recovery: Regaining consciousness (high C)

### Critical Test
**Does C cross 8.3 bit threshold between mild and moderate sedation?**

If YES → Validates C_critical prediction
If NO → Need to recalibrate threshold or D_max scaling

### Behavioral Correlation
**Does C correlate with**:
- Reaction time (lower RT = higher C)
- Hit rate (higher accuracy = higher C)
- Propofol concentration (higher dose = lower C)

## Publication Impact

### If Validation Succeeds
**Paper 1 becomes**:
- Simulation validation (proof of concept)
- Empirical validation with 20 subjects, 4 states
- Direct test of C_critical = 8.3 bits
- Correlation with behavioral markers

**Figure 2**:
- Panel A: C across 4 states (boxplot, N=20)
- Panel B: C vs propofol concentration (scatter + regression)
- Panel C: C vs reaction time (correlation)
- Panel D: Individual subject trajectories (baseline → recovery)

### If Validation Fails
**Diagnostic**:
- Does ordering still hold? (qualitative validation)
- Is scaling wrong? (need D_max recalibration)
- Are components responding? (Phi, R, D breakdown)

**Honest reporting**:
- "Empirical results show [findings]"
- "Discrepancy suggests [interpretation]"
- "Future work should [next steps]"

## Timeline

**Total**: 2-3 hours
- Download: 10-15 minutes (3.44 GB)
- Setup: 15 minutes (install MNE, test loading)
- Adaptation: 1 hour (modify validation script)
- Running: 30 minutes (20 subjects × 4 states)
- Analysis: 30 minutes (plots + statistics)

## Citation

**Required Attribution**:
Chennu, S., O'Connor, S., Adapa, R., Menon, D. K., & Bekinschtein, T. A. (2016). 
Brain Connectivity Dissociates Responsiveness from Drug Exposure during Propofol-Induced Transitions of Consciousness. 
PLOS Computational Biology, 12(1), e1004669. 
https://doi.org/10.1371/journal.pcbi.1004669

**Repository**:
University of Cambridge Data Repository
https://doi.org/10.17863/CAM.68959

---

**Status**: READY TO DOWNLOAD ✅
**Next**: Download dataset and begin validation
**Expected completion**: 2-3 hours
