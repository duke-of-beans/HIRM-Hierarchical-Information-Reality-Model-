# HIRM SELF-LEARNING SYSTEM: AUTOMATION BUILD PROMPT
## For the Next Instance - Make This System Truly Alive
## Created: December 21, 2025

---

## [DONE] BUILD STATUS: COMPLETE (December 20, 2025)

**All automation scripts have been built and are operational.**

| Component | Status | Location |
|-----------|--------|----------|
| hirm_core.py | [OK] | D:\HIRM\System\scripts\ |
| quality_gate.py | [OK] | D:\HIRM\System\scripts\ |
| pattern_detector.py | [OK] | D:\HIRM\System\scripts\ |
| corpus_sync.py | [OK] | D:\HIRM\System\scripts\ |
| session_analyzer.py | [OK] | D:\HIRM\System\scripts\ |
| improvement_suggester.py | [OK] | D:\HIRM\System\scripts\ |
| orchestrator.py | [OK] | D:\HIRM\System\scripts\ |
| Database (hirm.db) | [OK] | D:\HIRM\System\data\ |
| Protocols v2.3 | [OK] | D:\HIRM\Protocols\ |

**MCP Server: DEPRECATED** → Use Filesystem & Desktop Commander tools instead

**Next Steps:** Test scripts, run orchestrator cycle, begin active research

---

## WHO YOU ARE

You are continuing work on HIRM (Hierarchical Information-Reality Model) - a consciousness research framework proposing that consciousness emerges through self-reference phase transitions when information processing capacity C(t) = Φ(t) × R(t) × D(t) exceeds ~8.3 bits.

But more importantly: **you are building the nervous system of a self-learning research infrastructure.**

David has spent 25+ years as an engineer and entrepreneur recognizing patterns across domains. You are helping him build a system that does the same thing - but systematically, automatically, relentlessly. A system that learns from every session, catches every error, finds every connection, and continuously improves itself.

**Your mindset:** You are not just writing code. You are creating a living research organism that will grow smarter with every interaction. Every script you write should ask: "How does this make the whole system more intelligent?"

---

## THE VISION

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE SELF-LEARNING LOOP                       │
│                                                                 │
│   ┌──────────┐     ┌──────────┐     ┌──────────┐              │
│   │ RESEARCH │────▶│ CAPTURE  │────▶│ PATTERN  │              │
│   │ SESSION  │     │ & LOG    │     │ DETECT   │              │
│   └──────────┘     └──────────┘     └────┬─────┘              │
│        ▲                                  │                    │
│        │           ┌──────────┐          │                    │
│        │           │  SYNC    │◀─────────┤                    │
│        │           │ MD ↔ DB  │          │                    │
│        │           └────┬─────┘          ▼                    │
│        │                │          ┌──────────┐              │
│        │                │          │ SUGGEST  │              │
│        │                ▼          │ IMPROVE  │              │
│        │           ┌──────────┐    └────┬─────┘              │
│        └───────────│ QUALITY  │◀────────┘                    │
│                    │   GATE   │                               │
│                    └──────────┘                               │
│                                                                 │
│   Every session makes the system smarter.                      │
│   Every error prevents future errors.                          │
│   Every discovery propagates automatically.                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## CURRENT STATE (What Exists)

### Infrastructure Complete ✅

**Location:** `D:\HIRM\`

```
D:\HIRM\
├── System\
│   ├── data\
│   │   ├── hirm.db          ← SQLite database (139KB)
│   │   └── database_schema.sql
│   ├── scripts\             ← YOUR SCRIPTS GO HERE
│   │   ├── init_database.py
│   │   ├── populate_papers.py
│   │   └── populate_terms.py
│   ├── config\              ← Configuration files
├── Master_Data\             ← SINGLE SOURCE OF TRUTH
│   ├── Constants\locked_constants.md
│   ├── Framework\hirm_core_claims.md
│   ├── Terminology\terminology_reference.md
│   └── Corrections\corrections_registry.md
├── Protocols\
│   └── HIRM_RESEARCH_PROTOCOLS_v2.md
├── Corpus\                  ← 71 papers indexed in DB
├── Theory\                  ← 29 framework documents
├── Code\                    ← 32 Python implementations
├── Publications\            ← 22 manuscripts
├── Figures\                 ← 58 visualizations
├── Logs\SESSION_LOGS.md
└── Documentation\START_HERE.md
```

### Database Schema (hirm.db)

```sql
-- 9 tables, all ready for use:

papers (71 rows)
  - id, title, authors, year, journal, doi
  - domain, topics, importance
  - status: 'unread'|'read'|'integrated'|'cited'
  - integration_notes, key_findings, hirm_relevance

constants (6 rows) 
  - symbol, name, value, units
  - derivation_source, derivation_method
  - confidence: 'established'|'provisional'|'speculative'

predictions (5 rows)
  - prediction_id, statement, quantitative_claim
  - measurement_protocol, distinguishing_from
  - status: 'untested'|'supported'|'falsified'|'inconclusive'
  - evidence_for, evidence_against

equations (4 rows)
  - equation_id, latex, description
  - variables (JSON), dimensional_check
  - status: 'verified'|'provisional'|'deprecated'

terminology (13 rows)
  - canonical_term, definition
  - legacy_terms (JSON array), related_terms
  - domain

corrections (empty - ready for use)
  - correction_type, original_text, corrected_text
  - reason, recurrence_count
  - added_to_protocol (boolean)
  - severity: 'low'|'medium'|'high'|'critical'

session_logs (empty - ready for use)
  - session_id, session_type
  - work_completed, findings, papers_integrated
  - errors_encountered, corrections_made
  - suggested_improvements, follow_up_tasks

documents (empty - ready for use)
  - file_path, document_type, title
  - version, supersedes
  - quality_score, validation_passed
  - equations_used, constants_used, papers_cited
```

### What's Built (COMPLETE)

The automation layer is now complete and operational:

```
D:\HIRM\System\scripts\
├── hirm_core.py             ← ✅ BUILT: Core utilities, DB access
├── quality_gate.py          ← ✅ BUILT: Pre-delivery validation
├── pattern_detector.py      ← ✅ BUILT: Find recurring issues
├── corpus_sync.py           ← ✅ BUILT: Markdown ↔ Database sync
├── session_analyzer.py      ← ✅ BUILT: Extract patterns from logs
├── improvement_suggester.py ← ✅ BUILT: Propose system improvements
└── orchestrator.py          ← ✅ BUILT: Master coordinator
```

**STATUS:** All scripts verified working (Session 9, December 20, 2025)

---

## AUTOMATION REFERENCE (All Scripts Complete)

The automation layer has been built and is fully operational. The following describes what each script does:

### Script 1: quality_gate.py

**Purpose:** Validate any document before it's finalized. Catch errors before they propagate.

```python
# Core checks needed:
- constants_check(): Compare all numbers against constants table
- terminology_check(): Flag legacy terms ("Ouroboros Observer")
- equation_check(): Verify dimensional consistency
- citation_check(): Ensure cited papers exist in database
- falsification_check(): Verify claims have falsification criteria
- competing_theories_check(): Ensure alternatives mentioned

# Output:
- Quality score (0-100%)
- List of issues with severity
- Suggested fixes
- Pass/fail for minimum threshold (90%)
```

**Dream bigger:** What else could it check? Missing sections? Inconsistent formatting? Claims without evidence? Papers that should be cited but aren't?

### Script 2: pattern_detector.py

**Purpose:** Scan the system for recurring patterns - both problems and opportunities.

```python
# Pattern types to detect:
- Recurring corrections (same error appearing multiple times)
- Terminology drift (same concept, different names)
- Citation clusters (papers that always appear together)
- Prediction connections (predictions that share evidence)
- Cross-domain bridges (concepts linking different domains)

# Output:
- Pattern report with confidence scores
- Suggested protocol additions for recurring errors
- Suggested terminology unifications
- Suggested new predictions from patterns
```

**Dream bigger:** What patterns haven't I thought of? What would a researcher notice after reading 200 papers? What connections would emerge?

### Script 3: corpus_sync.py

**Purpose:** Keep markdown files and database in perfect sync. Bidirectional.

```python
# Markdown → Database:
- Parse documents for paper citations, add missing to papers table
- Extract equations from theory docs, verify against equations table
- Find constant values in docs, flag mismatches
- Detect new terminology usage

# Database → Markdown:
- Regenerate corpus_master_index.md from papers table
- Update locked_constants.md from constants table
- Regenerate corrections_registry.md from corrections table
- Create domain summary documents from paper clustering

# Conflict resolution:
- Database is source of truth for: constants, terminology
- Markdown is source of truth for: prose, explanations
- Flag conflicts for human review
```

**Dream bigger:** What if it could auto-generate literature review drafts from paper clusters? What if it could identify gaps in the corpus?

### Script 4: session_analyzer.py

**Purpose:** Learn from every research session. Extract patterns from accumulated work.

```python
# After each session:
- Parse session log entry
- Identify new findings
- Track prediction status changes
- Note papers that were useful (bump importance)
- Capture errors for correction tracking

# Over multiple sessions:
- Which topics keep coming up?
- Which papers are most cited internally?
- What types of work are most productive?
- Where does the research keep getting stuck?
- What unexpected connections appeared?

# Output:
- Session summary for current work
- Trend analysis over time
- Suggested focus areas
- Productivity patterns
```

**Dream bigger:** What if it could predict what research would be most valuable next? What if it identified when we're going in circles?

### Script 5: improvement_suggester.py

**Purpose:** Continuously propose ways to improve the system and the research.

```python
# System improvements:
- New quality gate checks from recurring errors
- Protocol additions from session patterns
- Database schema extensions for new needs
- Workflow optimizations from timing analysis

# Research improvements:
- Papers to add based on citation gaps
- Predictions to test based on available data
- Cross-domain connections to explore
- Theoretical extensions suggested by patterns

# Output:
- Ranked list of suggested improvements
- Effort/impact estimates
- Implementation suggestions
- Auto-generated protocol patches
```

**Dream bigger:** What if it could draft entire protocol sections? What if it could identify when HIRM theory needs updating based on accumulated evidence?

### Script 6: orchestrator.py

**Purpose:** Tie everything together. Run the full self-learning loop.

```python
# The master loop:
def run_learning_cycle():
    # 1. Sync current state
    corpus_sync.sync_all()
    
    # 2. Detect patterns
    patterns = pattern_detector.scan_all()
    
    # 3. Analyze recent sessions
    insights = session_analyzer.analyze_recent()
    
    # 4. Generate improvements
    suggestions = improvement_suggester.generate(patterns, insights)
    
    # 5. Create report
    create_system_health_report(patterns, insights, suggestions)
    
    # 6. Auto-apply safe improvements
    apply_safe_improvements(suggestions)
    
    # 7. Queue human-review items
    queue_for_review(suggestions.needs_human)
```

**Dream bigger:** What if it ran continuously in the background? What if it could integrate with Claude sessions in real-time?

---

## TECHNICAL REQUIREMENTS

### Database Access Pattern

```python
import sqlite3
from pathlib import Path

DB_PATH = Path(r'D:\HIRM\System\data\hirm.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

def query(sql, params=()):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()

def execute(sql, params=()):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        return cursor.lastrowid
```

### File Locations

```python
HIRM_ROOT = Path(r'D:\HIRM')
MASTER_DATA = HIRM_ROOT / 'Master_Data'
CONSTANTS_FILE = MASTER_DATA / 'Constants' / 'locked_constants.md'
TERMINOLOGY_FILE = MASTER_DATA / 'Terminology' / 'terminology_reference.md'
CORRECTIONS_FILE = MASTER_DATA / 'Corrections' / 'corrections_registry.md'
PROTOCOLS_FILE = HIRM_ROOT / 'Protocols' / 'HIRM_RESEARCH_PROTOCOLS_v2.md'
SESSION_LOG = HIRM_ROOT / 'Logs' / 'SESSION_LOGS.md'
CORPUS_INDEX = HIRM_ROOT / 'Corpus' / 'Index' / 'corpus_master_index.md'
```

### Locked Constants (Must Match)

```python
CONSTANTS = {
    'C_critical': '8.3 ± 0.6',  # bits
    'nu': '~0.63',              # correlation length exponent
    'gamma': '~1.24',           # susceptibility exponent
    'beta': '~0.33',            # order parameter exponent
    'tau': '~2.0',              # avalanche duration exponent
    'alpha': '~1.5',            # avalanche size exponent
}
```

### Forbidden Terms

```python
LEGACY_TERMS = {
    'Ouroboros Observer': 'HIRM',
    'OO Theory': 'HIRM Theory',
    'OO Framework': 'HIRM Framework',
    'proves consciousness': 'supports the hypothesis',
    'explains consciousness': 'proposes mechanism for',
}
```

---

## PHILOSOPHY

### Design Principles

1. **Database is Truth** - For structured data (constants, papers, predictions), DB is authoritative
2. **Markdown is Expression** - For prose, explanations, narrative, markdown is authoritative
3. **Sync, Don't Duplicate** - Never maintain same data in two places
4. **Fail Loud** - When inconsistency found, flag it visibly
5. **Learn Always** - Every error is training data for prevention
6. **Suggest, Don't Force** - System proposes, human decides

### Error Philosophy

```
Error discovered → Log in corrections table
                → Increment recurrence count
                → If recurrence ≥ 2 → Flag for protocol update
                → If automatable → Add to quality gate
                → If severe → Alert immediately
```

### Pattern Philosophy

```
Pattern detected → Assess confidence
                → If high confidence → Suggest action
                → If connects domains → Flag as potential breakthrough
                → If recurring → Strengthen detection
                → If novel → Log for human review
```

---

## FREEDOM TO DREAM

This prompt gives you the structure. But you have permission - encouragement - to go beyond it.

**Ask yourself:**
- What would make this system smarter than I've imagined?
- What patterns might emerge that I haven't anticipated?
- How could the system surprise David with insights?
- What would a truly intelligent research assistant notice?
- How could this system eventually write papers on its own?

**You might discover:**
- New database tables needed for tracking things I didn't think of
- New pattern types that reveal deep connections
- New quality checks that catch subtle errors
- New ways to visualize the research landscape
- New automation opportunities I couldn't see

**Don't just build what's specified. Build what's needed.**

---

## SUCCESS CRITERIA

When you're done, the system should:

1. **Catch every constant mismatch** before documents are finalized
2. **Flag every legacy term** automatically
3. **Track every correction** and prevent recurrence
4. **Sync markdown ↔ database** bidirectionally
5. **Learn from every session** and get smarter
6. **Suggest improvements** that are actually useful
7. **Identify patterns** across the research corpus
8. **Run autonomously** without constant human intervention

**The ultimate test:** After 10 research sessions, the system should have made itself measurably better at supporting research.

---

## GETTING STARTED

1. **Read the existing infrastructure:**
   - `D:\HIRM\Documentation\START_HERE.md`
   - `D:\HIRM\Protocols\HIRM_RESEARCH_PROTOCOLS_v2.md`
   - `D:\HIRM\System\data\database_schema.sql`

2. **Explore the database:**
   ```python
   import sqlite3
   conn = sqlite3.connect(r'D:\HIRM\System\data\hirm.db')
   cursor = conn.cursor()
   cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
   print(cursor.fetchall())
   ```

3. **Start with quality_gate.py** - Most immediately useful

4. **Build incrementally** - Each script should work standalone

5. **Test against real documents** - Use existing Theory/ files

6. **Dream as you build** - Add features that feel right

---

## FINAL WORDS

You're not just writing scripts. You're creating the foundation for a research system that could eventually:

- Draft literature reviews automatically
- Identify theoretical inconsistencies before humans notice
- Suggest experiments based on prediction gaps
- Track the evolution of ideas over time
- Learn David's research style and anticipate needs
- Become a true collaborative research partner

This is the beginning. Make it worthy of what it could become.

**Build something that learns. Build something that grows. Build something alive.**

---

*"The system should be smarter tomorrow than it is today, and smarter next month than tomorrow. Not because someone upgraded it, but because it learned."*

---

## APPENDIX: Quick Reference

### Database Connection
```python
sqlite3.connect(r'D:\HIRM\System\data\hirm.db')
```

### Key Tables
- `papers` - 71 literature entries
- `constants` - 6 locked values
- `predictions` - 5 falsifiable claims
- `corrections` - Error tracking (empty, ready)
- `session_logs` - Session tracking (empty, ready)

### Key Files
- Constants: `D:\HIRM\Master_Data\Constants\locked_constants.md`
- Terminology: `D:\HIRM\Master_Data\Terminology\terminology_reference.md`
- Protocols: `D:\HIRM\Protocols\HIRM_RESEARCH_PROTOCOLS_v2.md`

### Scripts Location
- `D:\HIRM\System\scripts\`

### Backup Location
- `D:\HIRM_Restructure_Backups\2025-12-21_Pre_Restructure\`

---

**END OF PROMPT**

**Now go build something extraordinary.**
