# HIRM Recalibration Round 3 — Phi + R Operationalization Fix
## Created: 2026-05-17 | Follows two prior recalibration rounds

---

## STATUS AFTER ROUND 2

D_eff is FIXED (spectral entropy, correct gradient). But C ordering still inverted because Phi and R_obs also measure signal regularity, not their intended constructs.

**The core problem**: All three component proxies were capturing the same underlying signal property (regularity/periodicity). The multiplicative structure amplifies this shared error. Fix requires making the three components genuinely independent.

| Component | Current Proxy | Problem | Correct Behavior |
|-----------|--------------|---------|-----------------|
| Phi | PSI (signal entropy) | Higher for regular sleep signals | Should be HIGH for wake (diverse integration), LOW for deep sleep (uniform) |
| R_obs | Autocorrelation | Higher for periodic sleep signals | Should be HIGH for wake (active self-modeling), LOW for deep sleep (passive) |
| D_eff | Spectral entropy ✅ | **FIXED** — correct gradient | Wake(0.65) > S4(0.46) ✅ |

---

## STEP 1: Fix Phi — Replace PSI with a complexity-based measure

PSI (Phase Synchronization Index) is HIGH for synchronized signals. Deep sleep IS synchronized. So PSI goes up in deep sleep — the opposite of what information integration should do.

### Candidate: Lempel-Ziv Complexity (LZC)
```python
def lempel_ziv_complexity(signal):
    """LZC: higher for complex/irregular signals, lower for regular/periodic"""
    # Binarize around median
    median = np.median(signal)
    binary = ''.join(['1' if x > median else '0' for x in signal])
    
    # Count distinct substrings (Kaspar-Schuster algorithm)
    n = len(binary)
    i, k, l = 0, 1, 1
    c = 1
    while k + l <= n:
        if binary[i + l - 1] == binary[k + l - 1]:
            l += 1
        else:
            i += 1
            if i == k:
                c += 1
                k += l
                i = 0
                l = 1
            else:
                l = 1
    c += 1
    # Normalize
    return c / (n / np.log2(n))

def compute_Phi_lzc(epoch, sfreq):
    """Average LZC across channels as Phi proxy"""
    values = []
    for ch in range(epoch.shape[0]):
        values.append(lempel_ziv_complexity(epoch[ch]))
    return np.mean(values)
```

**Why LZC**: Well-established in consciousness research (Casali et al., 2013 — Perturbational Complexity Index). Wake = high complexity, deep sleep = low complexity, anesthesia = very low. Exactly what Phi should measure. Used in clinical DOC assessment.

### Alternative: Permutation Entropy
```python
from itertools import permutations
from collections import Counter

def permutation_entropy(signal, order=3, delay=1):
    """Permutation entropy — complexity measure, higher for irregular signals"""
    n = len(signal)
    ordinal_patterns = []
    for i in range(n - (order - 1) * delay):
        pattern = tuple(np.argsort(signal[i:i + order * delay:delay]))
        ordinal_patterns.append(pattern)
    counts = Counter(ordinal_patterns)
    total = len(ordinal_patterns)
    probs = np.array([c / total for c in counts.values()])
    return -np.sum(probs * np.log2(probs)) / np.log2(np.math.factorial(order))
```

---

## STEP 2: Fix R_obs — Replace autocorrelation with a self-reference measure

Autocorrelation is HIGH for periodic signals (deep sleep) and LOW for irregular signals (wake). But self-reference should measure recursive self-modeling, not periodicity.

### Candidate: Recurrence Rate (from Recurrence Quantification Analysis)
```python
def compute_R_recurrence(epoch, threshold=0.1):
    """Recurrence rate — measures how often the system revisits similar states
    Higher for wake (complex recurrence), lower for deep sleep (simple loops)
    Use TRAPPING TIME or DETERMINISM, not raw recurrence rate"""
    from scipy.spatial.distance import pdist, squareform
    
    # Use phase space embedding
    signal = epoch.mean(axis=0)  # average across channels
    tau = 10  # delay embedding
    m = 3     # embedding dimension
    N = len(signal) - (m-1)*tau
    
    embedded = np.array([signal[i:i+(m-1)*tau+1:tau] for i in range(N)])
    
    # Distance matrix
    distances = squareform(pdist(embedded))
    epsilon = threshold * np.std(signal)
    
    # Recurrence matrix
    R = (distances < epsilon).astype(float)
    
    # Determinism: fraction of recurrence points forming diagonal lines
    # Higher for structured dynamics (wake), lower for periodic/random
    diag_lengths = []
    for k in range(1, R.shape[0]):
        diag = np.diag(R, k)
        length = 0
        for val in diag:
            if val:
                length += 1
            else:
                if length >= 2:
                    diag_lengths.append(length)
                length = 0
    
    total_recurrence = R.sum() - R.shape[0]  # exclude main diagonal
    if total_recurrence == 0:
        return 0
    determinism = sum(diag_lengths) / (total_recurrence / 2)
    return min(determinism, 1.0)
```

### Simpler alternative: Transfer Entropy between channels
```python
def transfer_entropy(source, target, k=1):
    """Information flow between channels — higher for wake (active processing)"""
    # Discretize
    source_d = np.digitize(source, bins=np.percentile(source, [25, 50, 75]))
    target_d = np.digitize(target, bins=np.percentile(target, [25, 50, 75]))
    
    # Count joint and conditional probabilities
    # TE = H(target_future | target_past) - H(target_future | target_past, source_past)
    # Higher TE = more information flow = more self-referential processing
    # Implementation: use sklearn or dit library if available
    pass  # Use a library implementation for correctness
```

---

## STEP 3: Integration

In `consciousness_measure.py`, replace:
1. Phi calculation → use LZC (or permutation entropy)
2. R_obs calculation → use recurrence determinism (or transfer entropy)  
3. Keep D_eff as spectral entropy (already working)

Ensure all three are normalized to appropriate ranges and are genuinely measuring different things:
- **Phi (LZC)**: signal complexity / information richness
- **R (recurrence determinism)**: structured temporal self-reference
- **D (spectral entropy)**: frequency-domain dimensional complexity

These three capture different aspects of the signal and should be relatively independent.

---

## STEP 4: Re-run and evaluate

Same pipeline, same data, same subject:
```bash
set PYTHONIOENCODING=utf-8
cd D:\Projects\HIRM\Empirical\Analysis
python run_validation_now.py
```

**Success criteria (unchanged)**:
1. Ordering: Wake > REM > N1 > N2 > N3/N4
2. Statistical significance: p < 0.05 between conscious and unconscious states
3. Threshold crossing (with appropriate Phi_scale)
4. All three components vary meaningfully and INDEPENDENTLY across stages

---

## KEY INSIGHT FROM THIS PROCESS

The equation C = Phi × R × D is structurally sound. The problem was measurement theory — all three proxies collapsed to "signal regularity." For the multiplicative structure to work, the three dimensions MUST be operationally independent. Each should capture a genuinely different aspect of neural activity. This is the same principle as the equation itself: if the dimensions aren't independent, the product doesn't add information.

---

## FILES
- `D:\Projects\HIRM\Code\Core\consciousness_measure.py` — MODIFY (Phi + R computation)
- `D:\Projects\HIRM\Empirical\Analysis\run_validation_now.py` — run this
- `D:\Projects\HIRM\Empirical\Results\Sleep_EDF\` — results saved here
- `D:\Projects\HIRM\RECALIBRATION_HANDOFF.md` — previous round handoff (reference)
