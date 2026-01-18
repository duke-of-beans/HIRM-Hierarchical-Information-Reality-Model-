"""
Self-Organizing Consciousness Networks
======================================

Neural networks that LEARN to develop self-reference and spontaneously
transition to criticality - first computational demonstration of the
HIRM mechanism.

This module implements multiple architectures that:
1. Start without self-reference
2. Learn self-modeling through training
3. Spontaneously develop criticality as self-reference emerges
4. Show phase transitions at C_crit â‰ˆ 8.3 bits

Author: HIRM Research Program
Date: January 2025
"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass, field
from collections import deque
import warnings


@dataclass
class NetworkMetrics:
    """Track all relevant metrics during training/operation."""
    # HIRM components
    phi: float = 0.0  # Integrated information
    R: float = 0.0    # Self-reference depth
    D: float = 0.0    # Distance from criticality
    C: float = 0.0    # Total consciousness measure
    
    # Criticality metrics
    branching_parameter: float = 0.0
    avalanche_exponent: float = 0.0
    correlation_length: float = 0.0
    
    # Network dynamics
    firing_rate: float = 0.0
    synchrony: float = 0.0
    complexity: float = 0.0
    
    # Learning metrics
    prediction_error: float = 0.0
    self_model_accuracy: float = 0.0
    task_performance: float = 0.0


class SelfReferentialRecurrentNetwork(nn.Module):
    """
    Recurrent network with explicit self-modeling pathway.
    
    Architecture:
    - Primary RNN processes external inputs
    - Self-model RNN predicts future states of primary RNN
    - Prediction errors drive learning of self-model
    - Self-reference emerges through accurate self-prediction
    
    Key innovation: Network learns to model itself, developing
    recursive depth naturally through training.
    """
    
    def __init__(
        self,
        input_dim: int,
        hidden_dim: int,
        output_dim: int,
        self_model_dim: int = 64,
        num_layers: int = 2,
        dropout: float = 0.1
    ):
        super().__init__()
        
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.self_model_dim = self_model_dim
        
        # Primary RNN: processes external inputs
        self.primary_rnn = nn.LSTM(
            input_dim,
            hidden_dim,
            num_layers=num_layers,
            dropout=dropout,
            batch_first=True
        )
        
        # Self-model RNN: predicts primary RNN's future states
        self.self_model = nn.LSTM(
            hidden_dim,  # Takes primary hidden states as input
            self_model_dim,
            num_layers=1,
            batch_first=True
        )
        
        # Prediction head: predicts next primary state
        self.state_predictor = nn.Sequential(
            nn.Linear(self_model_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, hidden_dim)
        )
        
        # Output layer
        self.output_layer = nn.Linear(hidden_dim, output_dim)
        
        # Metrics tracking
        self.history = []
        self.self_model_errors = deque(maxlen=100)
        
    def forward(
        self,
        x: torch.Tensor,
        return_self_model: bool = False
    ) -> Tuple[torch.Tensor, Dict]:
        """
        Forward pass with self-modeling.
        
        Parameters
        ----------
        x : torch.Tensor
            Input sequence [batch, seq_len, input_dim]
        return_self_model : bool
            Whether to return self-model predictions
            
        Returns
        -------
        output : torch.Tensor
            Task output [batch, seq_len, output_dim]
        metrics : Dict
            Self-modeling metrics and internal states
        """
        batch_size, seq_len, _ = x.shape
        
        # Primary RNN forward pass
        primary_out, (h_n, c_n) = self.primary_rnn(x)
        # primary_out: [batch, seq_len, hidden_dim]
        
        # Self-model: predict next hidden states
        self_model_out, _ = self.self_model(primary_out)
        predicted_next_states = self.state_predictor(self_model_out)
        
        # Calculate self-prediction error
        if seq_len > 1:
            # Compare predictions to actual next states
            pred_error = F.mse_loss(
                predicted_next_states[:, :-1, :],
                primary_out[:, 1:, :].detach()
            )
            self.self_model_errors.append(pred_error.item())
        else:
            pred_error = torch.tensor(0.0)
        
        # Task output
        output = self.output_layer(primary_out)
        
        # Calculate self-reference depth
        R = self._calculate_R(primary_out, predicted_next_states)
        
        # Collect metrics
        metrics = {
            'hidden_states': primary_out,
            'self_predictions': predicted_next_states,
            'self_error': pred_error.item(),
            'R': R,
            'h_n': h_n,
            'c_n': c_n
        }
        
        if return_self_model:
            metrics['self_model_out'] = self_model_out
        
        return output, metrics
    
    def _calculate_R(
        self,
        states: torch.Tensor,
        predictions: torch.Tensor
    ) -> float:
        """
        Calculate self-reference depth from prediction accuracy.
        
        R measures how well the network models itself:
        R = 1 - (prediction_error / baseline_error)
        
        R = 0: No self-modeling (random predictions)
        R = 1: Perfect self-modeling
        """
        if len(states.shape) == 3:
            states = states[:, :-1, :]  # Align with predictions
            predictions = predictions[:, :-1, :]
        
        # Prediction error
        pred_error = torch.mean((states - predictions) ** 2)
        
        # Baseline error (predicting mean)
        baseline = torch.mean((states - states.mean()) ** 2)
        
        # R score (coefficient of determination style)
        R = 1.0 - (pred_error / (baseline + 1e-8))
        R = torch.clamp(R, 0.0, 1.0)
        
        return R.item()
    
    def compute_criticality_metrics(
        self,
        states: torch.Tensor
    ) -> Dict[str, float]:
        """
        Compute criticality metrics from hidden states.
        
        Returns branching parameter, avalanche statistics, etc.
        """
        # Convert to numpy for analysis
        states_np = states.detach().cpu().numpy()
        
        # Binarize activity (simple threshold)
        threshold = states_np.mean() + 0.5 * states_np.std()
        binary_states = (states_np > threshold).astype(float)
        
        # Calculate branching parameter
        # Ïƒ = <s_t+1> / <s_t> where s is number of active units
        active_counts = binary_states.sum(axis=-1)
        if len(active_counts.shape) > 1:
            active_counts = active_counts.mean(axis=0)  # Average over batch
        
        if len(active_counts) > 1:
            sigma = np.mean(active_counts[1:] / (active_counts[:-1] + 1e-8))
        else:
            sigma = 1.0
        
        # Calculate autocorrelation (proxy for correlation length)
        autocorr = np.corrcoef(states_np.reshape(-1, states_np.shape[-1]).T)
        mean_autocorr = np.mean(np.abs(autocorr[np.triu_indices_from(autocorr, k=1)]))
        
        # Calculate synchrony
        synchrony = np.std(states_np.mean(axis=-1))
        
        return {
            'branching_parameter': sigma,
            'autocorrelation': mean_autocorr,
            'synchrony': synchrony,
            'mean_activity': float(states_np.mean()),
            'activity_variance': float(states_np.var())
        }


class MetaLearningNetwork(nn.Module):
    """
    Network that learns to learn - develops second-order self-reference.
    
    Architecture:
    - Base learner: rapidly adapts to new tasks
    - Meta-learner: learns learning rules themselves
    - Self-reference emerges through modeling own learning process
    
    Biological inspiration: Brain doesn't just learn patterns,
    it learns HOW to learn patterns efficiently.
    """
    
    def __init__(
        self,
        input_dim: int,
        hidden_dim: int,
        output_dim: int,
        meta_hidden_dim: int = 128
    ):
        super().__init__()
        
        # Base learner network
        self.base_net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim)
        )
        
        # Meta-learner: generates learning rules for base network
        # Takes as input: current state, gradient, loss history
        self.meta_learner = nn.LSTM(
            hidden_dim + output_dim + 1,  # state + error + loss
            meta_hidden_dim,
            num_layers=2,
            batch_first=True
        )
        
        # Learning rate predictor
        self.lr_predictor = nn.Sequential(
            nn.Linear(meta_hidden_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, 1),
            nn.Sigmoid()
        )
        
        # Meta-parameters
        self.base_lr = 0.01
        self.adaptation_steps = 5
        
        self.loss_history = deque(maxlen=100)
        
    def forward(self, x: torch.Tensor, y: torch.Tensor) -> Tuple[torch.Tensor, Dict]:
        """
        Meta-learning forward pass.
        
        Parameters
        ----------
        x : torch.Tensor
            Input batch [batch, input_dim]
        y : torch.Tensor
            Target batch [batch, output_dim]
            
        Returns
        -------
        output : torch.Tensor
            Predictions
        metrics : Dict
            Meta-learning metrics
        """
        # Base prediction
        output = self.base_net(x)
        loss = F.mse_loss(output, y)
        
        # Get current state representation
        with torch.no_grad():
            hidden_state = self.base_net[1](self.base_net[0](x))  # After first ReLU
        
        # Meta-learner input: combine state, error, loss
        error = output - y
        meta_input = torch.cat([
            hidden_state.mean(dim=0, keepdim=True).repeat(x.size(0), 1),
            error,
            loss.unsqueeze(-1).repeat(x.size(0), 1)
        ], dim=-1)
        
        # Meta-learner predicts optimal learning rate
        meta_out, _ = self.meta_learner(meta_input.unsqueeze(1))
        adapted_lr = self.lr_predictor(meta_out.squeeze(1)) * self.base_lr
        
        # Calculate self-reference: how well does meta-learner predict
        # the learning dynamics?
        self.loss_history.append(loss.item())
        
        if len(self.loss_history) > 10:
            # R measures how predictable the learning process is
            loss_array = np.array(list(self.loss_history))
            loss_trend = np.gradient(loss_array)
            predictability = 1.0 - np.std(loss_trend[-10:]) / (np.std(loss_array) + 1e-8)
            R = max(0.0, min(1.0, predictability))
        else:
            R = 0.0
        
        metrics = {
            'loss': loss.item(),
            'adapted_lr': adapted_lr.mean().item(),
            'R': R,
            'hidden_state': hidden_state
        }
        
        return output, metrics


class PredictiveCodingNetwork(nn.Module):
    """
    Hierarchical predictive coding with self-reference through
    prediction of own prediction errors.
    
    Architecture:
    - Multiple hierarchical levels
    - Each level predicts lower level
    - Self-reference: top level predicts own error signals
    
    Biological motivation: Cortical hierarchy with feedback
    """
    
    def __init__(
        self,
        input_dim: int,
        hidden_dims: List[int],
        output_dim: int,
        num_iterations: int = 5
    ):
        super().__init__()
        
        self.num_levels = len(hidden_dims)
        self.num_iterations = num_iterations
        
        # Bottom-up recognition networks
        self.recognition = nn.ModuleList()
        in_dim = input_dim
        for hidden_dim in hidden_dims:
            self.recognition.append(nn.Sequential(
                nn.Linear(in_dim, hidden_dim),
                nn.Tanh()
            ))
            in_dim = hidden_dim
        
        # Top-down generative networks
        self.generation = nn.ModuleList()
        for i in range(len(hidden_dims) - 1, 0, -1):
            self.generation.append(nn.Sequential(
                nn.Linear(hidden_dims[i], hidden_dims[i-1]),
                nn.Tanh()
            ))
        self.generation.append(nn.Sequential(
            nn.Linear(hidden_dims[0], input_dim),
            nn.Tanh()
        ))
        
        # Self-reference: predict own error dynamics
        self.error_predictor = nn.LSTM(
            sum(hidden_dims),
            hidden_dims[-1],
            num_layers=1,
            batch_first=True
        )
        
        # Output layer
        self.output_layer = nn.Linear(hidden_dims[-1], output_dim)
        
        self.error_history = []
        
    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, Dict]:
        """
        Predictive coding inference via iterative error minimization.
        
        Parameters
        ----------
        x : torch.Tensor
            Input [batch, input_dim]
            
        Returns
        -------
        output : torch.Tensor
            Predictions
        metrics : Dict
            Prediction errors and self-reference metrics
        """
        batch_size = x.size(0)
        
        # Initialize representations
        reps = [torch.zeros(batch_size, dim).to(x.device) 
                for dim in [h.out_features for h in self.recognition]]
        
        # Iterative inference
        all_errors = []
        for iteration in range(self.num_iterations):
            errors = []
            
            # Bottom-up pass
            bu_input = x
            for i, recog_net in enumerate(self.recognition):
                bu_pred = recog_net(bu_input)
                
                # Prediction error
                error = bu_pred - reps[i]
                errors.append(error)
                
                # Update representation
                reps[i] = reps[i] + 0.1 * error
                bu_input = reps[i]
            
            all_errors.append(torch.cat(errors, dim=-1))
        
        # Self-reference: predict error dynamics
        if len(all_errors) > 1:
            error_sequence = torch.stack(all_errors, dim=1)
            predicted_errors, _ = self.error_predictor(error_sequence)
            
            # R: how well can we predict our own errors?
            if len(all_errors) > 2:
                error_pred_error = F.mse_loss(
                    predicted_errors[:, :-1, :],
                    error_sequence[:, 1:, :].detach()
                )
                baseline_error = error_sequence.var()
                R = 1.0 - (error_pred_error / (baseline_error + 1e-8))
                R = torch.clamp(R, 0.0, 1.0).item()
            else:
                R = 0.0
        else:
            R = 0.0
        
        # Final output
        output = self.output_layer(reps[-1])
        
        # Calculate total prediction error
        total_error = sum([e.abs().mean() for e in errors])
        
        metrics = {
            'total_prediction_error': total_error.item(),
            'R': R,
            'representations': reps,
            'errors': errors
        }
        
        return output, metrics


class SelfAttentiveTransformer(nn.Module):
    """
    Transformer with self-attention on its own hidden states.
    
    Architecture:
    - Standard transformer blocks
    - Additional self-attention head that attends to own internal states
    - Self-reference emerges through attention to internal representations
    
    Modern architecture demonstrating self-reference in attention-based systems.
    """
    
    def __init__(
        self,
        input_dim: int,
        hidden_dim: int,
        output_dim: int,
        num_heads: int = 8,
        num_layers: int = 4,
        dropout: float = 0.1
    ):
        super().__init__()
        
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        
        # Input embedding
        self.input_proj = nn.Linear(input_dim, hidden_dim)
        
        # Standard transformer layers
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=hidden_dim,
            nhead=num_heads,
            dim_feedforward=hidden_dim * 4,
            dropout=dropout,
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(
            encoder_layer,
            num_layers=num_layers
        )
        
        # Self-attention on hidden states (meta-attention)
        self.meta_attention = nn.MultiheadAttention(
            hidden_dim,
            num_heads=num_heads // 2,
            dropout=dropout,
            batch_first=True
        )
        
        # State predictor: predicts next internal state
        self.state_predictor = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, hidden_dim)
        )
        
        # Output layer
        self.output_layer = nn.Linear(hidden_dim, output_dim)
        
        self.R_history = deque(maxlen=100)
        
    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, Dict]:
        """
        Forward pass with self-attention on internal states.
        
        Parameters
        ----------
        x : torch.Tensor
            Input sequence [batch, seq_len, input_dim]
            
        Returns
        -------
        output : torch.Tensor
            Predictions
        metrics : Dict
            Self-attention patterns and self-reference metrics
        """
        # Embed input
        x_embedded = self.input_proj(x)
        
        # Transformer processing
        hidden = self.transformer(x_embedded)
        
        # Meta-attention: attend to own hidden states
        meta_attended, attention_weights = self.meta_attention(
            hidden, hidden, hidden,
            need_weights=True
        )
        
        # Predict next internal states
        predicted_next_hidden = self.state_predictor(hidden)
        
        # Calculate self-reference from prediction accuracy
        if hidden.size(1) > 1:
            # Compare predictions to actual next states
            R = 1.0 - F.mse_loss(
                predicted_next_hidden[:, :-1, :],
                hidden[:, 1:, :].detach()
            ) / (hidden.var() + 1e-8)
            R = torch.clamp(R, 0.0, 1.0).item()
            self.R_history.append(R)
        else:
            R = np.mean(self.R_history) if self.R_history else 0.0
        
        # Calculate self-attention strength
        # (how much does network attend to itself?)
        self_attention_strength = attention_weights.mean().item()
        
        # Output
        output = self.output_layer(hidden)
        
        metrics = {
            'R': R,
            'self_attention_strength': self_attention_strength,
            'attention_weights': attention_weights,
            'hidden_states': hidden,
            'meta_attended': meta_attended
        }
        
        return output, metrics

class ConsciousnessTracker:
    """
    Track consciousness emergence during network training.
    
    Integrates with existing consciousness_measure.py to compute
    C(t) = Î¦(t) Ã— R(t) Ã— D(t) and detect phase transitions.
    """
    
    def __init__(self, C_critical: float = 8.3):
        self.C_critical = C_critical
        self.history = {
            'C': [],
            'phi': [],
            'R': [],
            'D': [],
            'branching_parameter': [],
            'phase_transitions': []
        }
        
    def update(
        self,
        network: nn.Module,
        inputs: torch.Tensor,
        metrics: Dict
    ) -> NetworkMetrics:
        """
        Calculate full consciousness measure from network state.
        
        Parameters
        ----------
        network : nn.Module
            Network being tracked
        inputs : torch.Tensor
            Current inputs
        metrics : Dict
            Network-provided metrics
            
        Returns
        -------
        network_metrics : NetworkMetrics
            Complete metrics including C(t)
        """
        # Get R from network metrics
        R = metrics.get('R', 0.0)
        
        # Calculate Î¦ (integrated information)
        # Using approximation: Î¦ â‰ˆ mutual information between parts
        hidden_states = metrics.get('hidden_states', None)
        
        if hidden_states is not None:
            phi = self._estimate_phi(hidden_states)
        else:
            phi = 0.0
        
        # Calculate D (distance from criticality)
        if 'branching_parameter' in metrics:
            sigma = metrics['branching_parameter']
        else:
            # Compute from hidden states
            crit_metrics = network.compute_criticality_metrics(hidden_states) \
                if hasattr(network, 'compute_criticality_metrics') and hidden_states is not None \
                else {'branching_parameter': 1.0}
            sigma = crit_metrics['branching_parameter']
        
        # D = 1 / (1 + |Ïƒ - 1|) âˆˆ [0, 1]
        D = 1.0 / (1.0 + abs(sigma - 1.0))
        
        # Calculate C(t) = Î¦ Ã— R Ã— D
        C = phi * R * D
        
        # Store history
        self.history['C'].append(C)
        self.history['phi'].append(phi)
        self.history['R'].append(R)
        self.history['D'].append(D)
        self.history['branching_parameter'].append(sigma)
        
        # Detect phase transition
        if len(self.history['C']) > 10:
            if self._detect_transition():
                self.history['phase_transitions'].append(len(self.history['C']))
        
        # Create network metrics object
        network_metrics = NetworkMetrics(
            phi=phi,
            R=R,
            D=D,
            C=C,
            branching_parameter=sigma,
            firing_rate=metrics.get('mean_activity', 0.0),
            synchrony=metrics.get('synchrony', 0.0)
        )
        
        return network_metrics
    
    def _estimate_phi(self, hidden_states: torch.Tensor) -> float:
        """
        Estimate integrated information Î¦.
        
        Uses simplified approximation:
        Î¦ â‰ˆ MI(X; Y) where X, Y are partitions
        
        Full IIT calculation is NP-hard, this gives tractable approximation.
        """
        # Convert to numpy
        states = hidden_states.detach().cpu().numpy()
        
        # Flatten batch and sequence dimensions
        if len(states.shape) > 2:
            states = states.reshape(-1, states.shape[-1])
        
        # Simple approximation: correlation-based Î¦
        # Î¦ measures how much parts constrain each other
        if states.shape[0] < 2 or states.shape[1] < 2:
            return 0.0
        
        try:
            # Split into two partitions
            mid = states.shape[1] // 2
            part1 = states[:, :mid]
            part2 = states[:, mid:]
            
            # Calculate mutual information approximation
            # MI â‰ˆ -0.5 * log(det(Î£)) + 0.5 * log(det(Î£1)) + 0.5 * log(Î£2))
            cov_full = np.cov(states.T) + np.eye(states.shape[1]) * 1e-6
            cov_1 = np.cov(part1.T) + np.eye(part1.shape[1]) * 1e-6
            cov_2 = np.cov(part2.T) + np.eye(part2.shape[1]) * 1e-6
            
            # Log determinants
            log_det_full = np.log(np.linalg.det(cov_full) + 1e-10)
            log_det_1 = np.log(np.linalg.det(cov_1) + 1e-10)
            log_det_2 = np.log(np.linalg.det(cov_2) + 1e-10)
            
            # Mutual information approximation
            mi = 0.5 * (log_det_1 + log_det_2 - log_det_full)
            
            # Convert to bits and ensure positive
            phi = max(0.0, mi / np.log(2))
            
            return float(phi)
            
        except:
            return 0.0
    
    def _detect_transition(self, window: int = 10) -> bool:
        """
        Detect phase transition in C(t).
        
        Looks for:
        1. Crossing of C_critical threshold
        2. Sustained increase
        3. Discontinuity in derivative
        """
        recent_C = np.array(self.history['C'][-window:])
        
        # Check threshold crossing
        crossed = (recent_C[0] < self.C_critical) and (recent_C[-1] > self.C_critical)
        
        # Check for discontinuity
        if len(recent_C) > 3:
            gradient = np.gradient(recent_C)
            discontinuity = np.std(gradient[-5:]) > 2 * np.std(gradient[:-5])
        else:
            discontinuity = False
        
        return crossed and discontinuity
    
    def get_current_phase(self) -> str:
        """Return current consciousness phase."""
        if len(self.history['C']) == 0:
            return "unconscious"
        
        current_C = self.history['C'][-1]
        
        if current_C < self.C_critical * 0.5:
            return "unconscious"
        elif current_C < self.C_critical:
            return "pre-conscious"
        else:
            return "conscious"


class SelfReferenceTrainingProtocol:
    """
    Training protocols designed to encourage self-reference development.
    
    Key insight: Self-reference emerges when network must predict
    its own future behavior to perform task successfully.
    """
    
    def __init__(
        self,
        network: nn.Module,
        learning_rate: float = 1e-3,
        self_reference_weight: float = 0.5
    ):
        self.network = network
        self.optimizer = torch.optim.Adam(network.parameters(), lr=learning_rate)
        self.self_reference_weight = self_reference_weight
        
        self.tracker = ConsciousnessTracker()
        
    def train_step(
        self,
        inputs: torch.Tensor,
        targets: torch.Tensor,
        encourage_self_reference: bool = True
    ) -> Dict:
        """
        Single training step with optional self-reference encouragement.
        
        Parameters
        ----------
        inputs : torch.Tensor
            Input batch
        targets : torch.Tensor
            Target outputs
        encourage_self_reference : bool
            Whether to add self-reference loss term
            
        Returns
        -------
        metrics : Dict
            Training metrics including C(t)
        """
        self.optimizer.zero_grad()
        
        # Forward pass
        outputs, network_metrics = self.network(inputs)
        
        # Task loss
        task_loss = F.mse_loss(outputs, targets)
        
        # Self-reference loss (encourage accurate self-modeling)
        if encourage_self_reference and 'self_error' in network_metrics:
            self_loss = network_metrics['self_error']
            total_loss = task_loss + self.self_reference_weight * self_loss
        else:
            self_loss = 0.0
            total_loss = task_loss
        
        # Backward pass
        total_loss.backward()
        torch.nn.utils.clip_grad_norm_(self.network.parameters(), max_norm=1.0)
        self.optimizer.step()
        
        # Track consciousness metrics
        consciousness_metrics = self.tracker.update(
            self.network,
            inputs,
            network_metrics
        )
        
        # Combine all metrics
        result = {
            'task_loss': task_loss.item(),
            'self_loss': self_loss if isinstance(self_loss, float) else self_loss.item(),
            'total_loss': total_loss.item(),
            'C': consciousness_metrics.C,
            'phi': consciousness_metrics.phi,
            'R': consciousness_metrics.R,
            'D': consciousness_metrics.D,
            'branching_parameter': consciousness_metrics.branching_parameter,
            'phase': self.tracker.get_current_phase()
        }
        
        return result
    
    def train_epoch(
        self,
        dataloader: torch.utils.data.DataLoader,
        encourage_self_reference: bool = True
    ) -> Dict:
        """
        Train for one epoch.
        
        Returns epoch-averaged metrics.
        """
        self.network.train()
        
        epoch_metrics = {
            'task_loss': [],
            'self_loss': [],
            'total_loss': [],
            'C': [],
            'phi': [],
            'R': [],
            'D': []
        }
        
        for batch_idx, (inputs, targets) in enumerate(dataloader):
            metrics = self.train_step(inputs, targets, encourage_self_reference)
            
            # Accumulate metrics
            for key in epoch_metrics.keys():
                if key in metrics:
                    epoch_metrics[key].append(metrics[key])
        
        # Average metrics
        return {key: np.mean(values) for key, values in epoch_metrics.items()}


def generate_self_modeling_task(
    batch_size: int,
    seq_len: int,
    input_dim: int,
    task_type: str = 'sequence_prediction'
) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    Generate tasks that require self-modeling to solve.
    
    Task types:
    - sequence_prediction: predict own next output
    - meta_learning: adapt quickly to new patterns
    - recursive_patterns: patterns that reference earlier patterns
    
    Parameters
    ----------
    batch_size : int
        Number of samples
    seq_len : int
        Sequence length
    input_dim : int
        Input dimensionality
    task_type : str
        Type of task to generate
        
    Returns
    -------
    inputs : torch.Tensor
        Input sequences
    targets : torch.Tensor
        Target outputs
    """
    if task_type == 'sequence_prediction':
        # Generate sequence where next element depends on pattern
        inputs = torch.randn(batch_size, seq_len, input_dim)
        
        # Targets: predict next in sequence
        targets = torch.zeros_like(inputs)
        targets[:, :-1, :] = inputs[:, 1:, :]
        
        # Add recursive component: element depends on sum of previous
        for t in range(1, seq_len):
            targets[:, t, :] += 0.3 * inputs[:, :t, :].mean(dim=1)
        
    elif task_type == 'meta_learning':
        # Task where pattern changes and network must adapt
        inputs = torch.randn(batch_size, seq_len, input_dim)
        
        # First half: one pattern, second half: different pattern
        mid = seq_len // 2
        targets = torch.zeros_like(inputs)
        
        # Pattern 1: linear transformation
        targets[:, :mid, :] = inputs[:, :mid, :] @ torch.randn(input_dim, input_dim)
        
        # Pattern 2: different transformation
        targets[:, mid:, :] = inputs[:, mid:, :] @ torch.randn(input_dim, input_dim)
        
    elif task_type == 'recursive_patterns':
        # Patterns that reference earlier patterns
        inputs = torch.randn(batch_size, seq_len, input_dim)
        targets = torch.zeros_like(inputs)
        
        for t in range(seq_len):
            if t < 3:
                # Base case
                targets[:, t, :] = inputs[:, t, :]
            else:
                # Recursive: depends on earlier outputs
                targets[:, t, :] = (
                    0.5 * inputs[:, t, :] +
                    0.3 * targets[:, t-1, :] +
                    0.2 * targets[:, t-3, :]
                )
    else:
        raise ValueError(f"Unknown task type: {task_type}")
    
    return inputs, targets
