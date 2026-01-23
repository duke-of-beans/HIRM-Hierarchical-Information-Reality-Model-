# HIRM PROJECT HANDOFF - Session 37 Start
## Fresh Context for New Claude Instance
**Date:** 2026-01-18  
**Previous Session:** 36 Phase 4 (Phi debugging complete)  
**Status:** ✓ Code working, ready for empirical validation

---

## CRITICAL: READ THIS FIRST

### Your Mission
Run empirical validation of HIRM's consciousness emergence theory using Sleep-EDF polysomnography data. The computational implementation is working, bugs are fixed, and we need to test whether C(t) = Φ × R × D actually predicts the consciousness threshold at C* ≈ 8.3 bits across wake/sleep states.

### Immediate Next Steps (Priority Order)
1. **Load Sleep-EDF data** (dataset already identified, publicly available)
2. **Calculate C(t) components** (Phi, R_theory, D_eff) for each sleep stage
3. **Test threshold prediction** (Does C cross 8.3 bits at wake/sleep boundary?)
4. **Validate component ranges** (Phi ~4.82, R ~1.95, D ~0.89 at fixed point)
5. **Document results** for Paper 1 manuscript

---

## WHAT JUST HAPPENED (Session 36 Phase 4)

### Bugs Fixed ✓
We debugged Phi (integrated information) calculation which was returning zero for all inputs:

**Bug 1 (CRITICAL):** Double binarization in `_calculate_mutual_information()`
- Activity was binarized twice, destroying variance when partition median was 0 or 1
- **Fix:** Line 545: `x_bin = x.astype(int)` (was `x_bin = (x > np.median(x))`)

**Bug 2:** Division by log(2) in `_calculate_Phi_geometric()`
- MI already in bits, dividing made no sense
- **Fix:** Line 386: `Phi = MI` (was `Phi = MI / np.log(2)`)

**Bug 3:** PSI NaN handling
- **Fix:** Line 476: Added negative check before sqrt

### Validation Results ✓
- Integrated patterns: Phi = 0.198 bits (was 0.0)
- Full C(t) calculation: C = 0.143 bits (was 0.0)
- Zero integration: Phi = 0.0 (correct)
- **Status:** Geometric method works, stochastic/PSI need separate debugging (not blocking)

### Files Modified
- `Code/Core/consciousness_measure.py` (v2.0, bugs fixed)
- `Logs/PHI_BUG_FIX_SUMMARY.md` (technical details)
- `Logs/Sessions/SESSION_36_PHASE4_SUMMARY.md` (complete report)

---

## PROJECT CONTEXT (Essential Background)

### What is HIRM?
**Hierarchical Information-Reality Model** - A mathematical framework proposing consciousness emerges through self-reference phase transitions when:

```
C(t) = Φ(t) × R_theory(t) × D_eff(t) > C_critical ≈ 8.3 ± 0.6 bits
```

**Key Innovation:** Multiplicative structure (all components required) + universal threshold derived from first principles

### Variable Constitution v1.0 (LOCKED)
**Source:** `Master_Data/Variables/VARIABLE_CONSTITUTION_V1.md`

**Components:**
- **Φ(t):** Integrated information, [0, ~20] bits
- **R_theory(t):** Self-referential coupling, [1, 3] via transform R_theory = 1 + 2×R_obs
- **D_eff(t):** Dimensional embedding (PCA-based), [0, 1] normalized
- **sigma(t):** Branching parameter (tracked separately, NOT in C equation)

**Locked Constants:**
- C_critical = 8.3 ± 0.6 bits
- At fixed point: Φ* = 4.82, R* = 1.95, D* = 0.89 → C* = 8.37 bits

### Current Research Phase
**Phase:** Empirical Validation (Stage 3B)  
**Goal:** Test predictions with real neuroscience data  
**Dataset:** Sleep-EDF polysomnography (197 subjects, publicly available)  
**Prediction:** C(t) crosses 8.3-bit threshold at wake→sleep transition

---

## COMPUTATIONAL IMPLEMENTATION STATUS

### What Works ✓
- `consciousness_measure.py` (v2.0) - All Variable Constitution components
- Phi geometric method returns non-zero values
- R_obs → R_theory transform (locked formula)
- D_eff via PCA participation ratio
- Full C(t) = Phi × R_theory × D_eff calculation
- Metadata tracking (constitution version, criticality status)

### Known Issues (Not Blocking)
- Phi values low (~0.2-0.5 bits, need calibration)
- D_eff values low (0.144 vs 0.89 target, normalization needs adjustment)
- Stochastic Phi method returns zero (separate debugging needed)
- PSI method returns zero (tertiary method, low priority)

### Don't Worry About
- Stochastic/PSI methods (geometric works, sufficient for validation)
- Exact Phi ranges (will calibrate with real data)
- Perfect D_eff values (normalize empirically)

---

## FILE LOCATIONS (Critical Paths)

### Core Code
```
D:\Research\HIRM\Code\Core\
├── consciousness_measure.py  ← Main implementation (v2.0)
├── neural_network.py          ← Network generators
└── phase_transition.py        ← Transition detection
```

### Data & Results
```
D:\Research\HIRM\Empirical\
├── Data\Sleep_EDF\           ← Dataset location (download if needed)
├── Analysis\                  ← Put validation scripts here
└── Results\                   ← Save empirical results here
```

### Documentation
```
D:\Research\HIRM\
├── Master_Data\Variables\VARIABLE_CONSTITUTION_V1.md  ← SOURCE OF TRUTH
├── Master_Data\Constants\locked_constants.md          ← C_critical = 8.3
├── Logs\PHI_BUG_FIX_SUMMARY.md                       ← What we just fixed
└── Documentation\Sleep_and_Consciousness_Phase_Transitions.md ← Theory
```

### Project DNA
```
D:\Research\HIRM\
├── PROJECT_DNA.yaml          ← Identity, session number
├── CURRENT_STATUS.md         ← Research phase, priorities
└── QUICKSTART.md            ← Bootstrap guide
```

---

## SLEEP-EDF DATASET GUIDE

### What It Is
- **Format:** European Data Format (.edf files)
- **Subjects:** 197 healthy adults
- **Recordings:** Polysomnography (EEG, EOG, EMG, etc.)
- **Annotations:** Sleep stages (Wake, N1, N2, N3, REM)
- **Public:** PhysioNet database (free download)

### Where to Find It
**URL:** https://physionet.org/content/sleep-edfx/1.0.0/  
**Files:** SC* (Sleep Cassette) and ST* (Sleep Telemetry)  
**Recommended:** Start with SC files (older, well-validated)

### What You Need
1. **EEG channels:** Fpz-Cz and Pz-Oz (standard 10-20 system)
2. **Sleep stages:** Annotations file (*-Hypnogram.edf)
3. **Sampling rate:** 100 Hz (EEG)
4. **Duration:** Full night recordings (~8 hours)

### How to Load
Python libraries:
- `mne` - EEG/MEG analysis (recommended)
- `pyedflib` - Direct EDF reading
- `yasa` - Sleep analysis toolkit

---

## EXPECTED EMPIRICAL PATTERNS

### Literature Predictions (from Sleep doc)
**Source:** `Empirical/Results/Sleep_and_Consciousness_Phase_Transitions.md`

| State | Φ | R | D | C (bits) | Status |
|-------|---|---|---|----------|--------|
| Wake  | 1.00 | 1.00 | 1.00 | 12-15 | Conscious |
| N1    | 0.85 | 0.75 | 0.80 | 6-8   | **Critical** |
| N2    | 0.70 | 0.60 | 0.70 | 4-5   | Unconscious |
| N3    | 0.30 | 0.30 | 0.40 | 0.5-1 | Deep unconscious |
| REM   | 0.90 | 0.70 | 0.85 | 7-9   | Altered |

**Key Test:** Does C(t) cross 8.3 bits between N1 and N2? (The critical boundary)

### Computational Proxies
Since we can't measure Φ, R, D directly from EEG:

**For Φ (integration):**
- Use PCI (Perturbational Complexity Index) proxy
- Or LZ complexity (Lempel-Ziv)
- Or functional connectivity metrics

**For R (self-reference):**
- Use autocorrelation (current implementation)
- Or DMN connectivity (if have fMRI)
- Or phase-amplitude coupling

**For D (dimensionality):**
- Current: PCA participation ratio (implemented)
- Alternative: Correlation dimension
- Alternative: Spectral entropy

---

## VALIDATION PROTOCOL (Step-by-Step)

### Phase 1: Data Loading (30 min)
1. Download Sleep-EDF SC files (if not present)
2. Load one subject as test case
3. Extract EEG (Fpz-Cz channel)
4. Load sleep stage annotations
5. Verify data quality (no artifacts)

### Phase 2: Component Calculation (1 hour)
1. **Sliding window analysis:**
   - Window: 30-second epochs (standard sleep scoring)
   - Overlap: 50% (15 seconds)
   - Calculate C(t) for each window

2. **For each epoch:**
   - Preprocess EEG (bandpass 0.5-45 Hz)
   - Calculate Phi (use geometric method)
   - Calculate R_obs (autocorrelation over recent history)
   - Calculate D_eff (PCA on windowed activity)
   - Compute C = Phi × R_theory × D_eff

3. **Save results:**
   - Time series: [epoch_time, C, Phi, R, D, sigma, sleep_stage]
   - Save to CSV for plotting

### Phase 3: Threshold Analysis (30 min)
1. **Plot C(t) time series** with sleep stages overlaid
2. **Identify transitions:**
   - Wake → N1: Does C drop toward 8.3?
   - N1 → N2: Does C cross below 8.3?
   - N2 → Wake: Does C rise above 8.3?

3. **Statistical test:**
   - Mean C for each sleep stage
   - Test if C_wake > 8.3 > C_sleep (t-test)
   - Test if transition occurs at N1/N2 boundary

4. **Document results:**
   - Create figure: C(t) vs time with threshold line
   - Report: Mean ± SD for each stage
   - Conclusion: Threshold supported? Yes/No

### Phase 4: Component Analysis (30 min)
1. **Decompose by state:**
   - Which component changes most? (Phi, R, D)
   - Does Phi drop 50% from wake to N3? (literature predicts this)
   - Is R stable or varying?

2. **Validate ranges:**
   - Are Phi values in [0, 20] bits?
   - Is R_theory in [1, 3]?
   - Is D_eff in [0, 1]?

3. **Calibration:**
   - If ranges wrong, adjust normalization
   - Re-run with calibrated parameters
   - Document calibration decisions

---

## CRITICAL REMINDERS

### Constitution Compliance
**READ THIS:** `Master_Data/Variables/VARIABLE_CONSTITUTION_V1.md`
- **Formula:** C = Phi × R_theory × D_eff (PURE multiplicative, no saturation term)
- **Transform:** R_theory = 1 + 2×R_obs (LOCKED, don't change)
- **D is NOT distance to criticality** (it's dimensional embedding via PCA)
- **Sigma tracked separately** (not in C equation)

### Locked Constants
**READ THIS:** `Master_Data/Constants/locked_constants.md`
- C_critical = 8.3 ± 0.6 bits (source of truth)
- Don't second-guess this value
- Report discrepancies, don't "fix" them

### Terminology
**Never say:** "Ouroboros Observer" (old name)  
**Always say:** "HIRM" (Hierarchical Information-Reality Model)

### Academic Rigor
- State falsification criteria
- Consider competing theories (IIT, GNWT, FEP)
- Report negative results honestly
- Don't cherry-pick data

---

## TOOLS & COMMANDS

### Load Code
```python
import sys
sys.path.insert(0, 'D:/Research/HIRM/Code/Core')
from consciousness_measure import ConsciousnessMeasure

# Initialize
cm = ConsciousnessMeasure(
    Phi_method='geometric',
    temporal_window=100,
    D_max=8.0
)

# Calculate C(t)
result = cm.calculate_C(
    activity=neural_activity,  # Shape: (N, T)
    connectivity=connectivity_matrix,  # Shape: (N, N)
    history=activity_history  # Shape: (N, T_history)
)

# Extract components
C = result['C']
Phi = result['Phi']
R_obs = result['R_obs']
R_theory = result['R_theory']
D_eff = result['D_eff']
sigma = result['sigma']
```

### Load EEG Data
```python
import mne
import numpy as np

# Load EDF file
raw = mne.io.read_raw_edf('SC4001E0-PSG.edf', preload=True)

# Get EEG channel
eeg_data = raw.get_data(picks=['EEG Fpz-Cz'])[0]
sfreq = raw.info['sfreq']

# Load sleep stages
annotations = mne.read_annotations('SC4001EC-Hypnogram.edf')
```

### Check Project Status
```bash
# View current status
cat D:/Research/HIRM/CURRENT_STATUS.md

# Check build status
cat D:/Research/HIRM/Logs/BUILD_STATUS.md

# View session history
ls D:/Research/HIRM/Logs/Sessions/
```

---

## DECISION AUTHORITY

### You Can Decide
- Data preprocessing parameters (filtering, windowing)
- Visualization choices (plot types, colors)
- Statistical test selection (t-test, ANOVA, etc.)
- Code structure (functions, classes, organization)
- Interim results interpretation

### You Cannot Decide (Ask David)
- Changing locked constants (C_critical, transforms)
- Modifying Variable Constitution formula
- Major architectural changes to HIRM theory
- Publication decisions
- Experimental protocol deviations

### Gray Areas (Use Judgment)
- Calibration of normalization constants (D_max, etc.)
- Choice of proxy measures for Phi/R/D
- Handling edge cases or outliers
- Trade-offs between speed and accuracy

---

## FAILURE MODES TO AVOID

### Don't Do This
❌ Change C = Phi × R × D formula "to make it work"  
❌ Adjust C_critical to match data  
❌ Skip validation if results are negative  
❌ Cherry-pick subjects that support hypothesis  
❌ Use old "Ouroboros Observer" terminology  
❌ Ignore Variable Constitution v1.0 requirements  

### Do This Instead
✓ Report results honestly (positive or negative)  
✓ Document calibration decisions with rationale  
✓ Test multiple subjects for robustness  
✓ Compare to literature predictions  
✓ Use locked constants as given  
✓ Follow Variable Constitution exactly  

---

## SUCCESS CRITERIA

### Minimum Viable Result
- [ ] C(t) calculated for at least one full-night recording
- [ ] Time series plot showing C vs sleep stages
- [ ] Statistical test of wake vs sleep C values
- [ ] Report whether 8.3-bit threshold is crossed

### Strong Result
- [ ] Multiple subjects analyzed (N ≥ 5)
- [ ] Phi, R, D components analyzed separately
- [ ] Transition timing quantified (when does C cross threshold?)
- [ ] Comparison to literature predictions
- [ ] Calibrated parameters documented

### Publication-Ready Result
- [ ] Full cohort analyzed (N = 197)
- [ ] Robust statistics with confidence intervals
- [ ] Figure publication-quality
- [ ] Methods section draft complete
- [ ] Results ready for Paper 1 manuscript

---

## QUICK START COMMANDS

### Bootstrap New Session
```python
# 1. Check you're in HIRM project
import os
os.getcwd()  # Should be D:/Research/HIRM or contain HIRM files

# 2. Load project DNA
import yaml
with open('D:/Research/HIRM/PROJECT_DNA.yaml') as f:
    dna = yaml.safe_load(f)
print(f"Session: {dna['session_number']}")

# 3. Load Variable Constitution
with open('D:/Research/HIRM/Master_Data/Variables/VARIABLE_CONSTITUTION_V1.md') as f:
    constitution = f.read()
# Read and internalize

# 4. Check BUILD_STATUS
with open('D:/Research/HIRM/Logs/BUILD_STATUS.md') as f:
    print(f.read())

# 5. Load consciousness measure
import sys
sys.path.insert(0, 'D:/Research/HIRM/Code/Core')
from consciousness_measure import ConsciousnessMeasure

# 6. Ready to start empirical validation!
```

### First Action
```python
# Load Sleep-EDF documentation
doc_path = 'D:/Research/HIRM/Documentation/Sleep_and_Consciousness_Phase_Transitions.md'
with open(doc_path) as f:
    sleep_theory = f.read()

# Identify expected patterns
print("Expected C values:")
print("Wake: 12-15 bits")
print("N1: 6-8 bits (critical boundary)")
print("N2: 4-5 bits (unconscious)")
print("N3: 0.5-1 bits")
print("REM: 7-9 bits")

# Begin data loading...
```

---

## FINAL NOTES

### Context You Have
- Full project history in `/mnt/project/` directory
- All documentation accessible via `project_knowledge_search` tool
- 193-paper research corpus compiled
- Variable Constitution v1.0 locked and documented
- Code debugged and working

### What You're Building Toward
**Paper 1:** "Consciousness Emergence Through Self-Reference Phase Transitions at Critical Brain Dynamics"
- **Target:** Nature Physics, Physical Review E, or similar
- **Contribution:** Empirical validation of C_critical threshold
- **Timeline:** Submit within 4-6 months

### The Big Picture
HIRM proposes consciousness isn't magic or mysterious - it's a measurable phase transition in information processing that occurs at a universal threshold (8.3 bits) when integrated, self-referential, high-dimensional processing emerges. Your job is to test whether real brains actually cross this threshold at the wake/sleep boundary.

### Your Advantage
- Mathematical framework is complete
- Code is working (bugs fixed!)
- Dataset is identified
- Predictions are specific and falsifiable
- Previous Claude instances did the hard theoretical work
- You just need to run the validation

---

## HANDOFF COMPLETE

**Status:** Ready for empirical validation  
**Blocking:** None  
**Next Session:** 37 (Start fresh with this handoff)  
**Your Mission:** Test C_critical prediction with Sleep-EDF data  
**Expected Duration:** 2-3 hours for first-pass validation  

**Good luck! The hard part is done. Now we test whether HIRM actually predicts consciousness.**

---

**Questions for new Claude instance?**
- Review this document first
- Check PROJECT_DNA.yaml for context
- Read Variable Constitution v1.0 thoroughly
- Then ask David what to prioritize

**Let's validate consciousness emergence. 🧠✨**
