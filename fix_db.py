import sqlite3

conn = sqlite3.connect('database/database.db')
c = conn.cursor()

columns = [
    "first_name VARCHAR(100)",
    "last_name VARCHAR(100)",
    "age INTEGER",
    "gender VARCHAR(20)",
    "phone VARCHAR(20)",
    "address_line_1 VARCHAR(255)",
    "address_line_2 VARCHAR(255)",
    "city VARCHAR(100)",
    "state VARCHAR(100)",
    "pincode VARCHAR(20)"
]

for col in columns:
    try:
        c.execute(f"ALTER TABLE users ADD COLUMN {col};")
        print(f"Added {col}")
    except sqlite3.OperationalError as e:
        print(f"Skipped {col} - {e}")

conn.commit()
conn.close()
