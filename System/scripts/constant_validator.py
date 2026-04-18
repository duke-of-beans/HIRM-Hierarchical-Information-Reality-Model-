#!/usr/bin/env python3
"""
HIRM Locked Constants Validator
Scans entire corpus for violations of locked constants.
Triggered when Master_Data/Constants/locked_constants.md is modified.

Created: 2026-01-17
Version: 1.0
"""

import re
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

class ConstantValidator:
    """Validates locked constants across HIRM corpus"""
    
    def __init__(self, corpus_root: Path):
        self.corpus_root = corpus_root
        self.locked_constants = self.load_locked_constants()
        self.violations: List[Dict] = []
    
    def load_locked_constants(self) -> Dict[str, str]:
        """Read locked constants from source of truth"""
        constants_file = self.corpus_root / "Master_Data" / "Constants" / "locked_constants.md"
        constants = {}
        
        try:
            with open(constants_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Extract C_critical = 8.3 ± 0.6 bits
                if match := re.search(r"C_critical.*?\|\s*\*\*?([\d.]+\s*±\s*[\d.]+)\*\*?", content):
                    constants['C_critical'] = match.group(1)
                    print(f"[OK] Loaded C_critical = {constants['C_critical']}")
                
                # Extract core equation
                if match := re.search(r"C\(t\)\s*=\s*Φ\(t\)\s*×\s*R\(t\)\s*×\s*D\(t\)", content):
                    constants['core_equation'] = "C(t) = Φ(t) × R(t) × D(t)"
                    print(f"[OK] Loaded core equation")
                
        except FileNotFoundError:
            print(f"[FAIL] Could not find {constants_file}")
            return {}
        
        return constants
    
    def scan_file(self, file_path: Path) -> List[Dict]:
        """Scan single file for constant violations"""
        violations = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Check for C_critical violations
            if "C_critical" in content or "C critical" in content:
                expected = self.locked_constants.get('C_critical', '8.3 ± 0.6')
                
                # Look for C_critical with different values
                for match in re.finditer(r"C[_\s]critical\s*[=:]\s*([\d.]+(?:\s*±\s*[\d.]+)?)", content, re.IGNORECASE):
                    found_value = match.group(1)
                    
                    # Normalize for comparison
                    if not re.search(r"8\.3\s*±\s*0\.6", found_value):
                        violations.append({
                            'file': str(file_path.relative_to(self.corpus_root)),
                            'constant': 'C_critical',
                            'expected': expected,
                            'found': found_value,
                            'line_number': content[:match.start()].count('\n') + 1,
                            'context': self.extract_context(content, match.start())
                        })
            
            # Check for outdated values mentioned in locked_constants.md
            error_values = ['7.5', '10.0', '7.5 bits', '10 bits']
            for error_val in error_values:
                if error_val in content:
                    violations.append({
                        'file': str(file_path.relative_to(self.corpus_root)),
                        'constant': 'C_critical',
                        'expected': self.locked_constants.get('C_critical', '8.3 ± 0.6'),
                        'found': error_val,
                        'line_number': 0,
                        'context': f"Found outdated value: {error_val}"
                    })
        
        except Exception as e:
            print(f"[WARN] Error reading {file_path}: {e}")
        
        return violations
    
    def scan_corpus(self) -> List[Dict]:
        """Scan all markdown files in corpus"""
        print(f"\n[START] Scanning corpus at {self.corpus_root}")
        
        file_count = 0
        for md_file in self.corpus_root.rglob("*.md"):
            # Skip archived files
            if "_Archive" in str(md_file) or "_Backups" in str(md_file):
                continue
            
            file_count += 1
            violations = self.scan_file(md_file)
            self.violations.extend(violations)
        
        print(f"[OK] Scanned {file_count} files")
        print(f"[{'FAIL' if self.violations else 'OK'}] Found {len(self.violations)} violations")
        
        return self.violations
    
    def extract_context(self, content: str, position: int, chars: int = 100) -> str:
        """Extract text around a position for context"""
        start = max(0, position - chars)
        end = min(len(content), position + chars)
        context = content[start:end]
        
        # Clean up newlines for display
        context = context.replace('\n', ' ').strip()
        if start > 0:
            context = "..." + context
        if end < len(content):
            context = context + "..."
        
        return context
    
    def generate_report(self, output_path: Optional[Path] = None) -> str:
        """Generate violation report"""
        if not self.violations:
            report = "# Locked Constants Validation Report\n\n"
            report += f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            report += f"**Status:** ✅ ALL CONSTANTS VALIDATED SUCCESSFULLY\n\n"
            report += "No violations found. All documents use correct locked constant values.\n"
            return report
        
        report = [
            "# Locked Constants Validation Report",
            "",
            f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Status:** ❌ {len(self.violations)} VIOLATIONS FOUND",
            "",
            "## Summary",
            "",
            f"- Total violations: {len(self.violations)}",
            f"- Files affected: {len(set(v['file'] for v in self.violations))}",
            "",
            "## Violations by File",
            ""
        ]
        
        # Group by file
        by_file = {}
        for v in self.violations:
            file = v['file']
            if file not in by_file:
                by_file[file] = []
            by_file[file].append(v)
        
        for file, violations in sorted(by_file.items()):
            report.append(f"### {file}")
            report.append("")
            
            for v in violations:
                report.append(f"**Line {v['line_number']}:**")
                report.append(f"- Constant: `{v['constant']}`")
                report.append(f"- Expected: `{v['expected']}`")
                report.append(f"- Found: `{v['found']}`")
                report.append(f"- Context: {v['context']}")
                report.append("")
        
        report.append("## Recommended Actions")
        report.append("")
        report.append("1. Review each violation above")
        report.append("2. Update files to use correct values")
        report.append("3. Log corrections to Master_Data/Corrections/corrections_registry.md")
        report.append("4. Re-run validator to confirm fixes")
        report.append("")
        report.append("---")
        report.append("")
        report.append("**Generated by:** constant_validator.py v1.0")
        
        report_text = '\n'.join(report)
        
        # Save to file if path provided
        if output_path:
            output_path.write_text(report_text, encoding='utf-8')
            print(f"[OK] Report saved to {output_path}")
        
        return report_text
    
    def log_to_database(self, db_path: Path):
        """Log violations to corrections table in database"""
        if not self.violations:
            return
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            for v in self.violations:
                cursor.execute("""
                    INSERT INTO corrections (
                        correction_type, original_text, corrected_text,
                        source_session, reason, severity, recurrence_count
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    'constant_violation',
                    f"{v['constant']} = {v['found']}",
                    f"{v['constant']} = {v['expected']}",
                    'auto_validator',
                    f"Found in {v['file']}:{v['line_number']}",
                    'high',
                    1
                ))
            
            conn.commit()
            conn.close()
            print(f"[OK] Logged {len(self.violations)} violations to database")
        
        except Exception as e:
            print(f"[WARN] Could not log to database: {e}")

def main():
    """Main execution"""
    corpus_root = Path("D:/Research/HIRM")
    
    print("=" * 60)
    print("HIRM Locked Constants Validator v1.0")
    print("=" * 60)
    
    validator = ConstantValidator(corpus_root)
    violations = validator.scan_corpus()
    
    # Generate report
    report_path = corpus_root / "Logs" / f"constant_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    report = validator.generate_report(report_path)
    
    # Log to database
    db_path = corpus_root / "System" / "data" / "hirm.db"
    if db_path.exists():
        validator.log_to_database(db_path)
    
    # Print summary
    print("\n" + "=" * 60)
    if violations:
        print(f"[FAIL] Validation failed - {len(violations)} violations found")
        print(f"[INFO] See report: {report_path}")
        return 1
    else:
        print("[OK] Validation passed - all constants correct")
        return 0

if __name__ == "__main__":
    exit(main())
