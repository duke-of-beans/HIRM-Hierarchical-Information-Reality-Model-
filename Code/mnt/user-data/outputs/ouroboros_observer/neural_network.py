"""
Neural Network Simulator
========================

Simulates neural dynamics with adjustable connectivity patterns and neuron models.
Supports leaky integrate-and-fire neurons, various network topologies, and 
real-time activity monitoring.
"""

import numpy as np
from typing import Optional, Tuple, Dict, Union
from dataclasses import dataclass
import networkx as nx
from scipy.sparse import csr_matrix


@dataclass
class NeuronParameters:
    """Parameters for leaky integrate-and-fire neurons."""
    tau_m: float = 20.0  # Membrane time constant (ms)
    V_rest: float = -70.0  # Resting potential (mV)
    V_threshold: float = -55.0  # Spike threshold (mV)
    V_reset: float = -75.0  # Reset potential (mV)
    tau_ref: float = 2.0  # Refractory period (ms)
    R_m: float = 10.0  # Membrane resistance (MOhm)


class NeuralNetwork:
    """
    Simulate neural dynamics with various connectivity patterns.
    
    Parameters
    ----------
    N_neurons : int
        Number of neurons in the network
    connectivity_matrix : np.ndarray or csr_matrix
        Synaptic connectivity weights (N x N)
    neuron_params : NeuronParameters, optional
        Parameters for neuron dynamics
    dt : float, optional
        Time step for integration (ms), default=0.1
    
    Attributes
    ----------
    V : np.ndarray
        Membrane potentials
    spikes : np.ndarray
        Binary spike indicators for current timestep
    spike_history : list
        History of spike times and neuron indices
    """
    
    def __init__(
        self,
        N_neurons: int,
        connectivity_matrix: Union[np.ndarray, csr_matrix],
        neuron_params: Optional[NeuronParameters] = None,
        dt: float = 0.1
    ):
        self.N = N_neurons
        self.W = connectivity_matrix
        self.dt = dt
        self.params = neuron_params or NeuronParameters()
        
        # State variables
        self.V = np.ones(N_neurons) * self.params.V_rest
        self.I_syn = np.zeros(N_neurons)  # Synaptic currents
        self.ref_time = np.zeros(N_neurons)  # Refractory period counter
        self.spikes = np.zeros(N_neurons, dtype=bool)
        
        # History tracking
        self.spike_history = []
        self.V_history = []
        self.time = 0.0
        
        # External input
        self.I_ext = np.zeros(N_neurons)
    
    def step(self, I_external: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Execute one time step of neural dynamics.
        
        Parameters
        ----------
        I_external : np.ndarray, optional
            External input currents to neurons
        
        Returns
        -------
        spikes : np.ndarray
            Binary array indicating which neurons spiked
        """
        if I_external is not None:
            self.I_ext = I_external
        
        # Synaptic current from previous spikes
        if hasattr(self.W, 'dot'):  # Sparse matrix
            self.I_syn = self.W.dot(self.spikes.astype(float))
        else:
            self.I_syn = np.dot(self.W, self.spikes.astype(float))
        
        # Update membrane potential (Euler integration)
        dV = (-(self.V - self.params.V_rest) + 
              self.params.R_m * (self.I_syn + self.I_ext)) / self.params.tau_m
        
        # Only update neurons not in refractory period
        active = self.ref_time <= 0
        self.V[active] += dV[active] * self.dt
        
        # Detect spikes
        self.spikes = (self.V >= self.params.V_threshold) & active
        
        # Reset spiking neurons
        self.V[self.spikes] = self.params.V_reset
        self.ref_time[self.spikes] = self.params.tau_ref
        
        # Decrease refractory counters
        self.ref_time -= self.dt
        
        # Record spikes
        spike_indices = np.where(self.spikes)[0]
        for idx in spike_indices:
            self.spike_history.append((self.time, idx))
        
        self.time += self.dt
        
        return self.spikes.copy()
    
    def run(
        self, 
        duration: float, 
        I_external: Optional[np.ndarray] = None,
        record_V: bool = False
    ) -> Dict[str, np.ndarray]:
        """
        Run simulation for specified duration.
        
        Parameters
        ----------
        duration : float
            Simulation duration (ms)
        I_external : np.ndarray, optional
            External input currents (N x T) or (N,) for constant input
        record_V : bool, optional
            Whether to record membrane potentials
        
        Returns
        -------
        results : dict
            Dictionary containing spike times, rates, and optionally V traces
        """
        n_steps = int(duration / self.dt)
        spike_raster = np.zeros((self.N, n_steps), dtype=bool)
        
        if record_V:
            self.V_history = np.zeros((self.N, n_steps))
        
        # Prepare external input
        if I_external is not None:
            if I_external.ndim == 1:
                I_ext = np.tile(I_external[:, np.newaxis], (1, n_steps))
            else:
                I_ext = I_external
        else:
            I_ext = np.zeros((self.N, n_steps))
        
        # Run simulation
        for t in range(n_steps):
            spikes = self.step(I_ext[:, t])
            spike_raster[:, t] = spikes
            
            if record_V:
                self.V_history[:, t] = self.V
        
        # Calculate firing rates
        firing_rates = spike_raster.sum(axis=1) / (duration / 1000.0)  # Hz
        
        results = {
            'spike_raster': spike_raster,
            'spike_times': np.array(self.spike_history),
            'firing_rates': firing_rates,
            'time': self.time
        }
        
        if record_V:
            results['V_traces'] = self.V_history
        
        return results
    
    def get_activity(self) -> Dict[str, np.ndarray]:
        """
        Return current network activity state.
        
        Returns
        -------
        activity : dict
            Dictionary with membrane potentials, spikes, and synaptic currents
        """
        return {
            'V': self.V.copy(),
            'spikes': self.spikes.copy(),
            'I_syn': self.I_syn.copy(),
            'time': self.time
        }
    
    def perturb(self, perturbation: np.ndarray, duration: float = 10.0):
        """
        Apply external perturbation to network.
        
        Parameters
        ----------
        perturbation : np.ndarray
            External currents (N,) or (N x T)
        duration : float, optional
            Duration of perturbation (ms)
        """
        if perturbation.ndim == 1:
            self.I_ext = perturbation
        else:
            # Multi-timestep perturbation
            self.run(duration, I_external=perturbation)
    
    def reset(self):
        """Reset network to initial conditions."""
        self.V = np.ones(self.N) * self.params.V_rest
        self.I_syn = np.zeros(self.N)
        self.ref_time = np.zeros(self.N)
        self.spikes = np.zeros(self.N, dtype=bool)
        self.spike_history = []
        self.V_history = []
        self.time = 0.0


class NetworkGenerator:
    """
    Generate various network connectivity patterns.
    
    Methods
    -------
    scale_free : Generate Barabási-Albert scale-free network
    small_world : Generate Watts-Strogatz small-world network
    random : Generate Erdős-Rényi random network
    biological_realistic : Generate distance-dependent connectivity
    """
    
    @staticmethod
    def scale_free(
        N: int, 
        m: int = 3, 
        weight_scale: float = 1.0,
        excitatory_fraction: float = 0.8
    ) -> csr_matrix:
        """
        Generate Barabási-Albert scale-free network.
        
        Parameters
        ----------
        N : int
            Number of neurons
        m : int
            Number of edges to attach from new node
        weight_scale : float
            Scale factor for synaptic weights
        excitatory_fraction : float
            Fraction of excitatory neurons
        
        Returns
        -------
        W : csr_matrix
            Connectivity matrix
        """
        G = nx.barabasi_albert_graph(N, m)
        W = nx.to_scipy_sparse_array(G, dtype=float)
        
        # Assign weights
        W = W * weight_scale
        
        # Assign excitatory/inhibitory
        n_exc = int(N * excitatory_fraction)
        W_data = W.data.copy()
        
        # Make random connections inhibitory
        inhibitory_mask = np.random.rand(len(W_data)) > excitatory_fraction
        W_data[inhibitory_mask] *= -1
        
        W.data = W_data
        return W
    
    @staticmethod
    def small_world(
        N: int, 
        k: int = 6, 
        p: float = 0.1,
        weight_scale: float = 1.0,
        excitatory_fraction: float = 0.8
    ) -> csr_matrix:
        """
        Generate Watts-Strogatz small-world network.
        
        Parameters
        ----------
        N : int
            Number of neurons
        k : int
            Each node connected to k nearest neighbors
        p : float
            Probability of rewiring each edge
        weight_scale : float
            Scale factor for synaptic weights
        excitatory_fraction : float
            Fraction of excitatory neurons
        
        Returns
        -------
        W : csr_matrix
            Connectivity matrix
        """
        G = nx.watts_strogatz_graph(N, k, p)
        W = nx.to_scipy_sparse_array(G, dtype=float)
        
        # Assign weights
        W = W * weight_scale
        
        # Assign excitatory/inhibitory
        W_data = W.data.copy()
        inhibitory_mask = np.random.rand(len(W_data)) > excitatory_fraction
        W_data[inhibitory_mask] *= -1
        
        W.data = W_data
        return W
    
    @staticmethod
    def random(
        N: int, 
        p: float = 0.1,
        weight_scale: float = 1.0,
        excitatory_fraction: float = 0.8
    ) -> csr_matrix:
        """
        Generate Erdős-Rényi random network.
        
        Parameters
        ----------
        N : int
            Number of neurons
        p : float
            Probability of edge creation
        weight_scale : float
            Scale factor for synaptic weights
        excitatory_fraction : float
            Fraction of excitatory neurons
        
        Returns
        -------
        W : csr_matrix
            Connectivity matrix
        """
        G = nx.erdos_renyi_graph(N, p)
        W = nx.to_scipy_sparse_array(G, dtype=float)
        
        # Assign weights
        W = W * weight_scale
        
        # Assign excitatory/inhibitory
        W_data = W.data.copy()
        inhibitory_mask = np.random.rand(len(W_data)) > excitatory_fraction
        W_data[inhibitory_mask] *= -1
        
        W.data = W_data
        return W
    
    @staticmethod
    def biological_realistic(
        N: int,
        grid_size: Optional[Tuple[int, int]] = None,
        connection_prob_func: Optional[callable] = None,
        weight_scale: float = 1.0,
        excitatory_fraction: float = 0.8
    ) -> csr_matrix:
        """
        Generate distance-dependent connectivity like cortex.
        
        Parameters
        ----------
        N : int
            Number of neurons
        grid_size : tuple, optional
            2D grid dimensions, default=(int(sqrt(N)), int(sqrt(N)))
        connection_prob_func : callable, optional
            Function f(distance) -> probability
        weight_scale : float
            Scale factor for synaptic weights
        excitatory_fraction : float
            Fraction of excitatory neurons
        
        Returns
        -------
        W : csr_matrix
            Connectivity matrix
        """
        if grid_size is None:
            side = int(np.sqrt(N))
            grid_size = (side, side)
            N = side * side  # Adjust N to perfect square
        
        if connection_prob_func is None:
            # Default: exponentially decaying probability
            lambda_decay = 10.0  # decay length
            connection_prob_func = lambda d: np.exp(-d / lambda_decay)
        
        # Place neurons on 2D grid
        positions = np.array([(i % grid_size[0], i // grid_size[0]) 
                             for i in range(N)])
        
        # Calculate pairwise distances
        diff = positions[:, np.newaxis, :] - positions[np.newaxis, :, :]
        distances = np.sqrt((diff ** 2).sum(axis=2))
        
        # Connection probabilities
        prob_matrix = connection_prob_func(distances)
        np.fill_diagonal(prob_matrix, 0)  # No self-connections
        
        # Generate connections
        connections = np.random.rand(N, N) < prob_matrix
        W = csr_matrix(connections.astype(float) * weight_scale)
        
        # Assign excitatory/inhibitory
        W_data = W.data.copy()
        inhibitory_mask = np.random.rand(len(W_data)) > excitatory_fraction
        W_data[inhibitory_mask] *= -1
        
        W.data = W_data
        return W
    
    @staticmethod
    def tune_to_criticality(
        W: csr_matrix, 
        target_branching: float = 1.0,
        n_iterations: int = 100
    ) -> csr_matrix:
        """
        Adjust synaptic weights to achieve critical dynamics.
        
        Uses homeostatic plasticity to self-organize to branching 
        parameter σ ≈ 1.0.
        
        Parameters
        ----------
        W : csr_matrix
            Initial connectivity matrix
        target_branching : float
            Target branching parameter
        n_iterations : int
            Number of tuning iterations
        
        Returns
        -------
        W_tuned : csr_matrix
            Tuned connectivity matrix
        """
        W_tuned = W.copy()
        
        # Estimate spectral radius (approximation of branching parameter)
        # For computational efficiency, use power iteration
        N = W.shape[0]
        v = np.random.rand(N)
        v = v / np.linalg.norm(v)
        
        for _ in range(20):  # Power iteration
            v_new = W_tuned.dot(v)
            eigenvalue = np.linalg.norm(v_new)
            if eigenvalue > 0:
                v = v_new / eigenvalue
        
        # Scale weights to achieve target branching
        scale_factor = target_branching / eigenvalue
        W_tuned = W_tuned * scale_factor
        
        return W_tuned
