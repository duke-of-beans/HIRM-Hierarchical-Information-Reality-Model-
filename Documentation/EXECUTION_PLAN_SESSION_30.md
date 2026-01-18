# HIRM EXECUTION PLAN - SESSION 30+
## Focus: Empirical Validation, Paper Completion, Publication
## Created: 2025-12-20
## Status: ACTIVE

---

## EXECUTIVE SUMMARY

Four parallel tracks:
1. **Computational Debugging** - Fix R(t)/Phi(t) returning zero
2. **Paper 3 Completion** - Integrate expanded sections (+~1,700 words)
3. **Empirical Validation** - Run Sleep-EDF analysis
4. **Publication Execution** - Prepare Paper 1 for submission

---

## TRACK 1: COMPUTATIONAL DEBUGGING

### Problem Diagnosis

**Files Involved:**
- D:\HIRM\Code\Core\consciousness_measure.py
- D:\HIRM\Code\Core\self_reference.py
- D:\HIRM\Empirical\Analysis\component_correlations.py

**Known Issues:**
1. `_calculate_phi_geometric()` returns 0 when:
   - Binary activity has p=0 or p=1 (entropy = 0)
   - Mutual information calculation fails
   - Correlation matrix has NaN values

2. `calculate_R()` returns 1.0 (default) when:
   - History has < 10 timesteps
   - Autocorrelation is zero (constant signal)
   - GFP (global field power) has no variation

3. `_calculate_D()` returns 0 when:
   - Branching parameter = 1.0 exactly
   - Spectral radius calculation fails

### Fix Strategy

**Step 1:** Add diagnostic logging
```python
# Add to each calculation method
print(f"DEBUG Phi: activity shape={activity.shape}, threshold={threshold}")
print(f"DEBUG Phi: p_active={p_active}, H_system={H_system}")
```

**Step 2:** Handle edge cases
```python
# In _calculate_phi_geometric
if p_active < 0.01 or p_active > 0.99:
    # Use alternative entropy calculation
    ...
```

**Step 3:** Validate with synthetic data
- Generate known-good test cases
- Verify expected outputs
- Compare with debug_phi.py results

### Testing Protocol (NO scipy execution - syntax only)

```bash
# Syntax check only
python -m py_compile D:\HIRM\Code\Core\consciousness_measure.py
python -m py_compile D:\HIRM\Empirical\Analysis\component_correlations.py
```

---

## TRACK 2: PAPER 3 COMPLETION

### Current State
- Consolidated draft: ~4,400 words (PAPER_3_CONSOLIDATED_v3.md)
- Target: 10,000 words
- Gap: ~5,600 words (but expanded sections exist)

### Expanded Sections Available
| Section | File | Words | Status |
|---------|------|-------|--------|
| Section 2 | Section_2_EXPANDED_v2.md | ~700 | READY |
| Section 4 | Section_4_EXPANDED_v2.md | ~500 | CHECK |
| Section 8 | Section_8_EXPANDED_v2.md | ~500 | CHECK |
| Section 9 | Section_9_EXPANDED_v2.md | ~500 | CHECK |
| Section 10 | Section_10_EXPANDED_v2.md | ~400 | CHECK |

### Integration Plan

**Phase 1: Merge Expanded Sections**
1. Review each _EXPANDED_v2.md file
2. Replace condensed versions in CONSOLIDATED
3. Verify coherence and flow
4. Update word count

**Phase 2: Add Missing Content (~1,700 words)**
- Section 3 (Mechanisms): +500 words on biological implementation
- Section 6 (Empirical): +500 words on clinical case studies
- Section 7 (Clinical): +500 words on treatment implications
- Introduction/Conclusion: +200 words for framing

**Phase 3: Final Polish**
- Check terminology against locked_constants.md
- Verify all citations
- Add figure references
- Format for journal submission

---

## TRACK 3: EMPIRICAL VALIDATION

### Sleep-EDF Analysis

**Files:**
- Code: D:\HIRM\Empirical\Analysis\component_correlations.py
- Data: Sleep-EDF database (197 subjects) - TO DOWNLOAD

**Predictions to Test:**
- P1: C(t) < 8.3 bits during N3 deep sleep
- P2: C(t) fluctuates above/below threshold in REM
- P3: Component correlations match estimates (rho ~ 0.2-0.3)

**Execution Steps:**
1. Download Sleep-EDF from PhysioNet
2. Extract EEG channels (Fpz-Cz, Pz-Oz)
3. Segment into 30-second epochs
4. Apply staging annotations
5. Calculate Phi, R, D for each epoch
6. Compute correlations and statistics

### Anesthesia Hysteresis (VitalDB)

**Prediction:** EC50_emergence / EC50_induction = 1.3-1.5

**Files:**
- Code: D:\HIRM\Empirical\Analysis\anesthesia_hysteresis.py
- Data: VitalDB (5,566 cases)

---

## TRACK 4: PUBLICATION EXECUTION

### Paper 1 Status: READY FOR SUBMISSION

**File:** D:\HIRM\Publications\Manuscripts\Paper_1_Brain_Criticality\Paper_1_UNIFIED_DRAFT.md
**Word Count:** ~16,100 words
**Sections:** 9/9 complete

### Target Journals (Ranked)
1. **Nature Neuroscience** - Highest impact, longest review
2. **PNAS** - Broad audience, faster review
3. **PLoS Computational Biology** - Open access, fair review
4. **Neuroscience of Consciousness** - Specialized, appropriate scope

### Submission Checklist

[ ] Final manuscript review
[ ] Abstract polish (250 words max)
[ ] Figure preparation (high-resolution)
[ ] Supplementary materials compilation
[ ] Author information
[ ] Cover letter draft
[ ] Suggested reviewers list
[ ] Competing interests statement
[ ] Data availability statement
[ ] Code availability statement

### Cover Letter Key Points
1. Novel theoretical synthesis (12+ mathematical frameworks)
2. Quantitative predictions (30+ falsifiable)
3. Clinical relevance (DOC, anesthesia)
4. Convergent validation (6 independent paths to C_critical)

---

## PRIORITY SEQUENCE

### This Session (30)
1. [HIGH] Fix computational bugs (syntax check only)
2. [HIGH] Integrate Paper 3 expanded sections
3. [MEDIUM] Create Paper 1 submission package outline

### Next Session (31)
1. [HIGH] Complete Paper 3 final draft
2. [MEDIUM] Prepare figures for Paper 1
3. [LOW] Plan empirical validation execution

### Future Sessions
1. Run Sleep-EDF analysis
2. Submit Paper 1
3. Run VitalDB analysis
4. Finalize Paper 2

---

## SUCCESS METRICS

| Deliverable | Target | Current | Status |
|-------------|--------|---------|--------|
| Paper 1 | 16-18k words | ~16,100 | [DONE] |
| Paper 2 | ~12k words | ~10,850 | [90%] |
| Paper 3 | ~10k words | ~8,300 | [83%] |
| Computational | Working | BUGGY | [FIX] |
| Sleep-EDF | Validated | - | [TODO] |
| VitalDB | Validated | - | [TODO] |
| Submission | Paper 1 sent | - | [TODO] |

---

**Document:** EXECUTION_PLAN_SESSION_30.md
**Location:** D:\HIRM\Documentation\
**Status:** ACTIVE
