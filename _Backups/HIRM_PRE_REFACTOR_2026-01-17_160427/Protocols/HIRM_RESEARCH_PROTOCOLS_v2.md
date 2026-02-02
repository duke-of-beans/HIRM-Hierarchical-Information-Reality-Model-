# HIRM RESEARCH PROTOCOLS v2.2
## Database-Backed Self-Learning Research System
## Hierarchical Information-Reality Model (HIRM) Framework

**Version:** 2.2  
**Release Date:** December 20, 2025  
**Project:** Consciousness Emergence Theory  
**Principal Investigator:** David  
**Status:** Production Ready

---

## WHAT'S NEW IN v2.2

### Key Upgrades from v2.0
1. **Complete automation suite** - 6 Python scripts for self-learning
2. **Quality gate automation** - Validates documents before delivery
3. **Pattern detection** - Automatically finds recurring issues
4. **Corpus synchronization** - Bidirectional markdown ↔ database sync
5. **Session analysis** - Extracts insights from research patterns
6. **Improvement suggestions** - Continuously proposes system enhancements
7. **Master orchestrator** - Runs complete self-learning cycles

### Upgrades from v1.0
1. **Database-backed system** - SQLite database (hirm.db) as central registry
2. **Self-healing corrections** - Errors logged and fed back into protocols
3. **Locked constants** - Single source of truth for all values
4. **Quality gates** - Automated validation before document finalization
5. **Structured directories** - 49-directory organization with clear roles
6. **Session logging** - All work tracked for continuity

### Philosophy Unchanged
- Rigorous falsification over confirmation
- Multiple competing hypotheses
- Empirical validation required
- Cross-disciplinary synthesis
- Intellectual honesty paramount

---

## SECTION 1: SYSTEM ARCHITECTURE

### 1.1 Directory Structure

```
D:\HIRM\
├── Master_Data\          [MASTER] SINGLE SOURCE OF TRUTH
│   ├── Constants\        -> locked_constants.md
│   ├── Framework\        -> hirm_core_claims.md, component_definitions.md
│   ├── Terminology\      -> terminology_reference.md
│   └── Corrections\      -> corrections_registry.md
├── System\               [SYSTEM] INFRASTRUCTURE
│   ├── data\             -> hirm.db (SQLite database)
│   ├── scripts\          -> Automation suite (see below)
│   └── config\           -> Configuration files
├── Protocols\            [PROTOCOLS] THIS DOCUMENT
├── Corpus\               [CORPUS] Literature (71+ papers indexed)
├── Theory\               [THEORY] Theoretical framework
├── Empirical\            [EMPIRICAL] Data & validation
├── Code\                 [CODE] Python implementations
├── Publications\         [PUBS] Manuscripts
├── Figures\              [FIGURES] Visualizations
├── Documentation\        [DOCS] Navigation
├── Logs\                 [LOGS] Session tracking
└── _Archive\             [ARCHIVE] Version history
```

### 1.2 The Database (hirm.db)

Central registry at `System/data/hirm.db`:

| Table | Purpose | Key Fields |
|-------|---------|------------|
| papers | Literature corpus (71+) | title, authors, domain, status |
| constants | Locked values (6) | symbol, value, confidence |
| predictions | Falsifiable claims (5) | statement, status, evidence |
| equations | Math expressions (4) | equation_id, latex, status |
| terminology | Canonical terms (13) | canonical_term, legacy_terms |
| corrections | Error tracking | original, corrected, recurrence |
| session_logs | Research tracking | work_completed, findings |
| documents | Generated docs | file_path, quality_score |

### 1.3 Self-Learning Mechanisms

**Error → Correction → Protocol Update:**
1. Error discovered during session
2. Logged in corrections table with severity
3. If recurrence ≥ 2, added to protocol
4. Quality gate updated to catch automatically
5. All affected documents flagged for review

### 1.4 Automation Scripts (System/scripts/)

The HIRM system includes a suite of Python automation tools:

| Script | Purpose | Usage |
|--------|---------|-------|
| `hirm_core.py` | Core utilities, database access | Import module |
| `quality_gate.py` | Document validation | `python quality_gate.py file.md` |
| `pattern_detector.py` | Find recurring issues | `python pattern_detector.py` |
| `corpus_sync.py` | Sync markdown ↔ database | `python corpus_sync.py` |
| `session_analyzer.py` | Extract session insights | `python session_analyzer.py` |
| `improvement_suggester.py` | Generate improvements | `python improvement_suggester.py` |
| `orchestrator.py` | Master controller | `python orchestrator.py` |

**Quick Commands:**
```bash
# Run quality gate on all documents
python quality_gate.py --all

# Quick system health check
python orchestrator.py --quick

# Full learning cycle
python orchestrator.py

# Sync database to markdown
python corpus_sync.py --db-to-md

# Detect patterns in research
python pattern_detector.py --output patterns.md
```

### 1.5 Claude AI Tool Integration (Filesystem & Desktop Commander)

**[WARN] IMPORTANT:** MCP server is DEPRECATED. Use these tools instead:

#### Recommended Tools for Claude Sessions

| Task | Tool | Example Command |
|------|------|-----------------|
| Read files | Filesystem:read_file | `read_file D:\HIRM\file.md` |
| List directories | Desktop Commander:list_directory | `list_directory D:\HIRM\` |
| Edit files | Desktop Commander:edit_block | `edit_block` with old/new text |
| Write files | Desktop Commander:write_file | `write_file` with content |
| Run Python | Desktop Commander:start_process | `python D:\HIRM\System\scripts\...` |
| Search files | Desktop Commander:start_search | Search by pattern |
| File metadata | Desktop Commander:get_file_info | Get size, dates, lines |

#### Standard Claude Session Workflow

```yaml
1_read_context:
  - Filesystem:read_file → D:\HIRM\Documentation\START_HERE.md
  - Filesystem:read_file → D:\HIRM\Master_Data\Constants\locked_constants.md
  - Desktop Commander:list_directory → Check relevant folders

2_run_automation:
  - Desktop Commander:start_process → "python D:\HIRM\System\scripts\quality_gate.py"
  - Read output for validation results

3_edit_documents:
  - Desktop Commander:read_file → Get current content
  - Desktop Commander:edit_block → Make surgical edits
  - OR Desktop Commander:write_file → Full file replacement

4_query_database:
  - Desktop Commander:start_process → Run Python with sqlite3
  - Parse results for research context
```

#### Database Access via Python Process

```python
# Start Python REPL for database queries
Desktop Commander:start_process → "python -i"

# Then interact:
Desktop Commander:interact_with_process → """
import sqlite3
conn = sqlite3.connect(r'D:\\HIRM\\System\\data\\hirm.db')
cursor = conn.cursor()
cursor.execute("SELECT symbol, value FROM constants")
print(cursor.fetchall())
"""
```

#### File Operations Best Practices

1. **Always use absolute paths**: `D:\HIRM\...` not relative paths
2. **Chunk large writes**: Use append mode for files >30 lines
3. **Use edit_block for surgical edits**: Minimal context, exact match
4. **Verify after edits**: Read file to confirm changes
5. **Update BUILD_STATUS.md**: Track progress for crash recovery


---

## SECTION 2: CORE IDENTITY (Unchanged from v1.0)

```yaml
project: HIRM_Consciousness_Research
focus: "Consciousness emergence through self-reference phase transitions at criticality"
scale: "193+ papers, mathematical frameworks, computational tools, experimental protocols"
philosophy: 
  - rigorous_falsification_over_confirmation
  - multiple_competing_hypotheses
  - empirical_validation_required
  - cross_disciplinary_synthesis
  - intellectual_honesty_paramount
```

### What Makes HIRM Unique
- Integrates quantum mechanics, neuroscience, information theory, statistical physics
- Proposes testable critical threshold: **C_critical ≈ 8.3 ± 0.6 bits**
- Requires multiplicative interaction: **C(t) = Φ(t) × R(t) × D(t)**
- Distinguishes via falsifiable predictions
- Addresses temporal continuity through dimensional persistence

### The Zero-Multiplier Theorem
Because C = Φ × R × D, ANY component = 0 means C = 0:
- Ant colonies: High Φ, R = 0 → Not conscious
- Cerebellum: High Φ, R ≈ 0 → Not conscious
- Current AI: High Φ, D high, R ≈ 0 → Not conscious (yet)

---

## SECTION 3: MANDATORY CHECKS

### 3.1 Before Starting ANY Research

```yaml
pre_research_checklist:
  [ ] Check Master_Data/Constants for current values
  [ ] Check Master_Data/Terminology for naming
  [ ] Review relevant predictions in database
  [ ] Load appropriate protocol sections
  [ ] Declare task type (A-E)
```

### 3.2 During Research

```yaml
continuous_checks:
  - terminology: "Am I using canonical terms? (Not 'Ouroboros Observer')"
  - constants: "Do my values match locked_constants.md?"
  - falsification: "Can this claim be proven wrong?"
  - alternatives: "Have I considered 3+ competing explanations?"
```

### 3.3 Before Delivering Any Document

```yaml
quality_gate:
  [ ] All constants match locked_constants.md
  [ ] No legacy terminology (especially "Ouroboros Observer")
  [ ] Falsification criteria explicit
  [ ] Competing theories addressed
  [ ] Dimensional analysis correct (if equations)
  [ ] Citations properly formatted
  minimum_score: 90%
```

---

## SECTION 4: LOCKED VALUES (Source of Truth)

### 4.1 Critical Constants

| Symbol | Name | Value | Status |
|--------|------|-------|--------|
| C_critical | Consciousness Threshold | **8.3 ± 0.6** bits | ESTABLISHED |
| ν | Correlation length exponent | ~0.63 | ESTABLISHED |
| γ | Susceptibility exponent | ~1.24 | ESTABLISHED |
| β | Order parameter exponent | ~0.33 | ESTABLISHED |
| τ | Avalanche duration exponent | ~2.0 | PROVISIONAL |
| α | Avalanche size exponent | ~1.5 | PROVISIONAL |

**CRITICAL:** Any document using different values is WRONG.

### 4.2 Core Equation

```
C(t) = Φ(t) × R(t) × D(t)
```

**Dimensional Analysis:**
- Φ: bits
- R: dimensionless (0-1)
- D: effective dimensions
- C: bits

### 4.3 Core Predictions

| ID | Prediction | Status |
|----|------------|--------|
| P1 | C ≥ 8.3 bits → consciousness | UNTESTED |
| P2 | C_sleep < 8 bits | UNTESTED |
| P3 | Anesthesia reduces C before LOC | UNTESTED |
| P4 | Critical avalanches τ ≈ 2.0 | PROVISIONAL |
| P5 | DOC stratifies by C value | UNTESTED |


---

## SECTION 5: RESEARCH WORKFLOW

### 5.1 Task Types

```yaml
Type_A_Literature_Review:
  when: "Synthesizing existing papers"
  first_step: "Query database for relevant papers"
  output: "Update papers table with integration notes"
  
Type_B_Theory_Development:
  when: "Extending HIRM framework"
  first_step: "Check Master_Data for conflicts"
  output: "New equations/predictions → database"
  
Type_C_Empirical_Analysis:
  when: "Testing predictions with data"
  first_step: "Check predictions table for hypothesis"
  output: "Update prediction status with evidence"
  
Type_D_Blue_Sky_Exploration:
  when: "Following unexpected patterns"
  first_step: "Document in session_logs"
  output: "Flag findings for future integration"
  
Type_E_Publication_Preparation:
  when: "Creating manuscript"
  first_step: "Run full quality gate"
  output: "Publication-ready document"
```

### 5.2 Standard Workflow

```yaml
Phase_1_Setup:
  1. Read START_HERE.md
  2. Check relevant Master_Data files
  3. Query database for context
  4. Declare task type
  
Phase_2_Research:
  1. Consult corpus (database + project knowledge)
  2. Document findings in session
  3. Check for terminology/constant violations
  4. Log any corrections needed
  
Phase_3_Synthesis:
  1. Connect to HIRM framework
  2. Identify falsification criteria
  3. Consider competing explanations
  4. Update database as needed
  
Phase_4_Delivery:
  1. Run quality gate checklist
  2. Create document in appropriate location
  3. Update documents table
  4. Log session summary
```

### 5.3 Session Logging

After EVERY research session, log:

```yaml
session_log_entry:
  date: "YYYY-MM-DD"
  task_type: "A|B|C|D|E"
  work_completed: ["list of accomplishments"]
  findings: ["key discoveries"]
  papers_integrated: ["paper titles"]
  predictions_tested: ["P1, P2, etc."]
  errors_found: ["any mistakes discovered"]
  corrections_made: ["fixes applied"]
  follow_up_tasks: ["next steps"]
```

---

## SECTION 6: TERMINOLOGY ENFORCEMENT

### 6.1 Forbidden Terms

| [NO] DO NOT USE | [YES] USE INSTEAD |
|--------------|---------------|
| Ouroboros Observer | HIRM |
| OO Theory | HIRM Theory |
| OO Framework | HIRM Framework |
| "proves consciousness" | "supports the hypothesis" |
| "explains consciousness" | "proposes mechanism" |

### 6.2 Required Terms

| Concept | Canonical Term |
|---------|---------------|
| Framework name | HIRM (Hierarchical Information-Reality Model) |
| Main equation | C(t) = Φ(t) × R(t) × D(t) |
| Threshold | C_critical ≈ 8.3 ± 0.6 bits |
| Integration component | Φ (Phi, integrated information) |
| Self-reference component | R (self-reference coefficient) |
| Complexity component | D (dimensional complexity) |

### 6.3 Confidence Qualifiers

Always indicate certainty:
- **ESTABLISHED** - Strong evidence, multiple sources
- **PROVISIONAL** - Good evidence, needs validation
- **SPECULATIVE** - Hypothesis stage
- **DEPRECATED** - Superseded

---

## SECTION 7: BIAS MITIGATION (Unchanged from v1.0)

### Critical Biases to Monitor

1. **Confirmation bias** - Seek disconfirming evidence
2. **Anchoring** - Test values beyond C_critical = 8.3
3. **Theory-laden observation** - Would non-HIRM researcher agree?
4. **P-hacking** - Prespecify analysis plans
5. **Publication bias** - Report null results honestly

### Quick Bias Check

Before finalizing any claim:
```yaml
bias_check:
  [ ] Did we look for disconfirming evidence?
  [ ] Did we consider 3+ alternative hypotheses?
  [ ] Can we specify what would prove this wrong?
  [ ] Is this independently replicable?
  [ ] Is this the simplest explanation?
```


---

## SECTION 8: COMPETING THEORIES

### Always Address These Frameworks

| Theory | Abbreviation | Must Consider |
|--------|--------------|---------------|
| Integrated Information Theory | IIT | Φ calculation differences |
| Global Neuronal Workspace | GNWT | Broadcast mechanism |
| Recurrent Processing Theory | RPT | Recurrence requirements |
| Attention Schema Theory | AST | Self-model comparison |
| Higher-Order Thought | HOT | Meta-representation |
| Free Energy Principle | FEP | Prediction error relationship |

### HIRM vs Competitors

| Aspect | HIRM | IIT | GNWT |
|--------|------|-----|------|
| Threshold | C ≥ 8.3 bits | Φ > 0 | Global broadcast |
| Components | Φ × R × D | Φ only | Ignition + broadcast |
| Cerebellum | Not conscious (R≈0) | Should be conscious | Not conscious |
| Key test | Threshold sharpness | Φ correlates | Broadcast timing |

### Engagement Protocol

For every major claim:
1. State what HIRM predicts
2. State what competing theories predict
3. Identify distinguishing tests
4. Acknowledge where others may explain better

---

## SECTION 9: DELIVERABLE STANDARDS

### 9.1 Quality Gate Checklist

```yaml
mandatory_checks:
  constants_correct:
    - C_critical = 8.3 ± 0.6 bits (not 7.5, not 10.0)
    - All exponents match locked_constants.md
  
  terminology_clean:
    - No "Ouroboros Observer"
    - No "proves consciousness"
    - All terms from terminology_reference.md
  
  falsification_explicit:
    - What would prove this wrong?
    - Specific, measurable criteria
  
  alternatives_considered:
    - Minimum 3 competing explanations
    - Fair treatment of other theories
  
  dimensional_analysis:
    - All equations dimensionally consistent
    - Units specified for all variables
```

### 9.2 Document Locations

| Document Type | Location |
|---------------|----------|
| Theory papers | Theory/Core/ or Theory/Extensions/ |
| Literature reviews | Corpus/Reviews/ |
| Manuscripts | Publications/Manuscripts/ |
| Protocols | Empirical/Protocols/ |
| Results | Empirical/Results/ |
| Code | Code/[appropriate subfolder]/ |

### 9.3 File Naming

```
[descriptive_name_with_underscores].md
Examples:
- brain_criticality_review_2025.md
- C_threshold_validation_results.md
- anesthesia_protocol_v2.md
```

---

## SECTION 10: DATABASE OPERATIONS

### 10.1 Querying the Database

```python
import sqlite3
conn = sqlite3.connect(r'D:\HIRM\System\data\hirm.db')
cursor = conn.cursor()

# Get all constants
cursor.execute("SELECT symbol, value, confidence FROM constants")

# Find papers by domain
cursor.execute("SELECT title, authors FROM papers WHERE domain='brain_criticality'")

# Check prediction status
cursor.execute("SELECT prediction_id, status FROM predictions")

# Search terminology
cursor.execute("SELECT canonical_term, definition FROM terminology")
```

### 10.2 Updating Records

```python
# Update prediction status after testing
cursor.execute("""
    UPDATE predictions 
    SET status='supported', last_tested=datetime('now')
    WHERE prediction_id='P1_threshold'
""")

# Log a correction
cursor.execute("""
    INSERT INTO corrections (correction_type, original_text, corrected_text, reason)
    VALUES ('terminology', 'Ouroboros Observer', 'HIRM', 'Legacy naming')
""")

# Add session log
cursor.execute("""
    INSERT INTO session_logs (session_type, work_completed, findings)
    VALUES ('literature', '["Reviewed 5 papers"]', '["New avalanche evidence"]')
""")

conn.commit()
```

### 10.3 Self-Healing Workflow

When error discovered:
1. Log in corrections table
2. Check recurrence count
3. If recurrence ≥ 2: flag for protocol update
4. Update quality gate if automatable
5. Mark `added_to_protocol = 1`


---

## SECTION 11: QUICK REFERENCE CARDS

### 11.1 Session Startup

```yaml
1_load_context:
  - Read: Documentation/START_HERE.md
  - Check: Master_Data/Constants/locked_constants.md
  - Query: database for relevant papers/predictions

2_declare_task:
  - Type A: Literature review
  - Type B: Theory development
  - Type C: Empirical analysis
  - Type D: Blue sky exploration
  - Type E: Publication prep

3_confirm_values:
  - C_critical = 8.3 ± 0.6 bits
  - Framework = "HIRM" (not Ouroboros Observer)
```

### 11.2 During Research

```yaml
check_every_30_minutes:
  - Am I using canonical terminology?
  - Do my constants match locked values?
  - Have I documented discoveries?
  - Am I considering alternatives?

when_finding_error:
  - Log immediately in corrections
  - Note severity (low/medium/high/critical)
  - Fix all instances
  - Update protocol if recurring
```

### 11.3 Pre-Delivery Checklist

```yaml
before_creating_document:
  [ ] Constants match locked_constants.md
  [ ] No legacy terminology
  [ ] Falsification criteria stated
  [ ] 3+ alternatives considered
  [ ] Dimensional analysis (if equations)
  [ ] Competing theories addressed
  [ ] Session logged
```

---

## SECTION 12: CRITICAL REMINDERS

### NEVER Do These

[NO] Use "Ouroboros Observer" (always "HIRM")  
[NO] Use C_critical values other than 8.3 +/- 0.6  
[NO] Claim to "prove" consciousness  
[NO] Skip the quality gate  
[NO] Ignore competing theories  
[NO] Leave session unlogged  

### ALWAYS Do These

[YES] Check locked_constants.md before using values  
[YES] Check terminology_reference.md for naming  
[YES] State falsification criteria for claims  
[YES] Consider 3+ alternative explanations  
[YES] Log session work  
[YES] Update database when adding content  

---

## SECTION 13: VERSION HISTORY

```yaml
version: 2.2
release_date: 2025-12-20
status: Production_Ready

changes_from_v2.1:
  - Added Section 1.5: Claude AI Tool Integration (Filesystem & Desktop Commander)
  - Explicit MCP deprecation notice
  - Added tool usage patterns and examples
  - Database access via Python process examples
  - File operations best practices
  - Crash recovery guidance

changes_from_v2.0:
  - Added complete automation suite (6 scripts)
  - Removed MCP server dependency
  - Added quality_gate.py for document validation
  - Added pattern_detector.py for recurring issues
  - Added corpus_sync.py for bidirectional sync
  - Added session_analyzer.py for research insights
  - Added improvement_suggester.py for suggestions
  - Added orchestrator.py master controller
  - Integrated with Filesystem/Desktop Commander tools

changes_from_v1:
  - Added SQLite database backend
  - Created self-healing corrections system
  - Locked constants as single source of truth
  - Quality gate automation
  - 49-directory structured organization
  - Session logging requirement
  - Database query integration

maintained_from_v1:
  - Core research philosophy
  - Bias mitigation framework
  - Competing theory engagement
  - Falsification requirements
  - Deliverable standards

future_versions:
  v2.2: "After first empirical validation"
  v2.3: "After Paper 1 submission"
  v3.0: "After peer review feedback"
```

---

## APPENDIX A: FILE LOCATIONS

| Need To... | Go To... |
|------------|----------|
| Start session | Documentation/START_HERE.md |
| Check constants | Master_Data/Constants/locked_constants.md |
| Check terms | Master_Data/Terminology/terminology_reference.md |
| See predictions | Master_Data/Framework/hirm_core_claims.md |
| Query database | System/data/hirm.db |
| Find papers | Corpus/Index/corpus_master_index.md |
| Log errors | Master_Data/Corrections/corrections_registry.md |
| Log session | Logs/SESSION_LOGS.md |

---

## APPENDIX B: DATABASE SCHEMA SUMMARY

```sql
-- papers: Literature corpus
-- constants: Locked values (C_critical, exponents)
-- predictions: Falsifiable claims (P1-P5)
-- equations: Mathematical expressions
-- terminology: Canonical terms + legacy mappings
-- corrections: Self-healing error registry
-- session_logs: Research session tracking
-- documents: Generated document registry
```

---

**HIRM RESEARCH PROTOCOLS v2.2 - COMPLETE**
**Database-backed self-learning research system**
**December 20, 2025**
