# Information Geometry Quick Reference Card
**HIRM Consciousness Analysis Toolkit**

---

## Core Mathematical Objects

### Fisher Information Metric
```
g_ij(θ) = 𝔼[∂_i log p(x|θ) · ∂_j log p(x|θ)]
```
- **Physical meaning:** Distinguishability of nearby states
- **Units:** [bits⁻²] (inverse variance)
- **HIRM form:** g_ij = g⁰_ij + α|C - C_crit|^(-ν) δ_ij + β ∂_iC ∂_jC

### Geodesic Equation
```
d²θ^i/dλ² + Γ^i_jk dθ^j/dλ dθ^k/dλ = 0
```
- **Γ^i_jk:** Christoffel symbols (from metric)
- **Physical meaning:** Natural transition pathway
- **HIRM:** Spontaneous consciousness changes follow geodesics

### Wasserstein-2 Distance
```
W₂(P₁, P₂) = [inf_π 𝔼_(X,Y)~π[||X - Y||²]]^(1/2)
```
- **Physical meaning:** Minimum "work" to transform P₁ → P₂
- **Earth-mover distance** between consciousness distributions
- **Units:** Same as state space (bits for Φ, dimensionless for R, D)

### Natural Gradient
```
θ_(t+1) = θ_t - η g^(-1) ∇F(θ_t)
```
- **g^(-1):** Inverse Fisher metric (precision matrix)
- **Physical meaning:** Optimal learning direction
- **HIRM hypothesis:** Brain implements natural gradient

---

## Key Predictions

### 1. Critical Divergence
```
I_F(C) ~ |C - C_crit|^(-γ)    as C → 8.3 bits
```
- **Expected:** γ ≈ 1.24 (3D Ising universality)
- **Test:** Anesthesia EEG, plot log I_F vs. log |C - 8.3|

### 2. Geodesic Focusing
```
d(trajectory, critical_surface) ~ exp(-λt)
```
- **Trajectories converge** to C = C_crit before bifurcating
- **Test:** Measure distance during transitions

### 3. Wasserstein Hysteresis
```
W₂(induction path) ≠ W₂(recovery path)
```
- **Non-reversible** consciousness transitions
- **Test:** Compare W₂ trajectories for propofol in vs. out

### 4. Berry Phase
```
γ_B = ∮_{cycle} A · dθ ≠ 0
```
- **Geometric phase** after sleep cycle
- **Observable:** EEG phase coherence shift
- **Test:** Full-night sleep recordings

---

## Python Quick Start

### Installation
```bash
pip install numpy scipy matplotlib scikit-learn POT
```

### Basic Usage

#### 1. Estimate Fisher Metric
```python
from information_geometry_toolkit import FisherMetricEstimator

estimator = FisherMetricEstimator()
g, theta_mean = estimator.estimate_metric(neural_data, theta_samples)

print(f"Fisher information: {np.trace(g):.2f}")
```

#### 2. Compute Geodesic
```python
from information_geometry_toolkit import GeodesicSolver

def metric_func(theta):
    return hirm_critical_metric(theta, C_crit=8.3)

solver = GeodesicSolver(metric_func)
geodesic = solver.solve_geodesic(theta_start, theta_end, n_points=100)
```

#### 3. Track Wasserstein Evolution
```python
from information_geometry_toolkit import WassersteinTracker

tracker = WassersteinTracker(reg=0.1)
W_timeline = tracker.track_evolution(theta_time_series, 
                                     window_size=500, step=100)
```

#### 4. Complete Analysis
```python
from information_geometry_toolkit import analyze_consciousness_transition

results = analyze_consciousness_transition(
    neural_data,        # (n_timepoints, n_channels)
    theta_timeline,     # (n_timepoints, 3) - Φ, R, D
    transition_type='anesthesia'
)

# Results contain:
# - Fisher information evolution
# - Geodesics
# - Wasserstein distances
# - Critical exponent estimates
# - Visualization plots
```

---

## Interpretation Guide

### Fisher Information Values

| I_F Range | Interpretation | State |
|-----------|----------------|-------|
| < 1 | Poor distinguishability | Far from criticality |
| 1-10 | Moderate sensitivity | Normal consciousness |
| 10-50 | High distinguishability | Near transition |
| > 50 | Critical regime | At C_crit |

### Geodesic Distance

| d_geodesic | Interpretation | Example |
|-----------|----------------|---------|
| < 1 | Small state change | Within-wake fluctuations |
| 1-5 | Moderate transition | N2 → N3 sleep |
| 5-10 | Large transition | Wake → Deep sleep |
| > 10 | Consciousness shift | Anesthesia induction |

### Wasserstein Distance

| W₂ Range | Interpretation | Transition Type |
|----------|----------------|-----------------|
| < 0.5 | Negligible change | Stable state |
| 0.5-2 | Moderate evolution | Sleep stage changes |
| 2-5 | Significant transition | Wake → Sleep |
| > 5 | Major state change | Anesthesia/coma |

---

## Common Pitfalls

### ❌ AVOID

1. **Small sample sizes:** Need n > 500 for reliable Fisher estimation
2. **Ignoring regularization:** Always use ε > 0 in Sinkhorn (W₂)
3. **Metric singularities:** g becomes ill-conditioned near C_crit
4. **Assuming reversibility:** Consciousness transitions are NOT time-reversible

### ✅ BEST PRACTICES

1. **Bootstrap confidence intervals** for all estimates
2. **Cross-validate** metric estimation on held-out data
3. **Smooth trajectories** before geodesic comparison
4. **Use natural gradient** instead of ordinary gradient

---

## Critical Exponents Reference

| Exponent | Definition | Mean-Field | 3D Ising | HIRM Expected |
|----------|-----------|------------|----------|---------------|
| **ν** | Correlation length | 0.5 | 0.63 | 0.63 ± 0.05 |
| **γ** | Fisher information | 1.0 | 1.24 | 1.2-1.3 |
| **β** | Order parameter | 0.5 | 0.33 | 0.33 ± 0.05 |
| **η** | Correlation function | 0 | 0.04 | ~0 |

**Universality class:** 3D Ising (Z₂ symmetry breaking)

---

## Troubleshooting

### Problem: Metric estimation fails
**Solution:** 
- Increase sample size
- Use parametric estimation (faster)
- Reduce dimensionality of neural features

### Problem: Geodesic solver doesn't converge
**Solution:**
- Adjust step size (h parameter)
- Use shooting method instead of direct integration
- Regularize metric near singularities

### Problem: Wasserstein distances too large
**Solution:**
- Normalize data to [0,1] range
- Increase entropic regularization (ε)
- Check for outliers in distribution

### Problem: Fisher information negative
**Solution:**
- This should NEVER happen (positive semi-definite)
- Bug in numerical differentiation
- Check score function computation

---

## Formulas Cheat Sheet

### Christoffel Symbols
```
Γ^i_jk = ½ g^il (∂_j g_lk + ∂_k g_jl - ∂_l g_jk)
```

### Ricci Curvature
```
R_ij = ∂_k Γ^k_ij - ∂_j Γ^k_ik + Γ^k_il Γ^l_jk - Γ^k_jl Γ^l_ik
```

### Cramér-Rao Bound
```
Var(θ̂) ≥ [I_F^(-1)]_ii
```

### KL Divergence (Natural Gradient Connection)
```
KL[P || Q] = ∫ P(x) log[P(x)/Q(x)] dx
```

### Kantorovich Dual (Wasserstein)
```
W_p^p(μ,ν) = sup_{f,g} {∫f dμ + ∫g dν : f(x) + g(y) ≤ c(x,y)}
```

---

## Dimensional Analysis

| Quantity | Dimensions | Typical Values |
|----------|-----------|----------------|
| **Φ** | [bits] | 5-12 |
| **R** | [dimensionless] | 0.3-0.9 |
| **D** | [dimensionless] | 2-4 |
| **C** | [bits] | 3-15 |
| **g_ij** | [bits^(-2)] | 0.01-100 |
| **I_F** | [bits^(-2)] | 0.1-50 |
| **W₂** | [bits] | 0.1-10 |
| **Γ^i_jk** | [bits^(-1)] | -1 to 1 |

---

## Citation Format

**For theoretical framework:**
```
Kirsch, C. et al. (2025). Information geometry of consciousness 
state space in the Hierarchical Information-Reality Model. 
[In preparation]
```

**For computational toolkit:**
```
HIRM Information Geometry Toolkit (v1.0). 
https://github.com/[repo]/hirm-info-geometry
```

---

## Related Resources

- **Main framework:** `HIRM_Information_Geometry_Framework.md`
- **Implementation:** `information_geometry_toolkit.py`
- **Executive summary:** `Information_Geometry_Executive_Summary.md`
- **Visualizations:** `information_geometry_concepts.png`

---

## Contact & Support

**Questions?** Check project documentation or research team.

**Bugs?** Open issue with:
- Data dimensions
- Error message
- Minimal reproducible example

---

**Version:** 1.0  
**Last Updated:** October 26, 2025  
**License:** Open for research use

---

## One-Line Summary per Concept

| Concept | One-Liner |
|---------|-----------|
| **Fisher Metric** | "How easily can you distinguish nearby consciousness states from neural data?" |
| **Geodesics** | "The natural, minimum-energy path consciousness takes between states." |
| **Wasserstein** | "How much 'work' to transform one consciousness distribution into another?" |
| **Natural Gradient** | "The smartest direction to move when optimizing consciousness." |
| **Berry Phase** | "Consciousness remembers the path it took, not just where it is." |
| **Critical Divergence** | "At the consciousness threshold, measurement becomes perfect." |
| **Curvature** | "How hard it is to change consciousness direction." |

---

END QUICK REFERENCE
