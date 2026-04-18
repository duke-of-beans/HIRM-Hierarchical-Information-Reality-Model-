#!/usr/bin/env python3
"""
HIRM Quality Gate
=================
Pre-delivery validation for all HIRM documents.
Catches errors before they propagate into the research corpus.

Checks performed:
1. Constants validation - Match against locked_constants.md
2. Terminology check - Flag legacy terms ("Ouroboros Observer")
3. Equation verification - Dimensional consistency
4. Citation check - Ensure cited papers exist in database
5. Falsification check - Verify claims have falsification criteria
6. Competing theories - Ensure alternatives are mentioned
7. Claim strength - Flag overly strong claims

Usage:
    python quality_gate.py <file_path>
    python quality_gate.py --all  # Check all documents
    python quality_gate.py --threshold 85  # Custom passing threshold

Created: 2025-12-20
Version: 1.0
"""

import sys
import re
import argparse
from pathlib import Path
from typing import List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass

# Import core utilities
from hirm_core import (
    HIRM_ROOT, MASTER_DATA, DB_PATH,
    get_locked_constants, get_legacy_terms, get_all_papers,
    get_predictions, get_equations, log_correction,
    register_document, find_hirm_files,
    Issue, IssueType, Severity, QualityReport,
    FORBIDDEN_TERMS, FORBIDDEN_CLAIMS, WRONG_CONSTANTS,
    normalize_text_for_comparison
)

# =============================================================================
# CONSTANTS FOR QUALITY GATE
# =============================================================================

DEFAULT_THRESHOLD = 90  # Minimum passing score

# Patterns that should trigger falsification check
CLAIM_PATTERNS = [
    r'hirm\s+predicts',
    r'the\s+theory\s+suggests',
    r'c\(t\)\s+(?:will|should|would)',
    r'consciousness\s+emerges?\s+when',
    r'this\s+(?:proves?|demonstrates?|shows?)',
]

# Patterns indicating competing theories should be discussed
COMPETITION_TRIGGERS = [
    r'(?:better|superior|improved)\s+(?:than|to)',
    r'unlike\s+(?:other|previous|existing)',
    r'in\s+contrast\s+to',
    r'compared\s+to\s+(?:iit|gnwt|rpt|ast)',
]

# =============================================================================
# CHECK FUNCTIONS
# =============================================================================

def check_constants(content: str, lines: List[str]) -> List[Issue]:
    """Check all numerical values against locked constants."""
    issues = []
    locked = get_locked_constants()
    normalized_content = normalize_text_for_comparison(content)
    
    # Check for wrong constant values
    for wrong_pattern, (correct, severity) in WRONG_CONSTANTS.items():
        if wrong_pattern.lower() in normalized_content:
            # Find line number
            line_num = None
            for i, line in enumerate(lines, 1):
                if wrong_pattern.lower() in line.lower():
                    line_num = i
                    break
            
            issues.append(Issue(
                issue_type=IssueType.CONSTANT_MISMATCH,
                severity=severity,
                message=f"Incorrect constant value detected",
                line_number=line_num,
                original_text=wrong_pattern,
                suggested_fix=correct
            ))
    
    # Check for C_critical variations
    c_crit_pattern = r'c[_\s]?critical\s*[=≈]\s*(\d+\.?\d*)'
    matches = re.finditer(c_crit_pattern, content, re.IGNORECASE)
    for match in matches:
        value = float(match.group(1))
        if abs(value - 8.3) > 0.1:  # Allow small variation
            line_num = content[:match.start()].count('\n') + 1
            issues.append(Issue(
                issue_type=IssueType.CONSTANT_MISMATCH,
                severity=Severity.HIGH,
                message=f"C_critical value {value} differs from locked value 8.3",
                line_number=line_num,
                original_text=match.group(0),
                suggested_fix="C_critical = 8.3 ± 0.6"
            ))
    
    return issues


def check_terminology(content: str, lines: List[str]) -> List[Issue]:
    """Check for legacy/forbidden terminology."""
    issues = []
    normalized_content = normalize_text_for_comparison(content)
    
    # Check forbidden terms from FORBIDDEN_TERMS
    for term, (replacement, severity) in FORBIDDEN_TERMS.items():
        if term.lower() in normalized_content:
            # Find line number
            line_num = None
            for i, line in enumerate(lines, 1):
                if term.lower() in line.lower():
                    line_num = i
                    break
            
            issues.append(Issue(
                issue_type=IssueType.LEGACY_TERMINOLOGY,
                severity=severity,
                message=f"Legacy term '{term}' found",
                line_number=line_num,
                original_text=term,
                suggested_fix=replacement
            ))
    
    # Check forbidden claims
    for claim, (replacement, severity) in FORBIDDEN_CLAIMS.items():
        if claim.lower() in normalized_content:
            line_num = None
            for i, line in enumerate(lines, 1):
                if claim.lower() in line.lower():
                    line_num = i
                    break
            
            issues.append(Issue(
                issue_type=IssueType.CLAIM_TOO_STRONG,
                severity=severity,
                message=f"Overly strong claim detected",
                line_number=line_num,
                original_text=claim,
                suggested_fix=replacement
            ))
    
    # Check for "Ouroboros" specifically (common legacy term)
    ouroboros_matches = list(re.finditer(r'\bouroboros\b', content, re.IGNORECASE))
    for match in ouroboros_matches:
        line_num = content[:match.start()].count('\n') + 1
        if not any(i.original_text and 'ouroboros' in i.original_text.lower() 
                   for i in issues):
            issues.append(Issue(
                issue_type=IssueType.LEGACY_TERMINOLOGY,
                severity=Severity.MEDIUM,
                message="Legacy 'Ouroboros' terminology found",
                line_number=line_num,
                original_text=match.group(0),
                suggested_fix="HIRM"
            ))
    
    return issues


def check_equations(content: str, lines: List[str]) -> List[Issue]:
    """Check equations for correctness."""
    issues = []
    normalized = normalize_text_for_comparison(content)
    
    # Check for additive equation error (should be multiplicative)
    additive_patterns = [
        r'c\s*=\s*[φΦphi]\s*\+\s*r\s*\+\s*d',
        r'c\(t\)\s*=\s*[φΦphi]\(t\)\s*\+\s*r\(t\)\s*\+\s*d\(t\)',
    ]
    
    for pattern in additive_patterns:
        if re.search(pattern, normalized, re.IGNORECASE):
            line_num = None
            for i, line in enumerate(lines, 1):
                if re.search(pattern, normalize_text_for_comparison(line), re.IGNORECASE):
                    line_num = i
                    break
            
            issues.append(Issue(
                issue_type=IssueType.EQUATION_ERROR,
                severity=Severity.CRITICAL,
                message="CRITICAL: Equation uses addition instead of multiplication",
                line_number=line_num,
                original_text="C = Φ + R + D",
                suggested_fix="C(t) = Φ(t) × R(t) × D(t)"
            ))
    
    return issues


def check_citations(content: str, lines: List[str]) -> List[Issue]:
    """Check that citations reference papers in our database."""
    issues = []
    papers = get_all_papers()
    paper_titles = {p['title'].lower() for p in papers}
    paper_authors = set()
    
    for p in papers:
        if p['authors']:
            # Handle both string and potential JSON array
            authors = p['authors']
            if isinstance(authors, str):
                paper_authors.add(authors.split(',')[0].strip().lower())
    
    # Look for citation patterns like "(Author, Year)" or "(Author Year)"
    citation_pattern = r'\(([A-Z][a-z]+(?:\s+et\s+al\.?)?)[,\s]+(\d{4})\)'
    matches = re.finditer(citation_pattern, content)
    
    for match in matches:
        author = match.group(1).lower().replace(' et al', '').replace('.', '')
        # Only flag if we have papers and the author isn't in our database
        if papers and author not in paper_authors and len(author) > 2:
            line_num = content[:match.start()].count('\n') + 1
            issues.append(Issue(
                issue_type=IssueType.CITATION_ERROR,
                severity=Severity.LOW,
                message=f"Citation '{match.group(0)}' - author not found in corpus",
                line_number=line_num,
                original_text=match.group(0),
                suggested_fix="Consider adding paper to corpus database"
            ))
    
    return issues


def check_falsification(content: str, lines: List[str]) -> List[Issue]:
    """Check that claims have falsification criteria."""
    issues = []
    
    # Count claim patterns
    claim_count = 0
    for pattern in CLAIM_PATTERNS:
        claim_count += len(re.findall(pattern, content, re.IGNORECASE))
    
    # Look for falsification indicators
    falsification_indicators = [
        r'falsif(?:y|ied|iable|ication)',
        r'would\s+be\s+(?:wrong|falsified|disproven)',
        r'if\s+(?:not|contrary)',
        r'prediction\s+(?:fails?|failed)',
        r'null\s+hypothesis',
        r'disconfirm',
    ]
    
    falsification_found = False
    for indicator in falsification_indicators:
        if re.search(indicator, content, re.IGNORECASE):
            falsification_found = True
            break
    
    # Only flag if there are significant claims without falsification
    if claim_count >= 3 and not falsification_found:
        issues.append(Issue(
            issue_type=IssueType.MISSING_FALSIFICATION,
            severity=Severity.MEDIUM,
            message="Document makes claims but lacks explicit falsification criteria",
            suggested_fix="Add section: 'What would prove this wrong?' or 'Falsification criteria'"
        ))
    
    return issues


def check_competing_theories(content: str, lines: List[str]) -> List[Issue]:
    """Check that competing theories are addressed when making comparisons."""
    issues = []
    
    # Check for comparison triggers
    making_comparisons = False
    for pattern in COMPETITION_TRIGGERS:
        if re.search(pattern, content, re.IGNORECASE):
            making_comparisons = True
            break
    
    if making_comparisons:
        # Look for mentions of competing theories
        theories = ['iit', 'gnwt', 'rpt', 'ast', 'hot', 'fep', 'tononi', 
                   'dehaene', 'lamme', 'graziano', 'friston']
        theory_mentions = sum(1 for t in theories 
                            if re.search(rf'\b{t}\b', content, re.IGNORECASE))
        
        if theory_mentions < 2:
            issues.append(Issue(
                issue_type=IssueType.MISSING_ALTERNATIVES,
                severity=Severity.LOW,
                message="Document makes comparisons but doesn't explicitly name competing theories",
                suggested_fix="Reference specific theories (IIT, GNWT, RPT, etc.) when making comparisons"
            ))
    
    return issues


def check_dimensional_analysis(content: str, lines: List[str]) -> List[Issue]:
    """Check for dimensional consistency in equations."""
    issues = []
    
    # Look for equations that might have dimensional issues
    # This is a simplified check - full dimensional analysis would need a parser
    
    # Check if document discusses equations
    has_equations = bool(re.search(r'[=×·/]\s*[ΦφRDCt]', content))
    
    if has_equations:
        # Look for dimensional analysis markers
        has_dim_check = bool(re.search(
            r'dimensional|units?|bits?\s*[×·]\s*dimensionless', 
            content, re.IGNORECASE
        ))
        
        if not has_dim_check:
            issues.append(Issue(
                issue_type=IssueType.DIMENSIONAL_ERROR,
                severity=Severity.LOW,
                message="Document contains equations but no dimensional analysis",
                suggested_fix="Add dimensional analysis showing units are consistent"
            ))
    
    return issues


# =============================================================================
# MAIN QUALITY GATE FUNCTION
# =============================================================================

def run_quality_gate(file_path: Path, threshold: int = DEFAULT_THRESHOLD) -> QualityReport:
    """
    Run all quality checks on a document.
    
    Args:
        file_path: Path to the document to check
        threshold: Minimum score to pass (0-100)
    
    Returns:
        QualityReport with results
    """
    report = QualityReport(
        file_path=file_path,
        timestamp=datetime.now(),
        passed=False,
        score=0.0,
        issues=[],
        checks_performed=[]
    )
    
    # Read file content
    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
    except Exception as e:
        report.summary = f"ERROR: Could not read file: {e}"
        return report
    
    # Run all checks
    checks = [
        ('constants', check_constants),
        ('terminology', check_terminology),
        ('equations', check_equations),
        ('citations', check_citations),
        ('falsification', check_falsification),
        ('competing_theories', check_competing_theories),
        ('dimensional_analysis', check_dimensional_analysis),
    ]
    
    for check_name, check_func in checks:
        report.checks_performed.append(check_name)
        try:
            issues = check_func(content, lines)
            report.issues.extend(issues)
        except Exception as e:
            print(f"Warning: Check '{check_name}' failed: {e}")
    
    # Calculate score
    # Start at 100 and deduct based on severity
    score = 100.0
    severity_deductions = {
        Severity.CRITICAL: 25,
        Severity.HIGH: 15,
        Severity.MEDIUM: 5,
        Severity.LOW: 2,
    }
    
    for issue in report.issues:
        score -= severity_deductions.get(issue.severity, 5)
    
    report.score = max(0, score)
    report.passed = report.score >= threshold
    
    # Generate summary
    critical_count = sum(1 for i in report.issues if i.severity == Severity.CRITICAL)
    high_count = sum(1 for i in report.issues if i.severity == Severity.HIGH)
    
    if report.passed:
        report.summary = f"✅ PASSED ({report.score:.0f}%): {len(report.issues)} issues found"
    else:
        report.summary = f"❌ FAILED ({report.score:.0f}%): {critical_count} critical, {high_count} high severity"
    
    return report


def format_report(report: QualityReport, verbose: bool = True) -> str:
    """Format a quality report for display."""
    output = []
    output.append("=" * 70)
    output.append(f"HIRM QUALITY GATE REPORT")
    output.append("=" * 70)
    output.append(f"File: {report.file_path}")
    output.append(f"Timestamp: {report.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    output.append(f"Checks: {', '.join(report.checks_performed)}")
    output.append("-" * 70)
    output.append(f"RESULT: {report.summary}")
    output.append(f"Score: {report.score:.0f}/100")
    output.append("-" * 70)
    
    if report.issues and verbose:
        output.append("\nISSUES FOUND:")
        output.append("")
        
        # Group by severity
        for severity in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]:
            sev_issues = [i for i in report.issues if i.severity == severity]
            if sev_issues:
                output.append(f"\n[{severity.value.upper()}]")
                for issue in sev_issues:
                    output.append(f"  • {issue.message}")
                    if issue.line_number:
                        output.append(f"    Line {issue.line_number}")
                    if issue.original_text:
                        output.append(f"    Found: {issue.original_text}")
                    if issue.suggested_fix:
                        output.append(f"    Fix: {issue.suggested_fix}")
                    output.append("")
    
    if not report.issues:
        output.append("\n✨ No issues found!")
    
    output.append("=" * 70)
    return '\n'.join(output)


# =============================================================================
# BATCH PROCESSING
# =============================================================================

def check_all_documents(threshold: int = DEFAULT_THRESHOLD) -> Tuple[List[QualityReport], dict]:
    """
    Run quality gate on all HIRM documents.
    
    Returns:
        Tuple of (list of reports, summary statistics)
    """
    reports = []
    files = find_hirm_files(extensions=['.md'])
    
    print(f"Checking {len(files)} documents...")
    
    for file_path in files:
        report = run_quality_gate(file_path, threshold)
        reports.append(report)
        
        # Log to database if failed
        if not report.passed:
            register_document(
                file_path=file_path,
                document_type='markdown',
                quality_score=report.score,
                validation_passed=False
            )
        
        # Log corrections for critical/high issues
        for issue in report.issues:
            if issue.severity in [Severity.CRITICAL, Severity.HIGH]:
                if issue.original_text and issue.suggested_fix:
                    log_correction(
                        correction_type=issue.issue_type.value,
                        original_text=issue.original_text,
                        corrected_text=issue.suggested_fix,
                        reason=issue.message,
                        severity=issue.severity,
                        source_session=f"quality_gate_{datetime.now().strftime('%Y%m%d')}"
                    )
    
    # Calculate statistics
    stats = {
        'total': len(reports),
        'passed': sum(1 for r in reports if r.passed),
        'failed': sum(1 for r in reports if not r.passed),
        'avg_score': sum(r.score for r in reports) / len(reports) if reports else 0,
        'critical_issues': sum(
            sum(1 for i in r.issues if i.severity == Severity.CRITICAL) 
            for r in reports
        ),
        'high_issues': sum(
            sum(1 for i in r.issues if i.severity == Severity.HIGH) 
            for r in reports
        ),
    }
    
    return reports, stats


# =============================================================================
# COMMAND LINE INTERFACE
# =============================================================================

def main():
    # Set UTF-8 encoding for Windows console
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    parser = argparse.ArgumentParser(
        description='HIRM Quality Gate - Document validation system',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python quality_gate.py document.md           Check single file
  python quality_gate.py --all                 Check all documents
  python quality_gate.py --threshold 85 file   Use 85% threshold
  python quality_gate.py --quiet file          Minimal output
        """
    )
    
    parser.add_argument('file', nargs='?', help='File to check')
    parser.add_argument('--all', '-a', action='store_true', 
                       help='Check all HIRM documents')
    parser.add_argument('--threshold', '-t', type=int, default=DEFAULT_THRESHOLD,
                       help=f'Minimum passing score (default: {DEFAULT_THRESHOLD})')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Minimal output')
    parser.add_argument('--output', '-o', help='Write report to file')
    
    args = parser.parse_args()
    
    if args.all:
        # Check all documents
        reports, stats = check_all_documents(args.threshold)
        
        if not args.quiet:
            print("\n" + "=" * 70)
            print("BATCH QUALITY GATE RESULTS")
            print("=" * 70)
            print(f"Total documents: {stats['total']}")
            print(f"Passed: {stats['passed']} ({100*stats['passed']/stats['total']:.0f}%)")
            print(f"Failed: {stats['failed']} ({100*stats['failed']/stats['total']:.0f}%)")
            print(f"Average score: {stats['avg_score']:.1f}")
            print(f"Critical issues: {stats['critical_issues']}")
            print(f"High severity issues: {stats['high_issues']}")
            print("=" * 70)
            
            # List failed documents
            failed = [r for r in reports if not r.passed]
            if failed:
                print("\n❌ FAILED DOCUMENTS:")
                for report in sorted(failed, key=lambda r: r.score):
                    print(f"  {report.score:.0f}% - {report.file_path.name}")
        
        sys.exit(0 if stats['failed'] == 0 else 1)
    
    elif args.file:
        # Check single file
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {file_path}")
            sys.exit(1)
        
        report = run_quality_gate(file_path, args.threshold)
        
        if not args.quiet:
            print(format_report(report))
        
        if args.output:
            Path(args.output).write_text(format_report(report))
            print(f"Report written to: {args.output}")
        
        sys.exit(0 if report.passed else 1)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
