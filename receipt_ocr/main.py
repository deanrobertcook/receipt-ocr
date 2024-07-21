import sqlite3

def initialize_db():
    conn = sqlite3.connect('receipts.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store TEXT NOT NULL,
            date TEXT NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            amount INTEGER NOT NULL,
        )
    ''')
    conn.commit()
    conn.close()

def add_item(name, quantity, price, date, store):
    conn = sqlite3.connect('receipts.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO items (name, quantity, price, date, store)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, quantity, price, date, store))
    conn.commit()
    conn.close()

def main():
    initialize_db()
    print("Hello")

