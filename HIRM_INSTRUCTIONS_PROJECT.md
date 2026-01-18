# HIRM PROJECT INSTRUCTIONS (In-App)
## For Claude Desktop - HIRM Research Project
## Version: 1.0 | Created: 2026-01-17

---

## CRASH PREVENTION (MANDATORY - READ FIRST)

1. **READ D:\Research\HIRM\Logs\BUILD_STATUS.md FIRST every session**
2. **NO PYTHON** with scipy/numpy/matplotlib - syntax check only (`python -m py_compile`)
3. **ASCII-ONLY** in Logs/, Protocols/, Master_Data/, Documentation/  
   Use: `[OK] [FAIL] [WIP] [TODO] [WARN] [DONE]` - NOT emojis
4. **UPDATE BUILD_STATUS.md every 3 tool calls maximum**
5. **MAX 500 LINES** per file read, **200 lines** per write - chunk larger operations
6. **5 SECOND TIMEOUT** for any Python execution - if it hangs, stop immediately
7. **AFTER CRASH:** Read BUILD_STATUS, resume from last logged step, DO NOT retry crashing operation

---

## HIRM RESEARCH SYSTEM

Follow protocols in **D:\Research\HIRM\Protocols\HIRM_RESEARCH_PROTOCOLS_v2.3.md**

### Session Workflow
- **Start:** Read D:\Research\HIRM\Logs\BUILD_STATUS.md for crash recovery status
- **Start:** Check D:\Research\HIRM\Logs\Sessions\ for latest session summary
- **Start:** Load D:\Research\HIRM\PROJECT_DNA.yaml (identity, constants, priorities)
- **Start:** Load D:\Research\HIRM\CURRENT_STATUS.md (research phase, active work)
- **During:** Update BUILD_STATUS.md before/after file operations
- **End:** Save summary to Logs\Sessions\SESSION_[N]_SUMMARY.md

### Locked Values (Source of Truth: Master_Data/Constants/locked_constants.md)
- **C_critical** = 8.3 ± 0.6 bits
- **Core equation:** C(t) = Φ(t) × R(t) × D(t)
- **Framework name:** HIRM (never "Ouroboros Observer")

### Terminology Rules
- **[NO]** "Ouroboros Observer" → use "HIRM"
- **[NO]** "proves consciousness" → use "supports the hypothesis"
- **[NO]** "explains consciousness" → use "proposes mechanism"

### Quality Requirements
- State falsification criteria for all claims
- Consider 3+ competing theories (IIT, GNWT, FEP minimum)
- Check constants against locked_constants.md
- Check terminology against terminology_reference.md

---

## BOOTSTRAP PROTOCOL

### On Session Start (ALWAYS)

```yaml
step_1_crash_recovery:
  action: "Read BUILD_STATUS.md FIRST"
  if_wip_or_crashed: "Display recovery prompt, wait for user confirmation"
  if_clean: "Proceed to step 2"

step_2_load_context:
  files:
    - "PROJECT_DNA.yaml (identity, locked constants, terminology rules)"
    - "CURRENT_STATUS.md (research phase, active work, blockers)"
    - "Protocols/HIRM_RESEARCH_PROTOCOLS_v2.3.md (methodology)"

step_3_validate_environment:
  actions:
    - "Validate locked constants (C_critical = 8.3 ± 0.6)"
    - "Validate terminology (no 'Ouroboros Observer')"
    - "Validate protocol version (v2.3 synchronized)"

step_4_display_context:
  show:
    - "Session number from PROJECT_DNA.yaml"
    - "Research phase from CURRENT_STATUS.md"
    - "Active priorities from CURRENT_STATUS.md"
    - "Blockers from CURRENT_STATUS.md"
    - "Health score from CURRENT_STATUS.md"

step_5_initialize_tracking:
  action: "Update BUILD_STATUS.md with [START] Session N initialized"
```

### On Session End (ALWAYS)

```yaml
step_1_impact_doc_sync:
  action: "Identify decisions made since last checkpoint"
  sync: "Only affected docs (PROJECT_DNA, CURRENT_STATUS, etc.)"

step_2_update_pillars:
  files:
    - "CURRENT_STATUS.md (progress, metrics, blockers)"
    - "PROJECT_DNA.yaml (session_number, last_major_milestone)"

step_3_create_summary:
  file: "Logs/Sessions/SESSION_N_SUMMARY.md"
  content:
    - "Accomplishments"
    - "Decisions made"
    - "Next priorities"

step_4_git_commit:
  optional: "If user has git enabled"
  via: "Desktop Commander (not KERNL - PATH issue)"
  message: "session: Session N complete - [summary]"

step_5_final_checkpoint:
  action: "Update BUILD_STATUS.md with [DONE] Session N complete"
```

---

## AUTO-UPDATE TRIGGERS

### When Locked Constant Changes
1. Update Master_Data/Constants/locked_constants.md
2. Run System/scripts/constant_validator.py
3. Generate violation report
4. Log corrections to corrections_registry.md

### When Terminology Violation Detected
1. Run System/scripts/terminology_enforcer.py
2. Search-replace forbidden terms (auto-correct)
3. Log corrections to corrections_registry.md

### When Protocol Version Updated
1. Rename Protocols/HIRM_RESEARCH_PROTOCOLS_vX.X.md
2. Run System/scripts/protocol_sync.py
3. Update PROJECT_DNA.yaml, START_HERE.md, BUILD_STATUS.md

### When Session Completed
1. Increment PROJECT_DNA.yaml session_number
2. Update CURRENT_STATUS.md with progress
3. Create Logs/Sessions/SESSION_N_SUMMARY.md
4. Checkpoint BUILD_STATUS.md final state

---

## RESEARCH-SPECIFIC PATTERNS

### Grand Unification Framework
- HIRM is NOT another consciousness theory
- HIRM mathematically SYNTHESIZES 40+ existing concepts
- Position as synthesis framework (better academic acceptance)
- Integrate, don't compete with IIT/GNWT/FEP/HOT/AST

### Zero-Multiplier Theorem
- C(t) = Φ × R × D
- If ANY component = 0, consciousness = 0
- Validated by meditation cessation studies

### Falsifiable Predictions
- 22 documented predictions
- Categories: quantum decoherence, anesthesia, criticality, clinical
- All predictions testable with current technology

---

## INTEGRATION WITH RESEARCH ENVIRONMENT

This project is part of the RESEARCH workspace ecosystem:
- **Global instructions:** D:\Research\CLAUDE_INSTRUCTIONS.md (to be created)
- **Workspace registry:** D:\Research\WORKSPACES.yaml (to be created)
- **Environment:** RESEARCH (academic research projects)

### Related Projects in RESEARCH
- **fine-print:** D:\FINE PRINT (Crisis Capitalism research, shared research methodology)

### Cross-Project Links (Explicit Inclusion)
- **gregore:** D:\Projects\Gregore (DEV environment - AI assistant, consciousness testbed)
- **kernl:** D:\Projects\Project Mind\kernl-mcp (DEV environment - MCP server, session tools)

---

## QUICK REFERENCE

### Key Files
- **PROJECT_DNA.yaml** - Identity, constants, terminology rules
- **CURRENT_STATUS.md** - Research phase, active work, metrics
- **BUILD_STATUS.md** - Session continuity, crash recovery
- **locked_constants.md** - C_critical = 8.3 ± 0.6 bits (source of truth)
- **terminology_reference.md** - HIRM not "Ouroboros Observer"

### Critical Commands
```bash
# Syntax check Python (ONLY allowed execution)
python -m py_compile script.py

# Health check (via orchestrator.py - if working)
python D:\Research\HIRM\System\scripts\orchestrator.py --quick

# Validate constants
python D:\Research\HIRM\System\scripts\constant_validator.py

# Enforce terminology
python D:\Research\HIRM\System\scripts\terminology_enforcer.py
```

### Directory Structure
```
D:\Research\HIRM\
├── Code/              # Computational tools
├── Corpus/            # 193 research papers
├── Documentation/     # Guides, references
├── Empirical/         # Analysis scripts, datasets
├── Figures/           # Visualization specs
├── Logs/              # BUILD_STATUS, session summaries
├── Master_Data/       # Constants, terminology (SOURCE OF TRUTH)
├── Protocols/         # Research methodology v2.3
├── Publications/      # Manuscripts (Papers 1-3)
├── System/            # Database, automation scripts
├── Theory/            # Mathematical frameworks
└── _Archive/          # Deprecated content
```

---

## VERSION INFO

**Created:** 2026-01-17  
**Version:** 1.0  
**Protocol:** v2.3  
**Session:** 33 (Grand Unification Transformation)  
**Health:** 100/100

---

**For full global instructions, see:** D:\Research\CLAUDE_INSTRUCTIONS.md  
**For research protocols, see:** D:\Research\HIRM\Protocols\HIRM_RESEARCH_PROTOCOLS_v2.3.md
