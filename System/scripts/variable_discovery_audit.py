#!/usr/bin/env python3
"""
Discovery Audit for R(t) and D(t) Variables
Extracts all definitions, uses, and operationalizations from HIRM corpus
Session 36 - Discovery-driven approach
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

class VariableDiscoveryAudit:
    """Extract what R and D actually ARE from the corpus"""
    
    def __init__(self, hirm_root: str):
        self.hirm_root = Path(hirm_root)
        self.findings = {
            'R': {'definitions': [], 'equations': [], 'ranges': [], 'units': [], 'implementations': []},
            'D': {'definitions': [], 'equations': [], 'ranges': [], 'units': [], 'implementations': []}
        }
        
    def search_patterns(self):
        """Define search patterns for R and D"""
        return {
            'R_definition': [
                r'R\(t\)\s*[=:]\s*(.+?)(?:\.|$)',
                r'self-reference.*?[=:]\s*(.+?)(?:\.|$)',
                r'R\s+represents?\s+(.+?)(?:\.|$)',
                r'recursion.*?defined.*?as\s+(.+?)(?:\.|$)',
            ],
            'D_definition': [
