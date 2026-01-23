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
        Phi_scale: float = 10.0  # CALIBRATED: Geometric method scaling factor
    ):
        self.Phi_method = Phi_method
        self.temporal_window = temporal_window
        self.D_max = D_max
        self.Phi_scale = Phi_scale
    
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
        else:
            raise ValueError(f"Unknown Phi method: {method}")
    
    def calculate_R_obs(self, activity_history: np.ndarray) -> float:
        """
        Calculate OBSERVABLE self-reference R_obs(t) from temporal patterns.
        
        CONSTITUTION: R_obs in [0, 1]
        
        This is a PROXY measure. Full clinical composite requires:
        R_obs = 0.35*R_PAC + 0.25*R_TC + 0.20*R_DMN + 0.20*R_LZC
        
        Current implementation uses autocorrelation as proxy for LZC component.
        
        Parameters
        ----------
        activity_history : np.ndarray
            Historical activity patterns (N, T)
        
        Returns
        -------
        R_obs : float
            Observable self-reference measure in [0, 1]
        """
        if activity_history.shape[1] < 10:
            return 0.0  # Insufficient history
        
        # Use only recent history
        T_window = min(self.temporal_window, activity_history.shape[1])
        recent = activity_history[:, -T_window:]
        
        # Calculate autocorrelation at multiple time scales
        max_lag = min(20, T_window // 2)
        autocorr = []
        
        for neuron_activity in recent:
            acf = self._autocorrelation(neuron_activity, max_lag)
            autocorr.append(acf)
        
        autocorr = np.array(autocorr).mean(axis=0)
        
        # Proxy for self-reference: slower decay = more self-modeling
        # Map to [0, 1] range
        if len(autocorr) > 1:
            # Area under autocorrelation curve as proxy
            R_proxy = np.sum(np.abs(autocorr)) / len(autocorr)
            R_obs = np.clip(R_proxy, 0.0, 1.0)
        else:
            R_obs = 0.0
        
        return R_obs
    
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
        Calculate dimensional embedding D_eff via PCA participation ratio.
        
        CONSTITUTION: D = D_eff in [0, 1] (normalized)
        
        Method: Participation ratio of eigenvalues
        D_eff = (sum lambda_i)^2 / sum(lambda_i^2)
        Then normalize: D = D_eff / D_max
        
        Parameters
        ----------
        activity : np.ndarray
            Activity pattern (N,) or (N, T)
        
        Returns
        -------
        D_eff : float
            Normalized dimensional embedding in [0, 1]
        """
        if activity.ndim == 1:
            # Single timepoint - limited dimensionality estimate
            # Use spread as proxy
            D_raw = 1.0
        else:
            # Multiple timepoints - can do PCA
            N, T = activity.shape
            
            if T < 3:
                D_raw = 1.0
            else:
                # Center data
                activity_centered = activity - activity.mean(axis=1, keepdims=True)
                
                # Covariance matrix
                cov = (activity_centered @ activity_centered.T) / T
                
                # Eigenvalues
                eigenvalues = np.linalg.eigvalsh(cov)
                eigenvalues = eigenvalues[eigenvalues > 1e-12]  # More lenient threshold
                
                if len(eigenvalues) == 0:
                    D_raw = 0.0
                else:
                    # Participation ratio
                    sum_eig = np.sum(eigenvalues)
                    sum_eig_sq = np.sum(eigenvalues**2)
                    
                    # BUG FIX: Eigenvalues from real EEG can be tiny (~10^-9)
                    # sum_eig_sq can be ~10^-18, so use relative threshold
                    if sum_eig_sq > 1e-20:
                        D_raw = (sum_eig**2) / sum_eig_sq
                    else:
                        D_raw = 0.0
        
        # Normalize to [0, 1]
        D_eff = D_raw / self.D_max
        D_eff = np.clip(D_eff, 0.0, 1.0)
        
        return D_eff
    
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
        Practical Simplicity Index (PSI).
        
        Fast approximation based on network complexity measures.
        FIXED: Properly handles temporal data (N, T) instead of collapsing to (N,)
        """
        # Handle temporal data properly
        if activity.ndim == 2:
            N, T = activity.shape
            # Use temporal variance as measure of node diversity
            node_vars = activity.var(axis=1)  # Variance across time for each node
            node_vars = node_vars / (node_vars.sum() + 1e-10)  # Normalize
            node_vars = node_vars[node_vars > 0]
            H_nodes = -np.sum(node_vars * np.log2(node_vars + 1e-10))
        else:
            # Single timepoint (static)
            N = len(activity)
            hist, _ = np.histogram(activity, bins=10, density=True)
            hist = hist[hist > 0]
            H_nodes = -np.sum(hist * np.log2(hist + 1e-10))
        
        # Connection diversity (same for both cases)
        if hasattr(connectivity, 'toarray'):
            W = connectivity.toarray()
        else:
            W = connectivity
        
        # Strength distribution
        strengths = np.abs(W).sum(axis=1)
        strengths = strengths / (strengths.sum() + 1e-10)
        strengths = strengths[strengths > 0]
        H_connections = -np.sum(strengths * np.log2(strengths + 1e-10))
        
        # PSI combines node and connection diversity
        # BUG FIX: Check for negative values before sqrt
        product = H_nodes * H_connections
        if product < 0:
            product = 0.0
        PSI = np.sqrt(product)
        
        # Handle NaN
        if np.isnan(PSI):
            PSI = 0.0
        
        return PSI
    
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
