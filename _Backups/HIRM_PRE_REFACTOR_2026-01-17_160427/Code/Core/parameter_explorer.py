"""
Parameter Explorer
==================

Systematic parameter space exploration including grid search, random sampling,
sensitivity analysis, and optimization.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Callable, Union
from dataclasses import dataclass
import itertools
from tqdm import tqdm
import warnings


@dataclass
class ParameterRange:
    """Define a parameter range for exploration."""
    name: str
    values: Union[np.ndarray, List]
    log_scale: bool = False


class ParameterExplorer:
    """
    Explore parameter space systematically.
    
    Methods
    -------
    grid_search : Exhaustive grid search
    random_search : Random sampling
    sensitivity_analysis : One-at-a-time perturbations
    optimize : Find optimal parameters
    """
    
    def __init__(
        self,
        simulation_function: Callable,
        metric_function: Callable
    ):
        """
        Initialize parameter explorer.
        
        Parameters
        ----------
        simulation_function : callable
            Function that runs simulation: f(params) -> results
        metric_function : callable
            Function that evaluates results: f(results) -> score
        """
        self.simulate = simulation_function
        self.evaluate = metric_function
        
        self.results_history = []
    
    def grid_search(
        self,
        param_ranges: Dict[str, ParameterRange],
        n_trials: int = 1,
        parallel: bool = False
    ) -> Dict[str, any]:
        """
        Exhaustive parameter space exploration.
        
        Parameters
        ----------
        param_ranges : dict
            Dictionary of ParameterRange objects
        n_trials : int
            Number of repeated trials per parameter combination
        parallel : bool
            Whether to use parallel execution
        
        Returns
        -------
        results : dict
            Complete results for all parameter combinations
        """
        # Generate all combinations
        param_names = list(param_ranges.keys())
        param_values = [param_ranges[name].values for name in param_names]
        combinations = list(itertools.product(*param_values))
        
        n_combinations = len(combinations)
        print(f"Grid search: {n_combinations} parameter combinations")
        
        # Storage
        all_results = []
        all_scores = []
        all_params = []
        
        # Iterate through combinations
        for combo in tqdm(combinations, desc="Grid search"):
            # Create parameter dictionary
            params = {name: value for name, value in zip(param_names, combo)}
            
            # Run trials
            trial_scores = []
            trial_results = []
            
            for trial in range(n_trials):
                # Run simulation
                result = self.simulate(params)
                score = self.evaluate(result)
                
                trial_scores.append(score)
                trial_results.append(result)
            
            # Average over trials
            mean_score = np.mean(trial_scores)
            std_score = np.std(trial_scores)
            
            all_results.append(trial_results)
            all_scores.append((mean_score, std_score))
            all_params.append(params)
        
        # Find best parameters
        mean_scores = [s[0] for s in all_scores]
        best_idx = np.argmax(mean_scores)
        
        self.results_history.append({
            'method': 'grid_search',
            'all_params': all_params,
            'all_scores': all_scores,
            'best_params': all_params[best_idx],
            'best_score': all_scores[best_idx][0],
            'n_combinations': n_combinations
        })
        
        return {
            'all_params': all_params,
            'all_scores': all_scores,
            'best_params': all_params[best_idx],
            'best_score': all_scores[best_idx][0],
            'best_std': all_scores[best_idx][1],
            'mean_scores': mean_scores,
            'exploration_summary': self._summarize_exploration(
                all_params, mean_scores
            )
        }
    
    def random_search(
        self,
        param_distributions: Dict[str, Callable],
        n_samples: int = 100,
        n_trials: int = 1
    ) -> Dict[str, any]:
        """
        Random sampling of parameter space.
        
        Parameters
        ----------
        param_distributions : dict
            Dictionary of sampling functions for each parameter
        n_samples : int
            Number of random samples
        n_trials : int
            Number of repeated trials per sample
        
        Returns
        -------
        results : dict
            Results from random sampling
        """
        param_names = list(param_distributions.keys())
        
        all_results = []
        all_scores = []
        all_params = []
        
        print(f"Random search: {n_samples} samples")
        
        for _ in tqdm(range(n_samples), desc="Random search"):
            # Sample parameters
            params = {name: dist() for name, dist in param_distributions.items()}
            
            # Run trials
            trial_scores = []
            trial_results = []
            
            for trial in range(n_trials):
                result = self.simulate(params)
                score = self.evaluate(result)
                
                trial_scores.append(score)
                trial_results.append(result)
            
            mean_score = np.mean(trial_scores)
            std_score = np.std(trial_scores)
            
            all_results.append(trial_results)
            all_scores.append((mean_score, std_score))
            all_params.append(params)
        
        # Find best
        mean_scores = [s[0] for s in all_scores]
        best_idx = np.argmax(mean_scores)
        
        return {
            'all_params': all_params,
            'all_scores': all_scores,
            'best_params': all_params[best_idx],
            'best_score': all_scores[best_idx][0],
            'best_std': all_scores[best_idx][1],
            'mean_scores': mean_scores
        }
    
    def sensitivity_analysis(
        self,
        baseline_params: Dict[str, float],
        perturbation_factors: List[float] = [0.8, 0.9, 1.1, 1.2],
        n_trials: int = 3
    ) -> Dict[str, any]:
        """
        One-at-a-time sensitivity analysis.
        
        Parameters
        ----------
        baseline_params : dict
            Baseline parameter values
        perturbation_factors : list
            Multiplicative factors for perturbations
        n_trials : int
            Number of trials per perturbation
        
        Returns
        -------
        sensitivity : dict
            Sensitivity results for each parameter
        """
        param_names = list(baseline_params.keys())
        
        # Baseline score
        print("Calculating baseline...")
        baseline_results = []
        for _ in range(n_trials):
            result = self.simulate(baseline_params)
            score = self.evaluate(result)
            baseline_results.append(score)
        
        baseline_score = np.mean(baseline_results)
        baseline_std = np.std(baseline_results)
        
        print(f"Baseline score: {baseline_score:.4f} ± {baseline_std:.4f}")
        
        # Sensitivity analysis
        sensitivities = {}
        
        for param_name in tqdm(param_names, desc="Sensitivity analysis"):
            param_sensitivities = []
            
            for factor in perturbation_factors:
                # Perturb this parameter
                perturbed_params = baseline_params.copy()
                perturbed_params[param_name] *= factor
                
                # Run trials
                scores = []
                for _ in range(n_trials):
                    result = self.simulate(perturbed_params)
                    score = self.evaluate(result)
                    scores.append(score)
                
                mean_score = np.mean(scores)
                std_score = np.std(scores)
                
                # Calculate sensitivity (normalized score change)
                sensitivity = (mean_score - baseline_score) / baseline_score
                
                param_sensitivities.append({
                    'factor': factor,
                    'score': mean_score,
                    'std': std_score,
                    'sensitivity': sensitivity
                })
            
            # Overall sensitivity: variance of scores across perturbations
            scores_array = np.array([s['score'] for s in param_sensitivities])
            total_sensitivity = np.std(scores_array) / (baseline_score + 1e-10)
            
            sensitivities[param_name] = {
                'perturbations': param_sensitivities,
                'total_sensitivity': total_sensitivity
            }
        
        # Rank parameters by sensitivity
        ranking = sorted(
            param_names,
            key=lambda p: sensitivities[p]['total_sensitivity'],
            reverse=True
        )
        
        return {
            'baseline_score': baseline_score,
            'baseline_std': baseline_std,
            'sensitivities': sensitivities,
            'ranking': ranking,
            'most_sensitive': ranking[0] if ranking else None
        }
    
    def optimize(
        self,
        initial_params: Dict[str, float],
        param_bounds: Dict[str, Tuple[float, float]],
        method: str = 'nelder-mead',
        n_iterations: int = 100
    ) -> Dict[str, any]:
        """
        Optimize parameters to maximize metric.
        
        Parameters
        ----------
        initial_params : dict
            Starting parameter values
        param_bounds : dict
            Min and max values for each parameter
        method : str
            Optimization method: 'nelder-mead', 'powell', 'gradient'
        n_iterations : int
            Maximum number of iterations
        
        Returns
        -------
        results : dict
            Optimization results
        """
        from scipy.optimize import minimize
        
        param_names = list(initial_params.keys())
        
        # Convert to array form for scipy
        x0 = np.array([initial_params[name] for name in param_names])
        bounds = [param_bounds[name] for name in param_names]
        
        # Objective function (negative because scipy minimizes)
        def objective(x):
            params = {name: value for name, value in zip(param_names, x)}
            result = self.simulate(params)
            score = self.evaluate(result)
            return -score  # Negative for minimization
        
        # Optimize
        print(f"Optimizing with {method}...")
        
        if method == 'nelder-mead':
            result = minimize(
                objective, x0,
                method='Nelder-Mead',
                options={'maxiter': n_iterations}
            )
        elif method == 'powell':
            result = minimize(
                objective, x0,
                method='Powell',
                bounds=bounds,
                options={'maxiter': n_iterations}
            )
        else:
            raise ValueError(f"Unknown optimization method: {method}")
        
        # Extract optimal parameters
        optimal_params = {name: value 
                         for name, value in zip(param_names, result.x)}
        optimal_score = -result.fun  # Convert back to positive
        
        return {
            'optimal_params': optimal_params,
            'optimal_score': optimal_score,
            'initial_params': initial_params,
            'initial_score': -objective(x0),
            'n_iterations': result.nit,
            'success': result.success,
            'optimization_result': result
        }
    
    def _summarize_exploration(
        self,
        all_params: List[Dict],
        all_scores: List[float]
    ) -> Dict[str, any]:
        """Generate summary statistics for parameter exploration."""
        # Convert to structured form
        param_names = list(all_params[0].keys())
        
        summary = {
            'score_mean': np.mean(all_scores),
            'score_std': np.std(all_scores),
            'score_min': np.min(all_scores),
            'score_max': np.max(all_scores),
        }
        
        # Per-parameter statistics
        for param_name in param_names:
            values = [p[param_name] for p in all_params]
            
            # Correlation with score
            corr = np.corrcoef(values, all_scores)[0, 1]
            
            summary[f'{param_name}_correlation'] = corr
            summary[f'{param_name}_mean'] = np.mean(values)
            summary[f'{param_name}_std'] = np.std(values)
        
        return summary


def visualize_parameter_exploration(
    results: Dict[str, any],
    param_names: Optional[List[str]] = None,
    figsize: Tuple[int, int] = (14, 10)
):
    """
    Visualize parameter exploration results.
    
    Parameters
    ----------
    results : dict
        Results from grid_search or random_search
    param_names : list, optional
        Names of parameters to visualize
    figsize : tuple
        Figure size
    """
    import matplotlib.pyplot as plt
    
    all_params = results['all_params']
    all_scores = [s[0] if isinstance(s, tuple) else s 
                  for s in results['all_scores']]
    
    if param_names is None:
        param_names = list(all_params[0].keys())
    
    n_params = len(param_names)
    n_cols = min(3, n_params)
    n_rows = (n_params + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    axes = np.atleast_2d(axes)
    
    for idx, param_name in enumerate(param_names):
        row = idx // n_cols
        col = idx % n_cols
        ax = axes[row, col]
        
        # Extract parameter values
        param_values = [p[param_name] for p in all_params]
        
        # Scatter plot
        scatter = ax.scatter(param_values, all_scores, 
                           c=all_scores, cmap='viridis',
                           alpha=0.6, s=30)
        
        # Mark best
        best_idx = np.argmax(all_scores)
        ax.scatter(param_values[best_idx], all_scores[best_idx],
                  c='red', s=200, marker='*', 
                  edgecolor='black', linewidth=2,
                  label='Best')
        
        ax.set_xlabel(param_name, fontsize=10)
        ax.set_ylabel('Score', fontsize=10)
        ax.set_title(f'{param_name} vs Score', fontsize=11)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.colorbar(scatter, ax=ax)
    
    # Hide unused subplots
    for idx in range(n_params, n_rows * n_cols):
        row = idx // n_cols
        col = idx % n_cols
        axes[row, col].axis('off')
    
    plt.suptitle('Parameter Space Exploration', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    return fig


def visualize_sensitivity(
    sensitivity_results: Dict[str, any],
    figsize: Tuple[int, int] = (12, 8)
):
    """
    Visualize sensitivity analysis results.
    
    Parameters
    ----------
    sensitivity_results : dict
        Results from sensitivity_analysis
    figsize : tuple
        Figure size
    """
    import matplotlib.pyplot as plt
    
    sensitivities = sensitivity_results['sensitivities']
    ranking = sensitivity_results['ranking']
    baseline = sensitivity_results['baseline_score']
    
    n_params = len(ranking)
    
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    
    # 1. Sensitivity ranking
    ax = axes[0]
    total_sens = [sensitivities[p]['total_sensitivity'] for p in ranking]
    colors = plt.cm.viridis(np.linspace(0, 1, n_params))
    
    bars = ax.barh(range(n_params), total_sens, color=colors)
    ax.set_yticks(range(n_params))
    ax.set_yticklabels(ranking)
    ax.set_xlabel('Total Sensitivity', fontsize=12)
    ax.set_title('Parameter Sensitivity Ranking', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    
    # 2. Perturbation responses
    ax = axes[1]
    for param_name in ranking[:5]:  # Show top 5
        perturbations = sensitivities[param_name]['perturbations']
        factors = [p['factor'] for p in perturbations]
        scores = [p['score'] for p in perturbations]
        
        ax.plot(factors, scores, marker='o', label=param_name, linewidth=2)
    
    ax.axhline(baseline, color='k', linestyle='--', 
              label='Baseline', linewidth=2)
    ax.axvline(1.0, color='gray', linestyle=':', alpha=0.5)
    
    ax.set_xlabel('Perturbation Factor', fontsize=12)
    ax.set_ylabel('Score', fontsize=12)
    ax.set_title('Top 5 Parameter Responses', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.suptitle('Sensitivity Analysis Results', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    return fig
