import sqlite3

conn = sqlite3.connect('database/database.db')
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS order_items;")
c.execute("DROP TABLE IF EXISTS orders;")
conn.commit()
conn.close()

from app import create_app
from models import db
app = create_app()
with app.app_context():
    db.create_all()
    print("Orders tables migrated successfully.")
