# High-Density EEG Dataset Search Results
# Phase 2: Empirical Data Search
# Created: 2026-01-18

## CRITICAL FINDING: Cambridge Dataset Available

### **BEST MATCH: Chennu et al. Propofol Sedation Study**

**Specifications**:
- **Channels**: 128-channel high-density EEG
- **System**: EGI NetAmps 300 amplifier
- **Sampling**: 250 Hz
- **Reference**: Vertex
- **License**: CC BY 2.0 UK
- **Availability**: University of Cambridge Data Repository ✅ PUBLICLY AVAILABLE

**Experimental Design**:
- Baseline (no drug)
- Mild sedation (0.6 μg/ml propofol)
- Moderate sedation (1.2 μg/ml propofol)
- Recovery
- Behavioral assessment: Two-choice speeded response task at each level
- Data: Hit rate, reaction time, drug dosage

**Processing**:
- Preprocessed with EEGLAB
- 91 channels over scalp surface retained (neck/cheeks/forehead excluded)
- Filtered 0.5-45 Hz
- Segmented into 10-second epochs

**Source**:
- Publication: Chennu et al. (reliable brain measures for loss of consciousness)
- Repository: University of Cambridge Data Repository
- Tutorial: FieldTrip toolbox - https://www.fieldtriptoolbox.org/workshop/madrid2019/eeg_sedation/

**HIRM Validation Potential**: ⭐⭐⭐⭐⭐
- ✅ 128 channels (exceeds 64 minimum)
- ✅ Clear consciousness transitions (3 levels + recovery)
- ✅ Behavioral markers (hit rate, RT)
- ✅ Public access
- ✅ Preprocessed and quality-controlled
- ✅ Multiple subjects (exact N not stated)

---

## Additional High-Density Datasets Found

### **2. Massimini Lab: 256-Channel Propofol Study**

**Specifications**:
- **Channels**: 256-channel high-density EEG
- **Drug**: Propofol
- **States**: Wake, sedation, LOC, recovery
- **Features**: Slow-wave analysis, source modeling
- **Source**: PMC3041704 (2011 publication)

**Key Finding**: "256-channel EEG recordings in humans during propofol anesthesia"

**HIRM Potential**: ⭐⭐⭐⭐⭐
- ✅ 256 channels (4× minimum requirement)
- ✅ Clear LOC/ROC transitions
- ❓ Public availability unknown (contact authors)

### **3. Purdon Lab: Multi-Channel Propofol**

**Specifications**:
- **Study**: "EEG signatures of loss and recovery of consciousness"
- **Drug**: Propofol with precise behavioral markers
- **Features**: Alpha-band phase-amplitude coupling, slow-wave coherence
- **Source**: PNAS 2013, PMC3607036

**Key Finding**: "Low-frequency phase modulated alpha amplitude" with LOC/ROC prediction

**HIRM Potential**: ⭐⭐⭐⭐
- ✅ Well-characterized LOC/ROC transitions
- ✅ Multiple frequency bands analyzed
- ❓ Channel count not specified in abstract (likely 32-128)
- ❓ Data availability unknown

### **4. 128-Channel Coherence Study**

**Specifications**:
- **Channels**: 128-channel EEG
- **Subjects**: 5 volunteers
- **Drug**: Propofol
- **Analysis**: Phase coherence, sub-delta (0.05-1.5 Hz)
- **Source**: PMC4212622

**Key Finding**: "Significant drop in sub-delta slow-wave coherence between frontal, occipital, frontal-occipital pairs"

**HIRM Potential**: ⭐⭐⭐⭐
- ✅ 128 channels
- ✅ Propofol transitions
- ⚠️ Small N (5 subjects)
- ❓ Data availability unknown

---

## Other Relevant Findings

### Lower-Density Studies (Informative but Insufficient)
- 4-channel PLE monitor studies
- 2-channel BIS monitor data (standard clinical)
- Single-channel entropy monitoring

### fMRI Studies (Wrong Modality)
- High temporal resolution needed for HIRM
- fMRI BOLD too slow (~1 Hz)
- EEG essential for phase dynamics

---

## Immediate Action Plan

### Step 1: Access Cambridge Dataset (30 minutes)
**URL**: https://www.fieldtriptoolbox.org/workshop/madrid2019/eeg_sedation/
**Action**: 
1. Navigate to FieldTrip tutorial page
2. Locate data repository link
3. Download dataset
4. Verify format (should be EEGLAB-compatible)

### Step 2: Contact Massimini Lab (15 minutes)
**Target**: Request 256-channel propofol dataset
**Email**: Find contact info from PMC3041704 publication
**Ask**: "Is raw 256-channel EEG data from 2011 propofol study available?"

### Step 3: Adapt Validation Pipeline (1 hour)
**File**: `sleep_edf_validation.py` → `cambridge_validation.py`
**Changes**:
- Load 128-channel data (vs 3-channel)
- Adapt channel selection (91 scalp channels)
- Handle 250 Hz sampling (vs 100 Hz)
- Extract 3 sedation levels + baseline
- Compare with behavioral markers

### Step 4: Run Validation (30 minutes)
**Expected**: C increases with sedation depth → LOC → recovery
**Test**: Does C cross 8.3 bit threshold at LOC?

---

## Expected Outcomes

### If Cambridge Data Works
**Paper 1 Impact**:
- Figure 1: Simulation validation (qualitative)
- Figure 2: Empirical validation with 128-channel EEG
- Results: "C_critical threshold validated at LOC with propofol"
- Discussion: "First empirical demonstration of HIRM predictions"

**Timeline**: 2-3 hours to adapt pipeline + run + analyze

### If Cambridge Data Unavailable
**Fallback**:
- Contact authors directly (Srivas Chennu)
- Search University of Cambridge repository manually
- Try other datasets (Massimini, Purdon)
- Worst case: Paper 1 proceeds with simulation only

---

## Data Access Strategy

### Priority 1: Direct Download
- FieldTrip tutorial may include sample data
- Cambridge repository link from publication

### Priority 2: Author Contact
**Srivas Chennu**: Lead author of sedation study
**Email**: Find via publication or university directory
**Request**: "Raw 128-channel EEG data for consciousness research validation"

### Priority 3: Alternative Datasets
- Massimini 256-channel (contact lab)
- High-density sleep EEG (check PhysioNet, NSRR)
- DOC patient databases (requires IRB)

---

## Success Criteria

**MINIMUM**: Access to 64+ channel data during consciousness transitions
**OPTIMAL**: Cambridge 128-channel dataset (publicly available)
**PUBLICATION-READY**: Replicate ordering validation with real neural data

---

**Status**: HIGH-DENSITY DATA IDENTIFIED ✅
**Next**: Access Cambridge dataset
**Timeline**: 2-3 hours total for Phase 2
