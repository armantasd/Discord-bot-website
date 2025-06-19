import sqlite3, json
DB_NAME = "Database.db"

def initiate_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            token TEXT,
            responces TEXT,
            commands TEXT,
            config TEXT
        )
''')
        
#template configuration
responces = {
    "Hello /bot/" : "Hi",
    "How are you my bot?" : "Good",
    "Thanks" : "Thanks, you too"
}
commands = {
    "Hello" : "Say hello bot",
    "Random_num" : "Tell me a random num",
    "Date" : "When is it?"
}
config = {
    "command_prefix" : "!",
    "user_replace" : "/user/",
    "bot_replace" : "/bot/"
}

def Login(username, password):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        return c.fetchone()
    
def Check_taken(username):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        return c.fetchone()

def Add_user(username, password):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, token, responces, commands, config) VALUES (?, ?, ?, ?, ?, ?)", (username, password, "No token", json.dumps(responces), json.dumps(commands), json.dumps(config)))
        conn.commit()

def Update_db(username, address, value):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute(f"UPDATE users SET {address} = ? WHERE username = ?", (value, username))
        conn.commit()

def Fetch_data(username, data_index):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute(f"SELECT * FROM users WHERE username = ?", (username,))
        values = c.fetchall()
        return values[0][data_index]