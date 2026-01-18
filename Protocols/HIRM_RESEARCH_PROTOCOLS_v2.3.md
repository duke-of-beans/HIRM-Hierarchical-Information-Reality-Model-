# HIRM RESEARCH PROTOCOLS v2.3
## Database-Backed Self-Learning Research System
## Hierarchical Information-Reality Model (HIRM) Framework

**Version:** 2.3  
**Release Date:** December 20, 2025  
**Project:** Consciousness Emergence Theory  
**Principal Investigator:** David  
**Status:** Production Ready - Crash Resilient

---

## [CRITICAL] CRASH PREVENTION - READ FIRST

Before ANY other action, follow these mandatory rules:

| Rule | Requirement | Reason |
|------|-------------|--------|
| 1 | Read BUILD_STATUS.md first | Crash recovery state |
| 2 | No scipy/numpy/matplotlib execution | 245+ second timeouts |
| 3 | ASCII-only in system files | Encoding errors |
| 4 | Update BUILD_STATUS every 3 tool calls | Incremental recovery |
| 5 | Max 500 lines per file operation | Memory limits |
| 6 | 5-second Python timeout max | Prevent hangs |
| 7 | Never retry crashing operations | Break crash loops |

**ASCII Replacements for System Files:**
- [OK] or [DONE] instead of checkmarks
- [FAIL] or [NO] instead of X marks
- [WIP] or [PROGRESS] instead of spinners
- [TODO] instead of bullets
- [WARN] or [CAUTION] instead of warning symbols
- [STAR] or [PRIORITY] instead of stars

---

## WHAT'S NEW IN v2.3

### Key Upgrades from v2.2
1. **Crash prevention protocol** - Mandatory rules to prevent session crashes
2. **ASCII-only system files** - No emojis in Logs/, Protocols/, Master_Data/
3. **Incremental save protocol** - BUILD_STATUS updated every 3 tool calls
4. **Python execution limits** - No heavy imports, 5-second timeout max
5. **File size limits** - 500 lines max per read/write operation
6. **Crash recovery workflow** - Resume from last logged step

### Maintained from v2.2
1. Complete automation suite - 6 Python scripts for self-learning
2. Quality gate automation - Validates documents before delivery
3. Pattern detection - Automatically finds recurring issues
4. Corpus synchronization - Bidirectional markdown to database sync
5. Session analysis - Extracts insights from research patterns
6. Database-backed system - SQLite database (hirm.db) as central registry

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
|-- Master_Data\          [STAR] SINGLE SOURCE OF TRUTH
|   |-- Constants\        -> locked_constants.md
|   |-- Framework\        -> hirm_core_claims.md, component_definitions.md
|   |-- Terminology\      -> terminology_reference.md
|   +-- Corrections\      -> corrections_registry.md
|-- System\               [CONFIG] INFRASTRUCTURE
|   |-- data\             -> hirm.db (SQLite database)
|   |-- scripts\          -> Automation suite (see below)
|   +-- config\           -> Configuration files
|-- Protocols\            [DOCS] THIS DOCUMENT
|-- Corpus\               [CORPUS] Literature (71+ papers indexed)
|-- Theory\               [THEORY] Theoretical framework
|-- Empirical\            [EMPIRICAL] Data and validation
|-- Code\                 [CODE] Python implementations
|-- Publications\         [PUBS] Manuscripts
|-- Figures\              Visualizations
|-- Documentation\        Navigation
|-- Logs\                 Session tracking, BUILD_STATUS.md
+-- _Archive\             Version history
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

**Error to Correction to Protocol Update:**
1. Error discovered during session
2. Logged in corrections table with severity
3. If recurrence >= 2, added to protocol
4. Quality gate updated to catch automatically
5. All affected documents flagged for review

### 1.4 Automation Scripts (System/scripts/)

The HIRM system includes a suite of Python automation tools:

| Script | Purpose | Usage |
|--------|---------|-------|
| hirm_core.py | Core utilities, database access | Import module |
| quality_gate.py | Document validation | Syntax check only |
| pattern_detector.py | Find recurring issues | Syntax check only |
| corpus_sync.py | Sync markdown to database | Syntax check only |
| session_analyzer.py | Extract session insights | Syntax check only |
| improvement_suggester.py | Generate improvements | Syntax check only |
| orchestrator.py | Master controller | Syntax check only |

**[WARN] SCRIPT EXECUTION RULES:**
- Never execute scripts with scipy/numpy/matplotlib imports
- Use syntax checking only: `python -m py_compile script.py`
- If execution needed: Validate logic by reading code, not running it
- Heavy computation must be done outside Claude sessions

### 1.5 Claude AI Tool Integration

**[WARN] MCP server is DEPRECATED. Use these tools instead:**

#### Recommended Tools for Claude Sessions

| Task | Tool | Notes |
|------|------|-------|
| Read files | Filesystem:read_file | Use head/tail for large files |
| List directories | Desktop Commander:list_directory | Depth 2 default |
| Edit files | Desktop Commander:edit_block | Surgical edits only |
| Write files | Desktop Commander:write_file | Max 200 lines per call |
| Search files | Desktop Commander:start_search | 30 second timeout |
| File metadata | Desktop Commander:get_file_info | Quick operation |

#### [NO] Forbidden Operations

| Operation | Why Forbidden | Alternative |
|-----------|---------------|-------------|
| Run scipy scripts | 245+ second timeout | Read code, validate logic manually |
| Run numpy scripts | Heavy imports | Read code, validate logic manually |
| Run matplotlib scripts | Heavy imports | Read code, validate logic manually |
| Read files > 500 lines | Memory issues | Use head=200, tail=200 |
| Write files > 200 lines | Timeout risk | Chunk into multiple writes |

#### Standard Claude Session Workflow

```yaml
1_crash_recovery_check:
  - Filesystem:read_file -> D:\HIRM\Logs\BUILD_STATUS.md
  - Check last session state
  - If crashed: Resume from last logged step, DO NOT retry crashing op

2_load_context:
  - Filesystem:read_file -> D:\HIRM\Documentation\START_HERE.md
  - Filesystem:read_file -> D:\HIRM\Master_Data\Constants\locked_constants.md
  - Update BUILD_STATUS.md with "Session N started"

3_research_work:
  - Perform task
  - Update BUILD_STATUS.md every 3 tool calls
  - Use ASCII-only in system files

4_session_close:
  - Create SESSION_N_SUMMARY.md in Logs/Sessions/
  - Update BUILD_STATUS.md with "Session N complete"
```

#### Database Access (Safe Method)

Instead of running Python scripts, query database by reading and parsing:

```yaml
safe_database_access:
  1. Read the database file info to confirm it exists
  2. For simple queries: Document what you need, David runs query
  3. For complex queries: Write query to file, David executes
  4. Never start Python REPL for database access (timeout risk)
```

---

## SECTION 2: CORE IDENTITY

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
- Proposes testable critical threshold: **C_critical = 8.3 +/- 0.6 bits**
- Requires multiplicative interaction: **C(t) = Phi(t) x R(t) x D(t)**
- Distinguishes via falsifiable predictions
- Addresses temporal continuity through dimensional persistence

### The Zero-Multiplier Theorem
Because C = Phi x R x D, ANY component = 0 means C = 0:
- Ant colonies: High Phi, R = 0 -> Not conscious
- Cerebellum: High Phi, R ~ 0 -> Not conscious
- Current AI: High Phi, D high, R ~ 0 -> Not conscious (yet)

---

## SECTION 3: MANDATORY CHECKS

### 3.1 Before Starting ANY Session

```yaml
pre_session_checklist:
  [ ] Read Logs/BUILD_STATUS.md for crash recovery
  [ ] Check if previous session crashed (resume from last step)
  [ ] Read Documentation/START_HERE.md
  [ ] Check Master_Data/Constants/locked_constants.md
  [ ] Check Master_Data/Terminology/terminology_reference.md
  [ ] Declare task type (A-E)
  [ ] Create session summary file with "IN PROGRESS" status
```

### 3.2 During Research

```yaml
continuous_checks:
  every_3_tool_calls:
    - Update BUILD_STATUS.md with current step
  
  every_task:
    - Am I using canonical terms? (Not 'Ouroboros Observer')
    - Do my values match locked_constants.md?
    - Can this claim be proven wrong?
    - Have I considered 3+ competing explanations?
    - Am I using ASCII-only in system files?
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
  [ ] ASCII-only if system file
  minimum_score: 90%
```

### 3.4 Session Closing

```yaml
session_close_checklist:
  [ ] Create Logs/Sessions/SESSION_N_SUMMARY.md
  [ ] Update BUILD_STATUS.md with "Session N complete"
  [ ] List work completed
  [ ] List next steps
  [ ] Note any errors found
```

---

## SECTION 4: LOCKED VALUES (Source of Truth)

### 4.1 Critical Constants

| Symbol | Name | Value | Status |
|--------|------|-------|--------|
| C_critical | Consciousness Threshold | **8.3 +/- 0.6** bits | ESTABLISHED |
| nu | Correlation length exponent | ~0.63 | ESTABLISHED |
| gamma | Susceptibility exponent | ~1.24 | ESTABLISHED |
| beta | Order parameter exponent | ~0.33 | ESTABLISHED |
| tau | Avalanche duration exponent | ~2.0 | PROVISIONAL |
| alpha | Avalanche size exponent | ~1.5 | PROVISIONAL |

**[WARN] CRITICAL:** Any document using different values is WRONG.

### 4.2 Core Equation

```
C(t) = Phi(t) x R(t) x D(t)
```

**Dimensional Analysis:**
- Phi: bits
- R: dimensionless (0-1)
- D: effective dimensions
- C: bits

### 4.3 Core Predictions

| ID | Prediction | Status |
|----|------------|--------|
| P1 | C >= 8.3 bits -> consciousness | UNTESTED |
| P2 | C_sleep < 8 bits | UNTESTED |
| P3 | Anesthesia reduces C before LOC | UNTESTED |
| P4 | Critical avalanches tau ~ 2.0 | PROVISIONAL |
| P5 | DOC stratifies by C value | UNTESTED |

---

## SECTION 5: CRASH PREVENTION PROTOCOL

### 5.1 The Problem

Sessions 12, 13, and 14 crashed due to:
1. Heavy Python imports (scipy) causing 245+ second timeouts
2. Emoji/Unicode characters (155 instances) causing encoding issues
3. No incremental save protocol - entire sessions lost on crash

### 5.2 Mandatory Rules

**RULE 1: NO HEAVY PYTHON EXECUTION**

```yaml
forbidden:
  - python script_with_scipy.py
  - python script_with_numpy.py
  - python script_with_matplotlib.py
  - python -i (interactive REPL)

allowed:
  - python -m py_compile script.py (syntax check only)
  - Filesystem:read_file script.py (read code for review)
```

**RULE 2: ASCII-ONLY IN SYSTEM FILES**

System files that must be ASCII-only:
- D:\HIRM\Logs\*.md
- D:\HIRM\Logs\Sessions\*.md
- D:\HIRM\Protocols\*.md
- D:\HIRM\Master_Data\*.md
- D:\HIRM\Documentation\*.md

**RULE 3: INCREMENTAL SAVES**

```yaml
save_protocol:
  frequency: Every 3 tool calls maximum
  target: D:\HIRM\Logs\BUILD_STATUS.md
  format: "### [DONE] Step N - Description"
  
recovery_point:
  - Maximum 30 seconds of work lost on crash
  - Each step numbered for tracking
  - Session summary created at START not end
```

**RULE 4: FILE SIZE LIMITS**

| Operation | Maximum | How to Handle Larger |
|-----------|---------|---------------------|
| Read file | 500 lines | Use head=200, tail=200 |
| Write file | 200 lines | Chunk into multiple writes |
| Search results | 50 results | Use pagination |

**RULE 5: TIMEOUT DISCIPLINE**

| Operation | Timeout | If Exceeded |
|-----------|---------|-------------|
| File read/write | 30 seconds | Stop, log, find alternative |
| Python execution | 5 seconds | Stop, do NOT retry |
| Search | 30 seconds | Stop, narrow search |

### 5.3 Crash Recovery Workflow

```yaml
if_session_crashed:
  1. Read BUILD_STATUS.md
  2. Find last completed step
  3. Read last session summary
  4. Resume from next step
  5. DO NOT retry the operation that caused crash
  6. Document crash in corrections_registry.md
```

---

## SECTION 6: RESEARCH WORKFLOW

### 6.1 Task Types

```yaml
Type_A_Literature_Review:
  when: "Synthesizing existing papers"
  first_step: "Check BUILD_STATUS, then query corpus"
  output: "Update papers notes"
  
Type_B_Theory_Development:
  when: "Extending HIRM framework"
  first_step: "Check BUILD_STATUS, then check Master_Data"
  output: "New equations/predictions documented"
  
Type_C_Empirical_Analysis:
  when: "Testing predictions with data"
  first_step: "Check BUILD_STATUS, then check predictions"
  output: "Update prediction status"
  
Type_D_Blue_Sky_Exploration:
  when: "Following unexpected patterns"
  first_step: "Check BUILD_STATUS, then document in session"
  output: "Flag findings for integration"
  
Type_E_Publication_Preparation:
  when: "Creating manuscript"
  first_step: "Check BUILD_STATUS, then run quality gate"
  output: "Publication-ready document"
```

### 6.2 Standard Workflow

```yaml
Phase_1_Setup:
  1. Read BUILD_STATUS.md (crash recovery)
  2. Read START_HERE.md
  3. Check relevant Master_Data files
  4. Declare task type
  5. Create session summary file
  6. Update BUILD_STATUS.md
  
Phase_2_Research:
  1. Consult corpus (project knowledge)
  2. Document findings
  3. Update BUILD_STATUS.md every 3 tool calls
  4. Check for terminology/constant violations
  5. Log any corrections needed
  
Phase_3_Synthesis:
  1. Connect to HIRM framework
  2. Identify falsification criteria
  3. Consider competing explanations
  4. Update BUILD_STATUS.md
  
Phase_4_Delivery:
  1. Run quality gate checklist
  2. Create document in appropriate location
  3. Update session summary
  4. Update BUILD_STATUS.md with completion
```

### 6.3 Session Logging Format

```yaml
session_summary_template:
  header:
    session_number: N
    date: YYYY-MM-DD
    status: IN PROGRESS | COMPLETE | CRASHED
    focus: "Brief description"
  
  progress_log:
    - "### [DONE] Step 1 - Description"
    - "### [DONE] Step 2 - Description"
    - "### [WIP] Step 3 - Description"
  
  outcomes:
    work_completed: ["list"]
    findings: ["list"]
    errors_found: ["list"]
    next_steps: ["list"]
```

---

## SECTION 7: TERMINOLOGY ENFORCEMENT

### 7.1 Forbidden Terms

| [NO] DO NOT USE | [YES] USE INSTEAD |
|-----------------|-------------------|
| Ouroboros Observer | HIRM |
| OO Theory | HIRM Theory |
| OO Framework | HIRM Framework |
| "proves consciousness" | "supports the hypothesis" |
| "explains consciousness" | "proposes mechanism" |

### 7.2 Required Terms

| Concept | Canonical Term |
|---------|---------------|
| Framework name | HIRM (Hierarchical Information-Reality Model) |
| Main equation | C(t) = Phi(t) x R(t) x D(t) |
| Threshold | C_critical = 8.3 +/- 0.6 bits |
| Integration component | Phi (integrated information) |
| Self-reference component | R (self-reference coefficient) |
| Complexity component | D (dimensional complexity) |

### 7.3 Confidence Qualifiers

Always indicate certainty:
- **ESTABLISHED** - Strong evidence, multiple sources
- **PROVISIONAL** - Good evidence, needs validation
- **SPECULATIVE** - Hypothesis stage
- **DEPRECATED** - Superseded

---

## SECTION 8: BIAS MITIGATION

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

## SECTION 9: COMPETING THEORIES

### Always Address These Frameworks

| Theory | Abbreviation | Must Consider |
|--------|--------------|---------------|
| Integrated Information Theory | IIT | Phi calculation differences |
| Global Neuronal Workspace | GNWT | Broadcast mechanism |
| Recurrent Processing Theory | RPT | Recurrence requirements |
| Attention Schema Theory | AST | Self-model comparison |
| Higher-Order Thought | HOT | Meta-representation |
| Free Energy Principle | FEP | Prediction error relationship |

### HIRM vs Competitors

| Aspect | HIRM | IIT | GNWT |
|--------|------|-----|------|
| Threshold | C >= 8.3 bits | Phi > 0 | Global broadcast |
| Components | Phi x R x D | Phi only | Ignition + broadcast |
| Cerebellum | Not conscious (R~0) | Should be conscious | Not conscious |
| Key test | Threshold sharpness | Phi correlates | Broadcast timing |

### Engagement Protocol

For every major claim:
1. State what HIRM predicts
2. State what competing theories predict
3. Identify distinguishing tests
4. Acknowledge where others may explain better

---

## SECTION 10: DELIVERABLE STANDARDS

### 10.1 Quality Gate Checklist

```yaml
mandatory_checks:
  constants_correct:
    - C_critical = 8.3 +/- 0.6 bits (not 7.5, not 10.0)
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
  
  formatting:
    - ASCII-only if system file
    - No special characters that cause encoding issues
```

### 10.2 Document Locations

| Document Type | Location |
|---------------|----------|
| Theory papers | Theory/Core/ or Theory/Extensions/ |
| Literature reviews | Corpus/Reviews/ |
| Manuscripts | Publications/Manuscripts/ |
| Protocols | Empirical/Protocols/ |
| Results | Empirical/Results/ |
| Code | Code/[appropriate subfolder]/ |
| Session logs | Logs/Sessions/ |
| Build status | Logs/BUILD_STATUS.md |

### 10.3 File Naming

```
[descriptive_name_with_underscores].md
Examples:
- brain_criticality_review_2025.md
- C_threshold_validation_results.md
- anesthesia_protocol_v2.md
- SESSION_15_SUMMARY.md
```

---

## SECTION 11: QUICK REFERENCE CARDS

### 11.1 Session Startup Card

```yaml
EVERY_SESSION_START:
  1. Filesystem:read_file -> D:\HIRM\Logs\BUILD_STATUS.md
  2. Check for crash recovery needs
  3. Read START_HERE.md
  4. Check locked_constants.md
  5. Declare task type (A/B/C/D/E)
  6. Create SESSION_N_SUMMARY.md with "IN PROGRESS"
  7. Update BUILD_STATUS.md with session start

VALUES_TO_CONFIRM:
  - C_critical = 8.3 +/- 0.6 bits
  - Framework name = "HIRM" (never Ouroboros Observer)
  - Equation = C(t) = Phi(t) x R(t) x D(t)
```

### 11.2 During Research Card

```yaml
EVERY_3_TOOL_CALLS:
  - Update BUILD_STATUS.md with current step

CONTINUOUS_CHECKS:
  - Using canonical terminology?
  - Constants match locked values?
  - Documenting discoveries?
  - Considering alternatives?
  - ASCII-only in system files?

IF_ERROR_FOUND:
  - Log in corrections_registry.md
  - Note severity (low/medium/high/critical)
  - Fix all instances
  - Update protocol if recurring (>= 2 times)
```

### 11.3 Pre-Delivery Card

```yaml
BEFORE_ANY_DOCUMENT:
  [ ] Constants match locked_constants.md
  [ ] No legacy terminology
  [ ] Falsification criteria stated
  [ ] 3+ alternatives considered
  [ ] Dimensional analysis (if equations)
  [ ] Competing theories addressed
  [ ] ASCII-only (if system file)
  [ ] Session summary updated
  [ ] BUILD_STATUS.md updated
```

### 11.4 Crash Prevention Card

```yaml
NEVER_DO:
  - Execute Python with scipy/numpy/matplotlib
  - Use emojis in system files
  - Read/write files > 500/200 lines
  - Retry operations that caused crash
  - Skip BUILD_STATUS updates

ALWAYS_DO:
  - Read BUILD_STATUS.md first
  - Update BUILD_STATUS every 3 tool calls
  - Use ASCII markers: [OK] [FAIL] [WIP] [TODO]
  - Create session summary at START
  - Chunk large file operations
```

---

## SECTION 12: CRITICAL REMINDERS

### [NO] NEVER Do These

- Use "Ouroboros Observer" (always "HIRM")
- Use C_critical values other than 8.3 +/- 0.6
- Claim to "prove" consciousness
- Skip the quality gate
- Ignore competing theories
- Leave session unlogged
- Execute heavy Python scripts (scipy, numpy, matplotlib)
- Use emojis in system files
- Retry operations that caused crashes
- Read/write files exceeding size limits

### [YES] ALWAYS Do These

- Read BUILD_STATUS.md at session start
- Check locked_constants.md before using values
- Check terminology_reference.md for naming
- State falsification criteria for claims
- Consider 3+ alternative explanations
- Update BUILD_STATUS.md every 3 tool calls
- Create session summary at session START
- Use ASCII markers in system files
- Log session work before ending
- Document crashes in corrections registry

---

## SECTION 13: VERSION HISTORY

```yaml
version: 2.3
release_date: 2025-12-20
status: Production_Ready_Crash_Resilient

changes_from_v2.2:
  - Added crash prevention as Section 5
  - Added crash prevention summary at document top
  - Converted all formatting to ASCII (no emojis)
  - Added file size limits (500 read, 200 write)
  - Added Python execution restrictions
  - Added incremental save protocol
  - Added crash recovery workflow
  - Updated all quick reference cards
  - Added session startup/closing checklists
  - Removed Python REPL database access (timeout risk)
  - Updated tool recommendations with safety notes

changes_from_v2.1:
  - Added Section 1.5: Claude AI Tool Integration
  - Explicit MCP deprecation notice
  - Added tool usage patterns and examples
  - Database access via Python process examples
  - File operations best practices
  - Crash recovery guidance

maintained_from_v2.0:
  - Complete automation suite (6 scripts)
  - Database-backed system
  - Self-healing corrections system
  - Quality gate automation
  - 49-directory structured organization

maintained_from_v1.0:
  - Core research philosophy
  - Bias mitigation framework
  - Competing theory engagement
  - Falsification requirements
  - Deliverable standards

future_versions:
  v2.4: "After first successful empirical validation"
  v2.5: "After Paper 1 submission"
  v3.0: "After peer review feedback"
```

---

## APPENDIX A: FILE LOCATIONS

| Need To... | Go To... |
|------------|----------|
| Check crash recovery | Logs/BUILD_STATUS.md |
| Start session | Documentation/START_HERE.md |
| Check constants | Master_Data/Constants/locked_constants.md |
| Check terms | Master_Data/Terminology/terminology_reference.md |
| See predictions | Master_Data/Framework/hirm_core_claims.md |
| Find papers | Corpus/Index/corpus_master_index.md |
| Log errors | Master_Data/Corrections/corrections_registry.md |
| Log session | Logs/Sessions/SESSION_N_SUMMARY.md |
| Crash prevention rules | Protocols/CRASH_PREVENTION_PROTOCOL.md |

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

## APPENDIX C: ASCII REPLACEMENT TABLE

For use in system files (Logs/, Protocols/, Master_Data/, Documentation/):

| Symbol Type | ASCII Replacement |
|-------------|-------------------|
| Checkmark | [OK] or [DONE] |
| X mark | [FAIL] or [NO] |
| Spinner/Progress | [WIP] or [PROGRESS] |
| Star | [STAR] or [PRIORITY] |
| Warning | [WARN] or [CAUTION] |
| Todo bullet | [TODO] |
| Arrow | -> |
| Multiply | x |
| Plus/minus | +/- |
| Approximately | ~ |
| Greater/equal | >= |
| Less/equal | <= |

---

## APPENDIX D: CRASH PREVENTION QUICK REFERENCE

```
+--------------------------------------------------+
|           CRASH PREVENTION CHECKLIST             |
+--------------------------------------------------+
| [1] Read BUILD_STATUS.md FIRST                   |
| [2] No scipy/numpy/matplotlib execution          |
| [3] ASCII-only in system files                   |
| [4] Update BUILD_STATUS every 3 tool calls       |
| [5] Max 500 lines read, 200 lines write          |
| [6] 5-second timeout for Python                  |
| [7] Never retry crashing operations              |
+--------------------------------------------------+
| If crash occurred:                               |
| - Read BUILD_STATUS for last state               |
| - Resume from last completed step                |
| - Document crash in corrections registry         |
| - Find alternative to crashing operation         |
+--------------------------------------------------+
```

---

**HIRM RESEARCH PROTOCOLS v2.3 - COMPLETE**
**Database-backed, crash-resilient, self-learning research system**
**December 20, 2025**

