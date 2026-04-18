"""
Parameter Space Exploration for Ouroboros Observer

Systematic exploration, sensitivity analysis, and optimization.
"""

import numpy as np
from typing import Dict, List, Tuple, Callable, Optional
from concurrent.futures import ProcessPoolExecutor
import itertools

try:
    from tqdm import tqdm
except ImportError:
    # Fallback if tqdm not available
    def tqdm(iterable, **kwargs):
        return iterable


class ParameterExplorer:
    """
    Explore parameter space systematically.
    
    Features:
    - Grid search
    - Random sampling
    - Sensitivity analysis
    - Bayesian optimization
    
    Parameters
    ----------
    objective_function : callable
        Function to evaluate (takes dict of parameters, returns scalar)
    seed : int, optional
        Random seed
    """
    
    def __init__(self, objective_function: Callable[[Dict], float],
                 seed: Optional[int] = None):
        self.objective_function = objective_function
        self.seed = seed
        self.results = []
        
        if seed is not None:
            np.random.seed(seed)
    
    def grid_search(self, param_ranges: Dict[str, np.ndarray],
                   parallel: bool = False,
                   n_workers: int = 4) -> List[Dict]:
        """
        Exhaustive grid search over parameter space.
        
        Parameters
        ----------
        param_ranges : dict
            Dictionary mapping parameter names to arrays of values
        parallel : bool
            Use parallel processing
        n_workers : int
            Number of parallel workers
        
        Returns
        -------
        list
            List of results, each dict with parameters and objective value
        """
        # Generate all combinations
        param_names = list(param_ranges.keys())
        param_values = list(param_ranges.values())
        combinations = list(itertools.product(*param_values))
        
        print(f"Grid search: {len(combinations)} combinations")
        
        if parallel:
            with ProcessPoolExecutor(max_workers=n_workers) as executor:
                results = list(tqdm(
                    executor.map(self._evaluate_point, 
                               [dict(zip(param_names, combo)) for combo in combinations]),
                    total=len(combinations)
                ))
        else:
            results = []
            for combo in tqdm(combinations):
                params = dict(zip(param_names, combo))
                results.append(self._evaluate_point(params))
        
        self.results = results
        return results
    
    def random_search(self, param_ranges: Dict[str, Tuple[float, float]],
                     n_samples: int = 100,
                     parallel: bool = False) -> List[Dict]:
        """
        Random sampling of parameter space.
        
        Parameters
        ----------
        param_ranges : dict
            Dictionary mapping parameter names to (min, max) tuples
        n_samples : int
            Number of random samples
        parallel : bool
            Use parallel processing
        
        Returns
        -------
        list
            List of results
        """
        # Generate random samples
        samples = []
        for _ in range(n_samples):
            sample = {}
            for param_name, (min_val, max_val) in param_ranges.items():
                sample[param_name] = np.random.uniform(min_val, max_val)
            samples.append(sample)
        
        if parallel:
            with ProcessPoolExecutor() as executor:
                results = list(tqdm(
                    executor.map(self._evaluate_point, samples),
                    total=n_samples
                ))
        else:
            results = [self._evaluate_point(s) for s in tqdm(samples)]
        
        self.results = results
        return results
    
    def sensitivity_analysis(self, baseline_params: Dict[str, float],
                           perturbation_fraction: float = 0.1,
                           n_samples_per_param: int = 10) -> Dict:
        """
        One-at-a-time sensitivity analysis.
        
        Parameters
        ----------
        baseline_params : dict
            Baseline parameter values
        perturbation_fraction : float
            Fraction to perturb each parameter
        n_samples_per_param : int
            Number of samples for each parameter
        
        Returns
        -------
        dict
            Sensitivity results for each parameter
        """
        baseline_value = self.objective_function(baseline_params)
        
        sensitivities = {}
        
        for param_name, baseline_val in baseline_params.items():
            # Perturb this parameter
            perturbations = np.linspace(
                baseline_val * (1 - perturbation_fraction),
                baseline_val * (1 + perturbation_fraction),
                n_samples_per_param
            )
            
            values = []
            for perturbed_val in perturbations:
                test_params = baseline_params.copy()
                test_params[param_name] = perturbed_val
                values.append(self.objective_function(test_params))
            
            # Calculate sensitivity metrics
            gradient = np.gradient(values, perturbations)
            
            sensitivities[param_name] = {
                'perturbations': perturbations,
                'values': np.array(values),
                'gradient': gradient,
                'mean_gradient': np.mean(np.abs(gradient)),
                'max_gradient': np.max(np.abs(gradient))
            }
        
        return sensitivities
    
    def optimize(self, initial_params: Dict[str, float],
                param_bounds: Dict[str, Tuple[float, float]],
                method: str = 'nelder-mead',
                maxiter: int = 100) -> Dict:
        """
        Optimize parameters to maximize objective.
        
        Parameters
        ----------
        initial_params : dict
            Starting point
        param_bounds : dict
            Bounds for each parameter
        method : str
            Optimization method
        maxiter : int
            Maximum iterations
        
        Returns
        -------
        dict
            Optimization results
        """
        from scipy.optimize import minimize
        
        param_names = list(initial_params.keys())
        x0 = [initial_params[name] for name in param_names]
        bounds = [param_bounds[name] for name in param_names]
        
        def objective(x):
            params = dict(zip(param_names, x))
            return -self.objective_function(params)  # Minimize negative
        
        result = minimize(objective, x0, method=method, 
                         bounds=bounds, options={'maxiter': maxiter})
        
        optimal_params = dict(zip(param_names, result.x))
        optimal_value = -result.fun
        
        return {
            'optimal_params': optimal_params,
            'optimal_value': optimal_value,
            'success': result.success,
            'n_iterations': result.nit
        }
    
    def _evaluate_point(self, params: Dict) -> Dict:
        """Evaluate objective at parameter point."""
        value = self.objective_function(params)
        result = params.copy()
        result['objective'] = value
        return result
    
    def get_best_result(self) -> Dict:
        """Get best result from search."""
        if not self.results:
            raise ValueError("No results available")
        
        return max(self.results, key=lambda x: x['objective'])
    
    def plot_1d_slice(self, param_name: str, 
                     fixed_params: Dict[str, float],
                     param_range: np.ndarray):
        """
        Plot 1D slice through parameter space.
        
        Parameters
        ----------
        param_name : str
            Parameter to vary
        fixed_params : dict
            Fixed values for other parameters
        param_range : np.ndarray
            Values to test
        """
        import matplotlib.pyplot as plt
        
        values = []
        for param_val in param_range:
            test_params = fixed_params.copy()
            test_params[param_name] = param_val
            values.append(self.objective_function(test_params))
        
        plt.figure(figsize=(8, 5))
        plt.plot(param_range, values, 'o-', linewidth=2)
        plt.xlabel(param_name)
        plt.ylabel('Objective Value')
        plt.title(f'1D Slice: {param_name}')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return plt.gcf()


def parallel_parameter_sweep(function: Callable,
                            param_grid: Dict[str, np.ndarray],
                            n_workers: int = 4) -> List[Dict]:
    """
    Parallel parameter sweep helper function.
    
    Parameters
    ----------
    function : callable
        Function to evaluate
    param_grid : dict
        Parameter ranges
    n_workers : int
        Number of parallel workers
    
    Returns
    -------
    list
        Results for all parameter combinations
    """
    param_names = list(param_grid.keys())
    param_values = list(param_grid.values())
    combinations = list(itertools.product(*param_values))
    
    def eval_combo(combo):
        params = dict(zip(param_names, combo))
        result = function(params)
        output = params.copy()
        output['result'] = result
        return output
    
    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        results = list(executor.map(eval_combo, combinations))
    
    return results
