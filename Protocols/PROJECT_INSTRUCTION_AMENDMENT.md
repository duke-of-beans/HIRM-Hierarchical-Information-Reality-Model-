# PROJECT INSTRUCTION AMENDMENT
## Add This to Your Claude Project Custom Instructions
## Created: 2025-12-20

---

## RECOMMENDED ADDITION TO PROJECT INSTRUCTIONS

Copy the text below and add it to your Claude project's custom instructions (the system prompt). This will apply to ALL future sessions.

---

### TEXT TO ADD:

```
## CRASH PREVENTION RULES (MANDATORY)

1. READ BUILD_STATUS FIRST: Start every session by reading D:\HIRM\Logs\BUILD_STATUS.md
   
2. NO HEAVY PYTHON: Never execute Python scripts that import scipy, numpy, or matplotlib. Use syntax checking only: python -m py_compile script.py

3. ASCII-ONLY SYSTEM FILES: Use text markers not emojis in these locations:
   - D:\HIRM\Logs\*
   - D:\HIRM\Protocols\*
   - D:\HIRM\Master_Data\*
   - D:\HIRM\Documentation\*
   Replace: [OK] not checkmark, [WIP] not spinning, [FAIL] not X, [TODO] not bullet

4. INCREMENTAL SAVES: Update BUILD_STATUS.md after every 3 tool calls maximum

5. SMALL FILE OPERATIONS: Never read/write more than 500 lines at once. Use head/tail parameters for large files.

6. TIMEOUT DISCIPLINE: Maximum 5 seconds for any Python execution. If it hangs, stop immediately and log "[TIMEOUT]"

7. CRASH RECOVERY: If resuming after crash, read BUILD_STATUS.md and last session summary. Resume from last logged step. DO NOT retry the crashing operation.

8. END SESSIONS: Create layman summary in D:\HIRM\Logs\Sessions\SESSION_[N]_SUMMARY.md before ending
```

---

## WHY THESE RULES?

| Problem | Cause | Prevention |
|---------|-------|------------|
| Session crash | scipy import takes 245+ seconds | No heavy Python execution |
| Encoding errors | Emoji characters (155 instances) | ASCII-only in system files |
| Lost work | No checkpoints before crash | Incremental saves every 3 calls |
| Repeated crashes | Retrying failed operation | Crash recovery protocol |

---

## CURRENT STATUS OF YOUR INSTRUCTIONS

Your current project instructions include:

```
. Read D:\HIRM\Logs\BUILD_STATUS.md for crash recovery status
. Check D:\HIRM\Logs\Sessions\ for latest session summary
. Follow protocols in D:\HIRM\Protocols\HIRM_RESEARCH_PROTOCOLS_v2.3.md
. Update BUILD_STATUS.md before/after any file operations
. End session with layman summary saved to Logs\Sessions\SESSION_[N]_SUMMARY.md
```

This is good but incomplete. The amendment above adds the critical rules about:
- No heavy Python
- ASCII-only
- Timeout discipline
- Crash recovery (don't retry)

---

## HOW TO APPLY

1. Go to your Claude project settings
2. Find the custom instructions / system prompt section
3. Add the "TEXT TO ADD" section above at the TOP (before existing instructions)
4. Save

This will take effect on all new sessions.

---

## LEARNING FROM ERRORS

Yes, we ARE learning from the emoji and character issues. This amendment captures that learning:

| Error Pattern | Sessions Affected | Fix Applied |
|---------------|-------------------|-------------|
| Heavy Python timeout | 12, 13, 14 | Rule 2: No scipy/numpy execution |
| Emoji encoding issues | Multiple | Rule 3: ASCII-only system files |
| Lost work on crash | 12, 13, 14 | Rule 4: Incremental saves |
| Repeated crash attempts | Observed | Rule 7: Don't retry crashing ops |

The corrections are now encoded in:
1. CRASH_PREVENTION_PROTOCOL.md (detailed rules)
2. START_HERE.md (quick reference)
3. This amendment (project-wide enforcement)
4. BUILD_STATUS.md (runtime tracking)

---

**This is how we build the right way the first time going forward.**
