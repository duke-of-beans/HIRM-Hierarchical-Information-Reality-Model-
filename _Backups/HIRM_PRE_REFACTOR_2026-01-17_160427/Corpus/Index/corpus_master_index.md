# HIRM CORPUS MASTER INDEX
## Literature Database Summary
## Auto-generated: 2025-12-21
## Database: D:\HIRM\System\data\hirm.db

---

## OVERVIEW

| Metric | Value |
|--------|-------|
| Total Papers | 71 |
| Domains | 6 |
| Status: Read | 71 |
| Status: Integrated | 0 (pending) |

---

## PAPERS BY DOMAIN

### Self-Reference & Strange Loops
Papers exploring recursive self-modeling, autopoiesis, and strange loop dynamics.
- Key authors: Hofstadter, Maturana, Varela, Graziano, Fleming
- Relevance: Core to HIRM's R(t) component

### Quantum Biology
Evidence for quantum effects in biological systems.
- Key topics: Photosynthetic coherence, radical pairs, tunneling
- Relevance: Informs quantum-classical bridge discussions

### Brain Criticality
Neural avalanches, scale-free dynamics, edge of chaos.
- Key authors: Beggs, Plenz, Shew
- Relevance: Core to HIRM phase transition mechanism

### Consciousness Theories
IIT, GNWT, AST, HOT, and empirical consciousness research.
- Key authors: Tononi, Dehaene, Graziano, Koch
- Relevance: Competing theories to compare/integrate

### Mathematical Frameworks
Information theory, topology, category theory applications.
- Relevance: Mathematical foundations for HIRM

### Experimental Methods
Measurement protocols, datasets, validation approaches.
- Relevance: Empirical testing of HIRM predictions

---

## QUERY THE DATABASE

To explore papers:

```python
import sqlite3
conn = sqlite3.connect(r'D:\HIRM\System\data\hirm.db')

# All papers in a domain
cursor.execute("SELECT title, authors, year FROM papers WHERE domain='brain_criticality'")

# High-importance papers
cursor.execute("SELECT title, authors FROM papers WHERE importance >= 7")

# Search by keyword
cursor.execute("SELECT title FROM papers WHERE key_findings LIKE '%phase transition%'")
```

---

## INTEGRATION STATUS

Papers should progress through:
1. **unread** → Initial state
2. **read** → Content reviewed
3. **integrated** → Connected to HIRM framework
4. **cited** → Used in publications

Current: All 71 papers at 'read' status, awaiting integration tagging.

---

## UPDATE PROTOCOL

When adding new papers:
1. Insert into database using `populate_papers.py`
2. Regenerate this index
3. Tag with appropriate domain
4. Update integration status as work progresses
