# HIRM 2.0 Architecture Specification
## Version: 0.1 DRAFT | Created: 2026-01-17 | Session 35

---

## Purpose

This document defines the modular architecture for HIRM 2.0, addressing structural issues identified through cross-LLM synthesis (GPT-4 and Gemini). The goal is to transform HIRM from a corpus into a system with clear epistemic layers, locked definitions, and explicit falsification criteria.

---

## Architectural Principles

1. **Modular Separation:** Claims at different epistemic tiers must be explicitly separated
2. **Definition Lock:** Variables must have ONE canonical definition across all documents and code
3. **Falsification First:** Every claim must state what would disprove it
4. **No Hidden Degrees of Freedom:** Normalization choices must be explicit and justified
5. **Theory vs Framework:** Be honest about what HIRM currently is and what it aspires to be

---

## Layer Architecture

### Layer 0: FOUNDATIONS
**Status:** Locked, non-negotiable, source of truth
**Location:** `/Master_Data/`

| Component | File | Purpose |
|-----------|------|---------|
| Variable Constitution | `VARIABLE_CONSTITUTION.md` | Canonical definitions for Phi, R, D, C |
| Locked Constants | `locked_constants.md` | C_crit = 8.3 +/- 0.6 with epistemic status |
| Terminology Reference | `terminology_reference.md` | HIRM nomenclature |
| Epistemic Status Guide | `epistemic_status_guide.md` | How to tag claims |

**Compliance Rule:** Any document or code that uses Phi, R, D, or C MUST conform to Variable Constitution. Violations are logged to `corrections_registry.md`.

---

### Layer 1: HIRM-CORE
**Status:** Standard neuroscience, publication-ready
**Evidentiary Standard:** Peer-reviewed empirical support, testable with current technology
**Location:** `/Theory/Core/` and `/Publications/Manuscripts/Paper_1_*/`

**Scope:**
- Phase transition framing of consciousness
- Clinical applications (anesthesia, sleep, disorders of consciousness)
- Criticality signatures (critical slowing, hysteresis, avalanche statistics)
- PCI/empirical anchoring
- Threshold behavior at C_crit

**What HIRM-Core Does NOT Claim:**
- Quantum mechanisms
- Measurement problem resolution
- Metaphysics of identity persistence

**Falsification Criteria:**
- C(t) fails to separate LOC vs ROC with preregistered AUC threshold
- No critical signatures across multiple anesthetic agents
- Threshold behavior absent in DOC stratification

---

### Layer 2: HIRM-DYNAMICS
**Status:** Systems theory, testable but theoretical
**Evidentiary Standard:** Mathematical consistency, indirect empirical support
**Location:** `/Theory/Mathematical_Tools/` and `/Theory/Extensions/`

**Scope:**
- Free Energy Principle integration (precision as R-dial)
- Renormalization Group flow formalism
- Bifurcation theory (cusp catastrophe, Bogdanov-Takens)
- Fast-slow dynamics (relaxation oscillator model)
- Information geometry (Fisher information, geodesics)

**Relationship to HIRM-Core:**
- Provides mechanistic underpinning for Core claims
- Generates additional predictions testable within Core framework
- Does not require acceptance of HIRM-Q

**Falsification Criteria:**
- RG flow parameters inconsistent across scales
- Predicted hysteresis width scaling fails
- Fast-slow separation not observable in neural data

---

### Layer 3: HIRM-Q (Quantum Extension)
**Status:** Speculative, higher burden of proof
**Evidentiary Standard:** Requires uniquely quantum predictions confirmed
**Location:** `/Theory/Extensions/Quantum_*/` and `/Publications/Manuscripts/Paper_2_*/`

**Scope:**
- Self-Reference-Induced Decoherence (SRID) mechanism
- Persistent Information Structure (PIS) with specified substrate
- Quantum signatures in consciousness transitions
- Measurement problem implications
- Three-layer architecture (QIL/CCL/MOL)

**Critical Dependencies:**
- SRID requires evidence that C_crit triggers quantum-relevant effects
- PIS requires physical substrate hypothesis (microtubules? connectome topology?)

**Relationship to Other Layers:**
- HIRM-Q is OPTIONAL—HIRM-Core and HIRM-Dynamics stand without it
- If HIRM-Q is falsified, the framework doesn't collapse

**Falsification Criteria:**
- Isotope anesthesia experiments show no effect (smoking gun)
- No quantum coherence signatures at threshold
- PIS cannot be operationalized/measured

---

### Layer 4: EXTENSIONS
**Status:** Future research, explicitly speculative
**Location:** `/Theory/Extensions/` and `/External/`

**Scope:**
- AI consciousness applications and safety tripwires
- Cross-species consciousness gradients
- Phenomenology integration (process philosophy, Buddhist no-self)
- Novel predictions (315-state convergence, bifurcation echo)
- Alternative substrates

**Epistemic Status:** "If HIRM is correct, then..." framing required

---

## Variable Constitution (DRAFT)

This is the most critical deliverable. Current conflicts must be resolved.

### Phi(t) - Integrated Information

| Property | Current State | Proposed Resolution |
|----------|---------------|---------------------|
| Units | Bits (claimed) | Bits (confirmed) |
| Range | Unbounded | [0, ~20] for neural systems |
| Definition | IIT-style, varies | Use PID-based synergy as proxy |
| Code implementation | Random partition correlation | Align with definition |

**Open Question:** Do we adopt Partial Information Decomposition as canonical Phi proxy?

### R(t) - Self-Reference Completeness

| Property | Current State | Proposed Resolution |
|----------|---------------|---------------------|
| Units | Dimensionless | Dimensionless |
| Range | [0,1] in theory, [1,3] in code, >1 in RG | **CONFLICT - MUST RESOLVE** |
| Definition | "Self-model completeness" | Needs operational specification |
| Code implementation | 1 + log(recursion_depth) | Misaligned with theory |

**Critical Decision Required:**
- Option A: R in [0,1] as true completeness ratio
- Option B: R as recursion gain (can exceed 1)
- Option C: Separate R_theory from R_operational with explicit transform

### D(t) - Dimensional Complexity

| Property | Current State | Proposed Resolution |
|----------|---------------|---------------------|
| Units | Dimensions OR dimensionless | **CONFLICT - MUST RESOLVE** |
| Range | ~7 raw OR [0,1] normalized | Pick one |
| Definition | PCA DoF OR distance-to-criticality | **CONFLICT - MUST RESOLVE** |
| Code implementation | abs(branching_param - 1) | Distance-to-criticality |

**Critical Decision Required:**
- Option A: D = D_dim (intrinsic manifold dimension)
- Option B: D = D_crit (distance to criticality)  
- Option C: Separate D_dim and D_crit as distinct variables

### C(t) - Consciousness Measure

| Property | Current State | Proposed Resolution |
|----------|---------------|---------------------|
| Units | Bits | Bits |
| Equation | Phi * R * D OR Phi * R * (1-exp(-lambda*D)) | **CONFLICT - MUST RESOLVE** |
| Log-space | Mentioned but not adopted | Consider: c = log(Phi) + log(R) + log(D) |

**Critical Decision Required:**
- Option A: C = Phi * R * D (pure multiplicative)
- Option B: C = Phi * R * f(D) where f saturates
- Option C: c = log(C) as primary variable

### C_crit - Critical Threshold

| Property | Current State | Proposed Resolution |
|----------|---------------|---------------------|
| Value | 8.3 +/- 0.6 bits | Maintain (pending review) |
| Epistemic Status | "First principles" claimed | Downgrade to "Empirically anchored with theoretical motivation" |
| Scale | Cortical column (1mm) | Explicitly state scale |

---

## Audit Protocol

### Phase 1: Conflict Detection

For each document in corpus:
1. Extract all uses of Phi, R, D, C
2. Compare against Variable Constitution (once finalized)
3. Flag conflicts with specific line numbers
4. Classify: definition conflict, range conflict, unit conflict

### Phase 2: Resolution

For each conflict:
1. Determine which version aligns with locked definition
2. If unclear, escalate for decision
3. Document resolution in corrections_registry.md

### Phase 3: Migration

1. Update documents to conform
2. Move non-conforming versions to `_Archive/superseded/`
3. Add epistemic status headers
4. Reorganize into layer structure

### Phase 4: Validation

1. Run consistency checks
2. External LLM review for remaining contradictions
3. Gap analysis per layer

---

## Epistemic Status Tags

Every major claim should be tagged:

- `[ESTABLISHED]` - Peer-reviewed empirical support
- `[SUPPORTED]` - Indirect evidence, theoretical consistency
- `[PROPOSED]` - Plausible hypothesis, awaiting test
- `[SPECULATIVE]` - Requires substantial new evidence
- `[EXPLORATORY]` - Future research direction

Example:
> The threshold behavior of consciousness at C_crit [SUPPORTED] suggests a phase transition mechanism [PROPOSED] that may resolve the measurement problem [SPECULATIVE].

---

## Directory Structure (Proposed)

```
D:\Research\HIRM\
|
+-- Master_Data/           # Layer 0: FOUNDATIONS (source of truth)
|   +-- Constants/
|   +-- Variables/         # NEW: Variable Constitution
|   +-- Terminology/
|   +-- Corrections/
|
+-- Theory/
|   +-- Core/              # Layer 1: HIRM-CORE
|   +-- Dynamics/          # Layer 2: HIRM-DYNAMICS (renamed from Mathematical_Tools)
|   +-- Quantum/           # Layer 3: HIRM-Q (new, extracted from Extensions)
|   +-- Extensions/        # Layer 4: EXTENSIONS
|
+-- Publications/
|   +-- Manuscripts/
|   |   +-- Paper_1_Brain_Criticality/    # HIRM-CORE
|   |   +-- Paper_2_Quantum_Classical/    # HIRM-Q
|   |   +-- Paper_3_Temporal_Persistence/ # HIRM-Q
|   +-- Popular/
|
+-- Empirical/             # Clinical/experimental support
+-- Code/                  # Computational implementations (MUST align with Variable Constitution)
+-- Documentation/         # Guides, summaries, synthesis
+-- Logs/                  # Session logs, audit reports
+-- _Archive/              # Superseded versions
```

---

## Success Criteria

HIRM 2.0 refactoring is complete when:

1. [ ] Variable Constitution finalized and locked
2. [ ] All documents audited for compliance
3. [ ] Conflicts resolved with documented decisions
4. [ ] Code aligned with Variable Constitution
5. [ ] Epistemic status tags on all major claims
6. [ ] Directory restructured by layers
7. [ ] External validation (LLM review) passes
8. [ ] Git commit with "HIRM 2.0 BASELINE" tag

---

## Next Immediate Actions

1. **Finalize Variable Constitution** - Make decisions on R range, D definition, equation form
2. **Audit key documents** - Start with Master Executive Summary, Mathematical Foundations, consciousness_measure.py
3. **Create epistemic status guide** - Establish tagging convention
4. **Document first batch of conflicts** - Produce conflict report

---

*This is a living document. Version 0.1 establishes the framework; subsequent versions will reflect decisions made during audit.*
