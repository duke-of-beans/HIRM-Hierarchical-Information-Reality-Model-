# HIRM — Hierarchical Information-Reality Model

A mathematical framework proposing that consciousness emerges through self-reference phase transitions when integrated information crosses a critical threshold. HIRM synthesizes Integrated Information Theory (IIT), Global Neuronal Workspace Theory (GNWT), Free Energy Principle (FEP), Self-Organized Criticality (SOC), and Higher-Order Thought theory (HOT) into a single predictive framework.

**Status:** Empirical validation in progress. Simulation validation complete (qualitative predictions confirmed). Sleep-EDF pipeline built and ready to execute. 22 falsifiable predictions documented.

---

## Core Equation

```
C(t) = Phi(t) x R(t) x D(t)
```

| Component | Name | Range | Role |
|-----------|------|-------|------|
| Phi(t) | Integrated Information | [0, ~20] bits | Integration strength (IIT-inspired) |
| R(t) | Self-Reference Coefficient | [1, 3] | Self-referential loop completeness |
| D(t) | Dimensional Complexity | [0, 1] normalized | Effective degrees of freedom |
| C(t) | Consciousness Measure | bits | Emerges when C > C_critical |

**Critical Threshold:** C_critical = 8.3 +/- 0.6 bits

**Fixed Point:** Phi* = 4.82, R* = 1.95, D* = 0.89 -> C* = 8.37 bits

R(t) is computed via the transform R_theory = 1 + 2 * R_obs, where R_obs is the observed self-reference metric in [0, 1]. This ensures the multiplicative structure preserves non-zero C when self-reference is present.

Consciousness is proposed to emerge when C(t) exceeds C_critical through a phase transition called **Self-Reference-Induced Decoherence (SRID)**.

---

## What HIRM Adds to Existing Theories

HIRM is not positioned as an alternative to existing consciousness theories. It is a synthesis framework — each major theory maps to a specific component or mechanism within HIRM:

| Theory | Maps To | HIRM's Additional Contribution |
|--------|---------|-------------------------------|
| IIT | Phi(t) | Threshold quantification, tractability via RG (O(2^N) -> O(N^3)) |
| GNWT | Neural ignition dynamics | Quantitative trigger condition via phase transition math |
| FEP | Dynamics near C_critical | State definition (when conscious), not just process |
| SOC | D(t) at criticality | Direct connection to consciousness measure |
| HOT | R(t) mechanism | Formalized as self-reference loop completeness |
| Orch-OR | Compatible substrate (QIL) | Self-reference mechanism vs. gravitational collapse |

---

## Simulation Validation Results

Kuramoto oscillator network simulation tested HIRM's core predictions under controlled conditions (Session 38). Results are documented in `Empirical/Simulation/VALIDATION_RESULTS.md`.

**Passed:**
- Ordering prediction: C_conscious (1.744) > C_pre-conscious (1.709) > C_unconscious (0.525)
- Non-monotonic relationship: Over-synchronization collapses C (0.166) — confirms edge-of-criticality requirement
- Zero-multiplier theorem: Multiplicative structure confirmed; any zero component drives C to zero

**Not yet validated:**
- Absolute threshold calibration: Simulation produced C_conscious = 1.74 bits vs. predicted 8.3 bits. Synthetic Kuramoto oscillators cannot capture biological neural network complexity. Absolute calibration requires empirical neural data.

---

## Empirical Validation (In Progress)

### Sleep-EDF Pipeline
A complete validation pipeline has been built to test whether C(t) crosses 8.3 bits at the wake/sleep boundary using polysomnography data from the Sleep-EDF database (197 subjects available).

- Pipeline: `Empirical/Analysis/sleep_edf_validation.py`
- Protocol: `Empirical/Protocols/Sleep_EDF_Validation_Protocol.md`
- Guide: `Empirical/Analysis/SLEEP_EDF_QUICKSTART.md`
- **Status:** Ready to execute. Results pending.

### Cambridge High-Density Dataset
20 subjects, 91 EEG channels, 4 consciousness states (wake, light anesthesia, deep anesthesia, recovery). Identified as the highest-value secondary validation dataset.

- Access instructions: `Empirical/Datasets/Cambridge_Access_Instructions.md`
- **Status:** Download pending.

### What "Empirical Support" Means Here
Several findings in the existing neuroscience literature are *consistent with* HIRM predictions — anesthesia hysteresis patterns, neural avalanche criticality signatures, PCI thresholds correlating with consciousness states. These are encouraging but they are not independent tests of HIRM. They are analogical mappings showing existing measurements could be compatible with C_critical = 8.3 bits. True empirical validation of HIRM requires running the HIRM pipeline on neural data and testing whether the specific predictions hold.

---

## Falsifiable Predictions

22 testable predictions are documented in `docs/HIRM_Falsifiable_Predictions.docx`, organized by category:

- Quantum decoherence timescales (5 predictions)
- Anesthesia transition dynamics (6 predictions)
- Neural criticality signatures (7 predictions)
- Clinical DOC stratification (4 predictions)

All predictions are designed to be falsifiable with currently available technology.

---

## Repository Structure

```
HIRM/
|- Code/Core/          # Computational framework (consciousness_measure.py, etc.)
|- Code/Tools/         # Analysis toolkits (RG, information geometry, stat mech)
|- Code/Notebooks/     # Tutorial notebooks
|- Corpus/             # 193-paper research corpus and citation indices
|- Empirical/          # Validation protocols, analysis scripts, results
|- External/           # Cross-domain investigations (Schauberger, UAP)
|- Figures/Publication/# Publication-ready figures
|- Master_Data/        # Locked constants and terminology (source of truth)
|- Mathematical/       # PCI-to-C_critical mapping
|- Publications/       # Manuscripts (3 papers in progress) and popular science
|- Theory/             # Core theory, extensions, mathematical tools
|- docs/               # Key documents (framework overview, predictions, bibliography)
```

---

## Manuscripts (In Progress)

Three papers are in active development. All are open for scrutiny and feedback.

**Paper 1: Brain Criticality and Consciousness Emergence**
- Target: 18,000 words (currently 16,100)
- Location: `Publications/Manuscripts/Paper_1_Brain_Criticality/`
- Status: Needs empirical results section + clinical protocols

**Paper 2: Quantum-Classical Bridge (SRID Mechanism)**
- Target: 12,000 words (currently 9,400)
- Location: `Publications/Manuscripts/Paper_2_Quantum_Classical/`
- Status: Needs Introduction, Competing Theories, Discussion, Conclusion

**Paper 3: Information Persistence Through Dimensional Bifurcation**
- Target: 12,000 words (currently 10,200)
- Location: `Publications/Manuscripts/Paper_3_Temporal_Persistence/`
- Status: Complete — ready for review

---

## Research Corpus

193 peer-reviewed papers synthesized across 7 domains. Citation indices and literature reviews are in `Corpus/`. Key reviews:

- `Corpus/Reviews/Consciousness_Literature_Corpus_193_Papers.md` — full corpus overview
- `Corpus/Reviews/Mathematical_Consciousness_Corpus_64_Papers.md` — mathematical foundations
- `Corpus/Index/Citations.json` — machine-readable citation database

---

## Getting Started

To understand the framework: start with `docs/HIRM_Framework_Overview.docx`

To run the computational tools: see `Code/Notebooks/tutorial_1_basic_C_calculation.ipynb`

To understand the empirical validation plan: see `Empirical/Analysis/SLEEP_EDF_QUICKSTART.md`

To see what's locked and why: see `Master_Data/Constants/locked_constants.md`

---

## Collaboration

This repository is open for academic scrutiny. If you have questions, critiques, or want to discuss methodology, predictions, or potential collaboration — open an issue.

Areas actively seeking input:
- Simulation-to-empirical calibration methodology
- Paper 1 clinical protocols and validation study design
- Paper 2 competing theories analysis
- Whether the R(t) transform adequately captures self-reference
- Alternative falsification approaches for the 22 predictions

---

## Locked Constants

These values are established across the framework and must be consistent everywhere:

| Constant | Value | Derivation |
|----------|-------|------------|
| C_critical | 8.3 +/- 0.6 bits | Holographic bound + RG fixed point convergence |
| Core equation | C(t) = Phi(t) x R(t) x D(t) | Multiplicative structure |
| Fixed point | Phi*=4.82, R*=1.95, D*=0.89 | RG flow convergence |

Source of truth: `Master_Data/Constants/locked_constants.md`