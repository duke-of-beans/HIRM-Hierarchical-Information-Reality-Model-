# HIRM RESEARCH CONTINUATION PROMPTS
## Copy-Paste Ready Prompts for New Claude Sessions

---

## 🚀 STANDARD CONTINUATION PROMPT

```
Continue HIRM research.

1. Read D:\HIRM\Logs\BUILD_STATUS.md for crash recovery status
2. Read D:\HIRM\Documentation\HIRM_RESEARCH_TOPICS.md for priorities
3. Check D:\HIRM\Logs\Sessions\ for latest session summary
4. Follow protocols in D:\HIRM\Protocols\HIRM_RESEARCH_PROTOCOLS_v2.3.md

Update BUILD_STATUS.md before/after any file operations.
End session with layman summary saved to Logs\Sessions\SESSION_[N]_SUMMARY.md
```

---

## 🎯 SPECIFIC TASK PROMPTS

### Execute Next Research Priority
```
Continue HIRM research - execute the next highest priority from HIRM_RESEARCH_TOPICS.md

Check BUILD_STATUS.md first, then:
1. Find next UNTESTED or incomplete item in Tier 1
2. Implement/analyze as appropriate
3. Update status when complete
4. End with session summary
```

### Literature Deep Dive
```
HIRM research: Deep dive on [TOPIC]

Search project knowledge and web for latest papers on [TOPIC].
Focus on:
- Connections to HIRM framework
- Potential falsification evidence
- New experimental approaches

Update HIRM_RESEARCH_TOPICS.md with findings.
End with session summary.
```

### Code Implementation
```
HIRM research: Implement [FEATURE/ANALYSIS]

Check BUILD_STATUS.md, then:
1. Review relevant existing code in D:\HIRM\Code\
2. Implement [FEATURE]
3. Add synthetic validation
4. Update BUILD_STATUS.md with ✅
5. End with session summary
```

### Validate/Debug Existing Code
```
HIRM research: Validate existing implementations

1. Run synthetic tests on Code/Core/*.py
2. Check for bugs (especially Φ calculation)
3. Verify outputs match locked_constants.md
4. Document any issues found
5. End with session summary
```

### Publication Prep
```
HIRM research: Publication preparation for [PAPER N]

Focus: [Paper 1: Brain Criticality / Paper 2: Quantum Bridge / Paper 3: Information Persistence]

1. Gather relevant materials from corpus
2. Check all constants against locked_constants.md
3. Run quality gate on any drafts
4. End with session summary
```

---

## 🔧 UTILITY PROMPTS

### Quick Status Check
```
HIRM status check - read BUILD_STATUS.md and HIRM_RESEARCH_TOPICS.md, give me a 5-line summary of where we are.
```

### Crash Recovery
```
Claude crashed. Check D:\HIRM\Logs\BUILD_STATUS.md for incomplete work. Verify any 🔄 files, clean up if needed, then continue.
```

### End Session Early
```
End HIRM session now. Update BUILD_STATUS.md and create session summary in Logs\Sessions\
```

---

## 📋 PROMPT COMPONENTS (Mix & Match)

### Always Include:
```
Check BUILD_STATUS.md first.
Update BUILD_STATUS.md before/after file operations.
End with session summary.
```

### For Research Tasks:
```
Follow HIRM_RESEARCH_PROTOCOLS_v2.3.md
Use locked_constants.md values (C_critical = 8.3 ± 0.6 bits)
No "Ouroboros Observer" terminology - use "HIRM"
```

### For Code Tasks:
```
Mark files 🔄 IN PROGRESS before starting
Mark ✅ COMPLETE with line count after
Include synthetic validation in scripts
```

### For Literature Tasks:
```
Search project knowledge first (193+ papers indexed)
Use web search for papers after 2024
Add new rabbit holes to HIRM_RESEARCH_TOPICS.md
```

---

## ⚡ QUICK START (Shortest Effective Prompt)

```
Continue HIRM. Check BUILD_STATUS.md → execute next priority from HIRM_RESEARCH_TOPICS.md → end with session summary.
```

---

**File Location:** `D:\HIRM\Documentation\CONTINUATION_PROMPTS.md`
**Created:** 2025-12-20
