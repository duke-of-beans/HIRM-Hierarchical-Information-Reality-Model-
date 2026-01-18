#!/usr/bin/env python3
"""
HIRM Terminology Enforcer
Scans corpus for forbidden terminology and auto-corrects violations.
Triggered when Master_Data/Terminology/terminology_reference.md is updated.

Created: 2026-01-17
Version: 1.0
"""

import re
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple

class TerminologyEnforcer:
    """Enforces HIRM terminology standards across corpus"""
    
    def __init__(self, corpus_root: Path):
        self.corpus_root = corpus_root
        self.forbidden_terms = self.load_forbidden_terms()
        self.violations: List[Dict] = []
        self.corrections_made: List[Dict] = []
    
    def load_forbidden_terms(self) -> Dict[str, str]:
        """Load forbidden → canonical term mappings"""
        terms_file = self.corpus_root / "Master_Data" / "Terminology" / "terminology_reference.md"
        forbidden = {}
        
        try:
            with open(terms_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Extract from LEGACY TERMINOLOGY MAPPING table
                # Format: | Ouroboros Observer | HIRM | ... |
                for match in re.finditer(
                    r'\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|[^|]*\|',
                    content
                ):
                    legacy_term = match.group(1).strip()
                    canonical_term = match.group(2).strip()
                    
                    # Skip table headers
                    if 'LEGACY' in legacy_term or 'NO' in legacy_term:
                        continue
                    
                    if legacy_term and canonical_term:
                        forbidden[legacy_term] = canonical_term
                
                # Also add common variations
                forbidden.update({
                    "Ouroboros Observer": "HIRM",
                    "Ouroboros Observer Theory": "HIRM",
                    "OO Theory": "HIRM",
                    "OO Framework": "HIRM Framework",
                    "The Observer Model": "HIRM",
                    "proves consciousness": "supports the hypothesis that consciousness",
                    "explains consciousness": "proposes a mechanism for consciousness",
                    "the theory is correct": "evidence supports the theory"
                })
                
                print(f"[OK] Loaded {len(forbidden)} forbidden terms")
        
        except FileNotFoundError:
            print(f"[FAIL] Could not find {terms_file}")
            # Fallback to minimal set
            forbidden = {
                "Ouroboros Observer": "HIRM",
                "OO Theory": "HIRM"
            }
        
        return forbidden
    
    def scan_file(self, file_path: Path) -> List[Dict]:
        """Scan single file for terminology violations"""
        violations = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            
            for forbidden, canonical in self.forbidden_terms.items():
                # Case-sensitive search for forbidden terms
                for match in re.finditer(re.escape(forbidden), content):
                    line_num = content[:match.start()].count('\n') + 1
                    
                    violations.append({
                        'file': str(file_path.relative_to(self.corpus_root)),
                        'forbidden': forbidden,
                        'canonical': canonical,
                        'line_number': line_num,
                        'position': match.start(),
                        'context': self.extract_context(content, match.start())
                    })
        
        except Exception as e:
            print(f"[WARN] Error reading {file_path}: {e}")
        
        return violations
    
    def scan_corpus(self) -> List[Dict]:
        """Scan all markdown files for terminology violations"""
        print(f"\n[START] Scanning corpus for terminology violations")
        
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
    
    def auto_correct(self, dry_run: bool = True) -> List[Dict]:
        """Automatically fix terminology violations"""
        print(f"\n[START] Auto-correct mode ({'DRY RUN' if dry_run else 'LIVE'})")
        
        corrections = []
        files_modified = set()
        
        for md_file in self.corpus_root.rglob("*.md"):
            # Skip archived files
            if "_Archive" in str(md_file) or "_Backups" in str(md_file):
                continue
            
            try:
                content = md_file.read_text(encoding='utf-8')
                original_content = content
                
                # Apply all replacements
                for forbidden, canonical in self.forbidden_terms.items():
                    if forbidden in content:
                        count = content.count(forbidden)
                        content = content.replace(forbidden, canonical)
                        
                        corrections.append({
                            'file': str(md_file.relative_to(self.corpus_root)),
                            'forbidden': forbidden,
                            'canonical': canonical,
                            'count': count
                        })
                        
                        files_modified.add(str(md_file))
                
                # Write back if modified and not dry run
                if content != original_content and not dry_run:
                    md_file.write_text(content, encoding='utf-8')
            
            except Exception as e:
                print(f"[WARN] Error processing {md_file}: {e}")
        
        self.corrections_made = corrections
        
        if dry_run:
            print(f"[DRY RUN] Would correct {len(corrections)} instances in {len(files_modified)} files")
        else:
            print(f"[OK] Corrected {len(corrections)} instances in {len(files_modified)} files")
        
        return corrections
    
    def extract_context(self, content: str, position: int, chars: int = 80) -> str:
        """Extract text around a position for context"""
        start = max(0, position - chars // 2)
        end = min(len(content), position + chars // 2)
        context = content[start:end]
        
        # Clean up for display
        context = context.replace('\n', ' ').strip()
        return f"...{context}..."
    
    def generate_report(self, output_path: Path = None) -> str:
        """Generate terminology enforcement report"""
        if not self.violations and not self.corrections_made:
            report = "# Terminology Enforcement Report\n\n"
            report += f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            report += f"**Status:** ✅ ALL TERMINOLOGY COMPLIANT\n\n"
            report += "No violations found. All documents use correct HIRM terminology.\n"
            return report
        
        report = [
            "# Terminology Enforcement Report",
            "",
            f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            ""
        ]
        
        if self.violations:
            report.extend([
                f"**Status:** ❌ {len(self.violations)} VIOLATIONS FOUND",
                "",
                "## Violations",
                "",
                f"- Total violations: {len(self.violations)}",
                f"- Files affected: {len(set(v['file'] for v in self.violations))}",
                ""
            ])
            
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
                    report.append(f"- Forbidden: `{v['forbidden']}`")
                    report.append(f"- Use instead: `{v['canonical']}`")
                    report.append(f"- Context: {v['context']}")
                    report.append("")
        
        if self.corrections_made:
            report.extend([
                "## Corrections Made",
                "",
                f"- Total corrections: {sum(c['count'] for c in self.corrections_made)}",
                f"- Files modified: {len(set(c['file'] for c in self.corrections_made))}",
                ""
            ])
            
            for c in self.corrections_made:
                report.append(f"- `{c['file']}`: {c['count']}x `{c['forbidden']}` → `{c['canonical']}`")
            report.append("")
        
        report.extend([
            "## Recommended Actions",
            "",
            "1. Review corrections made",
            "2. Run auto_correct(dry_run=False) to apply fixes",
            "3. Log corrections to Master_Data/Corrections/corrections_registry.md",
            "4. Re-run enforcer to verify compliance",
            "",
            "---",
            "",
            "**Generated by:** terminology_enforcer.py v1.0"
        ])
        
        report_text = '\n'.join(report)
        
        if output_path:
            output_path.write_text(report_text, encoding='utf-8')
            print(f"[OK] Report saved to {output_path}")
        
        return report_text
    
    def log_to_database(self, db_path: Path):
        """Log corrections to database"""
        if not self.corrections_made:
            return
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            for c in self.corrections_made:
                cursor.execute("""
                    INSERT INTO corrections (
                        correction_type, original_text, corrected_text,
                        source_session, reason, severity, recurrence_count
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    'terminology_violation',
                    c['forbidden'],
                    c['canonical'],
                    'auto_enforcer',
                    f"Found {c['count']} instances in {c['file']}",
                    'medium',
                    c['count']
                ))
            
            conn.commit()
            conn.close()
            print(f"[OK] Logged {len(self.corrections_made)} corrections to database")
        
        except Exception as e:
            print(f"[WARN] Could not log to database: {e}")

def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='HIRM Terminology Enforcer')
    parser.add_argument('--fix', action='store_true', help='Apply corrections (default is dry-run)')
    parser.add_argument('--scan-only', action='store_true', help='Only scan, do not correct')
    args = parser.parse_args()
    
    corpus_root = Path("D:/Research/HIRM")
    
    print("=" * 60)
    print("HIRM Terminology Enforcer v1.0")
    print("=" * 60)
    
    enforcer = TerminologyEnforcer(corpus_root)
    
    if args.scan_only:
        # Just scan
        violations = enforcer.scan_corpus()
    else:
        # Auto-correct (dry run unless --fix)
        corrections = enforcer.auto_correct(dry_run=not args.fix)
    
    # Generate report
    report_path = corpus_root / "Logs" / f"terminology_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    report = enforcer.generate_report(report_path)
    
    # Log to database if corrections were made
    if enforcer.corrections_made and args.fix:
        db_path = corpus_root / "System" / "data" / "hirm.db"
        if db_path.exists():
            enforcer.log_to_database(db_path)
    
    # Print summary
    print("\n" + "=" * 60)
    if enforcer.violations:
        print(f"[FAIL] Found {len(enforcer.violations)} violations")
        print(f"[INFO] Run with --fix to apply corrections")
    elif enforcer.corrections_made:
        if args.fix:
            print(f"[OK] Applied {sum(c['count'] for c in enforcer.corrections_made)} corrections")
        else:
            print(f"[DRY RUN] Would apply {sum(c['count'] for c in enforcer.corrections_made)} corrections")
    else:
        print("[OK] All terminology compliant")
    
    print(f"[INFO] See report: {report_path}")
    print("=" * 60)
    
    return 1 if enforcer.violations else 0

if __name__ == "__main__":
    exit(main())
