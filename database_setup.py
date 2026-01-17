import csv
import sqlite3

conn = sqlite3.connect("draft.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Rankings (
        id INTEGER PRIMARY KEY,
        mode TEXT,
        map_name TEXT,
        brawler_name TEXT,
        pick TEXT,
        description TEXT
    )
''')

with open('brawl.csv', 'r') as file:
    reader = csv.DictReader(file)
    next(reader)

    for row in reader:
        cursor.execute('''
            INSERT INTO Rankings (mode, map_name, brawler_name, pick)
            VALUES (?, ?, ?, ?)
    ''', (row['mode'], row['map_name'], row['brawler_name'], row['pick']))


conn.commit()
conn.close()