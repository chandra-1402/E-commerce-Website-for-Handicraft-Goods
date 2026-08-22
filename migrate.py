import sqlite3
try:
    conn = sqlite3.connect('database/database.db')
    c = conn.cursor()
    c.execute("ALTER TABLE users ADD COLUMN store_description TEXT")
    c.execute("ALTER TABLE users ADD COLUMN store_logo VARCHAR(255)")
    c.execute("ALTER TABLE users ADD COLUMN rating FLOAT DEFAULT 0.0")
    conn.commit()
    print("Migration successful")
except Exception as e:
    print(e)
finally:
    if conn: conn.close()
