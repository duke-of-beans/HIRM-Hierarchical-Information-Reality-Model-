"""
Visualization Tools for Ouroboros Observer

Publication-quality plots for C(t) dynamics, phase transitions,
network activity, and bifurcation diagrams.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import Optional, Tuple, Dict, List
import seaborn as sns

# Set publication style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['legend.fontsize'] = 9


def plot_C_timeseries(C_t: np.ndarray,
                      time: Optional[np.ndarray] = None,
                      critical_threshold: float = 8.3,
                      transitions: Optional[List] = None,
                      title: str = "Consciousness Measure C(t)",
                      figsize: Tuple[float, float] = (10, 4)):
    """
    Plot C(t) time series with critical threshold.
    
    Parameters
    ----------
    C_t : np.ndarray
        Time series of C(t) values
    time : np.ndarray, optional
        Time points
    critical_threshold : float
        Critical threshold line
    transitions : list, optional
        List of TransitionEvent objects to mark
    title : str
        Plot title
    figsize : tuple
        Figure size
    
    Returns
    -------
    fig, ax
        Matplotlib figure and axes
    """
    if time is None:
        time = np.arange(len(C_t))
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot C(t)
    ax.plot(time, C_t, 'b-', linewidth=1.5, label='C(t)')
    
    # Critical threshold
    ax.axhline(critical_threshold, color='r', linestyle='--', 
               linewidth=2, label=f'$C_{{critical}}$ = {critical_threshold} bits')
    
    # Mark transitions
    if transitions:
        for trans in transitions:
            ax.axvline(trans.time, color='orange', linestyle=':', alpha=0.7)
            ax.plot(trans.time, trans.C_after, 'ro', markersize=8)
    
    ax.set_xlabel('Time')
    ax.set_ylabel('C(t) [bits]')
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig, ax


def plot_phase_space(Phi_t: np.ndarray,
                    R_t: np.ndarray,
                    D_t: np.ndarray,
                    C_t: Optional[np.ndarray] = None,
                    figsize: Tuple[float, float] = (10, 8)):
    """
    Plot 3D phase space trajectory (Phi, R, D).
    
    Parameters
    ----------
    Phi_t : np.ndarray
        Integrated information time series
    R_t : np.ndarray
        Recursive depth time series
    D_t : np.ndarray
        Criticality distance time series
    C_t : np.ndarray, optional
        C(t) for color coding
    figsize : tuple
        Figure size
    
    Returns
    -------
    fig, ax
        Matplotlib figure and 3D axes
    """
    from mpl_toolkits.mplot3d import Axes3D
    
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    
    # Color by C(t) if available
    if C_t is not None:
        scatter = ax.scatter(Phi_t, R_t, D_t, c=C_t, 
                           cmap='viridis', s=20, alpha=0.6)
        cbar = plt.colorbar(scatter, ax=ax, label='C(t) [bits]')
    else:
        ax.plot(Phi_t, R_t, D_t, 'b-', alpha=0.6, linewidth=0.5)
        ax.scatter(Phi_t, R_t, D_t, c=np.arange(len(Phi_t)),
                  cmap='viridis', s=20, alpha=0.6)
    
    ax.set_xlabel('$\Phi$ (Integrated Information)')
    ax.set_ylabel('R (Recursive Depth)')
    ax.set_zlabel('D (Criticality)')
    ax.set_title('Phase Space Trajectory')
    
    plt.tight_layout()
    return fig, ax


def plot_bifurcation_diagram(parameter_values: np.ndarray,
                            C_values: List[np.ndarray],
                            parameter_name: str = "Control Parameter",
                            figsize: Tuple[float, float] = (10, 6)):
    """
    Plot bifurcation diagram showing C(t) vs parameter.
    
    Parameters
    ----------
    parameter_values : np.ndarray
        Parameter values swept
    C_values : list of np.ndarray
        C(t) values at each parameter (multiple points per parameter)
    parameter_name : str
        Name of control parameter
    figsize : tuple
        Figure size
    
    Returns
    -------
    fig, ax
        Matplotlib figure and axes
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot all C values for each parameter
    for i, param in enumerate(parameter_values):
        C_points = C_values[i]
        ax.plot([param] * len(C_points), C_points, 'k.', 
                markersize=1, alpha=0.3)
    
    ax.set_xlabel(parameter_name)
    ax.set_ylabel('C(t) [bits]')
    ax.set_title('Bifurcation Diagram')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig, ax


def plot_network_activity(activity: np.ndarray,
                         connectivity: Optional[np.ndarray] = None,
                         time_range: Optional[Tuple[int, int]] = None,
                         figsize: Tuple[float, float] = (12, 6)):
    """
    Plot raster plot of network activity with optional connectivity.
    
    Parameters
    ----------
    activity : np.ndarray
        T x N array of activity patterns
    connectivity : np.ndarray, optional
        N x N connectivity matrix
    time_range : tuple, optional
        (start, end) time indices to plot
    figsize : tuple
        Figure size
    
    Returns
    -------
    fig, axes
        Matplotlib figure and axes
    """
    if time_range is not None:
        activity = activity[time_range[0]:time_range[1]]
    
    if connectivity is not None:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    else:
        fig, ax1 = plt.subplots(figsize=(figsize[0]//2, figsize[1]))
    
    # Raster plot
    spike_times, spike_neurons = np.where(activity > 0)
    ax1.scatter(spike_times, spike_neurons, s=1, c='k', alpha=0.5)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Neuron Index')
    ax1.set_title('Network Activity (Raster Plot)')
    ax1.set_ylim(-0.5, activity.shape[1] - 0.5)
    
    # Connectivity matrix
    if connectivity is not None:
        im = ax2.imshow(connectivity, cmap='RdBu_r', aspect='auto')
        ax2.set_xlabel('Neuron (pre)')
        ax2.set_ylabel('Neuron (post)')
        ax2.set_title('Connectivity Matrix')
        plt.colorbar(im, ax=ax2, label='Weight')
    
    plt.tight_layout()
    return fig, (ax1, ax2) if connectivity is not None else (fig, ax1)


def plot_components(Phi_t: np.ndarray,
                   R_t: np.ndarray,
                   D_t: np.ndarray,
                   C_t: np.ndarray,
                   time: Optional[np.ndarray] = None,
                   figsize: Tuple[float, float] = (12, 8)):
    """
    Plot all C(t) components in subplots.
    
    Parameters
    ----------
    Phi_t, R_t, D_t, C_t : np.ndarray
        Component time series
    time : np.ndarray, optional
        Time points
    figsize : tuple
        Figure size
    
    Returns
    -------
    fig, axes
        Matplotlib figure and axes
    """
    if time is None:
        time = np.arange(len(C_t))
    
    fig, axes = plt.subplots(4, 1, figsize=figsize, sharex=True)
    
    axes[0].plot(time, Phi_t, 'b-', linewidth=1.5)
    axes[0].set_ylabel('$\Phi$ [bits]')
    axes[0].set_title('Integrated Information')
    axes[0].grid(True, alpha=0.3)
    
    axes[1].plot(time, R_t, 'g-', linewidth=1.5)
    axes[1].set_ylabel('R')
    axes[1].set_title('Recursive Depth')
    axes[1].grid(True, alpha=0.3)
    
    axes[2].plot(time, D_t, 'orange', linewidth=1.5)
    axes[2].set_ylabel('D')
    axes[2].set_title('Criticality Proximity')
    axes[2].grid(True, alpha=0.3)
    
    axes[3].plot(time, C_t, 'r-', linewidth=2)
    axes[3].axhline(8.3, color='k', linestyle='--', alpha=0.5)
    axes[3].set_ylabel('C(t) [bits]')
    axes[3].set_xlabel('Time')
    axes[3].set_title('Consciousness Measure')
    axes[3].grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig, axes


def plot_avalanche_statistics(avalanche_sizes: np.ndarray,
                              avalanche_durations: np.ndarray,
                              figsize: Tuple[float, float] = (12, 5)):
    """
    Plot avalanche size and duration distributions.
    
    Parameters
    ----------
    avalanche_sizes : np.ndarray
        Array of avalanche sizes
    avalanche_durations : np.ndarray
        Array of avalanche durations
    figsize : tuple
        Figure size
    
    Returns
    -------
    fig, axes
        Matplotlib figure and axes
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    
    # Size distribution (log-log)
    sizes = avalanche_sizes[avalanche_sizes > 0]
    if len(sizes) > 0:
        hist, bins = np.histogram(np.log10(sizes), bins=20)
        bin_centers = (bins[:-1] + bins[1:]) / 2
        ax1.loglog(10**bin_centers, hist, 'bo-', alpha=0.6)
        ax1.set_xlabel('Avalanche Size')
        ax1.set_ylabel('Count')
        ax1.set_title('Avalanche Size Distribution')
        ax1.grid(True, alpha=0.3)
    
    # Duration distribution (log-log)
    durations = avalanche_durations[avalanche_durations > 0]
    if len(durations) > 0:
        hist, bins = np.histogram(np.log10(durations), bins=15)
        bin_centers = (bins[:-1] + bins[1:]) / 2
        ax2.loglog(10**bin_centers, hist, 'ro-', alpha=0.6)
        ax2.set_xlabel('Avalanche Duration')
        ax2.set_ylabel('Count')
        ax2.set_title('Avalanche Duration Distribution')
        ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig, (ax1, ax2)


def animate_network_dynamics(network_activity: np.ndarray,
                            C_values: np.ndarray,
                            interval: int = 50,
                            save_path: Optional[str] = None):
    """
    Create animation of network dynamics with C(t) tracking.
    
    Parameters
    ----------
    network_activity : np.ndarray
        T x N activity matrix
    C_values : np.ndarray
        C(t) values for each time step
    interval : int
        Milliseconds between frames
    save_path : str, optional
        Path to save animation (e.g., 'animation.mp4')
    
    Returns
    -------
    animation
        Matplotlib animation object
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Initialize plots
    N = network_activity.shape[1]
    im = ax1.imshow(network_activity[:1].T, aspect='auto', 
                    cmap='binary', interpolation='nearest')
    ax1.set_ylabel('Neuron')
    ax1.set_title('Network Activity')
    
    line, = ax2.plot([], [], 'b-', linewidth=2)
    threshold_line = ax2.axhline(8.3, color='r', linestyle='--', alpha=0.5)
    ax2.set_xlim(0, len(C_values))
    ax2.set_ylim(0, max(C_values.max(), 10))
    ax2.set_xlabel('Time')
    ax2.set_ylabel('C(t) [bits]')
    ax2.set_title('Consciousness Measure')
    ax2.grid(True, alpha=0.3)
    
    def update(frame):
        # Update activity
        window_size = min(50, frame + 1)
        start = max(0, frame - window_size + 1)
        im.set_array(network_activity[start:frame+1].T)
        ax1.set_xlim(start, frame + 1)
        
        # Update C(t)
        line.set_data(range(frame + 1), C_values[:frame + 1])
        
        return im, line
    
    anim = FuncAnimation(fig, update, frames=len(C_values),
                        interval=interval, blit=True)
    
    if save_path:
        anim.save(save_path, writer='ffmpeg', fps=20)
    
    return anim


def plot_parameter_sensitivity(parameter_name: str,
                              parameter_values: np.ndarray,
                              C_means: np.ndarray,
                              C_stds: np.ndarray,
                              figsize: Tuple[float, float] = (8, 5)):
    """
    Plot sensitivity of C_critical to parameter variation.
    
    Parameters
    ----------
    parameter_name : str
        Name of parameter
    parameter_values : np.ndarray
        Parameter values tested
    C_means : np.ndarray
        Mean C values at transition
    C_stds : np.ndarray
        Standard deviations
    figsize : tuple
        Figure size
    
    Returns
    -------
    fig, ax
        Matplotlib figure and axes
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.errorbar(parameter_values, C_means, yerr=C_stds,
                fmt='o-', capsize=5, linewidth=2)
    ax.axhline(8.3, color='r', linestyle='--', 
               label='$C_{critical}$ = 8.3 bits')
    
    ax.set_xlabel(parameter_name)
    ax.set_ylabel('$C_{critical}$ [bits]')
    ax.set_title(f'Sensitivity to {parameter_name}')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig, ax
