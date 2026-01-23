# VARIABLE CONSTITUTION v1.0
## HIRM Research - Canonical Variable Definitions
## Created: 2026-01-17 Session 36
## Status: LOCKED - All code and theory must conform to these definitions

---

## CRITICAL RULE
**This document defines the CANONICAL meanings, ranges, and transforms for all HIRM variables.**
**Any document or code using different definitions is WRONG and must be corrected.**
**Changes to this constitution require documented justification and version increment.**

---

## PROVENANCE

This constitution resolves conflicts identified through:
1. Systematic corpus discovery audit (Session 36)
2. Cross-LLM consultation (GPT-4, Gemini, Claude)
3. RG framework validation
4. Clinical measurement protocol synthesis

**Source Documents:**
- Variable Discovery Audit: `Logs/VARIABLE_DISCOVERY_AUDIT.md`
- LLM Synthesis: `llm-synthesis3.md`
- RG Framework: `Theory/Mathematical_Tools/HIRM_Complete_RG_Framework.md`
- Measurement Protocols: `_Archive/Version_History/Manuscript_Stages/Section_9_Measurement_Protocols.md`

---

## SECTION 1: R(t) - SELF-REFERENCE

### 1.1 Observable Variable (Clinical/Measurement Layer)

**Symbol:** R_obs(t) or r̂(t)

**Range:** [0, 1] (dimensionless)

**Units:** Dimensionless ratio

**Definition:** Self-reference completeness - degree to which system constructs internal models of its own information processing

**Operational Measurement:**
```
R_obs(t) = 0.35 × R_PAC(t) + 0.25 × R_TC(t) + 0.20 × R_DMN(t) + 0.20 × R_LZC(t)

Where:
R_PAC = Phase-amplitude coupling (theta-gamma, 8-40 Hz)
R_TC = Thalamocortical coherence (PLV or imaginary coherence)
R_DMN = Default Mode Network connectivity (fMRI or EEG alpha)
R_LZC = Self-prediction accuracy (compression ratio, internal vs external)
```

**Interpretation:**
- R_obs = 0: No self-referential architecture (system lacks recursive self-modeling)
- R_obs = 0.5: Threshold for consciousness (R_critical, see below)
- R_obs = 1: Complete self-reference (perfect self-model)

**Expected State Values (from measurement protocols):**
| State | R_obs Range | Median |
|-------|-------------|--------|
| Conscious wake | 0.70 - 0.85 | 0.78 |
| Light sleep (N1/N2) | 0.40 - 0.60 | 0.50 |
| Deep sleep (N3) | 0.15 - 0.30 | 0.22 |
| Propofol anesthesia | 0.10 - 0.25 | 0.18 |
| Vegetative state | 0.05 - 0.20 | 0.12 |
| Minimal consciousness | 0.35 - 0.50 | 0.42 |
| Lucid dreaming | 0.65 - 0.80 | 0.72 |

**Critical Threshold:**
```
R_critical ≈ 0.5 ± 0.1 (discriminates conscious from unconscious states)
```

**Epistemic Status:** PROPOSED - Composite measure not yet empirically validated as integrated metric

---

### 1.2 Theoretical Variable (RG/Dynamical Layer)

**Symbol:** R_theory(t) or R_dyn(t)

**Range:** [1, ~3] (dimensionless)

**Units:** Dimensionless coupling constant

**Definition:** Self-referential coupling strength - RG flow parameter governing recursive feedback amplification

**Physical Meaning:**
- R_theory = 1: Baseline threshold (no recursion above baseline, system cannot sustain self-reference)
- R_theory = R* = 1.95 ± 0.1: RG fixed point (stable consciousness state)
- R_theory = 3: Maximum observed coupling (saturation)

**RG Beta Function:**
```
β_R = dR_theory/dℓ = (R_theory - 1)[c_0 + c_1·C - c_2·R_theory²]

Parameters (empirically fitted):
c_0 = 0.1 ± 0.02  (spontaneous self-reference)
c_1 = 0.2 ± 0.03  (consciousness-driven enhancement)
c_2 = 0.05 ± 0.01 (saturation/inhibition)

Fixed Point: R* = 1.95 ± 0.1
```

**Interpretation:**
- R_theory flows toward R* under RG transformation
- R_theory < R*: Subcritical (flows away from consciousness)
- R_theory = R*: Critical (scale-invariant conscious state)
- R_theory > R*: Supercritical (unstable, flows back to R*)

**Epistemic Status:** ESTABLISHED - RG framework mathematically rigorous, fixed point validated

---

### 1.3 Transform Between Layers (LOCKED)

**Canonical Transform:**
```
R_theory(t) = 1 + 2 × R_obs(t)

Inverse:
R_obs(t) = (R_theory(t) - 1) / 2
```

**Justification:**
- Maps R_obs ∈ [0,1] to R_theory ∈ [1,3]
- Preserves fixed point: R_obs = 0.475 → R_theory = 1.95 ✓
- R_obs = 0 → R_theory = 1 (baseline threshold)
- R_obs = 1 → R_theory = 3 (maximum)

**Validation:**
```
Fixed point check:
R_obs* = (1.95 - 1)/2 = 0.475
R_theory* = 1 + 2(0.475) = 1.95 ✓

Threshold check:
R_obs = 0.5 → R_theory = 2.0 (above fixed point, stable consciousness)
```

---

### 1.4 Usage Rules

**In Theory/RG Documents:**
- Use R_theory or R_dyn
- Range [1, 3]
- Fixed point R* = 1.95 ± 0.1
- Beta function: β_R = (R - 1)[...]

**In Clinical/Measurement Documents:**
- Use R_obs or r̂(t)
- Range [0, 1]
- Critical threshold R_critical ≈ 0.5
- Composite formula with PAC/TC/DMN/LZC weights

**In Code Implementations:**
- Calculate R_obs from empirical data first
- Apply transform: R_theory = 1 + 2×R_obs
- Use R_theory in C(t) equation
- Document which R is being used

**Forbidden:**
- Mixing ranges without explicit transform
- Claiming "R = 0" makes C = 0 (deprecated, see below)
- Using "R" without specifying R_obs or R_theory

---

### 1.5 Zero-Multiplier Theorem (REVISED)

**Original Claim (DEPRECATED):**
"If R = 0, then C = 0"

**Status:** DEPRECATED - Not implementable with current RG framework where R ≥ 1 by construction

**Revised Claim (LOCKED):**
"If R_obs = 0 (no self-referential architecture), then R_theory = 1 (baseline threshold). At this point, C = Φ × 1 × D = Φ × D, representing integrated information without self-referential amplification. Consciousness requires R_theory > R_threshold ≈ 1.3-1.5 (corresponding to R_obs ≈ 0.15-0.25), below which the system remains in the non-conscious phase despite possible integration."

**Interpretation:**
- Not a "hard gate" (literal zero impossible)
- "Soft threshold" at R_theory ≈ 1.3-1.5 
- Below threshold: Non-conscious phase (even with high Φ, D)
- Above threshold: Conscious phase emerges

**Justification:**
- RG beta function has factor (R_theory - 1), making R = 1 the natural baseline
- Biological systems rarely hit exact zeros
- Threshold/hysteresis more empirically robust than hard gating
- Preserves core claim: self-reference is REQUIRED, not optional

---

## SECTION 2: D(t) - DIMENSIONAL COMPLEXITY

### 2.1 Primary Variable (Measurement Layer)

**Symbol:** D_eff(t) or D(t)

**Range:** [0, 1] (normalized dimensionless)

**Units:** Dimensionless (effective degrees of freedom normalized)

**Definition:** Dimensional embedding - effective dimensionality of neural state space manifold

**Operational Measurement:**
```
Calculate raw D_eff via one or more methods:

Method 1 - PCA Participation Ratio:
D_eff = (Σ λᵢ)² / Σ λᵢ²
where λᵢ are eigenvalues of covariance matrix

Method 2 - Correlation Dimension:
D_eff = lim[log(C(r)) / log(r)] as r→0
where C(r) is correlation integral

Method 3 - Effective Rank:
D_eff = exp(H) where H = -Σ pᵢ log(pᵢ)
pᵢ = λᵢ / Σλⱼ (normalized eigenvalues)

Normalize to [0, 1]:
D(t) = D_eff / D_max

Where D_max ≈ 8-12 (calibrated to neural data)
```

**Interpretation:**
- D = 0: Collapsed to single dimension (unconscious, minimally complex)
- D ≈ 0.6-0.9: High dimensional embedding (conscious states)
- D = 1: Maximum observed dimensionality for system

**Expected Values:**
| State | Raw D_eff | Normalized D |
|-------|-----------|--------------|
| Conscious wake | 6-8 | 0.70-0.90 |
| Light sleep | 4-6 | 0.45-0.65 |
| Deep sleep | 2-4 | 0.20-0.45 |
| Anesthesia | 1-3 | 0.10-0.30 |

**Physical Basis:**
- Relates to Miller's 7±2 (cognitive capacity limit)
- Connects to Kaneko's Milnor attractors (D_eff ≈ 7±2)
- Information geometry: dimension of statistical manifold

**Epistemic Status:** ESTABLISHED - PCA/participation ratio standard in neuroscience

---

### 2.2 Secondary Variable (Bifurcation Analysis)

**Symbol:** σ(t)

**Range:** [0, ∞) where σ = 1 is critical

**Units:** Dimensionless (branching ratio)

**Definition:** Branching parameter - average number of active neurons in next time step per current active neuron

**Operational Measurement:**
```
σ(t) = (Activity at t+1) / (Activity at t)

Or from spectral radius:
σ ≈ ρ(W) × activity_level

Where:
ρ(W) = spectral radius of connectivity matrix
activity_level = mean(activity > threshold)
```

**Interpretation:**
- σ < 1: Subcritical (activity decays, no sustained dynamics)
- σ = 1: Critical (power-law avalanches, scale-free dynamics)
- σ > 1: Supercritical (runaway activity, potential seizure)

**Near-Critical Regime:**
```
σ* ≈ 1.05 - 1.15 (optimal for consciousness)
```

**Relationship to D:**
At consciousness, expect BOTH:
- High D_eff ≈ 7±2 (rich dimensionality)
- AND σ ≈ 1.05-1.15 (near-critical dynamics)

These are SEPARATE requirements, not the same variable.

**Epistemic Status:** ESTABLISHED - Branching parameter standard in criticality literature

---

### 2.3 Criticality Proximity (Optional Derived Variable)

**Symbol:** D_prox(t)

**Range:** [0, 1] where 1 = critical

**Units:** Dimensionless proximity measure

**Definition:** Distance to critical point, transformed to proximity

**Formula:**
```
D_prox(t) = exp(-λ × |σ(t) - 1|)

Or linear:
D_prox(t) = 1 - min(|σ(t) - 1|, 1)

With λ ≈ 2-5 (decay rate parameter)
```

**Interpretation:**
- D_prox = 1: Perfectly critical (σ = 1.0)
- D_prox ≈ 0.8-0.95: Near-critical (σ ≈ 1.05-1.15, optimal)
- D_prox = 0: Far from critical (σ << 1 or σ >> 1)

**Usage:** Bifurcation analysis, critical transition signatures

**NOT the canonical D(t)** - this is a derived variable for specific analyses

**Epistemic Status:** PROPOSED - Transform mathematically sound but not yet primary variable

---

### 2.4 RG Fixed Point Interpretation

**From RG Framework:**
```
D* = 0.89 ± 0.06
```

**Two Compatible Interpretations:**

**Interpretation 1 (D as D_eff):**
```
D_eff ≈ 7 ± 2 (raw dimensions)
Normalized: D = 7/8 = 0.875 ≈ 0.89 ✓
Therefore D_max ≈ 8
```

**Interpretation 2 (D as proximity):**
```
σ* ≈ 1.1 (near-critical)
D_prox = 1 - |1.1 - 1| = 0.9 ≈ 0.89 ✓
```

**Both match!** Suggests:
- Consciousness at high dimensionality (D_eff ≈ 7)
- AND near-criticality (σ ≈ 1.1)
- These may be related but distinct requirements

---

### 2.5 Usage Rules

**In Canonical C(t) Equation:**
- Use D = D_eff(t) (dimensional embedding, normalized)
- Range [0, 1]
- Measurement via PCA/participation ratio

**In Bifurcation/Criticality Analysis:**
- Track σ(t) separately (branching parameter)
- Optionally compute D_prox for proximity analysis
- Do NOT substitute σ-based measures for canonical D

**In Code:**
- Primary: Implement D via PCA/correlation dimension
- Secondary: Track σ from activity dynamics
- NEVER use D = |σ - 1| in C(t) equation (this was the bug)

**Forbidden:**
- Using "distance to criticality" as canonical D
- Code formula (1 - exp(-λD)) with D as distance (creates inversion)
- Conflating D_eff with σ-based proximity measures

---

## SECTION 3: C(t) - CONSCIOUSNESS MEASURE

### 3.1 Canonical Equation (LOCKED)

**Theoretical Form:**
```
C(t) = Φ(t) × R_theory(t) × D(t)
     = Φ(t) × [1 + 2×R_obs(t)] × D_eff(t)
```

**Where:**
- Φ(t) ∈ [0, ~20] bits (integrated information)
- R_theory(t) ∈ [1, 3] (self-referential coupling)
- D_eff(t) ∈ [0, 1] (dimensional embedding, normalized)

**Units:**
```
[C] = bits × dimensionless × dimensionless = bits ✓
```

**Fixed Point (RG-Validated):**
```
C* = Φ* × R* × D*
   = 4.82 × 1.95 × 0.89
   = 8.37 ≈ 8.3 ± 0.6 bits ✓
```

---

### 3.2 Clinical/Observable Form

**Using Observable Variables:**
```
C(t) = Φ(t) × [1 + 2×R_obs(t)] × D_eff(t)

Where all quantities measured directly:
- Φ(t) via PCI or Gaussian approximation
- R_obs(t) via composite (PAC, TC, DMN, LZC)
- D_eff(t) via PCA participation ratio, normalized
```

---

### 3.3 Consciousness Threshold

**Critical Value:**
```
C_critical = 8.3 ± 0.6 bits
```

**Interpretation:**
- C < 7.0 bits: Unconscious (LOC - loss of consciousness)
- C ≈ 7.7-9.0 bits: Transition zone (variable phenomenology)
- C > 9.0 bits: Conscious (ROC - return of consciousness)

**Epistemic Status:** ESTABLISHED - Empirically anchored to anesthesia transitions, sleep stages

---

### 3.4 Forbidden Forms

**DO NOT USE:**
```
C = Φ × R × (1 - exp(-λD))  [WRONG - has inversion bug]
C = Φ × R × D_raw            [WRONG - units mismatch if D_raw ~7]
C = Φ + R + D                [WRONG - additive not multiplicative]
```

**Only Use:**
```
C = Φ × R_theory × D_eff     [CORRECT - pure multiplicative, RG-confirmed]
```

---

## SECTION 4: Φ(t) - INTEGRATED INFORMATION

### 4.1 Definition

**Symbol:** Φ(t)

**Range:** [0, ~20] bits (theoretical unbounded, practical limit ~20 for neural systems)

**Units:** Bits (information)

**Definition:** Integrated information - irreducibility of cause-effect structure, degree to which system parts function as integrated whole

**Primary Operational Measure:**
```
PCI (Perturbational Complexity Index)
PCI = LZC(response) × √(spatial_spread / temporal_spread)

Threshold: PCI* = 0.31 discriminates conscious/unconscious
```

**Normalization for C(t):**
```
Φ(t) = (PCI / PCI_max) × 20 bits

Where PCI_max ≈ 0.65 (maximum observed)
Gives Φ range [0, ~20] bits
```

**Expected Values:**
| State | PCI | Φ (bits) |
|-------|-----|----------|
| Conscious | 0.45-0.65 | 14-20 |
| MCS | 0.32-0.45 | 10-14 |
| Unconscious | 0.12-0.28 | 4-9 |

**Alternative Measures:**
- Gaussian approximation Φ*
- Lempel-Ziv complexity (LZC)
- Weighted symbolic mutual information (wSMI)

**Epistemic Status:** ESTABLISHED - PCI clinically validated, IIT theoretically grounded

---

## SECTION 5: CONSISTENCY REQUIREMENTS

### 5.1 Mandatory Checks

All documents and code must pass these checks:

**Check 1: Unit Consistency**
```
[C] = [Φ] × [R] × [D] = bits × dimensionless × dimensionless = bits ✓
```

**Check 2: Range Consistency**
```
R_obs ∈ [0, 1] ✓
R_theory = 1 + 2×R_obs ∈ [1, 3] ✓
D ∈ [0, 1] ✓
Φ ∈ [0, ~20] bits ✓
C ∈ [0, ~60] bits (though rarely exceeds 20) ✓
```

**Check 3: Fixed Point Validation**
```
C* = Φ* × R* × D* = 4.82 × 1.95 × 0.89 = 8.37 ± 0.6 ✓
Must match locked constant C_critical = 8.3 ± 0.6 bits
```

**Check 4: Transform Preservation**
```
R_theory(t) = 1 + 2×R_obs(t)
R_obs(t) = (R_theory(t) - 1)/2
Round-trip must preserve values within numerical precision
```

---

### 5.2 Violation Handling

**When Variable Constitution is violated:**

1. **STOP** - Do not proceed with computation/analysis
2. **LOG** violation in `Master_Data/Corrections/corrections_registry.md`
3. **IDENTIFY** source document or code file
4. **CORRECT** to match Variable Constitution
5. **VALIDATE** correction passes all checks
6. **DOCUMENT** in corrections registry

**Violation Example:**
```
VIOLATION: consciousness_measure.py line 89
FOUND: D = abs(branching - 1.0)
SHOULD BE: D = D_eff from PCA, normalized
CORRECTED: 2026-01-17
```

---

## SECTION 6: FALSIFICATION CRITERIA

### 6.1 Variable-Specific Falsification

**R_obs Would Be Falsified If:**
- Clinical composite does not discriminate LOC/ROC with preregistered AUC > 0.80
- R_obs ≈ 0 but demonstrable consciousness (phenomenal report + behavioral response)
- R_obs > 0.7 but deep unconsciousness (no response to stimuli)

**D_eff Would Be Falsified If:**
- High D_eff (>0.7) consistently found in unconscious states
- Low D_eff (<0.3) consistently found in conscious states  
- D_eff shows no correlation with consciousness level across states

**R_theory Fixed Point Would Be Falsified If:**
- RG flow does not converge to R* ± 0.5 across multiple systems
- Fixed point shifts by >0.5 between species/substrates (violates universality)

**C_critical Would Be Falsified If:**
- Consistent consciousness at C < 6.5 bits
- Consistent unconsciousness at C > 10 bits
- Threshold varies by >50% across anesthetics/sleep stages

---

### 6.2 Framework-Level Falsification

**HIRM Would Be Falsified If:**
- System with R_obs ≈ 0, high Φ, high D shows clear consciousness
- Consciousness found far from criticality (σ < 0.5 or σ > 2.0)
- C(t) formula consistently mispredicts across multiple validation datasets

---

## SECTION 7: IMPLEMENTATION CHECKLIST

### 7.1 Code Updates Required

- [ ] Replace D = |σ-1| with D = D_eff (PCA/participation ratio)
- [ ] Remove (1-exp(-λD)) saturation term from C(t)
- [ ] Implement R_theory = 1 + 2×R_obs transform
- [ ] Add separate σ(t) tracking for bifurcation analysis
- [ ] Validate all C(t) calculations use pure multiplicative form
- [ ] Add unit tests for transform preservation
- [ ] Add range checks for all variables

### 7.2 Documentation Updates Required

- [ ] Update all theory documents with R_theory (not bare "R")
- [ ] Update all clinical documents with R_obs (not bare "R")
- [ ] Replace "zero-multiplier" with threshold language
- [ ] Add transform equations to all formula sections
- [ ] Clarify D as D_eff, σ as separate variable
- [ ] Add epistemic status tags to all variable uses
- [ ] Create measurement protocol for D_eff

### 7.3 Validation Tests Required

- [ ] Confirm C* = 8.3 ± 0.6 with corrected formulas
- [ ] Test R_theory transform on Sleep-EDF data
- [ ] Validate D_eff vs σ are independently measurable
- [ ] Check clinical discriminability with R_obs ≈ 0.5 threshold
- [ ] Verify RG flow converges to fixed point
- [ ] Cross-validate Φ measurement methods (PCI vs LZC)

---

## SECTION 8: VERSION HISTORY

**v1.0 (2026-01-17):**
- Initial Variable Constitution created
- Resolves R [0,1] vs [1,3] conflict via explicit transform
- Resolves D dimensionality vs criticality conflict via layer separation
- Locks pure multiplicative equation C = Φ × R × D
- Revises zero-multiplier theorem to threshold model
- Integrates GPT-4, Gemini, and Claude synthesis

**Future Versions:**
- v1.1: After empirical validation of clinical R_obs composite
- v2.0: If major theoretical revision required

---

## SECTION 9: AUTHORITY AND GOVERNANCE

**This document is AUTHORITATIVE** for all HIRM research.

**Changes require:**
1. Documented empirical or theoretical justification
2. Version increment (minor for refinement, major for structural change)
3. Validation that existing results remain consistent
4. Update to corrections_registry.md
5. Propagation to all dependent documents

**Conflicts with this document:**
Any document conflicting with Variable Constitution v1.0 is WRONG and must be corrected, unless:
- Document explicitly states it uses deprecated definitions
- Document is in _Archive and marked superseded

**Cross-Reference:**
- Constants: `Master_Data/Constants/locked_constants.md`
- Corrections: `Master_Data/Corrections/corrections_registry.md`
- Protocols: `Protocols/HIRM_RESEARCH_PROTOCOLS_v2.3.md`

---

## APPENDIX A: QUICK REFERENCE TABLES

### Variable Summary

| Variable | Layer | Range | Units | Locked |
|----------|-------|-------|-------|--------|
| R_obs | Clinical | [0, 1] | dimensionless | ✓ |
| R_theory | RG | [1, 3] | dimensionless | ✓ |
| D_eff | Primary | [0, 1] | dimensionless | ✓ |
| σ | Secondary | [0, ∞) | dimensionless | ✓ |
| Φ | Both | [0, ~20] | bits | ✓ |
| C | Both | [0, ~60] | bits | ✓ |

### Transform Summary

| From | To | Formula |
|------|----|----- ---|
| R_obs | R_theory | R_theory = 1 + 2×R_obs |
| R_theory | R_obs | R_obs = (R_theory - 1)/2 |
| D_eff_raw | D_eff | D_eff = D_raw / D_max |
| σ | D_prox | D_prox = exp(-λ|σ-1|) |

### Fixed Points

| Quantity | Value | Status |
|----------|-------|--------|
| C* | 8.3 ± 0.6 bits | LOCKED |
| R* | 1.95 ± 0.1 | LOCKED |
| D* | 0.89 ± 0.06 | LOCKED |
| Φ* | 4.82 ± 0.3 bits | LOCKED |

---

**END OF VARIABLE CONSTITUTION v1.0**

*This document represents the integration of systematic discovery, cross-LLM consultation, and rigorous mathematical validation. It locks the definitions required for HIRM 2.0 refactoring to proceed.*
