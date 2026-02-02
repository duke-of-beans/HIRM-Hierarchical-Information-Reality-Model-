# LOCKED CONSTANTS REGISTRY
## HIRM Research - Single Source of Truth
## Last Updated: 2025-12-21
## Status: AUTHORITATIVE - All documents must match these values

---

## CRITICAL RULE
**Any document using different values is WRONG and must be corrected.**
**Database (hirm.db) is the master - this file mirrors it for human reference.**

---

## CORE HIRM CONSTANTS

### Consciousness Threshold
| Symbol | Name | Value | Units | Status |
|--------|------|-------|-------|--------|
| C_critical | Critical Consciousness Threshold | **8.3 ± 0.6** | bits | ESTABLISHED |

**Derivation:** Holographic bound + RG fixed point convergence
**Source:** `Theory/Core/Mathematical_Foundations.md`
**Evidence:** Multiple independent derivations converge to this value

---

### Critical Exponents (Ising Universality Class)

| Symbol | Name | Value | Status |
|--------|------|-------|--------|
| ν (nu) | Correlation length exponent | ~0.63 | ESTABLISHED |
| γ (gamma) | Susceptibility exponent | ~1.24 | ESTABLISHED |
| β (beta) | Order parameter exponent | ~0.33 | ESTABLISHED |

**Source:** Standard statistical mechanics (3D Ising)
**Note:** Brain criticality expected to match Ising universality

---

### Neural Avalanche Exponents

| Symbol | Name | Value | Status |
|--------|------|-------|--------|
| τ (tau) | Avalanche duration exponent | ~2.0 | PROVISIONAL |
| α (alpha) | Avalanche size exponent | ~1.5 | PROVISIONAL |

**Source:** Critical brain dynamics literature (Beggs, Plenz)
**Note:** PROVISIONAL - awaiting independent verification

---

## LOCKED EQUATION: CONSCIOUSNESS MEASURE

```
C(t) = Φ(t) × R(t) × D(t)
```

**Where:**
- **Φ(t)** = Integrated information [bits] - IIT-inspired measure
- **R(t)** = Self-reference coefficient [dimensionless, 0-1]
- **D(t)** = Dimensional complexity [effective dimensions]
- **C(t)** = Consciousness capacity [bits]

**Dimensional Check:** bits × dimensionless × dimensions = bits ✓

---

## KNOWN ERRORS TO PREVENT

| Error | Correct Value | Source of Error |
|-------|---------------|-----------------|
| C_critical = 7.5 | 8.3 ± 0.6 | Outdated early estimate |
| C_critical = 10.0 | 8.3 ± 0.6 | Rounding error |
| Ouroboros Observer | HIRM | Legacy terminology |

---

## UPDATE PROTOCOL

When updating constants:
1. Update database: `hirm.db` constants table
2. Update this file
3. Run `quality_gate.py` on all documents using the constant
4. Log correction in corrections table
5. Flag affected documents for review
