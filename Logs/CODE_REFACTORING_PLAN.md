# HIRM Code Refactoring Plan
**Created:** Session 18, 2025-12-20
**Status:** READY FOR IMPLEMENTATION
**Priority:** HIGH - Blocks empirical validation

---

## EXECUTIVE SUMMARY

Code review identified 5 critical issues preventing C(t) calculations from working correctly. The core problems are:

1. **Package terminology** - Still uses "ouroboros_observer" instead of "hirm"
2. **Phi algorithm** - Random partitioning unreliable for integration measurement
3. **R calculation** - Autocorrelation doesn't capture true self-reference
4. **Missing integration** - SelfReferenceEngine not connected to ConsciousnessMeasure
5. **Test imports** - All tests will fail due to wrong package name

---

## ISSUE 1: Package Naming (TERMINOLOGY)

### Problem
- setup.py: `name='ouroboros-observer'`
- Import path: `from ouroboros_observer import ...`
- Violates HIRM terminology standards

### Fix Required
Files to update:
- [ ] Code/setup.py - Change package name to 'hirm'
- [ ] Code/__init__.py - Update module docstring
- [ ] Code/Core/__init__.py - Update imports
- [ ] All test files - Change import statements
- [ ] Entry point: `ouroboros-validate` -> `hirm-validate`

### Code Change (setup.py)
```python
# OLD
name='ouroboros-observer',
author='Ouroboros Observer Research Team',

# NEW  
name='hirm',
author='HIRM Research Team',
```

---

## ISSUE 2: Phi Calculation Algorithm

### Problem
The `_calculate_Phi_geometric()` method uses random partitioning:
```python
indices = np.random.permutation(N)
half = N // 2
part1, part2 = indices[:half], indices[half:2*half]
```

This won't find the Minimum Information Partition (MIP). Random splits give inconsistent, often near-zero results.

### Root Cause
IIT's exact Phi requires testing all 2^N partitions (exponential). The random approximation sacrifices too much accuracy.

### Proposed Fix
Replace with hierarchical clustering-based partitioning:

```python
def _calculate_Phi_geometric_improved(self, activity, connectivity):
    """Improved Phi using connectivity-informed partitioning."""
    
    # 1. Use spectral clustering on connectivity
    from scipy.sparse.csgraph import laplacian
    from scipy.linalg import eigh
    
    L = laplacian(connectivity, normed=True)
    eigenvalues, eigenvectors = eigh(L)
    
    # 2. Use Fiedler vector for natural partition
    fiedler = eigenvectors[:, 1]  # Second smallest eigenvalue
    part1 = np.where(fiedler < np.median(fiedler))[0]
    part2 = np.where(fiedler >= np.median(fiedler))[0]
    
    # 3. Calculate effective information between parts
    # ... (rest of calculation)
```

### Alternative: Use PSI Method
The PSI method already exists and is more stable. Consider making it the default:
```python
self.Phi_method = 'PSI'  # Change from 'geometric'
```

---

## ISSUE 3: R (Self-Reference) Calculation

### Problem
Current R uses autocorrelation decay:
```python
def calculate_R(self, activity_history):
    # Uses autocorrelation - measures temporal memory, NOT self-reference
    decay_rate = -np.polyfit(range(len(autocorr)), 
                             np.log(np.abs(autocorr) + 1e-10), 1)[0]
    R = 1.0 + np.exp(-decay_rate)
```

This measures **temporal memory** (how long activity persists), not **self-reference** (system modeling itself).

### Root Cause
Self-reference requires:
- A model of the system's own state
- Comparison between prediction and observation
- The model influencing the system

Autocorrelation doesn't capture this.

### Proposed Fix
Integrate SelfReferenceEngine into ConsciousnessMeasure:

```python
def calculate_R(self, activity_history, connectivity=None):
    """Calculate R using actual self-reference measurement."""
    
    if len(activity_history.T) < 10:
        return 1.0
    
    # Initialize self-reference engine
    engine = SelfReferenceEngine(
        state_dim=activity_history.shape[0]
    )
    
    # Run self-modeling simulation
    for t in range(activity_history.shape[1]):
        result = engine.step_recursion(activity_history[:, t])
    
    # R from convergence and loop strength
    loop_strength = engine.measure_strange_loop_strength()
    convergence = engine.check_convergence()
    
    # Map to R in [1, 3]
    if convergence['converged']:
        R = 1.0 + 2.0 * loop_strength  # Converged = stable self-model
    else:
        R = 1.0 + loop_strength  # Still developing
    
    return min(R, 3.0)
```

---

## ISSUE 4: Missing Integration

### Problem
SelfReferenceEngine (self_reference.py) and ConsciousnessMeasure (consciousness_measure.py) are completely separate. They don't share data or interact.

### Proposed Architecture

```
ConsciousnessMeasure
    |
    +-- calculate_Phi() --> Integration measure
    |
    +-- calculate_R() --> SelfReferenceEngine
    |       |
    |       +-- step_recursion()
    |       +-- measure_strange_loop_strength()
    |
    +-- calculate_D() --> Branching parameter
    |
    +-- calculate_C() --> Phi * R * (1 - exp(-lambda*D))
```

### Implementation
Add import and integration in consciousness_measure.py:

```python
from .self_reference import SelfReferenceEngine

class ConsciousnessMeasure:
    def __init__(self, ...):
        # ... existing code ...
        self.self_ref_engine = None  # Lazy initialization
```

---

## ISSUE 5: Test Import Paths

### Problem
All tests use:
```python
from ouroboros_observer.consciousness_measure import ...
```

After renaming to 'hirm', all tests will fail.

### Files to Update
- [ ] Tests/test_consciousness_measure.py
- [ ] Tests/test_neural_network.py
- [ ] Tests/test_bifurcation_detector.py
- [ ] Tests/test_neural.py
- [ ] Tests/test_consciousness.py
- [ ] Tests/test_bifurcation.py

### Fix Pattern
```python
# OLD
from ouroboros_observer.consciousness_measure import ...

# NEW
from hirm.consciousness_measure import ...
```

---

## IMPLEMENTATION PRIORITY

| Priority | Issue | Effort | Impact |
|----------|-------|--------|--------|
| 1 | Phi algorithm fix | Medium | HIGH - Core calculation |
| 2 | R integration | Medium | HIGH - Core calculation |
| 3 | Package rename | Low | Medium - Terminology compliance |
| 4 | Test imports | Low | Medium - Test suite |
| 5 | Architecture docs | Low | Low - Maintainability |

---

## VALIDATION APPROACH

After fixes, validate with MINIMAL Python (no scipy imports):

```bash
# Syntax check only
python -m py_compile Code/Core/consciousness_measure.py
python -m py_compile Code/Core/self_reference.py

# Then run one simple test
python -c "from hirm.consciousness_measure import ConsciousnessMeasure; print('Import OK')"
```

---

## NEXT STEPS

1. Create backup of current Code/ directory
2. Apply package rename (Issue 1, 3, 5)
3. Implement improved Phi algorithm (Issue 2)
4. Integrate SelfReferenceEngine (Issue 4)
5. Syntax-check all modified files
6. Run minimal validation tests
7. Update BUILD_STATUS with results

---

**Document Status:** Ready for implementation in future session
