#!/usr/bin/env python3
"""Add terminology and equations to HIRM database"""
import sqlite3

db_path = r'D:\HIRM\System\data\hirm.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Add core terminology
terminology = [
    ('HIRM', 'Hierarchical Information-Reality Model - framework for consciousness emergence', '["Ouroboros Observer", "OO Theory"]', 'physics'),
    ('C(t)', 'Consciousness measure - total information processing capacity at time t', '[]', 'measurement'),
    ('Phi', 'Integrated information - irreducible information integration', '[]', 'measurement'),
    ('R', 'Self-reference coefficient - degree to which system models itself', '[]', 'measurement'),
    ('D', 'Dimensional complexity - effective dimensionality of state space', '[]', 'measurement'),
    ('C_critical', 'Critical threshold - minimum C(t) for consciousness (~8.3 bits)', '[]', 'constant'),
    ('Phase Transition', 'Qualitative change in system behavior at critical point', '[]', 'physics'),
    ('Criticality', 'State where system exhibits scale-free dynamics', '[]', 'physics'),
    ('DOC', 'Disorders of Consciousness - clinical conditions with impaired awareness', '[]', 'clinical'),
    ('PCI', 'Perturbational Complexity Index - TMS-EEG measure', '[]', 'measurement'),
    ('IIT', 'Integrated Information Theory - Tononi consciousness theory', '[]', 'theory'),
    ('GNWT', 'Global Neuronal Workspace Theory - Dehaene theory', '[]', 'theory'),
    ('FEP', 'Free Energy Principle - Friston framework', '[]', 'theory'),
]

for term, defn, legacy, domain in terminology:
    cursor.execute('''
        INSERT OR IGNORE INTO terminology (canonical_term, definition, legacy_terms, domain)
        VALUES (?, ?, ?, ?)
    ''', (term, defn, legacy, domain))

# Add core equations
equations = [
    ('C_formula', 'C(t) = Phi(t) * R(t) * D(t)', 'Core consciousness measure', 'verified'),
    ('C_threshold', 'C(t) >= C_critical', 'Consciousness emergence condition', 'verified'),
    ('Phi_def', 'Phi = min[I(whole) - I(parts)]', 'Integrated information', 'verified'),
    ('D_def', 'D = (sum(lambda))^2 / sum(lambda^2)', 'Participation ratio', 'verified'),
]

for eq_id, latex, desc, status in equations:
    cursor.execute('''
        INSERT OR IGNORE INTO equations (equation_id, latex, description, status)
        VALUES (?, ?, ?, ?)
    ''', (eq_id, latex, desc, status))

conn.commit()

# Report
cursor.execute('SELECT COUNT(*) FROM terminology')
print(f'Terminology: {cursor.fetchone()[0]}')
cursor.execute('SELECT COUNT(*) FROM equations')
print(f'Equations: {cursor.fetchone()[0]}')
cursor.execute('SELECT COUNT(*) FROM papers')
print(f'Papers: {cursor.fetchone()[0]}')
cursor.execute('SELECT COUNT(*) FROM predictions')
print(f'Predictions: {cursor.fetchone()[0]}')
cursor.execute('SELECT COUNT(*) FROM constants')
print(f'Constants: {cursor.fetchone()[0]}')

conn.close()
print('Database population complete!')
