import sqlite3

conn = sqlite3.connect('raveya.db')
cursor = conn.cursor()
cursor.execute("UPDATE proposals SET status = 'PENDING' WHERE LOWER(status) = 'pending'")
affected = cursor.rowcount
conn.commit()
print(f"Updated {affected} proposals to PENDING status.")
conn.close()
