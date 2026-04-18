# PROMPT FOR FILE UPDATE GENERATION INSTANCE

## PURPOSE
You are receiving the SESSION_LOGS_MASTER_SYNTHESIS_v3.0.md document which contains ALL corrections, discoveries, and required updates from 21 application generation sessions (Dec 8-16, 2025). Your task is to generate individual, comprehensive prompts for development instances that will update each affected data file and protocol.

## YOUR DELIVERABLES

Generate a separate, self-contained prompt for EACH of the following files that require updates. Each prompt will be delivered to a dedicated development instance along with the ORIGINAL file being replaced.

### Files Requiring Update Prompts:

1. **Work_Group/professional_history.md** (LARGEST - ~35 distinct updates)
2. **Work_Group/achievements_database.md** (~15 updates + new sections)
3. **Work_Group/voice_writing_patterns.md** (~25 updates)
4. **Work_Group/philosophy_values.md** (~12 updates)
5. **Work_Group/skills_technical_proficiencies.md** (~8 updates)
6. **Work_Group/contact_information.md** (~4 updates)
7. **protocol_critical_stories_v1_machine.md** (~7 updates including CRITICAL title fix)
8. **protocol_resume_structure_v1_machine.md** (~5 updates)
9. **protocol_voice_enforcement_v1_machine.md** (~8 updates)
10. **PROJECT_INSTRUCTIONS_MASTER** (~12 updates)

### New Files to Create (prompts for creation):

11. **LOCKED_METRICS_REGISTRY.md**
12. **SIX_EXECUTIVE_ROSTER.md**
13. **RELOCATION_FRAMING_TEMPLATES.md**
14. **INDUSTRY_LANGUAGE_BANKS.md**
15. **OPENING_HOOK_TEMPLATES.md**
16. **COVER_LETTER_STRUCTURE_VARIANTS.md**

---

## PROMPT GENERATION REQUIREMENTS

Each prompt you generate must include:

### 1. CONTEXT HEADER
```
# FILE UPDATE PROMPT: [filename]
## Source: SESSION_LOGS_MASTER_SYNTHESIS_v3.0 (21 sessions, Dec 8-16, 2025)
## Priority: [CRITICAL/HIGH/MEDIUM]
## Update Count: [X distinct changes]
```

### 2. INSTRUCTIONS TO DEVELOPMENT INSTANCE
Clear instructions that the development instance will:
- Receive the ORIGINAL file they are replacing
- Make ALL specified changes
- Preserve all existing content not marked for change
- Maintain the file's existing format/structure
- Output a complete, updated file ready to replace the original

### 3. COMPLETE CHANGE MANIFEST
Every single change extracted from the synthesis, organized by section/category within that file. Include:
- Exact location of change (section name, line reference if helpful)
- Current/wrong value (if applicable)
- Correct/new value (with full text where needed)
- Source session (for traceability)

### 4. VERIFICATION CHECKLIST
A checklist the development instance must complete before delivering the updated file.

### 5. CRITICAL WARNINGS
Any "NEVER do X" or "ALWAYS do Y" rules relevant to that specific file.

---

## EXAMPLE PROMPT STRUCTURE

```markdown
# FILE UPDATE PROMPT: Work_Group/professional_history.md

## Source: SESSION_LOGS_MASTER_SYNTHESIS_v3.0 (21 sessions, Dec 8-16, 2025)
## Priority: CRITICAL
## Update Count: 35 distinct changes

---

## INSTRUCTIONS

You are receiving the original professional_history.md file. Your task is to apply ALL changes specified below while preserving all existing content not explicitly marked for modification. Output a complete, updated file.

---

## CHANGE MANIFEST

### Section: GOOD DAY FARM

**Change 1: Location Correction**
- WRONG: Monroe, Louisiana (if present)
- CORRECT: Ruston, Louisiana

**Change 2: Add cGMP/GAP-ready notation**
- ADD to facility description: "cGMP-level and GAP-ready operational infrastructure"

**Change 3: Add Hub-and-Spoke Achievement**
- ADD new content:
  ```
  Hub-and-Spoke Distribution Model:
  - Context: Facility in far north Louisiana (Ruston), retailers concentrated in south
  - Action: Proposed lean satellite inventory/distribution hub in Baton Rouge
  - Facility size: 30,000 sqft
  - Results: Cut overtime hours, improved on-time delivery, enabled scheduled service windows
  - Total under management: 225,000 sqft primary + 30,000 sqft satellite = 255,000 sqft
  ```

[... continue for all 35 changes ...]

---

## VERIFICATION CHECKLIST

Before delivering the updated file, confirm:
- [ ] All 35 changes applied
- [ ] Existing content preserved where not modified
- [ ] File format consistent with original
- [ ] No fabrication - only synthesis-specified content added
- [ ] Departure reasons use verified language from synthesis

---

## CRITICAL WARNINGS

- NEVER change content not specified in this prompt
- NEVER add content not specified in this prompt
- ALWAYS use exact text provided for new content
- If unsure about a change, mark it clearly for review rather than guessing
```

---

## EXTRACTION INSTRUCTIONS

For each file, extract from SESSION_LOGS_MASTER_SYNTHESIS_v3.0:

1. **Section 13 (File Update Checklist)** - Primary source of what changes each file needs
2. **Relevant numbered sections** - Details for each change:
   - Section 2 for professional_history.md
   - Section 3 for achievements_database.md
   - Section 4 for voice_writing_patterns.md
   - Section 5 for philosophy_values.md
   - Section 6 for skills_technical_proficiencies.md
   - Section 7 for contact_information.md
   - Sections 1, 8, 10 for protocol files
3. **Appendices** - For new files to create (A-E)

---

## PRIORITY ORDER FOR PROMPT GENERATION

Generate prompts in this order (CRITICAL first):

### CRITICAL (Generate First)
1. protocol_critical_stories_v1_machine.md (title correction affects fabrication prevention)
2. Work_Group/professional_history.md (most changes, foundational data)
3. Work_Group/voice_writing_patterns.md (organism analogy critical fix)

### HIGH (Generate Second)
4. Work_Group/achievements_database.md
5. Work_Group/skills_technical_proficiencies.md
6. protocol_resume_structure_v1_machine.md
7. LOCKED_METRICS_REGISTRY.md (new file)
8. SIX_EXECUTIVE_ROSTER.md (new file)

### MEDIUM (Generate Third)
9. Work_Group/philosophy_values.md
10. Work_Group/contact_information.md
11. protocol_voice_enforcement_v1_machine.md
12. PROJECT_INSTRUCTIONS_MASTER

### STANDARD (Generate Last)
13. RELOCATION_FRAMING_TEMPLATES.md (new file)
14. INDUSTRY_LANGUAGE_BANKS.md (new file)
15. OPENING_HOOK_TEMPLATES.md (new file)
16. COVER_LETTER_STRUCTURE_VARIANTS.md (new file)

---

## OUTPUT FORMAT

Generate each prompt as a separate markdown file:
- `UPDATE_PROMPT_professional_history.md`
- `UPDATE_PROMPT_achievements_database.md`
- `UPDATE_PROMPT_voice_writing_patterns.md`
- etc.

For new files:
- `CREATE_PROMPT_LOCKED_METRICS_REGISTRY.md`
- `CREATE_PROMPT_SIX_EXECUTIVE_ROSTER.md`
- etc.

---

## CRITICAL REMINDERS

1. **COMPLETENESS IS MANDATORY** - Every single item from the synthesis checklist (Section 13) must appear in the appropriate prompt. Missing items = incomplete update = errors in future sessions.

2. **EXACT TEXT FOR NEW CONTENT** - When the synthesis provides exact text (e.g., organism analogy, departure reasons), include that exact text in the prompt. Don't paraphrase.

3. **PRESERVE WHAT'S NOT CHANGING** - Development instances must be clearly instructed to keep all existing content that isn't being modified.

4. **TRACEABILITY** - Note which session(s) identified each change where relevant for future audit.

5. **NO FABRICATION** - Development instances should only add content specified in the prompt. If something seems missing, flag it rather than inventing content.

---

## VALIDATION

Before considering your prompt generation complete:
- [ ] All 10 existing files have update prompts
- [ ] All 6 new files have creation prompts
- [ ] Every checkbox in Section 13 of the synthesis is addressed in exactly one prompt
- [ ] Critical items (title corrections, organism analogy, R&D scope) are prominently featured
- [ ] Each prompt is self-contained and can be delivered independently

---

## BEGIN PROMPT GENERATION

You have received: SESSION_LOGS_MASTER_SYNTHESIS_v3.0.md

Start generating prompts for each file, beginning with the CRITICAL priority files.
