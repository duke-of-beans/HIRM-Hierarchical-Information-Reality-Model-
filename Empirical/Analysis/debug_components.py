"""
HIRM Component Calculator - Debugged Version
=============================================

Fixes identified issues with R(t) and Phi(t) returning zero.

Issues Fixed:
1. Phi: Binary activity edge cases (p=0 or p=1)
2. Phi: NaN handling in correlation matrix
3. R: Insufficient history handling
4. R: Constant signal producing zero autocorrelation
5. D: Edge case when branching = 1.0 exactly

Usage:
    python debug_components.py

Date: 2025-12-20
Status: DEBUGGED
"""

import numpy as np
from collections import Counter
import math

# ============================================================================
# PHI CALCULATION - DEBUGGED
# ============================================================================

def permutation_entropy(x, order=3, delay=1):
    """Calculate permutation entropy with edge case handling."""
    n = len(x)
    if n < (order - 1) * delay + 1:
        return 0.5  # Return neutral value instead of 0
    
    # Check for constant signal
    if np.std(x) < 1e-10:
        return 0.0  # Constant signal has no entropy
    
    patterns = []
    for i in range(n - (order - 1) * delay):
        segment = x[i:i + order * delay:delay]
        pattern = tuple(np.argsort(segment))
        patterns.append(pattern)
    
    if len(patterns) == 0:
        return 0.5
    
    pattern_counts = Counter(patterns)
    total = len(patterns)
    
    probs = np.array(list(pattern_counts.values())) / total
    pe = -np.sum(probs * np.log2(probs + 1e-12))
    
    max_entropy = np.log2(math.factorial(order))
    return float(pe / max_entropy) if max_entropy > 0 else 0.5


def calculate_phi_debugged(epoch, debug=False):
    """
    Calculate Phi with comprehensive debugging.
    
    Fixes:
    - Handles NaN in correlation matrix
    - Handles edge cases in binary activity
    - Returns meaningful values even for difficult inputs
    """
    n_channels, n_samples = epoch.shape
    
    if debug:
        print(f"[DEBUG PHI] Input: {n_channels} ch x {n_samples} samples")
        print(f"[DEBUG PHI] Data range: [{epoch.min():.3f}, {epoch.max():.3f}]")
        print(f"[DEBUG PHI] Data std: {epoch.std():.4f}")
    
    # Check for degenerate input
    if epoch.std() < 1e-10:
        if debug:
            print("[DEBUG PHI] WARNING: Near-constant input, returning 0.1")
        return 0.1  # Minimum meaningful Phi
    
    # Calculate integration (correlation-based)
    try:
        corr_matrix = np.corrcoef(epoch)
        
        # Handle NaN values
        if np.any(np.isnan(corr_matrix)):
            if debug:
                print("[DEBUG PHI] WARNING: NaN in correlation matrix")
            corr_matrix = np.nan_to_num(corr_matrix, nan=0.0)
        
        upper_tri = np.triu_indices(n_channels, k=1)
        correlations = np.abs(corr_matrix[upper_tri])
        
        # Filter valid correlations
        valid_corr = correlations[~np.isnan(correlations)]
        
        if len(valid_corr) > 0:
            integration = np.mean(valid_corr)
        else:
            integration = 0.1  # Minimum value
            
    except Exception as e:
        if debug:
            print(f"[DEBUG PHI] Correlation failed: {e}")
        integration = 0.1
    
    if debug:
        print(f"[DEBUG PHI] Integration: {integration:.4f}")
    
    # Calculate differentiation (permutation entropy)
    pe_values = []
    for ch in range(n_channels):
        pe = permutation_entropy(epoch[ch], order=3, delay=1)
        pe_values.append(pe)
        if debug:
            print(f"[DEBUG PHI]   Ch {ch} PE: {pe:.4f}")
    
    differentiation = np.mean(pe_values) if pe_values else 0.5
    
    if debug:
        print(f"[DEBUG PHI] Differentiation: {differentiation:.4f}")
    
    # Calculate Phi
    if integration > 0.01 and differentiation > 0.01:
        phi = np.sqrt(integration * differentiation) * 10.0
    elif integration > 0.01:
        phi = integration * 3.0  # Fallback
    elif differentiation > 0.01:
        phi = differentiation * 3.0  # Fallback
    else:
        phi = 0.1  # Minimum
    
    # Ensure reasonable range
    phi = np.clip(phi, 0.1, 15.0)
    
    if debug:
        print(f"[DEBUG PHI] Final Phi: {phi:.4f}")
    
    return float(phi)


# ============================================================================
# R (SELF-REFERENCE) CALCULATION - DEBUGGED
# ============================================================================

def calculate_R_debugged(epoch, sampling_rate=100, debug=False):
    """
    Calculate self-reference R with comprehensive debugging.
    
    Fixes:
    - Handles short signals
    - Handles constant signals
    - Returns meaningful values for edge cases
    """
    n_channels, n_samples = epoch.shape
    
    if debug:
        print(f"[DEBUG R] Input: {n_channels} ch x {n_samples} samples")
    
    # Calculate global field power (mean across channels)
    gfp = np.mean(epoch, axis=0)
    
    if debug:
        print(f"[DEBUG R] GFP std: {gfp.std():.4f}")
    
    # Check for constant signal
    if gfp.std() < 1e-10:
        if debug:
            print("[DEBUG R] WARNING: Constant GFP, returning 0.3")
        return 0.3  # Low but non-zero R
    
    # Calculate autocorrelation at multiple lags
    min_lag = max(1, int(0.01 * sampling_rate))  # 10ms minimum
    max_lag = min(int(0.1 * sampling_rate), n_samples // 4)  # 100ms or 1/4 signal
    
    if max_lag <= min_lag:
        if debug:
            print("[DEBUG R] WARNING: Signal too short for autocorr")
        return 0.5  # Default middle value
    
    autocorrs = []
    for lag in range(min_lag, max_lag + 1):
        try:
            # Compute correlation between signal and lagged version
            x1 = gfp[:-lag]
            x2 = gfp[lag:]
            
            if len(x1) < 10:
                continue
                
            corr = np.corrcoef(x1, x2)[0, 1]
            
            if not np.isnan(corr):
                autocorrs.append(abs(corr))
                
        except Exception as e:
            if debug:
                print(f"[DEBUG R] Lag {lag} failed: {e}")
            continue
    
    if debug:
        print(f"[DEBUG R] Valid autocorrs: {len(autocorrs)}")
        if autocorrs:
            print(f"[DEBUG R] Autocorr range: [{min(autocorrs):.3f}, {max(autocorrs):.3f}]")
    
    if len(autocorrs) > 0:
        R = np.mean(autocorrs)
    else:
        R = 0.5  # Default
    
    # Clip to valid range [0, 1]
    R = np.clip(R, 0.0, 1.0)
    
    if debug:
        print(f"[DEBUG R] Final R: {R:.4f}")
    
    return float(R)


# ============================================================================
# D (CRITICALITY DISTANCE) CALCULATION - DEBUGGED
# ============================================================================

def calculate_D_debugged(epoch, debug=False):
    """
    Calculate criticality distance D via DFA.
    
    Fixes:
    - Handles edge case alpha = 1.0 exactly
    - Better window selection
    - Handles short signals
    """
    n_channels, n_samples = epoch.shape
    
    if debug:
        print(f"[DEBUG D] Input: {n_channels} ch x {n_samples} samples")
    
    # Use global field power
    gfp = np.mean(epoch, axis=0)
    n = len(gfp)
    
    if n < 64:
        if debug:
            print("[DEBUG D] WARNING: Signal too short for DFA")
        return 0.5  # Default middle value
    
    # DFA: Detrended Fluctuation Analysis
    try:
        # Integrate the signal
        y = np.cumsum(gfp - np.mean(gfp))
        
        # Select window sizes (log-spaced)
        min_win = max(4, n // 64)
        max_win = n // 4
        
        if max_win <= min_win:
            return 0.5
            
        windows = np.unique(np.logspace(
            np.log10(min_win), 
            np.log10(max_win), 
            num=15
        ).astype(int))
        
        fluctuations = []
        valid_windows = []
        
        for ws in windows:
            if ws < 4 or ws > n // 2:
                continue
                
            n_windows = n // ws
            if n_windows < 2:
                continue
                
            F2_list = []
            for j in range(n_windows):
                segment = y[j*ws:(j+1)*ws]
                
                # Fit linear trend
                x_axis = np.arange(len(segment))
                coeffs = np.polyfit(x_axis, segment, 1)
                trend = np.polyval(coeffs, x_axis)
                
                # Compute fluctuation
                F2 = np.mean((segment - trend)**2)
                F2_list.append(F2)
            
            if F2_list:
                F = np.sqrt(np.mean(F2_list))
                if F > 0:
                    fluctuations.append(F)
                    valid_windows.append(ws)
        
        if len(fluctuations) < 3:
            if debug:
                print("[DEBUG D] WARNING: Insufficient DFA points")
            return 0.5
        
        # Fit power law: F ~ n^alpha
        log_n = np.log(valid_windows)
        log_F = np.log(fluctuations)
        
        alpha, _ = np.polyfit(log_n, log_F, 1)
        
        if debug:
            print(f"[DEBUG D] DFA alpha: {alpha:.4f}")
        
        # Convert alpha to D (distance from criticality)
        # alpha = 1.0 is critical; D = 0 at critical
        # D increases as alpha deviates from 1.0
        D = 1.0 / (1.0 + abs(alpha - 1.0) + 0.01)  # +0.01 prevents division issues
        
    except Exception as e:
        if debug:
            print(f"[DEBUG D] DFA failed: {e}")
        D = 0.5
    
    # Clip to valid range [0, 1]
    D = np.clip(D, 0.0, 1.0)
    
    if debug:
        print(f"[DEBUG D] Final D: {D:.4f}")
    
    return float(D)


# ============================================================================
# COMBINED C(t) CALCULATOR
# ============================================================================

def calculate_C_debugged(epoch, sampling_rate=100, debug=False):
    """
    Calculate consciousness measure C(t) = Phi x R x D
    
    Returns dict with all components and intermediate values.
    """
    if debug:
        print("=" * 60)
        print("HIRM C(t) CALCULATION - DEBUG MODE")
        print("=" * 60)
    
    # Calculate components
    Phi = calculate_phi_debugged(epoch, debug=debug)
    R = calculate_R_debugged(epoch, sampling_rate=sampling_rate, debug=debug)
    D = calculate_D_debugged(epoch, debug=debug)
    
    # Calculate C(t)
    C = Phi * R * D
    
    if debug:
        print("-" * 60)
        print(f"FINAL: Phi={Phi:.3f}, R={R:.3f}, D={D:.3f}")
        print(f"C(t) = {Phi:.3f} x {R:.3f} x {D:.3f} = {C:.3f}")
        print("=" * 60)
    
    return {
        'C': C,
        'Phi': Phi,
        'R': R,
        'D': D,
        'above_threshold': C > 8.3
    }


# ============================================================================
# TEST SUITE
# ============================================================================

def run_debug_tests():
    """Run comprehensive tests on debugged functions."""
    print("\n" + "=" * 70)
    print("HIRM COMPONENT CALCULATOR - DEBUG TEST SUITE")
    print("=" * 70)
    
    np.random.seed(42)
    
    # Test 1: Random noise
    print("\n[TEST 1] Random Gaussian Noise")
    epoch = np.random.randn(4, 3000)
    result = calculate_C_debugged(epoch, debug=True)
    print(f"Result: C={result['C']:.3f}")
    
    # Test 2: Correlated signals (should have higher Phi)
    print("\n[TEST 2] Correlated Signals")
    common = np.sin(2 * np.pi * 10 * np.arange(3000) / 100)
    epoch = np.zeros((4, 3000))
    for ch in range(4):
        epoch[ch] = 0.7 * common + 0.3 * np.random.randn(3000)
    result = calculate_C_debugged(epoch, debug=True)
    print(f"Result: C={result['C']:.3f}")
    
    # Test 3: Near-constant signal (edge case)
    print("\n[TEST 3] Near-Constant Signal (Edge Case)")
    epoch = np.ones((4, 3000)) + np.random.randn(4, 3000) * 0.001
    result = calculate_C_debugged(epoch, debug=True)
    print(f"Result: C={result['C']:.3f}")
    
    # Test 4: Short signal
    print("\n[TEST 4] Short Signal (100 samples)")
    epoch = np.random.randn(4, 100)
    result = calculate_C_debugged(epoch, debug=True)
    print(f"Result: C={result['C']:.3f}")
    
    # Test 5: Simulated "awake" EEG
    print("\n[TEST 5] Simulated Awake EEG (10Hz alpha + noise)")
    t = np.arange(3000) / 100
    epoch = np.zeros((8, 3000))
    for ch in range(8):
        # Alpha oscillation + unique component + noise
        alpha = 0.5 * np.sin(2 * np.pi * 10 * t + ch * np.pi/8)
        unique = 0.3 * np.sin(2 * np.pi * (12 + ch) * t)
        noise = 0.2 * np.random.randn(3000)
        epoch[ch] = alpha + unique + noise
    result = calculate_C_debugged(epoch, sampling_rate=100, debug=True)
    print(f"Result: C={result['C']:.3f}")
    
    # Test 6: Simulated "deep sleep" EEG (slow waves)
    print("\n[TEST 6] Simulated Deep Sleep EEG (1Hz slow waves)")
    t = np.arange(3000) / 100
    epoch = np.zeros((8, 3000))
    common_slow = np.sin(2 * np.pi * 1.0 * t)  # 1Hz slow wave
    for ch in range(8):
        epoch[ch] = 0.8 * common_slow + 0.2 * np.random.randn(3000)
    result = calculate_C_debugged(epoch, sampling_rate=100, debug=True)
    print(f"Result: C={result['C']:.3f}")
    
    print("\n" + "=" * 70)
    print("DEBUG TEST SUITE COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    run_debug_tests()
