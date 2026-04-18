"""
Self-Reference Engine
====================

Simulate self-referential information processing including recursive 
self-modeling, strange loop dynamics, and fixed-point convergence.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Callable
from dataclasses import dataclass
import warnings


@dataclass
class SelfReferenceConfig:
    """Configuration for self-reference simulation."""
    max_recursion_depth: int = 10
    convergence_threshold: float = 0.01
    update_rate: float = 0.1
    noise_level: float = 0.01


class SelfReferenceEngine:
    """
    Simulate self-referential information processing.
    
    Implements recursive self-modeling where the system maintains
    an internal model of itself and updates it based on observations.
    
    Parameters
    ----------
    state_dim : int
        Dimensionality of system state
    config : SelfReferenceConfig, optional
        Configuration parameters
    
    Attributes
    ----------
    state : np.ndarray
        Current state of the system
    model : np.ndarray
        Internal model of the state
    recursion_history : list
        History of recursive depth at each timestep
    """
    
    def __init__(
        self,
        state_dim: int,
        config: Optional[SelfReferenceConfig] = None
    ):
        self.state_dim = state_dim
        self.config = config or SelfReferenceConfig()
        
        # Initialize state and model
        self.state = np.random.randn(state_dim)
        self.model = np.zeros(state_dim)
        
        # Tracking
        self.recursion_history = []
        self.model_history = []
        self.convergence_history = []
        self.time = 0
    
    def step_recursion(
        self, 
        observed_activity: np.ndarray,
        dynamics_function: Optional[Callable] = None
    ) -> Dict[str, np.ndarray]:
        """
        Execute one step of self-modeling recursion.
        
        The system:
        1. Observes its current activity
        2. Updates its internal model
        3. Predicts next state
        4. Compares prediction to observation (error signal)
        
        Parameters
        ----------
        observed_activity : np.ndarray
            Externally observed activity pattern
        dynamics_function : callable, optional
            Function that generates next state: f(state, model)
        
        Returns
        -------
        result : dict
            Updated state, model, and diagnostics
        """
        # Default dynamics: simple autoregressive with self-reference
        if dynamics_function is None:
            dynamics_function = self._default_dynamics
        
        # Recursive self-modeling
        model_error = observed_activity - self.model
        
        # Update model with error correction
        self.model += self.config.update_rate * model_error
        
        # Add noise for realistic dynamics
        self.model += self.config.noise_level * np.random.randn(self.state_dim)
        
        # Update state using dynamics function
        self.state = dynamics_function(observed_activity, self.model)
        
        # Calculate recursive depth for this step
        depth = self._measure_recursive_depth()
        
        # Check convergence
        convergence = np.linalg.norm(model_error) / (np.linalg.norm(observed_activity) + 1e-10)
        
        # Store history
        self.recursion_history.append(depth)
        self.model_history.append(self.model.copy())
        self.convergence_history.append(convergence)
        self.time += 1
        
        return {
            'state': self.state.copy(),
            'model': self.model.copy(),
            'model_error': model_error,
            'recursion_depth': depth,
            'convergence': convergence
        }
    
    def _default_dynamics(
        self, 
        observed: np.ndarray, 
        model: np.ndarray
    ) -> np.ndarray:
        """
        Default dynamics incorporating self-reference.
        
        Next state depends on both observation and internal model.
        """
        # Weighted combination
        alpha = 0.7  # Weight on observation
        beta = 0.3   # Weight on model (self-reference)
        
        next_state = alpha * observed + beta * model
        
        # Add nonlinearity (tanh for bounded dynamics)
        next_state = np.tanh(next_state)
        
        return next_state
    
    def _measure_recursive_depth(self) -> int:
        """
        Measure current recursive depth.
        
        Depth is determined by how many levels of self-modeling
        are currently active (non-convergent).
        """
        if len(self.model_history) < 2:
            return 1
        
        # Compare recent model evolution
        recent_models = self.model_history[-min(5, len(self.model_history)):]
        
        # Calculate differences between consecutive models
        diffs = [np.linalg.norm(recent_models[i+1] - recent_models[i]) 
                for i in range(len(recent_models) - 1)]
        
        # Depth relates to number of significant changes
        significant_changes = sum(d > self.config.convergence_threshold 
                                 for d in diffs)
        
        depth = min(significant_changes + 1, self.config.max_recursion_depth)
        
        return depth
    
    def check_convergence(self, window: int = 20) -> Dict[str, any]:
        """
        Test for fixed-point convergence.
        
        A fixed point is reached when the model no longer changes
        significantly over time.
        
        Parameters
        ----------
        window : int
            Number of recent timesteps to analyze
        
        Returns
        -------
        result : dict
            Convergence status and diagnostics
        """
        if len(self.model_history) < window:
            return {
                'converged': False,
                'reason': 'insufficient_history',
                'window_size': len(self.model_history)
            }
        
        # Get recent history
        recent = self.model_history[-window:]
        
        # Calculate variance across time
        model_variance = np.var([np.linalg.norm(m) for m in recent])
        
        # Calculate mean change rate
        changes = [np.linalg.norm(recent[i+1] - recent[i]) 
                  for i in range(len(recent) - 1)]
        mean_change = np.mean(changes)
        
        # Convergence criteria
        converged = (model_variance < self.config.convergence_threshold and
                    mean_change < self.config.convergence_threshold)
        
        # If converged, identify the fixed point
        if converged:
            fixed_point = np.mean(recent, axis=0)
        else:
            fixed_point = None
        
        return {
            'converged': converged,
            'model_variance': model_variance,
            'mean_change_rate': mean_change,
            'fixed_point': fixed_point,
            'convergence_time': self.time if converged else None
        }
    
    def measure_strange_loop_strength(self) -> float:
        """
        Quantify strength of strange loop (self-reference closure).
        
        A strange loop occurs when the model of the system influences
        the system itself, creating a closed causal loop.
        
        Returns
        -------
        loop_strength : float
            Measure of strange loop strength (0 to 1)
        """
        if len(self.model_history) < 10:
            return 0.0
        
        # Correlation between model and subsequent state
        recent_models = np.array(self.model_history[-10:])
        recent_states = [self.state] + [m for m in self.model_history[-9:]]
        recent_states = np.array(recent_states)
        
        # Calculate lagged correlation
        correlations = []
        for lag in range(1, 4):
            if lag < len(recent_models):
                corr = np.corrcoef(
                    recent_models[:-lag].flatten(),
                    recent_states[lag:].flatten()
                )[0, 1]
                correlations.append(abs(corr))
        
        # Strong strange loop = high lagged correlation
        loop_strength = np.mean(correlations) if correlations else 0.0
        
        return np.clip(loop_strength, 0, 1)
    
    def simulate_recursive_collapse(
        self,
        n_steps: int = 100,
        external_input: Optional[np.ndarray] = None
    ) -> Dict[str, np.ndarray]:
        """
        Simulate recursive self-modeling leading to collapse/convergence.
        
        Parameters
        ----------
        n_steps : int
            Number of simulation steps
        external_input : np.ndarray, optional
            External driving input (state_dim, n_steps)
        
        Returns
        -------
        results : dict
            Time series of state, model, depth, convergence
        """
        # Initialize storage
        states = np.zeros((n_steps, self.state_dim))
        models = np.zeros((n_steps, self.state_dim))
        depths = np.zeros(n_steps)
        convergences = np.zeros(n_steps)
        
        # Generate external input if not provided
        if external_input is None:
            external_input = 0.5 * np.random.randn(self.state_dim, n_steps)
        
        # Run simulation
        for t in range(n_steps):
            # Observed activity combines current state with external input
            observed = self.state + external_input[:, t]
            
            # Step recursion
            result = self.step_recursion(observed)
            
            # Store results
            states[t] = result['state']
            models[t] = result['model']
            depths[t] = result['recursion_depth']
            convergences[t] = result['convergence']
        
        # Check final convergence
        final_convergence = self.check_convergence()
        
        return {
            'states': states,
            'models': models,
            'depths': depths,
            'convergences': convergences,
            'final_convergence': final_convergence,
            'mean_depth': np.mean(depths),
            'loop_strength': self.measure_strange_loop_strength()
        }
    
    def reset(self):
        """Reset to initial conditions."""
        self.state = np.random.randn(self.state_dim)
        self.model = np.zeros(self.state_dim)
        self.recursion_history = []
        self.model_history = []
        self.convergence_history = []
        self.time = 0


class MetaSelfReference:
    """
    Higher-order self-reference: modeling the modeling process itself.
    
    This implements "meta-cognition" where the system not only models
    itself but also models its own modeling process.
    """
    
    def __init__(self, state_dim: int, meta_levels: int = 3):
        self.state_dim = state_dim
        self.meta_levels = meta_levels
        
        # Create hierarchy of self-reference engines
        self.levels = [SelfReferenceEngine(state_dim) 
                      for _ in range(meta_levels)]
        
        self.time = 0
    
    def step(self, external_observation: np.ndarray) -> Dict[str, any]:
        """
        Execute one step of hierarchical self-reference.
        
        Level 0: Models external world
        Level 1: Models Level 0's modeling process
        Level 2: Models Level 1's modeling process
        etc.
        """
        results = []
        
        # Bottom level: observe external world
        result_0 = self.levels[0].step_recursion(external_observation)
        results.append(result_0)
        
        # Higher levels: observe lower level's model
        for i in range(1, self.meta_levels):
            lower_model = results[i-1]['model']
            result_i = self.levels[i].step_recursion(lower_model)
            results.append(result_i)
        
        self.time += 1
        
        # Calculate total recursive depth (sum across levels)
        total_depth = sum(r['recursion_depth'] for r in results)
        
        return {
            'level_results': results,
            'total_depth': total_depth,
            'top_level_model': results[-1]['model'],
            'time': self.time
        }
    
    def measure_hierarchical_integration(self) -> float:
        """
        Measure how well integrated the hierarchical levels are.
        
        High integration = levels are strongly coupled
        Low integration = levels operate independently
        """
        if self.time < 10:
            return 0.0
        
        # Correlation between adjacent levels
        correlations = []
        for i in range(self.meta_levels - 1):
            if len(self.levels[i].model_history) >= 5:
                model_i = np.array(self.levels[i].model_history[-5:])
                model_j = np.array(self.levels[i+1].model_history[-5:])
                
                corr = np.corrcoef(model_i.flatten(), model_j.flatten())[0, 1]
                correlations.append(abs(corr))
        
        integration = np.mean(correlations) if correlations else 0.0
        return integration


def visualize_recursive_dynamics(
    results: Dict[str, np.ndarray],
    figsize: Tuple[int, int] = (14, 10)
):
    """
    Visualize recursive self-reference dynamics.
    
    Parameters
    ----------
    results : dict
        Output from simulate_recursive_collapse
    figsize : tuple
        Figure dimensions
    """
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    
    n_steps = len(results['depths'])
    time = np.arange(n_steps)
    
    # 1. State and model evolution
    ax = axes[0, 0]
    # Plot first 3 dimensions for visualization
    for i in range(min(3, results['states'].shape[1])):
        ax.plot(time, results['states'][:, i], '-', 
               label=f'State dim {i}', alpha=0.7)
        ax.plot(time, results['models'][:, i], '--', 
               label=f'Model dim {i}', alpha=0.7)
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    ax.set_title('State and Model Evolution')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 2. Recursive depth
    ax = axes[0, 1]
    ax.plot(time, results['depths'], 'b-', linewidth=2)
    ax.fill_between(time, 0, results['depths'], alpha=0.3)
    ax.set_xlabel('Time')
    ax.set_ylabel('Recursive Depth')
    ax.set_title('Self-Reference Depth Over Time')
    ax.grid(True, alpha=0.3)
    
    # 3. Convergence
    ax = axes[1, 0]
    ax.semilogy(time, results['convergences'], 'r-', linewidth=2)
    ax.axhline(0.01, color='g', linestyle='--', label='Threshold')
    ax.set_xlabel('Time')
    ax.set_ylabel('Convergence Error (log scale)')
    ax.set_title('Convergence to Fixed Point')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 4. Phase space (first 2 dimensions)
    ax = axes[1, 1]
    if results['states'].shape[1] >= 2:
        scatter = ax.scatter(results['states'][:, 0], 
                           results['states'][:, 1],
                           c=time, cmap='viridis', 
                           s=20, alpha=0.6)
        plt.colorbar(scatter, ax=ax, label='Time')
        
        # Mark start and end
        ax.plot(results['states'][0, 0], results['states'][0, 1], 
               'go', markersize=10, label='Start')
        ax.plot(results['states'][-1, 0], results['states'][-1, 1], 
               'ro', markersize=10, label='End')
        
        ax.set_xlabel('State Dimension 0')
        ax.set_ylabel('State Dimension 1')
        ax.set_title('Phase Space Trajectory')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    # Add summary text
    fig.suptitle(f'Recursive Self-Reference Dynamics\n' +
                f'Mean Depth: {results["mean_depth"]:.2f}, ' +
                f'Loop Strength: {results["loop_strength"]:.2f}, ' +
                f'Converged: {results["final_convergence"]["converged"]}',
                fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    return fig
