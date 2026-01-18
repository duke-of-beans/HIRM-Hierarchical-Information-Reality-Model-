# HIRM RESEARCH INDEX
## Complete Directory Map
## Last Updated: 2025-12-21

---

## 📁 DIRECTORY STRUCTURE

```
D:\HIRM\
│
├── 📁 _Archive\                    # Versioned/retired content
│   ├── Contaminated\               # Known-error files quarantined
│   ├── Superseded\                 # Replaced by newer versions
│   └── Version_History\            # Named snapshots
│
├── 📁 _Backups\                    # Timestamped full backups
│
├── 📁 System\                      # Infrastructure
│   ├── data\
│   │   ├── hirm.db                 # ⭐ MASTER DATABASE
│   │   └── database_schema.sql     # Schema definition
│   ├── config\                     # System configuration
│   ├── scripts\                    # Automation tools
│   └── mcp\                        # MCP server files
│
├── 📁 Protocols\                   # Research standards
│   └── HIRM_RESEARCH_PROTOCOLS_v2.md  # ⭐ MASTER PROTOCOL
│
├── 📁 Master_Data\                 # ⭐ SINGLE SOURCE OF TRUTH
│   ├── Constants\
│   │   └── locked_constants.md     # C_critical, exponents
│   ├── Framework\
│   │   ├── hirm_core_claims.md     # Falsifiable predictions
│   │   └── component_definitions.md # Φ, R, D definitions
│   ├── Terminology\
│   │   └── terminology_reference.md # Canonical terms
│   └── Corrections\
│       └── corrections_registry.md  # Self-healing registry
│
├── 📁 Corpus\                      # Research literature
│   ├── Papers\
│   │   ├── Brain_Criticality\      # ~50 papers
│   │   ├── Quantum_Measurement\    # ~30 papers
│   │   ├── Consciousness_Theories\ # ~45 papers
│   │   ├── Mathematical\           # ~40 papers
│   │   ├── Quantum_Biology\        # ~25 papers
│   │   └── Experimental_Methods\   # ~50 papers
│   ├── Reviews\                    # Synthesis documents
│   └── Index\                      # Auto-generated catalogs
│
├── 📁 Theory\                      # Theoretical development
│   ├── Core\                       # Central HIRM theory
│   ├── Components\                 # Deep dives on Φ, R, D
│   ├── Extensions\                 # FEP, quantum, temporal
│   └── Mathematical_Tools\         # Bifurcation, RG, info geometry
│
├── 📁 Empirical\                   # Data & validation
│   ├── Datasets\                   # Sleep-EDF, anesthesia
│   ├── Protocols\                  # Experimental methods
│   ├── Results\                    # Analysis outputs
│   └── Validation\                 # Prediction testing
│
├── 📁 Code\                        # Computational tools
│   ├── Core\                       # Core algorithms
│   ├── Tools\                      # Utilities
│   ├── Tests\                      # Unit tests
│   ├── Demos\                      # Examples
│   ├── Notebooks\                  # Jupyter notebooks
│   └── Visualizations\             # Plotting
│
├── 📁 Publications\                # Publication pipeline
│   ├── Manuscripts\
│   │   ├── Paper_1_Brain_Criticality\
│   │   ├── Paper_2_Quantum_Classical\
│   │   └── Paper_3_Temporal_Persistence\
│   ├── Popular\                    # Accessible versions
│   └── Supplementary\              # Supporting materials
│
├── 📁 Figures\                     # All images
│   ├── Publication\                # Publication-quality
│   ├── Working\                    # In-progress
│   └── Archive\                    # Old versions
│
├── 📁 Documentation\               # Human navigation
│   ├── START_HERE.md               # ⭐ NEW SESSION START
│   └── INDEX.md                    # This file
│
├── 📁 Logs\                        # Session tracking
│   └── SESSION_LOGS.md
│
├── 📁 Temp\                        # Working space
│
└── 📁 External\                    # Non-HIRM explorations
    ├── UAP_Analysis\
    └── Schauberger\
```

---

## 🔍 QUICK LOOKUP

### By Task

| If you want to... | Go to... |
|-------------------|----------|
| Start a new session | `Documentation/START_HERE.md` |
| Check a constant value | `Master_Data/Constants/locked_constants.md` |
| Find a paper | `Corpus/Index/` or database |
| Understand the core equation | `Master_Data/Framework/component_definitions.md` |
| See falsifiable predictions | `Master_Data/Framework/hirm_core_claims.md` |
| Review protocols | `Protocols/HIRM_RESEARCH_PROTOCOLS_v2.md` |
| Run C(t) calculation | `Code/Core/consciousness_measure.py` |
| Work on Paper 1 | `Publications/Manuscripts/Paper_1_Brain_Criticality/` |
| Log an error | `Master_Data/Corrections/corrections_registry.md` |

### By File Type

| Extension | Location | Purpose |
|-----------|----------|---------|
| `.md` | Throughout | Documentation, theory |
| `.py` | `Code/` | Python implementations |
| `.db` | `System/data/` | SQLite database |
| `.sql` | `System/data/` | Database schema |
| `.png` | `Figures/` | Visualizations |
| `.ipynb` | `Code/Notebooks/` | Jupyter notebooks |

---

## 🗄️ DATABASE TABLES

| Table | Purpose | Key Fields |
|-------|---------|------------|
| papers | Literature corpus | title, authors, domain, status |
| constants | Locked values | symbol, value, units |
| equations | Math expressions | equation_id, latex, variables |
| predictions | Falsifiable claims | prediction_id, status |
| terminology | Canonical terms | canonical_term, legacy_terms |
| corrections | Error tracking | original, corrected, severity |
| session_logs | Research tracking | work_completed, findings |
| documents | Generated docs | file_path, quality_score |

---

## ⚠️ CRITICAL FILES

Files that should NEVER be modified without extreme care:

1. `System/data/hirm.db` - Master database
2. `Master_Data/Constants/locked_constants.md` - Source of truth
3. `Protocols/HIRM_RESEARCH_PROTOCOLS_v2.md` - Research standards
4. `Master_Data/Framework/hirm_core_claims.md` - Core predictions

**Any changes to these files must be logged in corrections registry.**
