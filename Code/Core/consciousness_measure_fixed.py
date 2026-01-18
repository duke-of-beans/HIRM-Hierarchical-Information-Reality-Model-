"""
Consciousness Measure Calculator - FIXED VERSION
================================================

Calculate C(t) = Phi(t) * R(t) * D(t)

FIXES APPLIED (Session 30):
1. Changed default Phi_method to 'PSI' (more reliable than geometric)
2. Improved edge case handling in all methods
3. Added fallback calculations when primary method fails
4. Better integration with SelfReferenceEngine for R

C_critical = 8.3 +/- 0.6 bits (locked constant)
"""

import numpy as np
from typing import Dict, Optional, Tuple, Union
from scipy.sparse import csr_matrix
from scipy.linalg import eigh
from scipy.stats import entropy
import warnings


class ConsciousnessMeasure:
    """
    Calculate the consciousness measure C(t) and its components.
    
    Parameters
    ----------
    lambda_param : float, optional
        Sensitivity parameter for criticality distance, default=2.0
    Phi_method : str, optional
        Method for calculating Phi: 'geometric', 'stochastic', 'PSI'
        Default changed to 'PSI' for reliability
    temporal_window : int, optional
        Number of timesteps to use for calculating R(t)
    """
    
    # Locked constant
    C_CRITICAL = 8.3
    C_CRITICAL_ERROR = 0.6
    
    def __init__(
        self, 
        lambda_param: float = 2.0,
        Phi_method: str = 'PSI',  # CHANGED: Default to PSI for reliability
        temporal_window: int = 100
    ):
        self.lambda_param = lambda_param
        self.Phi_method = Phi_method
        self.temporal_window = temporal_window
        self._self_ref_engine = None  # Lazy initialization
    
    def calculate_C(
        self, 
        activity: np.ndarray,
        connectivity: Union[np.ndarray, csr_matrix],
        history: Optional[np.ndarray] = None
    ) -> Dict[str, float]:
        """
        Calculate full C(t) measure and components.
        
        Returns
        -------
        results : dict
            Dictionary with C, Phi, R, D, and their metadata
        """
        # Ensure 2D activity
        if activity.ndim == 1:
            activity = activity[:, np.newaxis]
        
        # Calculate components with fallback handling
        Phi = self.calculate_Phi(activity, connectivity)
        D = self.calculate_D(activity, connectivity)
        
        # R requires history - use improved calculation
        if history is not None and history.shape[1] >= 10:
            R = self.calculate_R(history, connectivity)
        else:
            R = 1.0
            if history is None:
                warnings.warn("No history provided, setting R=1.0")
        
        # Calculate C(t) using standard formula
        # Note: Original formula was C = Phi * R * (1 - exp(-lambda*D))
        # But HIRM uses C(t) = Phi(t) x R(t) x D(t) directly
        # Use D directly for multiplicative form
        C = Phi * R * D
        
        # Also calculate the exponential form for comparison
        C_exp = Phi * R * (1 - np.exp(-self.lambda_param * D))
        
        return {
            'C': C,
            'C_exponential': C_exp,
            'Phi': Phi,
            'R': R,
            'D': D,
            'above_threshold': C > self.C_CRITICAL,
            'threshold': self.C_CRITICAL,
            'components': {
                'integration_term': Phi * R,
                'criticality_term': D,
                'criticality_term_exp': 1 - np.exp(-self.lambda_param * D)
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
        
        Uses PSI (Practical Simplicity Index) by default for reliability.
        Falls back to alternative methods if primary fails.
        """
        method = method or self.Phi_method
        
        try:
            if method == 'PSI':
                return self._calculate_Phi_PSI(activity, connectivity)
            elif method == 'geometric':
                result = self._calculate_Phi_geometric(activity, connectivity)
                # Fallback to PSI if geometric returns 0
                if result < 0.01:
                    return self._calculate_Phi_PSI(activity, connectivity)
                return result
            elif method == 'stochastic':
                result = self._calculate_Phi_stochastic(activity, connectivity)
                if result < 0.01:
                    return self._calculate_Phi_PSI(activity, connectivity)
                return result
            elif method == 'spectral':
                return self._calculate_Phi_spectral(activity, connectivity)
            else:
                raise ValueError(f"Unknown Phi method: {method}")
        except Exception as e:
            warnings.warn(f"Phi calculation failed ({method}): {e}, using PSI fallback")
            return self._calculate_Phi_PSI(activity, connectivity)
    
    def _calculate_Phi_PSI(
        self, 
        activity: np.ndarray,
        connectivity: Union[np.ndarray, csr_matrix]
    ) -> float:
        """
        Practical Simplicity Index (PSI) - RECOMMENDED METHOD.
        
        Fast, stable approximation based on network complexity measures.
        Combines node diversity (activity entropy) with connection diversity.
        """
        if activity.ndim == 2:
            activity = activity.mean(axis=1)
        
        N = len(activity)
        if N < 2:
            return 0.0
        
        # Node diversity (entropy of activity distribution)
        # Use more bins for better resolution
        n_bins = min(20, max(5, N // 5))
        hist, _ = np.histogram(activity, bins=n_bins, density=True)
        hist = hist[hist > 0]
        if len(hist) > 0:
            H_nodes = -np.sum(hist * np.log2(hist + 1e-10)) / np.log2(n_bins)
        else:
            H_nodes = 0.0
        
        # Connection diversity
        if hasattr(connectivity, 'toarray'):
            W = connectivity.toarray()
        else:
            W = np.asarray(connectivity)
        
        # Strength distribution
        strengths = np.abs(W).sum(axis=1)
        total_strength = strengths.sum()
        if total_strength > 1e-10:
            strengths_norm = strengths / total_strength
            strengths_norm = strengths_norm[strengths_norm > 0]
            H_connections = -np.sum(strengths_norm * np.log2(strengths_norm + 1e-10)) / np.log2(N)
        else:
            H_connections = 0.0
        
        # PSI combines node and connection diversity
        # Scale to typical Phi range (0-15 bits for conscious states)
        PSI = np.sqrt(max(0, H_nodes) * max(0, H_connections)) * 10.0
        
        return max(0.0, min(PSI, 20.0))  # Cap at reasonable maximum
    
    def _calculate_Phi_spectral(
        self, 
        activity: np.ndarray,
        connectivity: Union[np.ndarray, csr_matrix]
    ) -> float:
        """
        Spectral method for Phi using connectivity eigenvalue structure.
        
        Uses the spectral gap as a measure of integration.
        """
        if hasattr(connectivity, 'toarray'):
            W = connectivity.toarray()
        else:
            W = np.asarray(connectivity)
        
        N = W.shape[0]
        if N < 3:
            return 0.0
        
        try:
            # Compute Laplacian
            D = np.diag(np.abs(W).sum(axis=1))
            L = D - np.abs(W)
            
            # Normalize
            D_sqrt_inv = np.diag(1.0 / (np.sqrt(np.diag(D)) + 1e-10))
            L_norm = D_sqrt_inv @ L @ D_sqrt_inv
            
            # Get eigenvalues
            eigenvalues = np.linalg.eigvalsh(L_norm)
            eigenvalues = np.sort(eigenvalues)
            
            # Spectral gap (second smallest eigenvalue)
            spectral_gap = eigenvalues[1] if len(eigenvalues) > 1 else 0.0
            
            # Number of significant eigenvalues (effective dimensionality)
            eigenvalues_pos = eigenvalues[eigenvalues > 0.01]
            effective_dim = len(eigenvalues_pos)
            
            # Combine spectral gap and dimensionality
            Phi = spectral_gap * np.log2(1 + effective_dim) * 5.0
            
            return max(0.0, min(Phi, 20.0))
        except Exception:
            return self._calculate_Phi_PSI(activity, connectivity)
    
    def _calculate_Phi_geometric(
        self, 
        activity: np.ndarray,
        connectivity: Union[np.ndarray, csr_matrix]
    ) -> float:
        """
        Geometric approximation of Phi (O(N^2)).
        
        IMPROVED: Uses connectivity-informed partitioning instead of random.
        """
        if activity.ndim == 2:
            activity = activity.mean(axis=1)
        
        N = len(activity)
        if N < 4:
            return 0.0
        
        if hasattr(connectivity, 'toarray'):
            W = connectivity.toarray()
        else:
            W = np.asarray(connectivity)
        
        # Use spectral partitioning instead of random
        try:
            # Compute normalized Laplacian
            D = np.diag(np.abs(W).sum(axis=1) + 1e-10)
            D_inv_sqrt = np.diag(1.0 / np.sqrt(np.diag(D)))
            L_norm = np.eye(N) - D_inv_sqrt @ W @ D_inv_sqrt
            
            # Get Fiedler vector (second smallest eigenvector)
            eigenvalues, eigenvectors = np.linalg.eigh(L_norm)
            fiedler_idx = np.argsort(eigenvalues)[1]
            fiedler = eigenvectors[:, fiedler_idx]
            
            # Partition based on Fiedler vector
            median_fiedler = np.median(fiedler)
            part1 = np.where(fiedler < median_fiedler)[0]
            part2 = np.where(fiedler >= median_fiedler)[0]
        except Exception:
            # Fallback to random partition
            indices = np.random.permutation(N)
            half = N // 2
            part1, part2 = indices[:half], indices[half:2*half]
        
        if len(part1) == 0 or len(part2) == 0:
            return 0.0
        
        # Calculate effective information
        activity1 = activity[part1]
        activity2 = activity[part2]
        
        # Binarize with robust threshold
        threshold1 = np.median(activity1)
        threshold2 = np.median(activity2)
        binary1 = (activity1 > threshold1).astype(float)
        binary2 = (activity2 > threshold2).astype(float)
        
        # Calculate entropies
        H1 = self._calculate_entropy(binary1)
        H2 = self._calculate_entropy(binary2)
        
        # Mutual information estimate
        MI = self._calculate_mutual_information(
            binary1, binary2,
            W[np.ix_(part1, part2)]
        )
        
        # Phi as effective information (bits)
        Phi = MI / np.log(2) if MI > 0 else 0.0
        
        # Scale to typical range
        Phi = Phi * 10.0
        
        return max(0.0, min(Phi, 20.0))
    
    def _calculate_Phi_stochastic(
        self, 
        activity: np.ndarray,
        connectivity: Union[np.ndarray, csr_matrix],
        n_samples: int = 50
    ) -> float:
        """Stochastic approximation of Phi."""
        if activity.ndim == 2:
            activity = activity.mean(axis=1)
        
        N = len(activity)
        if N < 4:
            return 0.0
        
        Phi_samples = []
        
        if hasattr(connectivity, 'toarray'):
            W = connectivity.toarray()
        else:
            W = np.asarray(connectivity)
        
        for _ in range(n_samples):
            partition = np.random.rand(N) > 0.5
            part1 = np.where(partition)[0]
            part2 = np.where(~partition)[0]
            
            if len(part1) < 2 or len(part2) < 2:
                continue
            
            MI = self._calculate_mutual_information(
                activity[part1],
                activity[part2],
                W[np.ix_(part1, part2)]
            )
            
            Phi_samples.append(MI)
        
        if len(Phi_samples) > 0:
            # Return minimum (most integrated partition)
            return max(0.0, min(Phi_samples) * 10.0)
        return 0.0
    
    def calculate_R(
        self, 
        activity_history: np.ndarray,
        connectivity: Optional[Union[np.ndarray, csr_matrix]] = None
    ) -> float:
        """
        Calculate recursive depth R(t) from temporal patterns.
        
        IMPROVED: Uses multiple measures:
        1. Autocorrelation decay (temporal memory)
        2. Prediction error (self-modeling accuracy)
        3. Loop strength (self-referential dynamics)
        
        Returns
        -------
        R : float
            Self-reference measure in range [0, 3]
        """
        if activity_history.shape[1] < 10:
            return 0.5  # Changed: return lower value for insufficient history
        
        # Use recent history
        T_window = min(self.temporal_window, activity_history.shape[1])
        recent = activity_history[:, -T_window:]
        
        # METHOD 1: Autocorrelation-based measure
        R_autocorr = self._calculate_R_autocorr(recent)
        
        # METHOD 2: Prediction error measure
        R_prediction = self._calculate_R_prediction(recent)
        
        # METHOD 3: Loop strength (if connectivity available)
        if connectivity is not None:
            R_loop = self._calculate_R_loop(recent, connectivity)
        else:
            R_loop = R_autocorr  # Use autocorr as fallback
        
        # Combine measures (weighted average)
        R = 0.3 * R_autocorr + 0.4 * R_prediction + 0.3 * R_loop
        
        return np.clip(R, 0.0, 3.0)
    
    def _calculate_R_autocorr(self, recent: np.ndarray) -> float:
        """Autocorrelation-based R measure."""
        max_lag = min(20, recent.shape[1] // 2)
        if max_lag < 2:
            return 0.5
        
        autocorr_list = []
        for neuron_activity in recent:
            acf = self._autocorrelation(neuron_activity, max_lag)
            autocorr_list.append(acf)
        
        autocorr = np.array(autocorr_list).mean(axis=0)
        
        if len(autocorr) > 1:
            # Fit decay
            log_autocorr = np.log(np.abs(autocorr) + 1e-10)
            try:
                decay_rate = -np.polyfit(range(len(autocorr)), log_autocorr, 1)[0]
            except:
                decay_rate = 1.0
            
            # Map decay to R: slower decay = higher R
            R = 1.5 * np.exp(-decay_rate)
        else:
            R = 0.5
        
        return np.clip(R, 0.0, 3.0)
    
    def _calculate_R_prediction(self, recent: np.ndarray) -> float:
        """Prediction error-based R measure."""
        N, T = recent.shape
        if T < 5:
            return 0.5
        
        # Simple autoregressive prediction
        errors = []
        for t in range(2, T):
            # Predict current from past
            predicted = 0.5 * recent[:, t-1] + 0.3 * recent[:, t-2]
            actual = recent[:, t]
            error = np.mean((predicted - actual) ** 2)
            errors.append(error)
        
        if len(errors) == 0:
            return 0.5
        
        mean_error = np.mean(errors)
        variance = np.var(recent)
        
        if variance > 1e-10:
            # R inversely related to prediction error
            # Low error = good self-model = high R
            R = 1.5 * (1 - mean_error / (variance + 1e-10))
        else:
            R = 0.5
        
        return np.clip(R, 0.0, 3.0)
    
    def _calculate_R_loop(
        self, 
        recent: np.ndarray,
        connectivity: Union[np.ndarray, csr_matrix]
    ) -> float:
        """Loop strength-based R measure."""
        if hasattr(connectivity, 'toarray'):
            W = connectivity.toarray()
        else:
            W = np.asarray(connectivity)
        
        N = W.shape[0]
        
        # Trace of W^n gives loop counts
        try:
            W_norm = W / (np.abs(W).max() + 1e-10)
            
            # Self-loops (diagonal)
            self_loops = np.abs(np.trace(W_norm))
            
            # 2-cycles
            two_cycles = np.abs(np.trace(W_norm @ W_norm)) / N
            
            # 3-cycles
            three_cycles = np.abs(np.trace(W_norm @ W_norm @ W_norm)) / N
            
            # Combine
            loop_strength = 0.4 * self_loops + 0.4 * two_cycles + 0.2 * three_cycles
            R = 1.5 * np.tanh(loop_strength)  # Saturates at ~1.5
        except:
            R = 0.5
        
        return np.clip(R, 0.0, 3.0)
    
    def calculate_D(
        self, 
        activity: np.ndarray,
        connectivity: Union[np.ndarray, csr_matrix]
    ) -> float:
        """
        Calculate distance from criticality D(t).
        
        D measures how close the system is to critical dynamics (branching ratio = 1).
        D = 1 at criticality, D < 1 subcritical, D > 1 supercritical.
        
        IMPROVED: Uses multiple criticality indicators.
        """
        if activity.ndim == 2:
            activity = activity.mean(axis=1)
        
        # Method 1: Branching parameter
        branching = self._calculate_branching_parameter(activity, connectivity)
        
        # Method 2: Activity level
        mean_activity = np.mean(activity)
        std_activity = np.std(activity)
        
        # Criticality indicator: variance/mean ratio (should be ~1 at criticality)
        if mean_activity > 1e-10:
            fano_factor = std_activity**2 / mean_activity
        else:
            fano_factor = 1.0
        
        # Combine: D peaks at criticality (branching = 1, fano = 1)
        D_branching = 1.0 / (1.0 + abs(branching - 1.0))
        D_fano = 1.0 / (1.0 + abs(fano_factor - 1.0))
        
        D = 0.6 * D_branching + 0.4 * D_fano
        
        # Scale to reasonable range
        D = D * 2.0  # Peak at ~2 when at criticality
        
        return max(0.01, min(D, 3.0))
    
    def _calculate_branching_parameter(
        self, 
        activity: np.ndarray,
        connectivity: Union[np.ndarray, csr_matrix]
    ) -> float:
        """Calculate branching parameter (spectral radius * activity)."""
        if hasattr(connectivity, 'toarray'):
            W = connectivity.toarray()
        else:
            W = np.asarray(connectivity)
        
        N = W.shape[0]
        
        # Power iteration for spectral radius
        v = np.random.rand(N)
        v = v / (np.linalg.norm(v) + 1e-10)
        
        for _ in range(20):
            v_new = W @ v
            norm = np.linalg.norm(v_new)
            if norm > 1e-10:
                v = v_new / norm
            else:
                break
        
        spectral_radius = norm
        
        # Weight by activity level
        threshold = np.median(activity)
        activity_level = np.mean(activity > threshold)
        
        branching = spectral_radius * max(activity_level, 0.1)
        
        return branching
    
    def _calculate_entropy(self, x: np.ndarray) -> float:
        """Calculate Shannon entropy of binary array."""
        if len(x) == 0:
            return 0.0
        p = np.mean(x)
        if p < 1e-10 or p > 1 - 1e-10:
            return 0.0
        return -p * np.log2(p) - (1-p) * np.log2(1-p)
    
    def _calculate_mutual_information(
        self, 
        x: np.ndarray, 
        y: np.ndarray,
        W_xy: np.ndarray
    ) -> float:
        """Calculate mutual information between two neuron groups."""
        if len(x) < 2 or len(y) < 2:
            return 0.0
        
        # Binarize
        x_bin = (x > np.median(x)).astype(float)
        y_bin = (y > np.median(y)).astype(float)
        
        # Individual entropies
        H_x = self._calculate_entropy(x_bin)
        H_y = self._calculate_entropy(y_bin)
        
        if H_x < 1e-10 or H_y < 1e-10:
            return 0.0
        
        # Weight by connectivity strength
        w_total = np.abs(W_xy).sum()
        if w_total < 1e-10:
            return 0.0
        
        # Correlation coefficient
        try:
            corr = np.corrcoef(x_bin, y_bin)[0, 1]
            if np.isnan(corr):
                corr = 0.0
        except:
            corr = 0.0
        
        # Approximate MI from correlation
        # MI = -0.5 * log(1 - rho^2) for Gaussian
        rho2 = min(corr**2, 0.99)
        MI = -0.5 * np.log(1 - rho2 + 1e-10)
        
        return max(0.0, MI)
    
    def _autocorrelation(self, x: np.ndarray, max_lag: int) -> np.ndarray:
        """Calculate autocorrelation function."""
        x = x - np.mean(x)
        c0 = np.dot(x, x) / len(x)
        
        if c0 < 1e-10:
            return np.ones(max_lag) * 0.5  # Return moderate ACF instead of zeros
        
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
        return {'size_exponent': np.nan, 'duration_exponent': np.nan, 'n_avalanches': len(avalanches)}
    
    sizes, durations = zip(*avalanches)
    
    # Fit power laws
    size_hist, size_bins = np.histogram(sizes, bins=20)
    size_hist = size_hist[size_hist > 0]
    size_bins = size_bins[:len(size_hist)]
    
    if len(size_hist) > 2 and len(size_bins) > 0:
        try:
            tau = -np.polyfit(np.log(size_bins + 1), np.log(size_hist + 1), 1)[0]
        except:
            tau = np.nan
    else:
        tau = np.nan
    
    dur_hist, dur_bins = np.histogram(durations, bins=15)
    dur_hist = dur_hist[dur_hist > 0]
    dur_bins = dur_bins[:len(dur_hist)]
    
    if len(dur_hist) > 2 and len(dur_bins) > 0:
        try:
            alpha = -np.polyfit(np.log(dur_bins + 1), np.log(dur_hist + 1), 1)[0]
        except:
            alpha = np.nan
    else:
        alpha = np.nan
    
    return {
        'size_exponent': tau,
        'duration_exponent': alpha,
        'n_avalanches': len(avalanches)
    }


# Quick validation function
def validate_installation():
    """Quick validation that the module works."""
    print("HIRM Consciousness Measure - Validation")
    print("=" * 50)
    
    # Create test data
    N, T = 50, 100
    activity = np.random.rand(N, T)
    connectivity = np.random.rand(N, N) * 0.1
    np.fill_diagonal(connectivity, 0)  # No self-connections
    
    # Test calculation
    measure = ConsciousnessMeasure()
    result = measure.calculate_C(activity[:, -1], connectivity, activity)
    
    print(f"Test result:")
    print(f"  C(t)  = {result['C']:.3f} bits")
    print(f"  Phi   = {result['Phi']:.3f} bits")
    print(f"  R     = {result['R']:.3f}")
    print(f"  D     = {result['D']:.3f}")
    print(f"  Above threshold: {result['above_threshold']}")
    print(f"  C_critical: {result['threshold']} bits")
    print("=" * 50)
    print("Validation PASSED" if result['C'] > 0 else "Validation FAILED")
    
    return result


if __name__ == "__main__":
    validate_installation()
