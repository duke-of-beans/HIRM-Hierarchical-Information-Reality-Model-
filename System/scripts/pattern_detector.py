#!/usr/bin/env python3
"""
HIRM Pattern Detector
=====================
Scans the HIRM system for recurring patterns - both problems and opportunities.

Pattern types detected:
1. Recurring corrections (same error appearing multiple times)
2. Terminology drift (same concept, different names)
3. Citation clusters (papers that always appear together)
4. Prediction connections (predictions that share evidence)
5. Cross-domain bridges (concepts linking different domains)
6. Topic frequencies (what the research focuses on)

Usage:
    python pattern_detector.py              # Full scan
    python pattern_detector.py --corrections # Focus on corrections
    python pattern_detector.py --citations   # Focus on citation patterns
    python pattern_detector.py --output report.md

Created: 2025-12-20
Version: 1.0
"""

import argparse
import re
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple, Set
from collections import Counter, defaultdict
from datetime import datetime
from dataclasses import dataclass, field

from hirm_core import (
    HIRM_ROOT, get_recurring_corrections, get_all_papers, get_predictions,
    find_hirm_files, query_db, get_legacy_terms,
    generate_report_header, Severity
)

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class Pattern:
    """Represents a detected pattern."""
    pattern_type: str
    confidence: float  # 0-1
    description: str
    evidence: List[str] = field(default_factory=list)
    action_suggested: str = ""
    severity: str = "info"  # info, warning, action_required

@dataclass
class PatternReport:
    """Collection of detected patterns."""
    timestamp: datetime
    patterns: List[Pattern] = field(default_factory=list)
    summary: str = ""
    statistics: Dict[str, Any] = field(default_factory=dict)

# =============================================================================
# CORRECTION PATTERN DETECTION
# =============================================================================

def detect_correction_patterns() -> List[Pattern]:
    """Detect patterns in recurring corrections."""
    patterns = []
    
    corrections = get_recurring_corrections(min_count=1)
    
    if not corrections:
        return patterns
    
    # Group by correction type
    by_type = defaultdict(list)
    for corr in corrections:
        by_type[corr['correction_type']].append(corr)
    
    # Analyze each type
    for corr_type, items in by_type.items():
        total_recurrence = sum(c['recurrence_count'] for c in items)
        
        if total_recurrence >= 3:
            patterns.append(Pattern(
                pattern_type="recurring_correction",
                confidence=min(1.0, total_recurrence / 10),
                description=f"'{corr_type}' errors keep recurring ({total_recurrence} instances)",
                evidence=[f"{c['original_text']} -> {c['corrected_text']}" for c in items[:5]],
                action_suggested="Add automated check to quality_gate.py",
                severity="action_required" if total_recurrence >= 5 else "warning"
            ))
    
    # Check for terminology drift (similar corrections)
    term_corrections = [c for c in corrections if c['correction_type'] == 'terminology']
    if len(term_corrections) > 1:
        patterns.append(Pattern(
            pattern_type="terminology_drift",
            confidence=0.8,
            description="Multiple terminology corrections suggest naming inconsistency",
            evidence=[c['original_text'] for c in term_corrections],
            action_suggested="Review terminology_reference.md for completeness",
            severity="warning"
        ))
    
    return patterns


# =============================================================================
# CITATION PATTERN DETECTION
# =============================================================================

def detect_citation_patterns() -> List[Pattern]:
    """Detect patterns in how papers are cited together."""
    patterns = []
    papers = get_all_papers()
    
    if not papers:
        return patterns
    
    # Analyze domain distribution
    domain_counts = Counter(p['domain'] for p in papers if p.get('domain'))
    
    # Check for domain imbalance
    if domain_counts:
        most_common = domain_counts.most_common(1)[0]
        least_common = domain_counts.most_common()[-1]
        
        if most_common[1] > 3 * least_common[1] and least_common[1] < 10:
            patterns.append(Pattern(
                pattern_type="corpus_imbalance",
                confidence=0.7,
                description=f"Domain '{least_common[0]}' underrepresented in corpus",
                evidence=[f"{d}: {c} papers" for d, c in domain_counts.most_common()],
                action_suggested=f"Add more papers from '{least_common[0]}' domain",
                severity="info"
            ))
    
    # Check for papers that are frequently cited together (co-citation)
    files = find_hirm_files(extensions=['.md'])
    paper_cooccurrence = defaultdict(Counter)
    
    for file_path in files[:50]:  # Limit to avoid timeout
        try:
            content = file_path.read_text(encoding='utf-8').lower()
            cited_papers = []
            
            for paper in papers:
                # Check if paper's first author or title fragment is mentioned
                title_words = paper['title'].lower().split()[:3]
                if any(word in content for word in title_words if len(word) > 4):
                    cited_papers.append(paper['id'])
            
            # Record co-occurrences
            for i, p1 in enumerate(cited_papers):
                for p2 in cited_papers[i+1:]:
                    paper_cooccurrence[p1][p2] += 1
                    paper_cooccurrence[p2][p1] += 1
        except:
            continue
    
    # Find strongly co-cited papers
    strong_pairs = []
    for p1, coauthors in paper_cooccurrence.items():
        for p2, count in coauthors.items():
            if count >= 3 and p1 < p2:
                strong_pairs.append((p1, p2, count))
    
    if strong_pairs:
        patterns.append(Pattern(
            pattern_type="citation_cluster",
            confidence=0.8,
            description=f"Found {len(strong_pairs)} pairs of papers frequently cited together",
            evidence=[f"Paper {p1} + Paper {p2}: {c} times" for p1, p2, c in strong_pairs[:5]],
            action_suggested="Consider synthesizing these clusters into review documents",
            severity="info"
        ))
    
    return patterns


# =============================================================================
# TOPIC PATTERN DETECTION
# =============================================================================

def detect_topic_patterns() -> List[Pattern]:
    """Detect topic frequency and coverage patterns."""
    patterns = []
    
    # Key HIRM topics to track
    key_topics = {
        'criticality': ['critical', 'criticality', 'phase transition', 'edge of chaos'],
        'integration': ['integrated information', 'phi', 'Φ', 'integration'],
        'self_reference': ['self-reference', 'recursive', 'self-model', 'R(t)'],
        'dimensional': ['dimensional', 'dimension', 'D(t)', 'complexity'],
        'threshold': ['threshold', 'C_critical', '8.3', 'critical value'],
        'empirical': ['EEG', 'fMRI', 'anesthesia', 'sleep', 'experimental'],
        'quantum': ['quantum', 'decoherence', 'measurement', 'wave function'],
        'clinical': ['DOC', 'coma', 'consciousness disorder', 'patient'],
    }
    
    topic_mentions = Counter()
    topic_files = defaultdict(list)
    
    files = find_hirm_files(extensions=['.md'])
    
    for file_path in files:
        try:
            content = file_path.read_text(encoding='utf-8').lower()
            
            for topic, keywords in key_topics.items():
                count = sum(content.count(kw.lower()) for kw in keywords)
                if count > 0:
                    topic_mentions[topic] += count
                    topic_files[topic].append(file_path.name)
        except:
            continue
    
    # Check for underrepresented topics
    if topic_mentions:
        avg_mentions = sum(topic_mentions.values()) / len(topic_mentions)
        
        for topic, count in topic_mentions.items():
            if count < avg_mentions * 0.3:
                patterns.append(Pattern(
                    pattern_type="topic_underrepresented",
                    confidence=0.6,
                    description=f"Topic '{topic}' appears less frequently than average",
                    evidence=[f"{topic}: {count} mentions vs avg {avg_mentions:.0f}"],
                    action_suggested=f"Consider expanding coverage of '{topic}' in documentation",
                    severity="info"
                ))
    
    # Check for topic without empirical coverage
    if topic_mentions.get('empirical', 0) < topic_mentions.get('criticality', 0) * 0.3:
        patterns.append(Pattern(
            pattern_type="empirical_gap",
            confidence=0.7,
            description="Theoretical content significantly outweighs empirical validation",
            evidence=[
                f"Criticality mentions: {topic_mentions.get('criticality', 0)}",
                f"Empirical mentions: {topic_mentions.get('empirical', 0)}"
            ],
            action_suggested="Prioritize empirical validation work",
            severity="warning"
        ))
    
    return patterns


# =============================================================================
# CROSS-DOMAIN PATTERN DETECTION
# =============================================================================

def detect_crossdomain_patterns() -> List[Pattern]:
    """Detect cross-domain connections and bridges."""
    patterns = []
    
    # Domain keywords
    domains = {
        'physics': ['entropy', 'thermodynamic', 'quantum', 'critical exponent', 'scaling'],
        'neuroscience': ['neural', 'brain', 'EEG', 'cortex', 'neuron', 'synapse'],
        'information_theory': ['information', 'bits', 'entropy', 'mutual information'],
        'mathematics': ['topology', 'manifold', 'differential', 'renormalization'],
        'clinical': ['patient', 'anesthesia', 'coma', 'diagnosis', 'treatment'],
    }
    
    # Find files that bridge multiple domains
    bridge_files = []
    files = find_hirm_files(extensions=['.md'])
    
    for file_path in files:
        try:
            content = file_path.read_text(encoding='utf-8').lower()
            domains_present = []
            
            for domain, keywords in domains.items():
                if sum(content.count(kw.lower()) for kw in keywords) > 3:
                    domains_present.append(domain)
            
            if len(domains_present) >= 3:
                bridge_files.append((file_path.name, domains_present))
        except:
            continue
    
    if bridge_files:
        patterns.append(Pattern(
            pattern_type="cross_domain_bridge",
            confidence=0.9,
            description=f"Found {len(bridge_files)} documents bridging 3+ domains",
            evidence=[f"{name}: {', '.join(doms)}" for name, doms in bridge_files[:5]],
            action_suggested="These are key synthesis documents - ensure they're well-maintained",
            severity="info"
        ))
    
    # Check for isolated domains (domains that don't connect to others)
    domain_connections = defaultdict(set)
    
    for _, doms in bridge_files:
        for d1 in doms:
            for d2 in doms:
                if d1 != d2:
                    domain_connections[d1].add(d2)
    
    for domain in domains.keys():
        if domain not in domain_connections or len(domain_connections[domain]) < 2:
            patterns.append(Pattern(
                pattern_type="isolated_domain",
                confidence=0.5,
                description=f"Domain '{domain}' has limited cross-domain connections",
                evidence=[f"{domain} connects to: {domain_connections.get(domain, set())}"],
                action_suggested=f"Create bridge documents connecting '{domain}' to other domains",
                severity="info"
            ))
    
    return patterns


# =============================================================================
# PREDICTION PATTERN DETECTION
# =============================================================================

def detect_prediction_patterns() -> List[Pattern]:
    """Detect patterns in predictions and their testing status."""
    patterns = []
    predictions = get_predictions()
    
    if not predictions:
        return patterns
    
    # Count by status
    status_counts = Counter(p['status'] for p in predictions)
    
    # Check for untested predictions
    untested = status_counts.get('untested', 0)
    if untested > len(predictions) * 0.6:
        patterns.append(Pattern(
            pattern_type="untested_predictions",
            confidence=0.9,
            description=f"{untested} of {len(predictions)} predictions remain untested",
            evidence=[p['statement'][:50] for p in predictions if p['status'] == 'untested'],
            action_suggested="Prioritize empirical testing of core predictions",
            severity="action_required"
        ))
    
    # Check for predictions without quantitative claims
    vague_predictions = [p for p in predictions if not p.get('quantitative_claim')]
    if vague_predictions:
        patterns.append(Pattern(
            pattern_type="vague_predictions",
            confidence=0.7,
            description=f"{len(vague_predictions)} predictions lack quantitative claims",
            evidence=[p['prediction_id'] for p in vague_predictions],
            action_suggested="Add specific quantitative criteria to make predictions falsifiable",
            severity="warning"
        ))
    
    return patterns


# =============================================================================
# MAIN PATTERN SCAN
# =============================================================================

def run_full_scan() -> PatternReport:
    """Run all pattern detectors and compile report."""
    report = PatternReport(timestamp=datetime.now())
    
    print("Scanning for patterns...")
    
    # Run all detectors
    detectors = [
        ("Corrections", detect_correction_patterns),
        ("Citations", detect_citation_patterns),
        ("Topics", detect_topic_patterns),
        ("Cross-domain", detect_crossdomain_patterns),
        ("Predictions", detect_prediction_patterns),
    ]
    
    for name, detector in detectors:
        print(f"  Running {name} detector...")
        try:
            patterns = detector()
            report.patterns.extend(patterns)
        except Exception as e:
            print(f"  Warning: {name} detector failed: {e}")
    
    # Calculate statistics
    report.statistics = {
        'total_patterns': len(report.patterns),
        'action_required': sum(1 for p in report.patterns if p.severity == 'action_required'),
        'warnings': sum(1 for p in report.patterns if p.severity == 'warning'),
        'info': sum(1 for p in report.patterns if p.severity == 'info'),
        'high_confidence': sum(1 for p in report.patterns if p.confidence >= 0.8),
    }
    
    report.summary = (
        f"Found {report.statistics['total_patterns']} patterns: "
        f"{report.statistics['action_required']} require action, "
        f"{report.statistics['warnings']} warnings, "
        f"{report.statistics['info']} informational"
    )
    
    return report


def format_pattern_report(report: PatternReport) -> str:
    """Format pattern report as markdown."""
    output = [generate_report_header("Pattern Detection Report")]
    
    output.append(f"**Summary:** {report.summary}\n")
    output.append("---\n")
    
    # Group by severity
    for severity in ['action_required', 'warning', 'info']:
        patterns = [p for p in report.patterns if p.severity == severity]
        if patterns:
            emoji = {"action_required": "[ACTION]", "warning": "[WARN]", "info": "[INFO]"}[severity]
            output.append(f"## {emoji} {severity.replace('_', ' ').title()}\n")
            
            for pattern in patterns:
                output.append(f"### {pattern.pattern_type}")
                output.append(f"**Confidence:** {pattern.confidence:.0%}")
                output.append(f"\n{pattern.description}\n")
                
                if pattern.evidence:
                    output.append("**Evidence:**")
                    for e in pattern.evidence[:5]:
                        output.append(f"- {e}")
                    output.append("")
                
                if pattern.action_suggested:
                    output.append(f"**Suggested Action:** {pattern.action_suggested}\n")
                
                output.append("---\n")
    
    return '\n'.join(output)


# =============================================================================
# COMMAND LINE INTERFACE
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='HIRM Pattern Detector - Find recurring patterns in research'
    )
    parser.add_argument('--corrections', action='store_true',
                       help='Focus on correction patterns')
    parser.add_argument('--citations', action='store_true',
                       help='Focus on citation patterns')
    parser.add_argument('--output', '-o', help='Write report to file')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    if args.corrections:
        patterns = detect_correction_patterns()
        report = PatternReport(timestamp=datetime.now(), patterns=patterns)
    elif args.citations:
        patterns = detect_citation_patterns()
        report = PatternReport(timestamp=datetime.now(), patterns=patterns)
    else:
        report = run_full_scan()
    
    if args.json:
        import json
        output = json.dumps({
            'timestamp': report.timestamp.isoformat(),
            'patterns': [
                {
                    'type': p.pattern_type,
                    'confidence': p.confidence,
                    'description': p.description,
                    'severity': p.severity
                }
                for p in report.patterns
            ],
            'statistics': report.statistics
        }, indent=2)
    else:
        output = format_pattern_report(report)
    
    if args.output:
        Path(args.output).write_text(output)
        print(f"Report written to: {args.output}")
    else:
        print(output)


if __name__ == '__main__':
    main()
