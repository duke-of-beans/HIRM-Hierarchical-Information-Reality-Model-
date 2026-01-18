"""
Consciousness Measure Calculator
=================================

Calculate C(t) = Phi(t) * R(t) * [1 - exp(-lambda*D(t))]

Implements multiple methods for approximating integrated information (Phi),
measuring recursive depth (R), and distance from criticality (D).
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
    temporal_window : int, optional
        Number of timesteps to use for calculating R(t)
    
    Methods
    -------
    calculate_C : Calculate full C(t) measure
    calculate_Phi : Calculate integrated information
    calculate_R : Calculate recursive depth
    calculate_D : Calculate distance from criticality
    """
    
    def __init__(
        self, 
        lambda_param: float = 2.0,
        Phi_method: str = 'geometric',
        temporal_window: int = 100
    ):
        self.lambda_param = lambda_param
        self.Phi_method = Phi_method
        self.temporal_window = temporal_window
    
    def calculate_C(
        self, 
        activity: np.ndarray,
        connectivity: Union[np.ndarray, csr_matrix],
        history: Optional[np.ndarray] = None
    ) -> Dict[str, float]:
        """
        Calculate full C(t) measure and components.
        
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
            Dictionary with C, Phi, R, D, and their metadata
        """
        # Ensure 2D activity
        if activity.ndim == 1:
            activity = activity[:, np.newaxis]
        
        # Calculate components
        Phi = self.calculate_Phi(activity, connectivity)
        D = self.calculate_D(activity, connectivity)
        
        # R requires history
        if history is not None:
            R = self.calculate_R(history)
        else:
            R = 1.0  # Default for no history
            warnings.warn("No history provided, setting R=1.0")
        
        # Calculate C(t)
        C = Phi * R * (1 - np.exp(-self.lambda_param * D))
        
        return {
            'C': C,
            'Phi': Phi,
            'R': R,
            'D': D,
            'components': {
                'integration_term': Phi * R,
                'criticality_term': 1 - np.exp(-self.lambda_param * D)
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
            Integrated information in bits
        """
        method = method or self.Phi_method
        
        if method == 'geometric':
            return self._calculate_Phi_geometric(activity, connectivity)
        elif method == 'stochastic':
            return self._calculate_Phi_stochastic(activity, connectivity)
        elif method == 'PSI':
            return self._calculate_Phi_PSI(activity, connectivity)
        else:
            raise ValueError(f"Unknown Phi method: {method}")
    
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
        
        # Phi as effective information
        Phi = MI / np.log(2)  # Convert to bits
        
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
        """
        if activity.ndim == 2:
            activity = activity.mean(axis=1)
        
        N = len(activity)
        
        # Node diversity (entropy of activity distribution)
        hist, _ = np.histogram(activity, bins=10, density=True)
        hist = hist[hist > 0]
        H_nodes = -np.sum(hist * np.log2(hist + 1e-10))
        
        # Connection diversity
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
        PSI = np.sqrt(H_nodes * H_connections)
        
        return PSI
    
    def calculate_R(self, activity_history: np.ndarray) -> float:
        """
        Calculate recursive depth R(t) from temporal patterns.
        
        Parameters
        ----------
        activity_history : np.ndarray
            Historical activity patterns (N, T)
        
        Returns
        -------
        R : float
            Recursive depth measure (â‰¥ 1.0)
        """
        if activity_history.shape[1] < 10:
            return 1.0  # Insufficient history
        
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
        
        # R is related to decay rate of autocorrelation
        # Slower decay = more recursion = higher R
        if len(autocorr) > 1:
            decay_rate = -np.polyfit(range(len(autocorr)), 
                                     np.log(np.abs(autocorr) + 1e-10), 1)[0]
            R = 1.0 + np.exp(-decay_rate)  # Maps decay to R âˆˆ [1, ~3]
        else:
            R = 1.0
        
        return min(R, 3.0)  # Cap at reasonable maximum
    
    def calculate_D(
        self, 
        activity: np.ndarray,
        connectivity: Union[np.ndarray, csr_matrix]
    ) -> float:
        """
        Calculate distance from criticality D(t).
        
        Parameters
        ----------
        activity : np.ndarray
            Activity pattern (N,) or (N, T)
        connectivity : np.ndarray or csr_matrix
            Connectivity matrix
        
        Returns
        -------
        D : float
            Distance from criticality (0 = critical, >0 = sub/supercritical)
        """
        if activity.ndim == 2:
            activity = activity.mean(axis=1)
        
        # Calculate branching parameter
        branching = self._calculate_branching_parameter(activity, connectivity)
        
        # Distance from critical value (1.0)
        D = np.abs(branching - 1.0)
        
        return D
    
    def _calculate_branching_parameter(
        self, 
        activity: np.ndarray,
        connectivity: Union[np.ndarray, csr_matrix]
    ) -> float:
        """
        Calculate branching parameter from activity and connectivity.
        
        Ïƒ = average number of spikes in next generation per spike
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
        
        branching = spectral_radius * activity_level
        
        return branching
    
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
        """
        # Binarize
        x_bin = (x > np.median(x)).astype(int)
        y_bin = (y > np.median(y)).astype(int)
        
        # Individual entropies
        H_x = self._calculate_entropy(x_bin)
        H_y = self._calculate_entropy(y_bin)
        
        # Joint entropy (approximate)
        # Weight by connectivity strength
        w_total = np.abs(W_xy).sum()
        if w_total < 1e-10:
            return 0.0
        
        # Correlation coefficient
        corr = np.abs(np.corrcoef(x_bin, y_bin)[0, 1]) if len(x_bin) > 1 and len(y_bin) > 1 else 0
        
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
    # Size distribution: P(s) ~ s^(-Ï„)
    size_hist, size_bins = np.histogram(sizes, bins=20)
    size_hist = size_hist[size_hist > 0]
    size_bins = size_bins[:len(size_hist)]
    
    if len(size_hist) > 2:
        tau = -np.polyfit(np.log(size_bins), np.log(size_hist), 1)[0]
    else:
        tau = np.nan
    
    # Duration distribution: P(T) ~ T^(-Î±)
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
