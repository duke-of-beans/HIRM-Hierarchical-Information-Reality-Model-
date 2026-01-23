# HIRM Simulation-Based Validation Design
# Created: 2026-01-18
# Purpose: Validate HIRM framework in controlled synthetic environment

## Why Simulation?

**Problem**: Low-dimensional empirical data (N=3 channels) cannot distinguish:
- True integration (diverse coordinated signals)
- False integration (identical synchronized signals)

**Solution**: Build synthetic neural network where we CONTROL:
- Number of processing nodes (N)
- Integration strength (coupling)
- Self-reference depth (recurrent loops)
- Dimensional complexity (eigenvalue spectrum)

**Advantage**: Ground truth is KNOWN - we design the system, we know what C should be

---

## Simulation Architecture

### Base Network Model: Kuramoto Oscillators with Recurrent Coupling

**Why Kuramoto?**
- Captures phase synchronization (key to consciousness theories)
- Well-characterized phase transitions
- Controllable coupling strength
- Analytical solutions for some regimes

**Extended Model:**
```
dθᵢ/dt = ωᵢ + (K/N) Σⱼ sin(θⱼ - θᵢ) + αᵢ Σⱼ W_ij sin(θⱼ - θᵢ - φ_ij)
```

Where:
- θᵢ = phase of oscillator i
- ωᵢ = natural frequency of oscillator i
- K = global coupling strength (controls integration)
- W_ij = recurrent connection weights (controls self-reference)
- φ_ij = phase delays (creates temporal structure)
- αᵢ = self-reference strength parameter

---

## Controllable Parameters

### 1. Integration (Φ)
**Manipulate via**: Global coupling strength K
- K = 0: No coupling (Φ ≈ 0)
- K = K_critical: Partial synchrony (Φ moderate)
- K >> K_critical: Full synchrony (Φ high, but degenerates)

**Expected**: Bell curve - Φ peaks at edge of synchronization

### 2. Self-Reference (R)
**Manipulate via**: Recurrent weight matrix W_ij structure
- Feedforward only: W_ij sparse, no loops (R low)
- Recurrent loops: W_ij with cycles (R increases)
- Hierarchical recurrence: Multi-scale loops (R high)

**Expected**: R ∝ number of recurrent pathways

### 3. Dimensional Complexity (D)
**Manipulate via**: Frequency distribution σ(ω)
- Identical ωᵢ: All oscillators same (D ≈ 1)
- Narrow σ(ω): Similar frequencies (D low)
- Broad σ(ω): Diverse frequencies (D → N)

**Expected**: D ≈ effective rank of covariance matrix

---

## Experimental Conditions

### Condition 1: "Unconscious State" (Low C)
- **Integration**: K = 0.1 (weak coupling)
- **Self-reference**: Feedforward only (no recurrent loops)
- **Dimensionality**: Narrow frequency distribution (σ(ω) = 0.1)
- **Predicted C**: 0.5-2 bits

### Condition 2: "Pre-Conscious State" (Medium C)
- **Integration**: K = 0.5 (moderate coupling)
- **Self-reference**: Sparse recurrent loops (10% connectivity)
- **Dimensionality**: Moderate frequency spread (σ(ω) = 0.5)
- **Predicted C**: 4-6 bits

### Condition 3: "Conscious State" (High C)
- **Integration**: K = K_critical (edge of synchronization)
- **Self-reference**: Dense recurrent loops (hierarchical)
- **Dimensionality**: Broad frequency distribution (σ(ω) = 1.0)
- **Predicted C**: 8-12 bits (crossing C_critical threshold)

### Condition 4: "Over-Synchronized State" (Medium C)
- **Integration**: K >> K_critical (full synchrony)
- **Self-reference**: Dense recurrence
- **Dimensionality**: Degenerate (all frequencies locked)
- **Predicted C**: 3-5 bits (high Φ but D collapses)

---

## Implementation Plan

### Step 1: Core Simulator (2 hours)
- Kuramoto network with recurrent extensions
- Runge-Kutta integration
- Parameter sweep infrastructure
- Activity recording

### Step 2: HIRM Measurement (1 hour)
- Apply consciousness_measure.py to simulated activity
- Verify components (Φ, R, D) respond to parameter changes
- Check C(t) = Φ × R × D ordering

### Step 3: Validation Experiments (1 hour)
- Run 4 conditions above
- Measure C(t) for each
- Verify ordering: Conscious > Pre-conscious > Unconscious
- Check critical threshold crossing

### Step 4: Sensitivity Analysis (1 hour)
- Vary N (10, 20, 50, 100 oscillators)
- Vary parameter ranges
- Check robustness of C_critical ≈ 8.3 bits

### Step 5: Publication Figures (1 hour)
- Time series of oscillator phases
- C(t) across conditions
- Component breakdown (Φ, R, D)
- Parameter space map

---

## Success Criteria

**PASS if:**
1. C_conscious > C_critical > C_unconscious
2. All three components (Φ, R, D) independently controllable
3. Over-synchronization shows C decrease (validates non-monotonic relationship)
4. Results robust across N ∈ [20, 100]

**FAIL if:**
1. C ordering inverted
2. Components don't respond to parameters
3. C_critical threshold doesn't emerge
4. Results collapse with N changes

---

## Expected Timeline

- Design complete: 0.5 hours (THIS DOCUMENT)
- Implementation: 2 hours
- Validation: 2 hours
- Analysis + Figures: 1.5 hours
- **Total: 6 hours**

---

## Relationship to Paper 1

**Section**: Methods - Computational Validation
**Content**: 
- "To validate HIRM under controlled conditions, we simulated..."
- "Synthetic network allows independent manipulation of..."
- "Results confirm C(t) threshold behavior predicted by theory"

**Figure**: Multi-panel showing:
- Network architecture
- Oscillator time series for each condition
- C(t) measurements with C_critical threshold
- Component contributions (Φ, R, D) breakdown

---

## Next Steps After Simulation

1. **Search for high-density empirical data** (Phase 2)
2. **If found**: Replicate validation with real neural data
3. **If not found**: Paper 1 presents simulation validation
4. **Discussion**: "Empirical validation requires 64+ channel recordings"

---

## Notes

- This is PROOF OF CONCEPT, not mechanistic neuroscience
- Goal: Validate mathematical framework, not model real brains
- Honest about limitations: "Toy model demonstrates principle"
- Sets requirements for empirical validation

---

**Status**: Design complete, ready for implementation
**Next**: Build core simulator
