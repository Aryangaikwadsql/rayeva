import sqlite3
con = sqlite3.connect('raveya.db')
print('Tables:')
for row in con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"):
    print(row[0])
con.close()
