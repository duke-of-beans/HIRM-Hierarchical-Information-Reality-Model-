import sqlite3

# Connect to database
conn = sqlite3.connect(r'D:\HIRM\System\data\hirm.db')
cursor = conn.cursor()

# Missing papers to add (from quality gate findings)
papers = [
    ('Werner 2012', 'Werner', 2012, 'Consciousness related to neural complexity (to be enriched)', 'consciousness_theories', 'medium'),
    ('Denis et al. 2024', 'Denis', 2024, 'Recent consciousness research (to be enriched)', 'consciousness_theories', 'high'),
    ('Zanardi et al. 2007', 'Zanardi', 2007, 'Quantum information geometry foundations', 'mathematical', 'high'),
    ('Shew et al. 2011', 'Shew', 2011, 'Neural avalanches and criticality', 'brain_criticality', 'high'),
    ('Tegmark 2000', 'Tegmark', 2000, 'Quantum consciousness decoherence arguments', 'quantum_biology', 'high'),
    ('Hagan et al. 2024', 'Hagan', 2024, 'Quantum effects in biological systems', 'quantum_biology', 'medium'),
    ('Babcock et al. 2024', 'Babcock', 2024, 'Neural dynamics research', 'brain_criticality', 'medium'),
    ('Jae et al. 2024', 'Jae', 2024, 'Consciousness measurement advances', 'consciousness_theories', 'medium'),
    ('Liu et al. 2024', 'Liu', 2024, 'Neural information processing', 'consciousness_theories', 'medium'),
    ('Kurian et al. 2024', 'Kurian', 2024, 'Quantum biology advances', 'quantum_biology', 'medium'),
    ('Newman et al. 2024', 'Newman', 2024, 'Consciousness research advances', 'consciousness_theories', 'medium'),
    ('Comolatti et al. 2019', 'Comolatti', 2019, 'Perturbational complexity index research', 'consciousness_theories', 'high'),
    ('Lee et al. 2022', 'Lee', 2022, 'Neural criticality and consciousness', 'brain_criticality', 'medium'),
    ('Yang et al. 2022', 'Yang', 2022, 'Consciousness dynamics research', 'consciousness_theories', 'medium'),
    ('Wang et al. 2023', 'Wang', 2023, 'Neural information integration', 'consciousness_theories', 'medium'),
    ('Palva et al. 2016', 'Palva', 2016, 'Neural oscillations and consciousness', 'brain_criticality', 'high'),
    ('Yang et al. 2024', 'Yang', 2024, 'Recent consciousness advances', 'consciousness_theories', 'medium'),
    ('Anthropic 2024', 'Anthropic', 2024, 'AI and consciousness considerations', 'consciousness_theories', 'low'),
]

# Insert papers
inserted = 0
skipped = []
for title, author, year, desc, domain, importance in papers:
    try:
        cursor.execute('''
            INSERT INTO papers (title, authors, year, journal, domain, topics, importance, status, key_findings)
            VALUES (?, ?, ?, 'To be enriched', ?, ?, ?, 'unread', ?)
        ''', (title, author, year, domain, domain, importance, desc))
        inserted += 1
        print(f'Added: {title}')
    except sqlite3.IntegrityError:
        skipped.append(title)
        print(f'Skipped (exists): {title}')

conn.commit()

# Get new total
cursor.execute("SELECT COUNT(*) FROM papers")
total = cursor.fetchone()[0]

print(f'\n=== SUMMARY ===')
print(f'Inserted: {inserted} new papers')
print(f'Skipped: {len(skipped)}')
print(f'Total papers in database: {total}')

conn.close()
