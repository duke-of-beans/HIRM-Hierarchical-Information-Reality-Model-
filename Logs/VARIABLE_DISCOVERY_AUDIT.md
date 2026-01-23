# Variable Discovery Audit: R(t) and D(t) - COMPLETE
## Session 36 | 2026-01-17 | Discovery-Driven Analysis

---

## CROSS-LLM CONSULTATION RECOMMENDED

**Status:** Phase 1 discovery COMPLETE - All three R(t) definitions extracted  
**Recommendation:** Request GPT-4/Gemini synthesis before Variable Constitution decisions  
**See:** `Protocols/CROSS_LLM_SYNTHESIS_PROTOCOL.md` for request format

---

## Executive Summary

**Critical Finding:** R(t) has THREE distinct operational definitions across the HIRM corpus, each with different ranges and interpretations. D(t) has TWO distinct definitions that are conceptually incompatible. This is the root cause of definitional drift identified in LLM synthesis.

**ALL THREE R DEFINITIONS NOW EXTRACTED:**
1. Clinical composite [0, 1] - self-reference completeness
2. Autocorrelation gain [1, 3] - recursion amplification  
3. **RG fixed point [R* = 1.95 ± 0.1] - self-reference as coupling constant**

---

## R(t) - Self-Reference Completeness

### Definition 1: Clinical Composite [0, 1] - FROM THEORY

**Source:** `Section_9_Measurement_Protocols.md`, `Stage3A_Handoff_Document.md`

**Formula:**
```
R(t) = 0.35·R_PAC + 0.25·R_TC + 0.20·R_DMN + 0.20·R_LZC_ratio

Where:
R_PAC = Phase-amplitude coupling (cross-frequency)
R_TC = Thalamocortical coherence (feedback strength)  
R_DMN = Default Mode Network connectivity
R_LZC_ratio = Self-prediction accuracy (compression ratio)
```

**Range:** [0, 1] - Normalized completeness ratio

**Units:** Dimensionless

**Expected Values (from documentation):**
- Conscious wake: 0.70-0.85
- Light sleep (N1/N2): 0.40-0.60
- Deep sleep (N3): 0.15-0.30
- Anesthesia (propofol): 0.10-0.25
- Vegetative state: 0.05-0.20
- Minimal consciousness: 0.35-0.50
- Lucid dreaming: 0.65-0.80

**Interpretation:** True self-reference completeness as a ratio—how complete is the system's self-model? Zero means no self-reference, one means perfect self-reference.

**Epistemic Status:** Proposed protocol, not yet empirically validated as a composite

**Theoretical Role:** GATING variable - if R=0, consciousness impossible (zero-multiplier theorem)

---

### Definition 2: Autocorrelation Gain [1, ~3] - FROM CODE

**Source:** `consciousness_measure.py` (line 273-326)

**Formula:**
```python
def calculate_R(self, activity_history: np.ndarray) -> float:
    # Calculate autocorrelation at multiple time scales
    autocorr = [...]  # Mean autocorrelation across neurons
    
    # R related to decay rate of autocorrelation
    decay_rate = -np.polyfit(range(len(autocorr)), 
                             np.log(np.abs(autocorr) + 1e-10), 1)[0]
    
    R = 1.0 + np.exp(-decay_rate)  # Maps decay to R ∈ [1, ~3]
    
    return min(R, 3.0)  # Cap at reasonable maximum
```

**Range:** [1.0, 3.0] - Recursion amplification factor

**Units:** Dimensionless gain

**Interpretation:** Measures how much temporal autocorrelation amplifies system behavior. R=1 is baseline (no recursion), R=3 is maximum observed recursive depth. This is NOT a completeness ratio but a GAIN parameter.

**Default behavior:** If insufficient history, returns 1.0 (neutral gain)

**Physical meaning:** Slower autocorrelation decay → longer memory → deeper recursion → higher R

**Theoretical Role:** AMPLIFICATION factor - scales the integration×dimension product

---

### Definition 3: RG Fixed Point [R* = 1.95 ± 0.1] - FROM RG FRAMEWORK

**Source:** `HIRM_Complete_RG_Framework.md`, `Renormalization_Group_Framework.md`, `HIRM_RG_Quick_Reference.md`

**Fixed Point Value:**
```
R* = 1.95 ± 0.1 (self-reference completeness)
```

**Beta Function (RG Flow Equation):**
```
β_R = (R - 1)[c_0 + c_1 C - c_2 R²]

Parameters:
c_0 = 0.1 ± 0.02  (spontaneous self-reference)
c_1 = 0.2 ± 0.03  (consciousness-driven enhancement)
c_2 = 0.05 ± 0.01 (saturation/inhibition)
```

**Range:** Implicitly [1, ~3] based on:
- Fixed point at R* = 1.95
- Flow equation has form (R - 1)[...] suggesting R=1 is boundary
- Saturation term -c_2 R² prevents unbounded growth
- Code caps at 3.0

**Interpretation:** R is a **coupling constant** in RG flow, representing strength of self-referential feedback loops. At R < 1, system cannot sustain self-reference. At R = R*, system reaches scale-invariant critical state.

**Physical Meaning:**
- R=1: Threshold for self-reference onset
- R < R*: Sub-critical self-reference (flows away from consciousness)
- R = R*: Critical self-reference (consciousness emerges)
- R > R*: Super-critical (unstable, flows back to R*)

**Theoretical Role:** COUPLING CONSTANT in RG formalism - determines flow toward/away from consciousness fixed point

**Key RG Insight (from document):**
> **Hierarchy of Transitions:**
> 1. Quantum → Decoherent (PIS formation)
> 2. Decoherent → Integrated (Φ > Φ_crit)
> 3. **Integrated → Self-referential (R → 1): Recursive self-modeling**
> 4. Self-referential → Conscious (C = C_crit): Fixed point attainment

This suggests R=1 is the *threshold* for self-reference to begin, and R* = 1.95 is the *stable fixed point* where consciousness emerges.

---

### The R(t) Conflict Matrix - UPDATED

| Property | Clinical [0,1] | Code [1,3] | **RG Formalism [1, ~2]** |
|----------|----------------|------------|--------------------------|
| **Range** | [0, 1] | [1.0, 3.0] | **[1, ~3] (R*=1.95)** |
| **Zero means** | No self-ref | N/A (min=1) | **N/A (min=1)** |
| **One means** | Perfect self-ref | Baseline | **Threshold for self-ref** |
| **Units** | Ratio | Gain | **Coupling constant** |
| **Interpretation** | Completeness | Amplification | **RG flow parameter** |
| **Neutral value** | 0.5 (partial) | 1.0 (baseline) | **1.0 (threshold)** |
| **Fixed point** | N/A | N/A | **R* = 1.95** |
| **Physical basis** | 4 neural proxies | Autocorr decay | **Scale invariance** |
| **Consciousness requires** | R ~ 0.7-0.9 | R ~ 1.5-2.5? | **R = 1.95 (exactly)** |

**CRITICAL INCOMPATIBILITY IDENTIFIED:**

The RG framework and code implementation AGREE that R ≥ 1, but CONFLICT with clinical theory's [0,1] range:

1. **Clinical theory** requires R=0 to be possible (zero-multiplier theorem: "if R=0, C=0")
2. **RG formalism** has R=1 as THRESHOLD (β_R flow equation has factor (R-1))
3. **Code** returns minimum R=1.0 (cannot reach zero)

**This is NOT just a normalization difference - it's a fundamental conceptual split:**
- Clinical: R as completeness ratio (can be zero)
- RG/Code: R as gain/coupling above baseline (cannot be zero)

---

### Cross-Framework Consistency Check

**Question:** Does C* = Φ* × R* × D* hold in RG framework?

**From RG docs:**
```
C* = 8.28 ± 0.58 bits
Φ* = 4.82 ± 0.31 bits
R* = 1.95 ± 0.12
D* = 0.89 ± 0.06

Consistency Check: C* = Φ* × R* × D* = 4.82 × 1.95 × 0.89 = 8.37 ✓
```

**This CONFIRMS:**
- RG framework uses R* = 1.95 in the multiplicative equation
- Units work: bits × dimensionless × dimensionless = bits
- Formula is C = Φ × R × D (pure multiplicative, no saturation)

**But creates NEW CONFLICT:**
- If R ∈ [1, 3] instead of [0, 1], then R acts as AMPLIFIER not GATE
- When R=1, C = Φ × 1 × D = Φ × D (consciousness NOT zero, just not amplified)
- Zero-multiplier theorem BROKEN: Cannot make C=0 by setting R=0 (R can't be zero!)

---

## D(t) - Dimensional Complexity

### Definition 1: Intrinsic Manifold Dimension - FROM SOME THEORY DOCS

**Source:** Various mathematical framework documents (needs more systematic extraction)

**Formula:**
```
D(t) = D_intrinsic ≈ 7 ± 2

Where D_intrinsic is calculated via:
- PCA (effective degrees of freedom)
- Participation ratio
- Correlation dimension
```

**Range:** Typically ~5-9 for neural systems (raw dimensionality)

**Units:** Dimensions (integer or continuous)

**Interpretation:** How many independent degrees of freedom does the system have? Related to Miller's 7±2, Kaneko's Milnor attractors, etc.

**Normalization issue:** If D is raw dimension (~7), then C = Φ × R × D has units [bits × dimensionless × dimensions] = "bit-dimensions" (not pure bits)

**RG Framework says:** D* = 0.89 ± 0.06 (dimensionless, NOT ~7!)

This means RG framework is using Definition 2 (below), not raw dimension.

---

### Definition 2: Distance to Criticality - FROM CODE AND RG

**Source:** `consciousness_measure.py` (line 328-370), RG beta function for D

**Code Formula:**
```python
def calculate_D(self, activity, connectivity) -> float:
    # Calculate branching parameter
    branching = self._calculate_branching_parameter(activity, connectivity)
    
    # Distance from critical value (1.0)
    D = np.abs(branching - 1.0)
    
    return D
```

**RG Beta Function:**
```
β_D = d_0 tanh[(C - C_bif)/w_D]

Parameters:
d_0 = 0.4 ± 0.05  (maximum dimensional shift)
C_bif = 7.5 ± 0.4 bits  (bifurcation threshold)
w_D = 1.0 ± 0.2 bits  (transition width)
```

**Range:** [0, ∞) where 0 = perfectly critical (code), OR [0, ~1] from RG saturation

**Units:** Dimensionless (distance from σ = 1.0)

**Interpretation:** How far is the system from the critical branching ratio? D=0 means critical dynamics, D>0 means sub/supercritical.

**Physical meaning:** 
- σ < 1 (subcritical): D = 1 - σ, system decays
- σ = 1 (critical): D = 0, power-law dynamics
- σ > 1 (supercritical): D = σ - 1, system explodes

**In C(t) formula (CODE):** Used as `C = Φ × R × (1 - exp(-λ*D))`
- When D=0 (critical): term = 0, **C goes to zero** ← BACKWARDS!
- When D→∞ (far from critical): term → 1, C maximized

**THE CRITICAL BUG:** Current code implementation makes criticality KILL consciousness!

**RG Framework Fixed Point:** D* = 0.89 ± 0.06

**Interpretation of D* = 0.89:**
- This is NOT distance to criticality (would be ~0 if critical)
- This is likely a NORMALIZED proximity measure or transformed variable
- Tanh function in β_D saturates D at ~1.0 maximum

---

### The D(t) Conflict Matrix

| Property | Intrinsic Dimension | Distance to Criticality (Code) | **RG Formalism** |
|----------|---------------------|--------------------------------|------------------|
| **Range** | ~5-9 | [0, ∞) | **[0, ~1] via tanh** |
| **Units** | Dimensions | Dimensionless distance | **Dimensionless** |
| **D=0 means** | No dimensions (impossible) | **Perfect criticality** | **Sub-critical?** |
| **D=7 means** | 7 independent DoF | 6 units away from critical | **N/A (saturates at ~1)** |
| **D* value** | - | - | **0.89 ± 0.06** |
| **In C formula** | C = Φ×R×7 (bit-dims) | C = Φ×R×(1-exp(-λ*D)) | **C = Φ×R×D** |
| **Physical basis** | PCA, correlation dim | Branching parameter σ | **Tanh-transformed** |
| **Consciousness requires** | High D (~7) | **LOW D (~0)** | **High D (~0.89)** |

**CRITICAL INCOMPATIBILITY:**
- Code formula (1 - exp(-λ*D)) predicts consciousness when D is LARGE (far from critical)
- HIRM theory claims consciousness emerges AT criticality (D should be small)
- **These are OPPOSITE predictions!**

**RG Resolution:** D* = 0.89 suggests D is NOT raw distance but a transformed variable where:
- D ~ 1 means "close to critical" (good for consciousness)
- D ~ 0 means "far from critical" (bad for consciousness)

**Proposed interpretation:** D = 1 - |σ - 1| or D = exp(-|σ - 1|) so that:
- σ = 1 (critical) → D = 1 (maximum)
- σ far from 1 → D → 0 (minimum)

This would make D* = 0.89 mean "close to but not perfectly critical"

---

## The Equation Conflict

### Theory Documents Claim:
```
C(t) = Φ(t) × R(t) × D(t)
```

**RG Framework Confirms:**
```
C* = Φ* × R* × D* = 4.82 × 1.95 × 0.89 = 8.37 ✓
```

**Units:** bits × dimensionless × dimensionless = bits ✓

### Code Implements:
```python
C = Phi * R * (1 - np.exp(-self.lambda_param * D))
```

Where:
- Φ: bits (integrated information)
- R: [1, 3] gain factor
- D: distance from criticality  
- (1 - exp(-λ*D)): [0, 1] saturation term

**Units:** bits × gain × [0,1] = bits (if we interpret R gain as dimensionless scaling)

**Behavior:**
- When D→0 (critical): (1-exp(0)) = 0 → C→0 ← **WRONG!**
- When D→∞ (far from critical): (1-exp(-∞)) = 1 → C→max ← **WRONG!**

**This predicts consciousness is KILLED by criticality - opposite of HIRM thesis!**

---

## Discovery Findings Summary

### R(t) Pathology: Triple Identity Crisis

1. **Clinical theory** wants R ∈ [0, 1] as gating variable (no self-ref → no consciousness)
2. **Code implementation** has R ∈ [1, 3] as gain/amplification (can't gate to zero)
3. **RG formalism** has R ∈ [1, ~3] with R* = 1.95 as coupling constant (R=1 is threshold, not zero)

**Convergence:** Code and RG AGREE on range [1, ~3], DISAGREE with clinical [0,1]

**Consequence:** The "zero-multiplier theorem" (if R=0, C=0) CANNOT be implemented in current code OR RG framework - R cannot reach zero by design

**Deeper issue:** This is not just normalization - it's two different models:
- **Model A (Clinical):** R as completeness ratio [0,1] - true gating
- **Model B (RG/Code):** R as coupling/gain [1,∞) - amplification above baseline

### D(t) Pathology: Conceptual Inversion + Missing Transform

1. **Some theory** treats D as intrinsic dimension (~7 for consciousness) - creates unit problem
2. **Code** treats D as distance from criticality (should be ~0 for consciousness) - has inversion bug
3. **RG framework** has D* = 0.89 (normalized, dimensionless) - suggests transformed variable

**Convergence:** RG fixes code's inversion IF D is re-interpreted as proximity not distance

**Consequence:** Current code implementation predicts consciousness is SUPPRESSED by criticality (D=0 → C=0), contradicting core HIRM thesis

**Proposed resolution:** D should be criticality PROXIMITY, not distance:
- D = exp(-|σ - 1|) or D = 1 - |σ - 1| (with appropriate normalization)
- Then D → 1 when critical, D → 0 when far from critical
- RG fixed point D* = 0.89 means "near but not perfectly critical"

### Equation Pathology: Theory vs Implementation

1. **Theory/RG:** C = Φ × R × D (pure multiplicative) ✓ Confirmed by RG consistency check
2. **Code:** C = Φ × R × (1 - exp(-λ*D)) (saturating) ✗ Has criticality inversion bug
3. **Neither** is clearly consistent with clinical R ∈ [0,1] without re-scaling

---

## Recommended Resolutions

**These are PRELIMINARY - CROSS-LLM CONSULTATION RECOMMENDED before decisions**

### For R(t) Resolution:

**Option A: Adopt RG/Code range [1, ~3]**
- PROS: Mathematically consistent with RG fixed point, directly measurable
- CONS: Breaks zero-multiplier theorem, requires reframing HIRM theory
- REQUIRES: Abandon clinical composite [0,1], rewrite all theory referring to R=0

**Option B: Re-scale RG to [0, 1]**
- PROS: Preserves zero-multiplier theorem, aligns with clinical intuition
- CONS: Requires defining R_rescaled = (R_RG - 1) / (R_max - 1), arbitrary R_max choice
- REQUIRES: Transform R* = 1.95 → R*_rescaled = (1.95-1)/(3-1) = 0.475

**Option C: Separate R_clinical from R_RG**
- PROS: Acknowledge both are useful, no forced unification
- CONS: More complex, harder to communicate, two different R variables
- REQUIRES: R_clinical ∈ [0,1] for gating, R_RG ∈ [1,3] for RG flow

**Option D (CROSS-LLM RECOMMENDED): Discover the "right" interpretation**
- Examine what R PHYSICALLY represents across all 193 papers in corpus
- Let mathematical and empirical constraints determine the answer
- Consult GPT-4/Gemini for independent analysis

**Current lean:** Option A (adopt RG range) seems most mathematically principled, but breaks a claimed theoretical pillar (zero-multiplier). Need external perspective.

---

### For D(t) Resolution:

**Option A: D = Intrinsic Dimension (deprecated based on RG evidence)**
- CONS: RG has D* = 0.89, not ~7; creates unit problem
- Status: Likely NOT what corpus actually uses

**Option B: D = Criticality Proximity (invert current code)**
- PROS: Aligns with RG D* = 0.89, fixes criticality inversion bug
- FORMULA: D = exp(-λ|σ - 1|) so D→1 when critical
- REQUIRES: Change code, rewrite docs referring to "distance"

**Option C: Keep current code formula but redefine D**
- Keep: C = Φ × R × (1 - exp(-λ*D))
- Redefine: D as distance to sub-critical (NOT to critical)
- So: D=0 means stuck in sub-critical (bad), D→∞ means reached super-critical (good)?
- CONS: Still doesn't explain D* = 0.89

**Current lean:** Option B (proximity not distance) - matches RG, fixes bug, clean interpretation

---

### For Equation Resolution:

**Option A: Pure multiplicative (RG-confirmed)**
```
C(t) = Φ(t) × R(t) × D(t)

Where:
Φ(t) ∈ [0, ~20] bits
R(t) ∈ [1, ~3] gain
D(t) ∈ [0, 1] proximity
```

**Units:** bits × dimensionless × dimensionless = bits ✓

**Fixed point:** C* = 4.82 × 1.95 × 0.89 = 8.37 bits ✓

**Zero-multiplier:** BROKEN (R and D can't be zero)

**Option B: Rescaled to preserve gating**
```
C(t) = Φ(t) × [(R(t) - 1)/(R_max - 1)] × D(t)

Where:
Φ(t) ∈ [0, ~20] bits
R(t) ∈ [1, 3] → rescaled to [0, 1]
D(t) ∈ [0, 1] proximity
```

**Preserves:** Zero-multiplier if R=1 or D=0

**Breaks:** RG fixed point arithmetic (C* ≠ Φ* × R*_rescaled × D*)

---

## CROSS-LLM CONSULTATION REQUEST

### Trigger: MANDATORY - Finalizing Variable Constitution

### Decision Points:
1. Should R be [0,1] completeness OR [1,3] coupling OR separated?
2. Should D be intrinsic dimension OR criticality proximity?
3. Should equation be pure multiplicative OR rescaled OR other?
4. What is the "zero-multiplier theorem" status given R ≥ 1?
5. Does HIRM require gating (R can be zero) or just amplification?

### Files to Provide:
- VARIABLE_DISCOVERY_AUDIT.md (this file)
- HIRM_Complete_RG_Framework.md (RG formalism)
- Section_9_Measurement_Protocols.md (clinical composite)
- consciousness_measure.py (code implementation)
- LLM_SYNTHESIS_ANALYSIS.md (previous GPT/Gemini input)

### Expected Synthesis:
- Mathematical consistency analysis: which choice creates cleanest formalism?
- Empirical testability: which R/D most measurable with current tools?
- Theoretical parsimony: should variables be unified or separate?
- Hidden assumptions: what does each choice commit HIRM to claiming?
- Alternative framings: are we missing a simpler interpretation?
- Risk analysis: which choices could falsify HIRM vs which are "safe"?

---

## Next Steps

**IMMEDIATE:** Prepare cross-LLM consultation request (David to orchestrate)

**After consultation:**
1. [ ] Finalize Variable Constitution based on synthesis
2. [ ] Audit remaining theory documents for R/D usage
3. [ ] Fix code implementations (consciousness_measure.py, etc.)
4. [ ] Update all documentation to match locked definitions
5. [ ] Validate C_critical = 8.3 bits still holds with corrected formulas
6. [ ] Document all corrections in corrections_registry.md

---

*This is a living document. Phase 1 discovery complete. Cross-LLM consultation recommended before Phase 2 (resolution decisions).*
