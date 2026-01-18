"""
Neural Network Simulator for Ouroboros Observer Framework

Implements biologically-realistic neural dynamics with adjustable connectivity,
leaky integrate-and-fire neurons, and synaptic plasticity.
"""

import numpy as np
from typing import Optional, Tuple, Dict, Callable
from dataclasses import dataclass


@dataclass
class NeuronParams:
    """Parameters for leaky integrate-and-fire neurons."""
    tau_m: float = 20.0  # Membrane time constant (ms)
    V_rest: float = -70.0  # Resting potential (mV)
    V_reset: float = -70.0  # Reset potential (mV)
    V_threshold: float = -50.0  # Spike threshold (mV)
    R_m: float = 10.0  # Membrane resistance (MÎ©)
    t_refrac: float = 2.0  # Refractory period (ms)


@dataclass
class SynapseParams:
    """Parameters for synaptic dynamics."""
    tau_syn: float = 5.0  # Synaptic time constant (ms)
    J_exc: float = 0.1  # Excitatory synaptic strength (mV)
    J_inh: float = -0.5  # Inhibitory synaptic strength (mV)
    p_exc: float = 0.8  # Fraction of excitatory neurons


class NeuralNetwork:
    """
    Simulate neural network dynamics with biologically-realistic properties.
    
    Features:
    - Leaky integrate-and-fire neurons
    - Sparse connectivity (scale-free, small-world, or custom)
    - Excitatory and inhibitory neurons
    - Synaptic dynamics with exponential decay
    - External input and perturbations
    
    Parameters
    ----------
    N_neurons : int
        Number of neurons in the network
    connectivity_matrix : np.ndarray, optional
        NxN adjacency matrix. If None, generates scale-free network
    neuron_params : NeuronParams, optional
        Neuron model parameters
    synapse_params : SynapseParams, optional
        Synapse model parameters
    dt : float
        Time step for integration (ms)
    seed : int, optional
        Random seed for reproducibility
    """
    
    def __init__(
        self,
        N_neurons: int,
        connectivity_matrix: Optional[np.ndarray] = None,
        neuron_params: Optional[NeuronParams] = None,
        synapse_params: Optional[SynapseParams] = None,
        dt: float = 0.1,
        seed: Optional[int] = None
    ):
        self.N = N_neurons
        self.dt = dt
        
        # Set random seed
        if seed is not None:
            np.random.seed(seed)
        
        # Initialize parameters
        self.neuron_params = neuron_params or NeuronParams()
        self.synapse_params = synapse_params or SynapseParams()
        
        # Initialize connectivity
        if connectivity_matrix is not None:
            self.W = connectivity_matrix.copy()
        else:
            self.W = self._generate_scale_free_connectivity()
        
        # Assign excitatory/inhibitory types
        self.is_excitatory = np.random.rand(self.N) < self.synapse_params.p_exc
        
        # Apply synaptic strengths
        self._apply_synaptic_strengths()
        
        # Initialize state variables
        self.reset()
        
    def reset(self):
        """Reset network to initial state."""
        self.V = np.ones(self.N) * self.neuron_params.V_rest
        self.I_syn = np.zeros(self.N)
        self.t_last_spike = np.ones(self.N) * -np.inf
        self.spikes = np.zeros(self.N, dtype=bool)
        self.time = 0.0
        
        # History tracking
        self.spike_history = []
        self.V_history = []
        
    def _generate_scale_free_connectivity(self, k: int = 4) -> np.ndarray:
        """Generate scale-free network using preferential attachment."""
        W = np.zeros((self.N, self.N))
        
        # Start with small connected graph
        for i in range(k):
            for j in range(i+1, k):
                W[i, j] = 1
                W[j, i] = 1
        
        # Preferential attachment
        degrees = W.sum(axis=0)
        for i in range(k, self.N):
            # Probability proportional to degree
            probs = degrees / degrees.sum()
            targets = np.random.choice(i, size=min(k, i), replace=False, p=probs[:i]/probs[:i].sum())
            
            for j in targets:
                W[i, j] = 1
                W[j, i] = 1
                degrees[j] += 1
            degrees[i] = len(targets)
        
        return W
    
    def _apply_synaptic_strengths(self):
        """Apply excitatory/inhibitory synaptic weights."""
        for i in range(self.N):
            if self.is_excitatory[i]:
                self.W[i, :] *= self.synapse_params.J_exc
            else:
                self.W[i, :] *= self.synapse_params.J_inh
    
    def step(self, I_ext: Optional[np.ndarray] = None):
        """
        Advance simulation by one time step.
        
        Parameters
        ----------
        I_ext : np.ndarray, optional
            External input current to each neuron (nA)
        """
        if I_ext is None:
            I_ext = np.zeros(self.N)
        
        # Check refractory period
        in_refrac = (self.time - self.t_last_spike) < self.neuron_params.t_refrac
        
        # Synaptic current decay
        self.I_syn *= np.exp(-self.dt / self.synapse_params.tau_syn)
        
        # Add input from spikes in previous time step
        if self.spikes.any():
            self.I_syn += self.W.T @ self.spikes
        
        # Membrane potential dynamics (Euler integration)
        dV = (-(self.V - self.neuron_params.V_rest) + 
              self.neuron_params.R_m * (self.I_syn + I_ext)) / self.neuron_params.tau_m
        
        self.V[~in_refrac] += dV[~in_refrac] * self.dt
        
        # Check for spikes
        self.spikes = (self.V >= self.neuron_params.V_threshold) & ~in_refrac
        
        # Reset spiked neurons
        if self.spikes.any():
            self.V[self.spikes] = self.neuron_params.V_reset
            self.t_last_spike[self.spikes] = self.time
        
        # Update time
        self.time += self.dt
        
        # Store history
        self.spike_history.append(self.spikes.copy())
        self.V_history.append(self.V.copy())
    
    def run(self, duration: float, I_ext: Optional[np.ndarray] = None,
            I_ext_func: Optional[Callable[[float], np.ndarray]] = None) -> Dict:
        """
        Run simulation for specified duration.
        
        Parameters
        ----------
        duration : float
            Simulation duration (ms)
        I_ext : np.ndarray, optional
            Constant external input
        I_ext_func : callable, optional
            Time-dependent external input function I_ext(t)
        
        Returns
        -------
        dict
            Dictionary with 'spikes', 'V', and 'time' arrays
        """
        n_steps = int(duration / self.dt)
        
        for step in range(n_steps):
            if I_ext_func is not None:
                input_current = I_ext_func(self.time)
            else:
                input_current = I_ext
            
            self.step(input_current)
        
        return {
            'spikes': np.array(self.spike_history),
            'V': np.array(self.V_history),
            'time': np.arange(len(self.spike_history)) * self.dt
        }
    
    def get_activity(self) -> np.ndarray:
        """
        Get current activity pattern.
        
        Returns
        -------
        np.ndarray
            Binary spike pattern for current time step
        """
        return self.spikes.astype(float)
    
    def get_firing_rates(self, window: float = 100.0) -> np.ndarray:
        """
        Calculate firing rates over recent history.
        
        Parameters
        ----------
        window : float
            Time window for rate calculation (ms)
        
        Returns
        -------
        np.ndarray
            Firing rate for each neuron (Hz)
        """
        n_window = int(window / self.dt)
        if len(self.spike_history) < n_window:
            n_window = len(self.spike_history)
        
        recent_spikes = np.array(self.spike_history[-n_window:])
        spike_counts = recent_spikes.sum(axis=0)
        rates = spike_counts / (n_window * self.dt / 1000.0)  # Convert to Hz
        
        return rates
    
    def perturb(self, perturbation: np.ndarray, duration: float = 10.0):
        """
        Apply external perturbation (e.g., TMS-like pulse).
        
        Parameters
        ----------
        perturbation : np.ndarray
            Spatial pattern of perturbation strength
        duration : float
            Duration of perturbation (ms)
        """
        n_steps = int(duration / self.dt)
        for _ in range(n_steps):
            self.step(I_ext=perturbation)
    
    def tune_to_criticality(self, target_rate: float = 5.0, 
                           iterations: int = 100) -> float:
        """
        Adjust synaptic weights to achieve target firing rate (critical dynamics).
        
        Uses homeostatic plasticity to self-organize to critical regime.
        
        Parameters
        ----------
        target_rate : float
            Target mean firing rate (Hz)
        iterations : int
            Number of tuning iterations
        
        Returns
        -------
        float
            Final mean firing rate achieved
        """
        for _ in range(iterations):
            # Run short simulation
            self.run(duration=1000.0)
            
            # Measure current rates
            rates = self.get_firing_rates(window=1000.0)
            mean_rate = rates.mean()
            
            # Adjust weights
            if mean_rate > 0:
                scale_factor = target_rate / mean_rate
                scale_factor = np.clip(scale_factor, 0.9, 1.1)  # Limit adjustment
                self.W *= scale_factor
            
            # Reset for next iteration
            self.reset()
        
        # Final measurement
        self.run(duration=2000.0)
        final_rate = self.get_firing_rates(window=2000.0).mean()
        
        return final_rate


def generate_small_world(N: int, k: int = 6, p: float = 0.1, 
                         seed: Optional[int] = None) -> np.ndarray:
    """
    Generate Watts-Strogatz small-world network.
    
    Parameters
    ----------
    N : int
        Number of nodes
    k : int
        Each node connected to k nearest neighbors
    p : float
        Rewiring probability
    seed : int, optional
        Random seed
    
    Returns
    -------
    np.ndarray
        Adjacency matrix
    """
    if seed is not None:
        np.random.seed(seed)
    
    W = np.zeros((N, N))
    
    # Create ring lattice
    for i in range(N):
        for j in range(1, k//2 + 1):
            right = (i + j) % N
            left = (i - j) % N
            W[i, right] = 1
            W[i, left] = 1
    
    # Rewire with probability p
    for i in range(N):
        neighbors = np.where(W[i, :])[0]
        for j in neighbors:
            if np.random.rand() < p:
                # Rewire
                W[i, j] = 0
                # Find new target
                possible = np.setdiff1d(np.arange(N), np.concatenate([[i], np.where(W[i, :])[0]]))
                if len(possible) > 0:
                    new_target = np.random.choice(possible)
                    W[i, new_target] = 1
    
    return W


def generate_distance_dependent(N: int, positions: np.ndarray,
                                connection_func: Callable[[float], float],
                                seed: Optional[int] = None) -> np.ndarray:
    """
    Generate connectivity based on spatial distance.
    
    Parameters
    ----------
    N : int
        Number of neurons
    positions : np.ndarray
        Nx2 or Nx3 array of neuron positions
    connection_func : callable
        Function P(d) giving connection probability vs distance
    seed : int, optional
        Random seed
    
    Returns
    -------
    np.ndarray
        Adjacency matrix
    """
    if seed is not None:
        np.random.seed(seed)
    
    W = np.zeros((N, N))
    
    for i in range(N):
        for j in range(i+1, N):
            dist = np.linalg.norm(positions[i] - positions[j])
            prob = connection_func(dist)
            
            if np.random.rand() < prob:
                W[i, j] = 1
                W[j, i] = 1
    
    return W
