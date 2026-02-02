# CORRECTIONS REGISTRY
## Self-Healing Error Tracking
## Last Updated: 2025-12-21

---

## PURPOSE

This registry tracks errors, corrections, and theory updates to enable:
1. **Self-healing:** Prevent recurrence of known errors
2. **Learning:** Understand why errors occurred
3. **Protocol updates:** Add prevention to protocols when patterns emerge
4. **Intellectual honesty:** Transparent record of mistakes

---

## ACTIVE CORRECTIONS

### TERMINOLOGY CORRECTIONS

| ID | Original | Corrected | Reason | Recurrence | Added to Protocol |
|----|----------|-----------|--------|------------|-------------------|
| T001 | Ouroboros Observer | HIRM | Legacy branding, unprofessional | 5+ | [YES] |
| T002 | OO Theory | HIRM Theory | Legacy abbreviation | 3 | [YES] |
| T003 | "proves consciousness" | "supports the hypothesis" | Overly strong claim | 2 | [YES] |

### CONSTANT CORRECTIONS

| ID | Original | Corrected | Reason | Recurrence | Added to Protocol |
|----|----------|-----------|--------|------------|-------------------|
| C001 | C_critical = 7.5 | C_critical = 8.3 +/- 0.6 | Outdated early estimate | 1 | [YES] |

### EQUATION CORRECTIONS

| ID | Original | Corrected | Reason | Recurrence | Added to Protocol |
|----|----------|-----------|--------|------------|-------------------|
| E001 | C = Phi + R + D | C = Phi x R x D | Multiplicative, not additive | 0 | [YES] |

### CLAIM CORRECTIONS

| ID | Original | Corrected | Reason | Recurrence | Added to Protocol |
|----|----------|-----------|--------|------------|-------------------|
| (none yet) | | | | | |

---

## ERROR PREVENTION RULES

### From T001-T002: Terminology
**Rule:** Always check `terminology_reference.md` before using framework name
**Automated:** Quality gate flags "Ouroboros" in any document

### From T003: Claim Strength
**Rule:** Never claim to "prove" consciousness - use "support hypothesis"
**Automated:** Quality gate flags "proves consciousness"

### From C001: Constants
**Rule:** All constants must match `locked_constants.md`
**Automated:** Quality gate checks constant values against database

### From E001: Core Equation
**Rule:** Consciousness formula is multiplicative: C = Φ × R × D
**Automated:** Quality gate verifies equation form

---

## SEVERITY LEVELS

| Level | Definition | Action Required |
|-------|------------|-----------------|
| CRITICAL | Fundamental error in core claim | Immediate correction, notify David |
| HIGH | Significant factual error | Correct within session, update protocol |
| MEDIUM | Minor error, doesn't affect conclusions | Correct when convenient |
| LOW | Style/preference issue | Note for future reference |

---

## CORRECTION WORKFLOW

When an error is discovered:

1. **Document immediately:**
   - Original text
   - Corrected text
   - Reason for correction
   - Source of discovery

2. **Check recurrence:**
   - Search corpus for same error
   - Count instances
   - Update recurrence count

3. **Update database:**
   - Add to corrections table in hirm.db
   - Include severity level

4. **Fix all instances:**
   - Find all documents with error
   - Apply correction
   - Verify fix

5. **Add to protocol (if recurrence ≥ 2):**
   - Add prevention rule to relevant protocol
   - Update quality gate if possible
   - Mark "added_to_protocol = true"

---

## STATISTICS

| Metric | Value |
|--------|-------|
| Total corrections logged | 5 |
| Critical corrections | 0 |
| High severity | 1 (C001) |
| Medium severity | 4 (T001-T003, E001) |
| Added to protocol | 5 (100%) |

---

## MONTHLY REVIEW

At start of each month:
1. Review all corrections from previous month
2. Identify patterns
3. Update protocols to prevent recurrence
4. Clear resolved corrections older than 6 months
