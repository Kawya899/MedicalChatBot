import sqlite3

def init_db():
    conn = sqlite3.connect('medical_chatbot.db')
    with open('schema.sql', 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.close()
    print("Database initialized from schema.sql.")

if __name__ == '__main__':
    init_db()
