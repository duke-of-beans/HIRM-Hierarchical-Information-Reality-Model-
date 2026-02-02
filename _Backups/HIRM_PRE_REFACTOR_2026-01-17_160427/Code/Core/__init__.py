"""
Ouroboros Observer: Computational Toolkit for Consciousness Phase Transitions
"""

__version__ = "0.1.0"

from .core.neural_network import NeuralNetwork, NeuronParams, SynapseParams, generate_small_world
from .core.consciousness_measure import ConsciousnessMeasure, measure_branching_parameter
from .core.phase_transition import BifurcationDetector, TransitionEvent
from .analysis.parameter_exploration import ParameterExplorer
from .validation.framework import ValidationFramework

__all__ = [
    'NeuralNetwork', 'NeuronParams', 'SynapseParams',
    'ConsciousnessMeasure', 'BifurcationDetector',
    'ParameterExplorer', 'ValidationFramework'
]
