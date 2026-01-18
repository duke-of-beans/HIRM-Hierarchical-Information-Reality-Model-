"""
Information Geometry Toolkit for HIRM Consciousness Analysis
==============================================================

Computational tools for analyzing consciousness state space using:
- Fisher information metric estimation
- Geodesic computation and visualization
- Wasserstein distance evolution tracking
- Curvature and parallel transport
- Natural gradient dynamics

Author: HIRM Research Team
Date: October 26, 2025
Version: 1.0
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.stats import gaussian_kde
from scipy.spatial.distance import cdist
from scipy.optimize import minimize
from sklearn.manifold import MDS
from mpl_toolkits.mplot3d import Axes3D
import warnings

try:
    import ot  # Python Optimal Transport
    OT_AVAILABLE = True
except ImportError:
    warnings.warn("Python Optimal Transport (POT) not available. Install with: pip install POT")
    OT_AVAILABLE = False


# ==============================================================================
# 1. FISHER INFORMATION METRIC ESTIMATION
# ==============================================================================

class FisherMetricEstimator:
    """Estimate Fisher information metric from neural data."""
    
    def __init__(self, bandwidth='scott'):
        self.bandwidth = bandwidth
        
    def estimate_metric(self, neural_data, theta_samples, method='empirical'):
        """
        Estimate Fisher information metric g_ij.
        
        Parameters:
        -----------
        neural_data : array (n_samples, n_features)
            Neural observations
        theta_samples : array (n_samples, 3)
            Consciousness parameters (Î¦, R, D)
            
        Returns:
        --------
        g : array (3, 3)
            Fisher information metric
        """
        n_params = 3
        g = np.zeros((n_params, n_params))
        
        # Score function approach
        for i in range(n_params):
            score_i = self._compute_score(neural_data, theta_samples, i)
            for j in range(i, n_params):
                score_j = self._compute_score(neural_data, theta_samples, j)
                g[i, j] = np.mean(score_i * score_j)
                g[j, i] = g[i, j]
                
        return g
    
    def _compute_score(self, data, theta, param_idx, h=1e-5):
        """Numerical score function: âˆ‚_i log p(x|Î¸)"""
        n_samples = len(theta)
        scores = np.zeros(n_samples)
        
        kde = gaussian_kde(data.T, bw_method=self.bandwidth)
        
        for i in range(n_samples):
            theta_plus = theta[i].copy()
            theta_minus = theta[i].copy()
            theta_plus[param_idx] += h
            theta_minus[param_idx] -= h
            
            try:
                log_p_plus = kde.logpdf(data[i])
                log_p_minus = kde.logpdf(data[i])
                scores[i] = (log_p_plus - log_p_minus) / (2 * h)
            except:
                scores[i] = 0
        
        return scores


# ==============================================================================
# 2. GEODESIC COMPUTATION
# ==============================================================================

class GeodesicSolver:
    """Solve geodesic equations on consciousness manifold."""
    
    def __init__(self, metric_func):
        """
        Parameters:
        -----------
        metric_func : callable
            Function g(theta) returning metric tensor (3,3)
        """
        self.g = metric_func
        
    def compute_christoffel(self, theta, h=1e-5):
        """Compute Christoffel symbols numerically."""
        g = self.g(theta)
        g_inv = np.linalg.inv(g)
        
        # Metric derivatives
        dg = np.zeros((3, 3, 3))
        for j in range(3):
            theta_plus = theta.copy()
            theta_minus = theta.copy()
            theta_plus[j] += h
            theta_minus[j] -= h
            
            g_plus = self.g(theta_plus)
            g_minus = self.g(theta_minus)
            
            dg[j] = (g_plus - g_minus) / (2 * h)
        
        # Christoffel formula
        Gamma = np.zeros((3, 3, 3))
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        Gamma[i,j,k] += 0.5 * g_inv[i,l] * (
                            dg[k,l,j] + dg[j,l,k] - dg[l,j,k]
                        )
        
        return Gamma
    
    def solve_geodesic(self, theta_start, theta_end, n_points=100):
        """
        Compute geodesic connecting two consciousness states.
        
        Returns:
        --------
        geodesic : array (n_points, 3)
            Path through consciousness space
        """
        def geodesic_rhs(t, y):
            theta = y[:3]
            v = y[3:]
            
            Gamma = self.compute_christoffel(theta)
            accel = -np.einsum('ijk,j,k->i', Gamma, v, v)
            
            return np.concatenate([v, accel])
        
        # Initial velocity guess
        v0 = theta_end - theta_start
        y0 = np.concatenate([theta_start, v0])
        
        t_eval = np.linspace(0, 1, n_points)
        sol = solve_ivp(geodesic_rhs, [0, 1], y0, 
                       t_eval=t_eval, method='RK45')
        
        return sol.y[:3].T


# ==============================================================================
# 3. WASSERSTEIN DISTANCE TRACKING
# ==============================================================================

class WassersteinTracker:
    """Track consciousness evolution via Wasserstein distance."""
    
    def __init__(self, reg=0.1):
        if not OT_AVAILABLE:
            raise ImportError("POT required: pip install POT")
        self.reg = reg
    
    def wasserstein_distance(self, samples1, samples2):
        """
        Compute W2 distance between distributions.
        
        Parameters:
        -----------
        samples1, samples2 : array (n_samples, 3)
            Sample points in (Î¦, R, D) space
            
        Returns:
        --------
        W2 : float
            Wasserstein-2 distance
        """
        n1, n2 = len(samples1), len(samples2)
        weights1 = np.ones(n1) / n1
        weights2 = np.ones(n2) / n2
        
        M = cdist(samples1, samples2, metric='euclidean') ** 2
        W2_squared = ot.sinkhorn2(weights1, weights2, M, self.reg)
        
        return np.sqrt(W2_squared)
    
    def track_evolution(self, time_series, window_size=500, step=100):
        """
        Track consciousness distribution evolution.
        
        Returns:
        --------
        W_timeline : array
            Wasserstein distances between consecutive windows
        """
        n_windows = (len(time_series) - window_size) // step + 1
        W_timeline = []
        
        window_prev = time_series[:window_size]
        
        for i in range(1, n_windows):
            start = i * step
            window_curr = time_series[start:start + window_size]
            
            W = self.wasserstein_distance(window_prev, window_curr)
            W_timeline.append(W)
            
            window_prev = window_curr
        
        return np.array(W_timeline)


# ==============================================================================
# 4. VISUALIZATION TOOLS
# ==============================================================================

class ConsciousnessManifoldVisualizer:
    """Visualize consciousness state space geometry."""
    
    def __init__(self, geodesic_solver):
        self.geodesic_solver = geodesic_solver
    
    def plot_manifold_embedding(self, theta_samples, C_values, method='mds'):
        """
        Visualize consciousness manifold via dimensionality reduction.
        
        Parameters:
        -----------
        theta_samples : array (n_samples, 3)
            Consciousness states (Î¦, R, D)
        C_values : array (n_samples,)
            Consciousness measure C = Î¦Â·RÂ·D
        method : str
            'mds': Multidimensional scaling
            'geodesic': Use geodesic distances
        """
        n_samples = len(theta_samples)
        
        if method == 'geodesic':
            # Compute pairwise geodesic distances
            D = np.zeros((n_samples, n_samples))
            for i in range(n_samples):
                for j in range(i+1, n_samples):
                    geodesic = self.geodesic_solver.solve_geodesic(
                        theta_samples[i], theta_samples[j], n_points=20
                    )
                    D[i,j] = self._path_length(geodesic)
                    D[j,i] = D[i,j]
        else:
            # Euclidean distances
            D = cdist(theta_samples, theta_samples)
        
        # MDS embedding
        mds = MDS(n_components=3, dissimilarity='precomputed')
        embedding = mds.fit_transform(D)
        
        # 3D plot
        fig = plt.figure(figsize=(12, 9))
        ax = fig.add_subplot(111, projection='3d')
        
        scatter = ax.scatter(embedding[:,0], embedding[:,1], embedding[:,2],
                           c=C_values, cmap='viridis', s=50, alpha=0.7)
        
        ax.set_xlabel('Geodesic Coordinate 1')
        ax.set_ylabel('Geodesic Coordinate 2')
        ax.set_zlabel('Geodesic Coordinate 3')
        ax.set_title('Consciousness Manifold (Geodesic Distance Embedding)')
        
        plt.colorbar(scatter, label='C(t) [bits]')
        plt.tight_layout()
        return fig
    
    def _path_length(self, path):
        """Compute length of path."""
        length = 0
        for i in range(len(path)-1):
            length += np.linalg.norm(path[i+1] - path[i])
        return length
    
    def plot_geodesic_trajectory(self, theta_start, theta_end):
        """Plot geodesic between two states."""
        geodesic = self.geodesic_solver.solve_geodesic(
            theta_start, theta_end, n_points=100
        )
        
        fig = plt.figure(figsize=(12, 5))
        
        # 3D trajectory
        ax1 = fig.add_subplot(121, projection='3d')
        ax1.plot(geodesic[:,0], geodesic[:,1], geodesic[:,2], 
                'b-', linewidth=2, label='Geodesic')
        ax1.scatter(*theta_start, color='green', s=100, label='Start')
        ax1.scatter(*theta_end, color='red', s=100, label='End')
        ax1.set_xlabel('Î¦ [bits]')
        ax1.set_ylabel('R')
        ax1.set_zlabel('D')
        ax1.legend()
        
        # Time evolution
        ax2 = fig.add_subplot(122)
        t = np.linspace(0, 1, len(geodesic))
        ax2.plot(t, geodesic[:,0], label='Î¦(Î»)')
        ax2.plot(t, geodesic[:,1], label='R(Î»)')
        ax2.plot(t, geodesic[:,2], label='D(Î»)')
        ax2.set_xlabel('Path Parameter Î»')
        ax2.set_ylabel('Parameters')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        return fig


# ==============================================================================
# 5. EXAMPLE METRIC FUNCTIONS
# ==============================================================================

def hirm_critical_metric(theta, C_crit=8.3, alpha=1.0, nu=0.63, beta=0.1):
    """
    HIRM consciousness metric with critical behavior.
    
    g_ij = gâ°_ij + Î±|C - C_crit|^(-Î½) Î´_ij + Î² âˆ‚_i C âˆ‚_j C
    
    Parameters:
    -----------
    theta : array (3,)
        Consciousness state (Î¦, R, D)
    C_crit : float
        Critical threshold
    alpha, nu, beta : float
        Metric parameters
    """
    Phi, R, D = theta
    C = Phi * R * D
    
    # Background metric
    g0 = np.eye(3)
    
    # Critical divergence
    divergence = alpha * np.abs(C - C_crit)**(-nu)
    g_critical = divergence * np.eye(3)
    
    # C-gradient coupling
    grad_C = np.array([R*D, Phi*D, Phi*R])
    g_gradient = beta * np.outer(grad_C, grad_C)
    
    return g0 + g_critical + g_gradient


# ==============================================================================
# 6. COMPLETE ANALYSIS PIPELINE
# ==============================================================================

def analyze_consciousness_transition(neural_data, theta_timeline, 
                                    transition_type='anesthesia'):
    """
    Complete information-geometric analysis of consciousness transition.
    
    Parameters:
    -----------
    neural_data : array (n_timepoints, n_channels)
        Neural recordings
    theta_timeline : array (n_timepoints, 3)
        Consciousness parameters over time
    transition_type : str
        Type of transition being analyzed
        
    Returns:
    --------
    results : dict
        Comprehensive analysis results
    """
    results = {}
    
    print("=== Information Geometry Analysis ===\n")
    
    # 1. Fisher Information Evolution
    print("1. Computing Fisher information metric...")
    estimator = FisherMetricEstimator()
    
    # Sliding window analysis
    window_size = 1000
    I_F_timeline = []
    
    for i in range(0, len(neural_data) - window_size, 100):
        window_data = neural_data[i:i+window_size]
        window_theta = theta_timeline[i:i+window_size]
        
        g, _ = estimator.estimate_metric(window_data, window_theta)
        I_F = np.trace(g)
        I_F_timeline.append(I_F)
    
    results['fisher_information'] = np.array(I_F_timeline)
    
    # 2. Geodesic Analysis
    print("2. Computing geodesics...")
    metric_func = lambda theta: hirm_critical_metric(theta)
    solver = GeodesicSolver(metric_func)
    
    # Pre-transition to post-transition
    theta_pre = np.mean(theta_timeline[:window_size], axis=0)
    theta_post = np.mean(theta_timeline[-window_size:], axis=0)
    
    geodesic = solver.solve_geodesic(theta_pre, theta_post)
    results['geodesic'] = geodesic
    
    # 3. Wasserstein Distance Evolution
    print("3. Tracking Wasserstein distances...")
    if OT_AVAILABLE:
        tracker = WassersteinTracker()
        W_timeline = tracker.track_evolution(theta_timeline)
        results['wasserstein_timeline'] = W_timeline
    
    # 4. Visualization
    print("4. Generating visualizations...")
    visualizer = ConsciousnessManifoldVisualizer(solver)
    
    C_values = theta_timeline[:,0] * theta_timeline[:,1] * theta_timeline[:,2]
    
    # Sample for visualization (too many points slow down MDS)
    n_viz = min(200, len(theta_timeline))
    idx = np.linspace(0, len(theta_timeline)-1, n_viz, dtype=int)
    
    fig1 = visualizer.plot_manifold_embedding(
        theta_timeline[idx], C_values[idx]
    )
    results['manifold_plot'] = fig1
    
    fig2 = visualizer.plot_geodesic_trajectory(theta_pre, theta_post)
    results['geodesic_plot'] = fig2
    
    # 5. Critical Scaling Analysis
    print("5. Analyzing critical behavior...")
    if len(I_F_timeline) > 10:
        # Fit critical exponent
        C_timeline = C_values[::100][:len(I_F_timeline)]
        C_crit = 8.3
        
        distances = np.abs(C_timeline - C_crit)
        valid = distances > 0.5  # Avoid singularity
        
        if np.sum(valid) > 5:
            log_dist = np.log(distances[valid])
            log_IF = np.log(I_F_timeline[valid])
            
            gamma = -np.polyfit(log_dist, log_IF, 1)[0]
            results['critical_exponent'] = gamma
            
            print(f"   Estimated critical exponent Î³ = {gamma:.3f}")
    
    print("\nAnalysis complete!")
    return results


# ==============================================================================
# EXAMPLE USAGE
# ==============================================================================

if __name__ == "__main__":
    print("HIRM Information Geometry Toolkit - Example Usage\n")
    
    # Generate synthetic consciousness transition data
    np.random.seed(42)
    n_time = 5000
    t = np.linspace(0, 10, n_time)
    
    # Simulate anesthesia transition
    C_crit = 8.3
    Phi_t = 10 - 3 * (1 + np.tanh((t - 5) * 2))  # Decreasing
    R_t = 0.9 - 0.4 * (1 + np.tanh((t - 5) * 2))
    D_t = np.ones_like(t) * 3.0
    
    theta_timeline = np.column_stack([Phi_t, R_t, D_t])
    C_timeline = Phi_t * R_t * D_t
    
    # Synthetic neural data (simplified)
    neural_data = np.random.randn(n_time, 64)  # 64 "channels"
    
    # Add correlation with consciousness
    for i in range(64):
        neural_data[:,i] += 0.5 * C_timeline
    
    # Run analysis
    results = analyze_consciousness_transition(
        neural_data, theta_timeline, 'anesthesia'
    )
    
    # Plot Fisher information evolution
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1,2,1)
    plt.plot(C_timeline[::100][:len(results['fisher_information'])], 
             results['fisher_information'], 'b.-')
    plt.axvline(C_crit, color='r', linestyle='--', label='C_crit')
    plt.xlabel('C(t) [bits]')
    plt.ylabel('Fisher Information')
    plt.title('Fisher Information vs. Consciousness')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(1,2,2)
    if 'wasserstein_timeline' in results:
        plt.plot(results['wasserstein_timeline'], 'g.-')
        plt.xlabel('Time Window')
        plt.ylabel('Wasserstein Distance')
        plt.title('Consciousness Distribution Evolution')
        plt.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    print("\nâœ“ Example analysis complete!")
    print(f"âœ“ Results keys: {list(results.keys())}")
