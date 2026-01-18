"""
HIRM Renormalization Group Toolkit
Complete implementation of RG flow analysis, critical exponent extraction,
and multi-scale coarse-graining algorithms.

Author: HIRM Research Project
Date: October 26, 2025
Version: 2.0
"""

import numpy as np
from scipy.integrate import odeint
from scipy.optimize import curve_fit, fsolve
from scipy.stats import linregress
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Callable

# ============================================================================
# RG FLOW EQUATIONS
# ============================================================================

def beta_functions(x: np.ndarray, ell: float, params: Dict) -> np.ndarray:
    """
    Complete β-function system for HIRM consciousness parameters.
    
    Parameters:
    -----------
    x : array [C, Phi, R, D]
        Current values of consciousness parameters
    ell : float
        RG scale parameter (log of coarse-graining factor)
    params : dict
        Dictionary of coupling constants
        
    Returns:
    --------
    dxdell : array
        Derivatives [dC/dℓ, dΦ/dℓ, dR/dℓ, dD/dℓ]
    """
    C, Phi, R, D = x
    
    # Extract parameters with defaults
    gamma_C = params.get('gamma_C', 0.15)
    C_star = params.get('C_star', 8.3)
    alpha_Phi = params.get('alpha_Phi', 0.8)
    alpha_R = params.get('alpha_R', 2.1)
    gamma_Phi = params.get('gamma_Phi', 0.2)
    Phi_c = params.get('Phi_c', 4.5)
    beta_C = params.get('beta_C', 0.3)
    beta_sigma = params.get('beta_sigma', 0.5)
    sigma = params.get('sigma', 1.0)
    c0 = params.get('c0', 0.1)
    c1 = params.get('c1', 0.2)
    c2 = params.get('c2', 0.05)
    d0 = params.get('d0', 0.4)
    C_bif = params.get('C_bif', 7.5)
    w_D = params.get('w_D', 1.0)
    noise_amp = params.get('noise_amp', 0.05)
    
    # Φ flow equation
    dPhi_dell = -gamma_Phi * (Phi - Phi_c) + beta_C * C + beta_sigma * (sigma - 1)
    
    # C flow equation (consciousness)
    beta_C_val = (-gamma_C * (C - C_star) + 
                  alpha_Phi * Phi * dPhi_dell + 
                  alpha_R * np.sqrt(np.maximum(R - 1, 0)) +
                  noise_amp * np.random.randn())
    
    # R flow equation (self-reference)
    beta_R_val = (R - 1) * (c0 + c1 * C - c2 * R**2)
    
    # D flow equation (dimensionality)
    beta_D_val = d0 * np.tanh((C - C_bif) / w_D)
    
    return np.array([beta_C_val, dPhi_dell, beta_R_val, beta_D_val])


def integrate_rg_flow(initial_condition: np.ndarray, 
                      ell_range: np.ndarray,
                      params: Dict,
                      method: str = 'odeint') -> np.ndarray:
    """
    Integrate RG flow equations from initial condition.
    
    Parameters:
    -----------
    initial_condition : array [C0, Phi0, R0, D0]
    ell_range : array
        Range of scale parameters to integrate over
    params : dict
        RG parameters
    method : str
        Integration method ('odeint' or 'rk4')
        
    Returns:
    --------
    trajectory : array (len(ell_range), 4)
        Evolution of [C, Phi, R, D] along RG flow
    """
    if method == 'odeint':
        trajectory = odeint(beta_functions, initial_condition, ell_range, 
                          args=(params,), rtol=1e-6, atol=1e-8)
    else:
        # Manual RK4 integration
        trajectory = np.zeros((len(ell_range), 4))
        trajectory[0] = initial_condition
        
        for i in range(len(ell_range) - 1):
            dt = ell_range[i+1] - ell_range[i]
            x = trajectory[i]
            
            k1 = beta_functions(x, ell_range[i], params)
            k2 = beta_functions(x + 0.5*dt*k1, ell_range[i] + 0.5*dt, params)
            k3 = beta_functions(x + 0.5*dt*k2, ell_range[i] + 0.5*dt, params)
            k4 = beta_functions(x + dt*k3, ell_range[i+1], params)
            
            trajectory[i+1] = x + (dt/6)*(k1 + 2*k2 + 2*k3 + k4)
    
    return trajectory


def find_fixed_point(params: Dict, 
                     initial_guess: np.ndarray = None) -> Tuple[np.ndarray, bool]:
    """
    Find RG fixed point by solving β(x*) = 0.
    
    Parameters:
    -----------
    params : dict
        RG parameters
    initial_guess : array, optional
        Starting point for solver
        
    Returns:
    --------
    x_star : array [C*, Phi*, R*, D*]
    success : bool
    """
    if initial_guess is None:
        initial_guess = np.array([8.0, 4.5, 1.9, 0.85])
    
    def equations(x):
        return beta_functions(x, 0, params)
    
    solution = fsolve(equations, initial_guess, full_output=True)
    x_star = solution[0]
    info = solution[1]
    success = (info['fvec']**2).sum() < 1e-10
    
    return x_star, success


def compute_jacobian(x_star: np.ndarray, params: Dict, eps: float = 1e-6) -> np.ndarray:
    """
    Compute Jacobian matrix at fixed point: J_ij = ∂β_i/∂x_j
    
    Parameters:
    -----------
    x_star : array
        Fixed point coordinates
    params : dict
        RG parameters
    eps : float
        Finite difference step size
        
    Returns:
    --------
    J : array (4, 4)
        Jacobian matrix
    """
    n = len(x_star)
    J = np.zeros((n, n))
    
    beta_0 = beta_functions(x_star, 0, params)
    
    for j in range(n):
        x_perturbed = x_star.copy()
        x_perturbed[j] += eps
        beta_perturbed = beta_functions(x_perturbed, 0, params)
        J[:, j] = (beta_perturbed - beta_0) / eps
    
    return J


# ============================================================================
# CRITICAL EXPONENTS
# ============================================================================

def extract_critical_exponents(C_data: np.ndarray,
                               epsilon_data: np.ndarray,
                               xi_data: np.ndarray = None,
                               M_data: np.ndarray = None,
                               chi_data: np.ndarray = None) -> Dict:
    """
    Extract critical exponents from numerical or experimental data.
    
    Parameters:
    -----------
    C_data : array
        Consciousness measure values
    epsilon_data : array  
        Reduced distance from critical point: ε = (C - C*)/C*
    xi_data : array, optional
        Correlation lengths
    M_data : array, optional
        Order parameter (e.g., Φ - Φ*)
    chi_data : array, optional
        Susceptibility measurements
        
    Returns:
    --------
    exponents : dict
        {'nu': ν, 'beta': β, 'gamma': γ, 'errors': {...}}
    """
    exponents = {}
    errors = {}
    
    # Filter out epsilon = 0
    valid = np.abs(epsilon_data) > 1e-10
    eps_valid = epsilon_data[valid]
    
    # Correlation length exponent ν
    if xi_data is not None:
        xi_valid = xi_data[valid]
        log_eps = np.log(np.abs(eps_valid))
        log_xi = np.log(xi_valid)
        
        slope, intercept, r_value, p_value, std_err = linregress(log_eps, log_xi)
        
        exponents['nu'] = -slope
        errors['nu'] = std_err
        exponents['nu_r_squared'] = r_value**2
    
    # Order parameter exponent β
    if M_data is not None:
        M_valid = np.abs(M_data[valid])
        log_M = np.log(M_valid[M_valid > 0])
        log_eps_M = log_eps[M_valid > 0]
        
        slope_beta, intercept_beta, r_beta, p_beta, std_err_beta = linregress(
            log_eps_M, log_M)
        
        exponents['beta'] = slope_beta
        errors['beta'] = std_err_beta
        exponents['beta_r_squared'] = r_beta**2
    
    # Susceptibility exponent γ  
    if chi_data is not None:
        chi_valid = chi_data[valid]
        log_chi = np.log(chi_valid[chi_valid > 0])
        log_eps_chi = log_eps[chi_valid > 0]
        
        slope_gamma, intercept_gamma, r_gamma, p_gamma, std_err_gamma = linregress(
            log_eps_chi, log_chi)
        
        exponents['gamma'] = -slope_gamma
        errors['gamma'] = std_err_gamma
        exponents['gamma_r_squared'] = r_gamma**2
    
    exponents['errors'] = errors
    
    # Check scaling relations if enough exponents computed
    if 'nu' in exponents and 'gamma' in exponents:
        eta_estimated = 2 - exponents['gamma']/exponents['nu']
        exponents['eta_estimated'] = eta_estimated
        
        print(f"\nScaling Relation Check (Fisher):")
        print(f"  γ = ν(2 - η)")
        print(f"  LHS: γ = {exponents['gamma']:.3f}")
        print(f"  RHS: ν(2 - η_est) = {exponents['nu'] * (2 - eta_estimated):.3f}")
    
    return exponents


def universality_class_identification(exponents: Dict) -> str:
    """
    Identify universality class based on measured exponents.
    
    Parameters:
    -----------
    exponents : dict
        Measured critical exponents
        
    Returns:
    --------
    class_name : str
        Identified universality class
    """
    # Known universality classes
    classes = {
        '3D Ising': {'nu': 0.630, 'beta': 0.326, 'gamma': 1.237, 'eta': 0.036},
        'Mean Field': {'nu': 0.5, 'beta': 0.5, 'gamma': 1.0, 'eta': 0.0},
        '3D Percolation': {'nu': 0.875, 'beta': 0.417, 'gamma': 1.805, 'eta': 0.037},
        '3D XY': {'nu': 0.672, 'beta': 0.346, 'gamma': 1.316, 'eta': 0.038},
    }
    
    # Compute distances
    min_distance = float('inf')
    best_class = 'Unknown'
    
    for class_name, class_exps in classes.items():
        distance = 0
        count = 0
        
        for key in ['nu', 'beta', 'gamma']:
            if key in exponents and key in class_exps:
                distance += (exponents[key] - class_exps[key])**2
                count += 1
        
        if count > 0:
            distance = np.sqrt(distance / count)
            
            if distance < min_distance:
                min_distance = distance
                best_class = class_name
    
    print(f"\nUniversality Class Identification:")
    print(f"  Best match: {best_class}")
    print(f"  Distance: {min_distance:.4f}")
    
    return best_class


# ============================================================================
# NEURAL COARSE-GRAINING
# ============================================================================

def neural_block_spin_rg(neural_data: np.ndarray, 
                        block_size: int,
                        transformation_type: str = 'mean') -> np.ndarray:
    """
    Perform block-spin RG transformation on neural activity.
    
    Parameters:
    -----------
    neural_data : array (N_neurons, T_timesteps)
        Neural spike trains or activity
    block_size : int
        Number of neurons per block
    transformation_type : str
        'mean', 'majority', or 'weighted'
        
    Returns:
    --------
    coarse_data : array (N_blocks, T_timesteps)
        Coarse-grained activity
    """
    N_neurons, T = neural_data.shape
    N_blocks = N_neurons // block_size
    
    # Truncate to fit blocks evenly
    truncated_data = neural_data[:N_blocks * block_size]
    
    # Reshape into blocks
    blocked_data = truncated_data.reshape(N_blocks, block_size, T)
    
    if transformation_type == 'mean':
        # Block spin = average activity
        coarse_data = np.mean(blocked_data, axis=1)
        
    elif transformation_type == 'majority':
        # Majority vote (for binary spikes)
        coarse_data = (np.sum(blocked_data, axis=1) > block_size/2).astype(float)
        
    elif transformation_type == 'weighted':
        # Weighted average (weight by neuron importance)
        weights = np.random.rand(block_size)  # Could be data-driven
        weights /= weights.sum()
        coarse_data = np.tensordot(blocked_data, weights, axes=([1], [0]))
    
    return coarse_data


def compute_avalanche_distribution(activity_data: np.ndarray, 
                                  threshold: float = 0) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute avalanche size distribution from activity data.
    
    Parameters:
    -----------
    activity_data : array (N, T)
        Neural activity time series
    threshold : float
        Threshold for considering activity
        
    Returns:
    --------
    sizes : array
        Avalanche sizes
    counts : array  
        Probability distribution P(size)
    """
    T = activity_data.shape[1]
    avalanches = []
    
    # Compute total activity at each time
    total_activity = np.sum(activity_data > threshold, axis=0)
    
    # Detect avalanches
    in_avalanche = False
    current_size = 0
    
    for t in range(T):
        if total_activity[t] > 0:
            current_size += total_activity[t]
            in_avalanche = True
        else:
            if in_avalanche and current_size > 0:
                avalanches.append(current_size)
                current_size = 0
            in_avalanche = False
    
    # Histogram
    if len(avalanches) > 0:
        sizes, counts = np.unique(avalanches, return_counts=True)
        counts = counts.astype(float) / counts.sum()
    else:
        sizes, counts = np.array([]), np.array([])
    
    return sizes, counts


def fit_power_law(x_data: np.ndarray, 
                  y_data: np.ndarray,
                  x_min: float = None) -> Tuple[float, float, float]:
    """
    Fit power law: y = A * x^(-τ)
    
    Parameters:
    -----------
    x_data, y_data : arrays
        Data to fit
    x_min : float, optional
        Minimum x value to include in fit
        
    Returns:
    --------
    tau : float
        Power law exponent
    A : float
        Prefactor
    r_squared : float
        Goodness of fit
    """
    if x_min is not None:
        valid = x_data >= x_min
        x_data = x_data[valid]
        y_data = y_data[valid]
    
    # Log-log linear regression
    valid = (x_data > 0) & (y_data > 0)
    log_x = np.log(x_data[valid])
    log_y = np.log(y_data[valid])
    
    slope, intercept, r_value, _, _ = linregress(log_x, log_y)
    
    tau = -slope
    A = np.exp(intercept)
    r_squared = r_value**2
    
    return tau, A, r_squared


# ============================================================================
# VISUALIZATION
# ============================================================================

def plot_rg_flow_phase_diagram(initial_conditions: List[np.ndarray],
                               params: Dict,
                               ell_range: np.ndarray,
                               save_path: str = None):
    """
    Create comprehensive RG flow phase diagram.
    """
    fig = plt.figure(figsize=(16, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # Individual parameter flows
    ax_C = fig.add_subplot(gs[0, 0])
    ax_Phi = fig.add_subplot(gs[0, 1])
    ax_R = fig.add_subplot(gs[0, 2])
    ax_D = fig.add_subplot(gs[1, 0])
    
    # Phase space projections
    ax_CPhi = fig.add_subplot(gs[1, 1])
    ax_RD = fig.add_subplot(gs[1, 2])
    
    # Combined trajectories
    ax_combined = fig.add_subplot(gs[2, :])
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(initial_conditions)))
    
    # Fixed point
    x_star, success = find_fixed_point(params)
    if success:
        C_star, Phi_star, R_star, D_star = x_star
    else:
        C_star, Phi_star, R_star, D_star = 8.3, 4.82, 1.95, 0.89
    
    for i, x0 in enumerate(initial_conditions):
        traj = integrate_rg_flow(x0, ell_range, params)
        
        # Individual flows
        ax_C.plot(ell_range, traj[:, 0], color=colors[i], linewidth=2, 
                 label=f'IC{i+1}' if i < 3 else '')
        ax_Phi.plot(ell_range, traj[:, 1], color=colors[i], linewidth=2)
        ax_R.plot(ell_range, traj[:, 2], color=colors[i], linewidth=2)
        ax_D.plot(ell_range, traj[:, 3], color=colors[i], linewidth=2)
        
        # Phase space
        ax_CPhi.plot(traj[:, 0], traj[:, 1], color=colors[i], linewidth=2, alpha=0.7)
        ax_CPhi.scatter(x0[0], x0[1], color=colors[i], s=100, marker='o', 
                       edgecolors='black', zorder=5)
        
        ax_RD.plot(traj[:, 2], traj[:, 3], color=colors[i], linewidth=2, alpha=0.7)
        ax_RD.scatter(x0[2], x0[3], color=colors[i], s=100, marker='o',
                     edgecolors='black', zorder=5)
        
        # Combined normalized
        traj_norm = traj / x_star
        ax_combined.plot(ell_range, traj_norm[:, 0], color=colors[i], 
                        linewidth=2, linestyle='-', label='C/C*' if i==0 else '')
        ax_combined.plot(ell_range, traj_norm[:, 1], color=colors[i],
                        linewidth=1.5, linestyle='--', alpha=0.7,
                        label='Φ/Φ*' if i==0 else '')
    
    # Fixed point markers
    for ax, val, label in [(ax_C, C_star, 'C*'), (ax_Phi, Phi_star, 'Φ*'),
                           (ax_R, R_star, 'R*'), (ax_D, D_star, 'D*')]:
        ax.axhline(val, color='red', linestyle='--', linewidth=2, alpha=0.7)
        ax.text(ell_range[-1]*0.95, val*1.05, label, fontsize=12, color='red',
               fontweight='bold')
    
    ax_CPhi.scatter(C_star, Phi_star, color='red', s=200, marker='*',
                   edgecolors='black', linewidths=2, zorder=10, label='Fixed Point')
    ax_RD.scatter(R_star, D_star, color='red', s=200, marker='*',
                 edgecolors='black', linewidths=2, zorder=10)
    
    ax_combined.axhline(1.0, color='red', linestyle='--', linewidth=2, alpha=0.7)
    
    # Labels and styling
    ax_C.set_ylabel('C (bits)', fontsize=12, fontweight='bold')
    ax_Phi.set_ylabel('Φ (bits)', fontsize=12, fontweight='bold')
    ax_R.set_ylabel('R', fontsize=12, fontweight='bold')
    ax_D.set_ylabel('D', fontsize=12, fontweight='bold')
    
    for ax in [ax_C, ax_Phi, ax_R, ax_D]:
        ax.set_xlabel('Scale ℓ = log(Λ/Λ₀)', fontsize=11)
        ax.grid(alpha=0.3)
        ax.legend(fontsize=9)
    
    ax_CPhi.set_xlabel('C (bits)', fontsize=12)
    ax_CPhi.set_ylabel('Φ (bits)', fontsize=12)
    ax_CPhi.set_title('C-Φ Phase Space', fontsize=13, fontweight='bold')
    ax_CPhi.grid(alpha=0.3)
    ax_CPhi.legend()
    
    ax_RD.set_xlabel('R', fontsize=12)
    ax_RD.set_ylabel('D', fontsize=12)
    ax_RD.set_title('R-D Phase Space', fontsize=13, fontweight='bold')
    ax_RD.grid(alpha=0.3)
    
    ax_combined.set_xlabel('Scale ℓ = log(Λ/Λ₀)', fontsize=12)
    ax_combined.set_ylabel('Normalized Parameters', fontsize=12)
    ax_combined.set_title('Normalized RG Flow Convergence', fontsize=13, fontweight='bold')
    ax_combined.grid(alpha=0.3)
    ax_combined.legend(fontsize=10)
    
    plt.suptitle('HIRM Renormalization Group Flow Analysis', 
                fontsize=16, fontweight='bold', y=0.995)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        plt.savefig('/home/claude/hirm_rg_flow_complete.png', dpi=300, bbox_inches='tight')
    
    plt.close()


# ============================================================================
# DEFAULT PARAMETERS
# ============================================================================

DEFAULT_RG_PARAMS = {
    'gamma_C': 0.15,
    'C_star': 8.3,
    'alpha_Phi': 0.8,
    'alpha_R': 2.1,
    'gamma_Phi': 0.2,
    'Phi_c': 4.5,
    'beta_C': 0.3,
    'beta_sigma': 0.5,
    'sigma': 1.0,
    'c0': 0.1,
    'c1': 0.2,
    'c2': 0.05,
    'd0': 0.4,
    'C_bif': 7.5,
    'w_D': 1.0,
    'noise_amp': 0.0
}
