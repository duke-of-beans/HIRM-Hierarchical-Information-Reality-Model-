import sys
print(f"Python {sys.version}")
for mod in ['mne', 'scipy', 'matplotlib', 'numpy', 'pandas']:
    try:
        m = __import__(mod)
        print(f"  {mod}: {m.__version__}")
    except ImportError:
        print(f"  {mod}: NOT INSTALLED")
