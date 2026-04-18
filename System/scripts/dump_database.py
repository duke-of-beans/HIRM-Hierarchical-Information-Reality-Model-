import sqlite3

conn = sqlite3.connect(r'D:\HIRM\System\data\hirm.db')
cursor = conn.cursor()

print('=== ALL PAPERS BY DOMAIN ===')
cursor.execute('SELECT domain, COUNT(*) FROM papers GROUP BY domain ORDER BY COUNT(*) DESC')
for row in cursor.fetchall():
    print(f'{row[0]}: {row[1]} papers')

print('\n=== HIGH IMPORTANCE PAPERS ===')
cursor.execute("SELECT title, authors, year, domain, key_findings FROM papers WHERE importance='high' ORDER BY year DESC")
for row in cursor.fetchall():
    print(f'\n{row[0]} ({row[1]}, {row[2]})')
    print(f'  Domain: {row[3]}')
    if row[4]:
        print(f'  Findings: {row[4][:200]}...')

print('\n=== PREDICTIONS ===')
cursor.execute('SELECT prediction_id, statement, status FROM predictions')
for row in cursor.fetchall():
    print(f'{row[0]}: {row[1]} [{row[2]}]')

print('\n=== CONSTANTS ===')
cursor.execute('SELECT symbol, name, value, confidence FROM constants')
for row in cursor.fetchall():
    print(f'{row[0]} = {row[2]} ({row[1]}) [{row[3]}]')

print('\n=== TERMINOLOGY ===')
cursor.execute('SELECT canonical_term, definition FROM terminology')
for row in cursor.fetchall():
    print(f'{row[0]}: {row[1][:100] if row[1] else "No definition"}...')

conn.close()
