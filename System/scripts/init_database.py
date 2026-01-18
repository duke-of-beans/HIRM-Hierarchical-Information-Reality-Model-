#!/usr/bin/env python3
"""Initialize HIRM SQLite Database"""
import sqlite3
import os

db_path = r'D:\HIRM\System\data\hirm.db'
schema_path = r'D:\HIRM\System\data\database_schema.sql'

# Read schema
with open(schema_path, 'r') as f:
    schema = f.read()

# Create database and execute schema
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.executescript(schema)
conn.commit()

# Verify tables created
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Database created successfully!')
print('Tables:', [t[0] for t in tables])

# Verify constants inserted
cursor.execute('SELECT symbol, value FROM constants')
constants = cursor.fetchall()
print('Constants:', constants)

conn.close()
print(f'Database size: {os.path.getsize(db_path)} bytes')
