# PAPER 3 - SECTION 3: INFORMATION PERSISTENCE MECHANISMS

## 3. Information Persistence Mechanisms

How does information survive state-space reorganization? Four complementary mechanisms operate across scales.

### 3.1 Attractor Dynamics

**Continuous Attractors:**
Neural populations form continuous attractor networks where nearby states flow toward stable configurations. Hopfield networks demonstrate that memories can be stored as attractor basins - perturbations return to the stored pattern.

**Basin Stability:**
Identity persistence requires robust basins. Small perturbations (noise, fluctuations) must not push the system into different attractors. Basin depth and width determine robustness.

**Rajan et al. (2016) - Transient Attractors:**
Working memory can use transient attractors - temporarily stable states maintained by dynamic connectivity. Information persists not in fixed points but in time-varying manifolds.

**Identity Application:**
Core identity features occupy deep, wide attractor basins. Peripheral features occupy shallow basins, more susceptible to change. This explains why personality persists while opinions evolve.

### 3.2 Topological Invariants

**Betti Numbers:**
Topology characterizes spaces by features preserved under continuous deformation:
- β₀: Number of connected components
- β₁: Number of loops/holes
- β₂: Number of voids/cavities

These invariants persist through state-space stretching, compressing, or folding - as long as no tearing or gluing occurs.

**Persistent Homology:**
This technique tracks topological features across scales. Applied to neural data, it reveals structure invisible to correlation-based methods.

**Durstewitz et al. (2024) - MARBLE:**
Geometric deep learning for neural population dynamics shows that topological features of neural manifolds persist across sessions, animals, and conditions. The shape of neural state-space is more stable than the activity filling it.

**Identity Application:**
PIS encodes identity in topological features (β₁ = self-referential loops). These persist through CCL bifurcation because topology is preserved under dimensional changes that don't tear the manifold.

### 3.3 Geometric Invariants

**Information Geometry:**
Neural states form probability distributions. Information geometry treats these as manifolds with natural Riemannian metric (Fisher information).

**Oizumi et al. (2016):**
Integrated information Φ can be expressed as geodesic distance in probability space. This geometric formulation reveals that consciousness structure has natural metric properties.

**Preserved Quantities:**
Geometric invariants include:
- Geodesic distances (preserved under reparametrization)
- Scalar curvature (intrinsic manifold property)
- Effective dimensionality (from metric eigenvalues)

**Identity Application:**
The geometric shape of the PIS manifold - its curvature, distances between key states, dimensionality - persists through transitions even as coordinate representations change.

### 3.4 Group-Theoretic Invariants

**Anselmi et al. (2020):**
Object identity persists through nuisance transformations (rotation, translation, scaling) via group-theoretic invariants. Hierarchical simple-complex cell cascades in visual cortex implement this.

**Invariance Principle:**
Identity = what remains constant under the group of transformations the system undergoes. For visual objects, this is 3D structure. For personal identity, it is the self-model structure.

**Hebbian Implementation:**
Learning rules create invariant representations. After training, the representation responds identically to transformed versions of the same object/self.

**Identity Application:**
The PIS learns invariant self-representation. Transformations (sleep, anesthesia, aging) are "nuisance variables" that change the representation's coordinate form but not its invariant content.

### 3.5 Synthesis: Multi-Mechanism Redundancy

No single mechanism suffices. Identity persistence relies on:
1. Attractor dynamics (stability against perturbation)
2. Topological invariants (preservation through deformation)
3. Geometric invariants (metric structure conservation)
4. Group-theoretic invariants (transformation-invariant encoding)

This redundancy explains robustness: damage to one mechanism is compensated by others. Only catastrophic disruption to all four causes identity loss.

---

**Word Count:** ~550 words
**Status:** DRAFT
