#!/usr/bin/env python3
"""
HIRM Core Utilities
==================
Shared utilities for all HIRM automation scripts.
Provides database access, file paths, and common patterns.

Created: 2025-12-20
Version: 1.0
"""

import sqlite3
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum

# =============================================================================
# PATH CONFIGURATION
# =============================================================================

HIRM_ROOT = Path(r'D:\HIRM')
SYSTEM_DIR = HIRM_ROOT / 'System'
DATA_DIR = SYSTEM_DIR / 'data'
SCRIPTS_DIR = SYSTEM_DIR / 'scripts'
CONFIG_DIR = SYSTEM_DIR / 'config'

MASTER_DATA = HIRM_ROOT / 'Master_Data'
CONSTANTS_FILE = MASTER_DATA / 'Constants' / 'locked_constants.md'
TERMINOLOGY_FILE = MASTER_DATA / 'Terminology' / 'terminology_reference.md'
CORRECTIONS_FILE = MASTER_DATA / 'Corrections' / 'corrections_registry.md'
FRAMEWORK_FILE = MASTER_DATA / 'Framework' / 'hirm_core_claims.md'

PROTOCOLS_FILE = HIRM_ROOT / 'Protocols' / 'HIRM_RESEARCH_PROTOCOLS_v2.md'
SESSION_LOG_FILE = HIRM_ROOT / 'Logs' / 'SESSION_LOGS.md'
CORPUS_INDEX = HIRM_ROOT / 'Corpus' / 'Index' / 'corpus_master_index.md'

DB_PATH = DATA_DIR / 'hirm.db'

# =============================================================================
# ENUMERATIONS
# =============================================================================

class Severity(Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    CRITICAL = 'critical'

class Confidence(Enum):
    ESTABLISHED = 'established'
    PROVISIONAL = 'provisional'
    SPECULATIVE = 'speculative'
    DEPRECATED = 'deprecated'

class IssueType(Enum):
    CONSTANT_MISMATCH = 'constant_mismatch'
    LEGACY_TERMINOLOGY = 'legacy_terminology'
    EQUATION_ERROR = 'equation_error'
    MISSING_FALSIFICATION = 'missing_falsification'
    MISSING_ALTERNATIVES = 'missing_alternatives'
    CITATION_ERROR = 'citation_error'
    CLAIM_TOO_STRONG = 'claim_too_strong'
    DIMENSIONAL_ERROR = 'dimensional_error'

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class Issue:
    """Represents a quality issue found in a document."""
    issue_type: IssueType
    severity: Severity
    message: str
    line_number: Optional[int] = None
    original_text: Optional[str] = None
    suggested_fix: Optional[str] = None
    context: Optional[str] = None

@dataclass
class QualityReport:
    """Quality gate assessment report."""
    file_path: Path
    timestamp: datetime
    passed: bool
    score: float  # 0-100
    issues: List[Issue] = field(default_factory=list)
    checks_performed: List[str] = field(default_factory=list)
    summary: str = ""

# =============================================================================
# DATABASE ACCESS
# =============================================================================

def get_db_connection() -> sqlite3.Connection:
    """Get a connection to the HIRM database."""
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found at {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn

def query_db(sql: str, params: tuple = ()) -> List[sqlite3.Row]:
    """Execute a SELECT query and return results."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()

def execute_db(sql: str, params: tuple = ()) -> int:
    """Execute an INSERT/UPDATE/DELETE and return lastrowid."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        return cursor.lastrowid

def execute_many_db(sql: str, params_list: List[tuple]) -> int:
    """Execute multiple statements."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.executemany(sql, params_list)
        conn.commit()
        return cursor.rowcount

# =============================================================================
# CONSTANT RETRIEVAL
# =============================================================================

def get_locked_constants() -> Dict[str, Dict[str, Any]]:
    """Retrieve all locked constants from database."""
    rows = query_db("SELECT symbol, name, value, units, confidence FROM constants")
    return {
        row['symbol']: {
            'name': row['name'],
            'value': row['value'],
            'units': row['units'],
            'confidence': row['confidence']
        }
        for row in rows
    }

def get_constant(symbol: str) -> Optional[Dict[str, Any]]:
    """Get a specific constant by symbol."""
    rows = query_db(
        "SELECT symbol, name, value, units, confidence FROM constants WHERE symbol = ?",
        (symbol,)
    )
    if rows:
        row = rows[0]
        return {
            'symbol': row['symbol'],
            'name': row['name'],
            'value': row['value'],
            'units': row['units'],
            'confidence': row['confidence']
        }
    return None

# =============================================================================
# TERMINOLOGY RETRIEVAL
# =============================================================================

def get_legacy_terms() -> Dict[str, str]:
    """Get mapping of legacy terms to canonical terms."""
    rows = query_db("SELECT canonical_term, legacy_terms FROM terminology")
    legacy_map = {}
    for row in rows:
        if row['legacy_terms']:
            try:
                legacy_list = json.loads(row['legacy_terms'])
                for legacy in legacy_list:
                    legacy_map[legacy.lower()] = row['canonical_term']
            except json.JSONDecodeError:
                pass
    return legacy_map

def get_canonical_terms() -> Dict[str, str]:
    """Get all canonical terms with definitions."""
    rows = query_db("SELECT canonical_term, definition FROM terminology")
    return {row['canonical_term']: row['definition'] for row in rows}


# =============================================================================
# FORBIDDEN PATTERNS
# =============================================================================

# Legacy terminology that should never be used
FORBIDDEN_TERMS = {
    'ouroboros observer': ('HIRM', Severity.MEDIUM),
    'ouroboros': ('HIRM', Severity.MEDIUM),
    'oo theory': ('HIRM Theory', Severity.MEDIUM),
    'oo framework': ('HIRM Framework', Severity.MEDIUM),
    'the observer model': ('HIRM', Severity.LOW),
}

# Claims that are too strong
FORBIDDEN_CLAIMS = {
    'proves consciousness': ('supports the hypothesis that', Severity.HIGH),
    'proven to': ('evidence suggests', Severity.HIGH),
    'definitively shows': ('evidence supports', Severity.MEDIUM),
    'explains consciousness': ('proposes mechanism for consciousness emergence', Severity.MEDIUM),
    'the theory is correct': ('evidence supports the theory', Severity.MEDIUM),
    'demonstrates that consciousness': ('provides evidence consistent with', Severity.MEDIUM),
}

# Known constant variations that are WRONG
WRONG_CONSTANTS = {
    'c_critical = 7.5': ('C_critical = 8.3 ± 0.6', Severity.HIGH),
    'c_critical = 10': ('C_critical = 8.3 ± 0.6', Severity.HIGH),
    'c = 7.5': ('C = 8.3 ± 0.6', Severity.HIGH),
    'threshold of 7.5': ('threshold of 8.3 ± 0.6', Severity.HIGH),
    'c = φ + r + d': ('C = Φ × R × D', Severity.CRITICAL),
    'c(t) = φ(t) + r(t) + d(t)': ('C(t) = Φ(t) × R(t) × D(t)', Severity.CRITICAL),
}

# =============================================================================
# PAPER RETRIEVAL
# =============================================================================

def get_papers_by_domain(domain: str) -> List[Dict[str, Any]]:
    """Get all papers in a specific domain."""
    rows = query_db(
        "SELECT id, title, authors, year, journal, status FROM papers WHERE domain = ?",
        (domain,)
    )
    return [dict(row) for row in rows]

def get_paper_by_title(title_fragment: str) -> Optional[Dict[str, Any]]:
    """Find a paper by partial title match."""
    rows = query_db(
        "SELECT * FROM papers WHERE title LIKE ?",
        (f'%{title_fragment}%',)
    )
    if rows:
        return dict(rows[0])
    return None

def get_all_papers() -> List[Dict[str, Any]]:
    """Get all papers from database."""
    rows = query_db("SELECT * FROM papers ORDER BY year DESC, title")
    return [dict(row) for row in rows]

# =============================================================================
# PREDICTIONS RETRIEVAL
# =============================================================================

def get_predictions() -> List[Dict[str, Any]]:
    """Get all predictions from database."""
    rows = query_db("SELECT * FROM predictions")
    return [dict(row) for row in rows]

def get_prediction(prediction_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific prediction by ID."""
    rows = query_db(
        "SELECT * FROM predictions WHERE prediction_id = ?",
        (prediction_id,)
    )
    if rows:
        return dict(rows[0])
    return None

# =============================================================================
# EQUATIONS RETRIEVAL
# =============================================================================

def get_equations() -> List[Dict[str, Any]]:
    """Get all equations from database."""
    rows = query_db("SELECT * FROM equations")
    return [dict(row) for row in rows]

def get_equation(equation_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific equation by ID."""
    rows = query_db(
        "SELECT * FROM equations WHERE equation_id = ?",
        (equation_id,)
    )
    if rows:
        return dict(rows[0])
    return None

# =============================================================================
# CORRECTIONS MANAGEMENT
# =============================================================================

def log_correction(
    correction_type: str,
    original_text: str,
    corrected_text: str,
    reason: str,
    severity: Severity = Severity.MEDIUM,
    source_session: str = None
) -> int:
    """Log a correction to the database."""
    # Check if this correction already exists
    existing = query_db(
        """SELECT id, recurrence_count FROM corrections 
           WHERE correction_type = ? AND original_text = ?""",
        (correction_type, original_text)
    )
    
    if existing:
        # Increment recurrence count
        execute_db(
            """UPDATE corrections 
               SET recurrence_count = recurrence_count + 1,
                   updated_at = CURRENT_TIMESTAMP
               WHERE id = ?""",
            (existing[0]['id'],)
        )
        return existing[0]['id']
    else:
        # Insert new correction
        return execute_db(
            """INSERT INTO corrections 
               (correction_type, original_text, corrected_text, reason, 
                severity, source_session)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (correction_type, original_text, corrected_text, reason,
             severity.value, source_session)
        )

def get_recurring_corrections(min_count: int = 2) -> List[Dict[str, Any]]:
    """Get corrections that have occurred multiple times."""
    rows = query_db(
        """SELECT * FROM corrections 
           WHERE recurrence_count >= ?
           ORDER BY recurrence_count DESC""",
        (min_count,)
    )
    return [dict(row) for row in rows]

# =============================================================================
# SESSION LOG MANAGEMENT
# =============================================================================

def log_session(
    session_type: str,
    work_completed: List[str],
    findings: List[str] = None,
    papers_integrated: List[str] = None,
    errors_encountered: str = None,
    corrections_made: str = None,
    suggested_improvements: str = None,
    follow_up_tasks: List[str] = None
) -> int:
    """Log a research session to database."""
    session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
    return execute_db(
        """INSERT INTO session_logs 
           (session_id, session_type, work_completed, findings, 
            papers_integrated, errors_encountered, corrections_made,
            suggested_improvements, follow_up_tasks)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            session_id,
            session_type,
            json.dumps(work_completed),
            json.dumps(findings) if findings else None,
            json.dumps(papers_integrated) if papers_integrated else None,
            errors_encountered,
            corrections_made,
            suggested_improvements,
            json.dumps(follow_up_tasks) if follow_up_tasks else None
        )
    )

def get_recent_sessions(limit: int = 10) -> List[Dict[str, Any]]:
    """Get the most recent sessions."""
    rows = query_db(
        """SELECT * FROM session_logs 
           ORDER BY created_at DESC LIMIT ?""",
        (limit,)
    )
    return [dict(row) for row in rows]

# =============================================================================
# DOCUMENT TRACKING
# =============================================================================

def register_document(
    file_path: Path,
    document_type: str,
    title: str = None,
    quality_score: float = None,
    validation_passed: bool = None
) -> int:
    """Register a document in the database."""
    rel_path = str(file_path.relative_to(HIRM_ROOT) if file_path.is_absolute() else file_path)
    
    # Check if document already exists
    existing = query_db(
        "SELECT id FROM documents WHERE file_path = ?",
        (rel_path,)
    )
    
    if existing:
        execute_db(
            """UPDATE documents 
               SET updated_at = CURRENT_TIMESTAMP,
                   quality_score = COALESCE(?, quality_score),
                   validation_passed = COALESCE(?, validation_passed)
               WHERE id = ?""",
            (quality_score, validation_passed, existing[0]['id'])
        )
        return existing[0]['id']
    else:
        return execute_db(
            """INSERT INTO documents 
               (file_path, document_type, title, quality_score, validation_passed)
               VALUES (?, ?, ?, ?, ?)""",
            (rel_path, document_type, title, quality_score, validation_passed)
        )

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def find_hirm_files(
    directory: Path = HIRM_ROOT,
    extensions: List[str] = None,
    exclude_dirs: List[str] = None
) -> List[Path]:
    """Find all relevant files in HIRM directory."""
    if extensions is None:
        extensions = ['.md', '.py', '.txt']
    if exclude_dirs is None:
        exclude_dirs = ['_Archive', '_Backups', '.git', '__pycache__', 'Temp']
    
    files = []
    for ext in extensions:
        for file_path in directory.rglob(f'*{ext}'):
            # Skip excluded directories
            if not any(excl in file_path.parts for excl in exclude_dirs):
                files.append(file_path)
    return files

def extract_numbers_from_text(text: str) -> List[Tuple[str, float]]:
    """Extract numerical values with context from text."""
    # Pattern to find numbers with optional units
    pattern = r'(?:(?:C_?critical|threshold|C\s*[=≈])\s*[≈=]?\s*)?(\d+\.?\d*)\s*(?:±\s*\d+\.?\d*)?\s*(bits?)?'
    matches = re.findall(pattern, text, re.IGNORECASE)
    return [(m[0], float(m[0])) for m in matches if m[0]]

def normalize_text_for_comparison(text: str) -> str:
    """Normalize text for case-insensitive comparison."""
    return ' '.join(text.lower().split())

# =============================================================================
# REPORT GENERATION
# =============================================================================

def generate_report_header(title: str) -> str:
    """Generate a standard report header."""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f"""# {title}
## Generated: {now}
## HIRM Research System

---

"""

def format_issue_for_report(issue: Issue) -> str:
    """Format an issue for inclusion in a report."""
    lines = [f"### [{issue.severity.value.upper()}] {issue.issue_type.value}"]
    lines.append(f"**Message:** {issue.message}")
    if issue.line_number:
        lines.append(f"**Line:** {issue.line_number}")
    if issue.original_text:
        lines.append(f"**Found:** `{issue.original_text}`")
    if issue.suggested_fix:
        lines.append(f"**Fix:** `{issue.suggested_fix}`")
    lines.append("")
    return '\n'.join(lines)


if __name__ == '__main__':
    # Test database connection
    print("Testing HIRM Core Utilities...")
    
    constants = get_locked_constants()
    print(f"[OK] Loaded {len(constants)} constants")
    
    legacy = get_legacy_terms()
    print(f"[OK] Loaded {len(legacy)} legacy term mappings")
    
    papers = get_all_papers()
    print(f"[OK] Found {len(papers)} papers in database")
    
    predictions = get_predictions()
    print(f"[OK] Found {len(predictions)} predictions")
    
    print("\nHIRM Core utilities loaded successfully!")
