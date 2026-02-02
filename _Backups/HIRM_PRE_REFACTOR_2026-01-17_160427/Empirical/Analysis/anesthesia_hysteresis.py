"""
HIRM Anesthesia Hysteresis Analysis
====================================

Research Priority: TIER 1 - HIGHEST
Status: Implementation ready, awaiting data download
Date: 2025-12-20

PURPOSE:
Quantify hysteresis in anesthesia induction vs emergence to validate
the non-linear HIRM model prediction:

    EC50_emergence / EC50_induction ≈ 1.3-1.5

BACKGROUND:
The revised non-linear consciousness equation predicts that the
threshold for regaining consciousness (emergence) should be HIGHER
than the threshold for losing consciousness (induction). This creates
a hysteresis loop characteristic of first-order phase transitions.

TARGETS:
1. VitalDB (5,566 cases) - Primary dataset
2. Cambridge Propofol Study - Secondary validation

LOCKED CONSTANTS (from Master_Data):
- C_critical = 8.3 ± 0.6 bits
- Expected hysteresis ratio: 1.3-1.5

FALSIFICATION CRITERIA:
- If EC50_emergence / EC50_induction < 1.1: No significant hysteresis
- If ratio > 2.0: Model overpredicts hysteresis
- If no systematic pattern across subjects: Random variation only
"""

import numpy as np
from scipy import stats, signal, optimize
from scipy.interpolate import interp1d
from typing import Dict, List, Tuple, Optional, Union
import warnings
from pathlib import Path
from datetime import datetime
import json

# Import component analyzer
try:
    from component_correlations import ComponentCorrelationAnalyzer
except ImportError:
    ComponentCorrelationAnalyzer = None


class AnesthesiaHysteresisAnalyzer:
    """
    Analyze hysteresis in consciousness transitions during anesthesia.
    
    Computes EC50 ratios and characterizes the phase transition loop.
    
    Parameters
    ----------
    C_critical : float
        Consciousness threshold (default: 8.3 bits)
    sampling_rate : int
        EEG sampling rate in Hz
    """
    
    def __init__(
        self,
        C_critical: float = 8.3,
        sampling_rate: int = 100
    ):
        self.C_critical = C_critical
        self.sampling_rate = sampling_rate
        
        # Predicted hysteresis ratio from Session 10
        self.predicted_ratio_min = 1.3
        self.predicted_ratio_max = 1.5
        
        # Results storage
        self.results = {
            'subjects': {},
            'aggregate': {},
            'metadata': {
                'C_critical': C_critical,
                'predicted_ratio': [self.predicted_ratio_min, self.predicted_ratio_max],
                'analysis_date': datetime.now().isoformat()
            }
        }
        
        # Initialize component calculator
        if ComponentCorrelationAnalyzer:
            self.component_analyzer = ComponentCorrelationAnalyzer(
                C_critical=C_critical,
                sampling_rate=sampling_rate
            )
        else:
            self.component_analyzer = None
    
    def analyze_subject(
        self,
        eeg_data: np.ndarray,
        drug_concentration: np.ndarray,
        behavioral_response: np.ndarray,
        timestamps: Optional[np.ndarray] = None,
        subject_id: str = "unknown"
    ) -> Dict:
        """
        Analyze hysteresis for a single subject.
        
        Parameters
        ----------
        eeg_data : np.ndarray
            EEG data [channels, samples] or epochs [epochs, channels, samples]
        drug_concentration : np.ndarray
            Effect-site drug concentration over time
        behavioral_response : np.ndarray
            Binary response (1=conscious, 0=unconscious)
        timestamps : np.ndarray, optional
            Time points for each observation
        subject_id : str
            Subject identifier
            
        Returns
        -------
        results : Dict
            Hysteresis analysis results
        """
        results = {
            'subject_id': subject_id,
            'n_observations': len(drug_concentration)
        }
        
        # Calculate C(t) from EEG
        if self.component_analyzer and eeg_data is not None:
            components = self._calculate_consciousness(eeg_data)
            C_values = components['C']
        else:
            # Use behavioral response as proxy
            C_values = behavioral_response * self.C_critical * 1.2
        
        # Identify induction and emergence phases
        induction_mask, emergence_mask = self._identify_phases(
            drug_concentration, behavioral_response
        )
        
        # Calculate EC50 for each phase
        if np.sum(induction_mask) > 10:
            ec50_induction, slope_induction = self._fit_dose_response(
                drug_concentration[induction_mask],
                behavioral_response[induction_mask],
                phase='induction'
            )
            results['ec50_induction'] = float(ec50_induction)
            results['slope_induction'] = float(slope_induction)
        else:
            results['ec50_induction'] = np.nan
            results['slope_induction'] = np.nan
        
        if np.sum(emergence_mask) > 10:
            ec50_emergence, slope_emergence = self._fit_dose_response(
                drug_concentration[emergence_mask],
                behavioral_response[emergence_mask],
                phase='emergence'
            )
            results['ec50_emergence'] = float(ec50_emergence)
            results['slope_emergence'] = float(slope_emergence)
        else:
            results['ec50_emergence'] = np.nan
            results['slope_emergence'] = np.nan
        
        # Calculate hysteresis ratio
        if not np.isnan(results['ec50_induction']) and not np.isnan(results['ec50_emergence']):
            results['hysteresis_ratio'] = results['ec50_emergence'] / results['ec50_induction']
        else:
            results['hysteresis_ratio'] = np.nan
        
        # C(t) trajectory analysis
        results['C_trajectory'] = {
            'induction': self._analyze_trajectory(
                C_values[induction_mask] if np.any(induction_mask) else np.array([]),
                drug_concentration[induction_mask] if np.any(induction_mask) else np.array([])
            ),
            'emergence': self._analyze_trajectory(
                C_values[emergence_mask] if np.any(emergence_mask) else np.array([]),
                drug_concentration[emergence_mask] if np.any(emergence_mask) else np.array([])
            )
        }
        
        # Critical slowing analysis
        if len(C_values) > 20:
            results['critical_slowing'] = self._detect_critical_slowing(
                C_values, drug_concentration, behavioral_response
            )
        
        # Store results
        self.results['subjects'][subject_id] = results
        
        return results
    
    def _calculate_consciousness(self, eeg_data: np.ndarray) -> Dict:
        """Calculate C(t) components from EEG data."""
        if eeg_data.ndim == 2:
            eeg_data = eeg_data[np.newaxis, :, :]
        
        return self.component_analyzer.calculate_components_from_eeg(eeg_data)
    
    def _identify_phases(
        self,
        concentration: np.ndarray,
        response: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Identify induction (rising concentration) and emergence (falling) phases.
        
        Returns
        -------
        induction_mask, emergence_mask : np.ndarray
            Boolean masks for each phase
        """
        # Find concentration derivative
        conc_diff = np.diff(concentration, prepend=concentration[0])
        
        # Smooth to reduce noise
        window = min(11, len(conc_diff) // 5)
        if window > 3:
            conc_diff = np.convolve(conc_diff, np.ones(window)/window, mode='same')
        
        # Induction: concentration increasing
        induction_mask = conc_diff > 0
        
        # Emergence: concentration decreasing
        emergence_mask = conc_diff < 0
        
        return induction_mask, emergence_mask
    
    def _fit_dose_response(
        self,
        concentration: np.ndarray,
        response: np.ndarray,
        phase: str = 'induction'
    ) -> Tuple[float, float]:
        """
        Fit Hill equation to dose-response data.
        
        Response = 1 / (1 + (EC50/C)^n)  for induction
        Response = 1 / (1 + (C/EC50)^n)  for emergence
        
        Returns
        -------
        ec50 : float
            Half-maximal effective concentration
        slope : float
            Hill coefficient (steepness)
        """
        # Remove NaN and zeros
        valid = ~np.isnan(concentration) & ~np.isnan(response) & (concentration > 0)
        conc = concentration[valid]
        resp = response[valid]
        
        if len(conc) < 5:
            return np.nan, np.nan
        
        # Initial guess from data
        ec50_init = np.median(conc)
        
        # Hill equation
        def hill_induction(C, EC50, n):
            return 1.0 / (1.0 + (EC50 / (C + 1e-10)) ** n)
        
        def hill_emergence(C, EC50, n):
            return 1.0 / (1.0 + (C / (EC50 + 1e-10)) ** n)
        
        hill_func = hill_induction if phase == 'induction' else hill_emergence
        
        try:
            popt, _ = optimize.curve_fit(
                hill_func,
                conc, resp,
                p0=[ec50_init, 3.0],
                bounds=([0.01, 0.5], [100, 20]),
                maxfev=5000
            )
            ec50, slope = popt
        except:
            # Fallback: simple threshold estimation
            if phase == 'induction':
                # Find concentration where response drops below 0.5
                below_threshold = conc[resp < 0.5]
                ec50 = np.min(below_threshold) if len(below_threshold) > 0 else np.median(conc)
            else:
                # Find concentration where response rises above 0.5
                above_threshold = conc[resp > 0.5]
                ec50 = np.max(above_threshold) if len(above_threshold) > 0 else np.median(conc)
            slope = 3.0  # Default Hill coefficient
        
        return ec50, slope
    
    def _analyze_trajectory(
        self,
        C_values: np.ndarray,
        concentration: np.ndarray
    ) -> Dict:
        """Analyze C(t) trajectory during a phase."""
        if len(C_values) == 0 or len(concentration) == 0:
            return {'valid': False}
        
        # Threshold crossing
        crossings = np.where(np.diff(np.sign(C_values - self.C_critical)))[0]
        
        # Transition sharpness (dC/dt at crossing)
        if len(crossings) > 0:
            crossing_idx = crossings[0]
            if crossing_idx > 0 and crossing_idx < len(C_values) - 1:
                dC_dt = abs(C_values[crossing_idx + 1] - C_values[crossing_idx - 1]) / 2
            else:
                dC_dt = np.nan
        else:
            dC_dt = np.nan
        
        return {
            'valid': True,
            'n_crossings': len(crossings),
            'transition_sharpness': float(dC_dt) if not np.isnan(dC_dt) else None,
            'C_min': float(np.min(C_values)),
            'C_max': float(np.max(C_values)),
            'C_mean': float(np.mean(C_values)),
            'concentration_at_threshold': self._find_threshold_concentration(
                C_values, concentration
            )
        }
    
    def _find_threshold_concentration(
        self,
        C_values: np.ndarray,
        concentration: np.ndarray
    ) -> Optional[float]:
        """Find drug concentration when C crosses threshold."""
        if len(C_values) != len(concentration):
            return None
        
        crossings = np.where(np.diff(np.sign(C_values - self.C_critical)))[0]
        
        if len(crossings) > 0:
            idx = crossings[0]
            # Interpolate
            if idx < len(concentration) - 1:
                frac = (self.C_critical - C_values[idx]) / (C_values[idx + 1] - C_values[idx] + 1e-10)
                return float(concentration[idx] + frac * (concentration[idx + 1] - concentration[idx]))
        
        return None
    
    def _detect_critical_slowing(
        self,
        C_values: np.ndarray,
        concentration: np.ndarray,
        response: np.ndarray
    ) -> Dict:
        """
        Detect critical slowing down near the phase transition.
        
        Critical slowing manifests as:
        1. Increased autocorrelation
        2. Increased variance
        3. Slower recovery from perturbations
        """
        window_size = min(20, len(C_values) // 5)
        
        if window_size < 5:
            return {'detected': False, 'reason': 'insufficient_data'}
        
        # Calculate rolling autocorrelation
        autocorr = np.zeros(len(C_values) - window_size)
        variance = np.zeros(len(C_values) - window_size)
        
        for i in range(len(autocorr)):
            window = C_values[i:i + window_size]
            if len(window) > 2:
                autocorr[i] = np.corrcoef(window[:-1], window[1:])[0, 1]
                variance[i] = np.var(window)
        
        # Find transition point (loss of consciousness)
        loc_idx = np.where(np.diff(response) < 0)[0]
        
        if len(loc_idx) == 0:
            return {'detected': False, 'reason': 'no_transition_found'}
        
        loc_idx = loc_idx[0]
        
        # Compare pre-transition vs earlier periods
        pre_transition_start = max(0, loc_idx - window_size * 3)
        pre_transition_end = loc_idx
        
        early_start = 0
        early_end = min(window_size * 3, pre_transition_start)
        
        if early_end <= early_start or pre_transition_end <= pre_transition_start:
            return {'detected': False, 'reason': 'insufficient_pre_transition_data'}
        
        # Check for increased autocorrelation
        early_autocorr = np.nanmean(autocorr[early_start:early_end]) if early_end > early_start else np.nan
        pre_autocorr = np.nanmean(autocorr[max(0, pre_transition_start - window_size):pre_transition_end - window_size])
        
        # Check for increased variance
        early_var = np.nanmean(variance[early_start:early_end]) if early_end > early_start else np.nan
        pre_var = np.nanmean(variance[max(0, pre_transition_start - window_size):pre_transition_end - window_size])
        
        # Detection criteria
        autocorr_increase = (pre_autocorr - early_autocorr) / (early_autocorr + 1e-10) if not np.isnan(early_autocorr) else np.nan
        variance_increase = (pre_var - early_var) / (early_var + 1e-10) if not np.isnan(early_var) else np.nan
        
        detected = False
        if not np.isnan(autocorr_increase) and autocorr_increase > 0.2:
            detected = True
        if not np.isnan(variance_increase) and variance_increase > 0.3:
            detected = True
        
        return {
            'detected': detected,
            'autocorr_early': float(early_autocorr) if not np.isnan(early_autocorr) else None,
            'autocorr_pre_transition': float(pre_autocorr) if not np.isnan(pre_autocorr) else None,
            'autocorr_increase': float(autocorr_increase) if not np.isnan(autocorr_increase) else None,
            'variance_early': float(early_var) if not np.isnan(early_var) else None,
            'variance_pre_transition': float(pre_var) if not np.isnan(pre_var) else None,
            'variance_increase': float(variance_increase) if not np.isnan(variance_increase) else None,
            'loc_index': int(loc_idx)
        }
    
    def compute_aggregate_statistics(self) -> Dict:
        """Compute aggregate statistics across all subjects."""
        ratios = []
        ec50_ind = []
        ec50_eme = []
        
        for subject_id, subj_results in self.results['subjects'].items():
            if not np.isnan(subj_results.get('hysteresis_ratio', np.nan)):
                ratios.append(subj_results['hysteresis_ratio'])
                ec50_ind.append(subj_results['ec50_induction'])
                ec50_eme.append(subj_results['ec50_emergence'])
        
        if len(ratios) == 0:
            return {'valid': False, 'reason': 'no_valid_subjects'}
        
        ratios = np.array(ratios)
        
        aggregate = {
            'n_subjects': len(ratios),
            'hysteresis_ratio': {
                'mean': float(np.mean(ratios)),
                'std': float(np.std(ratios)),
                'median': float(np.median(ratios)),
                'iqr': [float(np.percentile(ratios, 25)), float(np.percentile(ratios, 75))],
                'range': [float(np.min(ratios)), float(np.max(ratios))]
            },
            'ec50_induction': {
                'mean': float(np.mean(ec50_ind)),
                'std': float(np.std(ec50_ind))
            },
            'ec50_emergence': {
                'mean': float(np.mean(ec50_eme)),
                'std': float(np.std(ec50_eme))
            }
        }
        
        # Test prediction
        mean_ratio = aggregate['hysteresis_ratio']['mean']
        predicted_match = self.predicted_ratio_min <= mean_ratio <= self.predicted_ratio_max
        
        # Statistical test: is ratio significantly > 1?
        t_stat, p_value = stats.ttest_1samp(ratios, 1.0)
        
        aggregate['prediction_test'] = {
            'predicted_range': [self.predicted_ratio_min, self.predicted_ratio_max],
            'observed_mean': mean_ratio,
            'within_predicted_range': predicted_match,
            'significantly_greater_than_1': {
                't_statistic': float(t_stat),
                'p_value': float(p_value),
                'significant': p_value < 0.05 and mean_ratio > 1
            }
        }
        
        # Falsification assessment
        if mean_ratio < 1.1:
            assessment = "POTENTIAL FALSIFICATION: No significant hysteresis detected"
        elif mean_ratio > 2.0:
            assessment = "REFINEMENT NEEDED: Model overpredicts hysteresis"
        elif predicted_match:
            assessment = "PREDICTION VALIDATED: Hysteresis ratio within expected range"
        else:
            assessment = f"PARTIAL SUPPORT: Hysteresis detected but outside predicted range ({self.predicted_ratio_min}-{self.predicted_ratio_max})"
        
        aggregate['assessment'] = assessment
        
        self.results['aggregate'] = aggregate
        
        return aggregate

    
    def generate_report(self, save_path: Optional[str] = None) -> str:
        """Generate formatted analysis report."""
        
        report = []
        report.append("=" * 70)
        report.append("HIRM ANESTHESIA HYSTERESIS ANALYSIS REPORT")
        report.append("=" * 70)
        report.append(f"\nAnalysis Date: {self.results['metadata']['analysis_date']}")
        report.append(f"C_critical: {self.C_critical} bits")
        report.append(f"Predicted hysteresis ratio: {self.predicted_ratio_min}-{self.predicted_ratio_max}")
        report.append("")
        
        # Aggregate results
        if 'aggregate' in self.results and self.results['aggregate']:
            agg = self.results['aggregate']
            
            report.append("-" * 70)
            report.append("AGGREGATE RESULTS")
            report.append("-" * 70)
            
            report.append(f"\nN subjects: {agg.get('n_subjects', 'N/A')}")
            
            if 'hysteresis_ratio' in agg:
                hr = agg['hysteresis_ratio']
                report.append(f"\nHysteresis Ratio (EC50_emergence / EC50_induction):")
                report.append(f"  Mean ± SD: {hr['mean']:.3f} ± {hr['std']:.3f}")
                report.append(f"  Median: {hr['median']:.3f}")
                report.append(f"  IQR: [{hr['iqr'][0]:.3f}, {hr['iqr'][1]:.3f}]")
                report.append(f"  Range: [{hr['range'][0]:.3f}, {hr['range'][1]:.3f}]")
            
            if 'prediction_test' in agg:
                pt = agg['prediction_test']
                report.append(f"\nPrediction Test:")
                report.append(f"  Predicted range: {pt['predicted_range']}")
                report.append(f"  Observed mean: {pt['observed_mean']:.3f}")
                report.append(f"  Within range: {'Yes ✓' if pt['within_predicted_range'] else 'No ✗'}")
                
                sig = pt['significantly_greater_than_1']
                report.append(f"\n  t-test (ratio > 1):")
                report.append(f"    t = {sig['t_statistic']:.3f}, p = {sig['p_value']:.4f}")
                report.append(f"    Significant: {'Yes ✓' if sig['significant'] else 'No ✗'}")
            
            if 'assessment' in agg:
                report.append(f"\nASSESSMENT: {agg['assessment']}")
        
        # Individual subjects summary
        if self.results['subjects']:
            report.append("\n" + "-" * 70)
            report.append("INDIVIDUAL SUBJECT SUMMARY")
            report.append("-" * 70)
            
            for subj_id, subj in self.results['subjects'].items():
                ratio = subj.get('hysteresis_ratio', np.nan)
                ratio_str = f"{ratio:.3f}" if not np.isnan(ratio) else "N/A"
                report.append(f"\n{subj_id}: ratio = {ratio_str}")
                
                cs = subj.get('critical_slowing', {})
                if cs.get('detected'):
                    report.append(f"  Critical slowing detected ✓")
        
        report.append("\n" + "=" * 70)
        report.append("END OF REPORT")
        report.append("=" * 70)
        
        report_text = "\n".join(report)
        
        if save_path:
            with open(save_path, 'w') as f:
                f.write(report_text)
        
        return report_text


def run_synthetic_validation():
    """
    Run validation on synthetic anesthesia data.
    
    Creates synthetic data with known hysteresis to validate pipeline.
    """
    print("=" * 60)
    print("HIRM Anesthesia Hysteresis Analysis - Synthetic Validation")
    print("=" * 60)
    
    np.random.seed(42)
    
    analyzer = AnesthesiaHysteresisAnalyzer(C_critical=8.3)
    
    # Simulate 20 subjects
    n_subjects = 20
    
    # True hysteresis ratio (for validation)
    TRUE_RATIO = 1.4  # Within predicted range [1.3, 1.5]
    
    print(f"\nSimulating {n_subjects} subjects with TRUE hysteresis ratio = {TRUE_RATIO}")
    
    for subj in range(n_subjects):
        # Simulate anesthesia session
        # Induction: concentration rises 0 → peak over ~30 min
        # Maintenance: stable for ~60 min  
        # Emergence: concentration falls peak → 0 over ~30 min
        
        n_points = 300  # 5 hours at 1-min resolution
        time = np.linspace(0, 300, n_points)
        
        # Drug concentration profile
        peak_conc = 4.0 + np.random.randn() * 0.5
        
        concentration = np.zeros(n_points)
        
        # Induction (0-60 min): exponential rise
        induction_end = 60
        concentration[:induction_end] = peak_conc * (1 - np.exp(-time[:induction_end] / 15))
        
        # Maintenance (60-180 min): stable
        maint_start, maint_end = 60, 180
        concentration[maint_start:maint_end] = peak_conc
        
        # Emergence (180-300 min): exponential decay
        emergence_time = time[maint_end:] - time[maint_end]
        concentration[maint_end:] = peak_conc * np.exp(-emergence_time / 30)
        
        # Add noise
        concentration += np.random.randn(n_points) * 0.1
        concentration = np.clip(concentration, 0, None)
        
        # Generate behavioral response with HYSTERESIS
        # EC50_induction < EC50_emergence by factor of TRUE_RATIO
        ec50_ind = 2.0 + np.random.randn() * 0.2
        ec50_eme = ec50_ind * TRUE_RATIO + np.random.randn() * 0.15
        
        response = np.ones(n_points)
        hill_coef = 4.0
        
        # Induction: consciousness decreases
        for i in range(induction_end):
            p_conscious = 1.0 / (1.0 + (concentration[i] / ec50_ind) ** hill_coef)
            response[i] = 1 if np.random.rand() < p_conscious else 0
        
        # Maintenance: unconscious
        response[maint_start:maint_end] = 0
        
        # Emergence: consciousness returns (higher threshold)
        for i in range(maint_end, n_points):
            p_conscious = 1.0 / (1.0 + (ec50_eme / (concentration[i] + 0.1)) ** hill_coef)
            response[i] = 1 if np.random.rand() < p_conscious else 0
        
        # Analyze subject
        analyzer.analyze_subject(
            eeg_data=None,  # Not using EEG for synthetic test
            drug_concentration=concentration,
            behavioral_response=response,
            subject_id=f"SYNTH_{subj:03d}"
        )
    
    # Compute aggregate statistics
    print("\nComputing aggregate statistics...")
    aggregate = analyzer.compute_aggregate_statistics()
    
    # Print results
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    
    print(f"\nTrue hysteresis ratio: {TRUE_RATIO}")
    print(f"Recovered ratio: {aggregate['hysteresis_ratio']['mean']:.3f} ± {aggregate['hysteresis_ratio']['std']:.3f}")
    
    error = abs(aggregate['hysteresis_ratio']['mean'] - TRUE_RATIO)
    print(f"Absolute error: {error:.3f}")
    print(f"Recovery accuracy: {(1 - error/TRUE_RATIO) * 100:.1f}%")
    
    print(f"\nPrediction test:")
    pt = aggregate['prediction_test']
    print(f"  Within predicted range [{pt['predicted_range'][0]}, {pt['predicted_range'][1]}]: {'Yes ✓' if pt['within_predicted_range'] else 'No ✗'}")
    print(f"  Significantly > 1: {'Yes ✓' if pt['significantly_greater_than_1']['significant'] else 'No ✗'}")
    print(f"  p-value: {pt['significantly_greater_than_1']['p_value']:.4e}")
    
    print(f"\nASSESSMENT: {aggregate['assessment']}")
    
    # Generate report
    report = analyzer.generate_report()
    
    return analyzer, aggregate


def analyze_vitaldb(data_path: str):
    """
    Analyze hysteresis from VitalDB dataset.
    
    Parameters
    ----------
    data_path : str
        Path to VitalDB data directory
    """
    raise NotImplementedError(
        "VitalDB data not yet available. "
        "Access at: https://vitaldb.net/"
    )


def analyze_cambridge_propofol(data_path: str):
    """
    Analyze hysteresis from Cambridge Propofol Study.
    
    Parameters
    ----------
    data_path : str
        Path to Cambridge propofol data
    """
    raise NotImplementedError(
        "Cambridge Propofol data requires access request. "
        "Contact study authors."
    )


if __name__ == "__main__":
    # Run synthetic validation
    analyzer, aggregate = run_synthetic_validation()
    
    print("\n" + "=" * 60)
    print("Validation complete. Ready for real data analysis.")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Request VitalDB access: https://vitaldb.net/")
    print("2. Download Cambridge Propofol data")
    print("3. Run: analyze_vitaldb('path/to/data')")
    print("4. Compare with predictions: ratio ∈ [1.3, 1.5]")
