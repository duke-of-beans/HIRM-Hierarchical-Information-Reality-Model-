"""
HIRM Simulation: Kuramoto Oscillator Network with Recurrent Coupling
Created: 2026-01-18
Purpose: Controllable synthetic neural system for HIRM validation
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import sys
sys.path.append('D:/Research/HIRM/Code/Core')

from consciousness_measure import ConsciousnessMeasure


class KuramotoNetwork:
    """
    Extended Kuramoto oscillator network with recurrent coupling.
    
    Allows independent control of:
    - Integration (via global coupling K)
    - Self-reference (via recurrent weight matrix W)
    - Dimensionality (via frequency distribution)
    """
    
    def __init__(
        self,
        N: int = 50,
        K: float = 1.0,
        omega_mean: float = 1.0,
        omega_std: float = 0.5,
        W_recurrent: np.ndarray = None,
        alpha: float = 0.5,
        seed: int = 42
    ):
        """
        Parameters
        ----------
        N : int
            Number of oscillators
        K : float
            Global coupling strength (controls integration)
        omega_mean : float
            Mean natural frequency
        omega_std : float
            Std of natural frequencies (controls dimensionality)
        W_recurrent : np.ndarray or None
            Recurrent weight matrix (controls self-reference)
            If None, uses feedforward (no recurrence)
        alpha : float
            Self-reference strength parameter
        seed : int
            Random seed for reproducibility
        """
        np.random.seed(seed)
        
        self.N = N
        self.K = K
        self.alpha = alpha
        
        # Natural frequencies (controls dimensionality)
        self.omega = np.random.normal(omega_mean, omega_std, N)
        
        # Recurrent connectivity (controls self-reference)
        if W_recurrent is None:
            # Default: feedforward only (no recurrence)
            self.W = np.zeros((N, N))
        else:
            self.W = W_recurrent
            
        # Phase delays (creates temporal structure)
        self.phi = np.random.uniform(0, 2*np.pi, (N, N))
        
    def dynamics(self, theta: np.ndarray, t: float) -> np.ndarray:
        """
        Kuramoto dynamics with recurrent coupling.
        
        dθᵢ/dt = ωᵢ + (K/N) Σⱼ sin(θⱼ - θᵢ) + αᵢ Σⱼ W_ij sin(θⱼ - θᵢ - φ_ij)
        """
        dtheta = np.zeros(self.N)
        
        for i in range(self.N):
            # Global coupling term (integration)
            global_coupling = (self.K / self.N) * np.sum(
                np.sin(theta - theta[i])
            )
            
            # Recurrent coupling term (self-reference)
            recurrent_coupling = self.alpha * np.sum(
                self.W[i, :] * np.sin(theta - theta[i] - self.phi[i, :])
            )
            
            dtheta[i] = self.omega[i] + global_coupling + recurrent_coupling
            
        return dtheta
    
    def simulate(
        self,
        duration: float = 30.0,
        dt: float = 0.01,
        theta0: np.ndarray = None
    ) -> tuple:
        """
        Simulate network dynamics.
        
        Parameters
        ----------
        duration : float
            Simulation duration (seconds)
        dt : float
            Time step
        theta0 : np.ndarray or None
            Initial phases (random if None)
            
        Returns
        -------
        t : np.ndarray
            Time points
        theta : np.ndarray
            Phase trajectories (time × N)
        activity : np.ndarray
            Neural activity signals (N × time)
        """
        # Initial conditions
        if theta0 is None:
            theta0 = np.random.uniform(0, 2*np.pi, self.N)
        
        # Time points
        t = np.arange(0, duration, dt)
        
        # Integrate
        theta = odeint(self.dynamics, theta0, t)
        
        # Convert phases to activity (sine wave approximation of neural signal)
        activity = np.sin(theta.T)  # (N, time)
        
        return t, theta, activity


def create_recurrent_network(
    N: int,
    recurrence_type: str = 'none',
    sparsity: float = 0.1
) -> np.ndarray:
    """
    Create recurrent weight matrix with different structures.
    
    Parameters
    ----------
    N : int
        Number of nodes
    recurrence_type : str
        'none' - feedforward only (no recurrence)
        'sparse' - random sparse recurrent connections
        'hierarchical' - hierarchical recurrent structure
    sparsity : float
        Connection density for sparse/hierarchical
        
    Returns
    -------
    W : np.ndarray
        Recurrent weight matrix (N × N)
    """
    if recurrence_type == 'none':
        return np.zeros((N, N))
    
    elif recurrence_type == 'sparse':
        # Random sparse connections
        W = np.random.rand(N, N)
        W[W > sparsity] = 0
        W[W > 0] = 1.0
        return W / (W.sum(axis=1, keepdims=True) + 1e-10)
    
    elif recurrence_type == 'hierarchical':
        # Hierarchical structure with multiple recurrent loops
        W = np.zeros((N, N))
        
        # Level 1: Local recurrent loops (neighbors)
        for i in range(N):
            neighbors = [(i-1) % N, (i+1) % N]
            W[i, neighbors] = 1.0
            
        # Level 2: Medium-range loops
        for i in range(0, N, 5):
            targets = [(i+5) % N, (i-5) % N]
            W[i, targets] = 0.5
            
        # Level 3: Global recurrent pathways
        for i in range(0, N, 10):
            targets = [(i + N//2) % N]
            W[i, targets] = 0.3
            
        return W / (W.sum(axis=1, keepdims=True) + 1e-10)
    
    else:
        raise ValueError(f"Unknown recurrence_type: {recurrence_type}")


def run_condition(
    name: str,
    N: int,
    K: float,
    omega_std: float,
    recurrence_type: str,
    duration: float = 30.0,
    dt: float = 0.01
) -> dict:
    """
    Run one experimental condition.
    
    Returns
    -------
    results : dict
        Contains network, activity, and HIRM measurements
    """
    print(f"\n[WIP] Running condition: {name}")
    print(f"  N={N}, K={K:.2f}, omega_std={omega_std:.2f}, recurrence={recurrence_type}")
    
    # Create network
    W = create_recurrent_network(N, recurrence_type=recurrence_type, sparsity=0.1)
    network = KuramotoNetwork(
        N=N,
        K=K,
        omega_mean=1.0,
        omega_std=omega_std,
        W_recurrent=W,
        alpha=0.5
    )
    
    # Simulate
    t, theta, activity = network.simulate(duration=duration, dt=dt)
    print(f"  [OK] Simulation complete: {activity.shape}")
    
    # Measure consciousness
    cm = ConsciousnessMeasure(
        Phi_method='PSI',
        temporal_window=int(duration / dt),
        D_max=N * 0.8,  # Scale with network size
        Phi_scale=1.0
    )
    
    # Compute connectivity from activity
    connectivity = np.corrcoef(activity)
    connectivity = np.abs(connectivity)
    np.fill_diagonal(connectivity, 1.0)
    connectivity += 0.1 * np.eye(N)  # Regularization
    
    # Calculate on activity window
    result = cm.calculate_C(activity, connectivity)
    
    print(f"  [OK] HIRM measurement complete:")
    print(f"    Phi = {result['Phi']:.3f} bits")
    print(f"    R = {result['R_theory']:.3f}")
    print(f"    D = {result['D_eff']:.3f}")
    print(f"    C = {result['C']:.3f} bits")
    
    return {
        'name': name,
        'network': network,
        't': t,
        'theta': theta,
        'activity': activity,
        'Phi': result['Phi'],
        'R': result['R_theory'],
        'D': result['D_eff'],
        'C': result['C']
    }


if __name__ == '__main__':
    print("="*70)
    print("HIRM SIMULATION VALIDATION")
    print("="*70)
    
    # Configuration
    N = 50  # Number of oscillators
    duration = 30.0  # seconds
    dt = 0.01  # time step
    
    # Run all conditions
    conditions = []
    
    # Condition 1: Unconscious (low integration, no recurrence, low dimensionality)
    conditions.append(run_condition(
        name='Unconscious',
        N=N,
        K=0.1,  # Weak coupling
        omega_std=0.1,  # Narrow frequency distribution
        recurrence_type='none',  # No recurrence
        duration=duration,
        dt=dt
    ))
    
    # Condition 2: Pre-conscious (moderate integration, sparse recurrence, moderate D)
    conditions.append(run_condition(
        name='Pre-Conscious',
        N=N,
        K=0.5,  # Moderate coupling
        omega_std=0.5,  # Moderate frequency spread
        recurrence_type='sparse',  # Sparse recurrence
        duration=duration,
        dt=dt
    ))
    
    # Condition 3: Conscious (critical coupling, hierarchical recurrence, high D)
    conditions.append(run_condition(
        name='Conscious',
        N=N,
        K=1.0,  # Critical coupling (Kuramoto transition ~1.0)
        omega_std=1.0,  # Broad frequency distribution
        recurrence_type='hierarchical',  # Hierarchical recurrence
        duration=duration,
        dt=dt
    ))
    
    # Condition 4: Over-synchronized (very high coupling, recurrence, but D collapses)
    conditions.append(run_condition(
        name='Over-Synchronized',
        N=N,
        K=3.0,  # Very strong coupling
        omega_std=0.2,  # Narrow (synchrony locks frequencies)
        recurrence_type='hierarchical',  # Recurrence present
        duration=duration,
        dt=dt
    ))
    
    print("\n" + "="*70)
    print("VALIDATION RESULTS")
    print("="*70)
    
    # Summary table
    print(f"\n{'Condition':<20} {'Phi':<10} {'R':<10} {'D':<10} {'C':<10}")
    print("-" * 60)
    for cond in conditions:
        print(f"{cond['name']:<20} {cond['Phi']:<10.3f} {cond['R']:<10.3f} {cond['D']:<10.3f} {cond['C']:<10.3f}")
    
    # Check ordering
    print("\n" + "="*70)
    print("VALIDATION CHECKS")
    print("="*70)
    
    C_values = {cond['name']: cond['C'] for cond in conditions}
    
    # Expected ordering: Conscious > Pre-conscious > Unconscious
    check1 = C_values['Conscious'] > C_values['Pre-Conscious'] > C_values['Unconscious']
    print(f"[{'PASS' if check1 else 'FAIL'}] C ordering: Conscious > Pre-Conscious > Unconscious")
    
    # Expected: Over-synchronized lower than Conscious (non-monotonic)
    check2 = C_values['Over-Synchronized'] < C_values['Conscious']
    print(f"[{'PASS' if check2 else 'FAIL'}] Over-synchronization shows C decrease")
    
    # Expected: Conscious crosses threshold
    check3 = C_values['Conscious'] > 8.3 and C_values['Unconscious'] < 8.3
    print(f"[{'PASS' if check3 else 'FAIL'}] Conscious crosses C_critical = 8.3 bits")
    
    overall = check1 and check2
    print(f"\n{'='*70}")
    print(f"OVERALL: [{'PASS' if overall else 'FAIL'}]")
    print(f"{'='*70}")
    
    # Save results
    import pickle
    with open('D:/Research/HIRM/Empirical/Simulation/simulation_results.pkl', 'wb') as f:
        pickle.dump(conditions, f)
    print("\n[OK] Results saved to simulation_results.pkl")
