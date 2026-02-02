# CRASH RECOVERY PROTOCOL
## For HIRM Research Sessions

---

## THE PROBLEM
Claude sessions crash during long research tasks. Work may be:
- ✅ Complete but unconfirmed
- 🔄 Partially written (file truncated)
- ❌ Never started

---

## THE SOLUTION

### File: `D:\HIRM\Logs\BUILD_STATUS.md`

Claude updates this file at **3 checkpoints**:

1. **BEFORE starting a file:** Mark as 🔄 IN PROGRESS
2. **AFTER completing a file:** Mark as ✅ COMPLETE with line count
3. **On session end:** Summary of all work

---

## FOR DAVID: Quick Recovery Steps

### Step 1: Check BUILD_STATUS.md
```powershell
Get-Content D:\HIRM\Logs\BUILD_STATUS.md
```

### Step 2: Verify any 🔄 files
```powershell
# Check file exists and size
Get-ChildItem "D:\HIRM\path\to\file.py" | Select-Object Name, Length

# Check last lines (should have proper ending)
Get-Content "D:\HIRM\path\to\file.py" -Tail 10
```

### Step 3: Resume with new Claude
Just say: "Check BUILD_STATUS.md and continue"

---

## FOR CLAUDE: Update Protocol

### At session start:
```
Read D:\HIRM\Logs\BUILD_STATUS.md
Check for incomplete (🔄) items
Resume or clean up as needed
```

### Before creating/editing any file:
```
Update BUILD_STATUS.md:
- Add file path
- Mark as 🔄 IN PROGRESS
- Note expected outcome
```

### After completing any file:
```
Update BUILD_STATUS.md:
- Mark as ✅ COMPLETE
- Add line count
- Add verification note
```

---

## EXAMPLE BUILD_STATUS.md ENTRY

```markdown
### 🔄 my_analysis.py (IN PROGRESS)
- **Path:** `D:\HIRM\Code\my_analysis.py`
- **Expected:** ~200 lines, consciousness analysis
- **Started:** 13:45 PST

### ✅ my_analysis.py (COMPLETE)
- **Path:** `D:\HIRM\Code\my_analysis.py`
- **Lines:** 215
- **Verified:** Has proper main block, imports work
- **Completed:** 13:52 PST
```

---

## INTEGRATION WITH PROTOCOLS v2.2

Add to Section 5.3 Session Logging:

> **Crash Recovery:** Update `Logs/BUILD_STATUS.md` before and after 
> each file operation. This file serves as real-time progress tracking
> that survives session crashes.

---

**Created:** 2025-12-20
**Purpose:** Never lose work to Claude crashes again
