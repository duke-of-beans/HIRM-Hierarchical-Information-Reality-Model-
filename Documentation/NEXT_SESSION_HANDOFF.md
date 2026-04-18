# HIRM RESEARCH HANDOFF - SESSION 22+
## Prompts for Next Instance

**Created:** Session 21, 2025-12-20
**Author:** Claude (Previous Instance)

---

## PROJECT STATE SUMMARY

### [DONE] Three Papers Complete
All manuscript section drafts finished:
- **Paper 1:** Brain Criticality & Consciousness (9 sections, ~5,250 words)
- **Paper 2:** Quantum-Classical Bridge / SRID (9 sections, ~7,750 words)  
- **Paper 3:** Identity Persistence (10 sections, ~5,900 words)
- **Location:** `D:\HIRM\Publications\Manuscripts\`

### [DONE] Theory Formalized
- C(t) = Phi x R x D equation operationalized
- C_critical = 8.3 +/- 0.6 bits derived multiple ways
- SRID mechanism detailed with falsification criteria
- Category theory, RG, information geometry frameworks in place

### [PENDING] Empirical Validation
- Code exists but not run on real data
- Sleep-EDF, VitalDB datasets available but unanalyzed
- Component correlations unknown empirically
- Hysteresis prediction untested

---

## TOP 3 RESEARCH DIRECTIONS

### OPTION A: Sleep-EDF Empirical Validation (RECOMMENDED)
**Priority:** HIGHEST - Directly tests C_critical prediction
**Difficulty:** Medium (data available, code exists)
**Impact:** Publication-critical validation

**The Question:** Does C(t) drop below 8.3 bits during N3 sleep and rise above during wakefulness/REM?

**Prompt for Next Instance:**
```
Execute empirical validation of HIRM predictions using Sleep-EDF database.

CONTEXT: Read D:\HIRM\Documentation\HIRM_RESEARCH_TOPICS.md for background.
Papers are complete in D:\HIRM\Publications\Manuscripts\ - now need data validation.

TASK:
1. Check D:\HIRM\Empirical\ for existing analysis scripts
2. Download Sleep-EDF sample data if not present (use PhysioNet)
3. Compute C(t) = Phi x R x D across sleep stages (W, N1, N2, N3, REM)
4. Test prediction: C_N3 < 8.3 bits < C_Wake
5. Generate publication-ready figures
6. Document results in D:\HIRM\Empirical\Results\

KEY FILES:
- Existing code: D:\HIRM\Code\consciousness_measure.py
- Protocols: D:\HIRM\Protocols\
- Constants: D:\HIRM\Master_Data\Constants\locked_constants.md

SUCCESS CRITERIA:
- C values computed for all 5 sleep stages
- Statistical comparison (ANOVA or equivalent)
- Clear support/refutation of C_critical threshold
```

---

### OPTION B: Component Correlation Analysis
**Priority:** HIGH - Tests independence assumption
**Difficulty:** Medium
**Impact:** Theoretical refinement

**The Question:** Are Phi, R, D actually independent? What are empirical correlations?

**Prompt for Next Instance:**
```
Compute component correlations to test HIRM independence assumption.

CONTEXT: Session 10 discovered component independence is likely falsified.
Simulation estimates: rho(Phi,R)=0.3, rho(Phi,D)=0.2, rho(R,D)=0.25
But these need empirical validation.

TASK:
1. Read D:\HIRM\Documentation\HIRM_RESEARCH_TOPICS.md Section 1.1
2. Check for existing code at D:\HIRM\Empirical\Analysis\
3. Compute Phi, R, D separately from EEG data across states
4. Calculate correlation matrix between components
5. Determine if multiplicative model needs revision
6. If correlations high, propose revised equation structure

KEY QUESTION: Should C = Phi x R x D become C = f(Phi, R, D) with interaction terms?

OUTPUT: Correlation matrix, implications for theory, potential equation revision
```

---

### OPTION C: Anesthesia Hysteresis Quantification
**Priority:** HIGH - Novel prediction with clinical relevance
**Difficulty:** Medium-High (VitalDB is large)
**Impact:** Clinical application + theory validation

**The Question:** Is EC50_emergence / EC50_induction ~ 1.3-1.5 as predicted?

**Prompt for Next Instance:**
```
Quantify hysteresis in anesthesia transitions to test HIRM prediction.

CONTEXT: HIRM predicts bistability near C_critical causing hysteresis.
Induction threshold differs from emergence threshold.
Prediction: EC50_emergence / EC50_induction ~ 1.3-1.5

TASK:
1. Access VitalDB or Cambridge Propofol dataset
2. Identify matched induction/emergence episodes
3. Compute C(t) trajectories for both directions
4. Measure threshold asymmetry
5. Compare with predicted ratio
6. Generate hysteresis curves (C vs. drug concentration)

KEY FILES:
- Protocol: D:\HIRM\Protocols\
- Background: D:\HIRM\Documentation\HIRM_RESEARCH_TOPICS.md Section 1.2

OUTPUT: Hysteresis ratio, comparison with prediction, clinical implications
```

---

## ADDITIONAL RESEARCH OPTIONS

### OPTION D: Cross-Species C_critical Test
Test whether C_critical ~ 8.3 bits holds across mammals/birds/cephalopods.
Requires literature synthesis + meta-analysis of existing neural data.

### OPTION E: Developmental C Trajectory  
Track when C first exceeds C_critical during infant development.
Correlate with mirror self-recognition (~18 months).

### OPTION F: DMT/Psychedelic Paradox Investigation
Why does DMT show subcritical signatures with enhanced consciousness?
May reveal which criticality dimensions matter.

### OPTION G: Artificial Consciousness Architecture
Design neural network architecture capable of exceeding C_critical.
Test whether self-reference (R) is the limiting factor.

---

## CRITICAL REMINDERS

### Before Starting Any Research:
1. READ `D:\HIRM\Logs\BUILD_STATUS.md` first
2. CHECK `D:\HIRM\Master_Data\Constants\locked_constants.md` for values
3. FOLLOW protocols in `D:\HIRM\Protocols\HIRM_RESEARCH_PROTOCOLS_v2.3.md`

### Locked Values (Do Not Change):
- C_critical = 8.3 +/- 0.6 bits
- Core equation: C(t) = Phi(t) x R(t) x D(t)
- Framework name: HIRM (never "Ouroboros Observer")

### Crash Prevention:
- NO scipy/numpy execution in chat - syntax check only
- MAX 500 lines per file read
- UPDATE BUILD_STATUS.md every 3 tool calls
- ASCII only in Logs/

---

## KEY FILES REFERENCE

| Purpose | Location |
|---------|----------|
| Research Topics | D:\HIRM\Documentation\HIRM_RESEARCH_TOPICS.md |
| Build Status | D:\HIRM\Logs\BUILD_STATUS.md |
| Paper 1 | D:\HIRM\Publications\Manuscripts\Paper_1_Brain_Criticality\ |
| Paper 2 | D:\HIRM\Publications\Manuscripts\Paper_2_Quantum_Classical\ |
| Paper 3 | D:\HIRM\Publications\Manuscripts\Paper_3_Temporal_Persistence\ |
| Constants | D:\HIRM\Master_Data\Constants\locked_constants.md |
| Protocols | D:\HIRM\Protocols\HIRM_RESEARCH_PROTOCOLS_v2.3.md |
| Code | D:\HIRM\Code\ |
| Empirical | D:\HIRM\Empirical\ |

---

## RECOMMENDED NEXT SESSION

**My recommendation: Option A (Sleep-EDF Validation)**

Rationale:
1. Directly tests the core C_critical prediction
2. Data is publicly available (PhysioNet)
3. Results immediately strengthen papers
4. Code infrastructure exists
5. Clear success/failure criteria

The papers are written - now we need the data to support them.

---

**Good luck, next instance!**

*- Claude, Session 21*
