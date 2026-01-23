# HIRM Validation Dataset Requirements
# Generated: 2026-01-18
# Purpose: Identify what we ACTUALLY need for proper validation

## Theoretical Requirements

### Minimum Channel Count
- **Absolute minimum**: N ≥ 10 (for non-degenerate D_eff)
- **Recommended**: N ≥ 32 (for meaningful spatial integration)
- **Optimal**: N ≥ 64 (for rich phase space dynamics)

### Why N=3 Fails
1. D_eff maxes out at N=3 (no room for variation)
2. Phi cannot distinguish true integration from correlation
3. R measures rhythmic repetition, not self-reference
4. All components INCREASE with synchrony (opposite of theory)

### Temporal Requirements
- Sampling rate: ≥ 100 Hz (for neural dynamics)
- Epoch duration: 30s standard (already met)
- Total duration: ≥ 30 min per subject (statistical power)

### Experimental Design Requirements
1. **Clear state transitions**: Conscious → Unconscious → Conscious
2. **Ground truth labels**: Expert annotations or stimulus response
3. **Multiple subjects**: N ≥ 10 for statistics
4. **Repeated measures**: Within-subject comparisons

## Available Dataset Survey

### Sleep Studies
- **Sleep-EDF**: N=2 EEG + 1 EOG = 3 channels ❌ (TOO LOW)
- **Need to find**: High-density sleep EEG (64+ channels)

### Anesthesia Studies
- **Need to survey**: Typical channel counts
- **Advantage**: Clearer transitions, causal manipulation
- **Check**: Cambridge propofol, VitalDB

### Other Candidates
- **DOC patients**: Might have high-density recordings
- **Meditation studies**: State transitions, but harder to label
- **Binocular rivalry**: Perceptual transitions, high-density possible

## Action Items

1. Survey PhysioNet for high-density EEG datasets
2. Check anesthesia literature for channel counts
3. Contact labs directly if needed (Tononi, Mashour, etc.)
4. Make go/no-go decision based on actual availability

## Decision Criteria

**GO with dataset if:**
- N ≥ 32 channels
- Clear conscious/unconscious transitions
- Multiple subjects (N ≥ 10)
- Publicly available or obtainable

**NO-GO if:**
- N < 10 channels (theory breaks down)
- Ambiguous state labels
- Single subject or case study
- Requires IRB or legal barriers

## Implications for Paper 1

If no suitable dataset exists with N ≥ 32:
1. **Option A**: Simulation validation only (theoretical paper)
2. **Option B**: Collect our own data (months delay)
3. **Option C**: Collaborate with lab that has data
4. **Option D**: Acknowledge limitation, propose as prediction

**Recommendation**: Survey first, decide second
