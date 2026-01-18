"""
HIRM Component Correlation Analysis
====================================

Research Priority: TIER 1 - HIGHEST
Status: Implementation ready, awaiting data download
Date: 2025-12-20

PURPOSE:
Calculate correlations ρ(Φ,R), ρ(Φ,D), ρ(R,D) across consciousness states
to test component independence assumption in HIRM framework.

BACKGROUND (Session 10):
The multiplicative model C(t) = Φ(t) × R(t) × D(t) assumes component
quasi-independence. Stochastic simulation estimates suggest:
- ρ_phi_r = 0.3 (Φ-R correlation)
- ρ_phi_d = 0.2 (Φ-D correlation)  
- ρ_r_d = 0.25 (R-D correlation)

LOCKED CONSTANTS (from Master_Data):
- C_critical = 8.3 ± 0.6 bits
"""

import numpy as np
from scipy.stats import pearsonr, spearmanr, kendalltau
from typing import Dict, List, Optional
from collections import Counter
import warnings
import math

class ComponentCorrelationAnalyzer:
    """Analyze correlations between HIRM components (Φ, R, D)."""
    
    def __init__(self, C_critical: float = 8.3, sampling_rate: int = 100):
        self.C_critical = C_critical
        self.sampling_rate = sampling_rate
        self.results = {}
    
    def calculate_components_from_eeg(self, eeg_data: np.ndarray) -> Dict[str, np.ndarray]:
        """Calculate Φ, R, D components from EEG epochs."""
        if eeg_data.ndim == 2:
            eeg_data = eeg_data[np.newaxis, :, :]
        
        n_epochs = eeg_data.shape[0]
        Phi = np.zeros(n_epochs)
        R = np.zeros(n_epochs)
        D = np.zeros(n_epochs)
        
        for i in range(n_epochs):
            Phi[i] = self._calculate_phi(eeg_data[i])
            R[i] = self._calculate_R(eeg_data[i])
            D[i] = self._calculate_D(eeg_data[i])
        
        return {'Phi': Phi, 'R': R, 'D': D, 'C': Phi * R * D}
    
    def _calculate_phi(self, epoch: np.ndarray) -> float:
        """Calculate integrated information Φ."""
        n_ch = epoch.shape[0]
        try:
            corr = np.corrcoef(epoch)
            upper = np.triu_indices(n_ch, k=1)
            integration = np.nanmean(np.abs(corr[upper]))
        except:
            integration = 0.0
        
        diff_vals = [self._perm_entropy(epoch[ch]) for ch in range(n_ch)]
        differentiation = np.mean(diff_vals) if diff_vals else 0.0
        
        if integration > 0 and differentiation > 0:
            return float(np.sqrt(integration * differentiation) * 10.0)
        return 0.0
    
    def _calculate_R(self, epoch: np.ndarray) -> float:
        """Calculate self-reference coefficient R."""
        gfp = np.mean(epoch, axis=0)
        lag_min, lag_max = int(0.01 * self.sampling_rate), int(0.1 * self.sampling_rate)
        
        autocorrs = []
        for lag in range(lag_min, min(lag_max + 1, len(gfp) - 1)):
            try:
                c = np.corrcoef(gfp[:-lag], gfp[lag:])[0, 1]
                if not np.isnan(c):
                    autocorrs.append(abs(c))
            except:
                pass
        
        return float(np.clip(np.mean(autocorrs) if autocorrs else 0.5, 0, 1))
    
    def _calculate_D(self, epoch: np.ndarray) -> float:
        """Calculate effective dimensionality D via DFA."""
        gfp = np.mean(epoch, axis=0)
        try:
            alpha = self._dfa(gfp)
            return float(1.0 / (1.0 + abs(alpha - 1.0)))
        except:
            return 0.5
    
    def _perm_entropy(self, x: np.ndarray, order: int = 3) -> float:
        """Permutation entropy."""
        n = len(x)
        if n < order + 1:
            return 0.0
        patterns = [tuple(np.argsort(x[i:i+order])) for i in range(n - order)]
        counts = Counter(patterns)
        probs = np.array(list(counts.values())) / len(patterns)
        return float(-np.sum(probs * np.log2(probs + 1e-12)) / np.log2(math.factorial(order)))
    
    def _dfa(self, x: np.ndarray) -> float:
        """Detrended Fluctuation Analysis exponent."""
        n = len(x)
        if n < 16:
            return 1.0
        y = np.cumsum(x - np.mean(x))
        windows = np.unique(np.logspace(np.log10(4), np.log10(n // 4), 15).astype(int))
        
        flucts, valid_ws = [], []
        for ws in windows:
            if ws < 4 or ws > n // 2:
                continue
            n_win = n // ws
            F2 = []
            for j in range(n_win):
                seg = y[j*ws:(j+1)*ws]
                trend = np.polyval(np.polyfit(np.arange(len(seg)), seg, 1), np.arange(len(seg)))
                F2.append(np.mean((seg - trend)**2))
            if F2:
                flucts.append(np.sqrt(np.mean(F2)))
                valid_ws.append(ws)
        
        if len(flucts) < 3:
            return 1.0
        return float(np.polyfit(np.log(valid_ws), np.log(flucts), 1)[0])
    
    def compute_correlations(self, components: Dict, state_labels: Optional[np.ndarray] = None) -> Dict:
        """Compute pairwise correlations between Φ, R, D."""
        Phi, R, D = components['Phi'], components['R'], components['D']
        
        results = {'global': {}, 'by_state': {}, 'n': len(Phi)}
        pairs = [('Phi', 'R', Phi, R), ('Phi', 'D', Phi, D), ('R', 'D', R, D)]
        
        for n1, n2, a1, a2 in pairs:
            key = f'rho_{n1}_{n2}'
            r, p = pearsonr(a1, a2)
            rho, ps = spearmanr(a1, a2)
            results['global'][key] = {'pearson': {'r': float(r), 'p': float(p)},
                                      'spearman': {'rho': float(rho), 'p': float(ps)}, 'n': len(a1)}
        
        if state_labels is not None:
            for state in np.unique(state_labels):
                mask = state_labels == state
                if np.sum(mask) < 10:
                    continue
                results['by_state'][str(state)] = {'n': int(np.sum(mask))}
                for n1, n2, a1, a2 in pairs:
                    r, p = pearsonr(a1[mask], a2[mask])
                    results['by_state'][str(state)][f'rho_{n1}_{n2}'] = {'r': float(r), 'p': float(p)}
        
        # Independence test
        r_PhiR, _ = pearsonr(Phi, R)
        r_PhiD, _ = pearsonr(Phi, D)
        r_RD, _ = pearsonr(R, D)
        max_corr = max(abs(r_PhiR), abs(r_PhiD), abs(r_RD))
        
        results['independence_tests'] = {
            'independence_assessment': {
                'max_correlation': float(max_corr),
                'quasi_independent': max_corr < 0.3,
                'interpretation': 'Components quasi-independent' if max_corr < 0.3 else 'Significant coupling detected'
            }
        }
        
        self.results = results
        return results


def run_synthetic_validation():
    """Validate on synthetic data."""
    print("=" * 70)
    print("HIRM Component Correlation Analysis - Synthetic Validation")
    print("=" * 70)
    
    np.random.seed(42)
    
    n_epochs, n_ch, n_samp = 100, 8, 3000
    states = np.repeat(['Wake', 'N1', 'N2', 'N3', 'REM'], n_epochs // 5)
    
    params = {'Wake': (12, 0.8, 0.9), 'N1': (8, 0.6, 0.7), 'N2': (5, 0.5, 0.6),
              'N3': (2, 0.3, 0.4), 'REM': (9, 0.65, 0.85)}
    
    print("\nGenerating synthetic EEG...")
    eeg = np.zeros((len(states), n_ch, n_samp))
    
    for i, st in enumerate(states):
        phi, _, _ = params[st]
        corr_str = phi / 15
        base = np.random.randn(n_samp) * corr_str
        
        t = np.arange(n_samp) / 100
        for ch in range(n_ch):
            sig = base + np.random.randn(n_samp) * (1 - corr_str)
            if st == 'Wake':
                sig += 0.5 * np.sin(2*np.pi*10*t)
            elif st == 'N3':
                sig += 1.0 * np.sin(2*np.pi*1.5*t)
            elif st == 'REM':
                sig += 0.3 * np.sin(2*np.pi*8*t)
            eeg[i, ch] = sig
    
    analyzer = ComponentCorrelationAnalyzer()
    
    print("Calculating components...")
    components = analyzer.calculate_components_from_eeg(eeg)
    
    print(f"\nComponent stats:")
    print(f"  Phi: {np.mean(components['Phi']):.2f} +/- {np.std(components['Phi']):.2f}")
    print(f"  R: {np.mean(components['R']):.3f} +/- {np.std(components['R']):.3f}")
    print(f"  D: {np.mean(components['D']):.3f} +/- {np.std(components['D']):.3f}")
    print(f"  C: {np.mean(components['C']):.2f} +/- {np.std(components['C']):.2f}")
    
    print("\nComputing correlations...")
    correlations = analyzer.compute_correlations(components, states)
    
    print("\n" + "-" * 50)
    print("GLOBAL CORRELATIONS:")
    for pair, stats in correlations['global'].items():
        r = stats['pearson']['r']
        p = stats['pearson']['p']
        sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
        print(f"  {pair}: r = {r:.3f} (p = {p:.4f}) {sig}")
    
    print("\n" + "-" * 50)
    print("STATE-STRATIFIED:")
    for st, st_data in correlations['by_state'].items():
        print(f"\n  {st} (N={st_data['n']}):")
        for k, v in st_data.items():
            if k != 'n' and isinstance(v, dict):
                print(f"    {k}: r = {v['r']:.3f}")
    
    print("\n" + "-" * 50)
    print("INDEPENDENCE:")
    assess = correlations['independence_tests']['independence_assessment']
    print(f"  Max |r|: {assess['max_correlation']:.3f}")
    print(f"  {assess['interpretation']}")
    
    print("\n" + "=" * 70)
    print("VALIDATION COMPLETE")
    print("=" * 70)
    
    return analyzer, components, correlations


if __name__ == "__main__":
    run_synthetic_validation()
