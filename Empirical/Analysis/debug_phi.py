"""Debug Phi calculation"""
import numpy as np
from collections import Counter

def permutation_entropy(x, order=3, delay=1):
    """Calculate permutation entropy."""
    n = len(x)
    if n < (order - 1) * delay + 1:
        return 0.0
    
    patterns = []
    for i in range(n - (order - 1) * delay):
        pattern = tuple(np.argsort(x[i:i + order * delay:delay]))
        patterns.append(pattern)
    
    pattern_counts = Counter(patterns)
    total = len(patterns)
    
    probs = np.array(list(pattern_counts.values())) / total
    pe = -np.sum(probs * np.log2(probs + 1e-12))
    
    max_entropy = np.log2(np.math.factorial(order))
    return float(pe / max_entropy) if max_entropy > 0 else 0.0


def calculate_phi(epoch):
    """Debug Phi calculation."""
    n_channels, n_samples = epoch.shape
    print(f"Epoch shape: {n_channels} channels, {n_samples} samples")
    
    # Integration
    corr_matrix = np.corrcoef(epoch)
    print(f"Correlation matrix shape: {corr_matrix.shape}")
    print(f"Corr matrix:\n{corr_matrix}")
    
    upper_tri = np.triu_indices(n_channels, k=1)
    correlations = np.abs(corr_matrix[upper_tri])
    print(f"Upper triangle correlations: {correlations}")
    
    correlations_clean = correlations[~np.isnan(correlations)]
    integration = np.mean(correlations_clean) if len(correlations_clean) > 0 else 0.0
    print(f"Integration: {integration:.4f}")
    
    # Differentiation
    pe_values = []
    for ch in range(n_channels):
        pe = permutation_entropy(epoch[ch], order=3, delay=1)
        pe_values.append(pe)
        print(f"  Channel {ch} PE: {pe:.4f}")
    
    differentiation = np.mean(pe_values)
    print(f"Differentiation: {differentiation:.4f}")
    
    # Phi
    if integration > 0 and differentiation > 0:
        phi = np.sqrt(integration * differentiation) * 10.0
    else:
        phi = 0.0
    print(f"Phi = sqrt({integration:.4f} * {differentiation:.4f}) * 10 = {phi:.4f}")
    
    return phi


# Generate test epoch
print("="*60)
print("Test with random data")
print("="*60)
epoch = np.random.randn(4, 3000)
phi = calculate_phi(epoch)

print("\n" + "="*60)
print("Test with correlated data")
print("="*60)
common = np.sin(2 * np.pi * 10 * np.arange(3000) / 100)
epoch = np.zeros((4, 3000))
for ch in range(4):
    epoch[ch] = 0.6 * common + 0.4 * np.random.randn(3000)
phi = calculate_phi(epoch)

print("\n" + "="*60)
print("Test with sinusoidal data (like synthetic generator)")
print("="*60)
t = np.arange(3000) / 100
common_signal = np.sin(2 * np.pi * 10 * t) + 0.3 * np.sin(2 * np.pi * 20 * t)
epoch = np.zeros((4, 3000))
for ch in range(4):
    unique = np.sin(2 * np.pi * (10 + ch * 0.5) * t + ch * np.pi/4) + 0.3 * np.random.randn(3000)
    epoch[ch] = 0.6 * common_signal + 0.4 * unique
phi = calculate_phi(epoch)
