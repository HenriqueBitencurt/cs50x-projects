from cs50 import SQL

db = SQL("sqlite:///studysync.db")

db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        hash TEXT NOT NULL
    );
""")

db.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        subject TEXT NOT NULL,
        due_date TEXT,
        status TEXT DEFAULT 'pendente',
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
""")

db.execute("""
    CREATE TABLE IF NOT EXISTS exams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        subject TEXT NOT NULL,
        exam_date TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
""")

db.execute("""
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        subject TEXT NOT NULL,
        assessment_name TEXT NOT NULL,
        score REAL NOT NULL,
        max_score REAL NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
""")

print("Base de dados 'studysync.db' criada com sucesso e tabelas configuradas!")
