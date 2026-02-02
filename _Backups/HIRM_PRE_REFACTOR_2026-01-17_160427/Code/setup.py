"""
Setup configuration for the HIRM (Hierarchical Information-Reality Model) package.
"""

from setuptools import setup, find_packages
import os

# Read README for long description
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hirm',
    version='0.2.0',
    author='HIRM Research Team',
    author_email='research@hirm-consciousness.org',
    description='Computational toolkit for consciousness phase transitions at critical brain dynamics',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ouroboros-observer/toolkit',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Physics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
    install_requires=[
        'numpy>=1.20',
        'scipy>=1.7',
        'matplotlib>=3.3',
        'seaborn>=0.11',
        'networkx>=2.6',
        'scikit-learn>=0.24',
        'tqdm>=4.60',
    ],
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.12',
            'jupyter>=1.0',
            'sphinx>=4.0',
            'sphinx-rtd-theme>=0.5',
        ],
        'gpu': [
            'cupy>=9.0',  # Optional GPU acceleration
        ],
    },
    entry_points={
        'console_scripts': [
            'hirm-validate=hirm.validation:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
