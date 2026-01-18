#!/usr/bin/env python3
"""
HIRM Improvement Suggester
==========================
Continuously proposes ways to improve the system and research.

Suggests improvements for:
1. System - New quality gate checks, protocol additions
2. Research - Papers to add, predictions to test, connections to explore
3. Workflow - Optimizations based on usage patterns
4. Theory - Extensions suggested by patterns in the data

Usage:
    python improvement_suggester.py              # Generate all suggestions
    python improvement_suggester.py --system     # System improvements only
    python improvement_suggester.py --research   # Research improvements only
    python improvement_suggester.py --priority   # High priority only

Created: 2025-12-20
Version: 1.0
"""

import argparse
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

from hirm_core import (
    HIRM_ROOT, get_recurring_corrections, get_all_papers, get_predictions,
    get_locked_constants, find_hirm_files, query_db, generate_report_header
)

# =============================================================================
# DATA CLASSES
# =============================================================================

class Priority(Enum):
    CRITICAL = 'critical'    # Do immediately
    HIGH = 'high'            # Do this week
    MEDIUM = 'medium'        # Do this month
    LOW = 'low'              # Nice to have

class ImprovementCategory(Enum):
    SYSTEM = 'system'
    RESEARCH = 'research'
    WORKFLOW = 'workflow'
    THEORY = 'theory'

@dataclass
class Improvement:
    """A suggested improvement."""
    category: ImprovementCategory
    priority: Priority
    title: str
    description: str
    effort: str  # "quick", "moderate", "significant"
    impact: str  # "low", "medium", "high"
    implementation: str = ""
    evidence: List[str] = field(default_factory=list)

@dataclass
class ImprovementReport:
    """Collection of suggested improvements."""
    timestamp: datetime
    improvements: List[Improvement] = field(default_factory=list)
    summary: str = ""


# =============================================================================
# SUGGESTION GENERATORS
# =============================================================================

def suggest_system_improvements() -> List[Improvement]:
    """Suggest improvements to the HIRM system."""
    improvements = []
    
    # Check for recurring corrections that need automation
    corrections = get_recurring_corrections(min_count=2)
    
    for corr in corrections:
        if not corr.get('added_to_protocol'):
            improvements.append(Improvement(
                category=ImprovementCategory.SYSTEM,
                priority=Priority.HIGH if corr['recurrence_count'] >= 3 else Priority.MEDIUM,
                title=f"Automate check for '{corr['correction_type']}' errors",
                description=f"Error '{corr['original_text'][:30]}...' has occurred {corr['recurrence_count']} times",
                effort="quick",
                impact="medium",
                implementation=f"Add pattern check to quality_gate.py: '{corr['original_text']}' -> '{corr['corrected_text']}'",
                evidence=[f"Recurrence: {corr['recurrence_count']}"]
            ))
    
    # Check for empty database tables
    tables_to_check = ['documents', 'session_logs']
    for table in tables_to_check:
        count = query_db(f"SELECT COUNT(*) as c FROM {table}")[0]['c']
        if count == 0:
            improvements.append(Improvement(
                category=ImprovementCategory.SYSTEM,
                priority=Priority.LOW,
                title=f"Start populating '{table}' table",
                description=f"The {table} table is empty - not tracking {table.replace('_', ' ')}",
                effort="moderate",
                impact="medium",
                implementation=f"Update scripts to log to {table} table after each session/document"
            ))
    
    # Check script coverage
    expected_scripts = ['quality_gate.py', 'pattern_detector.py', 'corpus_sync.py',
                       'session_analyzer.py', 'improvement_suggester.py', 'orchestrator.py']
    scripts_dir = HIRM_ROOT / 'System' / 'scripts'
    existing = {f.name for f in scripts_dir.glob('*.py')}
    
    missing = set(expected_scripts) - existing
    if missing:
        improvements.append(Improvement(
            category=ImprovementCategory.SYSTEM,
            priority=Priority.HIGH,
            title="Create missing automation scripts",
            description=f"Missing scripts: {', '.join(missing)}",
            effort="significant",
            impact="high",
            implementation="Build remaining automation infrastructure"
        ))
    
    return improvements


def suggest_research_improvements() -> List[Improvement]:
    """Suggest improvements to the research corpus and content."""
    improvements = []
    
    # Check prediction testing status
    predictions = get_predictions()
    untested = [p for p in predictions if p.get('status') == 'untested']
    
    if len(untested) >= 2:
        improvements.append(Improvement(
            category=ImprovementCategory.RESEARCH,
            priority=Priority.HIGH,
            title="Test core HIRM predictions",
            description=f"{len(untested)} predictions remain untested",
            effort="significant",
            impact="high",
            implementation="Design and run empirical tests for: " + 
                         ', '.join(p['prediction_id'] for p in untested[:3]),
            evidence=[p['statement'][:50] for p in untested[:3]]
        ))
    
    # Check corpus coverage by domain
    papers = get_all_papers()
    if papers:
        from collections import Counter
        domains = Counter(p.get('domain', 'unclassified') for p in papers)
        
        # Check for underrepresented domains
        avg = sum(domains.values()) / len(domains) if domains else 0
        
        for domain, count in domains.items():
            if count < avg * 0.5 and count < 10:
                improvements.append(Improvement(
                    category=ImprovementCategory.RESEARCH,
                    priority=Priority.MEDIUM,
                    title=f"Expand '{domain}' corpus coverage",
                    description=f"Only {count} papers in {domain} (avg: {avg:.0f})",
                    effort="moderate",
                    impact="medium",
                    implementation=f"Search for and add key papers in {domain} domain"
                ))
    
    # Check for papers not integrated
    not_integrated = [p for p in papers if p.get('status') in ['unread', 'read']]
    if len(not_integrated) > len(papers) * 0.3:
        improvements.append(Improvement(
            category=ImprovementCategory.RESEARCH,
            priority=Priority.MEDIUM,
            title="Integrate more corpus papers",
            description=f"{len(not_integrated)} papers not yet integrated into HIRM framework",
            effort="moderate",
            impact="medium",
            implementation="Schedule literature review sessions to integrate key papers",
            evidence=[p['title'][:40] for p in not_integrated[:5]]
        ))
    
    return improvements


def suggest_workflow_improvements() -> List[Improvement]:
    """Suggest workflow optimizations."""
    improvements = []
    
    # Check for session logging
    recent_sessions = query_db("SELECT COUNT(*) as c FROM session_logs")
    if recent_sessions[0]['c'] < 5:
        improvements.append(Improvement(
            category=ImprovementCategory.WORKFLOW,
            priority=Priority.MEDIUM,
            title="Improve session logging",
            description="Few sessions logged - losing valuable tracking data",
            effort="quick",
            impact="medium",
            implementation="Log all research sessions to SESSION_LOGS.md and database"
        ))
    
    # Check for quality gate usage
    docs = query_db("SELECT COUNT(*) as c FROM documents WHERE quality_score IS NOT NULL")
    if docs[0]['c'] == 0:
        improvements.append(Improvement(
            category=ImprovementCategory.WORKFLOW,
            priority=Priority.MEDIUM,
            title="Run quality gate on documents",
            description="No documents have quality scores - quality gate not being used",
            effort="quick",
            impact="high",
            implementation="Run 'python quality_gate.py --all' to check all documents"
        ))
    
    return improvements


def suggest_theory_improvements() -> List[Improvement]:
    """Suggest theoretical extensions and clarifications."""
    improvements = []
    
    # Check for constants without strong derivation
    constants = query_db("SELECT * FROM constants WHERE confidence = 'provisional'")
    
    for const in constants:
        improvements.append(Improvement(
            category=ImprovementCategory.THEORY,
            priority=Priority.LOW,
            title=f"Strengthen derivation for {const['symbol']}",
            description=f"Constant {const['symbol']} = {const['value']} is provisional",
            effort="significant",
            impact="medium",
            implementation="Seek independent derivation or empirical validation"
        ))
    
    # Check predictions without measurement protocols
    predictions = get_predictions()
    no_protocol = [p for p in predictions if not p.get('measurement_protocol')]
    
    if no_protocol:
        improvements.append(Improvement(
            category=ImprovementCategory.THEORY,
            priority=Priority.MEDIUM,
            title="Define measurement protocols for predictions",
            description=f"{len(no_protocol)} predictions lack measurement protocols",
            effort="moderate",
            impact="high",
            implementation="Specify exactly how to measure each prediction",
            evidence=[p['prediction_id'] for p in no_protocol]
        ))
    
    return improvements


# =============================================================================
# MAIN GENERATION
# =============================================================================

def generate_all_suggestions() -> ImprovementReport:
    """Generate all improvement suggestions."""
    report = ImprovementReport(timestamp=datetime.now())
    
    print("Generating improvement suggestions...")
    
    generators = [
        ("System", suggest_system_improvements),
        ("Research", suggest_research_improvements),
        ("Workflow", suggest_workflow_improvements),
        ("Theory", suggest_theory_improvements),
    ]
    
    for name, generator in generators:
        print(f"  Checking {name}...")
        try:
            improvements = generator()
            report.improvements.extend(improvements)
        except Exception as e:
            print(f"  Warning: {name} generator failed: {e}")
    
    # Sort by priority
    priority_order = {Priority.CRITICAL: 0, Priority.HIGH: 1, Priority.MEDIUM: 2, Priority.LOW: 3}
    report.improvements.sort(key=lambda x: priority_order[x.priority])
    
    # Generate summary
    by_priority = {}
    for imp in report.improvements:
        by_priority[imp.priority.value] = by_priority.get(imp.priority.value, 0) + 1
    
    report.summary = (
        f"Found {len(report.improvements)} improvements: " +
        ', '.join(f"{v} {k}" for k, v in by_priority.items())
    )
    
    return report


def format_improvement_report(report: ImprovementReport, priority_filter: Optional[Priority] = None) -> str:
    """Format improvement report as markdown."""
    output = [generate_report_header("Improvement Suggestions")]
    
    output.append(f"**{report.summary}**\n")
    output.append("---\n")
    
    improvements = report.improvements
    if priority_filter:
        improvements = [i for i in improvements if i.priority == priority_filter]
    
    # Group by category
    by_category = {}
    for imp in improvements:
        cat = imp.category.value
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(imp)
    
    category_labels = {
        'system': '[SYSTEM]',
        'research': '[RESEARCH]',
        'workflow': '[WORKFLOW]',
        'theory': '[THEORY]'
    }
    
    priority_labels = {
        Priority.CRITICAL: '[CRITICAL]',
        Priority.HIGH: '[HIGH]',
        Priority.MEDIUM: '[MEDIUM]',
        Priority.LOW: '[LOW]'
    }
    
    for category, imps in by_category.items():
        label = category_labels.get(category, '[OTHER]')
        output.append(f"## {label} {category.title()} Improvements\n")
        
        for imp in imps:
            p_label = priority_labels.get(imp.priority, '[?]')
            output.append(f"### {p_label} {imp.title}")
            output.append(f"**Priority:** {imp.priority.value} | **Effort:** {imp.effort} | **Impact:** {imp.impact}")
            output.append(f"\n{imp.description}\n")
            
            if imp.implementation:
                output.append(f"**How to implement:** {imp.implementation}")
            
            if imp.evidence:
                output.append("\n**Evidence:**")
                for e in imp.evidence[:3]:
                    output.append(f"- {e}")
            
            output.append("\n---\n")
    
    if not improvements:
        output.append("\n[OK] No improvements needed at this time!")
    
    return '\n'.join(output)


# =============================================================================
# COMMAND LINE INTERFACE
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='HIRM Improvement Suggester - Generate system improvement suggestions'
    )
    parser.add_argument('--system', action='store_true', help='System improvements only')
    parser.add_argument('--research', action='store_true', help='Research improvements only')
    parser.add_argument('--priority', choices=['critical', 'high', 'medium', 'low'],
                       help='Filter by priority')
    parser.add_argument('--output', '-o', help='Write report to file')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    if args.system:
        improvements = suggest_system_improvements()
        report = ImprovementReport(timestamp=datetime.now(), improvements=improvements)
    elif args.research:
        improvements = suggest_research_improvements()
        report = ImprovementReport(timestamp=datetime.now(), improvements=improvements)
    else:
        report = generate_all_suggestions()
    
    priority_filter = Priority(args.priority) if args.priority else None
    
    if args.json:
        output = json.dumps({
            'timestamp': report.timestamp.isoformat(),
            'improvements': [
                {
                    'category': i.category.value,
                    'priority': i.priority.value,
                    'title': i.title,
                    'description': i.description,
                    'effort': i.effort,
                    'impact': i.impact
                }
                for i in report.improvements
            ],
            'summary': report.summary
        }, indent=2)
        print(output)
    else:
        output = format_improvement_report(report, priority_filter)
        print(output)
        
        if args.output:
            Path(args.output).write_text(output)
            print(f"\nReport written to: {args.output}")


if __name__ == '__main__':
    main()
