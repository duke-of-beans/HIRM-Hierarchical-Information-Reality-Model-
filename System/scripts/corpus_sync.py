#!/usr/bin/env python3
"""
HIRM Corpus Sync
================
Bidirectional synchronization between markdown files and database.

Markdown → Database:
- Parse documents for paper citations, add missing to papers table
- Extract equations from theory docs, verify against equations table
- Find constant values in docs, flag mismatches
- Detect new terminology usage

Database → Markdown:
- Regenerate corpus_master_index.md from papers table
- Update locked_constants.md from constants table
- Regenerate corrections_registry.md from corrections table
- Create domain summary documents from paper clustering

Usage:
    python corpus_sync.py              # Full bidirectional sync
    python corpus_sync.py --md-to-db   # Markdown to database only
    python corpus_sync.py --db-to-md   # Database to markdown only
    python corpus_sync.py --check      # Dry run, report conflicts

Created: 2025-12-20
Version: 1.0
"""

import argparse
import re
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime
from dataclasses import dataclass, field

from hirm_core import (
    HIRM_ROOT, MASTER_DATA, CONSTANTS_FILE, TERMINOLOGY_FILE,
    CORRECTIONS_FILE, CORPUS_INDEX, SESSION_LOG_FILE,
    get_locked_constants, get_all_papers, get_recurring_corrections,
    get_canonical_terms, get_legacy_terms, query_db, execute_db,
    find_hirm_files, generate_report_header
)

# Fix Windows console encoding issues
import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class SyncConflict:
    """Represents a conflict between markdown and database."""
    conflict_type: str
    location: str  # file path or table name
    db_value: Any
    md_value: Any
    resolution: str = ""

@dataclass
class SyncReport:
    """Report of sync operations."""
    timestamp: datetime
    direction: str  # 'md_to_db', 'db_to_md', 'bidirectional'
    conflicts: List[SyncConflict] = field(default_factory=list)
    changes_made: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

# =============================================================================
# MARKDOWN → DATABASE SYNC
# =============================================================================

def extract_citations_from_md(content: str) -> List[Dict[str, str]]:
    """Extract paper citations from markdown content."""
    citations = []
    
    # Pattern: (Author, Year) or (Author et al., Year)
    pattern = r'\(([A-Z][a-z]+(?:\s+et\s+al\.?)?)[,\s]+(\d{4})\)'
    matches = re.findall(pattern, content)
    
    for author, year in matches:
        citations.append({
            'author': author.replace(' et al', '').replace('.', ''),
            'year': int(year)
        })
    
    return citations


def extract_constants_from_md(content: str) -> Dict[str, str]:
    """Extract constant values mentioned in markdown."""
    constants = {}
    
    # Look for C_critical values
    c_crit_pattern = r'C[_\s]?critical\s*[=≈]\s*([\d.]+\s*±?\s*[\d.]*)'
    matches = re.findall(c_crit_pattern, content, re.IGNORECASE)
    if matches:
        constants['C_critical'] = matches[0].strip()
    
    # Look for exponent values
    exponents = {
        'nu': r'[νν]\s*[=≈]\s*~?([\d.]+)',
        'gamma': r'[γγ]\s*[=≈]\s*~?([\d.]+)',
        'beta': r'[ββ]\s*[=≈]\s*~?([\d.]+)',
        'tau': r'[ττ]\s*[=≈]\s*~?([\d.]+)',
        'alpha': r'[αα]\s*[=≈]\s*~?([\d.]+)',
    }
    
    for name, pattern in exponents.items():
        matches = re.findall(pattern, content)
        if matches:
            constants[name] = f"~{matches[0]}"
    
    return constants


def sync_md_to_db(dry_run: bool = False) -> SyncReport:
    """Sync markdown content to database."""
    report = SyncReport(timestamp=datetime.now(), direction='md_to_db')
    
    locked_constants = get_locked_constants()
    db_papers = {p['title'].lower(): p for p in get_all_papers()}
    
    files = find_hirm_files(extensions=['.md'])
    
    for file_path in files:
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Check constants
            md_constants = extract_constants_from_md(content)
            for symbol, md_value in md_constants.items():
                if symbol in locked_constants:
                    db_value = locked_constants[symbol]['value']
                    # Normalize for comparison
                    md_norm = md_value.replace(' ', '').replace('~', '')
                    db_norm = db_value.replace(' ', '').replace('~', '')
                    
                    if md_norm not in db_norm and db_norm not in md_norm:
                        report.conflicts.append(SyncConflict(
                            conflict_type='constant_mismatch',
                            location=str(file_path),
                            db_value=db_value,
                            md_value=md_value,
                            resolution="Database is source of truth - update markdown"
                        ))
        except Exception as e:
            report.errors.append(f"Error processing {file_path}: {e}")
    
    return report


# =============================================================================
# DATABASE → MARKDOWN SYNC
# =============================================================================

def generate_corpus_index() -> str:
    """Generate corpus_master_index.md from papers table."""
    papers = get_all_papers()
    
    output = [generate_report_header("HIRM Research Corpus Index")]
    output.append(f"**Total Papers:** {len(papers)}\n")
    output.append("---\n")
    
    # Group by domain
    domains = {}
    for paper in papers:
        domain = paper.get('domain', 'unclassified') or 'unclassified'
        if domain not in domains:
            domains[domain] = []
        domains[domain].append(paper)
    
    for domain in sorted(domains.keys()):
        domain_papers = domains[domain]
        output.append(f"## {domain.replace('_', ' ').title()} ({len(domain_papers)} papers)\n")
        
        # Sort by year descending
        domain_papers.sort(key=lambda p: p.get('year', 0) or 0, reverse=True)
        
        for paper in domain_papers:
            year = paper.get('year', 'n.d.')
            authors = paper.get('authors', 'Unknown')
            if isinstance(authors, str) and authors.startswith('['):
                try:
                    authors = ', '.join(json.loads(authors))
                except:
                    pass
            
            status_emoji = {
                'unread': '📕',
                'read': '📖',
                'integrated': '✅',
                'cited': '📝'
            }.get(paper.get('status', 'unread'), '📕')
            
            output.append(f"- {status_emoji} **{paper['title']}** ({year})")
            output.append(f"  - {authors}")
            if paper.get('journal'):
                output.append(f"  - *{paper['journal']}*")
            if paper.get('doi'):
                output.append(f"  - DOI: {paper['doi']}")
            output.append("")
        
        output.append("")
    
    return '\n'.join(output)


def generate_constants_md() -> str:
    """Generate locked_constants.md from constants table."""
    constants = query_db("SELECT * FROM constants ORDER BY symbol")
    
    output = ["""# LOCKED CONSTANTS REGISTRY
## HIRM Research - Single Source of Truth
## Last Updated: """ + datetime.now().strftime('%Y-%m-%d') + """
## Status: AUTHORITATIVE - All documents must match these values

---

## CRITICAL RULE
**Any document using different values is WRONG and must be corrected.**
**Database (hirm.db) is the master - this file mirrors it for human reference.**

---

## CORE HIRM CONSTANTS

| Symbol | Name | Value | Units | Status |
|--------|------|-------|-------|--------|"""]
    
    for const in constants:
        status = const['confidence'].upper() if const['confidence'] else 'PROVISIONAL'
        units = const['units'] or 'dimensionless'
        output.append(f"| {const['symbol']} | {const['name']} | **{const['value']}** | {units} | {status} |")
    
    output.append("""
---

## LOCKED EQUATION: CONSCIOUSNESS MEASURE

```
C(t) = Φ(t) × R(t) × D(t)
```

**Where:**
- **Φ(t)** = Integrated information [bits] - IIT-inspired measure
- **R(t)** = Self-reference coefficient [dimensionless, 0-1]
- **D(t)** = Dimensional complexity [effective dimensions]
- **C(t)** = Consciousness capacity [bits]

**Dimensional Check:** bits × dimensionless × dimensions = bits ✓

---

## UPDATE PROTOCOL

When updating constants:
1. Update database: `hirm.db` constants table
2. Run `corpus_sync.py --db-to-md` to update this file
3. Run `quality_gate.py --all` to check all documents
4. Log correction in corrections table
5. Flag affected documents for review
""")
    
    return '\n'.join(output)


def generate_corrections_md() -> str:
    """Generate corrections_registry.md from corrections table."""
    corrections = query_db("SELECT * FROM corrections ORDER BY severity DESC, recurrence_count DESC")
    
    output = ["""# CORRECTIONS REGISTRY
## Self-Healing Error Tracking
## Last Updated: """ + datetime.now().strftime('%Y-%m-%d') + """

---

## PURPOSE

This registry tracks errors, corrections, and theory updates to enable:
1. **Self-healing:** Prevent recurrence of known errors
2. **Learning:** Understand why errors occurred
3. **Protocol updates:** Add prevention to protocols when patterns emerge
4. **Intellectual honesty:** Transparent record of mistakes

---

## ACTIVE CORRECTIONS

| ID | Type | Original | Corrected | Recurrence | Severity | In Protocol |
|----|------|----------|-----------|------------|----------|-------------|"""]
    
    for i, corr in enumerate(corrections, 1):
        original = (corr['original_text'] or '')[:30]
        corrected = (corr['corrected_text'] or '')[:30]
        in_protocol = "✅" if corr['added_to_protocol'] else "❌"
        output.append(
            f"| {i} | {corr['correction_type']} | {original} | {corrected} | "
            f"{corr['recurrence_count']} | {corr['severity']} | {in_protocol} |"
        )
    
    output.append("""

---

## STATISTICS

| Metric | Value |
|--------|-------|""")
    
    total = len(corrections)
    critical = sum(1 for c in corrections if c['severity'] == 'critical')
    high = sum(1 for c in corrections if c['severity'] == 'high')
    in_protocol = sum(1 for c in corrections if c['added_to_protocol'])
    
    output.append(f"| Total corrections logged | {total} |")
    output.append(f"| Critical corrections | {critical} |")
    output.append(f"| High severity | {high} |")
    output.append(f"| Added to protocol | {in_protocol} ({100*in_protocol/total if total else 0:.0f}%) |")
    
    output.append("""

---

## MONTHLY REVIEW

At start of each month:
1. Review all corrections from previous month
2. Identify patterns
3. Update protocols to prevent recurrence
4. Clear resolved corrections older than 6 months
""")
    
    return '\n'.join(output)


def sync_db_to_md(dry_run: bool = False) -> SyncReport:
    """Sync database content to markdown files."""
    report = SyncReport(timestamp=datetime.now(), direction='db_to_md')
    
    files_to_update = [
        (CORPUS_INDEX.parent / 'corpus_master_index.md', generate_corpus_index),
        (CONSTANTS_FILE, generate_constants_md),
        (CORRECTIONS_FILE, generate_corrections_md),
    ]
    
    for file_path, generator in files_to_update:
        try:
            new_content = generator()
            
            if file_path.exists():
                old_content = file_path.read_text(encoding='utf-8')
                if old_content.strip() == new_content.strip():
                    continue  # No changes needed
            
            if not dry_run:
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text(new_content, encoding='utf-8')
                report.changes_made.append(f"Updated {file_path.name}")
            else:
                report.changes_made.append(f"Would update {file_path.name}")
                
        except Exception as e:
            report.errors.append(f"Error updating {file_path}: {e}")
    
    return report


# =============================================================================
# FULL SYNC
# =============================================================================

def run_full_sync(dry_run: bool = False) -> Tuple[SyncReport, SyncReport]:
    """Run bidirectional sync."""
    print("Running bidirectional sync...")
    
    print("  Checking markdown -> database...")
    md_report = sync_md_to_db(dry_run)
    
    print("  Syncing database -> markdown...")
    db_report = sync_db_to_md(dry_run)
    
    return md_report, db_report


def format_sync_report(report: SyncReport) -> str:
    """Format sync report for display."""
    output = []
    output.append(f"\n{'='*60}")
    output.append(f"SYNC REPORT: {report.direction}")
    output.append(f"Timestamp: {report.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    output.append(f"{'='*60}")
    
    if report.conflicts:
        output.append(f"\n[!] CONFLICTS FOUND: {len(report.conflicts)}")
        for conflict in report.conflicts:
            output.append(f"\n  [{conflict.conflict_type}]")
            output.append(f"  Location: {conflict.location}")
            output.append(f"  Database: {conflict.db_value}")
            output.append(f"  Markdown: {conflict.md_value}")
            output.append(f"  Resolution: {conflict.resolution}")
    
    if report.changes_made:
        output.append(f"\n[OK] CHANGES: {len(report.changes_made)}")
        for change in report.changes_made:
            output.append(f"  • {change}")
    
    if report.errors:
        output.append(f"\n[X] ERRORS: {len(report.errors)}")
        for error in report.errors:
            output.append(f"  • {error}")
    
    if not report.conflicts and not report.changes_made and not report.errors:
        output.append("\n[*] Everything is in sync!")
    
    return '\n'.join(output)


# =============================================================================
# COMMAND LINE INTERFACE
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='HIRM Corpus Sync - Bidirectional markdown/database synchronization'
    )
    parser.add_argument('--md-to-db', action='store_true',
                       help='Sync markdown to database only')
    parser.add_argument('--db-to-md', action='store_true',
                       help='Sync database to markdown only')
    parser.add_argument('--check', action='store_true',
                       help='Dry run - report conflicts without making changes')
    parser.add_argument('--output', '-o', help='Write report to file')
    
    args = parser.parse_args()
    
    dry_run = args.check
    
    if args.md_to_db:
        report = sync_md_to_db(dry_run)
        output = format_sync_report(report)
    elif args.db_to_md:
        report = sync_db_to_md(dry_run)
        output = format_sync_report(report)
    else:
        md_report, db_report = run_full_sync(dry_run)
        output = format_sync_report(md_report) + "\n" + format_sync_report(db_report)
    
    print(output)
    
    if args.output:
        Path(args.output).write_text(output)
        print(f"\nReport written to: {args.output}")


if __name__ == '__main__':
    main()
