#!/usr/bin/env python3
"""
Parse HIRM literature corpus and populate database
"""
import sqlite3
import re
import json

db_path = r'D:\HIRM\System\data\hirm.db'
corpus_path = r'D:\HIRM\Corpus\Reviews\Consciousness_Literature_Corpus_193_Papers.md'

def parse_corpus(filepath):
    """Parse markdown corpus file into paper entries"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    papers = []
    current_domain = None
    
    # Domain mapping
    domain_map = {
        'STRANGE LOOPS': 'self_reference',
        'SELF-REFERENCE': 'self_reference',
        'QUANTUM BIOLOGY': 'quantum_biology',
        'BRAIN CRITICALITY': 'brain_criticality',
        'CRITICAL PHENOMENA': 'brain_criticality',
        'CONSCIOUSNESS': 'consciousness_theories',
        'PHENOMENAL': 'consciousness_theories',
        'INFORMATION': 'information_theory',
        'MATHEMATICAL': 'mathematical',
        'EXPERIMENTAL': 'experimental_methods',
        'MEASUREMENT': 'experimental_methods',
    }
    
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Check for domain headers
        if line.startswith('## ') and any(d in line.upper() for d in domain_map.keys()):
            for key, val in domain_map.items():
                if key in line.upper():
                    current_domain = val
                    break
        
        # Check for paper entry (bold author/year pattern)
        if line.startswith('**') and '(' in line and ')' in line:
            # Parse author and year
            match = re.match(r'\*\*(.+?)\s*\((\d{4})\)\*\*', line)
            if match:
                authors = match.group(1).strip()
                year = int(match.group(2))
                
                # Get title (after dash)
                title_match = re.search(r'\*\*\s*[-–]\s*\*(.+?)\*', line)
                title = title_match.group(1) if title_match else ''
                
                # Get journal from next line
                journal = ''
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if not next_line.startswith('**') and not next_line.startswith('#'):
                        journal = next_line.split('.')[0] if '.' in next_line else next_line
                
                # Get description (following lines until next entry)
                description_lines = []
                j = i + 2
                while j < len(lines):
                    desc_line = lines[j].strip()
                    if desc_line.startswith('**') or desc_line.startswith('##') or desc_line.startswith('###'):
                        break
                    if desc_line:
                        description_lines.append(desc_line)
                    j += 1
                
                description = ' '.join(description_lines)
                
                # Extract citations if mentioned
                citations_match = re.search(r'Citations[:\s]*[~>]*([\d,]+)', description)
                citations = citations_match.group(1).replace(',', '') if citations_match else None
                
                papers.append({
                    'title': title,
                    'authors': authors,
                    'year': year,
                    'journal': journal,
                    'domain': current_domain or 'unclassified',
                    'key_findings': description[:500] if description else '',
                    'importance': 7 if citations and int(citations) > 1000 else 5
                })
        
        i += 1
    
    return papers

def insert_papers(papers):
    """Insert papers into database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    inserted = 0
    for p in papers:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO papers 
                (title, authors, year, journal, domain, key_findings, importance, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'read')
            ''', (p['title'], p['authors'], p['year'], p['journal'], 
                  p['domain'], p['key_findings'], p['importance']))
            if cursor.rowcount > 0:
                inserted += 1
        except Exception as e:
            print(f"Error inserting {p['title'][:50]}: {e}")
    
    conn.commit()
    
    # Get total count
    cursor.execute('SELECT COUNT(*) FROM papers')
    total = cursor.fetchone()[0]
    
    conn.close()
    return inserted, total

if __name__ == '__main__':
    print("Parsing corpus...")
    papers = parse_corpus(corpus_path)
    print(f"Found {len(papers)} papers")
    
    print("Inserting into database...")
    inserted, total = insert_papers(papers)
    print(f"Inserted {inserted} new papers")
    print(f"Total papers in database: {total}")
