"""
Bifurcation Detector
====================

Detect and analyze phase transitions when C(t) crosses C_critical = 8.3 bits.
Includes real-time monitoring, critical slowing down detection, and 
post-transition branch analysis.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from scipy.signal import find_peaks, savgol_filter
from scipy.stats import linregress
import warnings


class BifurcationDetector:
    """
    Detect phase transitions in C(t) time series.
    
    Parameters
    ----------
    C_critical : float, optional
        Critical threshold for consciousness emergence, default=8.3 bits
    pre_transition_window : int, optional
        Number of points to analyze before transition
    post_transition_window : int, optional
        Number of points to analyze after transition
    
    Methods
    -------
    monitor : Continuous monitoring of C(t)
    detect_transition : Identify transition points
    detect_critical_slowing : Detect early warning signs
    analyze_branches : Quantify bifurcation branches
    detect_hysteresis : Check for hysteresis in transitions
    """
    
    def __init__(
        self,
        C_critical: float = 8.3,
        pre_transition_window: int = 50,
        post_transition_window: int = 100
    ):
        self.C_critical = C_critical
        self.pre_window = pre_transition_window
        self.post_window = post_transition_window
        
        # State tracking
        self.is_monitoring = False
        self.current_state = "subcritical"
        self.transition_history = []
    
    def monitor(
        self, 
        C_timeseries: np.ndarray,
        time: Optional[np.ndarray] = None
    ) -> Dict[str, any]:
        """
        Continuous monitoring of C(t) for transitions.
        
        Parameters
        ----------
        C_timeseries : np.ndarray
            Time series of C values
        time : np.ndarray, optional
            Time stamps corresponding to C values
        
        Returns
        -------
        status : dict
            Current state and any detected transitions
        """
        if time is None:
            time = np.arange(len(C_timeseries))
        
        # Current value
        C_current = C_timeseries[-1]
        
        # Update state
        if C_current < self.C_critical - 0.5:
            new_state = "subcritical"
        elif C_current > self.C_critical + 0.5:
            new_state = "supercritical"
        else:
            new_state = "near_critical"
        
        # Detect transition
        transition_detected = False
        if len(C_timeseries) >= 2:
            prev_C = C_timeseries[-2]
            if prev_C < self.C_critical <= C_current:
                transition_detected = True
                self.transition_history.append({
                    'time': time[-1],
                    'direction': 'up',
                    'C_before': prev_C,
                    'C_after': C_current
                })
            elif prev_C > self.C_critical >= C_current:
                transition_detected = True
                self.transition_history.append({
                    'time': time[-1],
                    'direction': 'down',
                    'C_before': prev_C,
                    'C_after': C_current
                })
        
        # Check for critical slowing if near threshold
        critical_slowing = False
        if len(C_timeseries) >= self.pre_window:
            recent = C_timeseries[-self.pre_window:]
            if new_state == "near_critical":
                cs_result = self.detect_critical_slowing(recent)
                critical_slowing = cs_result['detected']
        
        self.current_state = new_state
        
        return {
            'current_C': C_current,
            'state': new_state,
            'transition_detected': transition_detected,
            'critical_slowing': critical_slowing,
            'n_transitions': len(self.transition_history),
            'last_transition': self.transition_history[-1] if self.transition_history else None
        }
    
    def detect_transition(
        self, 
        C_timeseries: np.ndarray,
        threshold: Optional[float] = None,
        time: Optional[np.ndarray] = None
    ) -> Dict[str, any]:
        """
        Identify all transition points in time series.
        
        Parameters
        ----------
        C_timeseries : np.ndarray
            Time series of C values
        threshold : float, optional
            Custom threshold (default: C_critical)
        time : np.ndarray, optional
            Time stamps
        
        Returns
        -------
        transitions : dict
            Information about detected transitions
        """
        threshold = threshold or self.C_critical
        
        if time is None:
            time = np.arange(len(C_timeseries))
        
        # Find crossings
        below = C_timeseries < threshold
        above = C_timeseries >= threshold
        
        # Detect transitions
        up_transitions = np.where(below[:-1] & above[1:])[0] + 1
        down_transitions = np.where(above[:-1] & below[1:])[0] + 1
        
        # Analyze each transition
        up_details = []
        for idx in up_transitions:
            if idx >= self.pre_window and idx + self.post_window < len(C_timeseries):
                details = self._analyze_single_transition(
                    C_timeseries, idx, 'up', time
                )
                up_details.append(details)
        
        down_details = []
        for idx in down_transitions:
            if idx >= self.pre_window and idx + self.post_window < len(C_timeseries):
                details = self._analyze_single_transition(
                    C_timeseries, idx, 'down', time
                )
                down_details.append(details)
        
        return {
            'n_up_transitions': len(up_transitions),
            'n_down_transitions': len(down_transitions),
            'up_transition_indices': up_transitions,
            'down_transition_indices': down_transitions,
            'up_transition_details': up_details,
            'down_transition_details': down_details,
            'total_transitions': len(up_transitions) + len(down_transitions)
        }
    
    def _analyze_single_transition(
        self,
        C_timeseries: np.ndarray,
        transition_idx: int,
        direction: str,
        time: np.ndarray
    ) -> Dict[str, float]:
        """Analyze details of a single transition."""
        # Pre-transition dynamics
        pre_data = C_timeseries[transition_idx - self.pre_window:transition_idx]
        pre_mean = np.mean(pre_data)
        pre_std = np.std(pre_data)
        
        # Calculate variance growth (critical slowing indicator)
        mid_point = len(pre_data) // 2
        early_var = np.var(pre_data[:mid_point])
        late_var = np.var(pre_data[mid_point:])
        variance_growth = late_var / (early_var + 1e-10)
        
        # Post-transition dynamics
        post_data = C_timeseries[transition_idx:transition_idx + self.post_window]
        post_mean = np.mean(post_data)
        post_std = np.std(post_data)
        
        # Transition sharpness (how quickly it occurs)
        transition_region = C_timeseries[transition_idx-2:transition_idx+3]
        sharpness = np.max(np.abs(np.diff(transition_region)))
        
        return {
            'time': time[transition_idx],
            'index': transition_idx,
            'direction': direction,
            'pre_mean': pre_mean,
            'pre_std': pre_std,
            'post_mean': post_mean,
            'post_std': post_std,
            'transition_magnitude': post_mean - pre_mean,
            'variance_growth': variance_growth,
            'sharpness': sharpness
        }
    
    def detect_critical_slowing(
        self, 
        C_timeseries: np.ndarray
    ) -> Dict[str, any]:
        """
        Detect critical slowing down as early warning of transition.
        
        Critical slowing manifests as:
        1. Increasing variance
        2. Increasing autocorrelation
        3. Decreasing recovery rate from perturbations
        
        Parameters
        ----------
        C_timeseries : np.ndarray
            Recent time series approaching critical point
        
        Returns
        -------
        result : dict
            Detection results and indicators
        """
        if len(C_timeseries) < 20:
            return {'detected': False, 'reason': 'insufficient_data'}
        
        # Split into early and late periods
        mid = len(C_timeseries) // 2
        early = C_timeseries[:mid]
        late = C_timeseries[mid:]
        
        # 1. Variance increase
        var_early = np.var(early)
        var_late = np.var(late)
        variance_ratio = var_late / (var_early + 1e-10)
        
        # 2. Autocorrelation increase (lag-1)
        acf_early = self._lag1_autocorr(early)
        acf_late = self._lag1_autocorr(late)
        acf_increase = acf_late > acf_early
        
        # 3. Trend detection (slowing down = flattening)
        detrended = C_timeseries - np.mean(C_timeseries)
        velocity = np.abs(np.diff(detrended))
        early_vel = np.mean(velocity[:mid-1])
        late_vel = np.mean(velocity[mid:])
        velocity_decrease = late_vel < early_vel
        
        # Detection criteria
        detected = (variance_ratio > 1.5) and acf_increase
        
        return {
            'detected': detected,
            'variance_ratio': variance_ratio,
            'acf_early': acf_early,
            'acf_late': acf_late,
            'velocity_decrease': velocity_decrease,
            'early_velocity': early_vel,
            'late_velocity': late_vel
        }
    
    def analyze_branches(
        self, 
        post_transition_data: np.ndarray,
        n_branches: int = 5
    ) -> Dict[str, any]:
        """
        Quantify bifurcation branches after phase transition.
        
        After crossing C_critical, the system should settle into one of
        4-5 distinct attractor states (branches).
        
        Parameters
        ----------
        post_transition_data : np.ndarray
            Activity data after transition (N, T) or C(t) values
        n_branches : int
            Expected number of branches
        
        Returns
        -------
        branches : dict
            Information about detected branches
        """
        if post_transition_data.ndim == 1:
            # C(t) time series
            C_values = post_transition_data
            
            # Smooth the signal
            if len(C_values) > 10:
                C_smooth = savgol_filter(C_values, 
                                        window_length=min(11, len(C_values)//2*2-1), 
                                        polyorder=3)
            else:
                C_smooth = C_values
            
            # Find stable plateaus (attractors)
            peaks, properties = find_peaks(C_smooth, 
                                          distance=len(C_smooth)//n_branches,
                                          prominence=0.5)
            
            # Cluster C values
            from sklearn.cluster import KMeans
            if len(C_values) > n_branches:
                kmeans = KMeans(n_clusters=n_branches, random_state=42)
                labels = kmeans.fit_predict(C_values.reshape(-1, 1))
                centers = kmeans.cluster_centers_.flatten()
                
                # Calculate branch populations
                unique, counts = np.unique(labels, return_counts=True)
                populations = counts / len(labels)
                
                # Sort by C value
                sort_idx = np.argsort(centers)
                centers = centers[sort_idx]
                populations = populations[sort_idx]
            else:
                centers = np.array([np.mean(C_values)])
                populations = np.array([1.0])
        
        else:
            # Activity patterns (N, T)
            # Use PCA to identify branches
            from sklearn.decomposition import PCA
            from sklearn.cluster import KMeans
            
            pca = PCA(n_components=min(5, post_transition_data.shape[0]))
            patterns_reduced = pca.fit_transform(post_transition_data.T)
            
            # Cluster in reduced space
            kmeans = KMeans(n_clusters=n_branches, random_state=42)
            labels = kmeans.fit_predict(patterns_reduced)
            
            # Calculate statistics for each branch
            unique, counts = np.unique(labels, return_counts=True)
            populations = counts / len(labels)
            
            # Average C value per branch (approximate)
            centers = np.array([np.mean(post_transition_data[:, labels == i]) 
                              for i in unique])
        
        # Information-theoretic measure of branch distribution
        # Ideal: uniform distribution across branches
        # Reality: power-law distributed
        if len(populations) > 0:
            entropy_branches = -np.sum(populations * np.log2(populations + 1e-10))
            max_entropy = np.log2(len(populations))
            uniformity = entropy_branches / max_entropy
        else:
            uniformity = 0
        
        return {
            'n_branches_detected': len(centers),
            'branch_centers': centers,
            'branch_populations': populations,
            'branch_entropy': entropy_branches if len(populations) > 0 else 0,
            'uniformity': uniformity,
            'power_law_exponent': self._estimate_power_law_exponent(populations)
        }
    
    def detect_hysteresis(
        self,
        C_timeseries: np.ndarray,
        parameter_series: Optional[np.ndarray] = None
    ) -> Dict[str, any]:
        """
        Detect hysteresis in phase transitions.
        
        Hysteresis: transition thresholds differ for up vs down transitions.
        
        Parameters
        ----------
        C_timeseries : np.ndarray
            Time series of C values
        parameter_series : np.ndarray, optional
            Control parameter being varied
        
        Returns
        -------
        hysteresis : dict
            Hysteresis detection results
        """
        # Detect all transitions
        transitions = self.detect_transition(C_timeseries)
        
        if transitions['total_transitions'] < 2:
            return {
                'detected': False,
                'reason': 'insufficient_transitions'
            }
        
        # Compare up vs down thresholds
        up_values = []
        down_values = []
        
        for detail in transitions['up_transition_details']:
            up_values.append(detail['pre_mean'])
        
        for detail in transitions['down_transition_details']:
            down_values.append(detail['pre_mean'])
        
        if len(up_values) > 0 and len(down_values) > 0:
            up_threshold = np.mean(up_values)
            down_threshold = np.mean(down_values)
            
            hysteresis_gap = np.abs(down_threshold - up_threshold)
            detected = hysteresis_gap > 0.5  # Significant gap
            
            return {
                'detected': detected,
                'up_threshold': up_threshold,
                'down_threshold': down_threshold,
                'hysteresis_gap': hysteresis_gap,
                'n_up_transitions': len(up_values),
                'n_down_transitions': len(down_values)
            }
        else:
            return {
                'detected': False,
                'reason': 'missing_transition_direction'
            }
    
    def _lag1_autocorr(self, x: np.ndarray) -> float:
        """Calculate lag-1 autocorrelation."""
        if len(x) < 2:
            return 0
        x_norm = (x - np.mean(x)) / (np.std(x) + 1e-10)
        return np.corrcoef(x_norm[:-1], x_norm[1:])[0, 1]
    
    def _estimate_power_law_exponent(self, populations: np.ndarray) -> float:
        """
        Estimate power-law exponent of branch distribution.
        
        Theory predicts power-law: P(branch) ~ branch^(-alpha)
        """
        if len(populations) < 3:
            return np.nan
        
        # Rank-frequency
        sorted_pop = np.sort(populations)[::-1]  # Descending
        ranks = np.arange(1, len(sorted_pop) + 1)
        
        # Fit power law: log(pop) = -alpha * log(rank) + const
        log_ranks = np.log(ranks)
        log_pops = np.log(sorted_pop + 1e-10)
        
        slope, _, _, _, _ = linregress(log_ranks, log_pops)
        
        return -slope  # Power law exponent


def plot_bifurcation_diagram(
    C_timeseries: np.ndarray,
    time: Optional[np.ndarray] = None,
    C_critical: float = 8.3,
    transitions: Optional[Dict] = None
):
    """
    Create bifurcation diagram visualization.
    
    Parameters
    ----------
    C_timeseries : np.ndarray
        Time series of C values
    time : np.ndarray, optional
        Time stamps
    C_critical : float
        Critical threshold
    transitions : dict, optional
        Pre-computed transition information
    """
    import matplotlib.pyplot as plt
    
    if time is None:
        time = np.arange(len(C_timeseries))
    
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    # Main time series
    ax = axes[0]
    ax.plot(time, C_timeseries, 'b-', linewidth=1.5, alpha=0.7)
    ax.axhline(C_critical, color='r', linestyle='--', linewidth=2, 
              label=f'C_critical = {C_critical}')
    ax.fill_between(time, 0, C_timeseries, alpha=0.2)
    
    # Mark transitions
    if transitions:
        for idx in transitions.get('up_transition_indices', []):
            ax.axvline(time[idx], color='green', alpha=0.5, linestyle=':')
        for idx in transitions.get('down_transition_indices', []):
            ax.axvline(time[idx], color='orange', alpha=0.5, linestyle=':')
    
    ax.set_ylabel('C(t) [bits]', fontsize=12)
    ax.set_title('Consciousness Measure and Phase Transitions', fontsize=14, 
                fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Velocity (rate of change)
    ax = axes[1]
    velocity = np.diff(C_timeseries) / np.diff(time) if len(time) > 1 else np.diff(C_timeseries)
    ax.plot(time[1:], velocity, 'purple', linewidth=1.5)
    ax.axhline(0, color='k', linestyle='-', alpha=0.3)
    ax.fill_between(time[1:], 0, velocity, alpha=0.2, color='purple')
    
    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('dC/dt', fontsize=12)
    ax.set_title('Rate of Change', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig
