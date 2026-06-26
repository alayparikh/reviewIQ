import sqlite3
import json
from datetime import datetime

DB_PATH = 'reviewsense.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create reports table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reports (
        id TEXT PRIMARY KEY,
        business_name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        summary_json TEXT
    )
    ''')
    
    # Create reviews table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_id TEXT,
        source TEXT, -- 'self' or 'competitor'
        business_name TEXT,
        rating INTEGER,
        text TEXT,
        sentiment_score REAL,
        topics TEXT,
        suggested_reply TEXT,
        timestamp TEXT,
        FOREIGN KEY (report_id) REFERENCES reports (id)
    )
    ''')
    
    conn.commit()
    conn.close()

def save_report(report_id, business_name, summary_json, reviews):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO reports (id, business_name, summary_json) VALUES (?, ?, ?)',
        (report_id, business_name, json.dumps(summary_json))
    )
    
    for review in reviews:
        cursor.execute('''
        INSERT INTO reviews (report_id, source, business_name, rating, text, sentiment_score, topics, suggested_reply, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            report_id,
            review.get('source'),
            review.get('business_name'),
            review.get('rating'),
            review.get('text'),
            review.get('sentiment_score'),
            json.dumps(review.get('topics')),
            review.get('suggested_reply'),
            review.get('timestamp')
        ))
    
    conn.commit()
    conn.close()

def get_report(report_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    report = cursor.execute('SELECT * FROM reports WHERE id = ?', (report_id,)).fetchone()
    if not report:
        conn.close()
        return None
    
    reviews = cursor.execute('SELECT * FROM reviews WHERE report_id = ?', (report_id,)).fetchall()
    
    report_dict = dict(report)
    report_dict['summary'] = json.loads(report_dict['summary_json'])
    report_dict['reviews'] = [dict(r) for r in reviews]
    for r in report_dict['reviews']:
        r['topics'] = json.loads(r['topics'])
        
    conn.close()
    return report_dict

if __name__ == '__main__':
    init_db()
    print("Database initialized.")
