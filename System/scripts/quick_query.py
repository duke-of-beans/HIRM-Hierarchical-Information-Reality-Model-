import sqlite3
conn = sqlite3.connect(r'D:\HIRM\System\data\hirm.db')
c = conn.cursor()

print("=== DOMAIN DISTRIBUTION ===")
for r in c.execute('SELECT domain, COUNT(*) FROM papers GROUP BY domain ORDER BY 2 DESC').fetchall():
    print(f"  {r[0]}: {r[1]} papers")

print("\n=== PREDICTIONS STATUS ===")
for r in c.execute('SELECT prediction_id, status, statement FROM predictions').fetchall():
    print(f"  {r[0]} [{r[1]}]: {r[2][:60]}...")

print("\n=== TABLES IN DATABASE ===")
for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall():
    print(f"  {r[0]}")

conn.close()
