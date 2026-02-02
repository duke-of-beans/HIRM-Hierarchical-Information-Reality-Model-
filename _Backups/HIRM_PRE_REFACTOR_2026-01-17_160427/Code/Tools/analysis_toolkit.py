"""
Consciousness Emergence Analysis Toolkit
========================================

Comprehensive analysis tools for studying self-reference-driven
consciousness emergence in neural networks.
"""

import numpy as np
from scipy import stats, signal
from scipy.optimize import curve_fit
from typing import Dict, List, Tuple, Optional
import warnings


class PhaseTransitionAnalyzer:
    """
    Detect and characterize phase transitions in consciousness measures.
    """
    
    def __init__(self, C_critical: float = 8.3, window_size: int = 10):
        self.C_critical = C_critical
        self.window_size = window_size
        
    def detect_transitions(
        self,
        C_timeseries: np.ndarray,
        threshold: float = None
    ) -> Dict:
        """
        Detect phase transitions in C(t) timeseries.
        
        Returns transition indices, characteristics, and confidence.
        """
        if threshold is None:
            threshold = self.C_critical
            
        # Find threshold crossings
        crossings = self._find_crossings(C_timeseries, threshold)
        
        # Detect discontinuities
        discontinuities = self._detect_discontinuities(C_timeseries)
        
        # Measure critical slowing
        slowing = self._measure_critical_slowing(C_timeseries)
        
        # Identify true transitions (combine evidence)
        transitions = self._identify_transitions(
            crossings, discontinuities, slowing
        )
        
        return {
            'transitions': transitions,
            'crossings': crossings,
            'discontinuities': discontinuities,
            'critical_slowing': slowing,
            'confidence': self._calculate_confidence(transitions, C_timeseries)
        }
    
    def _find_crossings(
        self,
        timeseries: np.ndarray,
        threshold: float
    ) -> List[int]:
        """Find indices where timeseries crosses threshold upward."""
        crossings = []
        for i in range(1, len(timeseries)):
            if timeseries[i-1] < threshold <= timeseries[i]:
                crossings.append(i)
        return crossings
    
    def _detect_discontinuities(
        self,
        timeseries: np.ndarray
    ) -> List[Tuple[int, float]]:
        """
        Detect discontinuities using derivative analysis.
        
        Returns list of (index, jump_size) tuples.
        """
        # Calculate derivative
        derivative = np.gradient(timeseries)
        
        # Calculate running statistics
        mean = np.convolve(derivative, np.ones(self.window_size)/self.window_size, mode='same')
        std = np.array([
            np.std(derivative[max(0, i-self.window_size):min(len(derivative), i+self.window_size)])
            for i in range(len(derivative))
        ])
        
        # Detect outliers (discontinuities)
        z_scores = np.abs((derivative - mean) / (std + 1e-8))
        discontinuities = []
        
        for i in range(self.window_size, len(z_scores) - self.window_size):
            if z_scores[i] > 3.0:  # 3 sigma threshold
                discontinuities.append((i, derivative[i]))
        
        return discontinuities
    
    def _measure_critical_slowing(
        self,
        timeseries: np.ndarray
    ) -> Dict:
        """
        Measure critical slowing: increased autocorrelation before transition.
        
        Returns autocorrelation at each timepoint.
        """
        autocorr = np.zeros(len(timeseries) - self.window_size)
        
        for i in range(len(autocorr)):
            window = timeseries[i:i+self.window_size]
            if len(window) > 1:
                # Lag-1 autocorrelation
                autocorr[i] = np.corrcoef(window[:-1], window[1:])[0, 1]
        
        # Detect increases in autocorrelation
        derivative = np.gradient(autocorr)
        slowing_regions = np.where(derivative > np.percentile(derivative, 90))[0]
        
        return {
            'autocorrelation': autocorr,
            'slowing_regions': slowing_regions,
            'mean_autocorr': np.mean(autocorr)
        }
    
    def _identify_transitions(
        self,
        crossings: List[int],
        discontinuities: List[Tuple[int, float]],
        slowing: Dict
    ) -> List[Dict]:
        """
        Identify true transitions by combining multiple evidence sources.
        """
        transitions = []
        
        for crossing_idx in crossings:
            # Check for nearby discontinuity
            discontinuity_nearby = any(
                abs(crossing_idx - disc_idx) < self.window_size
                for disc_idx, _ in discontinuities
            )
            
            # Check for critical slowing before crossing
            slowing_before = any(
                (crossing_idx - self.window_size*2 < slow_idx < crossing_idx)
                for slow_idx in slowing['slowing_regions']
            )
            
            # Calculate confidence
            evidence_count = sum([
                True,  # crossing itself
                discontinuity_nearby,
                slowing_before
            ])
            
            if evidence_count >= 2:  # Require at least 2/3 evidence types
                transitions.append({
                    'index': crossing_idx,
                    'evidence': {
                        'crossing': True,
                        'discontinuity': discontinuity_nearby,
                        'slowing': slowing_before
                    },
                    'confidence': evidence_count / 3
                })
        
        return transitions
    
    def _calculate_confidence(
        self,
        transitions: List[Dict],
        timeseries: np.ndarray
    ) -> float:
        """Calculate overall confidence in transition detection."""
        if not transitions:
            return 0.0
        
        # Average individual transition confidences
        avg_confidence = np.mean([t['confidence'] for t in transitions])
        
        # Penalize multiple transitions (expect 1-2 max)
        multiplicity_penalty = 1.0 / (1 + 0.3 * max(0, len(transitions) - 2))
        
        return avg_confidence * multiplicity_penalty


class CriticalityAnalyzer:
    """
    Analyze criticality metrics from neural network dynamics.
    """
    
    def __init__(self):
        self.avalanche_exponents = []
        
    def calculate_branching_parameter(
        self,
        activity: np.ndarray
    ) -> Dict:
        """
        Calculate branching parameter Ïƒ from activity timeseries.
        
        Parameters
        ----------
        activity : np.ndarray
            Neural activity [time, neurons] or [time]
            
        Returns
        -------
        results : Dict
            Branching parameter and related metrics
        """
        # Binarize activity
        if len(activity.shape) > 1:
            threshold = activity.mean() + 0.5 * activity.std()
            binary = (activity > threshold).astype(float)
            active_counts = binary.sum(axis=1)
        else:
            threshold = activity.mean() + 0.5 * activity.std()
            binary = (activity > threshold).astype(float)
            active_counts = binary
        
        # Calculate branching parameter: Ïƒ = <n_{t+1}> / <n_t>
        if len(active_counts) > 1:
            sigma = np.mean(active_counts[1:] / (active_counts[:-1] + 1e-8))
            sigma = np.clip(sigma, 0, 2)  # Reasonable bounds
        else:
            sigma = 1.0
        
        # Calculate variance of branching
        if len(active_counts) > 2:
            branching_ratios = active_counts[1:] / (active_counts[:-1] + 1e-8)
            sigma_variance = np.var(branching_ratios)
        else:
            sigma_variance = 0.0
        
        # Distance from criticality
        distance = abs(sigma - 1.0)
        
        return {
            'sigma': sigma,
            'sigma_variance': sigma_variance,
            'distance_from_critical': distance,
            'is_critical': distance < 0.1,
            'active_counts': active_counts
        }
    
    def analyze_avalanches(
        self,
        activity: np.ndarray,
        threshold: Optional[float] = None
    ) -> Dict:
        """
        Analyze avalanche statistics.
        
        Identifies avalanches as contiguous periods of above-threshold activity.
        """
        # Binarize
        if threshold is None:
            threshold = activity.mean() + activity.std()
        
        if len(activity.shape) > 1:
            activity = activity.sum(axis=1)  # Sum across neurons
        
        binary = (activity > threshold).astype(int)
        
        # Find avalanches
        avalanches = []
        in_avalanche = False
        current_avalanche = []
        
        for t, active in enumerate(binary):
            if active:
                current_avalanche.append(activity[t])
                in_avalanche = True
            else:
                if in_avalanche and current_avalanche:
                    avalanches.append(current_avalanche)
                    current_avalanche = []
                in_avalanche = False
        
        if not avalanches:
            return {'avalanche_count': 0}
        
        # Calculate statistics
        sizes = [sum(av) for av in avalanches]
        durations = [len(av) for av in avalanches]
        
        # Fit power law
        size_exponent = self._fit_power_law(sizes)
        duration_exponent = self._fit_power_law(durations)
        
        return {
            'avalanche_count': len(avalanches),
            'mean_size': np.mean(sizes),
            'mean_duration': np.mean(durations),
            'size_exponent': size_exponent,
            'duration_exponent': duration_exponent,
            'sizes': sizes,
            'durations': durations
        }
    
    def _fit_power_law(self, data: List[float]) -> float:
        """Fit power law exponent using log-log linear regression."""
        if len(data) < 10:
            return np.nan
        
        # Remove zeros
        data = [x for x in data if x > 0]
        if not data:
            return np.nan
        
        # Log-log fit
        hist, bins = np.histogram(data, bins=20)
        bins = bins[:-1]
        
        # Filter valid points
        valid = (hist > 0) & (bins > 0)
        if sum(valid) < 3:
            return np.nan
        
        log_bins = np.log(bins[valid])
        log_hist = np.log(hist[valid])
        
        # Linear fit
        slope, intercept = np.polyfit(log_bins, log_hist, 1)
        
        return -slope  # Power law exponent


class SelfReferenceAnalyzer:
    """
    Analyze self-reference metrics and fixed-point dynamics.
    """
    
    def __init__(self):
        pass
    
    def measure_self_prediction_accuracy(
        self,
        states: np.ndarray,
        predictions: np.ndarray
    ) -> Dict:
        """
        Measure how well system predicts its own future states.
        
        Parameters
        ----------
        states : np.ndarray
            Actual states [time, features]
        predictions : np.ndarray
            Predicted states [time, features]
            
        Returns
        -------
        metrics : Dict
            Self-prediction metrics including R
        """
        # Align arrays
        if states.shape != predictions.shape:
            min_len = min(len(states), len(predictions))
            states = states[:min_len]
            predictions = predictions[:min_len]
        
        # Prediction error
        pred_error = np.mean((states - predictions) ** 2)
        
        # Baseline error (predict mean)
        baseline_error = np.mean((states - states.mean(axis=0)) ** 2)
        
        # R score (like RÂ² but for self-reference)
        R = 1.0 - (pred_error / (baseline_error + 1e-8))
        R = np.clip(R, 0, 1)
        
        # Temporal correlation
        if len(states) > 1:
            correlations = []
            for i in range(states.shape[1]):
                corr = np.corrcoef(states[:, i], predictions[:, i])[0, 1]
                if not np.isnan(corr):
                    correlations.append(corr)
            mean_correlation = np.mean(correlations) if correlations else 0.0
        else:
            mean_correlation = 0.0
        
        return {
            'R': float(R),
            'prediction_error': float(pred_error),
            'baseline_error': float(baseline_error),
            'temporal_correlation': float(mean_correlation)
        }
    
    def detect_strange_loops(
        self,
        trajectory: np.ndarray,
        tolerance: float = 0.1
    ) -> Dict:
        """
        Detect strange loop / fixed point convergence.
        
        Looks for cycles or convergence in state space.
        """
        # Calculate distance matrix
        n_points = len(trajectory)
        distances = np.zeros((n_points, n_points))
        
        for i in range(n_points):
            for j in range(i+1, n_points):
                dist = np.linalg.norm(trajectory[i] - trajectory[j])
                distances[i, j] = dist
                distances[j, i] = dist
        
        # Find recurring states (close returns)
        recurrences = []
        for i in range(n_points):
            close_points = np.where((distances[i] < tolerance) & (np.arange(n_points) > i))[0]
            if len(close_points) > 0:
                recurrences.append({
                    'start': i,
                    'returns': close_points.tolist(),
                    'min_distance': float(distances[i, close_points].min())
                })
        
        # Check for convergence to fixed point
        final_segment = trajectory[-10:] if len(trajectory) >= 10 else trajectory
        convergence_variance = np.var(final_segment, axis=0).mean()
        
        return {
            'recurrence_count': len(recurrences),
            'recurrences': recurrences[:5],  # Top 5
            'convergence_variance': float(convergence_variance),
            'converged': convergence_variance < 0.01,
            'loop_strength': len(recurrences) / n_points
        }
    
    def measure_recursive_depth(
        self,
        self_model_layers: List[np.ndarray]
    ) -> Dict:
        """
        Measure depth of recursive self-modeling.
        
        Parameters
        ----------
        self_model_layers : List[np.ndarray]
            Hierarchy of self-model representations
            
        Returns
        -------
        depth_metrics : Dict
            Recursive depth and hierarchy metrics
        """
        if not self_model_layers:
            return {'depth': 0}
        
        # Calculate information at each level
        entropies = []
        for layer in self_model_layers:
            # Estimate entropy
            if len(layer.shape) > 1:
                layer_flat = layer.reshape(-1, layer.shape[-1])
            else:
                layer_flat = layer.reshape(-1, 1)
            
            # Approximate entropy via variance
            entropy = np.log(np.var(layer_flat, axis=0).mean() + 1e-8)
            entropies.append(entropy)
        
        # Depth = number of informative levels
        threshold = np.mean(entropies) - 0.5 * np.std(entropies)
        depth = sum(e > threshold for e in entropies)
        
        # Hierarchical organization
        if len(entropies) > 1:
            hierarchy_score = np.corrcoef(range(len(entropies)), entropies)[0, 1]
        else:
            hierarchy_score = 0.0
        
        return {
            'depth': depth,
            'max_depth': len(self_model_layers),
            'entropies': entropies,
            'hierarchy_score': float(hierarchy_score)
        }


class IntegratedInformationAnalyzer:
    """
    Calculate integrated information Î¦ approximations.
    """
    
    def __init__(self):
        pass
    
    def calculate_phi_approximation(
        self,
        states: np.ndarray,
        method: str = 'correlation'
    ) -> float:
        """
        Calculate Î¦ approximation.
        
        Parameters
        ----------
        states : np.ndarray
            Network states [time, neurons]
        method : str
            'correlation', 'mutual_info', or 'partition'
            
        Returns
        -------
        phi : float
            Integrated information estimate in bits
        """
        if method == 'correlation':
            return self._phi_correlation(states)
        elif method == 'mutual_info':
            return self._phi_mutual_info(states)
        elif method == 'partition':
            return self._phi_partition(states)
        else:
            raise ValueError(f"Unknown method: {method}")
    
    def _phi_correlation(self, states: np.ndarray) -> float:
        """Correlation-based Î¦ approximation."""
        if len(states.shape) == 1:
            return 0.0
        
        if states.shape[0] < 2 or states.shape[1] < 2:
            return 0.0
        
        try:
            # Correlation matrix
            corr = np.corrcoef(states.T)
            
            # Î¦ â‰ˆ average absolute correlation
            n = corr.shape[0]
            phi = np.sum(np.abs(corr)) - n  # Subtract diagonal
            phi = phi / (n * (n - 1))  # Normalize
            
            # Convert to bits (rough approximation)
            phi = -np.log2(1 - phi + 1e-8)
            
            return float(np.clip(phi, 0, 20))
        except:
            return 0.0
    
    def _phi_mutual_info(self, states: np.ndarray) -> float:
        """Mutual information based Î¦."""
        if len(states.shape) == 1:
            return 0.0
            
        if states.shape[0] < 2 or states.shape[1] < 2:
            return 0.0
        
        try:
            # Split into partitions
            mid = states.shape[1] // 2
            part1 = states[:, :mid]
            part2 = states[:, mid:]
            
            # Estimate mutual information via covariance
            cov_full = np.cov(states.T) + np.eye(states.shape[1]) * 1e-6
            cov_1 = np.cov(part1.T) + np.eye(part1.shape[1]) * 1e-6
            cov_2 = np.cov(part2.T) + np.eye(part2.shape[1]) * 1e-6
            
            # Mutual information approximation
            log_det_full = np.log(np.linalg.det(cov_full) + 1e-10)
            log_det_1 = np.log(np.linalg.det(cov_1) + 1e-10)
            log_det_2 = np.log(np.linalg.det(cov_2) + 1e-10)
            
            mi = 0.5 * (log_det_1 + log_det_2 - log_det_full)
            phi = max(0.0, mi / np.log(2))
            
            return float(phi)
        except:
            return 0.0
    
    def _phi_partition(self, states: np.ndarray) -> float:
        """Partition-based Î¦ (simplified IIT)."""
        # Simplified version - full IIT is NP-hard
        return self._phi_mutual_info(states)


class ConsciousnessMetricsCalculator:
    """
    Calculate complete C(t) = Î¦(t) Ã— R(t) Ã— D(t).
    """
    
    def __init__(self, C_critical: float = 8.3):
        self.C_critical = C_critical
        self.phi_analyzer = IntegratedInformationAnalyzer()
        self.self_ref_analyzer = SelfReferenceAnalyzer()
        self.criticality_analyzer = CriticalityAnalyzer()
        
    def calculate_C(
        self,
        states: np.ndarray,
        predictions: Optional[np.ndarray] = None,
        activity: Optional[np.ndarray] = None
    ) -> Dict:
        """
        Calculate complete consciousness measure.
        
        Parameters
        ----------
        states : np.ndarray
            Network states [time, neurons]
        predictions : np.ndarray, optional
            Self-predictions [time, neurons]
        activity : np.ndarray, optional
            Activity for criticality analysis
            
        Returns
        -------
        metrics : Dict
            Complete C(t) and components
        """
        # Calculate Î¦
        phi = self.phi_analyzer.calculate_phi_approximation(states)
        
        # Calculate R
        if predictions is not None:
            R_metrics = self.self_ref_analyzer.measure_self_prediction_accuracy(
                states, predictions
            )
            R = R_metrics['R']
        else:
            R = 0.0
        
        # Calculate D
        if activity is not None:
            crit_metrics = self.criticality_analyzer.calculate_branching_parameter(activity)
            sigma = crit_metrics['sigma']
        else:
            sigma = 1.0
        
        D = 1.0 / (1.0 + abs(sigma - 1.0))
        
        # Calculate C
        C = phi * R * D
        
        return {
            'C': float(C),
            'phi': float(phi),
            'R': float(R),
            'D': float(D),
            'sigma': float(sigma),
            'above_critical': C > self.C_critical,
            'distance_to_critical': float(abs(C - self.C_critical))
        }
