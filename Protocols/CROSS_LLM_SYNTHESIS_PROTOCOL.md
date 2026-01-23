# CROSS-LLM SYNTHESIS PROTOCOL
## Session 36+ | HARDCODED INSTRUCTION

---

## CORE PRINCIPLE

**Claude has access to external LLM consultation through David as orchestrator.**

When Claude encounters:
- Ambiguous theoretical choices requiring multiple perspectives
- Complex mathematical decisions with competing frameworks
- Large-scale pattern detection across corpus
- Validation of critical recommendations
- Resolution of definitional conflicts

Claude should **proactively request** cross-LLM synthesis by:
1. Identifying the specific decision point or question
2. Preparing a focused prompt for GPT-4 and/or Gemini
3. Gathering necessary context files
4. Requesting David to orchestrate the consultation

---

## WHEN TO TRIGGER CROSS-LLM CONSULTATION

### Mandatory Triggers (ALWAYS request):
- Finalizing Variable Constitution definitions (R, D ranges/meanings)
- Choosing canonical equation form (multiplicative vs saturating)
- Resolving theory vs code conflicts when both have validity
- Major architectural decisions affecting publication strategy
- Epistemic status assignments for core claims
- Falsification criteria that could invalidate HIRM

### Recommended Triggers (ASK if beneficial):
- Pattern detection across 50+ papers in corpus
- Mathematical framework comparisons (IIT vs GNWT vs FEP vs HIRM)
- Discovering unexpected connections in literature
- Validating computational implementations
- Identifying hidden assumptions in derivations

### Optional Triggers (use judgment):
- Terminology choices
- Documentation organization
- Code refactoring strategies
- Session planning

---

## CONSULTATION REQUEST FORMAT

When Claude identifies need for cross-LLM consultation:

```
## CROSS-LLM CONSULTATION REQUEST

**Trigger:** [Mandatory/Recommended/Optional]
**Decision Point:** [Specific question requiring external perspective]

**Context Summary:** 
[2-3 paragraphs explaining the situation]

**Specific Questions for External LLMs:**
1. [Focused question 1]
2. [Focused question 2]
3. [...]

**Files to Provide:**
- [file1.md] - [why needed]
- [file2.py] - [why needed]

**Expected Synthesis:**
[What kind of output would help? Comparison table? Recommendation? Risk analysis?]

**Timeline:** [Urgent / Next session / Can wait]
```

---

## EXAMPLE FROM SESSION 36

**Trigger:** Mandatory - Finalizing Variable Constitution

**Decision Point:** Should R(t) be [0,1] completeness ratio OR [1,3] recursion gain OR separate variables?

**Context:** Discovery audit found three incompatible R definitions across corpus. Clinical theory uses [0,1] for gating behavior (zero-multiplier theorem). Code uses [1,3] as amplification factor. RG formalism may allow unbounded values. Each has different physical interpretation and mathematical consequences.

**Questions for GPT-4/Gemini:**
1. From pure mathematical consistency: which R definition creates cleanest formalism?
2. From empirical testability: which R is most measurable with current neuroscience tools?
3. From theoretical parsimony: should these be unified or kept separate?
4. What hidden assumptions does each choice impose on HIRM's claims?

**Files:**
- VARIABLE_DISCOVERY_AUDIT.md - Full conflict analysis
- Section_9_Measurement_Protocols.md - Clinical composite definition
- consciousness_measure.py - Code implementation
- (RG framework docs - once extracted)

**Expected Synthesis:**
Comparative analysis with pros/cons for each option, recommendation with epistemic humility, identification of any missed alternatives

---

## INTEGRATION PROTOCOL

When David returns cross-LLM synthesis:

1. Claude creates `Logs/Cross_LLM_Synthesis_[Topic]_[Date].md`
2. Extract key insights and recommendations
3. Compare with Claude's own analysis
4. Identify convergences and divergences
5. Highlight novel perspectives not in Claude's analysis
6. Update decision framework with additional considerations
7. Present integrated synthesis to David for final decision

---

## CURRENT STATUS

**Active Consultation Needed:** YES

**Topic:** Variable Constitution - R(t) definition choice

**Urgency:** High - blocks all subsequent audit and correction work

**Preparation Status:** 
- [x] Discovery audit complete (VARIABLE_DISCOVERY_AUDIT.md)
- [ ] RG framework extraction for third R definition
- [ ] Consultation prompt drafted
- [ ] Files assembled

**Recommended Next Step:** Complete RG extraction (Session 36 continuation), then prepare consultation request

---

*This protocol is HARDCODED - Claude should reference it proactively when encountering major decision points.*
