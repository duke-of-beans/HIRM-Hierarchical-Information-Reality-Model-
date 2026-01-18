"""
HIRM Statistical Mechanics Toolkit
===================================

Production-ready implementation of statistical mechanics framework
for consciousness emergence through phase transitions.

Author: HIRM Research Project
Date: October 26, 2025
Version: 1.0
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from scipy.optimize import curve_fit
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# Core Ising Model Class
# ============================================================================

class IsingBrain:
    """
    Ising model for neural networks with consciousness measures.
    
    Implements:
    - Metropolis and Wolff Monte Carlo algorithms
    - Consciousness calculation (C = Φ × R × D)
    - Phase transition analysis
    - Critical exponent extraction
    """
    
    def __init__(
        self, 
        N: int, 
        connectivity_type: str = 'small_world',
        J_mean: float = 1.0,
        J_std: float = 0.2,
        seed: Optional[int] = None
    ):
        """
        Initialize Ising brain model.
        
        Parameters
        ----------
        N : int
            Number of neurons (spins)
        connectivity_type : str
            'lattice', 'random', 'small_world', 'scale_free'
        J_mean, J_std : float
            Coupling distribution parameters
        seed : int, optional
            Random seed for reproducibility
        """
        if seed is not None:
            np.random.seed(seed)
        
        self.N = N
        self.spins = np.random.choice([-1, 1], size=N)
        self.J = self._generate_connectivity(connectivity_type, J_mean, J_std)
        self.h = np.zeros(N)
        
        # History for self-reference calculation
        self.history = []
        self.max_history = 50
        
    def _generate_connectivity(
        self, 
        conn_type: str, 
        J_mean: float, 
        J_std: float
    ) -> np.ndarray:
        """Generate connectivity matrix J_ij."""
        
        if conn_type == 'lattice':
            return self._lattice_connectivity(J_mean)
        elif conn_type == 'random':
            return self._random_connectivity(J_mean, J_std)
        elif conn_type == 'small_world':
            return self._small_world_connectivity(J_mean, k=4, p=0.1)
        elif conn_type == 'scale_free':
            return self._scale_free_connectivity(J_mean, m=3)
        else:
            raise ValueError(f"Unknown connectivity type: {conn_type}")
    
    def _lattice_connectivity(self, J_mean: float) -> np.ndarray:
        """2D lattice nearest-neighbor connectivity."""
        side = int(np.sqrt(self.N))
        J = np.zeros((self.N, self.N))
        
        for i in range(side):
            for j in range(side):
                idx = i * side + j
                # Right neighbor
                if j < side - 1:
                    J[idx, idx + 1] = J_mean
                    J[idx + 1, idx] = J_mean
                # Down neighbor
                if i < side - 1:
                    J[idx, idx + side] = J_mean
                    J[idx + side, idx] = J_mean
        
        return J
    
    def _random_connectivity(self, J_mean: float, J_std: float) -> np.ndarray:
        """Random Gaussian connectivity."""
        J = np.random.normal(J_mean, J_std, (self.N, self.N))
        J = (J + J.T) / 2  # Symmetrize
        np.fill_diagonal(J, 0)
        return J
    
    def _small_world_connectivity(
        self, 
        J_mean: float, 
        k: int, 
        p: float
    ) -> np.ndarray:
        """Watts-Strogatz small-world network."""
        J = np.zeros((self.N, self.N))
        
        # Ring lattice
        for i in range(self.N):
            for j in range(1, k // 2 + 1):
                J[i, (i + j) % self.N] = J_mean
                J[(i + j) % self.N, i] = J_mean
        
        # Rewire with probability p
        for i in range(self.N):
            neighbors = np.where(J[i, :] > 0)[0]
            for j in neighbors:
                if j > i and np.random.rand() < p:
                    J[i, j] = 0
                    J[j, i] = 0
                    k_new = np.random.randint(self.N)
                    while k_new == i or J[i, k_new] > 0:
                        k_new = np.random.randint(self.N)
                    J[i, k_new] = J_mean
                    J[k_new, i] = J_mean
        
        return J
    
    def _scale_free_connectivity(self, J_mean: float, m: int) -> np.ndarray:
        """Barabási-Albert scale-free network."""
        J = np.zeros((self.N, self.N))
        degrees = np.zeros(self.N)
        
        # Start with small complete graph
        for i in range(m):
            for j in range(i + 1, m):
                J[i, j] = J_mean
                J[j, i] = J_mean
                degrees[i] += 1
                degrees[j] += 1
        
        # Add nodes with preferential attachment
        for i in range(m, self.N):
            # Select m nodes to connect to (preferential attachment)
            probs = degrees[:i] / np.sum(degrees[:i])
            targets = np.random.choice(i, size=min(m, i), replace=False, p=probs)
            
            for j in targets:
                J[i, j] = J_mean
                J[j, i] = J_mean
                degrees[i] += 1
                degrees[j] += 1
        
        return J
    
    def energy(self) -> float:
        """Total energy of current configuration."""
        interaction = -0.5 * np.sum(self.J * np.outer(self.spins, self.spins))
        field = -np.dot(self.h, self.spins)
        return interaction + field
    
    def magnetization(self) -> float:
        """Order parameter (mean spin)."""
        return np.mean(self.spins)
    
    def compute_phi(self) -> float:
        """
        Integrated information (simplified).
        
        Uses bipartition mutual information as proxy for Φ.
        """
        mid = self.N // 2
        
        # Partition into two halves
        s1 = self.spins[:mid]
        s2 = self.spins[mid:]
        
        # Compute marginal entropies
        p1 = (np.mean(s1) + 1) / 2  # Map [-1,1] to [0,1]
        p2 = (np.mean(s2) + 1) / 2
        p_total = (np.mean(self.spins) + 1) / 2
        
        H1 = self._binary_entropy(p1)
        H2 = self._binary_entropy(p2)
        H_total = self._binary_entropy(p_total)
        
        # Mutual information (upper bound on Φ)
        phi = H1 + H2 - H_total
        return max(0, phi)
    
    def compute_self_reference(self) -> float:
        """
        Self-reference completeness R(t).
        
        Measures how well past states predict current state.
        """
        if len(self.history) < 5:
            return 0.0
        
        # Average correlation with recent history
        recent = np.array(self.history[-10:])
        correlations = [np.corrcoef(past, self.spins)[0, 1] 
                       for past in recent if len(past) == len(self.spins)]
        
        R = np.mean([max(0, c) for c in correlations if not np.isnan(c)])
        return R
    
    def compute_dimensionality(self) -> float:
        """
        Effective dimensionality D.
        
        Uses participation ratio: D = (Σa_i)² / Σa_i²
        where a_i is activity level.
        """
        activity = (self.spins + 1) / 2  # Map to [0, 1]
        
        sum_a = np.sum(activity)
        sum_a2 = np.sum(activity ** 2)
        
        if sum_a2 < 1e-10:
            return 1.0
        
        D = sum_a ** 2 / sum_a2
        return D
    
    def consciousness(self) -> float:
        """
        Consciousness measure C(t) = Φ(t) × R(t) × D(t)
        """
        phi = self.compute_phi()
        R = self.compute_self_reference()
        D = self.compute_dimensionality()
        
        return phi * R * D
    
    @staticmethod
    def _binary_entropy(p: float) -> float:
        """Shannon entropy for binary variable."""
        if p <= 0 or p >= 1:
            return 0.0
        return -(p * np.log2(p) + (1 - p) * np.log2(1 - p))
    
    def metropolis_step(self, beta: float):
        """Single Metropolis Monte Carlo step."""
        i = np.random.randint(self.N)
        
        # Local field
        h_local = np.dot(self.J[i, :], self.spins) + self.h[i]
        
        # Energy change if we flip
        delta_E = 2 * self.spins[i] * h_local
        
        # Accept/reject
        if delta_E <= 0 or np.random.rand() < np.exp(-beta * delta_E):
            self.spins[i] *= -1
    
    def wolff_step(self, beta: float) -> int:
        """
        Single Wolff cluster update.
        
        Returns cluster size.
        """
        i_seed = np.random.randint(self.N)
        cluster = {i_seed}
        frontier = {i_seed}
        
        while frontier:
            i = frontier.pop()
            
            # Find neighbors
            neighbors = np.where(self.J[i, :] != 0)[0]
            
            for j in neighbors:
                if j not in cluster and self.spins[i] == self.spins[j]:
                    # Add with probability 1 - exp(-2β|J_ij|)
                    p_add = 1 - np.exp(-2 * beta * abs(self.J[i, j]))
                    if np.random.rand() < p_add:
                        cluster.add(j)
                        frontier.add(j)
        
        # Flip entire cluster
        for i in cluster:
            self.spins[i] *= -1
        
        return len(cluster)
    
    def simulate(
        self, 
        beta: float, 
        n_steps: int,
        algorithm: str = 'metropolis',
        sample_interval: int = 10,
        equilibration: int = 1000
    ) -> Dict[str, np.ndarray]:
        """
        Run Monte Carlo simulation.
        
        Parameters
        ----------
        beta : float
            Inverse temperature (1 / k_B T)
        n_steps : int
            Number of Monte Carlo steps
        algorithm : str
            'metropolis' or 'wolff'
        sample_interval : int
            Sampling frequency
        equilibration : int
            Equilibration steps before measurement
        
        Returns
        -------
        trajectory : dict
            Time series of observables
        """
        # Equilibration
        for _ in range(equilibration):
            if algorithm == 'metropolis':
                self.metropolis_step(beta)
            elif algorithm == 'wolff':
                self.wolff_step(beta)
            else:
                raise ValueError(f"Unknown algorithm: {algorithm}")
        
        # Measurement
        trajectory = {
            'step': [],
            'magnetization': [],
            'energy': [],
            'phi': [],
            'R': [],
            'D': [],
            'consciousness': []
        }
        
        for step in range(n_steps):
            if algorithm == 'metropolis':
                self.metropolis_step(beta)
            elif algorithm == 'wolff':
                self.wolff_step(beta)
            
            # Sample
            if step % sample_interval == 0:
                # Update history for R calculation
                self.history.append(self.spins.copy())
                if len(self.history) > self.max_history:
                    self.history.pop(0)
                
                # Measure observables
                trajectory['step'].append(step)
                trajectory['magnetization'].append(self.magnetization())
                trajectory['energy'].append(self.energy())
                
                phi = self.compute_phi()
                R = self.compute_self_reference()
                D = self.compute_dimensionality()
                C = phi * R * D
                
                trajectory['phi'].append(phi)
                trajectory['R'].append(R)
                trajectory['D'].append(D)
                trajectory['consciousness'].append(C)
        
        return {k: np.array(v) for k, v in trajectory.items()}

# ============================================================================
# Phase Transition Analysis
# ============================================================================

class PhaseTransitionAnalyzer:
    """
    Tools for analyzing phase transitions and extracting critical exponents.
    """
    
    @staticmethod
    def scan_temperature(
        N: int,
        T_range: np.ndarray,
        connectivity_type: str = 'small_world',
        n_steps: int = 5000,
        algorithm: str = 'wolff',
        seed: Optional[int] = None
    ) -> Dict[str, np.ndarray]:
        """
        Scan across temperatures to map phase transition.
        
        Returns
        -------
        results : dict
            'T', 'magnetization', 'susceptibility', 'consciousness', etc.
        """
        results = {
            'T': [],
            'beta': [],
            'magnetization': [],
            'magnetization_std': [],
            'susceptibility': [],
            'consciousness': [],
            'consciousness_std': [],
            'energy': [],
            'specific_heat': []
        }
        
        print(f"Scanning {len(T_range)} temperatures with N={N} spins...")
        
        for i, T in enumerate(T_range):
            beta = 1.0 / T
            
            # Create model
            model = IsingBrain(N, connectivity_type=connectivity_type, seed=seed)
            
            # Simulate
            traj = model.simulate(
                beta=beta,
                n_steps=n_steps,
                algorithm=algorithm,
                sample_interval=10,
                equilibration=1000
            )
            
            # Extract observables
            m = np.abs(traj['magnetization'])
            E = traj['energy']
            C = traj['consciousness']
            
            results['T'].append(T)
            results['beta'].append(beta)
            results['magnetization'].append(np.mean(m))
            results['magnetization_std'].append(np.std(m))
            results['susceptibility'].append(beta * N * np.var(traj['magnetization']))
            results['consciousness'].append(np.mean(C))
            results['consciousness_std'].append(np.std(C))
            results['energy'].append(np.mean(E))
            results['specific_heat'].append(beta**2 * np.var(E))
            
            if (i + 1) % 5 == 0:
                print(f"  Progress: {i+1}/{len(T_range)} "
                      f"(T={T:.2f}, m={results['magnetization'][-1]:.3f})")
        
        return {k: np.array(v) for k, v in results.items()}
    
    @staticmethod
    def estimate_T_critical(results: Dict[str, np.ndarray]) -> float:
        """
        Estimate critical temperature from susceptibility peak.
        """
        chi = results['susceptibility']
        T = results['T']
        
        # Find peak
        i_max = np.argmax(chi)
        T_c = T[i_max]
        
        return T_c
    
    @staticmethod
    def extract_critical_exponents(
        results: Dict[str, np.ndarray],
        T_c: float,
        fit_range: float = 0.3
    ) -> Dict[str, Tuple[float, float]]:
        """
        Extract critical exponents via power-law fits.
        
        Fits:
        - β: m ~ (T_c - T)^β  (T < T_c)
        - γ: χ ~ |T - T_c|^(-γ)
        - α: C_V ~ |T - T_c|^(-α)
        
        Returns
        -------
        exponents : dict
            {'beta': (value, error), 'gamma': (value, error), ...}
        """
        T = results['T']
        m = results['magnetization']
        chi = results['susceptibility']
        C_V = results['specific_heat']
        
        exponents = {}
        
        # Exponent β (magnetization)
        mask_low = (T < T_c) & (T > T_c - fit_range)
        if np.sum(mask_low) > 3:
            x = np.log(T_c - T[mask_low])
            y = np.log(m[mask_low] + 1e-10)
            slope, intercept, r_value, p_value, std_err = linregress(x, y)
            exponents['beta'] = (slope, std_err)
        
        # Exponent γ (susceptibility)
        mask = (np.abs(T - T_c) < fit_range) & (np.abs(T - T_c) > 0.05)
        if np.sum(mask) > 3:
            x = np.log(np.abs(T[mask] - T_c))
            y = np.log(chi[mask])
            slope, intercept, r_value, p_value, std_err = linregress(x, y)
            exponents['gamma'] = (-slope, std_err)
        
        # Exponent α (specific heat)
        if np.sum(mask) > 3:
            x = np.log(np.abs(T[mask] - T_c))
            y = np.log(C_V[mask])
            slope, intercept, r_value, p_value, std_err = linregress(x, y)
            exponents['alpha'] = (-slope, std_err)
        
        return exponents

# ============================================================================
# Visualization Tools
# ============================================================================

class Visualizer:
    """Plotting utilities for phase transition analysis."""
    
    @staticmethod
    def plot_phase_transition(
        results: Dict[str, np.ndarray],
        T_c: Optional[float] = None,
        save_path: Optional[str] = None
    ):
        """
        Create comprehensive phase transition visualization.
        """
        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        fig.suptitle('HIRM Statistical Mechanics: Phase Transition Analysis', 
                     fontsize=16, fontweight='bold')
        
        T = results['T']
        
        # Magnetization
        axes[0, 0].plot(T, results['magnetization'], 'o-', color='steelblue', linewidth=2)
        axes[0, 0].set_xlabel('Temperature T', fontsize=12)
        axes[0, 0].set_ylabel('|Magnetization| m', fontsize=12)
        axes[0, 0].set_title('Order Parameter')
        axes[0, 0].grid(True, alpha=0.3)
        if T_c:
            axes[0, 0].axvline(T_c, color='red', linestyle='--', linewidth=2, 
                              label=f'T_c = {T_c:.2f}')
            axes[0, 0].legend()
        
        # Susceptibility
        axes[0, 1].plot(T, results['susceptibility'], 's-', color='coral', linewidth=2)
        axes[0, 1].set_xlabel('Temperature T', fontsize=12)
        axes[0, 1].set_ylabel('Susceptibility χ', fontsize=12)
        axes[0, 1].set_title('Response Function')
        axes[0, 1].grid(True, alpha=0.3)
        if T_c:
            axes[0, 1].axvline(T_c, color='red', linestyle='--', linewidth=2)
        
        # Consciousness
        axes[0, 2].plot(T, results['consciousness'], '^-', color='purple', linewidth=2)
        axes[0, 2].fill_between(
            T, 
            results['consciousness'] - results['consciousness_std'],
            results['consciousness'] + results['consciousness_std'],
            alpha=0.3, color='purple'
        )
        axes[0, 2].set_xlabel('Temperature T', fontsize=12)
        axes[0, 2].set_ylabel('Consciousness C(t)', fontsize=12)
        axes[0, 2].set_title('HIRM Consciousness Measure')
        axes[0, 2].grid(True, alpha=0.3)
        if T_c:
            axes[0, 2].axvline(T_c, color='red', linestyle='--', linewidth=2,
                              label='C_critical')
            axes[0, 2].legend()
        
        # Energy
        axes[1, 0].plot(T, results['energy'], 'o-', color='green', linewidth=2)
        axes[1, 0].set_xlabel('Temperature T', fontsize=12)
        axes[1, 0].set_ylabel('Energy ⟨E⟩', fontsize=12)
        axes[1, 0].set_title('Mean Energy')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Specific Heat
        axes[1, 1].plot(T, results['specific_heat'], 's-', color='orange', linewidth=2)
        axes[1, 1].set_xlabel('Temperature T', fontsize=12)
        axes[1, 1].set_ylabel('Specific Heat C_V', fontsize=12)
        axes[1, 1].set_title('Heat Capacity')
        axes[1, 1].grid(True, alpha=0.3)
        if T_c:
            axes[1, 1].axvline(T_c, color='red', linestyle='--', linewidth=2)
        
        # Phase diagram (conceptual)
        axes[1, 2].text(0.5, 0.7, 'Unconscious\n(Disordered)', 
                       ha='center', va='center', fontsize=14, color='blue',
                       bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
        axes[1, 2].text(0.5, 0.3, 'Conscious\n(Ordered)', 
                       ha='center', va='center', fontsize=14, color='red',
                       bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.5))
        if T_c:
            axes[1, 2].axhline(0.5, color='red', linewidth=3, linestyle='--')
            axes[1, 2].text(0.5, 0.52, f'C_critical ≈ {T_c:.2f} bits', 
                           ha='center', fontsize=12, fontweight='bold')
        axes[1, 2].set_xlim(0, 1)
        axes[1, 2].set_ylim(0, 1)
        axes[1, 2].axis('off')
        axes[1, 2].set_title('Phase Diagram (Schematic)')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Figure saved to: {save_path}")
        
        plt.show()
    
    @staticmethod
    def plot_critical_scaling(
        results: Dict[str, np.ndarray],
        T_c: float,
        exponents: Dict[str, Tuple[float, float]],
        save_path: Optional[str] = None
    ):
        """
        Plot critical scaling with fitted power laws.
        """
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        fig.suptitle('Critical Scaling Near Phase Transition', 
                     fontsize=16, fontweight='bold')
        
        T = results['T']
        m = results['magnetization']
        chi = results['susceptibility']
        
        # Magnetization scaling (T < T_c)
        mask = (T < T_c) & (T > T_c - 0.5)
        if np.sum(mask) > 0 and 'beta' in exponents:
            beta_exp, beta_err = exponents['beta']
            
            axes[0].loglog(T_c - T[mask], m[mask], 'o', label='Data')
            
            # Fit line
            t_fit = np.logspace(np.log10(np.min(T_c - T[mask])),
                                np.log10(np.max(T_c - T[mask])), 100)
            m_fit = t_fit ** beta_exp
            axes[0].loglog(t_fit, m_fit * m[mask][0] / m_fit[0], '--', 
                          label=f'β = {beta_exp:.3f} ± {beta_err:.3f}')
            
            axes[0].set_xlabel('T_c - T', fontsize=12)
            axes[0].set_ylabel('Magnetization m', fontsize=12)
            axes[0].set_title('Order Parameter Scaling')
            axes[0].legend()
            axes[0].grid(True, alpha=0.3, which='both')
        
        # Susceptibility scaling
        mask = (np.abs(T - T_c) < 0.5) & (np.abs(T - T_c) > 0.05)
        if np.sum(mask) > 0 and 'gamma' in exponents:
            gamma_exp, gamma_err = exponents['gamma']
            
            axes[1].loglog(np.abs(T[mask] - T_c), chi[mask], 's', label='Data')
            
            # Fit line
            t_fit = np.logspace(np.log10(np.min(np.abs(T[mask] - T_c))),
                                np.log10(np.max(np.abs(T[mask] - T_c))), 100)
            chi_fit = t_fit ** (-gamma_exp)
            axes[1].loglog(t_fit, chi_fit * chi[mask][0] / chi_fit[0], '--',
                          label=f'γ = {gamma_exp:.3f} ± {gamma_err:.3f}')
            
            axes[1].set_xlabel('|T - T_c|', fontsize=12)
            axes[1].set_ylabel('Susceptibility χ', fontsize=12)
            axes[1].set_title('Susceptibility Divergence')
            axes[1].legend()
            axes[1].grid(True, alpha=0.3, which='both')
        
        # Universality class comparison
        universality_data = {
            'Mean-Field': {'beta': 0.5, 'gamma': 1.0, 'nu': 0.5},
            '2D Ising': {'beta': 0.125, 'gamma': 1.75, 'nu': 1.0},
            '3D Ising': {'beta': 0.326, 'gamma': 1.237, 'nu': 0.630},
            'Percolation (3D)': {'beta': 0.41, 'gamma': 1.80, 'nu': 0.875}
        }
        
        labels = list(universality_data.keys())
        beta_theory = [universality_data[k]['beta'] for k in labels]
        gamma_theory = [universality_data[k]['gamma'] for k in labels]
        
        x = np.arange(len(labels))
        width = 0.35
        
        axes[2].bar(x - width/2, beta_theory, width, label='Theoretical β', alpha=0.7)
        axes[2].bar(x + width/2, gamma_theory, width, label='Theoretical γ', alpha=0.7)
        
        if 'beta' in exponents and 'gamma' in exponents:
            beta_measured, _ = exponents['beta']
            gamma_measured, _ = exponents['gamma']
            axes[2].axhline(beta_measured, color='C0', linestyle='--', 
                           label=f'Measured β = {beta_measured:.3f}')
            axes[2].axhline(gamma_measured, color='C1', linestyle='--',
                           label=f'Measured γ = {gamma_measured:.3f}')
        
        axes[2].set_xticks(x)
        axes[2].set_xticklabels(labels, rotation=15, ha='right')
        axes[2].set_ylabel('Critical Exponent Value', fontsize=12)
        axes[2].set_title('Universality Class Identification')
        axes[2].legend(fontsize=9)
        axes[2].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Figure saved to: {save_path}")
        
        plt.show()

# ============================================================================
# Main Execution & Examples
# ============================================================================

def run_complete_analysis(
    N: int = 30,
    connectivity_type: str = 'small_world',
    T_min: float = 0.5,
    T_max: float = 4.0,
    n_temps: int = 25,
    save_outputs: bool = True,
    output_dir: str = '/mnt/user-data/outputs'
):
    """
    Run complete phase transition analysis pipeline.
    
    Parameters
    ----------
    N : int
        System size (number of spins)
    connectivity_type : str
        Network topology
    T_min, T_max : float
        Temperature range
    n_temps : int
        Number of temperature points
    save_outputs : bool
        Whether to save figures
    output_dir : str
        Output directory
    """
    print("=" * 70)
    print("HIRM STATISTICAL MECHANICS: PHASE TRANSITION ANALYSIS")
    print("=" * 70)
    print(f"\nConfiguration:")
    print(f"  System size: N = {N}")
    print(f"  Connectivity: {connectivity_type}")
    print(f"  Temperature range: [{T_min}, {T_max}]")
    print(f"  Number of points: {n_temps}")
    print("\n" + "=" * 70 + "\n")
    
    # Temperature scan
    T_range = np.linspace(T_min, T_max, n_temps)
    results = PhaseTransitionAnalyzer.scan_temperature(
        N=N,
        T_range=T_range,
        connectivity_type=connectivity_type,
        n_steps=5000,
        algorithm='wolff',
        seed=42
    )
    
    # Estimate critical point
    T_c = PhaseTransitionAnalyzer.estimate_T_critical(results)
    print(f"\nEstimated critical temperature: T_c = {T_c:.3f}")
    
    # Extract exponents
    print("\nExtracting critical exponents...")
    exponents = PhaseTransitionAnalyzer.extract_critical_exponents(
        results, T_c, fit_range=0.4
    )
    
    print("\nCritical Exponents:")
    for name, (value, error) in exponents.items():
        print(f"  {name}: {value:.3f} ± {error:.3f}")
    
    # Compare with universality classes
    print("\nUniversality Class Comparison:")
    print("  Mean-field:  β=0.500, γ=1.000, ν=0.500")
    print("  2D Ising:    β=0.125, γ=1.750, ν=1.000")
    print("  3D Ising:    β=0.326, γ=1.237, ν=0.630")
    print("  Percolation: β=0.410, γ=1.800, ν=0.875")
    
    if 'beta' in exponents and 'gamma' in exponents:
        beta_val, _ = exponents['beta']
        gamma_val, _ = exponents['gamma']
        
        # Check which universality class is closest
        classes = {
            'Mean-field': (0.5, 1.0),
            '2D Ising': (0.125, 1.75),
            '3D Ising': (0.326, 1.237),
            'Percolation': (0.41, 1.80)
        }
        
        distances = {
            name: np.sqrt((beta_val - b)**2 + (gamma_val - g)**2)
            for name, (b, g) in classes.items()
        }
        
        best_match = min(distances, key=distances.get)
        print(f"\n  → Best match: {best_match}")
    
    # Visualize
    print("\nGenerating visualizations...")
    
    if save_outputs:
        Visualizer.plot_phase_transition(
            results, T_c,
            save_path=f"{output_dir}/hirm_phase_transition.png"
        )
        
        Visualizer.plot_critical_scaling(
            results, T_c, exponents,
            save_path=f"{output_dir}/hirm_critical_scaling.png"
        )
    else:
        Visualizer.plot_phase_transition(results, T_c)
        Visualizer.plot_critical_scaling(results, T_c, exponents)
    
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE!")
    print("=" * 70)
    
    return results, T_c, exponents

# ============================================================================
# Quick Demo
# ============================================================================

if __name__ == '__main__':
    import sys
    
    # Run analysis
    results, T_c, exponents = run_complete_analysis(
        N=30,
        connectivity_type='small_world',
        T_min=0.5,
        T_max=4.0,
        n_temps=25,
        save_outputs=True
    )
    
    print("\n" + "="*70)
    print("Output files saved to: /mnt/user-data/outputs/")
    print("  - hirm_phase_transition.png")
    print("  - hirm_critical_scaling.png")
    print("="*70)
