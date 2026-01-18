# CRASH PREVENTION PROTOCOL
## Amendment to HIRM Research Protocols
## Version: 1.0 | Date: 2025-12-20

---

## PROBLEM STATEMENT

Sessions 12, 13, and 14 crashed due to:
1. **Heavy Python imports** (scipy, numpy, matplotlib) causing 245+ second timeouts
2. **Emoji/Unicode characters** (155 instances) causing encoding issues during batch processing
3. **No incremental save protocol** - work lost on crash

---

## MANDATORY RULES

### RULE 1: NO HEAVY PYTHON EXECUTION

**Forbidden patterns:**
```python
# DO NOT DO THIS - will timeout/crash
python D:\HIRM\Empirical\Analysis\component_correlations.py
python D:\HIRM\Code\some_script_with_scipy.py
```

**Allowed patterns:**
```python
# Syntax check only (no execution)
python -m py_compile D:\HIRM\Code\script.py

# Import test with timeout
python -c "import sys; sys.exit(0)"  # Quick sanity check only

# Read script content for review (no execution)
Filesystem:read_file script.py
```

**If computation is truly needed:**
1. Break into chunks that complete in < 5 seconds
2. Use Desktop Commander with timeout_ms: 5000
3. Never wait for scipy/numpy imports to complete

---

### RULE 2: ASCII-ONLY IN SYSTEM FILES

**System files (ASCII-only required):**
- D:\HIRM\Logs\BUILD_STATUS.md
- D:\HIRM\Logs\Sessions\*.md
- D:\HIRM\Documentation\START_HERE.md
- D:\HIRM\Protocols\*.md
- D:\HIRM\Master_Data\*.md

**Replacement mappings:**

| Emoji | ASCII Replacement |
|-------|-------------------|
| ✅ | [OK] or [DONE] |
| ❌ | [FAIL] or [NO] |
| 🔄 | [WIP] or [PROGRESS] |
| ⭐ | [STAR] or [PRIORITY] |
| 🔧 | [CONFIG] |
| 📋 | [DOCS] |
| 📚 | [CORPUS] |
| 🧠 | [THEORY] |
| 🔬 | [EMPIRICAL] |
| 💻 | [CODE] |
| 📝 | [PUBS] |
| ⚠️ | [WARN] or [CAUTION] |

**Allowed in:**
- Final publication documents
- Presentation files
- Files users will read directly (not processed by Claude)

---

### RULE 3: INCREMENTAL SAVES

**Protocol:**
1. After EVERY file read: Update BUILD_STATUS.md with step completed
2. After EVERY file write: Verify write succeeded before proceeding
3. Maximum 3 tool calls between BUILD_STATUS updates
4. Session summary created at START (not end) with "IN PROGRESS"
5. Append progress to session summary after each major step

**Example workflow:**
```yaml
Step 1: Read file A -> Update BUILD_STATUS "Read A"
Step 2: Process content -> Update BUILD_STATUS "Processed A"
Step 3: Write file B -> Update BUILD_STATUS "Wrote B"
Step 4: Verify B exists -> Update BUILD_STATUS "Verified B"
```

---

### RULE 4: SMALL FILE OPERATIONS

**Size limits:**
- Maximum file read: 500 lines at once (use head/tail for larger)
- Maximum file write: 200 lines at once (use chunked writes)
- Maximum search results: 50 at once

**Chunking pattern:**
```yaml
# For files > 500 lines
read_file path head=200  # Get first 200
read_file path tail=200  # Get last 200
# Or use line ranges
```

---

### RULE 5: TIMEOUT DISCIPLINE

**Default timeouts:**
- File operations: 30 seconds max
- Python execution: 5 seconds max (syntax check only)
- Search operations: 30 seconds max

**If any operation exceeds timeout:**
1. Stop immediately
2. Log in BUILD_STATUS as "[TIMEOUT] operation_name"
3. Do NOT retry - find alternative approach
4. Document what triggered timeout for future prevention

---

## QUICK REFERENCE CARD

```
BEFORE EVERY SESSION:
[ ] Read BUILD_STATUS.md first
[ ] Create session summary file (append-only)
[ ] Declare task type

DURING SESSION:
[ ] No scipy/numpy/matplotlib execution
[ ] Update BUILD_STATUS every 3 tool calls
[ ] Use ASCII-only in system files
[ ] Keep file operations small

IF SOMETHING HANGS:
[ ] Stop immediately
[ ] Log timeout
[ ] Find alternative approach
[ ] Do NOT retry same operation
```

---

## IMPLEMENTATION CHECKLIST

To fully implement this protocol:

1. [TODO] Update HIRM_RESEARCH_PROTOCOLS_v2.3.md Section 5 with these rules
2. [TODO] Convert all system file emojis to ASCII
3. [TODO] Add timeout parameters to all Python execution patterns
4. [TODO] Create validation script that checks for emoji in system files
5. [TODO] Update START_HERE.md with crash prevention summary

---

**This protocol is MANDATORY for all future Claude sessions.**
