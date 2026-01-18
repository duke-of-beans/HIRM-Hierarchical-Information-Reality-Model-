"""
Validation Framework for Ouroboros Observer

Generate synthetic data and validate predictions against theory.
"""

import numpy as np
from typing import Dict, Tuple, Optional
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix


class ValidationFramework:
    """
    Test predictions using synthetic data with known properties.
    
    Parameters
    ----------
    seed : int, optional
        Random seed for reproducibility
    """
    
    def __init__(self, seed: Optional[int] = None):
        self.seed = seed
        if seed is not None:
            np.random.seed(seed)
    
    def generate_synthetic_conscious(self, N_neurons: int = 100,
                                    duration: float = 5000.0,
                                    dt: float = 0.1) -> Dict:
        """
        Generate synthetic data mimicking conscious state.
        
        Properties:
        - Critical dynamics (sigma ~ 1.0)
        - High integration
        - Strong self-reference patterns
        - C(t) > C_critical
        
        Parameters
        ----------
        N_neurons : int
            Network size
        duration : float
            Duration (ms)
        dt : float
            Time step (ms)
        
        Returns
        -------
        dict
            Synthetic data with activity, connectivity, and components
        """
        from ..core.neural_network import NeuralNetwork, NeuronParams, SynapseParams
        
        # Configure for critical, integrated dynamics
        neuron_params = NeuronParams(
            tau_m=20.0,
            V_threshold=-50.0,
            R_m=10.0
        )
        
        synapse_params = SynapseParams(
            J_exc=0.15,  # Strong excitation
            J_inh=-0.6,
            p_exc=0.8
        )
        
        # Create network
        network = NeuralNetwork(
            N_neurons,
            neuron_params=neuron_params,
            synapse_params=synapse_params,
            dt=dt,
            seed=self.seed
        )
        
        # Tune to criticality
        network.tune_to_criticality(target_rate=5.0, iterations=50)
        
        # Run with moderate external input
        I_ext = np.random.randn(N_neurons) * 2.0 + 5.0
        results = network.run(duration, I_ext=I_ext)
        
        data = {
            'activity': np.array(results['spikes']),
            'connectivity': network.W,
            'time': results['time'],
            'label': 'conscious',
            'expected_C': 10.0  # Above critical
        }
        
        return data
    
    def generate_synthetic_unconscious(self, N_neurons: int = 100,
                                      duration: float = 5000.0,
                                      dt: float = 0.1) -> Dict:
        """
        Generate synthetic data mimicking unconscious state.
        
        Properties:
        - Subcritical dynamics
        - Low integration
        - Weak self-reference
        - C(t) < C_critical
        
        Parameters
        ----------
        N_neurons : int
            Network size
        duration : float
            Duration (ms)
        dt : float
            Time step (ms)
        
        Returns
        -------
        dict
            Synthetic data
        """
        from ..core.neural_network import NeuralNetwork, NeuronParams, SynapseParams
        
        # Configure for subcritical dynamics
        neuron_params = NeuronParams(
            tau_m=20.0,
            V_threshold=-45.0,  # Higher threshold
            R_m=10.0
        )
        
        synapse_params = SynapseParams(
            J_exc=0.05,  # Weak excitation
            J_inh=-0.3,
            p_exc=0.8
        )
        
        network = NeuralNetwork(
            N_neurons,
            neuron_params=neuron_params,
            synapse_params=synapse_params,
            dt=dt,
            seed=self.seed
        )
        
        # Weak external input
        I_ext = np.random.randn(N_neurons) * 0.5 + 1.0
        results = network.run(duration, I_ext=I_ext)
        
        data = {
            'activity': np.array(results['spikes']),
            'connectivity': network.W,
            'time': results['time'],
            'label': 'unconscious',
            'expected_C': 4.0  # Below critical
        }
        
        return data
    
    def validate_classifier(self, predictions: np.ndarray,
                          ground_truth: np.ndarray,
                          C_values: Optional[np.ndarray] = None) -> Dict:
        """
        Calculate classification performance metrics.
        
        Parameters
        ----------
        predictions : np.ndarray
            Binary predictions (conscious=1, unconscious=0)
        ground_truth : np.ndarray
            True labels
        C_values : np.ndarray, optional
            Continuous C(t) values for ROC analysis
        
        Returns
        -------
        dict
            Performance metrics
        """
        accuracy = accuracy_score(ground_truth, predictions)
        
        # Confusion matrix
        cm = confusion_matrix(ground_truth, predictions)
        tn, fp, fn, tp = cm.ravel()
        
        sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        
        results = {
            'accuracy': accuracy,
            'sensitivity': sensitivity,
            'specificity': specificity,
            'confusion_matrix': cm,
            'true_positives': int(tp),
            'false_positives': int(fp),
            'true_negatives': int(tn),
            'false_negatives': int(fn)
        }
        
        if C_values is not None:
            auc = roc_auc_score(ground_truth, C_values)
            results['auc'] = auc
        
        return results
    
    def test_transition_prediction(self, n_trials: int = 10) -> Dict:
        """
        Test prediction that C_critical â‰ˆ 8.3 bits.
        
        Generate multiple transition events and measure C_critical.
        
        Parameters
        ----------
        n_trials : int
            Number of transition trials
        
        Returns
        -------
        dict
            Transition analysis results
        """
        from ..core.consciousness_measure import ConsciousnessMeasure
        from ..core.phase_transition import BifurcationDetector
        
        C_criticals = []
        
        for trial in range(n_trials):
            # Generate gradual transition
            data = self._generate_transition_sequence()
            
            # Calculate C(t)
            measure = ConsciousnessMeasure()
            detector = BifurcationDetector()
            
            C_timeseries = []
            for t in range(len(data['activity'])):
                activity = data['activity'][t]
                history = data['activity'][max(0, t-50):t+1]
                
                C, _ = measure.calculate_C(
                    activity,
                    data['connectivity'],
                    history
                )
                C_timeseries.append(C)
            
            # Detect transitions
            transitions = detector.detect_transitions(
                np.array(C_timeseries),
                np.arange(len(C_timeseries))
            )
            
            if transitions:
                # Record C at transition
                C_criticals.append(transitions[0].C_after)
        
        results = {
            'n_trials': n_trials,
            'C_criticals': C_criticals,
            'mean_C_critical': np.mean(C_criticals),
            'std_C_critical': np.std(C_criticals),
            'theoretical_C_critical': 8.3,
            'deviation': abs(np.mean(C_criticals) - 8.3)
        }
        
        return results
    
    def _generate_transition_sequence(self) -> Dict:
        """Generate activity sequence with gradual transition."""
        from ..core.neural_network import NeuralNetwork
        
        N = 100
        network = NeuralNetwork(N, seed=self.seed)
        
        # Gradually increase input to induce transition
        duration = 10000.0
        n_steps = int(duration / network.dt)
        
        activity_sequence = []
        
        for step in range(n_steps):
            # Ramp input
            input_strength = 1.0 + 10.0 * (step / n_steps)
            I_ext = np.random.randn(N) * 1.0 + input_strength
            
            network.step(I_ext)
            activity_sequence.append(network.get_activity())
        
        return {
            'activity': np.array(activity_sequence),
            'connectivity': network.W
        }
    
    def test_branch_number(self, n_trials: int = 5) -> Dict:
        """
        Test prediction that 4-5 branches emerge post-transition.
        
        Parameters
        ----------
        n_trials : int
            Number of trials
        
        Returns
        -------
        dict
            Branch analysis results
        """
        from ..core.phase_transition import BifurcationDetector
        
        branch_counts = []
        
        for trial in range(n_trials):
            # Generate post-transition data
            data = self.generate_synthetic_conscious(duration=5000.0)
            
            detector = BifurcationDetector()
            
            # Analyze branches
            branch_analysis = detector.analyze_branches(
                np.ones(len(data['activity'])) * 10.0,  # Supercritical C
                data['activity'],
                (0, len(data['activity']))
            )
            
            branch_counts.append(branch_analysis['n_branches'])
        
        results = {
            'n_trials': n_trials,
            'branch_counts': branch_counts,
            'mean_branches': np.mean(branch_counts),
            'std_branches': np.std(branch_counts),
            'theoretical_range': (4, 5),
            'in_range': all(4 <= b <= 5 for b in branch_counts)
        }
        
        return results
    
    def comprehensive_validation(self) -> Dict:
        """
        Run comprehensive validation suite.
        
        Returns
        -------
        dict
            All validation results
        """
        print("Running comprehensive validation...")
        
        # Test 1: Binary classification
        print("Test 1: Binary classification...")
        conscious_data = self.generate_synthetic_conscious()
        unconscious_data = self.generate_synthetic_unconscious()
        
        from ..core.consciousness_measure import ConsciousnessMeasure
        measure = ConsciousnessMeasure()
        
        # Calculate C for both
        C_conscious, _ = measure.calculate_C(
            conscious_data['activity'][-1],
            conscious_data['connectivity'],
            conscious_data['activity'][-100:]
        )
        
        C_unconscious, _ = measure.calculate_C(
            unconscious_data['activity'][-1],
            unconscious_data['connectivity'],
            unconscious_data['activity'][-100:]
        )
        
        predictions = np.array([C_conscious > 8.3, C_unconscious > 8.3])
        ground_truth = np.array([1, 0])
        
        classification_results = self.validate_classifier(
            predictions, ground_truth,
            C_values=np.array([C_conscious, C_unconscious])
        )
        
        # Test 2: C_critical value
        print("Test 2: C_critical value...")
        transition_results = self.test_transition_prediction(n_trials=5)
        
        # Test 3: Branch number
        print("Test 3: Branch number...")
        branch_results = self.test_branch_number(n_trials=3)
        
        return {
            'classification': classification_results,
            'C_critical': transition_results,
            'branches': branch_results
        }
