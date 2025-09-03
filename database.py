import sqlite3

DB_NAME = "game.db"

# --- Setup tables ---
def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id INTEGER,
        score INTEGER,
        FOREIGN KEY (player_id) REFERENCES players(id)
    )
    """)

    conn.commit()
    conn.close()


# --- CRUD functions ---
def create_player(name):
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO players (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def get_player_id(name):
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM players WHERE name = ?", (name,))
    result = cursor.fetchone()
    if result:
        conn.close()
        return result[0]
    create_player(name)
    conn.close()
    return get_player_id(name)

def update_score(name, score):
    player_id = get_player_id(name)
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO scores (player_id, score) VALUES (?, ?)", (player_id, score))
    conn.commit()
    conn.close()

def read_players():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT players.name, scores.score
        FROM scores
        JOIN players ON players.id = scores.player_id
        ORDER BY scores.score DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows
