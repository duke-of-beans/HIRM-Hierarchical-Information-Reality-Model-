"""Quick test for consciousness_measure_fixed.py"""
import sys
sys.path.insert(0, r'D:\HIRM\Code\Core')

import numpy as np

print("Importing module...")
from consciousness_measure_fixed import ConsciousnessMeasure, validate_installation

print("Running validation...")
result = validate_installation()

print(f"\nFinal check - all components non-zero: Phi={result['Phi']:.3f}, R={result['R']:.3f}, D={result['D']:.3f}")
print("SUCCESS" if result['C'] > 0 and result['Phi'] > 0 and result['R'] > 0 and result['D'] > 0 else "FAILURE")
