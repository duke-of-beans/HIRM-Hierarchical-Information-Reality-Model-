# Ouroboros Observer Toolkit - Quick Start Guide

## Installation

```bash
# Navigate to the toolkit directory
cd ouroboros-observer

# Install the package
pip install -e .

# Verify installation
python -c "import ouroboros_observer; print('Installation successful!')"
```

## 5-Minute Quickstart

### 1. Basic Simulation

```python
from ouroboros_observer import NeuralNetwork, ConsciousnessMeasure

# Create network
network = NeuralNetwork(N_neurons=100)

# Run simulation
results = network.run(duration=5000.0)

# Calculate consciousness measure
measure = ConsciousnessMeasure()
C, components = measure.calculate_C(
    activity=results['spikes'][-1],
    connectivity=network.W,
    activity_history=results['spikes'][-100:]
)

print(f"C(t) = {C:.2f} bits")
if C > 8.3:
    print("State: CONSCIOUS")
else:
    print("State: UNCONSCIOUS")
```

### 2. Run Demo Script

```bash
cd examples
python demo_consciousness_transition.py
```

This will:
- Simulate a 10-second consciousness transition
- Detect phase transitions automatically
- Generate publication-quality visualization
- Save results as `consciousness_transition_demo.png`

### 3. Run Validation Suite

```bash
cd examples
python run_validation.py
```

This validates:
- C_critical â‰ˆ 8.3 bits
- 4-5 bifurcation branches
- Binary classification accuracy

### 4. Explore Tutorials

Open Jupyter notebooks in `examples/`:

```bash
jupyter notebook examples/tutorial_1_basic_C_calculation.ipynb
```

Available tutorials:
1. Basic C(t) calculation
2. Network simulation
3. Phase transition detection
4. Parameter exploration
5. Reproducing key predictions

## Core Components

### Neural Network
```python
from ouroboros_observer import NeuralNetwork

network = NeuralNetwork(
    N_neurons=100,
    dt=0.1,  # Time step (ms)
    seed=42  # For reproducibility
)

# Run with external input
I_ext = np.ones(100) * 5.0
results = network.run(duration=1000.0, I_ext=I_ext)
```

### Consciousness Measure
```python
from ouroboros_observer import ConsciousnessMeasure

measure = ConsciousnessMeasure(
    lambda_param=5.0,
    Phi_method='geometric'  # or 'stochastic', 'psi'
)

C, components = measure.calculate_C(activity, connectivity, history)

# Access components
Phi = components['Phi']  # Integration
R = components['R']      # Recursion
D = components['D']      # Criticality
```

### Phase Transition Detector
```python
from ouroboros_observer import BifurcationDetector

detector = BifurcationDetector(C_critical=8.3)

# Monitor C(t) time series
results = detector.monitor(C_timeseries, time)

# Detect transitions
transitions = detector.detect_transitions(C_timeseries, time)
```

### Visualization
```python
from ouroboros_observer.visualization import plots

# Plot C(t) time series
fig, ax = plots.plot_C_timeseries(C_t, time, transitions=transitions)

# Plot all components
fig, axes = plots.plot_components(Phi_t, R_t, D_t, C_t, time)

# 3D phase space
fig, ax = plots.plot_phase_space(Phi_t, R_t, D_t, C_t)
```

## Common Tasks

### Task 1: Detect Consciousness Transition
```python
# Gradually increase input
C_timeseries = []
for strength in np.linspace(0, 10, 1000):
    I_ext = np.ones(100) * strength
    network.step(I_ext)
    
    C, _ = measure.calculate_C(...)
    C_timeseries.append(C)

# Find transition point
detector = BifurcationDetector()
transitions = detector.detect_transitions(np.array(C_timeseries))

if transitions:
    print(f"Transition at step {transitions[0].time}")
    print(f"C_critical = {transitions[0].C_after:.2f} bits")
```

### Task 2: Parameter Sensitivity
```python
from ouroboros_observer import ParameterExplorer

def objective(params):
    network = NeuralNetwork(params['N'])
    # ... run simulation
    return C_value

explorer = ParameterExplorer(objective)

# Sensitivity analysis
sensitivities = explorer.sensitivity_analysis(
    baseline_params={'N': 100, 'J_exc': 0.1}
)

# Most sensitive parameter
max_sensitivity = max(sensitivities.items(), 
                     key=lambda x: x[1]['mean_gradient'])
print(f"Most sensitive: {max_sensitivity[0]}")
```

### Task 3: Validate Predictions
```python
from ouroboros_observer import ValidationFramework

validator = ValidationFramework(seed=42)

# Test C_critical
results = validator.test_transition_prediction(n_trials=10)
print(f"C_critical = {results['mean_C_critical']:.2f} Â± {results['std_C_critical']:.2f}")

# Test branch number
results = validator.test_branch_number(n_trials=5)
print(f"Branches = {results['mean_branches']:.1f} Â± {results['std_branches']:.1f}")
```

## Troubleshooting

### Issue: C(t) always near zero
**Solution**: Increase external input or tune network to criticality
```python
network.tune_to_criticality(target_rate=5.0)
```

### Issue: No transitions detected
**Solution**: Ensure sufficient parameter sweep range and sampling
```python
# Use wider range
for strength in np.linspace(0, 20, 2000):  # More samples, wider range
    ...
```

### Issue: Phi calculation too slow
**Solution**: Use faster method or reduce network size
```python
measure = ConsciousnessMeasure(Phi_method='psi')  # Fastest method
```

## Next Steps

1. **Read Documentation**: Full API docs at [ReadTheDocs]
2. **Study Examples**: Work through all tutorial notebooks
3. **Run Experiments**: Modify demo scripts for your research
4. **Cite the Work**: See README for citation information

## Getting Help

- **Issues**: Report bugs on GitHub
- **Questions**: Check documentation or contact maintainers
- **Contributions**: See CONTRIBUTING.md

## Performance Tips

1. **Network Size**: Start with N=50-100 for testing, scale up as needed
2. **Sampling**: Sample C(t) every 50-100 steps (not every step)
3. **Phi Method**: Use 'geometric' for speed, 'stochastic' for accuracy
4. **Parallel**: Use parallel parameter sweeps for large explorations

## Key Thresholds

- **C_critical**: 8.3 bits (consciousness transition)
- **Firing rate**: 5 Hz (critical dynamics)
- **Branching parameter**: Ïƒ â‰ˆ 1.0 (criticality)
- **Branches**: 4-5 (post-transition states)

---

**Ready to explore consciousness dynamics!** ðŸ§ âœ¨
