#!/usr/bin/env python3
"""
HIRM Session Analyzer
=====================
Analyzes research sessions to extract patterns and insights.

Functions:
1. Parse session log entries
2. Track findings over time
3. Identify productive work patterns
4. Track prediction status changes
5. Note frequently used papers
6. Detect research momentum/stalls

Usage:
    python session_analyzer.py              # Analyze all sessions
    python session_analyzer.py --recent 5   # Analyze last 5 sessions
    python session_analyzer.py --topics     # Topic analysis
    python session_analyzer.py --output report.md

Created: 2025-12-20
Version: 1.0
"""

import argparse
import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from dataclasses import dataclass, field

from hirm_core import (
    HIRM_ROOT, SESSION_LOG_FILE, get_recent_sessions, query_db,
    get_predictions, generate_report_header
)

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class SessionInsight:
    """An insight derived from session analysis."""
    insight_type: str
    description: str
    confidence: float
    evidence: List[str] = field(default_factory=list)
    recommendation: str = ""

@dataclass
class SessionAnalysis:
    """Complete session analysis report."""
    timestamp: datetime
    sessions_analyzed: int
    insights: List[SessionInsight] = field(default_factory=list)
    topic_frequencies: Dict[str, int] = field(default_factory=dict)
    productivity_metrics: Dict[str, Any] = field(default_factory=dict)
    trends: List[str] = field(default_factory=list)

# =============================================================================
# SESSION PARSING
# =============================================================================

def parse_session_log_md() -> List[Dict[str, Any]]:
    """Parse SESSION_LOGS.md into structured data."""
    sessions = []
    
    if not SESSION_LOG_FILE.exists():
        return sessions
    
    content = SESSION_LOG_FILE.read_text(encoding='utf-8')
    
    # Split by session headers (### Session YYYY-MM-DD...)
    session_pattern = r'### Session (\d{4}-\d{2}-\d{2}[-_]\d+)[:\s]*(.*?)(?=### Session|\Z)'
    matches = re.findall(session_pattern, content, re.DOTALL)
    
    for session_id, session_content in matches:
        session = {
            'session_id': session_id,
            'raw_content': session_content,
            'type': None,
            'work_completed': [],
            'findings': [],
            'errors': [],
        }
        
        # Extract type
        type_match = re.search(r'type:\s*(\w+)', session_content)
        if type_match:
            session['type'] = type_match.group(1)
        
        # Extract work completed
        work_match = re.search(r'work_completed:\s*\n((?:\s*-.*\n?)+)', session_content)
        if work_match:
            session['work_completed'] = [
                line.strip().lstrip('- ') 
                for line in work_match.group(1).split('\n') 
                if line.strip().startswith('-')
            ]
        
        # Extract findings
        findings_match = re.search(r'findings:\s*\n((?:\s*-.*\n?)+)', session_content)
        if findings_match:
            session['findings'] = [
                line.strip().lstrip('- ') 
                for line in findings_match.group(1).split('\n') 
                if line.strip().startswith('-')
            ]
        
        sessions.append(session)
    
    return sessions


def get_all_sessions() -> List[Dict[str, Any]]:
    """Get sessions from both database and markdown."""
    # Get from database
    db_sessions = get_recent_sessions(limit=100)
    
    # Get from markdown
    md_sessions = parse_session_log_md()
    
    # Merge (database is primary)
    all_sessions = db_sessions.copy()
    
    # Add markdown sessions not in database
    db_ids = {s.get('session_id') for s in db_sessions if s.get('session_id')}
    for md_session in md_sessions:
        if md_session['session_id'] not in db_ids:
            all_sessions.append(md_session)
    
    return all_sessions


# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def analyze_topic_frequency(sessions: List[Dict[str, Any]]) -> Dict[str, int]:
    """Analyze what topics appear most frequently across sessions."""
    topic_keywords = {
        'criticality': ['critical', 'phase transition', 'avalanche'],
        'integration': ['phi', 'integration', 'Φ', 'integrated information'],
        'self_reference': ['self-reference', 'recursive', 'R(t)'],
        'empirical': ['EEG', 'data', 'experiment', 'validation', 'sleep'],
        'mathematical': ['equation', 'derivation', 'theorem', 'proof'],
        'clinical': ['anesthesia', 'DOC', 'patient', 'disorder'],
        'theoretical': ['theory', 'framework', 'model', 'hypothesis'],
        'literature': ['paper', 'review', 'corpus', 'citation'],
        'infrastructure': ['database', 'script', 'protocol', 'system'],
    }
    
    frequencies = Counter()
    
    for session in sessions:
        # Combine all text from session
        text = ' '.join([
            session.get('raw_content', ''),
            ' '.join(session.get('work_completed', [])),
            ' '.join(session.get('findings', [])),
        ]).lower()
        
        for topic, keywords in topic_keywords.items():
            if any(kw.lower() in text for kw in keywords):
                frequencies[topic] += 1
    
    return dict(frequencies.most_common())


def analyze_productivity(sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze productivity metrics from sessions."""
    metrics = {
        'total_sessions': len(sessions),
        'sessions_with_findings': 0,
        'avg_tasks_per_session': 0,
        'session_types': Counter(),
        'most_productive_type': None,
    }
    
    if not sessions:
        return metrics
    
    task_counts = []
    finding_counts = []
    
    for session in sessions:
        work = session.get('work_completed', [])
        findings = session.get('findings', [])
        session_type = session.get('type', 'unknown')
        
        if isinstance(work, str):
            try:
                work = json.loads(work)
            except:
                work = [work] if work else []
        
        if isinstance(findings, str):
            try:
                findings = json.loads(findings)
            except:
                findings = [findings] if findings else []
        
        task_counts.append(len(work))
        finding_counts.append(len(findings))
        
        if findings:
            metrics['sessions_with_findings'] += 1
        
        metrics['session_types'][session_type] += 1
    
    metrics['avg_tasks_per_session'] = sum(task_counts) / len(task_counts) if task_counts else 0
    metrics['avg_findings_per_session'] = sum(finding_counts) / len(finding_counts) if finding_counts else 0
    
    if metrics['session_types']:
        metrics['most_productive_type'] = metrics['session_types'].most_common(1)[0][0]
    
    return metrics


def detect_trends(sessions: List[Dict[str, Any]]) -> List[str]:
    """Detect trends in the research direction."""
    trends = []
    
    if len(sessions) < 2:
        return ["Insufficient data for trend analysis"]
    
    # Check for focus shifts
    recent = sessions[:len(sessions)//2]
    older = sessions[len(sessions)//2:]
    
    recent_topics = analyze_topic_frequency(recent)
    older_topics = analyze_topic_frequency(older)
    
    # Find growing topics
    for topic in set(recent_topics.keys()) | set(older_topics.keys()):
        recent_count = recent_topics.get(topic, 0)
        older_count = older_topics.get(topic, 0)
        
        if recent_count > older_count * 1.5 and recent_count >= 2:
            trends.append(f"[UP] Increasing focus on '{topic}'")
        elif older_count > recent_count * 1.5 and older_count >= 2:
            trends.append(f"[DOWN] Decreasing focus on '{topic}'")
    
    # Check session type patterns
    recent_types = Counter(s.get('type', 'unknown') for s in recent)
    older_types = Counter(s.get('type', 'unknown') for s in older)
    
    for stype in set(recent_types.keys()) | set(older_types.keys()):
        recent_count = recent_types.get(stype, 0)
        older_count = older_types.get(stype, 0)
        
        if recent_count > older_count + 2:
            trends.append(f"[SHIFT] More '{stype}' sessions recently")
    
    if not trends:
        trends.append("Research focus appears stable")
    
    return trends


def generate_insights(sessions: List[Dict[str, Any]], 
                     topic_freq: Dict[str, int],
                     metrics: Dict[str, Any],
                     trends: List[str]) -> List[SessionInsight]:
    """Generate actionable insights from analysis."""
    insights = []
    
    # Insight: Empirical work ratio
    empirical = topic_freq.get('empirical', 0)
    theoretical = topic_freq.get('theoretical', 0)
    
    if empirical < theoretical * 0.3 and theoretical > 3:
        insights.append(SessionInsight(
            insight_type="balance",
            description="Theoretical work significantly outpaces empirical validation",
            confidence=0.8,
            evidence=[f"Theoretical: {theoretical}, Empirical: {empirical}"],
            recommendation="Schedule dedicated empirical validation sessions"
        ))
    
    # Insight: Session productivity
    if metrics['avg_findings_per_session'] < 1:
        insights.append(SessionInsight(
            insight_type="productivity",
            description="Sessions averaging less than 1 finding each",
            confidence=0.7,
            evidence=[f"Avg findings: {metrics['avg_findings_per_session']:.1f}"],
            recommendation="Consider more focused session objectives"
        ))
    
    # Insight: Literature vs implementation
    lit = topic_freq.get('literature', 0)
    infra = topic_freq.get('infrastructure', 0)
    
    if lit > infra * 3 and lit > 5:
        insights.append(SessionInsight(
            insight_type="balance",
            description="Heavy literature focus, light implementation",
            confidence=0.6,
            evidence=[f"Literature: {lit}, Infrastructure: {infra}"],
            recommendation="Balance reading with building - implement ideas as you find them"
        ))
    
    # Insight: Prediction testing
    predictions = get_predictions()
    untested = sum(1 for p in predictions if p.get('status') == 'untested')
    if untested >= 3:
        insights.append(SessionInsight(
            insight_type="validation",
            description=f"{untested} predictions remain untested",
            confidence=0.9,
            evidence=[p['prediction_id'] for p in predictions if p.get('status') == 'untested'],
            recommendation="Prioritize testing core HIRM predictions"
        ))
    
    return insights


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def run_analysis(limit: Optional[int] = None) -> SessionAnalysis:
    """Run complete session analysis."""
    sessions = get_all_sessions()
    
    if limit and len(sessions) > limit:
        sessions = sessions[:limit]
    
    analysis = SessionAnalysis(
        timestamp=datetime.now(),
        sessions_analyzed=len(sessions)
    )
    
    # Run analyses
    analysis.topic_frequencies = analyze_topic_frequency(sessions)
    analysis.productivity_metrics = analyze_productivity(sessions)
    analysis.trends = detect_trends(sessions)
    analysis.insights = generate_insights(
        sessions, 
        analysis.topic_frequencies,
        analysis.productivity_metrics,
        analysis.trends
    )
    
    return analysis


def format_analysis_report(analysis: SessionAnalysis) -> str:
    """Format analysis as markdown report."""
    output = [generate_report_header("Session Analysis Report")]
    
    output.append(f"**Sessions Analyzed:** {analysis.sessions_analyzed}")
    output.append(f"**Analysis Date:** {analysis.timestamp.strftime('%Y-%m-%d %H:%M')}")
    output.append("\n---\n")
    
    # Productivity metrics
    output.append("## [METRICS] Productivity Metrics\n")
    m = analysis.productivity_metrics
    output.append(f"- Total sessions: {m.get('total_sessions', 0)}")
    output.append(f"- Sessions with findings: {m.get('sessions_with_findings', 0)}")
    output.append(f"- Avg tasks per session: {m.get('avg_tasks_per_session', 0):.1f}")
    output.append(f"- Avg findings per session: {m.get('avg_findings_per_session', 0):.1f}")
    output.append(f"- Most common session type: {m.get('most_productive_type', 'N/A')}")
    output.append("")
    
    # Topic frequencies
    output.append("## [TOPICS] Topic Focus\n")
    if analysis.topic_frequencies:
        for topic, count in analysis.topic_frequencies.items():
            bar = "#" * min(count, 20)
            output.append(f"- {topic}: {bar} ({count})")
    else:
        output.append("No topic data available")
    output.append("")
    
    # Trends
    output.append("## [TRENDS] Trends\n")
    for trend in analysis.trends:
        output.append(f"- {trend}")
    output.append("")
    
    # Insights
    output.append("## [INSIGHTS] Insights\n")
    if analysis.insights:
        for insight in analysis.insights:
            label = {"balance": "[BALANCE]", "productivity": "[GOAL]", "validation": "[VALIDATE]"}.get(
                insight.insight_type, "[NOTE]"
            )
            output.append(f"### {label} {insight.insight_type.title()}")
            output.append(f"**{insight.description}**")
            output.append(f"- Confidence: {insight.confidence:.0%}")
            if insight.evidence:
                output.append("- Evidence: " + ', '.join(str(e) for e in insight.evidence[:3]))
            if insight.recommendation:
                output.append(f"- **Recommendation:** {insight.recommendation}")
            output.append("")
    else:
        output.append("No significant insights detected")
    
    return '\n'.join(output)


# =============================================================================
# COMMAND LINE INTERFACE
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='HIRM Session Analyzer - Extract insights from research sessions'
    )
    parser.add_argument('--recent', '-r', type=int, 
                       help='Analyze only the N most recent sessions')
    parser.add_argument('--topics', action='store_true',
                       help='Focus on topic analysis')
    parser.add_argument('--output', '-o', help='Write report to file')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    print("Analyzing sessions...")
    analysis = run_analysis(limit=args.recent)
    
    if args.topics:
        # Just show topic frequencies
        print("\nTopic Frequencies:")
        for topic, count in analysis.topic_frequencies.items():
            bar = "#" * min(count, 30)
            print(f"  {topic:20s} {bar} ({count})")
    elif args.json:
        output = json.dumps({
            'timestamp': analysis.timestamp.isoformat(),
            'sessions_analyzed': analysis.sessions_analyzed,
            'topic_frequencies': analysis.topic_frequencies,
            'productivity_metrics': {k: v for k, v in analysis.productivity_metrics.items() 
                                    if not isinstance(v, Counter)},
            'trends': analysis.trends,
            'insights': [
                {'type': i.insight_type, 'description': i.description, 
                 'recommendation': i.recommendation}
                for i in analysis.insights
            ]
        }, indent=2)
        print(output)
    else:
        output = format_analysis_report(analysis)
        print(output)
        
        if args.output:
            Path(args.output).write_text(output)
            print(f"\nReport written to: {args.output}")


if __name__ == '__main__':
    main()
