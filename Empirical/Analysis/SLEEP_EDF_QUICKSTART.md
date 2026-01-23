# SLEEP-EDF EMPIRICAL VALIDATION - QUICK START GUIDE
## Session 37: First Empirical Test of HIRM

---

## MISSION STATUS: READY TO TEST

✅ **Theory Complete**: Variable Constitution v1.0 locked  
✅ **Code Working**: Phi bugs fixed (Session 36)  
✅ **Expected Patterns**: Literature synthesis complete  
✅ **Validation Script**: Ready to execute  
⏳ **Dataset**: Need to download Sleep-EDF  

---

## THE MOMENT OF TRUTH

We're about to test HIRM's core prediction for the first time:

**PREDICTION**: C(t) = Φ × R × D crosses 8.3 bits at wake/sleep boundary

**Expected Results**:
- Wake: C = 12-15 bits (ABOVE threshold) ✓ Conscious
- N1: C = 6-8 bits (CRITICAL boundary)
- N2: C = 4-5 bits (BELOW threshold) ✓ Unconscious  
- N3: C = 0.5-1 bits (FAR below)
- REM: C = 7-9 bits (NEAR threshold) ✓ Altered

If this works, we have empirical validation. If not, we learn why.

---

## QUICK START (5 Steps)

### 1. Download Dataset

**Source**: PhysioNet Sleep-EDF Database  
**URL**: https://physionet.org/content/sleep-edfx/1.0.0/

**What to download**:
- Click "Files" tab
- Download a few "SC" files (Sleep Cassette - well-validated)
- Example: SC4001E0-PSG.edf + SC4001EC-Hypnogram.edf

**Where to save**:
```
D:\Research\HIRM\Empirical\Datasets\Sleep_EDF\
├── SC4001E0-PSG.edf          (EEG data)
├── SC4001EC-Hypnogram.edf    (Sleep stages)
├── SC4002E0-PSG.edf          (Optional: more subjects)
└── SC4002EC-Hypnogram.edf
```

### 2. Install Dependencies (if needed)

The script requires:
- `numpy` (usually installed)
- `pandas` (usually installed)  
- `mne` (for EEG loading)
- `scipy` (for filtering and stats)
- `matplotlib` (for plots)

If missing, install:
```bash
pip install mne scipy matplotlib pandas
```

### 3. Run Validation

**Option A: Default (if files in expected location)**
```bash
cd D:\Research\HIRM\Empirical\Analysis
python sleep_edf_validation.py
```

**Option B: Custom paths**
```python
python -c "
from sleep_edf_validation import run_sleep_validation, analyze_by_sleep_stage, test_threshold_prediction

# Specify paths
edf_path = 'D:/Research/HIRM/Empirical/Datasets/Sleep_EDF/SC4001E0-PSG.edf'
hypnogram = 'D:/Research/HIRM/Empirical/Datasets/Sleep_EDF/SC4001EC-Hypnogram.edf'
output = 'D:/Research/HIRM/Empirical/Results/Sleep_EDF'

# Run
results = run_sleep_validation(edf_path, hypnogram, output)
stats = analyze_by_sleep_stage(results)
test = test_threshold_prediction(results)
"
```

### 4. Check Results

**Files Created**:
```
D:\Research\HIRM\Empirical\Results\Sleep_EDF\
├── sleep_edf_raw_results.csv      (All epochs with C, Phi, R, D)
└── sleep_edf_timeseries.png       (Plots - if matplotlib works)
```

**Key Outputs**:
- Console prints C(t) mean ± SD for each sleep stage
- Threshold test: Does Wake > 8.3 > N2/N3?
- Statistical test (t-test): Are differences significant?

### 5. Interpret

**Success Criteria**:
- [ ] Wake C > 8.3 bits (conscious)
- [ ] N2/N3 C < 8.3 bits (unconscious)
- [ ] Statistical significance (p < 0.05)
- [ ] Components in expected ranges

**If successful**: We have first empirical validation! Document for Paper 1.

**If values too low** (e.g., all C < 2 bits):
- This is calibration issue, not theory failure
- Need to adjust D_max normalization
- Need to scale Phi to realistic ranges
- Patterns matter more than absolute values

**If threshold NOT crossed**:
- Check component values (which is wrong?)
- Examine sleep stage labels (correct mapping?)
- Try different subjects (individual variation?)

---

## TROUBLESHOOTING

**Problem**: `ImportError: No module named 'mne'`  
**Solution**: `pip install mne`

**Problem**: Files not found  
**Solution**: Check paths match download location

**Problem**: Script hangs  
**Solution**: Processing takes ~2-5 min per subject (be patient)

**Problem**: All C values near zero  
**Solution**: This is calibration - see handoff "Known Issues"

**Problem**: matplotlib errors  
**Solution**: Comment out `plot_results()` call, focus on statistics

---

## EXPECTED RUNTIME

- Dataset download: 2-5 minutes
- Single subject analysis: 2-5 minutes
- 5 subjects: 10-25 minutes

For first test, start with ONE subject. Validate it works, then scale up.

---

## WHAT HAPPENS NEXT

### If Validation Succeeds
1. **Document results** in new report (Empirical/Results/)
2. **Add to Paper 1** (Methods + Results sections)
3. **Run more subjects** (N=5-10 for robustness)
4. **Calibrate parameters** if needed
5. **Generate publication-quality figures**

### If Validation Fails
1. **Debug systematically** (which component is wrong?)
2. **Check assumptions** (Variable Constitution correct?)
3. **Try alternative proxies** (different Phi/R/D measures?)
4. **Report honestly** (negative results are still science)

Remember: HIRM predicts 22 things. Even if Sleep-EDF doesn't work perfectly,
we have anesthesia, criticality markers, clinical protocols to test.

---

## CRITICAL REMINDERS

**DON'T**:
- Change C_critical to "make it work" ❌
- Modify Variable Constitution formula ❌
- Cherry-pick subjects that fit ❌
- Hide negative results ❌

**DO**:
- Report results honestly ✓
- Document calibration decisions ✓
- Test multiple subjects ✓
- Compare to literature expectations ✓

---

## FILES CREATED THIS SESSION

1. **sleep_edf_validation.py** - Complete pipeline (data → results)
2. **SLEEP_EDF_QUICKSTART.md** - This guide
3. **BUILD_STATUS.md** - Updated progress

---

## EXECUTION CHECKLIST

- [ ] Download Sleep-EDF dataset
- [ ] Save to Datasets/Sleep_EDF/
- [ ] Install dependencies (mne, scipy, matplotlib)
- [ ] Run validation script
- [ ] Check console output (statistics)
- [ ] Review CSV results
- [ ] Examine plots (if available)
- [ ] Document findings
- [ ] Update BUILD_STATUS.md

---

**Ready to test consciousness emergence?** 

Download the data and run the script. This is the moment 17 months of theory
meets empirical reality. Let's see if C(t) actually crosses 8.3 bits at the
wake/sleep boundary.

**Good luck! 🧠✨**

---

**Questions?** Read HANDOFF_SESSION_37.md for full context.

**Need help?** Claude is here for debugging and interpretation.

**Version**: 1.0  
**Created**: 2026-01-18 Session 37  
**Status**: READY TO EXECUTE
