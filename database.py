import sqlite3
import os

DB_NAME = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Prompts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            prompt TEXT NOT NULL
        )
    ''')
    
    # Check if empty and add sample prompts
    cursor.execute('SELECT COUNT(*) FROM prompts')
    if cursor.fetchone()[0] == 0:
        prompts = [
            ('Gratitude', 'What are three things you are grateful for today?'),
            ('Gratitude', 'Who is someone that made a positive impact on your life recently?'),
            ('Productivity', 'What is the one most important task you want to accomplish today?'),
            ('Productivity', 'How can you eliminate one distraction from your workspace?'),
            ('Self-Care', 'What is one thing you can do today to nourish your body?'),
            ('Self-Care', 'Describe a place where you feel completely at peace.'),
            ('Creativity', 'If you could start any creative project today, what would it be?'),
            ('Creativity', 'Write about a color and the emotions it evokes for you.')
        ]
        cursor.executemany('INSERT INTO prompts (category, prompt) VALUES (?, ?)', prompts)
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
