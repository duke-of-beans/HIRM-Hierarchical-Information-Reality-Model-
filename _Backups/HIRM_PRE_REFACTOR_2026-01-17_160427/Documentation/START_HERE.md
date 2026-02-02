# START HERE - HIRM Research System
## Hierarchical Information-Reality Model
## Version 2.3 | December 2025

---

## [CRITICAL] CRASH PREVENTION - READ FIRST

**MANDATORY FOR ALL CLAUDE SESSIONS:**

1. **NO HEAVY PYTHON** - Never execute scripts importing scipy/numpy/matplotlib
2. **ASCII-ONLY** - Use [OK], [FAIL], [WIP] not emojis in system files
3. **SAVE OFTEN** - Update BUILD_STATUS.md every 3 tool calls max
4. **SMALL CHUNKS** - Never read/write files > 500 lines at once
5. **QUICK TIMEOUT** - 5 seconds max for any Python execution

See: `Protocols/CRASH_PREVENTION_PROTOCOL.md` for full rules.

---

## WHAT IS THIS?

This is the HIRM (Hierarchical Information-Reality Model) research system - a self-learning, database-backed infrastructure for consciousness research.

**Core Hypothesis:** Consciousness emerges through self-reference phase transitions when information processing capacity C(t) exceeds a critical threshold of ~8.3 bits.

---

## QUICK ORIENTATION

### Key Directories

| Directory | Purpose | Start Here |
|-----------|---------|------------|
| Master_Data/ | SOURCE OF TRUTH - Constants, definitions | locked_constants.md |
| Theory/ | Theoretical framework documents | Core/Mathematical_Foundations.md |
| Corpus/ | Research literature (193+ papers) | Index/corpus_master_index.md |
| Empirical/ | Datasets, protocols, results | Datasets/Dataset_Guide.md |
| Code/ | Python implementations | Core/consciousness_measure.py |
| Publications/ | Manuscript drafts | Manuscripts/ |
| System/ | Database, scripts, config | data/hirm.db |
| Protocols/ | Research protocols | HIRM_RESEARCH_PROTOCOLS_v2.3.md |
| Logs/ | Session tracking, crash recovery | BUILD_STATUS.md |

### The Database (hirm.db)

The SQLite database at System/data/hirm.db is the central registry:
- papers: 193+ literature corpus entries
- constants: Locked scientific values (C_critical, exponents)
- predictions: Falsifiable claims and their status
- equations: All mathematical expressions
- corrections: Error tracking for self-healing

---

## FIRST TIME? DO THIS:

1. Read BUILD_STATUS.md for crash recovery state
2. Read the core claims: Master_Data/Framework/hirm_core_claims.md
3. Check locked constants: Master_Data/Constants/locked_constants.md
4. Review terminology: Master_Data/Terminology/terminology_reference.md
5. Load protocols: Protocols/HIRM_RESEARCH_PROTOCOLS_v2.3.md

---

## THE CORE EQUATION

```
C(t) = Phi(t) x R(t) x D(t)
```

| Component | Meaning | Units |
|-----------|---------|-------|
| C(t) | Consciousness capacity | bits |
| Phi(t) | Integrated information | bits |
| R(t) | Self-reference coefficient | dimensionless (0-1) |
| D(t) | Dimensional complexity | effective dimensions |

**Critical Threshold:** C >= 8.3 +/- 0.6 bits -> Consciousness

---

## CRITICAL RULES

### [NO] NEVER:
- Use "Ouroboros Observer" (legacy name - use HIRM)
- Use C_critical values other than 8.3 +/- 0.6
- Claim to "prove" consciousness
- Skip quality checks for deliverables
- Execute heavy Python scripts (scipy, numpy imports)
- Use emojis in system files

### [YES] ALWAYS:
- Check BUILD_STATUS.md first
- Check locked_constants.md before using values
- Check terminology_reference.md for naming
- Update BUILD_STATUS.md every 3 tool calls
- Log session work
- Use ASCII markers: [OK], [FAIL], [WIP], [TODO]

---

## CRASH RECOVERY

If Claude crashed mid-session:
1. Read D:\HIRM\Logs\BUILD_STATUS.md
2. Check D:\HIRM\Logs\Sessions\ for last session state
3. Resume from last logged step
4. DO NOT retry the operation that caused crash

---

## GETTING HELP

- Navigation: See INDEX.md for full directory map
- Protocols: See Protocols/ for research standards
- Crash Prevention: See Protocols/CRASH_PREVENTION_PROTOCOL.md

---

**Welcome to HIRM Research!**
