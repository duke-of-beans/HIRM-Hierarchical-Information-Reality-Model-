"""
Consciousness Measure C(t) Calculator

Implements C(t) = Phi(t) * R(t) * [1 - exp(-lambda*D(t))]

Where:
- Phi(t): Integrated information (bits)
- R(t): Recursive depth (dimensionless)
- D(t): Inverse distance from criticality (dimensionless)
- lambda: Tuning parameter
"""

import numpy as np
from typing import Optional, Tuple, Dict
from scipy.spatial.distance import pdist, squareform
from scipy.special import xlogy
from sklearn.metrics import mutual_info_score


class ConsciousnessMeasure:
    """
    Calculate consciousness measure C(t) from neural activity.
    
    Parameters
    ----------
    lambda_param : float
        Criticality sensitivity parameter (default: 5.0)
    Phi_method : str
        Method for Phi approximation: 'geometric', 'stochastic', 'psi'
    seed : int, optional
        Random seed for stochastic methods
    """
    
    def __init__(self, lambda_param: float = 5.0, 
                 Phi_method: str = 'geometric',
                 seed: Optional[int] = None):
        self.lambda_param = lambda_param
        self.Phi_method = Phi_method
        self.seed = seed
        
        if seed is not None:
            np.random.seed(seed)
    
    def calculate_Phi(self, activity: np.ndarray, 
                     connectivity: np.ndarray,
                     **kwargs) -> float:
        """
        Calculate integrated information Phi.
        
        Parameters
        ----------
        activity : np.ndarray
            Current activity pattern (N neurons)
        connectivity : np.ndarray
            Connectivity matrix (NxN)
        **kwargs
            Method-specific parameters
        
        Returns
        -------
        float
            Integrated information in bits
        """
        if self.Phi_method == 'geometric':
            return self._Phi_geometric(activity, connectivity)
        elif self.Phi_method == 'stochastic':
            n_samples = kwargs.get('n_samples', 100)
            return self._Phi_stochastic(activity, connectivity, n_samples)
        elif self.Phi_method == 'psi':
            return self._Phi_PSI(activity, connectivity)
        else:
            raise ValueError(f"Unknown Phi method: {self.Phi_method}")
    
    def _Phi_geometric(self, activity: np.ndarray, 
                       connectivity: np.ndarray) -> float:
        """
        Geometric measure of integration.
        
        Approximates Phi using mutual information between subsystems.
        Complexity: O(N^2)
        """
        N = len(activity)
        
        if N < 2:
            return 0.0
        
        # Binarize activity
        binary_activity = (activity > activity.mean()).astype(int)
        
        # Calculate pairwise mutual information
        MI_total = 0.0
        count = 0
        
        for i in range(N):
            for j in range(i+1, N):
                if connectivity[i, j] > 0:
                    mi = self._mutual_information(
                        binary_activity[i:i+1],
                        binary_activity[j:j+1]
                    )
                    MI_total += mi
                    count += 1
        
        if count == 0:
            return 0.0
        
        # Normalize
        Phi = MI_total / count
        
        # Scale by network integration measure
        integration_factor = self._measure_integration(connectivity)
        
        return Phi * integration_factor
    
    def _Phi_stochastic(self, activity: np.ndarray, 
                        connectivity: np.ndarray,
                        n_samples: int) -> float:
        """
        Stochastic approximation using random bipartitions.
        
        Complexity: O(N^2 * M) where M = n_samples
        """
        N = len(activity)
        
        if N < 2:
            return 0.0
        
        binary_activity = (activity > activity.mean()).astype(int)
        
        min_info_loss = np.inf
        
        for _ in range(n_samples):
            # Random bipartition
            partition = np.random.rand(N) < 0.5
            
            if partition.sum() == 0 or partition.sum() == N:
                continue
            
            # Information loss from partition
            info_loss = self._bipartition_info_loss(
                binary_activity, connectivity, partition
            )
            
            min_info_loss = min(min_info_loss, info_loss)
        
        return min_info_loss if min_info_loss < np.inf else 0.0
    
    def _Phi_PSI(self, activity: np.ndarray, 
                 connectivity: np.ndarray) -> float:
        """
        Practical Simplicity Index (PSI).
        
        Fast approximation based on network structure.
        """
        N = len(activity)
        
        # Average activity
        mean_activity = activity.mean()
        
        # Effective connectivity (weighted by activity)
        effective_conn = connectivity * np.outer(activity, activity)
        
        # Information content
        H = -xlogy(mean_activity, mean_activity) - xlogy(1-mean_activity, 1-mean_activity)
        H = np.nan_to_num(H)
        
        # Integration measure
        integration = effective_conn.sum() / (N * (N-1))
        
        return H * integration * N / np.log(2)  # Convert to bits
    
    def calculate_R(self, activity_history: np.ndarray,
                   max_depth: int = 5) -> float:
        """
        Calculate recursive depth R(t).
        
        Measures depth of self-referential processing from temporal patterns.
        
        Parameters
        ----------
        activity_history : np.ndarray
            History of activity patterns (T x N)
        max_depth : int
            Maximum recursion depth to test
        
        Returns
        -------
        float
            Recursive depth (dimensionless)
        """
        if len(activity_history) < 2:
            return 0.0
        
        # Calculate autocorrelation at different lags
        autocorr_depths = []
        
        for depth in range(1, min(max_depth + 1, len(activity_history) // 2)):
            autocorr = self._pattern_autocorrelation(activity_history, depth)
            autocorr_depths.append(autocorr * depth)  # Weight by depth
        
        if len(autocorr_depths) == 0:
            return 0.0
        
        # Recursive depth is weighted sum of correlations
        R = np.sum(autocorr_depths)
        
        return R
    
    def _pattern_autocorrelation(self, history: np.ndarray, lag: int) -> float:
        """Calculate pattern autocorrelation at given lag."""
        if len(history) < lag + 1:
            return 0.0
        
        # Spatial patterns at different times
        pattern1 = history[:-lag].flatten()
        pattern2 = history[lag:].flatten()
        
        # Correlation
        if pattern1.std() > 0 and pattern2.std() > 0:
            corr = np.corrcoef(pattern1, pattern2)[0, 1]
            return max(0, corr)  # Only positive correlations
        else:
            return 0.0
    
    def calculate_D(self, activity: np.ndarray,
                   connectivity: Optional[np.ndarray] = None,
                   activity_history: Optional[np.ndarray] = None) -> float:
        """
        Calculate inverse distance from criticality D(t).
        
        Uses multiple indicators:
        - Branching parameter
        - Avalanche statistics (if history available)
        - Variance measures
        
        Parameters
        ----------
        activity : np.ndarray
            Current activity pattern
        connectivity : np.ndarray, optional
            Network connectivity
        activity_history : np.ndarray, optional
            Recent activity history for avalanche analysis
        
        Returns
        -------
        float
            Inverse distance from criticality (0 = far, 1 = critical)
        """
        D_components = []
        
        # Component 1: Activity variance
        if activity.std() > 0:
            # Critical systems have specific variance scaling
            normalized_variance = min(activity.var(), 1.0)
            D_components.append(normalized_variance)
        
        # Component 2: Branching parameter (if history available)
        if activity_history is not None and len(activity_history) > 1:
            sigma = self._branching_parameter(activity_history)
            # sigma = 1 is critical
            D_branching = 1.0 - abs(sigma - 1.0)
            D_branching = max(0, D_branching)
            D_components.append(D_branching)
        
        # Component 3: Connectivity eigenvalue spectrum (if available)
        if connectivity is not None:
            try:
                eigenvalues = np.linalg.eigvals(connectivity)
                spectral_radius = np.abs(eigenvalues).max()
                # Critical at spectral radius ~ 1
                D_spectral = 1.0 - abs(spectral_radius - 1.0)
                D_spectral = max(0, min(1, D_spectral))
                D_components.append(D_spectral)
            except:
                pass
        
        if len(D_components) == 0:
            return 0.0
        
        return np.mean(D_components)
    
    def _branching_parameter(self, history: np.ndarray) -> float:
        """
        Estimate branching parameter sigma.
        
        sigma = (spikes at t+1) / (spikes at t)
        """
        if len(history) < 2:
            return 0.0
        
        spike_counts = history.sum(axis=1)
        
        # Avoid division by zero
        valid_mask = spike_counts[:-1] > 0
        if valid_mask.sum() == 0:
            return 0.0
        
        ratios = spike_counts[1:][valid_mask] / spike_counts[:-1][valid_mask]
        sigma = np.mean(ratios)
        
        return sigma
    
    def calculate_C(self, activity: np.ndarray, 
                   connectivity: np.ndarray,
                   activity_history: np.ndarray,
                   **kwargs) -> Tuple[float, Dict]:
        """
        Calculate full consciousness measure C(t).
        
        C(t) = Phi(t) * R(t) * [1 - exp(-lambda * D(t))]
        
        Parameters
        ----------
        activity : np.ndarray
            Current activity pattern
        connectivity : np.ndarray
            Network connectivity matrix
        activity_history : np.ndarray
            Recent activity history
        **kwargs
            Additional parameters for component calculations
        
        Returns
        -------
        C : float
            Consciousness measure in bits
        components : dict
            Individual components (Phi, R, D) for analysis
        """
        # Calculate components
        Phi = self.calculate_Phi(activity, connectivity, **kwargs)
        R = self.calculate_R(activity_history, max_depth=kwargs.get('max_depth', 5))
        D = self.calculate_D(activity, connectivity, activity_history)
        
        # Full measure
        criticality_factor = 1.0 - np.exp(-self.lambda_param * D)
        C = Phi * R * criticality_factor
        
        components = {
            'Phi': Phi,
            'R': R,
            'D': D,
            'criticality_factor': criticality_factor
        }
        
        return C, components
    
    def _mutual_information(self, X: np.ndarray, Y: np.ndarray) -> float:
        """Calculate mutual information between two variables."""
        # Discretize if needed
        X_discrete = (X > X.mean()).astype(int).flatten()
        Y_discrete = (Y > Y.mean()).astype(int).flatten()
        
        if len(X_discrete) < 2:
            return 0.0
        
        try:
            mi = mutual_info_score(X_discrete, Y_discrete)
            return mi
        except:
            return 0.0
    
    def _measure_integration(self, connectivity: np.ndarray) -> float:
        """
        Measure network integration.
        
        Uses global efficiency and modularity metrics.
        """
        N = len(connectivity)
        
        # Normalize connectivity
        W = connectivity.copy()
        if W.max() > 0:
            W = W / W.max()
        
        # Path length measure (simplified)
        # Higher connectivity -> higher integration
        density = W.sum() / (N * (N - 1))
        
        # Clustering coefficient
        clustering = self._clustering_coefficient(W)
        
        # Integration combines density and clustering
        integration = np.sqrt(density * clustering)
        
        return integration
    
    def _clustering_coefficient(self, W: np.ndarray) -> float:
        """Calculate average clustering coefficient."""
        N = len(W)
        clustering_sum = 0.0
        
        for i in range(N):
            neighbors = np.where(W[i, :] > 0)[0]
            k = len(neighbors)
            
            if k < 2:
                continue
            
            # Count triangles
            triangles = 0
            for j in range(len(neighbors)):
                for m in range(j+1, len(neighbors)):
                    if W[neighbors[j], neighbors[m]] > 0:
                        triangles += 1
            
            # Clustering coefficient for node i
            clustering_sum += 2 * triangles / (k * (k - 1))
        
        return clustering_sum / N if N > 0 else 0.0
    
    def _bipartition_info_loss(self, activity: np.ndarray,
                               connectivity: np.ndarray,
                               partition: np.ndarray) -> float:
        """Calculate information loss from bipartition."""
        # Simplified: measure cross-partition connectivity
        cross_connections = connectivity[partition, :][:, ~partition].sum()
        total_connections = connectivity.sum()
        
        if total_connections == 0:
            return 0.0
        
        info_loss = cross_connections / total_connections
        
        return info_loss


def measure_branching_parameter(spike_history: np.ndarray) -> float:
    """
    Measure branching parameter from spike history.
    
    Parameters
    ----------
    spike_history : np.ndarray
        T x N array of spike patterns
    
    Returns
    -------
    float
        Branching parameter sigma
    """
    spike_counts = spike_history.sum(axis=1)
    
    valid_mask = spike_counts[:-1] > 0
    if valid_mask.sum() == 0:
        return 0.0
    
    ratios = spike_counts[1:][valid_mask] / spike_counts[:-1][valid_mask]
    sigma = np.mean(ratios)
    
    return sigma


def measure_avalanche_exponents(spike_history: np.ndarray,
                                min_avalanche_size: int = 2) -> Dict[str, float]:
    """
    Measure power-law exponents for neuronal avalanches.
    
    Parameters
    ----------
    spike_history : np.ndarray
        T x N array of spike patterns
    min_avalanche_size : int
        Minimum avalanche size to consider
    
    Returns
    -------
    dict
        Dictionary with size and duration exponents
    """
    # Detect avalanches
    total_spikes = spike_history.sum(axis=1)
    
    avalanche_sizes = []
    avalanche_durations = []
    
    in_avalanche = False
    current_size = 0
    current_duration = 0
    
    for t in range(len(total_spikes)):
        if total_spikes[t] > 0:
            if not in_avalanche:
                in_avalanche = True
                current_size = 0
                current_duration = 0
            
            current_size += total_spikes[t]
            current_duration += 1
        else:
            if in_avalanche:
                if current_size >= min_avalanche_size:
                    avalanche_sizes.append(current_size)
                    avalanche_durations.append(current_duration)
                in_avalanche = False
    
    results = {}
    
    # Fit power laws
    if len(avalanche_sizes) > 10:
        sizes = np.array(avalanche_sizes)
        # Log-binning for power-law fit
        log_sizes = np.log10(sizes[sizes > 0])
        hist, bin_edges = np.histogram(log_sizes, bins=20)
        
        # Linear fit in log-log space
        valid = hist > 0
        if valid.sum() > 2:
            bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
            log_hist = np.log10(hist[valid])
            slope, _ = np.polyfit(bin_centers[valid], log_hist, 1)
            results['size_exponent'] = -slope
    
    if len(avalanche_durations) > 10:
        durations = np.array(avalanche_durations)
        log_durations = np.log10(durations[durations > 0])
        hist, bin_edges = np.histogram(log_durations, bins=15)
        
        valid = hist > 0
        if valid.sum() > 2:
            bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
            log_hist = np.log10(hist[valid])
            slope, _ = np.polyfit(bin_centers[valid], log_hist, 1)
            results['duration_exponent'] = -slope
    
    return results
