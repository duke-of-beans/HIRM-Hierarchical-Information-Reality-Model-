"""
Consciousness Measure Calculator - CONSTITUTION COMPLIANT
==========================================================

Calculate C(t) = Phi(t) * R_theory(t) * D_eff(t)

Implements Variable Constitution v1.0:
- Pure multiplicative formula (no saturation)
- R_theory = 1 + 2*R_obs transform
- D as dimensional embedding (PCA-based), NOT distance to criticality
- sigma(t) tracked separately for bifurcation analysis

VERSION: 2.0 - Variable Constitution Compliant
UPDATED: 2026-01-17 Session 36
SOURCE: Master_Data/Variables/VARIABLE_CONSTITUTION_V1.md
"""

import numpy as np
from typing import Dict, Optional, Tuple, Union
from scipy.sparse import csr_matrix
from scipy.linalg import eigh
from scipy.stats import entropy
from scipy.signal import welch
import warnings


class ConsciousnessMeasure:
    """
    Calculate the consciousness measure C(t) and its components.
    
    VARIABLE CONSTITUTION COMPLIANT:
    --------------------------------
    C(t) = Phi(t) * R_theory(t) * D_eff(t)
    
    Where:
    - Phi(t) in [0, ~20] bits (integrated information)
    - R_theory(t) in [1, 3] (self-referential coupling)
    - D_eff(t) in [0, 1] (dimensional embedding, normalized)
    - sigma(t) tracked separately (branching parameter for criticality)
    
    Parameters
    ----------
    Phi_method : str, optional
        Method for calculating Phi: 'geometric', 'stochastic', 'PSI'
    temporal_window : int, optional
        Number of timesteps to use for calculating R(t)
    D_max : float, optional
        Normalization constant for D_eff (default 8.0, calibrate empirically)
    
    Methods
    -------
    calculate_C : Calculate full C(t) measure
    calculate_Phi : Calculate integrated information
    calculate_R_obs : Calculate observable self-reference [0,1]
    calculate_R_theory : Transform R_obs to theoretical coupling [1,3]
    calculate_D_eff : Calculate dimensional embedding (PCA-based)
    calculate_sigma : Calculate branching parameter (separate from D)
    """
    
    def __init__(
        self, 
        Phi_method: str = 'PSI',  # Changed to PSI for low-dimensional systems
        temporal_window: int = 100,
        D_max: float = 1.5,  # CALIBRATED: Empirical fit to Sleep-EDF data
        Phi_scale: float = 10.0,  # CALIBRATED: Geometric method scaling factor
        sfreq: float = 100.0  # Sampling frequency (Hz) for spectral D_eff
    ):
        self.Phi_method = Phi_method
        self.temporal_window = temporal_window
        self.D_max = D_max
        self.Phi_scale = Phi_scale
        self.sfreq = sfreq
    
    def calculate_C(
        self, 
        activity: np.ndarray,
        connectivity: Union[np.ndarray, csr_matrix],
        history: Optional[np.ndarray] = None
    ) -> Dict[str, float]:
        """
        Calculate full C(t) measure and components.
        
        CONSTITUTION COMPLIANT: C = Phi * R_theory * D_eff
        
        Parameters
        ----------
        activity : np.ndarray
            Current activity pattern (N,) or (N, T)
        connectivity : np.ndarray or csr_matrix
            Network connectivity matrix (N, N)
        history : np.ndarray, optional
            Historical activity for R calculation (N, T)
        
        Returns
        -------
        results : dict
            Dictionary with C, Phi, R_obs, R_theory, D_eff, sigma, and metadata
        """
        # Ensure 2D activity
        if activity.ndim == 1:
            activity = activity[:, np.newaxis]
        
        # Calculate components per Variable Constitution
        Phi = self.calculate_Phi(activity, connectivity)
        D_eff = self.calculate_D_eff(activity)
        sigma = self.calculate_sigma(activity, connectivity)
        
        # R requires history
        if history is not None:
            R_obs = self.calculate_R_obs(history)
            R_theory = self.calculate_R_theory(R_obs)
        else:
            R_obs = 0.0  # No self-reference observable
            R_theory = 1.0  # Baseline threshold
            warnings.warn("No history provided, setting R_obs=0, R_theory=1.0 (baseline)")
        
        # Calculate C(t) - PURE MULTIPLICATIVE per Constitution
        C = Phi * R_theory * D_eff
        
        return {
            'C': C,
            'Phi': Phi,
            'R_obs': R_obs,
            'R_theory': R_theory,
            'D_eff': D_eff,
            'sigma': sigma,
            'components': {
                'integration': Phi,
                'self_reference_coupling': R_theory,
                'dimensional_embedding': D_eff,
                'branching_parameter': sigma
            },
            'metadata': {
                'constitution_version': '1.0',
                'equation': 'C = Phi * R_theory * D_eff',
                'R_transform': 'R_theory = 1 + 2*R_obs',
                'criticality_status': 'subcritical' if sigma < 1 else 'supercritical' if sigma > 1 else 'critical'
            }
        }
    
    def calculate_Phi(
        self, 
        activity: np.ndarray,
        connectivity: Union[np.ndarray, csr_matrix],
        method: Optional[str] = None
    ) -> float:
        """
        Calculate integrated information Phi.
        
        Parameters
        ----------
        activity : np.ndarray
            Activity pattern (N,) or (N, T)
        connectivity : np.ndarray or csr_matrix
            Connectivity matrix (N, N)
        method : str, optional
            'geometric', 'stochastic', or 'PSI'
        
        Returns
        -------
        Phi : float
            Integrated information in bits, range [0, ~20]
        """
        method = method or self.Phi_method
        
        if method == 'geometric':
            Phi_raw = self._calculate_Phi_geometric(activity, connectivity)
            return Phi_raw * self.Phi_scale  # Apply empirical scaling
        elif method == 'stochastic':
            Phi_raw = self._calculate_Phi_stochastic(activity, connectivity)
            return Phi_raw * self.Phi_scale
        elif method == 'PSI':
            return self._calculate_Phi_PSI(activity, connectivity)
        elif method == 'LZC':
            return self._calculate_Phi_LZC(activity)
        else:
            raise ValueError(f"Unknown Phi method: {method}")
    
    def calculate_R_obs(self, activity_history: np.ndarray) -> float:
        """
        Calculate OBSERVABLE self-reference R_obs(t) via Lempel-Ziv Complexity.
        
        RECALIBRATED 2026-05-17: LZC measures distinct pattern count in
        binarized signal. HIGH for complex (wake), LOW for regular (sleep).
        
        CONSTITUTION: R_obs in [0, 1]
        """
        if activity_history.ndim == 1 or activity_history.shape[1] < 30:
            return 0.0
        
        N_ch, T = activity_history.shape
        
        # Downsample to ~300 points for speed (LZC is O(n²))
        step = max(1, T // 300)
        
        lzc_values = []
        for ch in range(N_ch):
            sig = activity_history[ch, ::step]
            
            # Binarize around median
            binary = (sig > np.median(sig)).astype(np.int8)
            
            # Lempel-Ziv complexity (fast version)
            lzc = self._lzc_fast(binary)
            
            # Normalize: random binary has LZC ≈ n / log2(n)
            n = len(binary)
            if n > 1:
                lzc_norm = lzc * np.log2(n) / n
            else:
                lzc_norm = 0.0
            
            lzc_values.append(lzc_norm)
        
        R_obs = float(np.mean(lzc_values))
        return np.clip(R_obs, 0.0, 1.0)
    
    @staticmethod
    def _lzc_fast(binary_seq):
        """Fast Lempel-Ziv complexity using string matching."""
        n = len(binary_seq)
        if n <= 1:
            return n
        
        s = ''.join(str(int(b)) for b in binary_seq)
        complexity = 1
        l = 1
        
        while l < n:
            # Find longest match of s[l:] in s[0:l]
            k = 1
            while l + k <= n:
                if s[l:l+k] in s[0:l+k-1]:
                    k += 1
                else:
                    break
            complexity += 1
            l += max(k, 1)
        
        return complexity
    
    def calculate_R_theory(self, R_obs: float) -> float:
        """
        Transform observable R to theoretical coupling parameter.
        
        CONSTITUTION LOCKED TRANSFORM:
        R_theory = 1 + 2 * R_obs
        
        Parameters
        ----------
        R_obs : float
            Observable self-reference in [0, 1]
        
        Returns
        -------
        R_theory : float
            Theoretical coupling in [1, 3]
        """
        # Locked transform per Variable Constitution v1.0
        R_theory = 1.0 + 2.0 * R_obs
        
        # Validate range
        if R_theory < 1.0 or R_theory > 3.0:
            warnings.warn(f"R_theory={R_theory:.3f} outside expected [1,3] range")
        
        return R_theory
    
    def calculate_D_eff(self, activity: np.ndarray) -> float:
        """
        Calculate effective dimensionality D_eff via spectral entropy.
        
        RECALIBRATED 2026-05-17: Replaced PCA participation ratio with
        spectral entropy. PCA-PR saturated at 1.0 for NREM stages due to
        only 3 EEG channels — provided zero discrimination.
        
        Spectral entropy is HIGH for flat/desynchronized spectra (wake)
        and LOW for peaked/synchronized spectra (deep sleep).
        
        CONSTITUTION: D_eff in [0, 1] (normalized)
        
        Parameters
        ----------
        activity : np.ndarray
            Activity pattern (N,) or (N, T)
        
        Returns
        -------
        D_eff : float
            Normalized spectral entropy in [0, 1]
        """
        if activity.ndim == 1:
            return 0.5  # Single timepoint — no spectral info, return neutral
        
        N, T = activity.shape
        
        if T < 8:
            return 0.5  # Too few samples for spectral estimate
        
        D_values = []
        for ch in range(N):
            try:
                nperseg = min(256, T)
                freqs, psd = welch(activity[ch], fs=self.sfreq, nperseg=nperseg)
                
                # Skip DC component (index 0)
                psd = psd[1:]
                
                if psd.sum() < 1e-20:
                    D_values.append(0.0)
                    continue
                
                # Normalize PSD to probability distribution
                psd_norm = psd / psd.sum()
                
                # Shannon entropy, normalized to [0, 1]
                se = entropy(psd_norm) / np.log(len(psd_norm))
                D_values.append(se)
            except Exception:
                D_values.append(0.5)
        
        if len(D_values) == 0:
            return 0.5
        
        D_eff = float(np.mean(D_values))
        return np.clip(D_eff, 0.0, 1.0)
    
    # --- OLD D_eff (PCA participation ratio) — removed 2026-05-17 ---
    # Saturated at 1.0 for all NREM stages with 3-channel EEG.
    # See RECALIBRATION_HANDOFF.md for full diagnosis.
    # def calculate_D_eff_pca(self, activity):
    #     ... (PCA participation ratio code) ...
    
    def calculate_sigma(
        self, 
        activity: np.ndarray,
        connectivity: Union[np.ndarray, csr_matrix]
    ) -> float:
        """
        Calculate branching parameter sigma(t).
        
        CONSTITUTION: sigma is SEPARATE from D_eff
        
        sigma = 1 is critical
        sigma < 1 is subcritical (activity decays)
        sigma > 1 is supercritical (activity grows)
        
        Parameters
        ----------
        activity : np.ndarray
            Activity pattern (N,) or (N, T)
        connectivity : np.ndarray or csr_matrix
            Connectivity matrix
        
        Returns
        -------
        sigma : float
            Branching parameter (0 to infinity, typically 0.8-1.2)
        """
        if activity.ndim == 2:
            activity = activity.mean(axis=1)
        
        # Calculate branching parameter from spectral radius
        sigma = self._calculate_branching_parameter(activity, connectivity)
        
        return sigma
    
    def _calculate_Phi_geometric(
        self, 
        activity: np.ndarray,
        connectivity: Union[np.ndarray, csr_matrix]
    ) -> float:
        """
        Geometric approximation of Phi (O(N^2)).
        
        Based on the geometric measure of integration.
        """
        if activity.ndim == 2:
            activity = activity.mean(axis=1)  # Average over time
        
        N = len(activity)
        
        # Binarize activity
        threshold = np.median(activity)
        binary_activity = (activity > threshold).astype(float)
        
        # Calculate effective connectivity
        if hasattr(connectivity, 'toarray'):
            W = connectivity.toarray()
        else:
            W = connectivity
        
        # System entropy
        p_active = binary_activity.sum() / N
        if p_active == 0 or p_active == 1:
            H_system = 0
        else:
            H_system = -p_active * np.log2(p_active) - (1-p_active) * np.log2(1-p_active)
        H_system *= N  # Total entropy
        
        # Partition into two random halves
        indices = np.random.permutation(N)
        half = N // 2
        part1, part2 = indices[:half], indices[half:2*half]
        
        # Entropy of parts
        H_part1 = self._calculate_entropy(binary_activity[part1])
        H_part2 = self._calculate_entropy(binary_activity[part2])
        
        # Mutual information
        MI = self._calculate_mutual_information(
            binary_activity[part1], 
            binary_activity[part2],
            W[np.ix_(part1, part2)]
        )
        
        # Phi is mutual information (already in bits)
        # BUG FIX: Don't divide by log(2), MI is already in bits
        Phi = MI
        
        return max(0, Phi)  # Ensure non-negative
    
    def _calculate_Phi_stochastic(
        self, 
        activity: np.ndarray,
        connectivity: Union[np.ndarray, csr_matrix],
        n_samples: int = 50
    ) -> float:
        """
        Stochastic approximation of Phi (O(N^2 * M)).
        
        Samples multiple partitions to estimate minimum information partition.
        """
        if activity.ndim == 2:
            activity = activity.mean(axis=1)
        
        N = len(activity)
        Phi_samples = []
        
        for _ in range(n_samples):
            # Random partition
            partition = np.random.rand(N) > 0.5
            part1 = np.where(partition)[0]
            part2 = np.where(~partition)[0]
            
            if len(part1) == 0 or len(part2) == 0:
                continue
            
            # Calculate Phi for this partition
            if hasattr(connectivity, 'toarray'):
                W = connectivity.toarray()
            else:
                W = connectivity
            
            MI = self._calculate_mutual_information(
                activity[part1],
                activity[part2],
                W[np.ix_(part1, part2)]
            )
            
            Phi_samples.append(MI)
        
        # Return minimum (most integrated partition)
        if len(Phi_samples) > 0:
            return max(0, min(Phi_samples))
        else:
            return 0.0
    
    def _calculate_Phi_PSI(
        self, 
        activity: np.ndarray,
        connectivity: Union[np.ndarray, csr_matrix]
    ) -> float:
        """
        Phi proxy via permutation entropy × cross-channel integration.
        
        RECALIBRATED 2026-05-17: Old PSI used temporal variance, which is
        HIGH for high-amplitude slow waves (deep sleep) — inverted.
        
        New approach:
        - Permutation entropy (PE) per channel: HIGH for complex/irregular
          signals (wake), LOW for regular oscillations (sleep).
        - Cross-channel coherence: integration between channels.
        - Phi = mean(PE) * coherence_factor
        
        Permutation entropy is well-validated as a consciousness proxy
        (Sitt et al. 2014, Schartner et al. 2015, King et al. 2013).
        """
        if activity.ndim == 1:
            activity = activity[:, np.newaxis]
        
        N, T = activity.shape
        
        if T < 10:
            return 0.5
        
        # Downsample to ~500 points for PE speed
        step = max(1, T // 500)
        activity_ds = activity[:, ::step]
        T_ds = activity_ds.shape[1]
        
        # 1. Permutation entropy per channel (order 3, fast)
        order = 3
        pe_values = []
        for ch in range(N):
            pe = self._permutation_entropy(activity_ds[ch], order=order)
            pe_values.append(pe)
        
        mean_pe = np.mean(pe_values) if pe_values else 0.5
        
        # 2. Cross-channel diversity: std of per-channel spectral entropies
        if N >= 2:
            se_per_ch = []
            for ch in range(N):
                try:
                    _, psd = welch(activity[ch], fs=self.sfreq, nperseg=min(256, T))
                    psd = psd[1:]
                    if psd.sum() > 1e-20:
                        psd_n = psd / psd.sum()
                        se_per_ch.append(entropy(psd_n) / np.log(len(psd_n)))
                except Exception:
                    pass
            # Diversity = how different the channels are (integration proxy)
            if len(se_per_ch) >= 2:
                coh_factor = 0.5 + np.std(se_per_ch)
            else:
                coh_factor = 0.5
        else:
            coh_factor = 0.5
        
        # Combine: PE captures differentiation, coherence captures integration
        # Scale to produce values in reasonable range for Phi
        Phi = mean_pe * (0.5 + coh_factor) * 2.0
        
        return max(0.0, float(Phi))
    
    def _permutation_entropy(self, x, order=3, delay=1):
        """
        Compute normalized permutation entropy — VECTORIZED.
        Returns value in [0, 1]: 1 = maximum complexity, 0 = fully regular.
        """
        n = len(x)
        if n < order * delay + 1:
            return 0.5
        
        # Vectorized: create all windows at once
        n_windows = n - (order - 1) * delay
        indices = np.arange(order) * delay
        windows = np.array([x[i + indices] for i in range(n_windows)])
        
        # Argsort all windows at once → rank patterns
        ranks = np.argsort(windows, axis=1)
        
        # Convert rank patterns to unique integers for fast counting
        # For order=3: pattern (0,1,2) → 0*6+1*2+2 = 4, etc.
        multipliers = np.array([np.math.factorial(order - 1 - i) for i in range(order)])
        pattern_ids = (ranks * multipliers).sum(axis=1)
        
        # Count occurrences
        _, counts = np.unique(pattern_ids, return_counts=True)
        probs = counts / counts.sum()
        
        # Shannon entropy normalized by max
        import math
        H = -np.sum(probs * np.log2(probs))
        max_H = math.log2(math.factorial(order))
        
        return H / max_H if max_H > 0 else 0.5
    
    def _calculate_Phi_LZC(self, activity: np.ndarray) -> float:
        """
        Phi via Lempel-Ziv Complexity (LZC).
        
        RECALIBRATED 2026-05-17 Round 3: Replaces PSI which was inverted
        (high for synchronized sleep). LZC is HIGH for complex/irregular
        signals (wake) and LOW for regular/periodic signals (deep sleep).
        
        Based on Casali et al. 2013 (Perturbational Complexity Index).
        Well-established in consciousness research and clinical DOC assessment.
        
        Returns Phi scaled by Phi_scale for compatibility with C equation.
        """
        if activity.ndim == 1:
            return 0.5 * self.Phi_scale
        
        N, T = activity.shape
        if T < 20:
            return 0.5 * self.Phi_scale
        
        lzc_values = []
        for ch in range(N):
            lzc = self._lempel_ziv_complexity(activity[ch])
            lzc_values.append(lzc)
        
        # Average LZC across channels, scale
        mean_lzc = float(np.mean(lzc_values))
        return mean_lzc * self.Phi_scale
    
    @staticmethod
    def _lempel_ziv_complexity(signal: np.ndarray) -> float:
        """
        Kaspar-Schuster Lempel-Ziv complexity, normalized to [0, 1].
        
        Higher for complex/irregular signals, lower for periodic/regular.
        """
        # Binarize around median
        median = np.median(signal)
        binary = ''.join(['1' if x > median else '0' for x in signal])
        
        n = len(binary)
        if n < 2:
            return 0.0
        
        # Kaspar-Schuster algorithm
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
        
        # Normalize: theoretical max complexity for random binary string
        norm = n / np.log2(n) if n > 1 else 1.0
        return c / norm
    
    def _calculate_branching_parameter(
        self, 
        activity: np.ndarray,
        connectivity: Union[np.ndarray, csr_matrix]
    ) -> float:
        """
        Calculate branching parameter from activity and connectivity.
        
        sigma = average number of spikes in next generation per spike
        """
        # Approximate using spectral radius of connectivity
        if hasattr(connectivity, 'toarray'):
            W = connectivity.toarray()
        else:
            W = connectivity
        
        # Power iteration for largest eigenvalue
        N = W.shape[0]
        v = np.random.rand(N)
        v = v / np.linalg.norm(v)
        
        for _ in range(20):
            v_new = W @ v
            norm = np.linalg.norm(v_new)
            if norm > 1e-10:
                v = v_new / norm
            else:
                break
        
        spectral_radius = norm
        
        # Weight by activity level
        activity_level = np.mean(activity > np.median(activity))
        
        sigma = spectral_radius * activity_level
        
        return sigma
    
    def _calculate_entropy(self, x: np.ndarray) -> float:
        """Calculate Shannon entropy of binary array."""
        if len(x) == 0:
            return 0.0
        p = np.mean(x)
        if p == 0 or p == 1:
            return 0.0
        return -p * np.log2(p) - (1-p) * np.log2(1-p)
    
    def _calculate_mutual_information(
        self, 
        x: np.ndarray, 
        y: np.ndarray,
        W_xy: np.ndarray
    ) -> float:
        """
        Calculate mutual information between two neuron groups.
        
        MI(X;Y) = H(X) + H(Y) - H(X,Y)
        
        NOTE: x and y are ALREADY binarized by caller
        """
        # x and y are already binary from _calculate_Phi_geometric
        # DO NOT binarize again or we lose all variance!
        x_bin = x.astype(int)
        y_bin = y.astype(int)
        
        # Individual entropies
        H_x = self._calculate_entropy(x_bin)
        H_y = self._calculate_entropy(y_bin)
        
        # Joint entropy (approximate)
        # Weight by connectivity strength
        w_total = np.abs(W_xy).sum()
        if w_total < 1e-10:
            return 0.0
        
        # Correlation coefficient (handle different-sized partitions)
        if len(x_bin) > 1 and len(y_bin) > 1 and len(x_bin) == len(y_bin):
            corr = np.abs(np.corrcoef(x_bin, y_bin)[0, 1])
        else:
            # Different sizes - use weighted connectivity as proxy
            corr = w_total / (len(x_bin) * len(y_bin) + 1e-10)
            corr = np.clip(corr, 0, 1)  # Ensure [0,1] range
        
        # Handle NaN from corrcoef (can happen with zero variance)
        if np.isnan(corr):
            corr = 0.0
        
        # Approximate joint entropy
        H_xy = H_x + H_y - corr * min(H_x, H_y)
        
        # MI
        MI = H_x + H_y - H_xy
        
        return max(0, MI)
    
    def _autocorrelation(self, x: np.ndarray, max_lag: int) -> np.ndarray:
        """Calculate autocorrelation function."""
        x = x - np.mean(x)
        c0 = np.dot(x, x) / len(x)
        
        if c0 < 1e-10:
            return np.zeros(max_lag)
        
        acf = []
        for lag in range(max_lag):
            if lag < len(x):
                c_lag = np.dot(x[:-lag or None], x[lag:]) / (len(x) - lag)
                acf.append(c_lag / c0)
            else:
                acf.append(0)
        
        return np.array(acf)


def calculate_avalanche_exponents(activity: np.ndarray) -> Dict[str, float]:
    """
    Calculate power-law exponents for avalanche statistics.
    
    Parameters
    ----------
    activity : np.ndarray
        Binary spike raster (N, T)
    
    Returns
    -------
    exponents : dict
        Dictionary with size and duration exponents
    """
    # Detect avalanches (continuous periods of activity)
    total_activity = activity.sum(axis=0)
    avalanches = []
    
    in_avalanche = False
    current_size = 0
    current_duration = 0
    
    for t in range(len(total_activity)):
        if total_activity[t] > 0:
            if not in_avalanche:
                in_avalanche = True
                current_size = 0
                current_duration = 0
            current_size += total_activity[t]
            current_duration += 1
        else:
            if in_avalanche:
                avalanches.append((current_size, current_duration))
                in_avalanche = False
    
    if len(avalanches) < 10:
        return {'size_exponent': np.nan, 'duration_exponent': np.nan}
    
    sizes, durations = zip(*avalanches)
    
    # Fit power laws (use log-log regression)
    # Size distribution: P(s) ~ s^(-tau)
    size_hist, size_bins = np.histogram(sizes, bins=20)
    size_hist = size_hist[size_hist > 0]
    size_bins = size_bins[:len(size_hist)]
    
    if len(size_hist) > 2:
        tau = -np.polyfit(np.log(size_bins), np.log(size_hist), 1)[0]
    else:
        tau = np.nan
    
    # Duration distribution: P(T) ~ T^(-alpha)
    dur_hist, dur_bins = np.histogram(durations, bins=15)
    dur_hist = dur_hist[dur_hist > 0]
    dur_bins = dur_bins[:len(dur_hist)]
    
    if len(dur_hist) > 2:
        alpha = -np.polyfit(np.log(dur_bins), np.log(dur_hist), 1)[0]
    else:
        alpha = np.nan
    
    return {
        'size_exponent': tau,
        'duration_exponent': alpha,
        'n_avalanches': len(avalanches)
    }
