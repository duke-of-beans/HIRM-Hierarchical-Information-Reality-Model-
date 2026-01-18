"""
Tests for consciousness_measure module
"""

import pytest
import numpy as np
from scipy.sparse import csr_matrix

from hirm.Core.consciousness_measure import (
    ConsciousnessMeasure, calculate_avalanche_exponents
)
from hirm.Core.neural_network import NetworkGenerator


class TestConsciousnessMeasure:
    """Test ConsciousnessMeasure class."""
    
    def setup_method(self):
        """Setup for each test."""
        self.measure = ConsciousnessMeasure()
        self.N = 50
        self.W = NetworkGenerator.random(self.N, p=0.1)
        self.activity = np.random.rand(self.N, 100)
    
    def test_initialization(self):
        """Test measure initialization."""
        assert self.measure.lambda_param == 2.0
        assert self.measure.Phi_method == 'geometric'
    
    def test_calculate_C(self):
        """Test full C(t) calculation."""
        result = self.measure.calculate_C(
            self.activity[:, 0],
            self.W,
            self.activity
        )
        
        assert 'C' in result
        assert 'Phi' in result
        assert 'R' in result
        assert 'D' in result
        
        # Check ranges
        assert result['C'] >= 0
        assert result['Phi'] >= 0
        assert result['R'] >= 1.0
        assert result['D'] >= 0
    
    def test_calculate_Phi_geometric(self):
        """Test geometric Phi approximation."""
        Phi = self.measure.calculate_Phi(
            self.activity[:, 0],
            self.W,
            method='geometric'
        )
        
        assert isinstance(Phi, float)
        assert Phi >= 0
    
    def test_calculate_Phi_PSI(self):
        """Test PSI approximation."""
        Phi = self.measure.calculate_Phi(
            self.activity[:, 0],
            self.W,
            method='PSI'
        )
        
        assert isinstance(Phi, float)
        assert Phi >= 0
    
    def test_calculate_R(self):
        """Test recursive depth calculation."""
        R = self.measure.calculate_R(self.activity)
        
        assert isinstance(R, float)
        assert R >= 1.0
        assert R <= 3.0
    
    def test_calculate_D(self):
        """Test distance from criticality."""
        D = self.measure.calculate_D(self.activity[:, 0], self.W)
        
        assert isinstance(D, float)
        assert D >= 0
    
    def test_C_components(self):
        """Test that C components multiply correctly."""
        result = self.measure.calculate_C(
            self.activity[:, 0],
            self.W,
            self.activity
        )
        
        Phi = result['Phi']
        R = result['R']
        D = result['D']
        C = result['C']
        
        # Verify formula
        expected_C = Phi * R * (1 - np.exp(-self.measure.lambda_param * D))
        assert np.isclose(C, expected_C, rtol=1e-5)


def test_calculate_avalanche_exponents():
    """Test avalanche statistics calculation."""
    # Create synthetic avalanche data
    N = 100
    T = 1000
    activity = np.zeros((N, T), dtype=bool)
    
    # Add some avalanches
    for _ in range(10):
        start = np.random.randint(0, T-50)
        duration = np.random.randint(5, 20)
        size = np.random.randint(10, 30)
        
        for t in range(start, min(start + duration, T)):
            active_neurons = np.random.choice(N, size=min(size, N), replace=False)
            activity[active_neurons, t] = True
    
    exponents = calculate_avalanche_exponents(activity)
    
    assert 'size_exponent' in exponents
    assert 'duration_exponent' in exponents
    assert 'n_avalanches' in exponents


def test_C_increases_with_integration():
    """Test that C increases with network integration."""
    measure = ConsciousnessMeasure()
    N = 50
    
    # Create activities with different integration levels
    C_values = []
    
    for integration in [0.3, 0.5, 0.7]:
        # Weakly vs strongly integrated
        activity = np.random.rand(N, 100)
        
        # Add correlations
        for t in range(100):
            activity[:, t] = (1-integration) * activity[:, t] + \
                           integration * activity[:, t].mean()
        
        W = NetworkGenerator.random(N, p=0.2)
        result = measure.calculate_C(activity[:, 0], W, activity)
        C_values.append(result['C'])
    
    # C should generally increase with integration
    # (though stochastic, so not strict monotonic)
    assert C_values[-1] > C_values[0]


def test_different_Phi_methods():
    """Test that different Phi methods give reasonable results."""
    measure = ConsciousnessMeasure()
    N = 50
    W = NetworkGenerator.random(N, p=0.1)
    activity = np.random.rand(N)
    
    Phi_geometric = measure.calculate_Phi(activity, W, method='geometric')
    Phi_PSI = measure.calculate_Phi(activity, W, method='PSI')
    
    # Both should be non-negative
    assert Phi_geometric >= 0
    assert Phi_PSI >= 0
    
    # Should be in reasonable range
    assert Phi_geometric < 20
    assert Phi_PSI < 20


def test_R_increases_with_recursion():
    """Test that R increases with recursive patterns."""
    measure = ConsciousnessMeasure()
    N = 50
    
    # Activity without recursion
    activity_simple = np.random.rand(N, 100)
    R_simple = measure.calculate_R(activity_simple)
    
    # Activity with recursive patterns
    activity_recursive = np.random.rand(N, 100)
    for delay in [10, 20]:
        activity_recursive[:, delay:] += 0.3 * activity_recursive[:, :-delay]
    
    R_recursive = measure.calculate_R(activity_recursive)
    
    # Recursive should have higher R
    assert R_recursive >= R_simple


def test_D_near_zero_at_criticality():
    """Test that D is near zero for critical networks."""
    measure = ConsciousnessMeasure()
    N = 50
    
    # Create critical network
    W = NetworkGenerator.random(N, p=0.1)
    W = NetworkGenerator.tune_to_criticality(W, target_branching=1.0)
    
    activity = np.random.rand(N)
    D = measure.calculate_D(activity, W)
    
    # D should be small for critical network
    assert D < 0.5


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
