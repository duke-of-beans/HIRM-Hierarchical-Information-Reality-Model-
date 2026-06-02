"""Unbuffered runner for recalibration."""
import sys, os
sys.stdout = open(r'D:\Projects\HIRM\run3.log', 'w', buffering=1)  # line-buffered
sys.stderr = sys.stdout
os.chdir(r'D:\Projects\HIRM\Empirical\Analysis')
sys.path.insert(0, r'D:\Projects\HIRM\Code\Core')
exec(open('run_validation_now.py').read())
