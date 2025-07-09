import sqlite3

DB_PATH = "users.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            first_name TEXT,
            username TEXT,
            age INTEGER,
            gender TEXT,
            city TEXT,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER,
            receiver_id INTEGER,
            text TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(sender_id) REFERENCES users(user_id),
            FOREIGN KEY(receiver_id) REFERENCES users(user_id)
        )
    """)
    conn.commit()
    conn.close()

def add_user_to_db(user_id, first_name, username, age=None, gender=None, city=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""INSERT OR IGNORE INTO users 
        (user_id, first_name, username, age, gender, city) 
        VALUES (?, ?, ?, ?, ?, ?)""",
              (user_id, first_name, username, age, gender, city))
    c.execute("""UPDATE users SET age=?, gender=?, city=? WHERE user_id=?""",
              (age, gender, city, user_id))
    conn.commit()
    conn.close()

def add_message(sender_id, receiver_id, text):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""INSERT INTO messages (sender_id, receiver_id, text) 
                 VALUES (?, ?, ?)""",
              (sender_id, receiver_id, text))
    conn.commit()
    conn.close()

# Run init on import
init_db()
