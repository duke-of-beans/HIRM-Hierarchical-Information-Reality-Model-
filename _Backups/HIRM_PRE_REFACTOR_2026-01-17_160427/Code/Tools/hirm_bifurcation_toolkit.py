"""
HIRM Bifurcation Theory: Computational Toolkit
Complete implementation of dynamical systems analysis for consciousness transitions

Date: October 26, 2025
Framework: Hierarchical Information-Reality Model (HIRM)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint, solve_ivp
from scipy.optimize import fsolve, minimize
from scipy import signal
from scipy.stats import kurtosis
from dataclasses import dataclass
from typing import Callable, List, Tuple, Dict
import warnings
warnings.filterwarnings('ignore')

# =======================
# 1. NORMAL FORM DYNAMICS
# =======================

class BifurcationDynamics:
    """Collection of normal form bifurcations for consciousness transitions"""
    
    @staticmethod
    def saddle_node(C, t, mu):
        """
        Saddle-node bifurcation: dC/dt = μ + C²
        Application: Anesthesia-induced loss of consciousness
        """
        return mu + C**2
    
    @staticmethod
    def transcritical(C, t, mu):
        """
        Transcritical bifurcation: dC/dt = μC - C²
        Application: Sleep-wake transitions
        """
        return mu * C - C**2
    
    @staticmethod
    def pitchfork(C, t, mu):
        """
        Pitchfork bifurcation: dC/dt = μC - C³
        Application: Symmetry breaking (SRID)
        """
        return mu * C - C**3
    
    @staticmethod
    def hopf(state, t, mu, omega=10.0):
        """
        Hopf bifurcation: Emergence of oscillations
        Application: Alpha rhythm emergence
        
        state = [x, y]
        dx/dt = μx - ωy - x(x² + y²)
        dy/dt = μy + ωx - y(x² + y²)
        """
        x, y = state
        r_squared = x**2 + y**2
        dx = mu*x - omega*y - x*r_squared
        dy = mu*y + omega*x - y*r_squared
        return [dx, dy]
    
    @staticmethod
    def bogdanov_takens(state, t, mu1, mu2):
        """
        Bogdanov-Takens bifurcation (codimension-2)
        Application: C_critical as organizing center
        
        state = [x, y]
        dx/dt = y
        dy/dt = μ₁ + μ₂x + x² - xy
        """
        x, y = state
        dx = y
        dy = mu1 + mu2*x + x**2 - x*y
        return [dx, dy]


class BifurcationAnalyzer:
    """Tools for analyzing bifurcations in dynamical systems"""
    
    def __init__(self, dynamics: Callable, dim: int):
        """
        Parameters:
        - dynamics: Function(state, t, *params) returning derivatives
        - dim: System dimension
        """
        self.dynamics = dynamics
        self.dim = dim
        
    def find_fixed_points(self, param_range: np.ndarray, 
                         initial_guess: np.ndarray) -> np.ndarray:
        """
        Find fixed points across parameter range
        
        Returns: (n_params, dim) array of fixed points
        """
        fixed_points = []
        
        for param in param_range:
            def equations(state):
                return self.dynamics(state, 0, param)
            
            try:
                fp = fsolve(equations, initial_guess, full_output=True)
                if fp[2] == 1:  # Successful convergence
                    fixed_points.append(fp[0])
                else:
                    fixed_points.append(np.full(self.dim, np.nan))
            except:
                fixed_points.append(np.full(self.dim, np.nan))
        
        return np.array(fixed_points)
    
    def compute_jacobian(self, state: np.ndarray, param: float, 
                        epsilon: float = 1e-6) -> np.ndarray:
        """
        Numerical Jacobian matrix at given state and parameter
        """
        J = np.zeros((self.dim, self.dim))
        f0 = np.array(self.dynamics(state, 0, param))
        
        for i in range(self.dim):
            state_perturbed = np.array(state, dtype=float)
            state_perturbed[i] += epsilon
            f_perturbed = np.array(self.dynamics(state_perturbed, 0, param))
            J[:, i] = (f_perturbed - f0) / epsilon
        
        return J
    
    def stability_analysis(self, fixed_point: np.ndarray, 
                          param: float) -> Dict:
        """
        Analyze stability of fixed point
        
        Returns: {
            'eigenvalues': complex array,
            'stable': bool,
            'type': str ('stable node', 'saddle', 'focus', etc.)
        }
        """
        J = self.compute_jacobian(fixed_point, param)
        eigenvalues = np.linalg.eigvals(J)
        
        stable = all(eigenvalues.real < 0)
        
        # Classify fixed point
        if stable:
            if all(eigenvalues.imag == 0):
                fp_type = 'stable node'
            else:
                fp_type = 'stable focus'
        else:
            if any(eigenvalues.real > 0) and any(eigenvalues.real < 0):
                fp_type = 'saddle'
            elif all(eigenvalues.imag == 0):
                fp_type = 'unstable node'
            else:
                fp_type = 'unstable focus'
        
        return {
            'eigenvalues': eigenvalues,
            'stable': stable,
            'type': fp_type
        }
    
    def create_bifurcation_diagram(self, param_range: np.ndarray,
                                   initial_guesses: List[np.ndarray],
                                   figsize: Tuple = (10, 6)):
        """
        Generate bifurcation diagram
        """
        plt.figure(figsize=figsize)
        
        colors = ['blue', 'red', 'green', 'orange']
        
        for idx, guess in enumerate(initial_guesses):
            fixed_points = self.find_fixed_points(param_range, guess)
            
            # Classify stability for each point
            stabilities = []
            for i, (fp, param) in enumerate(zip(fixed_points, param_range)):
                if not np.any(np.isnan(fp)):
                    stability = self.stability_analysis(fp, param)
                    stabilities.append(stability['stable'])
                else:
                    stabilities.append(False)
            
            stabilities = np.array(stabilities)
            
            # Plot stable and unstable separately
            if self.dim == 1:
                stable_fp = fixed_points[stabilities]
                unstable_fp = fixed_points[~stabilities]
                stable_params = param_range[stabilities]
                unstable_params = param_range[~stabilities]
                
                if len(stable_fp) > 0:
                    plt.plot(stable_params, stable_fp, 'o', 
                            color=colors[idx % len(colors)], 
                            markersize=3, label=f'Branch {idx+1} (stable)')
                if len(unstable_fp) > 0:
                    plt.plot(unstable_params, unstable_fp, 'o', 
                            color=colors[idx % len(colors)], 
                            markersize=3, alpha=0.3, 
                            label=f'Branch {idx+1} (unstable)')
            else:
                # For higher dimensions, plot first component
                stable_fp = fixed_points[stabilities, 0]
                unstable_fp = fixed_points[~stabilities, 0]
                stable_params = param_range[stabilities]
                unstable_params = param_range[~stabilities]
                
                if len(stable_fp) > 0:
                    plt.plot(stable_params, stable_fp, '-', 
                            color=colors[idx % len(colors)], linewidth=2)
                if len(unstable_fp) > 0:
                    plt.plot(unstable_params, unstable_fp, '--', 
                            color=colors[idx % len(colors)], linewidth=2, alpha=0.5)
        
        plt.xlabel('Control Parameter μ', fontsize=12)
        plt.ylabel('Fixed Point Value', fontsize=12)
        plt.title('Bifurcation Diagram', fontsize=14, fontweight='bold')
        plt.grid(alpha=0.3)
        plt.legend()
        
        return plt.gcf()


# ===========================
# 2. CATASTROPHE THEORY
# ===========================

class CuspCatastrophe:
    """
    Cusp catastrophe model for hysteresis in consciousness transitions
    V(C, a, b) = C⁴/4 + aC²/2 + bC
    """
    
    def __init__(self):
        self.name = "Cusp Catastrophe"
        
    def potential(self, C: np.ndarray, a: float, b: float) -> np.ndarray:
        """Potential function V(C, a, b)"""
        return C**4 / 4 + a * C**2 / 2 + b * C
    
    def equilibria(self, a: float, b: float) -> np.ndarray:
        """
        Find equilibria by solving ∂V/∂C = 0
        C³ + aC + b = 0
        """
        coeffs = [1, 0, a, b]  # C³ + 0·C² + aC + b
        roots = np.roots(coeffs)
        return roots[np.isreal(roots)].real
    
    def discriminant(self, a: float, b: float) -> float:
        """
        Cusp boundary: Δ = 4a³ + 27b² = 0
        """
        return 4 * a**3 + 27 * b**2
    
    def plot_behavior_surface(self, a_range: Tuple = (-2, 2), 
                             b_range: Tuple = (-2, 2), 
                             resolution: int = 50):
        """
        Create 3D behavior surface plot
        """
        from mpl_toolkits.mplot3d import Axes3D
        
        a_vals = np.linspace(a_range[0], a_range[1], resolution)
        b_vals = np.linspace(b_range[0], b_range[1], resolution)
        A, B = np.meshgrid(a_vals, b_vals)
        
        C_surface = np.zeros_like(A)
        
        for i in range(resolution):
            for j in range(resolution):
                equilibria = self.equilibria(A[i, j], B[i, j])
                if len(equilibria) == 3:
                    # Take middle (unstable) for visualization
                    C_surface[i, j] = np.sort(equilibria)[1]
                elif len(equilibria) == 1:
                    C_surface[i, j] = equilibria[0]
                else:
                    C_surface[i, j] = np.nan
        
        fig = plt.figure(figsize=(14, 6))
        
        # 3D surface
        ax1 = fig.add_subplot(121, projection='3d')
        ax1.plot_surface(A, B, C_surface, cmap='viridis', alpha=0.8)
        ax1.set_xlabel('Arousal (a)', fontsize=11)
        ax1.set_ylabel('Anesthetic Depth (b)', fontsize=11)
        ax1.set_zlabel('Consciousness Level C', fontsize=11)
        ax1.set_title('Cusp Catastrophe: Behavior Surface', fontsize=12, fontweight='bold')
        
        # Control space with cusp boundary
        ax2 = fig.add_subplot(122)
        a_cusp = np.linspace(-1.5, 0, 100)
        b_cusp_upper = np.sqrt(-4 * a_cusp**3 / 27)
        b_cusp_lower = -np.sqrt(-4 * a_cusp**3 / 27)
        
        ax2.fill_between(a_cusp, b_cusp_lower, b_cusp_upper, 
                        alpha=0.3, color='red', label='Bistable region')
        ax2.plot(a_cusp, b_cusp_upper, 'r-', linewidth=2)
        ax2.plot(a_cusp, b_cusp_lower, 'r-', linewidth=2)
        ax2.set_xlabel('Arousal (a)', fontsize=11)
        ax2.set_ylabel('Anesthetic Depth (b)', fontsize=11)
        ax2.set_title('Control Space: Cusp Boundary', fontsize=12, fontweight='bold')
        ax2.legend()
        ax2.grid(alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def simulate_hysteresis_loop(self, arousal_baseline: float = -1.0):
        """
        Simulate forward (induction) and reverse (emergence) paths
        """
        # Forward path: increasing anesthetic depth
        b_forward = np.linspace(-1.0, 1.0, 100)
        a_forward = arousal_baseline * np.ones_like(b_forward)
        
        C_forward = []
        current_C = -2.0  # Start awake (stable negative root)
        
        for a, b in zip(a_forward, b_forward):
            equilibria = self.equilibria(a, b)
            equilibria_sorted = np.sort(equilibria)
            
            # Follow closest equilibrium
            if len(equilibria) == 3:
                # Choose equilibrium closest to current state
                distances = np.abs(equilibria - current_C)
                current_C = equilibria[np.argmin(distances)]
            elif len(equilibria) == 1:
                current_C = equilibria[0]
            
            C_forward.append(current_C)
        
        # Reverse path: decreasing anesthetic depth
        b_reverse = np.linspace(1.0, -1.0, 100)
        a_reverse = arousal_baseline * np.ones_like(b_reverse)
        
        C_reverse = []
        current_C = 2.0  # Start unconscious (stable positive root)
        
        for a, b in zip(a_reverse, b_reverse):
            equilibria = self.equilibria(a, b)
            
            if len(equilibria) == 3:
                distances = np.abs(equilibria - current_C)
                current_C = equilibria[np.argmin(distances)]
            elif len(equilibria) == 1:
                current_C = equilibria[0]
            
            C_reverse.append(current_C)
        
        return {
            'b_forward': b_forward,
            'C_forward': np.array(C_forward),
            'b_reverse': b_reverse,
            'C_reverse': np.array(C_reverse)
        }


# ===========================
# 3. FAST-SLOW DYNAMICS
# ===========================

class FastSlowSystem:
    """
    Singular perturbation analysis for consciousness dynamics
    Fast: Φ(t) ~ 100ms
    Slow: R(t) ~ seconds
    """
    
    def __init__(self, epsilon: float = 0.05, phi_max: float = 10.0, R0: float = 1.0):
        """
        Parameters:
        - epsilon: Timescale separation (small)
        - phi_max: Maximum information integration
        - R0: Self-reference characteristic scale
        """
        self.epsilon = epsilon
        self.phi_max = phi_max
        self.R0 = R0
        
    def dynamics(self, state, t, eta=0.5):
        """
        Fast-slow dynamics:
        dΦ/dt = -Φ + Φ_max·tanh(R/R₀) - η
        ε dR/dt = Φ - R
        """
        phi, R = state
        dphi = -phi + self.phi_max * np.tanh(R / self.R0) - eta
        dR = (phi - R) / self.epsilon
        return [dphi, dR]
    
    def slow_manifold(self, R: np.ndarray, eta: float = 0.5) -> np.ndarray:
        """
        Slow manifold: set where fast dynamics equilibrate
        Φ = Φ_max·tanh(R/R₀) - η
        """
        return self.phi_max * np.tanh(R / self.R0) - eta
    
    def simulate_relaxation_oscillation(self, t_span: Tuple = (0, 50), 
                                       initial_state: List = [0.5, 0.5]):
        """
        Simulate trajectory showing relaxation oscillations
        """
        t_eval = np.linspace(t_span[0], t_span[1], 5000)
        solution = odeint(self.dynamics, initial_state, t_eval)
        
        return {
            't': t_eval,
            'phi': solution[:, 0],
            'R': solution[:, 1],
            'C': solution[:, 0] * solution[:, 1]  # Simplified C = Φ·R
        }
    
    def plot_phase_portrait(self, eta_values: List = [0, 0.5, 1.0, 1.5]):
        """
        Phase portrait showing slow manifold and trajectories
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        for idx, eta in enumerate(eta_values):
            ax = axes[idx // 2, idx % 2]
            
            # Simulate trajectory
            result = self.simulate_relaxation_oscillation(initial_state=[0.5, 0.5])
            
            # Plot trajectory
            ax.plot(result['R'], result['phi'], 'b-', linewidth=1.5, alpha=0.7, label='Trajectory')
            
            # Plot slow manifold
            R_manifold = np.linspace(0, 5, 100)
            phi_manifold = self.slow_manifold(R_manifold, eta)
            ax.plot(R_manifold, phi_manifold, 'r--', linewidth=2, label='Slow manifold')
            
            ax.set_xlabel('Self-Reference R (slow)', fontsize=11)
            ax.set_ylabel('Integration Φ (fast)', fontsize=11)
            ax.set_title(f'η = {eta}', fontsize=11)
            ax.legend()
            ax.grid(alpha=0.3)
        
        plt.suptitle('Fast-Slow Dynamics: Phase Portraits', fontsize=14, fontweight='bold')
        plt.tight_layout()
        return fig


# ===========================
# 4. HIRM FULL SYSTEM
# ===========================

class HIRMDynamicalSystem:
    """
    Complete HIRM dynamics with bifurcation detection
    State: [Φ, R, D]
    """
    
    def __init__(self, C_crit: float = 8.3, gamma_decohere: float = 0.1):
        self.C_crit = C_crit
        self.gamma_decohere = gamma_decohere
        
    def dynamics(self, state, t, external_input=0):
        """
        Full HIRM dynamics:
        dΦ/dt = -Φ + 10·tanh(R) + input - 0.5·D
        dR/dt = (Φ - R) / 10
        dD/dt = 0.01·(C - D)
        
        With decoherence term near C_critical
        """
        Phi, R, D = state
        
        # Consciousness measure
        C = Phi * R * D
        
        # Base dynamics
        dPhi = -Phi + 10*np.tanh(R) + external_input - 0.5*D
        dR = (Phi - R) / 10  # Slow
        dD = 0.01 * (C - D)   # Very slow
        
        # Decoherence near C_critical
        if abs(C - self.C_crit) < 0.5 and C > 0:
            decoherence = self.gamma_decohere * (C - self.C_crit)
            dPhi -= decoherence * Phi / C
            dR -= decoherence * R / C
            dD -= decoherence * D / C
        
        return [dPhi, dR, dD]
    
    def compute_jacobian(self, state, external_input=0, epsilon=1e-6):
        """Numerical Jacobian"""
        J = np.zeros((3, 3))
        f0 = np.array(self.dynamics(state, 0, external_input))
        
        for i in range(3):
            state_perturbed = np.array(state, dtype=float)
            state_perturbed[i] += epsilon
            f_perturbed = np.array(self.dynamics(state_perturbed, 0, external_input))
            J[:, i] = (f_perturbed - f0) / epsilon
        
        return J
    
    def detect_bifurcation(self, state):
        """
        Detect if system is near bifurcation point
        """
        Phi, R, D = state
        C = Phi * R * D
        
        # Check C value
        near_critical = abs(C - self.C_crit) < 0.5
        
        # Check eigenvalues
        J = self.compute_jacobian(state)
        eigenvalues = np.linalg.eigvals(J)
        near_zero_eigenvalue = any(abs(eigenvalues.real) < 0.1)
        
        return {
            'C': C,
            'near_C_crit': near_critical,
            'eigenvalues': eigenvalues,
            'near_zero_eig': near_zero_eigenvalue,
            'bifurcating': near_critical and near_zero_eigenvalue
        }
    
    def simulate_transition(self, t_span: Tuple = (0, 100),
                          initial_state: List = [3.0, 1.5, 1.2],
                          input_function: Callable = None):
        """
        Simulate consciousness transition with optional time-varying input
        """
        if input_function is None:
            input_function = lambda t: 0.5 * np.sin(2*np.pi*t/50) + 0.5
        
        t_eval = np.linspace(t_span[0], t_span[1], 1000)
        
        def dynamics_with_input(state, t):
            return self.dynamics(state, t, external_input=input_function(t))
        
        solution = odeint(dynamics_with_input, initial_state, t_eval)
        
        # Compute C(t)
        C_trajectory = solution[:, 0] * solution[:, 1] * solution[:, 2]
        
        # Detect bifurcations
        bifurcation_times = []
        eigenvalue_trajectories = []
        
        for i, state in enumerate(solution[::10]):  # Subsample
            detection = self.detect_bifurcation(state)
            if detection['bifurcating']:
                bifurcation_times.append(t_eval[i*10])
            eigenvalue_trajectories.append(detection['eigenvalues'].real)
        
        return {
            't': t_eval,
            'phi': solution[:, 0],
            'R': solution[:, 1],
            'D': solution[:, 2],
            'C': C_trajectory,
            'bifurcation_times': bifurcation_times,
            'eigenvalues': np.array(eigenvalue_trajectories),
            't_eigenvalues': t_eval[::10]
        }


# ===========================
# 5. BASIN OF ATTRACTION
# ===========================

class BasinAnalyzer:
    """
    Analyze basins of attraction for consciousness states
    """
    
    def __init__(self, system: HIRMDynamicalSystem):
        self.system = system
        
    def map_basin_structure(self, state_ranges: Dict, 
                           n_points: int = 30,
                           fixed_D: float = 1.5) -> Dict:
        """
        Map basin boundaries in (Φ, R) space with D fixed
        """
        Phi_range = np.linspace(state_ranges['Phi'][0], state_ranges['Phi'][1], n_points)
        R_range = np.linspace(state_ranges['R'][0], state_ranges['R'][1], n_points)
        
        basin_map = np.zeros((n_points, n_points))
        
        for i, Phi in enumerate(Phi_range):
            for j, R in enumerate(R_range):
                initial_state = [Phi, R, fixed_D]
                
                # Integrate forward to determine final state
                t_eval = np.linspace(0, 50, 500)
                solution = odeint(self.system.dynamics, initial_state, t_eval, args=(0,))
                
                # Classify based on final C
                final_C = solution[-1, 0] * solution[-1, 1] * solution[-1, 2]
                
                if final_C > self.system.C_crit + 0.5:
                    basin_map[j, i] = 1  # High consciousness
                elif final_C < self.system.C_crit - 0.5:
                    basin_map[j, i] = -1  # Low consciousness
                else:
                    basin_map[j, i] = 0  # Critical region
        
        return {
            'Phi_range': Phi_range,
            'R_range': R_range,
            'basin_map': basin_map
        }
    
    def compute_resilience(self, basin_map: np.ndarray) -> Dict:
        """
        Quantify resilience based on basin size
        """
        high_consciousness_volume = np.sum(basin_map == 1)
        low_consciousness_volume = np.sum(basin_map == -1)
        total_volume = basin_map.size
        
        return {
            'high_consciousness_resilience': high_consciousness_volume / total_volume,
            'low_consciousness_resilience': low_consciousness_volume / total_volume,
            'critical_region_fraction': np.sum(basin_map == 0) / total_volume
        }


# ===========================
# 6. EXPERIMENTAL PREDICTIONS
# ===========================

class ExperimentalPredictor:
    """
    Generate predictions for experimental validation
    """
    
    @staticmethod
    def perturbation_response_curve(baseline_C: float, C_crit: float = 8.3,
                                    n_intensities: int = 50) -> Dict:
        """
        Predict response to perturbations of varying intensity
        """
        intensities = np.linspace(0, 2, n_intensities)
        distance_from_critical = abs(baseline_C - C_crit)
        
        # Response amplification near bifurcation
        response_amplitude = intensities / (distance_from_critical + 0.1)
        
        # Add critical fluctuations
        noise_level = 1.0 / (distance_from_critical + 0.2)
        responses = response_amplitude + noise_level * np.random.randn(n_intensities)
        
        return {
            'intensities': intensities,
            'responses': responses,
            'baseline_C': baseline_C
        }
    
    @staticmethod
    def critical_slowing_prediction(baseline_C_range: np.ndarray, 
                                   C_crit: float = 8.3) -> Dict:
        """
        Predict critical slowing (response time divergence) near C_critical
        """
        response_times = []
        
        for baseline_C in baseline_C_range:
            distance = abs(baseline_C - C_crit)
            # τ ∝ 1/√|μ|
            tau = 1.0 / (np.sqrt(distance) + 0.01)
            response_times.append(tau)
        
        return {
            'baseline_C': baseline_C_range,
            'response_times': np.array(response_times)
        }
    
    @staticmethod
    def hysteresis_loop_prediction(arousal_values: np.ndarray,
                                   cusp_model: CuspCatastrophe) -> Dict:
        """
        Predict hysteresis loops for different arousal baselines
        """
        loops = {}
        
        for arousal in arousal_values:
            loop = cusp_model.simulate_hysteresis_loop(arousal_baseline=arousal)
            loops[f'arousal_{arousal:.2f}'] = loop
        
        return loops


# ===========================
# 7. VISUALIZATION SUITE
# ===========================

class BifurcationVisualizer:
    """
    Comprehensive visualization tools
    """
    
    @staticmethod
    def plot_full_hirm_simulation(result: Dict, C_crit: float = 8.3):
        """
        Create comprehensive plot of HIRM simulation
        """
        fig, axes = plt.subplots(3, 1, figsize=(12, 10))
        
        # C(t) trajectory
        axes[0].plot(result['t'], result['C'], 'b-', linewidth=2)
        axes[0].axhline(y=C_crit, color='r', linestyle='--', linewidth=2, label='C_critical')
        axes[0].fill_between(result['t'], C_crit-0.5, C_crit+0.5, alpha=0.2, color='red')
        
        for bt in result['bifurcation_times']:
            axes[0].axvline(x=bt, color='orange', alpha=0.5, linestyle=':')
        
        axes[0].set_ylabel('C(t) (bits)', fontsize=11)
        axes[0].set_title('Consciousness Measure Through Bifurcation', fontsize=12, fontweight='bold')
        axes[0].legend()
        axes[0].grid(alpha=0.3)
        
        # Phase space
        axes[1].plot(result['phi'], result['R'], 'g-', linewidth=1.5, alpha=0.7)
        axes[1].plot(result['phi'][0], result['R'][0], 'go', markersize=10, label='Start')
        axes[1].plot(result['phi'][-1], result['R'][-1], 'ro', markersize=10, label='End')
        axes[1].set_xlabel('Φ (bits)', fontsize=11)
        axes[1].set_ylabel('R (self-reference)', fontsize=11)
        axes[1].set_title('Phase Space Trajectory', fontsize=12, fontweight='bold')
        axes[1].legend()
        axes[1].grid(alpha=0.3)
        
        # Eigenvalue evolution
        for i in range(result['eigenvalues'].shape[1]):
            axes[2].plot(result['t_eigenvalues'], result['eigenvalues'][:, i], 
                        linewidth=2, label=f'λ_{i+1}')
        
        axes[2].axhline(y=0, color='k', linestyle='--', alpha=0.5)
        axes[2].set_xlabel('Time (s)', fontsize=11)
        axes[2].set_ylabel('Re(λ)', fontsize=11)
        axes[2].set_title('Stability (Eigenvalue Evolution)', fontsize=12, fontweight='bold')
        axes[2].legend()
        axes[2].grid(alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_basin_structure(basin_result: Dict, C_crit: float = 8.3):
        """
        Visualize basin of attraction structure
        """
        plt.figure(figsize=(10, 8))
        
        cf = plt.contourf(basin_result['Phi_range'], basin_result['R_range'], 
                    basin_result['basin_map'], 
                    levels=[-1.5, -0.5, 0.5, 1.5],
                    colors=['blue', 'gray', 'red'], alpha=0.6)
        
        plt.contour(basin_result['Phi_range'], basin_result['R_range'],
                   basin_result['basin_map'], levels=[0], 
                   colors='black', linewidths=2)
        
        cbar = plt.colorbar(cf, ticks=[-1, 0, 1])
        cbar.set_label('Basin Classification', fontsize=11)
        plt.xlabel('Φ (bits)', fontsize=12)
        plt.ylabel('R (self-reference)', fontsize=12)
        plt.title('Basins of Attraction for Consciousness States', 
                 fontsize=14, fontweight='bold')
        plt.grid(alpha=0.3)
        
        return plt.gcf()


# ===========================
# 8. EXAMPLE USAGE
# ===========================

def demo_complete_analysis():
    """
    Demonstration of full bifurcation analysis workflow
    """
    print("=" * 60)
    print("HIRM BIFURCATION ANALYSIS DEMONSTRATION")
    print("=" * 60)
    
    # 1. Normal form analysis
    print("\n1. SADDLE-NODE BIFURCATION (Anesthesia)")
    analyzer_sn = BifurcationAnalyzer(BifurcationDynamics.saddle_node, dim=1)
    mu_range = np.linspace(-0.5, 0.5, 100)
    analyzer_sn.create_bifurcation_diagram(mu_range, [np.array([2.0]), np.array([-2.0])])
    plt.savefig('/mnt/user-data/outputs/saddle_node_bifurcation.png', dpi=150, bbox_inches='tight')
    print("   ✓ Bifurcation diagram saved")
    
    # 2. Cusp catastrophe
    print("\n2. CUSP CATASTROPHE (Hysteresis)")
    cusp = CuspCatastrophe()
    cusp.plot_behavior_surface()
    plt.savefig('/mnt/user-data/outputs/cusp_catastrophe.png', dpi=150, bbox_inches='tight')
    print("   ✓ Behavior surface saved")
    
    # 3. Fast-slow dynamics
    print("\n3. FAST-SLOW DYNAMICS (Relaxation Oscillations)")
    fast_slow = FastSlowSystem(epsilon=0.05)
    fast_slow.plot_phase_portrait()
    plt.savefig('/mnt/user-data/outputs/fast_slow_dynamics.png', dpi=150, bbox_inches='tight')
    print("   ✓ Phase portraits saved")
    
    # 4. Full HIRM simulation
    print("\n4. HIRM FULL SYSTEM SIMULATION")
    hirm = HIRMDynamicalSystem(C_crit=8.3)
    result = hirm.simulate_transition()
    BifurcationVisualizer.plot_full_hirm_simulation(result)
    plt.savefig('/mnt/user-data/outputs/hirm_full_simulation.png', dpi=150, bbox_inches='tight')
    print("   ✓ Full simulation saved")
    print(f"   Bifurcation events detected: {len(result['bifurcation_times'])}")
    
    # 5. Basin analysis
    print("\n5. BASIN OF ATTRACTION ANALYSIS")
    basin_analyzer = BasinAnalyzer(hirm)
    basin_result = basin_analyzer.map_basin_structure(
        {'Phi': [0, 10], 'R': [0, 3]}, n_points=30
    )
    resilience = basin_analyzer.compute_resilience(basin_result['basin_map'])
    BifurcationVisualizer.plot_basin_structure(basin_result)
    plt.savefig('/mnt/user-data/outputs/basin_structure.png', dpi=150, bbox_inches='tight')
    print("   ✓ Basin structure saved")
    print(f"   High consciousness resilience: {resilience['high_consciousness_resilience']:.3f}")
    
    # 6. Experimental predictions
    print("\n6. EXPERIMENTAL PREDICTIONS")
    predictor = ExperimentalPredictor()
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Perturbation responses
    for baseline_C in [7.5, 8.0, 8.3, 8.6, 9.0]:
        pred = predictor.perturbation_response_curve(baseline_C)
        label = f'C = {baseline_C}' + (' (critical)' if baseline_C == 8.3 else '')
        axes[0].plot(pred['intensities'], pred['responses'], linewidth=2, label=label)
    
    axes[0].set_xlabel('Perturbation Intensity', fontsize=11)
    axes[0].set_ylabel('Response (PCI)', fontsize=11)
    axes[0].set_title('Perturbation-Response Curves', fontsize=12, fontweight='bold')
    axes[0].legend()
    axes[0].grid(alpha=0.3)
    
    # Critical slowing
    baseline_range = np.linspace(7, 10, 50)
    slowing = predictor.critical_slowing_prediction(baseline_range)
    axes[1].plot(slowing['baseline_C'], slowing['response_times'], 'b-', linewidth=2)
    axes[1].axvline(x=8.3, color='r', linestyle='--', linewidth=2, label='C_critical')
    axes[1].set_xlabel('Baseline C (bits)', fontsize=11)
    axes[1].set_ylabel('Response Time τ', fontsize=11)
    axes[1].set_title('Critical Slowing', fontsize=12, fontweight='bold')
    axes[1].legend()
    axes[1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/experimental_predictions.png', dpi=150, bbox_inches='tight')
    print("   ✓ Experimental predictions saved")
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("All figures saved to /mnt/user-data/outputs/")
    print("=" * 60)
    
    return {
        'hirm_result': result,
        'basin_result': basin_result,
        'resilience': resilience
    }


if __name__ == "__main__":
    # Run demonstration
    results = demo_complete_analysis()
    
    print("\n✓ Bifurcation analysis toolkit ready for use")
    print("✓ Import this module to access all classes and functions")
    print("✓ See documentation in comprehensive framework document")
