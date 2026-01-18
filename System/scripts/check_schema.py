import sqlite3
conn = sqlite3.connect(r'D:\HIRM\System\data\hirm.db')
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(session_logs)")
print("session_logs columns:")
for row in cursor.fetchall():
    print(f"  {row}")
conn.close()
