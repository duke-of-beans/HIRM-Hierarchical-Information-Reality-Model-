"""
Tests for neural_network module
"""

import pytest
import numpy as np
from scipy.sparse import csr_matrix

from hirm.Core.neural_network import (
    NeuralNetwork, NetworkGenerator, NeuronParameters
)


class TestNeuralNetwork:
    """Test NeuralNetwork class."""
    
    def setup_method(self):
        """Setup for each test."""
        self.N = 50
        self.W = NetworkGenerator.random(self.N, p=0.1)
        self.network = NeuralNetwork(self.N, self.W)
    
    def test_initialization(self):
        """Test network initialization."""
        assert self.network.N == self.N
        assert self.network.V.shape == (self.N,)
        assert len(self.network.spike_history) == 0
    
    def test_step(self):
        """Test single time step."""
        spikes = self.network.step()
        assert spikes.shape == (self.N,)
        assert spikes.dtype == bool
    
    def test_run(self):
        """Test simulation run."""
        duration = 100  # ms
        results = self.network.run(duration)
        
        assert 'spike_raster' in results
        assert 'firing_rates' in results
        assert 'spike_times' in results
        
        n_steps = int(duration / self.network.dt)
        assert results['spike_raster'].shape == (self.N, n_steps)
    
    def test_external_input(self):
        """Test external input application."""
        I_ext = np.ones(self.N) * 10  # Strong input
        results = self.network.run(100, I_external=I_ext)
        
        # Should have some spikes with strong input
        assert results['spike_raster'].sum() > 0
    
    def test_reset(self):
        """Test network reset."""
        self.network.run(100)
        initial_time = self.network.time
        
        self.network.reset()
        assert self.network.time == 0
        assert len(self.network.spike_history) == 0


class TestNetworkGenerator:
    """Test NetworkGenerator class."""
    
    def test_scale_free(self):
        """Test scale-free network generation."""
        N = 100
        W = NetworkGenerator.scale_free(N, m=3)
        
        assert isinstance(W, csr_matrix)
        assert W.shape == (N, N)
        assert W.nnz > 0  # Has connections
    
    def test_small_world(self):
        """Test small-world network generation."""
        N = 100
        W = NetworkGenerator.small_world(N, k=6, p=0.1)
        
        assert isinstance(W, csr_matrix)
        assert W.shape == (N, N)
    
    def test_random(self):
        """Test random network generation."""
        N = 100
        W = NetworkGenerator.random(N, p=0.1)
        
        assert isinstance(W, csr_matrix)
        assert W.shape == (N, N)
    
    def test_biological_realistic(self):
        """Test biological-realistic network."""
        N = 64  # Perfect square
        W = NetworkGenerator.biological_realistic(N)
        
        assert isinstance(W, csr_matrix)
        assert W.shape == (N, N)
    
    def test_tune_to_criticality(self):
        """Test criticality tuning."""
        N = 100
        W = NetworkGenerator.random(N, p=0.1)
        
        W_tuned = NetworkGenerator.tune_to_criticality(W, target_branching=1.0)
        
        assert isinstance(W_tuned, csr_matrix)
        assert W_tuned.shape == W.shape
        
        # Should scale weights
        assert not np.allclose(W_tuned.data, W.data)


class TestNeuronParameters:
    """Test NeuronParameters dataclass."""
    
    def test_default_parameters(self):
        """Test default parameter values."""
        params = NeuronParameters()
        
        assert params.tau_m == 20.0
        assert params.V_threshold == -55.0
        assert params.V_rest == -70.0
    
    def test_custom_parameters(self):
        """Test custom parameter values."""
        params = NeuronParameters(tau_m=15.0, V_threshold=-50.0)
        
        assert params.tau_m == 15.0
        assert params.V_threshold == -50.0


def test_network_dynamics():
    """Test realistic network dynamics."""
    N = 100
    W = NetworkGenerator.scale_free(N, m=4)
    W = NetworkGenerator.tune_to_criticality(W)
    
    network = NeuralNetwork(N, W)
    
    # Run with external input
    I_ext = np.random.rand(N) * 5
    results = network.run(500, I_external=I_ext)
    
    # Check basic properties
    assert results['firing_rates'].mean() > 0  # Some activity
    assert results['firing_rates'].mean() < 100  # Not too high
    
    # Check spike counts
    n_spikes = results['spike_raster'].sum()
    assert n_spikes > 0


def test_activity_patterns():
    """Test that network produces varied activity patterns."""
    N = 50
    W = NetworkGenerator.random(N, p=0.2)
    network = NeuralNetwork(N, W)
    
    # Run multiple trials
    patterns = []
    for _ in range(5):
        network.reset()
        results = network.run(100)
        patterns.append(results['firing_rates'])
    
    patterns = np.array(patterns)
    
    # Patterns should vary across trials
    variance = np.var(patterns, axis=0).mean()
    assert variance > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
