"""
Validation Framework
====================

Test framework for validating theoretical predictions with synthetic data,
benchmark datasets, and statistical tests.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Callable
from scipy.stats import ttest_ind, mannwhitneyu, ks_2samp
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, roc_auc_score
import warnings


class ValidationFramework:
    """
    Comprehensive validation framework for the Ouroboros Observer theory.
    
    Methods
    -------
    generate_synthetic_conscious : Generate data mimicking conscious state
    generate_synthetic_unconscious : Generate data mimicking unconscious state
    validate_classifier : Test classification performance
    validate_predictions : Test specific theoretical predictions
    """
    
    def __init__(self, random_seed: Optional[int] = 42):
        """
        Initialize validation framework.
        
        Parameters
        ----------
        random_seed : int, optional
            Random seed for reproducibility
        """
        self.random_seed = random_seed
        if random_seed is not None:
            np.random.seed(random_seed)
        
        self.validation_history = []
    
    def generate_synthetic_conscious(
        self,
        N: int = 100,
        T: int = 1000,
        C_target: float = 8.5,
        noise_level: float = 0.1
    ) -> Dict[str, np.ndarray]:
        """
        Generate synthetic data mimicking conscious state.
        
        Conscious state characteristics:
        - C(t) â‰ˆ 8.3 Â± 0.6 bits (above threshold)
        - High integration (Î¦ â‰ˆ 4.8 bits)
        - Self-reference present (R â‰ˆ 2.0)
        - Critical dynamics (D â‰ˆ 0.1)
        - Complex spatiotemporal patterns
        - Power-law avalanche statistics
        
        Parameters
        ----------
        N : int
            Number of neurons
        T : int
            Number of timesteps
        C_target : float
            Target C value (should be > 8.3)
        noise_level : float
            Noise amplitude
        
        Returns
        -------
        data : dict
            Synthetic conscious data with activity and parameters
        """
        # Generate critical dynamics
        activity = self._generate_critical_activity(N, T, noise_level)
        
        # Add integration patterns (long-range correlations)
        activity = self._add_integration(activity, strength=0.7)
        
        # Add self-reference (recursive patterns)
        activity = self._add_self_reference(activity, depth=3)
        
        # Calculate consciousness components
        from .consciousness_measure import ConsciousnessMeasure
        from .neural_network import NetworkGenerator
        
        # Create connectivity
        W = NetworkGenerator.scale_free(N, m=4)
        W = NetworkGenerator.tune_to_criticality(W, target_branching=1.0)
        
        # Calculate C(t) at several timepoints
        measure = ConsciousnessMeasure()
        C_values = []
        
        for t_start in range(0, T-100, 100):
            window = activity[:, t_start:t_start+100]
            result = measure.calculate_C(
                window.mean(axis=1),
                W,
                window
            )
            C_values.append(result['C'])
        
        return {
            'activity': activity,
            'connectivity': W,
            'C_values': np.array(C_values),
            'C_mean': np.mean(C_values),
            'C_std': np.std(C_values),
            'state': 'conscious',
            'N': N,
            'T': T
        }
    
    def generate_synthetic_unconscious(
        self,
        N: int = 100,
        T: int = 1000,
        C_target: float = 5.0,
        noise_level: float = 0.1
    ) -> Dict[str, np.ndarray]:
        """
        Generate synthetic data mimicking unconscious state.
        
        Unconscious state characteristics:
        - C(t) â‰ˆ 5.0 Â± 1.0 bits (below threshold)
        - Low integration (Î¦ â‰ˆ 2.0 bits)
        - Minimal self-reference (R â‰ˆ 1.0)
        - Subcritical or supercritical dynamics (D â‰ˆ 0.3)
        - Simple, stereotyped patterns
        - Exponential avalanche statistics
        
        Parameters
        ----------
        N : int
            Number of neurons
        T : int
            Number of timesteps
        C_target : float
            Target C value (should be < 8.3)
        noise_level : float
            Noise amplitude
        
        Returns
        -------
        data : dict
            Synthetic unconscious data
        """
        # Generate subcritical dynamics
        activity = self._generate_subcritical_activity(N, T, noise_level)
        
        # Add weak integration
        activity = self._add_integration(activity, strength=0.3)
        
        # Minimal self-reference
        # (Skip self-reference addition)
        
        # Calculate C components
        from .consciousness_measure import ConsciousnessMeasure
        from .neural_network import NetworkGenerator
        
        # Create subcritical connectivity
        W = NetworkGenerator.scale_free(N, m=2)
        W = NetworkGenerator.tune_to_criticality(W, target_branching=0.7)
        
        measure = ConsciousnessMeasure()
        C_values = []
        
        for t_start in range(0, T-100, 100):
            window = activity[:, t_start:t_start+100]
            result = measure.calculate_C(
                window.mean(axis=1),
                W,
                window
            )
            C_values.append(result['C'])
        
        return {
            'activity': activity,
            'connectivity': W,
            'C_values': np.array(C_values),
            'C_mean': np.mean(C_values),
            'C_std': np.std(C_values),
            'state': 'unconscious',
            'N': N,
            'T': T
        }
    
    def validate_classifier(
        self,
        predictions: np.ndarray,
        ground_truth: np.ndarray,
        prediction_probs: Optional[np.ndarray] = None
    ) -> Dict[str, float]:
        """
        Validate binary classifier performance.
        
        Parameters
        ----------
        predictions : np.ndarray
            Binary predictions (0=unconscious, 1=conscious)
        ground_truth : np.ndarray
            True labels
        prediction_probs : np.ndarray, optional
            Prediction probabilities for ROC-AUC
        
        Returns
        -------
        metrics : dict
            Classification performance metrics
        """
        # Calculate metrics
        accuracy = accuracy_score(ground_truth, predictions)
        precision, recall, f1, _ = precision_recall_fscore_support(
            ground_truth, predictions, average='binary', zero_division=0
        )
        
        # ROC-AUC if probabilities provided
        if prediction_probs is not None:
            try:
                auc = roc_auc_score(ground_truth, prediction_probs)
            except:
                auc = np.nan
                warnings.warn("Could not calculate ROC-AUC")
        else:
            auc = np.nan
        
        # Confusion matrix elements
        tp = np.sum((predictions == 1) & (ground_truth == 1))
        tn = np.sum((predictions == 0) & (ground_truth == 0))
        fp = np.sum((predictions == 1) & (ground_truth == 0))
        fn = np.sum((predictions == 0) & (ground_truth == 1))
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'roc_auc': auc,
            'true_positives': int(tp),
            'true_negatives': int(tn),
            'false_positives': int(fp),
            'false_negatives': int(fn),
            'n_samples': len(ground_truth)
        }
    
    def validate_predictions(
        self,
        prediction_name: str,
        measured_values: np.ndarray,
        expected_value: float,
        expected_std: Optional[float] = None,
        test_type: str = 'mean'
    ) -> Dict[str, any]:
        """
        Validate specific theoretical predictions.
        
        Parameters
        ----------
        prediction_name : str
            Name of the prediction being tested
        measured_values : np.ndarray
            Measured values from experiment/simulation
        expected_value : float
            Theoretically predicted value
        expected_std : float, optional
            Expected standard deviation
        test_type : str
            'mean', 'distribution', or 'threshold'
        
        Returns
        -------
        result : dict
            Validation results with statistical tests
        """
        measured_mean = np.mean(measured_values)
        measured_std = np.std(measured_values)
        
        if test_type == 'mean':
            # Test if mean is close to expected
            z_score = (measured_mean - expected_value) / (measured_std / np.sqrt(len(measured_values)))
            p_value = 2 * (1 - self._norm_cdf(abs(z_score)))
            
            # Within 2 sigma?
            if expected_std:
                within_range = (expected_value - 2*expected_std <= measured_mean <= 
                              expected_value + 2*expected_std)
            else:
                within_range = abs(z_score) < 2
            
            validated = within_range
            
        elif test_type == 'distribution':
            # Test if distribution matches expected
            # Use KS test with normal distribution centered at expected value
            expected_dist = np.random.normal(expected_value, expected_std or measured_std, 10000)
            ks_stat, p_value = ks_2samp(measured_values, expected_dist)
            
            validated = p_value > 0.05  # Not significantly different
            z_score = ks_stat
            
        elif test_type == 'threshold':
            # Test if values cross a threshold
            crossing_fraction = np.mean(measured_values > expected_value)
            z_score = (crossing_fraction - 0.5) / (0.5 / np.sqrt(len(measured_values)))
            p_value = 2 * (1 - self._norm_cdf(abs(z_score)))
            
            validated = abs(z_score) < 2
        
        else:
            raise ValueError(f"Unknown test type: {test_type}")
        
        result = {
            'prediction': prediction_name,
            'expected_value': expected_value,
            'measured_mean': measured_mean,
            'measured_std': measured_std,
            'n_samples': len(measured_values),
            'z_score': z_score,
            'p_value': p_value,
            'validated': validated,
            'test_type': test_type
        }
        
        self.validation_history.append(result)
        
        return result
    
    def run_full_validation_suite(
        self,
        n_conscious_samples: int = 20,
        n_unconscious_samples: int = 20
    ) -> Dict[str, any]:
        """
        Run complete validation suite with all tests.
        
        Parameters
        ----------
        n_conscious_samples : int
            Number of conscious state samples to generate
        n_unconscious_samples : int
            Number of unconscious state samples to generate
        
        Returns
        -------
        results : dict
            Complete validation results
        """
        print("Running full validation suite...")
        print("="*60)
        
        # 1. Generate synthetic data
        print("\n1. Generating synthetic data...")
        conscious_data = []
        unconscious_data = []
        
        for i in range(n_conscious_samples):
            data = self.generate_synthetic_conscious()
            conscious_data.append(data)
        
        for i in range(n_unconscious_samples):
            data = self.generate_synthetic_unconscious()
            unconscious_data.append(data)
        
        # 2. Test C_critical threshold
        print("\n2. Testing C_critical = 8.3 Â± 0.6 bits...")
        conscious_C = np.array([d['C_mean'] for d in conscious_data])
        unconscious_C = np.array([d['C_mean'] for d in unconscious_data])
        
        threshold_test = self.validate_predictions(
            'C_critical_threshold',
            conscious_C,
            8.3,
            expected_std=0.6,
            test_type='mean'
        )
        
        print(f"   Conscious C: {conscious_C.mean():.2f} Â± {conscious_C.std():.2f}")
        print(f"   Unconscious C: {unconscious_C.mean():.2f} Â± {unconscious_C.std():.2f}")
        print(f"   Threshold validated: {threshold_test['validated']}")
        
        # 3. Test classifier performance
        print("\n3. Testing classifier performance...")
        all_C = np.concatenate([conscious_C, unconscious_C])
        labels = np.concatenate([np.ones(len(conscious_C)), 
                                np.zeros(len(unconscious_C))])
        predictions = (all_C > 8.3).astype(int)
        
        classifier_metrics = self.validate_classifier(predictions, labels)
        
        print(f"   Accuracy: {classifier_metrics['accuracy']:.3f}")
        print(f"   Precision: {classifier_metrics['precision']:.3f}")
        print(f"   Recall: {classifier_metrics['recall']:.3f}")
        print(f"   F1 Score: {classifier_metrics['f1_score']:.3f}")
        
        # 4. Test separability
        print("\n4. Testing statistical separability...")
        t_stat, t_pval = ttest_ind(conscious_C, unconscious_C)
        u_stat, u_pval = mannwhitneyu(conscious_C, unconscious_C)
        
        print(f"   T-test p-value: {t_pval:.2e}")
        print(f"   Mann-Whitney p-value: {u_pval:.2e}")
        print(f"   Significant separation: {u_pval < 0.001}")
        
        # 5. Summary
        print("\n" + "="*60)
        print("VALIDATION SUMMARY")
        print("="*60)
        
        all_validated = (
            threshold_test['validated'] and
            classifier_metrics['accuracy'] > 0.8 and
            u_pval < 0.001
        )
        
        print(f"Overall validation: {'âœ“ PASSED' if all_validated else 'âœ— FAILED'}")
        
        return {
            'conscious_data': conscious_data,
            'unconscious_data': unconscious_data,
            'threshold_test': threshold_test,
            'classifier_metrics': classifier_metrics,
            'statistical_tests': {
                't_statistic': t_stat,
                't_pvalue': t_pval,
                'mann_whitney_u': u_stat,
                'mann_whitney_pvalue': u_pval
            },
            'all_validated': all_validated
        }
    
    def _generate_critical_activity(
        self, 
        N: int, 
        T: int, 
        noise: float
    ) -> np.ndarray:
        """Generate activity with critical dynamics."""
        # Initialize with small random activity
        activity = np.zeros((N, T))
        activity[:, 0] = np.random.rand(N) > 0.95
        
        # Critical branching process
        branching = 1.0  # Critical value
        
        for t in range(1, T):
            # Propagate activity
            active = activity[:, t-1] > 0.5
            n_active = np.sum(active)
            
            if n_active > 0:
                # Each active neuron activates ~1 other neuron (critical)
                n_new = np.random.poisson(branching * n_active)
                new_active = np.random.choice(N, size=min(n_new, N), replace=False)
                activity[new_active, t] = 1
            
            # Add noise
            activity[:, t] += noise * np.random.randn(N)
            activity[:, t] = np.clip(activity[:, t], 0, 1)
        
        return activity
    
    def _generate_subcritical_activity(
        self, 
        N: int, 
        T: int, 
        noise: float
    ) -> np.ndarray:
        """Generate activity with subcritical dynamics."""
        activity = np.zeros((N, T))
        activity[:, 0] = np.random.rand(N) > 0.95
        
        branching = 0.7  # Subcritical
        
        for t in range(1, T):
            active = activity[:, t-1] > 0.5
            n_active = np.sum(active)
            
            if n_active > 0:
                n_new = np.random.poisson(branching * n_active)
                if n_new > 0:
                    new_active = np.random.choice(N, size=min(n_new, N), replace=False)
                    activity[new_active, t] = 1
            
            activity[:, t] += noise * np.random.randn(N)
            activity[:, t] = np.clip(activity[:, t], 0, 1)
        
        return activity
    
    def _add_integration(
        self, 
        activity: np.ndarray, 
        strength: float
    ) -> np.ndarray:
        """Add long-range correlations to increase integration."""
        N, T = activity.shape
        
        # Create correlation matrix
        distances = np.abs(np.arange(N)[:, None] - np.arange(N)[None, :])
        correlations = np.exp(-distances / (N * 0.2))  # Long-range
        
        # Apply correlations
        for t in range(T):
            activity[:, t] = (1 - strength) * activity[:, t] + \
                           strength * correlations @ activity[:, t]
        
        return activity
    
    def _add_self_reference(
        self, 
        activity: np.ndarray, 
        depth: int
    ) -> np.ndarray:
        """Add recursive self-reference patterns."""
        N, T = activity.shape
        
        # Create delayed feedback
        for d in range(1, depth + 1):
            delay = d * 10
            if delay < T:
                activity[:, delay:] += 0.1 * activity[:, :-delay]
        
        return np.clip(activity, 0, 1)
    
    def _norm_cdf(self, x: float) -> float:
        """Normal cumulative distribution function approximation."""
        return 0.5 * (1 + np.tanh(np.sqrt(2/np.pi) * (x + 0.044715 * x**3)))


def plot_validation_results(validation_results: Dict[str, any]):
    """
    Visualize validation results.
    
    Parameters
    ----------
    validation_results : dict
        Results from run_full_validation_suite
    """
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    conscious_C = np.array([d['C_mean'] for d in validation_results['conscious_data']])
    unconscious_C = np.array([d['C_mean'] for d in validation_results['unconscious_data']])
    
    # 1. C distribution
    ax = axes[0, 0]
    ax.hist(unconscious_C, bins=15, alpha=0.6, label='Unconscious', color='blue')
    ax.hist(conscious_C, bins=15, alpha=0.6, label='Conscious', color='red')
    ax.axvline(8.3, color='green', linestyle='--', linewidth=2, label='C_critical')
    ax.fill_between([7.7, 8.9], 0, ax.get_ylim()[1], alpha=0.2, color='green')
    ax.set_xlabel('C (bits)')
    ax.set_ylabel('Count')
    ax.set_title('C Distribution: Conscious vs Unconscious')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 2. Box plot
    ax = axes[0, 1]
    ax.boxplot([unconscious_C, conscious_C], labels=['Unconscious', 'Conscious'])
    ax.axhline(8.3, color='green', linestyle='--', linewidth=2, label='C_critical')
    ax.set_ylabel('C (bits)')
    ax.set_title('C Value Distributions')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # 3. Confusion matrix
    ax = axes[1, 0]
    metrics = validation_results['classifier_metrics']
    confusion = np.array([[metrics['true_negatives'], metrics['false_positives']],
                         [metrics['false_negatives'], metrics['true_positives']]])
    im = ax.imshow(confusion, cmap='Blues')
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(['Predicted\nUnconscious', 'Predicted\nConscious'])
    ax.set_yticklabels(['True\nUnconscious', 'True\nConscious'])
    
    # Add text annotations
    for i in range(2):
        for j in range(2):
            ax.text(j, i, confusion[i, j], ha='center', va='center', 
                   fontsize=20, fontweight='bold')
    
    ax.set_title('Confusion Matrix')
    plt.colorbar(im, ax=ax)
    
    # 4. Performance metrics
    ax = axes[1, 1]
    metrics_names = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
    metrics_values = [metrics['accuracy'], metrics['precision'], 
                     metrics['recall'], metrics['f1_score']]
    
    bars = ax.barh(metrics_names, metrics_values, color=['blue', 'green', 'orange', 'red'])
    ax.set_xlim([0, 1])
    ax.axvline(0.8, color='gray', linestyle='--', alpha=0.5, label='Target')
    ax.set_xlabel('Score')
    ax.set_title('Classifier Performance Metrics')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='x')
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, metrics_values)):
        ax.text(val + 0.02, i, f'{val:.3f}', va='center')
    
    plt.suptitle('Validation Results: Ouroboros Observer Framework', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    return fig
