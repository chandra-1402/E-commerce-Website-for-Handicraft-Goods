import sqlite3

conn = sqlite3.connect('database/database.db')
c = conn.cursor()
try:
    c.execute("ALTER TABLE users ADD COLUMN first_name VARCHAR(100);")
    c.execute("ALTER TABLE users ADD COLUMN last_name VARCHAR(100);")
    c.execute("ALTER TABLE users ADD COLUMN age INTEGER;")
    c.execute("ALTER TABLE users ADD COLUMN gender VARCHAR(20);")
    c.execute("ALTER TABLE users ADD COLUMN phone VARCHAR(20);")
    c.execute("ALTER TABLE users ADD COLUMN address_line_1 VARCHAR(255);")
    c.execute("ALTER TABLE users ADD COLUMN address_line_2 VARCHAR(255);")
    c.execute("ALTER TABLE users ADD COLUMN city VARCHAR(100);")
    c.execute("ALTER TABLE users ADD COLUMN state VARCHAR(100);")
    c.execute("ALTER TABLE users ADD COLUMN pincode VARCHAR(20);")
except sqlite3.OperationalError as e:
    print(f"Columns might already exist: {e}")
conn.commit()
conn.close()

from app import create_app
from models import db
app = create_app()
with app.app_context():
    db.create_all()
    print("User table migrated successfully.")
