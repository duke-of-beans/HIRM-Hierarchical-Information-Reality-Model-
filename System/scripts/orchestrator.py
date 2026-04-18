#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HIRM Orchestrator
=================
Master script that ties all automation components together.
Runs the complete self-learning loop.

The Learning Loop:
1. Sync current state (corpus_sync)
2. Detect patterns (pattern_detector)
3. Analyze recent sessions (session_analyzer)
4. Generate improvements (improvement_suggester)
5. Create system health report
6. Auto-apply safe improvements
7. Queue human-review items

Usage:
    python orchestrator.py              # Run full learning cycle
    python orchestrator.py --quick      # Quick check only
    python orchestrator.py --report     # Generate health report only
    python orchestrator.py --auto-fix   # Auto-fix safe issues

Created: 2025-12-20
Version: 1.0
"""

import argparse
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, field

from hirm_core import (
    HIRM_ROOT, log_session, register_document, execute_db,
    generate_report_header, find_hirm_files
)

# Import other automation modules
from corpus_sync import run_full_sync, sync_db_to_md
from pattern_detector import run_full_scan as run_pattern_scan
from session_analyzer import run_analysis as run_session_analysis
from improvement_suggester import generate_all_suggestions
from quality_gate import run_quality_gate, check_all_documents

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class SystemHealth:
    """Overall system health assessment."""
    timestamp: datetime
    status: str  # 'healthy', 'warning', 'critical'
    score: float  # 0-100
    components: Dict[str, str] = field(default_factory=dict)
    issues: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

@dataclass
class LearningCycleResult:
    """Result of a complete learning cycle."""
    timestamp: datetime
    sync_conflicts: int = 0
    patterns_found: int = 0
    insights_generated: int = 0
    improvements_suggested: int = 0
    auto_fixes_applied: int = 0
    items_for_review: int = 0
    errors: List[str] = field(default_factory=list)


# =============================================================================
# SYSTEM HEALTH ASSESSMENT
# =============================================================================

def assess_system_health() -> SystemHealth:
    """Assess overall system health."""
    health = SystemHealth(
        timestamp=datetime.now(),
        status='healthy',
        score=100
    )
    
    # Check database
    try:
        from hirm_core import get_locked_constants, get_all_papers
        constants = get_locked_constants()
        papers = get_all_papers()
        health.components['database'] = f'OK ({len(constants)} constants, {len(papers)} papers)'
    except Exception as e:
        health.components['database'] = f'ERROR: {e}'
        health.issues.append(f"Database error: {e}")
        health.score -= 30
    
    # Check critical files
    critical_files = [
        HIRM_ROOT / 'Master_Data' / 'Constants' / 'locked_constants.md',
        HIRM_ROOT / 'Master_Data' / 'Terminology' / 'terminology_reference.md',
        HIRM_ROOT / 'Protocols' / 'HIRM_RESEARCH_PROTOCOLS_v2.md',
    ]
    
    missing = [f for f in critical_files if not f.exists()]
    if missing:
        health.components['files'] = f'MISSING: {len(missing)} critical files'
        health.issues.append(f"Missing files: {', '.join(f.name for f in missing)}")
        health.score -= 20
    else:
        health.components['files'] = 'OK (all critical files present)'
    
    # Check scripts
    scripts_dir = HIRM_ROOT / 'System' / 'scripts'
    expected_scripts = ['hirm_core.py', 'quality_gate.py', 'pattern_detector.py',
                       'corpus_sync.py', 'session_analyzer.py', 'improvement_suggester.py',
                       'orchestrator.py']
    existing = {f.name for f in scripts_dir.glob('*.py')}
    missing_scripts = set(expected_scripts) - existing
    
    if missing_scripts:
        health.components['scripts'] = f'INCOMPLETE: missing {len(missing_scripts)}'
        health.issues.append(f"Missing scripts: {', '.join(missing_scripts)}")
        health.score -= 10
    else:
        health.components['scripts'] = 'OK (all automation scripts present)'
    
    # Determine overall status
    if health.score >= 90:
        health.status = 'healthy'
    elif health.score >= 70:
        health.status = 'warning'
    else:
        health.status = 'critical'
    
    # Add recommendations
    if 'database' in health.components and 'ERROR' in health.components['database']:
        health.recommendations.append("Run init_database.py to recreate database")
    if missing:
        health.recommendations.append("Restore missing critical files from backup")
    
    return health


# =============================================================================
# LEARNING CYCLE
# =============================================================================

def run_learning_cycle(auto_fix: bool = False, verbose: bool = True) -> LearningCycleResult:
    """Run the complete self-learning loop."""
    result = LearningCycleResult(timestamp=datetime.now())
    
    if verbose:
        print("=" * 60)
        print("HIRM LEARNING CYCLE")
        print("=" * 60)
    
    # Step 1: Sync current state
    if verbose:
        print("\n[1/5] Syncing corpus...")
    try:
        md_report, db_report = run_full_sync(dry_run=not auto_fix)
        result.sync_conflicts = len(md_report.conflicts)
        if md_report.conflicts and verbose:
            print(f"  ⚠️ {len(md_report.conflicts)} sync conflicts found")
    except Exception as e:
        result.errors.append(f"Sync failed: {e}")
        if verbose:
            print(f"  ❌ Sync failed: {e}")
    
    # Step 2: Detect patterns
    if verbose:
        print("\n[2/5] Detecting patterns...")
    try:
        pattern_report = run_pattern_scan()
        result.patterns_found = len(pattern_report.patterns)
        if verbose:
            print(f"  📊 {result.patterns_found} patterns detected")
            action_req = sum(1 for p in pattern_report.patterns if p.severity == 'action_required')
            if action_req:
                print(f"  🚨 {action_req} require action")
    except Exception as e:
        result.errors.append(f"Pattern detection failed: {e}")
        if verbose:
            print(f"  ❌ Pattern detection failed: {e}")
    
    # Step 3: Analyze sessions
    if verbose:
        print("\n[3/5] Analyzing sessions...")
    try:
        session_analysis = run_session_analysis()
        result.insights_generated = len(session_analysis.insights)
        if verbose:
            print(f"  💡 {result.insights_generated} insights generated")
    except Exception as e:
        result.errors.append(f"Session analysis failed: {e}")
        if verbose:
            print(f"  ❌ Session analysis failed: {e}")
    
    # Step 4: Generate improvements
    if verbose:
        print("\n[4/5] Generating improvements...")
    try:
        improvement_report = generate_all_suggestions()
        result.improvements_suggested = len(improvement_report.improvements)
        high_priority = sum(1 for i in improvement_report.improvements 
                          if i.priority.value in ['critical', 'high'])
        if verbose:
            print(f"  📝 {result.improvements_suggested} improvements suggested")
            if high_priority:
                print(f"  🔴 {high_priority} high priority items")
    except Exception as e:
        result.errors.append(f"Improvement generation failed: {e}")
        if verbose:
            print(f"  ❌ Improvement generation failed: {e}")
    
    # Step 5: Apply safe auto-fixes
    if auto_fix and verbose:
        print("\n[5/5] Applying safe fixes...")
        try:
            # Sync database to markdown (always safe)
            sync_db_to_md(dry_run=False)
            result.auto_fixes_applied += 1
            print("  ✅ Synced database to markdown files")
        except Exception as e:
            result.errors.append(f"Auto-fix failed: {e}")
            print(f"  ❌ Auto-fix failed: {e}")
    
    # Calculate items for review
    result.items_for_review = (
        result.sync_conflicts + 
        sum(1 for p in pattern_report.patterns if p.severity == 'action_required') if 'pattern_report' in dir() else 0 +
        sum(1 for i in improvement_report.improvements if i.priority.value == 'high') if 'improvement_report' in dir() else 0
    )
    
    # Log session
    try:
        log_session(
            session_type='learning_cycle',
            work_completed=[
                f"Sync: {result.sync_conflicts} conflicts",
                f"Patterns: {result.patterns_found} found",
                f"Insights: {result.insights_generated} generated",
                f"Improvements: {result.improvements_suggested} suggested"
            ],
            findings=[f"Items for review: {result.items_for_review}"],
            errors_encountered='\n'.join(result.errors) if result.errors else None
        )
    except:
        pass  # Don't fail on logging error
    
    return result


# =============================================================================
# REPORT GENERATION
# =============================================================================

def generate_health_report() -> str:
    """Generate comprehensive system health report."""
    health = assess_system_health()
    
    output = [generate_report_header("HIRM System Health Report")]
    
    # Overall status
    status_emoji = {'healthy': '✅', 'warning': '⚠️', 'critical': '🚨'}[health.status]
    output.append(f"## {status_emoji} Overall Status: {health.status.upper()}")
    output.append(f"**Health Score:** {health.score:.0f}/100\n")
    output.append("---\n")
    
    # Components
    output.append("## Component Status\n")
    for component, status in health.components.items():
        emoji = '✅' if 'OK' in status else ('⚠️' if 'INCOMPLETE' in status else '❌')
        output.append(f"- **{component}:** {emoji} {status}")
    output.append("")
    
    # Issues
    if health.issues:
        output.append("## ⚠️ Issues\n")
        for issue in health.issues:
            output.append(f"- {issue}")
        output.append("")
    
    # Recommendations
    if health.recommendations:
        output.append("## 📋 Recommendations\n")
        for rec in health.recommendations:
            output.append(f"1. {rec}")
        output.append("")
    
    return '\n'.join(output)


def generate_cycle_report(result: LearningCycleResult) -> str:
    """Generate report from learning cycle."""
    output = [generate_report_header("Learning Cycle Report")]
    
    output.append(f"**Timestamp:** {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n")
    output.append("---\n")
    
    output.append("## 📊 Results\n")
    output.append(f"| Metric | Value |")
    output.append(f"|--------|-------|")
    output.append(f"| Sync Conflicts | {result.sync_conflicts} |")
    output.append(f"| Patterns Found | {result.patterns_found} |")
    output.append(f"| Insights Generated | {result.insights_generated} |")
    output.append(f"| Improvements Suggested | {result.improvements_suggested} |")
    output.append(f"| Auto-fixes Applied | {result.auto_fixes_applied} |")
    output.append(f"| Items for Review | {result.items_for_review} |")
    output.append("")
    
    if result.errors:
        output.append("## ❌ Errors\n")
        for error in result.errors:
            output.append(f"- {error}")
        output.append("")
    
    # Summary
    if result.items_for_review > 0:
        output.append(f"## 📌 Action Required\n")
        output.append(f"**{result.items_for_review} items need human review.**")
        output.append("\nRun these commands for details:")
        output.append("```bash")
        output.append("python pattern_detector.py  # See patterns requiring action")
        output.append("python improvement_suggester.py --priority high  # See high priority improvements")
        output.append("```")
    else:
        output.append("## All Clear\n")
        output.append("No items requiring immediate attention.")
    
    return '\n'.join(output)


def quick_check() -> None:
    """Run a quick system check."""
    print("\n[CHECK] HIRM Quick Check")
    print("=" * 40)
    
    health = assess_system_health()
    status_text = {'healthy': '[OK]', 'warning': '[WARN]', 'critical': '[CRITICAL]'}[health.status]
    
    print(f"\nStatus: {status_text} {health.status.upper()} ({health.score:.0f}/100)")
    
    for component, status in health.components.items():
        marker = '[OK]' if 'OK' in status else '[!!]'
        print(f"  {marker} {component}")
    
    if health.issues:
        print(f"\n[!!] {len(health.issues)} issue(s) found")
        for issue in health.issues[:3]:
            print(f"  - {issue}")
    else:
        print("\n[OK] No issues found")


# =============================================================================
# COMMAND LINE INTERFACE
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='HIRM Orchestrator - Master automation controller'
    )
    parser.add_argument('--quick', '-q', action='store_true',
                       help='Quick health check only')
    parser.add_argument('--report', '-r', action='store_true',
                       help='Generate health report only')
    parser.add_argument('--auto-fix', action='store_true',
                       help='Auto-apply safe fixes')
    parser.add_argument('--output', '-o', help='Write report to file')
    parser.add_argument('--verbose', '-v', action='store_true', default=True,
                       help='Verbose output')
    
    args = parser.parse_args()
    
    if args.quick:
        quick_check()
        return
    
    if args.report:
        output = generate_health_report()
        print(output)
        if args.output:
            Path(args.output).write_text(output)
            print(f"\nReport written to: {args.output}")
        return
    
    # Run full learning cycle
    result = run_learning_cycle(auto_fix=args.auto_fix, verbose=args.verbose)
    
    # Print summary
    print("\n" + "=" * 60)
    print("LEARNING CYCLE COMPLETE")
    print("=" * 60)
    
    if result.errors:
        print(f"\n[ERROR] {len(result.errors)} errors occurred")
    
    if result.items_for_review > 0:
        print(f"\n[REVIEW] {result.items_for_review} items need human review")
        print("   Run 'python orchestrator.py --report' for details")
    else:
        print("\n[OK] All systems nominal")
    
    if args.output:
        report = generate_cycle_report(result)
        Path(args.output).write_text(report)
        print(f"\nReport written to: {args.output}")


if __name__ == '__main__':
    main()
