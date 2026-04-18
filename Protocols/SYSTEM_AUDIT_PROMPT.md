# HIRM SYSTEM AUDIT PROMPT
## Copy this entire prompt into a new Claude chat to audit the system
## Created: 2025-12-20

---

## COPY EVERYTHING BELOW THIS LINE

---

# HIRM SYSTEM AUDIT REQUEST

You are auditing the HIRM (Hierarchical Information-Reality Model) research system located at D:\HIRM\

## CRITICAL: CRASH PREVENTION DURING AUDIT

Before you begin, follow these rules to prevent session crashes:
- NO Python execution with scipy/numpy/matplotlib
- Use syntax check only: python -m py_compile script.py
- MAX 500 lines per file read - use head/tail for larger files
- Update D:\HIRM\Logs\BUILD_STATUS.md every 3 tool calls
- ASCII-ONLY markers in system files: [OK] [FAIL] [WIP] [TODO] [WARN]
- If anything hangs for more than 5 seconds, stop immediately

## AUDIT TASKS

Perform the following audits in order. After each section, update BUILD_STATUS.md with your progress.

### AUDIT 1: Crash Prevention Compliance

Check these files for emoji/special character violations:
- D:\HIRM\Logs\BUILD_STATUS.md
- D:\HIRM\Logs\Sessions\*.md (all session files)
- D:\HIRM\Documentation\START_HERE.md
- D:\HIRM\Protocols\*.md (all protocol files)
- D:\HIRM\Master_Data\**\*.md (all master data files)

Report: List any files containing emojis or special characters that should be ASCII-only.

### AUDIT 2: Locked Constants Verification

Read D:\HIRM\Master_Data\Constants\locked_constants.md

Then search across the entire D:\HIRM\ directory for these values:
- Any mention of C_critical that is NOT 8.3 +/- 0.6
- Any mention of "7.5 bits" or "10 bits" as consciousness threshold
- Any outdated exponent values

Report: List any files with incorrect constant values.

### AUDIT 3: Terminology Compliance

Search the D:\HIRM\ directory for forbidden terms:
- "Ouroboros Observer" (should be "HIRM")
- "OO Theory" or "OO Framework"
- "proves consciousness" (should be "supports the hypothesis")
- "explains consciousness" (should be "proposes mechanism")

Report: List any files containing forbidden terminology.

### AUDIT 4: Protocol Version Check

Verify that all references point to v2.3:
- Check D:\HIRM\Documentation\START_HERE.md references correct protocol version
- Check D:\HIRM\Logs\BUILD_STATUS.md references correct protocol version
- Check any other files that reference protocol versions

Report: List any files referencing outdated protocol versions (v2.0, v2.1, v2.2).

### AUDIT 5: Directory Structure Validation

List the top-level directories in D:\HIRM\ and verify these exist:
- Master_Data\
- System\
- Protocols\
- Corpus\
- Theory\
- Empirical\
- Code\
- Publications\
- Figures\
- Documentation\
- Logs\
- _Archive\

Report: List any missing directories or unexpected directories.

### AUDIT 6: Critical File Existence

Verify these critical files exist:
- D:\HIRM\Logs\BUILD_STATUS.md
- D:\HIRM\Documentation\START_HERE.md
- D:\HIRM\Protocols\HIRM_RESEARCH_PROTOCOLS_v2.3.md
- D:\HIRM\Protocols\CRASH_PREVENTION_PROTOCOL.md
- D:\HIRM\Master_Data\Constants\locked_constants.md
- D:\HIRM\Master_Data\Terminology\terminology_reference.md
- D:\HIRM\Master_Data\Corrections\corrections_registry.md
- D:\HIRM\System\data\hirm.db

Report: List any missing critical files.

### AUDIT 7: Session Log Continuity

Read the session files in D:\HIRM\Logs\Sessions\
- Check for gaps in session numbering
- Check for sessions marked as crashed vs complete
- Identify the most recent session number

Report: Session continuity status and current session number.

### AUDIT 8: Database Integrity (Read-Only)

Check if D:\HIRM\System\data\hirm.db exists and report its file size.
Do NOT attempt to query the database (no Python execution).

Report: Database file exists (yes/no) and file size.

### AUDIT 9: Code Syntax Validation

For each Python file in D:\HIRM\Code\ and D:\HIRM\System\scripts\:
- Run: python -m py_compile [filename]
- This checks syntax WITHOUT executing

Report: List any files with syntax errors.

### AUDIT 10: Cross-Reference Check

Verify internal consistency:
- Does START_HERE.md reference the correct protocol version?
- Does BUILD_STATUS.md match the latest session summary?
- Do the locked constants in Master_Data match what's documented in protocols?

Report: Any inconsistencies found.

## OUTPUT FORMAT

After completing all audits, create a file:
D:\HIRM\Logs\AUDIT_REPORT_[DATE].md

Structure:
```
# HIRM SYSTEM AUDIT REPORT
Date: [DATE]
Auditor: Claude
Status: [PASS/FAIL/WARNINGS]

## Summary
- Total issues found: [N]
- Critical issues: [N]
- Warnings: [N]

## Audit 1: Crash Prevention Compliance
Status: [PASS/FAIL]
Issues: [list or "None"]

## Audit 2: Locked Constants
Status: [PASS/FAIL]
Issues: [list or "None"]

[...continue for all 10 audits...]

## Recommended Actions
1. [action item]
2. [action item]
...

## Files Modified During Audit
- [list any files updated, or "None - read-only audit"]
```

## FINAL STEP

After creating the audit report:
1. Update D:\HIRM\Logs\BUILD_STATUS.md with audit completion
2. Provide a brief summary to David

Begin the audit now.

---

## END OF AUDIT PROMPT

