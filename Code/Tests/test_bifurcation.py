"""
Tests for bifurcation_detector module
"""

import pytest
import numpy as np

from hirm.Core.bifurcation_detector import BifurcationDetector


class TestBifurcationDetector:
    """Test BifurcationDetector class."""
    
    def setup_method(self):
        """Setup for each test."""
        self.detector = BifurcationDetector(C_critical=8.3)
    
    def test_initialization(self):
        """Test detector initialization."""
        assert self.detector.C_critical == 8.3
        assert self.detector.current_state == "subcritical"
    
    def test_monitor_subcritical(self):
        """Test monitoring subcritical state."""
        C_series = np.ones(10) * 7.0
        status = self.detector.monitor(C_series)
        
        assert status['state'] == 'subcritical'
        assert not status['transition_detected']
    
    def test_monitor_supercritical(self):
        """Test monitoring supercritical state."""
        C_series = np.ones(10) * 9.0
        status = self.detector.monitor(C_series)
        
        assert status['state'] == 'supercritical'
    
    def test_detect_transition_up(self):
        """Test detecting upward transition."""
        # Create series with transition
        C_series = np.concatenate([
            np.ones(50) * 7.0,  # Subcritical
            np.ones(50) * 9.0   # Supercritical
        ])
        
        transitions = self.detector.detect_transition(C_series)
        
        assert transitions['n_up_transitions'] > 0
        assert len(transitions['up_transition_indices']) > 0
    
    def test_detect_transition_down(self):
        """Test detecting downward transition."""
        C_series = np.concatenate([
            np.ones(50) * 9.0,  # Supercritical
            np.ones(50) * 7.0   # Subcritical
        ])
        
        transitions = self.detector.detect_transition(C_series)
        
        assert transitions['n_down_transitions'] > 0
    
    def test_detect_critical_slowing(self):
        """Test critical slowing detection."""
        # Series with increasing variance (critical slowing)
        early = np.random.randn(25) * 0.1 + 8.0
        late = np.random.randn(25) * 0.5 + 8.0
        C_series = np.concatenate([early, late])
        
        result = self.detector.detect_critical_slowing(C_series)
        
        assert 'detected' in result
        assert 'variance_ratio' in result
        assert result['variance_ratio'] > 1.0
    
    def test_analyze_branches(self):
        """Test branch analysis."""
        # Post-transition data with multiple states
        C_post = np.concatenate([
            np.ones(20) * 8.5,
            np.ones(20) * 9.0,
            np.ones(20) * 9.5,
            np.ones(20) * 10.0,
        ])
        
        branches = self.detector.analyze_branches(C_post, n_branches=4)
        
        assert 'n_branches_detected' in branches
        assert 'branch_centers' in branches
        assert 'branch_populations' in branches
        assert branches['n_branches_detected'] > 0
    
    def test_detect_hysteresis(self):
        """Test hysteresis detection."""
        # Create series with hysteresis
        C_series = np.concatenate([
            np.linspace(7.0, 9.0, 50),  # Up transition
            np.linspace(9.0, 7.0, 50),  # Down transition
        ])
        
        hysteresis = self.detector.detect_hysteresis(C_series)
        
        assert 'detected' in hysteresis


def test_transition_sharpness():
    """Test transition sharpness measurement."""
    detector = BifurcationDetector()
    
    # Sharp transition
    C_sharp = np.concatenate([
        np.ones(50) * 7.0,
        np.ones(50) * 9.0
    ])
    
    # Gradual transition
    C_gradual = np.concatenate([
        np.ones(25) * 7.0,
        np.linspace(7.0, 9.0, 50),
        np.ones(25) * 9.0
    ])
    
    trans_sharp = detector.detect_transition(C_sharp)
    trans_gradual = detector.detect_transition(C_gradual)
    
    # Both should detect transitions
    assert trans_sharp['total_transitions'] > 0
    assert trans_gradual['total_transitions'] > 0


def test_multiple_transitions():
    """Test detecting multiple transitions."""
    detector = BifurcationDetector()
    
    # Series with multiple crossings
    C_series = np.array([7, 7, 9, 9, 7, 7, 9, 9, 7])
    
    transitions = detector.detect_transition(C_series)
    
    # Should detect multiple transitions
    assert transitions['total_transitions'] >= 2


def test_no_transition():
    """Test behavior with no transitions."""
    detector = BifurcationDetector()
    
    # Constant series
    C_series = np.ones(100) * 7.0
    
    transitions = detector.detect_transition(C_series)
    
    assert transitions['total_transitions'] == 0
    assert transitions['n_up_transitions'] == 0
    assert transitions['n_down_transitions'] == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
