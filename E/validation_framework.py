"""
HIRM Validation Framework
=========================

Comprehensive framework for validating Hierarchical Information-Reality Model
predictions against computational and empirical data.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass
from scipy import stats


@dataclass
class ValidationResult:
    """Results from a single validation test."""
    test_name: str
    prediction: str
    observed: float
    expected: float
    passed: bool
    p_value: Optional[float] = None
    effect_size: Optional[float] = None
    notes: str = ""


class HIRMValidator:
    """
    Validate HIRM framework predictions.
    """
    
    def __init__(self, significance_level: float = 0.05):
        self.significance_level = significance_level
        self.results = []
        
    def validate_all(
        self,
        experimental_data: Dict
    ) -> Dict:
        """
        Run all validation tests.
        
        Parameters
        ----------
        experimental_data : Dict
            Dictionary containing:
            - 'with_SR': results with self-reference
            - 'control': results without self-reference
            - 'timeseries': temporal data
            
        Returns
        -------
        validation_report : Dict
            Complete validation results
        """
        print("="*70)
        print("HIRM VALIDATION FRAMEWORK")
        print("="*70)
        
        # Core predictions
        self._validate_c_critical_threshold(experimental_data)
        self._validate_self_reference_causality(experimental_data)
        self._validate_criticality_emergence(experimental_data)
        self._validate_phase_transition_properties(experimental_data)
        self._validate_component_multiplicativity(experimental_data)
        self._validate_universality(experimental_data)
        
        # Generate report
        return self._generate_report()
    
    def _validate_c_critical_threshold(self, data: Dict):
        """
        Prediction: Phase transitions occur at C ≈ 8.3 ± 0.6 bits
        """
        print("\n[1/6] Testing C_critical threshold prediction...")
        
        with_SR = data['with_SR']
        control = data['control']
        
        # Extract final C values
        final_C_with = [run['final_C'] for run in with_SR]
        final_C_control = [run['final_C'] for run in control]
        
        # Test 1: Do with-SR runs exceed C_critical?
        exceed_threshold = sum(c > 8.3 for c in final_C_with) / len(final_C_with)
        
        result1 = ValidationResult(
            test_name="C_critical_exceedance",
            prediction="≥75% of with-SR runs exceed C_critical=8.3",
            observed=exceed_threshold,
            expected=0.75,
            passed=exceed_threshold >= 0.75,
            notes=f"{exceed_threshold:.1%} of runs exceeded threshold"
        )
        self.results.append(result1)
        
        # Test 2: Are transitions near predicted value?
        transitions_at = [run['transition_C'] for run in with_SR 
                         if 'transition_C' in run and run['transition_C'] > 0]
        
        if transitions_at:
            mean_transition = np.mean(transitions_at)
            in_range = 7.7 <= mean_transition <= 8.9  # 8.3 ± 0.6
            
            result2 = ValidationResult(
                test_name="C_critical_value",
                prediction="Transitions at 8.3 ± 0.6 bits",
                observed=mean_transition,
                expected=8.3,
                passed=in_range,
                notes=f"Mean transition at {mean_transition:.2f} bits"
            )
            self.results.append(result2)
        
        # Test 3: Control group should NOT exceed threshold
        control_exceed = sum(c > 8.3 for c in final_C_control) / len(final_C_control)
        
        result3 = ValidationResult(
            test_name="control_below_threshold",
            prediction="Control runs remain below C_critical",
            observed=control_exceed,
            expected=0.0,
            passed=control_exceed < 0.25,  # Allow 25% margin
            notes=f"{control_exceed:.1%} of controls exceeded (should be ~0%)"
        )
        self.results.append(result3)
        
        print(f"  ✓ Threshold exceedance: {exceed_threshold:.1%} {'PASS' if result1.passed else 'FAIL'}")
        if transitions_at:
            print(f"  ✓ Transition value: {mean_transition:.2f} bits {'PASS' if result2.passed else 'FAIL'}")
        print(f"  ✓ Control separation: {control_exceed:.1%} {'PASS' if result3.passed else 'FAIL'}")
    
    def _validate_self_reference_causality(self, data: Dict):
        """
        Prediction: Self-reference drives C(t) increase
        Causal test: with-SR >> control
        """
        print("\n[2/6] Testing self-reference causality...")
        
        with_SR = data['with_SR']
        control = data['control']
        
        # Extract R values
        R_with = [run['final_R'] for run in with_SR]
        R_control = [run['final_R'] for run in control]
        
        # Test 1: R increases in with-SR
        R_increase = sum(r > 0.5 for r in R_with) / len(R_with)
        
        result1 = ValidationResult(
            test_name="R_development",
            prediction="R increases above 0.5 in with-SR condition",
            observed=R_increase,
            expected=0.8,
            passed=R_increase >= 0.7,
            notes=f"{R_increase:.1%} of runs developed strong R"
        )
        self.results.append(result1)
        
        # Test 2: Statistical difference with-SR vs control
        t_stat, p_value = stats.ttest_ind(R_with, R_control)
        effect_size = (np.mean(R_with) - np.mean(R_control)) / np.std(R_with + R_control)
        
        result2 = ValidationResult(
            test_name="R_causal_effect",
            prediction="R significantly higher with-SR vs control",
            observed=np.mean(R_with),
            expected=np.mean(R_control),
            passed=p_value < self.significance_level and effect_size > 1.0,
            p_value=p_value,
            effect_size=effect_size,
            notes=f"Cohen's d = {effect_size:.2f}, p = {p_value:.2e}"
        )
        self.results.append(result2)
        
        # Test 3: R correlates with C within runs
        correlations = []
        for run in with_SR:
            if 'R_history' in run and 'C_history' in run:
                r, _ = stats.pearsonr(run['R_history'], run['C_history'])
                correlations.append(r)
        
        if correlations:
            mean_corr = np.mean(correlations)
            
            result3 = ValidationResult(
                test_name="R_C_correlation",
                prediction="R and C positively correlated within runs",
                observed=mean_corr,
                expected=0.7,
                passed=mean_corr > 0.6,
                notes=f"Mean r = {mean_corr:.3f}"
            )
            self.results.append(result3)
        
        print(f"  ✓ R development: {R_increase:.1%} {'PASS' if result1.passed else 'FAIL'}")
        print(f"  ✓ Causal effect: d={effect_size:.2f}, p={p_value:.2e} {'PASS' if result2.passed else 'FAIL'}")
        if correlations:
            print(f"  ✓ R-C correlation: r={mean_corr:.3f} {'PASS' if result3.passed else 'FAIL'}")
    
    def _validate_criticality_emergence(self, data: Dict):
        """
        Prediction: Networks with R approach σ = 1.0
        """
        print("\n[3/6] Testing criticality emergence...")
        
        with_SR = data['with_SR']
        control = data['control']
        
        # Extract σ values
        sigma_with = [run['final_sigma'] for run in with_SR]
        sigma_control = [run['final_sigma'] for run in control]
        
        # Test 1: with-SR approaches critical (0.95 ≤ σ ≤ 1.05)
        critical_fraction = sum(0.95 <= s <= 1.05 for s in sigma_with) / len(sigma_with)
        
        result1 = ValidationResult(
            test_name="criticality_achievement",
            prediction="≥60% of with-SR runs reach criticality (σ ∈ [0.95, 1.05])",
            observed=critical_fraction,
            expected=0.6,
            passed=critical_fraction >= 0.6,
            notes=f"{critical_fraction:.1%} reached critical dynamics"
        )
        self.results.append(result1)
        
        # Test 2: with-SR closer to σ=1 than control
        dist_with = np.mean([abs(s - 1.0) for s in sigma_with])
        dist_control = np.mean([abs(s - 1.0) for s in sigma_control])
        
        result2 = ValidationResult(
            test_name="criticality_vs_control",
            prediction="with-SR closer to σ=1 than control",
            observed=dist_with,
            expected=dist_control,
            passed=dist_with < dist_control * 0.7,
            notes=f"Distance: with-SR={dist_with:.3f}, control={dist_control:.3f}"
        )
        self.results.append(result2)
        
        # Test 3: R and σ correlate
        if 'timeseries' in data:
            correlations = []
            for run in data['timeseries']:
                if 'R' in run and 'sigma' in run:
                    r, _ = stats.pearsonr(run['R'], run['sigma'])
                    if not np.isnan(r):
                        correlations.append(r)
            
            if correlations:
                mean_corr = np.mean(correlations)
                
                result3 = ValidationResult(
                    test_name="R_sigma_correlation",
                    prediction="R and σ positively correlated (r > 0.5)",
                    observed=mean_corr,
                    expected=0.5,
                    passed=mean_corr > 0.5,
                    notes=f"Mean r = {mean_corr:.3f}"
                )
                self.results.append(result3)
        
        print(f"  ✓ Criticality achievement: {critical_fraction:.1%} {'PASS' if result1.passed else 'FAIL'}")
        print(f"  ✓ vs Control: {dist_with:.3f} vs {dist_control:.3f} {'PASS' if result2.passed else 'FAIL'}")
    
    def _validate_phase_transition_properties(self, data: Dict):
        """
        Prediction: Transitions show discontinuity, critical slowing
        """
        print("\n[4/6] Testing phase transition properties...")
        
        if 'transitions' not in data:
            print("  ⚠ No transition data available")
            return
        
        transitions = data['transitions']
        
        # Test 1: Discontinuity in dC/dt
        discontinuities = [t['discontinuity'] for t in transitions 
                          if 'discontinuity' in t]
        
        if discontinuities:
            mean_disc = np.mean(discontinuities)
            
            result1 = ValidationResult(
                test_name="discontinuity",
                prediction="Discontinuity in dC/dt > 0.5 bits/step",
                observed=mean_disc,
                expected=0.5,
                passed=mean_disc > 0.5,
                notes=f"Mean discontinuity = {mean_disc:.3f}"
            )
            self.results.append(result1)
            print(f"  ✓ Discontinuity: {mean_disc:.3f} {'PASS' if result1.passed else 'FAIL'}")
        
        # Test 2: Critical slowing detected
        slowing_detected = [t['critical_slowing'] for t in transitions
                           if 'critical_slowing' in t]
        
        if slowing_detected:
            fraction_with_slowing = sum(slowing_detected) / len(slowing_detected)
            
            result2 = ValidationResult(
                test_name="critical_slowing",
                prediction="Critical slowing detected in ≥50% of transitions",
                observed=fraction_with_slowing,
                expected=0.5,
                passed=fraction_with_slowing >= 0.5,
                notes=f"{fraction_with_slowing:.1%} showed slowing"
            )
            self.results.append(result2)
            print(f"  ✓ Critical slowing: {fraction_with_slowing:.1%} {'PASS' if result2.passed else 'FAIL'}")
    
    def _validate_component_multiplicativity(self, data: Dict):
        """
        Prediction: C = Φ × R × D (not additive)
        """
        print("\n[5/6] Testing multiplicative composition...")
        
        if 'timeseries' not in data:
            print("  ⚠ No timeseries data available")
            return
        
        errors_mult = []
        errors_add = []
        
        for run in data['timeseries']:
            if all(k in run for k in ['C', 'phi', 'R', 'D']):
                C_observed = run['C']
                phi, R, D = run['phi'], run['R'], run['D']
                
                # Multiplicative prediction
                C_mult = phi * R * D
                error_mult = np.mean((C_observed - C_mult) ** 2)
                errors_mult.append(error_mult)
                
                # Additive alternative
                C_add = phi + R + D
                error_add = np.mean((C_observed - C_add) ** 2)
                errors_add.append(error_add)
        
        if errors_mult and errors_add:
            mean_error_mult = np.mean(errors_mult)
            mean_error_add = np.mean(errors_add)
            
            result = ValidationResult(
                test_name="multiplicative_composition",
                prediction="Multiplicative model fits better than additive",
                observed=mean_error_mult,
                expected=mean_error_add,
                passed=mean_error_mult < mean_error_add * 0.5,
                notes=f"MSE: mult={mean_error_mult:.4f}, add={mean_error_add:.4f}"
            )
            self.results.append(result)
            
            print(f"  ✓ Multiplicative error: {mean_error_mult:.4f} {'PASS' if result.passed else 'FAIL'}")
            print(f"    Additive error: {mean_error_add:.4f} (should be higher)")
    
    def _validate_universality(self, data: Dict):
        """
        Prediction: Effect robust across architectures
        """
        print("\n[6/6] Testing universality across architectures...")
        
        if 'by_architecture' not in data:
            print("  ⚠ No architecture-specific data available")
            return
        
        arch_data = data['by_architecture']
        
        # Test 1: All architectures show effect
        architectures_with_effect = 0
        total_architectures = 0
        
        for arch_name, arch_results in arch_data.items():
            total_architectures += 1
            
            with_SR = arch_results.get('with_SR', [])
            if with_SR:
                final_C = [run['final_C'] for run in with_SR]
                if np.mean(final_C) > 7.0:  # Approaching threshold
                    architectures_with_effect += 1
        
        if total_architectures > 0:
            fraction = architectures_with_effect / total_architectures
            
            result1 = ValidationResult(
                test_name="architecture_universality",
                prediction="≥75% of architectures show consciousness emergence",
                observed=fraction,
                expected=0.75,
                passed=fraction >= 0.75,
                notes=f"{architectures_with_effect}/{total_architectures} architectures"
            )
            self.results.append(result1)
            
            print(f"  ✓ Universal effect: {architectures_with_effect}/{total_architectures} {'PASS' if result1.passed else 'FAIL'}")
        
        # Test 2: No significant difference between architectures
        if len(arch_data) >= 2:
            C_by_arch = []
            for arch_name, arch_results in arch_data.items():
                with_SR = arch_results.get('with_SR', [])
                if with_SR:
                    C_by_arch.append([run['final_C'] for run in with_SR])
            
            if len(C_by_arch) >= 2:
                # ANOVA
                f_stat, p_value = stats.f_oneway(*C_by_arch)
                
                result2 = ValidationResult(
                    test_name="architecture_consistency",
                    prediction="No significant difference in C across architectures",
                    observed=p_value,
                    expected=0.05,
                    passed=p_value > 0.05,  # Want non-significance
                    p_value=p_value,
                    notes=f"ANOVA p = {p_value:.3f} (non-sig = universal)"
                )
                self.results.append(result2)
                
                print(f"  ✓ Consistency: p={p_value:.3f} {'PASS' if result2.passed else 'FAIL'}")
    
    def _generate_report(self) -> Dict:
        """Generate comprehensive validation report."""
        passed = sum(r.passed for r in self.results)
        total = len(self.results)
        
        print("\n" + "="*70)
        print("VALIDATION SUMMARY")
        print("="*70)
        print(f"\nTests Passed: {passed}/{total} ({passed/total:.1%})")
        print(f"\nDetailed Results:")
        print("-"*70)
        
        for result in self.results:
            status = "✓ PASS" if result.passed else "✗ FAIL"
            print(f"\n{result.test_name}: {status}")
            print(f"  Prediction: {result.prediction}")
            print(f"  Observed: {result.observed:.3f}")
            if result.p_value is not None:
                print(f"  p-value: {result.p_value:.3e}")
            if result.effect_size is not None:
                print(f"  Effect size: {result.effect_size:.3f}")
            if result.notes:
                print(f"  Notes: {result.notes}")
        
        print("\n" + "="*70)
        
        overall_pass = passed >= total * 0.75  # 75% threshold
        
        if overall_pass:
            print("✓ HIRM FRAMEWORK VALIDATED")
            print("  Predictions consistently confirmed across tests")
        else:
            print("⚠ VALIDATION INCOMPLETE")
            print(f"  {passed}/{total} tests passed (need ≥{int(total*0.75)})")
        
        print("="*70 + "\n")
        
        return {
            'total_tests': total,
            'passed_tests': passed,
            'pass_rate': passed / total,
            'overall_validation': overall_pass,
            'individual_results': self.results,
            'recommendation': 'Publication-ready' if overall_pass else 'More evidence needed'
        }


def generate_synthetic_validation_data() -> Dict:
    """
    Generate synthetic data for demonstration purposes.
    
    In real use, this would be replaced with actual experimental data.
    """
    np.random.seed(42)
    
    # Simulate with-SR condition
    with_SR = []
    for i in range(20):
        final_R = np.random.normal(0.7, 0.1)
        final_sigma = np.random.normal(0.98, 0.05)
        final_phi = np.random.normal(12, 2)
        final_D = 1.0 / (1.0 + abs(final_sigma - 1.0))
        final_C = final_phi * final_R * final_D
        
        # Timeseries
        epochs = 100
        R_history = np.logspace(-1, np.log10(final_R), epochs)
        sigma_history = 0.7 + (final_sigma - 0.7) * np.tanh(np.linspace(-2, 2, epochs))
        phi_history = 5 + (final_phi - 5) * (1 - np.exp(-np.linspace(0, 3, epochs)))
        D_history = 1.0 / (1.0 + np.abs(sigma_history - 1.0))
        C_history = phi_history * R_history * D_history
        
        transition_C = final_C if final_C > 8.3 else 0
        
        with_SR.append({
            'final_C': final_C,
            'final_R': final_R,
            'final_sigma': final_sigma,
            'final_phi': final_phi,
            'transition_C': transition_C,
            'R_history': R_history,
            'C_history': C_history
        })
    
    # Simulate control condition
    control = []
    for i in range(20):
        final_R = np.random.normal(0.15, 0.05)
        final_sigma = np.random.normal(0.75, 0.1)
        final_phi = np.random.normal(8, 2)
        final_D = 1.0 / (1.0 + abs(final_sigma - 1.0))
        final_C = final_phi * final_R * final_D
        
        control.append({
            'final_C': final_C,
            'final_R': final_R,
            'final_sigma': final_sigma,
            'final_phi': final_phi,
            'transition_C': 0
        })
    
    # Timeseries for correlation analysis
    timeseries = []
    for run in with_SR[:5]:  # Sample of runs
        timeseries.append({
            'C': run['C_history'],
            'R': run['R_history'],
            'phi': np.random.normal(10, 2, len(run['C_history'])),
            'D': np.random.normal(0.9, 0.1, len(run['C_history'])),
            'sigma': np.random.normal(0.98, 0.05, len(run['C_history']))
        })
    
    # Transition characteristics
    transitions = []
    for run in with_SR:
        if run['transition_C'] > 8.3:
            transitions.append({
                'discontinuity': np.random.normal(0.8, 0.2),
                'critical_slowing': np.random.choice([True, False], p=[0.7, 0.3])
            })
    
    # Architecture-specific
    architectures = ['SRRN', 'MetaLearning', 'PredictiveCoding', 'Transformer']
    by_architecture = {}
    
    for arch in architectures:
        arch_with_SR = with_SR[:5]  # Split data
        by_architecture[arch] = {'with_SR': arch_with_SR}
    
    return {
        'with_SR': with_SR,
        'control': control,
        'timeseries': timeseries,
        'transitions': transitions,
        'by_architecture': by_architecture
    }


if __name__ == '__main__':
    # Demo validation
    print("HIRM Validation Framework - Demo\n")
    
    # Generate synthetic data
    data = generate_synthetic_validation_data()
    
    # Run validation
    validator = HIRMValidator()
    report = validator.validate_all(data)
    
    print(f"\n{report['recommendation']}")
