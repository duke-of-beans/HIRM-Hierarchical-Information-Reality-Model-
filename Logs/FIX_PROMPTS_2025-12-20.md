# HIRM AUDIT FIX PROMPTS
**Generated:** 2025-12-20
**Source:** AUDIT_REPORT_2025-12-20.md

Run these prompts in separate sessions to fix audit issues safely.
Each prompt is self-contained and crash-resistant.

---

## PROMPT 1: Protocol Version Update (v2.2 -> v2.3)

```
HIRM FIX TASK: Update Protocol Version References

CRASH PREVENTION:
- Read BUILD_STATUS.md first
- Update BUILD_STATUS every 3 tool calls
- ASCII-only markers: [OK] [DONE] [FAIL]

TASK: Update all v2.2 references to v2.3

FILES TO UPDATE (4 files):
1. D:\HIRM\Protocols\CRASH_PREVENTION_PROTOCOL.md
2. D:\HIRM\Protocols\PROJECT_INSTRUCTION_AMENDMENT.md
3. D:\HIRM\START_HERE.md
4. D:\HIRM\Protocols\CONTINUATION_PROMPTS.md (has 3 references)

PROCESS:
1. Read BUILD_STATUS.md
2. Log "FIX-1: Protocol Version Update - STARTED" to BUILD_STATUS
3. For each file:
   - Read file (max 500 lines)
   - Find "v2.2" or "2.2" references to protocols
   - Replace with "v2.3" or "2.3"
   - Save file
   - Log "[DONE] filename" to BUILD_STATUS
4. Log "FIX-1: COMPLETE" to BUILD_STATUS

DO NOT: Run any Python, import libraries, or execute scripts.
```

---

## PROMPT 2: Terminology Fix - Theory/Core (5 files)

```
HIRM FIX TASK: Terminology Compliance - Theory/Core

CRASH PREVENTION:
- Read BUILD_STATUS.md first
- Update BUILD_STATUS every 3 tool calls
- ASCII-only markers: [OK] [DONE] [FAIL]
- Max 500 lines per file read

TASK: Replace forbidden terminology in Theory/Core/

TERMINOLOGY RULES:
- "Ouroboros Observer" -> "HIRM"
- "OO Theory" -> "HIRM"
- "proves consciousness" -> "supports the hypothesis that"
- "explains consciousness" -> "proposes a mechanism for"

PROCESS:
1. Read BUILD_STATUS.md
2. Log "FIX-2: Terminology Core - STARTED" to BUILD_STATUS
3. List D:\HIRM\Theory\Core\ directory
4. For each .md file:
   - Search for forbidden terms
   - If found, read file and apply replacements
   - Save file
   - Log result to BUILD_STATUS
5. Log "FIX-2: COMPLETE" to BUILD_STATUS

DO NOT: Run any Python, modify _Archive files, or execute scripts.
```

---

## PROMPT 3: Terminology Fix - Theory/Extensions (12 files)

```
HIRM FIX TASK: Terminology Compliance - Theory/Extensions

CRASH PREVENTION:
- Read BUILD_STATUS.md first
- Update BUILD_STATUS every 3 tool calls
- ASCII-only markers: [OK] [DONE] [FAIL]
- Max 500 lines per file read
- Process max 4 files per session to avoid timeout

TASK: Replace forbidden terminology in Theory/Extensions/

TERMINOLOGY RULES:
- "Ouroboros Observer" -> "HIRM"
- "OO Theory" -> "HIRM"
- "proves consciousness" -> "supports the hypothesis that"
- "explains consciousness" -> "proposes a mechanism for"

PROCESS:
1. Read BUILD_STATUS.md
2. Log "FIX-3: Terminology Extensions - STARTED" to BUILD_STATUS
3. List D:\HIRM\Theory\Extensions\ directory
4. Process first 4 files with violations:
   - Search for forbidden terms
   - If found, read file and apply replacements
   - Save file
   - Log result to BUILD_STATUS
5. Log "FIX-3: PARTIAL/COMPLETE" to BUILD_STATUS
6. If more files remain, note them for next session

DO NOT: Run any Python, modify _Archive files, or process more than 4 files.
```

---

## PROMPT 4: Terminology Fix - Theory/Extensions (Batch 2)

```
HIRM FIX TASK: Terminology Compliance - Theory/Extensions Batch 2

CRASH PREVENTION:
- Read BUILD_STATUS.md first
- Update BUILD_STATUS every 3 tool calls
- ASCII-only markers: [OK] [DONE] [FAIL]
- Max 500 lines per file read
- Process max 4 files per session

TASK: Continue fixing Theory/Extensions/ from where Prompt 3 stopped

PROCESS:
1. Read BUILD_STATUS.md to see which files were already fixed
2. Log "FIX-4: Terminology Extensions Batch 2 - STARTED"
3. Process next 4 unfixed files
4. Log results
5. Log "FIX-4: COMPLETE" if all done

DO NOT: Run any Python, modify _Archive files, or reprocess already-fixed files.
```

---

## PROMPT 5: Terminology Fix - Theory/Extensions (Batch 3)

```
HIRM FIX TASK: Terminology Compliance - Theory/Extensions Batch 3

CRASH PREVENTION:
- Read BUILD_STATUS.md first
- Update BUILD_STATUS every 3 tool calls
- ASCII-only markers: [OK] [DONE] [FAIL]
- Max 500 lines per file read
- Process remaining files (should be 4 or fewer)

TASK: Complete fixing Theory/Extensions/

PROCESS:
1. Read BUILD_STATUS.md to see which files were already fixed
2. Log "FIX-5: Terminology Extensions Batch 3 - STARTED"
3. Process remaining unfixed files
4. Log results
5. Log "FIX-5: COMPLETE - All Extensions fixed"

DO NOT: Run any Python, modify _Archive files, or reprocess already-fixed files.
```

---

## PROMPT 6: Emoji Conversion - Logs/ Directory

```
HIRM FIX TASK: ASCII Conversion - Logs Directory

CRASH PREVENTION:
- Read BUILD_STATUS.md first
- Update BUILD_STATUS every 3 tool calls
- ASCII-only output
- Max 500 lines per file read
- Process max 3 files per session

TASK: Convert emojis to ASCII markers in Logs/

CONVERSION TABLE:
- Checkmark emojis -> [OK] or [DONE]
- X/cross emojis -> [FAIL]
- Warning emojis -> [WARN]
- Arrow/pointer emojis -> [TODO] or "->"
- Star/sparkle emojis -> [NOTE]
- Any other emojis -> remove or replace with text equivalent

PRIORITY FILES:
1. SESSION_14_SUMMARY.md
2. SESSION_9_AUDIT_SUMMARY.md
3. Any other session files with emojis

PROCESS:
1. Read BUILD_STATUS.md
2. Log "FIX-6: Emoji Logs - STARTED"
3. List Logs/ and Logs/Sessions/
4. For each file with emojis (max 3):
   - Read file
   - Replace emojis per conversion table
   - Save file
   - Log "[DONE] filename"
5. Log progress to BUILD_STATUS

DO NOT: Run Python, process more than 3 files, or modify BUILD_STATUS format.
```

---

## PROMPT 7: Emoji Conversion - Protocols/ Directory

```
HIRM FIX TASK: ASCII Conversion - Protocols Directory

CRASH PREVENTION:
- Read BUILD_STATUS.md first
- Update BUILD_STATUS every 3 tool calls
- ASCII-only output
- Max 500 lines per file read
- Process max 2 files per session (protocols are larger)

TASK: Convert emojis to ASCII markers in Protocols/

CONVERSION TABLE:
- Checkmark emojis -> [OK] or [DONE]
- X/cross emojis -> [FAIL]
- Warning emojis -> [WARN]
- Arrow/pointer emojis -> [TODO] or "->"
- Star/sparkle emojis -> [NOTE]
- Any other emojis -> remove or replace with text equivalent

PRIORITY FILES:
1. MASTER_SYNTHESIS_ENGINE_v2.md
2. Other protocol files with emojis

PROCESS:
1. Read BUILD_STATUS.md
2. Log "FIX-7: Emoji Protocols - STARTED"
3. Search Protocols/ for emoji content
4. Process max 2 files per session
5. Log progress to BUILD_STATUS

DO NOT: Run Python, process more than 2 files, or break file formatting.
```

---

## PROMPT 8: Emoji Conversion - Master_Data/ Directory

```
HIRM FIX TASK: ASCII Conversion - Master_Data Directory

CRASH PREVENTION:
- Read BUILD_STATUS.md first
- Update BUILD_STATUS every 3 tool calls
- ASCII-only output
- Max 500 lines per file read
- Process max 3 files per session

TASK: Convert emojis to ASCII markers in Master_Data/

CONVERSION TABLE:
- Checkmark emojis -> [OK] or [DONE]
- X/cross emojis -> [FAIL]
- Warning emojis -> [WARN]
- Arrow/pointer emojis -> [TODO] or "->"
- Star/sparkle emojis -> [NOTE]
- Any other emojis -> remove or replace with text equivalent

PRIORITY FILES:
1. terminology_reference.md
2. corrections_registry.md
3. Other Master_Data files with emojis

PROCESS:
1. Read BUILD_STATUS.md
2. Log "FIX-8: Emoji Master_Data - STARTED"
3. Search Master_Data/ subdirectories for emoji content
4. Process max 3 files per session
5. Log progress to BUILD_STATUS

CRITICAL: Do NOT modify locked_constants.md values, only emoji formatting if present.

DO NOT: Run Python, change constant values, or process more than 3 files.
```

---

## PROMPT 9: START_HERE.md Version Header Fix

```
HIRM FIX TASK: Fix START_HERE.md Version Inconsistency

CRASH PREVENTION:
- Read BUILD_STATUS.md first
- Update BUILD_STATUS after fix
- ASCII-only markers

TASK: Fix version header inconsistency in START_HERE.md

ISSUE: Header shows "Version 2.1" but should reference v2.3

PROCESS:
1. Read BUILD_STATUS.md
2. Log "FIX-9: START_HERE Version - STARTED"
3. Read D:\HIRM\START_HERE.md
4. Update version header from 2.1 to 2.3
5. Verify any other version references are 2.3
6. Save file
7. Log "FIX-9: COMPLETE"

DO NOT: Run Python or change any content other than version numbers.
```

---

## PROMPT 10: Verification Audit

```
HIRM FIX TASK: Verification Audit

CRASH PREVENTION:
- Read BUILD_STATUS.md first
- Update BUILD_STATUS every 3 tool calls
- ASCII-only markers
- NO Python execution

TASK: Verify all fixes from Prompts 1-9 were applied correctly

CHECKS:
1. Search for "v2.2" - should return 0 results in active files
2. Search for "Ouroboros Observer" in Theory/ - should return 0 in non-Archive
3. Spot-check 3 files for emoji presence in Logs/, Protocols/, Master_Data/
4. Verify START_HERE.md shows v2.3

PROCESS:
1. Read BUILD_STATUS.md
2. Log "FIX-10: Verification - STARTED"
3. Run each check using search tools
4. Document any remaining issues
5. Create VERIFICATION_REPORT_[DATE].md in Logs/
6. Log "FIX-10: COMPLETE" or "FIX-10: ISSUES REMAIN"

OUTPUT: Summary of verification with pass/fail for each check.

DO NOT: Run Python or make any file modifications.
```

---

## EXECUTION ORDER

Run prompts in this order, one per session:

| Order | Prompt | Est. Files | Priority |
|-------|--------|------------|----------|
| 1 | Protocol Version (Prompt 1) | 4 | CRITICAL |
| 2 | START_HERE Fix (Prompt 9) | 1 | CRITICAL |
| 3 | Terminology Core (Prompt 2) | 5 | CRITICAL |
| 4 | Terminology Ext 1 (Prompt 3) | 4 | CRITICAL |
| 5 | Terminology Ext 2 (Prompt 4) | 4 | CRITICAL |
| 6 | Terminology Ext 3 (Prompt 5) | 4 | CRITICAL |
| 7 | Emoji Logs (Prompt 6) | 3 | MEDIUM |
| 8 | Emoji Protocols (Prompt 7) | 2 | MEDIUM |
| 9 | Emoji Master_Data (Prompt 8) | 3 | MEDIUM |
| 10 | Verification (Prompt 10) | 0 | REQUIRED |

**Total estimated sessions:** 10
**Can combine:** Prompts 1+9 if session stable

---

## NOTES

- Each prompt is designed to be crash-resistant
- If a session crashes, restart with the same prompt
- BUILD_STATUS.md tracks progress across sessions
- _Archive files are intentionally NOT modified (historical record)
- Emoji fixes are lower priority than terminology/version fixes

---

*Generated from AUDIT_REPORT_2025-12-20.md*
