"""
Phase Transition Detector for Ouroboros Observer

Detects when C(t) crosses the critical threshold C_critical â‰ˆ 8.3 bits
Includes pre-transition warnings and post-transition branch analysis.
"""

import numpy as np
from typing import List, Tuple, Dict, Optional
from scipy.signal import find_peaks
from dataclasses import dataclass


@dataclass
class TransitionEvent:
    """Data structure for detected phase transition."""
    time: float
    C_before: float
    C_after: float
    transition_type: str  # 'subcritical_to_supercritical' or vice versa
    branch_id: Optional[int] = None


class BifurcationDetector:
    """
    Detect phase transitions in C(t) time series.
    
    Features:
    - Real-time monitoring with threshold detection
    - Critical slowing down analysis (pre-transition warning)
    - Post-transition branch identification
    - Hysteresis detection
    
    Parameters
    ----------
    C_critical : float
        Critical threshold value (default: 8.3 bits)
    window_size : int
        Window size for variance and autocorrelation calculations
    slowing_threshold : float
        Threshold for critical slowing detection
    """
    
    def __init__(self, C_critical: float = 8.3,
                 window_size: int = 100,
                 slowing_threshold: float = 0.7):
        self.C_critical = C_critical
        self.window_size = window_size
        self.slowing_threshold = slowing_threshold
        
        # State tracking
        self.transitions: List[TransitionEvent] = []
        self.current_branch = None
        self.warning_active = False
    
    def monitor(self, C_timeseries: np.ndarray, 
                time: Optional[np.ndarray] = None) -> Dict:
        """
        Continuous monitoring of C(t) for transitions.
        
        Parameters
        ----------
        C_timeseries : np.ndarray
            Time series of C(t) values
        time : np.ndarray, optional
            Time points corresponding to C values
        
        Returns
        -------
        dict
            Monitoring results including transitions, warnings, and branches
        """
        if time is None:
            time = np.arange(len(C_timeseries))
        
        # Detect transitions
        transitions = self.detect_transitions(C_timeseries, time)
        
        # Analyze critical slowing
        slowing_warnings = self._detect_critical_slowing(C_timeseries, time)
        
        # Current state
        current_state = 'supercritical' if C_timeseries[-1] > self.C_critical else 'subcritical'
        
        results = {
            'transitions': transitions,
            'warnings': slowing_warnings,
            'current_state': current_state,
            'current_C': C_timeseries[-1],
            'distance_to_critical': abs(C_timeseries[-1] - self.C_critical)
        }
        
        return results
    
    def detect_transitions(self, C_timeseries: np.ndarray,
                          time: np.ndarray,
                          threshold: Optional[float] = None) -> List[TransitionEvent]:
        """
        Identify transition points where C(t) crosses threshold.
        
        Parameters
        ----------
        C_timeseries : np.ndarray
            Time series of C(t) values
        time : np.ndarray
            Time points
        threshold : float, optional
            Override default C_critical
        
        Returns
        -------
        list
            List of TransitionEvent objects
        """
        if threshold is None:
            threshold = self.C_critical
        
        transitions = []
        
        # Find crossings
        above_threshold = C_timeseries > threshold
        
        for i in range(1, len(above_threshold)):
            if above_threshold[i] != above_threshold[i-1]:
                # Transition detected
                if above_threshold[i]:
                    trans_type = 'subcritical_to_supercritical'
                else:
                    trans_type = 'supercritical_to_subcritical'
                
                event = TransitionEvent(
                    time=time[i],
                    C_before=C_timeseries[i-1],
                    C_after=C_timeseries[i],
                    transition_type=trans_type
                )
                transitions.append(event)
        
        self.transitions = transitions
        return transitions
    
    def _detect_critical_slowing(self, C_timeseries: np.ndarray,
                                 time: np.ndarray) -> List[Dict]:
        """
        Detect critical slowing down as early warning signal.
        
        Critical systems show:
        - Increased variance
        - Increased autocorrelation
        - Slower recovery from perturbations
        """
        warnings = []
        
        if len(C_timeseries) < 2 * self.window_size:
            return warnings
        
        for i in range(self.window_size, len(C_timeseries) - self.window_size):
            # Calculate metrics in sliding window
            window = C_timeseries[i-self.window_size:i]
            
            # Variance
            variance = np.var(window)
            
            # Autocorrelation at lag 1
            if len(window) > 1:
                autocorr = np.corrcoef(window[:-1], window[1:])[0, 1]
            else:
                autocorr = 0.0
            
            # Check for critical slowing
            if autocorr > self.slowing_threshold:
                # Approaching criticality
                warnings.append({
                    'time': time[i],
                    'autocorrelation': autocorr,
                    'variance': variance,
                    'C_value': C_timeseries[i],
                    'message': 'Critical slowing detected - transition imminent'
                })
        
        return warnings
    
    def analyze_branches(self, C_timeseries: np.ndarray,
                        activity_patterns: np.ndarray,
                        time_window: Tuple[float, float]) -> Dict:
        """
        Analyze bifurcation branches after transition.
        
        Parameters
        ----------
        C_timeseries : np.ndarray
            C(t) values
        activity_patterns : np.ndarray
            Neural activity patterns (T x N)
        time_window : tuple
            (start_time, end_time) for analysis
        
        Returns
        -------
        dict
            Branch analysis results
        """
        start_idx = int(time_window[0])
        end_idx = int(time_window[1])
        
        if end_idx > len(C_timeseries):
            end_idx = len(C_timeseries)
        
        window_data = activity_patterns[start_idx:end_idx]
        window_C = C_timeseries[start_idx:end_idx]
        
        # Cluster activity patterns
        branches = self._identify_branches(window_data)
        
        # Analyze each branch
        branch_stats = []
        for branch_id in np.unique(branches):
            mask = branches == branch_id
            branch_C = window_C[mask]
            branch_patterns = window_data[mask]
            
            stats = {
                'branch_id': int(branch_id),
                'n_points': int(mask.sum()),
                'mean_C': float(branch_C.mean()),
                'std_C': float(branch_C.std()),
                'mean_activity': float(branch_patterns.mean()),
                'fraction': float(mask.sum() / len(branches))
            }
            branch_stats.append(stats)
        
        # Power-law distribution check
        fractions = [s['fraction'] for s in branch_stats]
        fractions.sort(reverse=True)
        
        results = {
            'n_branches': len(branch_stats),
            'branches': branch_stats,
            'branch_fractions': fractions,
            'power_law_fit': self._fit_power_law(fractions)
        }
        
        return results
    
    def _identify_branches(self, patterns: np.ndarray,
                          n_clusters: Optional[int] = None) -> np.ndarray:
        """
        Identify distinct branches using clustering.
        
        Uses k-means clustering on PCA-reduced patterns.
        """
        from sklearn.decomposition import PCA
        from sklearn.cluster import KMeans
        
        # Dimensionality reduction
        if patterns.shape[1] > 10:
            pca = PCA(n_components=10)
            patterns_reduced = pca.fit_transform(patterns)
        else:
            patterns_reduced = patterns
        
        # Determine number of clusters if not specified
        if n_clusters is None:
            # Use elbow method (simplified)
            n_clusters = min(5, len(patterns) // 20)
            n_clusters = max(2, n_clusters)
        
        # Cluster
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        labels = kmeans.fit_predict(patterns_reduced)
        
        return labels
    
    def _fit_power_law(self, values: List[float]) -> Dict:
        """Fit power-law distribution to branch fractions."""
        if len(values) < 3:
            return {'exponent': None, 'quality': 0.0}
        
        values = np.array(values)
        values = values[values > 0]
        
        if len(values) < 3:
            return {'exponent': None, 'quality': 0.0}
        
        # Log-log fit
        log_x = np.log(np.arange(1, len(values) + 1))
        log_y = np.log(values)
        
        # Linear regression
        coeffs = np.polyfit(log_x, log_y, 1)
        exponent = -coeffs[0]
        
        # R-squared
        y_pred = np.polyval(coeffs, log_x)
        r_squared = 1 - np.sum((log_y - y_pred)**2) / np.sum((log_y - log_y.mean())**2)
        
        return {
            'exponent': float(exponent),
            'quality': float(r_squared)
        }
    
    def detect_hysteresis(self, C_forward: np.ndarray,
                         C_backward: np.ndarray,
                         parameter_values: np.ndarray) -> Dict:
        """
        Detect hysteresis in forward vs backward parameter sweeps.
        
        Parameters
        ----------
        C_forward : np.ndarray
            C(t) values during forward parameter sweep
        C_backward : np.ndarray
            C(t) values during backward parameter sweep
        parameter_values : np.ndarray
            Parameter values at each point
        
        Returns
        -------
        dict
            Hysteresis analysis results
        """
        # Find transitions in forward direction
        forward_transitions = []
        for i in range(1, len(C_forward)):
            if (C_forward[i] > self.C_critical and 
                C_forward[i-1] <= self.C_critical):
                forward_transitions.append(parameter_values[i])
        
        # Find transitions in backward direction
        backward_transitions = []
        for i in range(1, len(C_backward)):
            if (C_backward[i] < self.C_critical and 
                C_backward[i-1] >= self.C_critical):
                backward_transitions.append(parameter_values[i])
        
        # Calculate hysteresis width
        if forward_transitions and backward_transitions:
            hysteresis_width = abs(
                np.mean(forward_transitions) - np.mean(backward_transitions)
            )
            has_hysteresis = True
        else:
            hysteresis_width = 0.0
            has_hysteresis = False
        
        results = {
            'has_hysteresis': has_hysteresis,
            'hysteresis_width': hysteresis_width,
            'forward_transition_points': forward_transitions,
            'backward_transition_points': backward_transitions
        }
        
        return results


def calculate_lyapunov_exponent(timeseries: np.ndarray,
                                 embedding_dim: int = 3,
                                 delay: int = 1) -> float:
    """
    Estimate largest Lyapunov exponent.
    
    Positive exponent indicates chaos.
    Zero exponent indicates critical dynamics.
    Negative exponent indicates stable dynamics.
    
    Parameters
    ----------
    timeseries : np.ndarray
        Time series data
    embedding_dim : int
        Embedding dimension
    delay : int
        Time delay for embedding
    
    Returns
    -------
    float
        Largest Lyapunov exponent
    """
    # Simplified Rosenstein algorithm
    N = len(timeseries)
    
    # Time-delay embedding
    embedded = []
    for i in range(N - (embedding_dim - 1) * delay):
        point = [timeseries[i + j * delay] for j in range(embedding_dim)]
        embedded.append(point)
    
    embedded = np.array(embedded)
    
    if len(embedded) < 10:
        return 0.0
    
    # Find nearest neighbors
    divergences = []
    
    for i in range(len(embedded) - 1):
        # Find nearest neighbor
        distances = np.linalg.norm(embedded - embedded[i], axis=1)
        distances[i] = np.inf  # Exclude self
        
        nearest_idx = np.argmin(distances)
        
        # Track divergence
        if i < len(embedded) - 1 and nearest_idx < len(embedded) - 1:
            dist_0 = distances[nearest_idx]
            dist_1 = np.linalg.norm(embedded[i+1] - embedded[nearest_idx+1])
            
            if dist_0 > 0 and dist_1 > 0:
                divergences.append(np.log(dist_1 / dist_0))
    
    if len(divergences) == 0:
        return 0.0
    
    # Lyapunov exponent is average divergence rate
    lyapunov = np.mean(divergences)
    
    return lyapunov
