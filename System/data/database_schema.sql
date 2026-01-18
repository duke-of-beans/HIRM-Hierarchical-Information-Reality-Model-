-- ============================================================================
-- HIRM RESEARCH DATABASE SCHEMA v1.0
-- Created: 2025-12-21
-- Purpose: Self-learning research operating system for consciousness research
-- ============================================================================

-- PAPERS TABLE: Track all corpus papers
CREATE TABLE IF NOT EXISTS papers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Paper identification
    title TEXT NOT NULL,
    authors TEXT NOT NULL,           -- JSON array
    year INTEGER,
    journal TEXT,
    doi TEXT UNIQUE,
    arxiv_id TEXT,
    
    -- Classification
    domain TEXT,                     -- 'brain_criticality', 'quantum_measurement', etc.
    topics TEXT,                     -- JSON array of keywords
    importance INTEGER DEFAULT 5,    -- 1-10 scale
    
    -- Location
    file_path TEXT,                  -- Path in corpus relative to HIRM root
    
    -- Integration status
    status TEXT DEFAULT 'unread',    -- 'unread', 'read', 'integrated', 'cited'
    integration_notes TEXT,
    key_findings TEXT,               -- JSON array
    hirm_relevance TEXT,             -- How it relates to HIRM
    
    -- Citations
    times_cited_by_us INTEGER DEFAULT 0,
    cited_in_papers TEXT             -- JSON array of our paper IDs
);

-- CONSTANTS TABLE: Locked scientific values (source of truth)
CREATE TABLE IF NOT EXISTS constants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    symbol TEXT UNIQUE NOT NULL,     -- 'C_critical', 'nu', 'gamma'
    name TEXT NOT NULL,              -- 'Critical Threshold'
    value TEXT NOT NULL,             -- '8.3 ± 0.6'
    units TEXT,                      -- 'bits'
    
    derivation_source TEXT,          -- Which document derives this
    derivation_method TEXT,          -- 'holographic_bound', 'RG_fixed_point'
    confidence TEXT DEFAULT 'provisional', -- 'established', 'provisional', 'speculative'
    
    last_verified TIMESTAMP,
    verification_source TEXT
);


-- EQUATIONS TABLE: All mathematical expressions
CREATE TABLE IF NOT EXISTS equations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    equation_id TEXT UNIQUE NOT NULL,  -- 'C_formula', 'Phi_definition'
    latex TEXT NOT NULL,               -- LaTeX representation
    description TEXT,
    
    variables TEXT,                    -- JSON: {symbol: {name, units, meaning}}
    dimensional_check TEXT,            -- Verification of units
    
    source_document TEXT,
    derivation_document TEXT,
    
    status TEXT DEFAULT 'verified'     -- 'verified', 'provisional', 'deprecated'
);

-- PREDICTIONS TABLE: Falsifiable claims (core of HIRM)
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    prediction_id TEXT UNIQUE NOT NULL,
    statement TEXT NOT NULL,
    
    -- Specificity
    quantitative_claim TEXT,          -- e.g., "C_critical = 8.3 ± 0.6 bits"
    measurement_protocol TEXT,
    distinguishing_from TEXT,         -- Which theories this differs from
    
    -- Testing status
    status TEXT DEFAULT 'untested',   -- 'untested', 'supported', 'falsified', 'inconclusive'
    evidence_for TEXT,                -- JSON: papers supporting
    evidence_against TEXT,            -- JSON: papers contradicting
    
    -- Dates
    proposed_date TIMESTAMP,
    last_tested TIMESTAMP,
    test_result TEXT
);

-- TERMINOLOGY TABLE: Canonical naming
CREATE TABLE IF NOT EXISTS terminology (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    canonical_term TEXT UNIQUE NOT NULL,
    definition TEXT NOT NULL,
    
    legacy_terms TEXT,                 -- JSON array of old names
    related_terms TEXT,                -- JSON array
    
    domain TEXT,                       -- 'physics', 'neuroscience', etc.
    first_used_in TEXT
);

-- CORRECTIONS TABLE: Self-healing registry
CREATE TABLE IF NOT EXISTS corrections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    correction_type TEXT NOT NULL,     -- 'equation', 'constant', 'claim', 'terminology'
    original_text TEXT,
    corrected_text TEXT,
    
    source_session TEXT,
    reason TEXT,
    
    recurrence_count INTEGER DEFAULT 1,
    added_to_protocol BOOLEAN DEFAULT 0,
    
    severity TEXT DEFAULT 'medium'     -- 'low', 'medium', 'high', 'critical'
);


-- SESSION_LOGS TABLE: Research session tracking
CREATE TABLE IF NOT EXISTS session_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    session_id TEXT,
    session_type TEXT,                 -- 'literature', 'theory', 'empirical', 'writing'
    
    work_completed TEXT,               -- JSON array
    findings TEXT,                     -- JSON array
    papers_integrated TEXT,            -- JSON array
    predictions_tested TEXT,           -- JSON array
    
    errors_encountered TEXT,
    corrections_made TEXT,
    suggested_improvements TEXT,
    follow_up_tasks TEXT
);

-- DOCUMENTS TABLE: Track all generated documents
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    file_path TEXT UNIQUE NOT NULL,
    document_type TEXT,                -- 'theory', 'review', 'protocol', 'manuscript'
    title TEXT,
    
    -- Versioning
    version TEXT,
    supersedes TEXT,                   -- Path to previous version
    
    -- Quality
    quality_score REAL,
    validation_passed BOOLEAN,
    
    -- Content tracking
    equations_used TEXT,               -- JSON array of equation IDs
    constants_used TEXT,               -- JSON array of constant IDs
    papers_cited TEXT,                 -- JSON array of paper IDs
    
    -- Status
    status TEXT DEFAULT 'draft'        -- 'draft', 'review', 'final', 'archived'
);

-- ============================================================================
-- INDICES FOR FAST QUERYING
-- ============================================================================
CREATE INDEX IF NOT EXISTS idx_papers_domain ON papers(domain);
CREATE INDEX IF NOT EXISTS idx_papers_status ON papers(status);
CREATE INDEX IF NOT EXISTS idx_papers_year ON papers(year);
CREATE INDEX IF NOT EXISTS idx_constants_symbol ON constants(symbol);
CREATE INDEX IF NOT EXISTS idx_predictions_status ON predictions(status);
CREATE INDEX IF NOT EXISTS idx_corrections_type ON corrections(correction_type);
CREATE INDEX IF NOT EXISTS idx_documents_type ON documents(document_type);
CREATE INDEX IF NOT EXISTS idx_documents_status ON documents(status);

-- ============================================================================
-- INSERT CORE HIRM CONSTANTS
-- ============================================================================
INSERT OR IGNORE INTO constants (symbol, name, value, units, derivation_method, confidence) VALUES
    ('C_critical', 'Critical Consciousness Threshold', '8.3 ± 0.6', 'bits', 'holographic_bound + RG_fixed_point', 'established'),
    ('nu', 'Correlation Length Exponent', '~0.63', 'dimensionless', 'Ising universality class', 'established'),
    ('gamma', 'Susceptibility Exponent', '~1.24', 'dimensionless', 'Ising universality class', 'established'),
    ('beta', 'Order Parameter Exponent', '~0.33', 'dimensionless', 'Ising universality class', 'established'),
    ('tau', 'Avalanche Duration Exponent', '~2.0', 'dimensionless', 'critical brain dynamics', 'provisional'),
    ('alpha', 'Avalanche Size Exponent', '~1.5', 'dimensionless', 'critical brain dynamics', 'provisional');

-- ============================================================================
-- INSERT CORE PREDICTIONS
-- ============================================================================
INSERT OR IGNORE INTO predictions (prediction_id, statement, quantitative_claim, status) VALUES
    ('P1_threshold', 'Consciousness emerges when C(t) exceeds critical threshold', 'C_critical = 8.3 ± 0.6 bits', 'untested'),
    ('P2_sleep', 'Sleep states show C(t) below threshold', 'C_sleep < 8 bits', 'untested'),
    ('P3_anesthesia', 'Anesthesia systematically reduces C(t)', 'C drops before behavioral LOC', 'untested'),
    ('P4_avalanche', 'Conscious brain shows critical avalanche statistics', 'tau ≈ 2.0, alpha ≈ 1.5', 'provisional'),
    ('P5_DOC', 'DOC patients stratify by C(t) value', 'Coma < UWS < MCS < Conscious', 'untested');
