"""
Database module for storing prediction history
Uses SQLite for local data persistence
"""

import sqlite3
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from datetime import datetime
from contextlib import contextmanager

DATABASE_PATH = 'predictions_history.db'


@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_database():
    """Initialize the database and create tables if they don't exist"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Create predictions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                prediction TEXT NOT NULL,
                confidence REAL NOT NULL,
                message TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                ip_address TEXT,
                text_length INTEGER
            )
        ''')
        
        # Create index for faster queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON predictions(timestamp DESC)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_prediction 
            ON predictions(prediction)
        ''')
        
        conn.commit()
        print("✓ Database initialized successfully")


def save_prediction(text, prediction, confidence, message, ip_address=None):
    """
    Save a prediction to the database
    
    Args:
        text: The input text analyzed
        prediction: FAKE or REAL
        confidence: Confidence percentage
        message: Analysis message
        ip_address: Optional IP address of requester
    
    Returns:
        int: ID of the inserted record
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Use local time instead of UTC
        local_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
            INSERT INTO predictions (text, prediction, confidence, message, timestamp, ip_address, text_length)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (text, prediction, confidence, message, local_timestamp, ip_address, len(text)))
        conn.commit()
        return cursor.lastrowid


def get_all_predictions(limit=100):
    """
    Get all predictions from database
    
    Args:
        limit: Maximum number of records to return
    
    Returns:
        list: List of prediction records
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, text, prediction, confidence, message, timestamp, text_length
            FROM predictions
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        return cursor.fetchall()


def get_statistics():
    """
    Get statistics about predictions
    
    Returns:
        dict: Statistics including counts and averages
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Total predictions
        cursor.execute('SELECT COUNT(*) as total FROM predictions')
        total = cursor.fetchone()['total']
        
        # Fake count
        cursor.execute("SELECT COUNT(*) as count FROM predictions WHERE prediction = 'FAKE'")
        fake_count = cursor.fetchone()['count']
        
        # Real count
        cursor.execute("SELECT COUNT(*) as count FROM predictions WHERE prediction = 'REAL'")
        real_count = cursor.fetchone()['count']
        
        # Average confidence
        cursor.execute('SELECT AVG(confidence) as avg_confidence FROM predictions')
        avg_confidence = cursor.fetchone()['avg_confidence'] or 0
        
        # Average text length
        cursor.execute('SELECT AVG(text_length) as avg_length FROM predictions')
        avg_length = cursor.fetchone()['avg_length'] or 0
        
        return {
            'total_predictions': total,
            'fake_count': fake_count,
            'real_count': real_count,
            'average_confidence': round(avg_confidence, 2),
            'average_text_length': round(avg_length, 2)
        }


def get_recent_predictions(limit=10):
    """Get most recent predictions"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, 
                   SUBSTR(text, 1, 100) as text_preview,
                   prediction, 
                   confidence, 
                   timestamp
            FROM predictions
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        return cursor.fetchall()


def get_prediction_by_id(prediction_id):
    """Get a single prediction by ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, text, prediction, confidence, message, timestamp, text_length
            FROM predictions
            WHERE id = ?
        ''', (prediction_id,))
        return cursor.fetchone()


def delete_all_predictions():
    """Delete all prediction records (admin function)"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM predictions')
        conn.commit()
        return cursor.rowcount


def export_to_csv():
    """Export all predictions to CSV format"""
    import csv
    from io import StringIO
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, text, prediction, confidence, message, timestamp, text_length
            FROM predictions
            ORDER BY timestamp DESC
        ''')
        
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', 'Text', 'Prediction', 'Confidence', 'Message', 'Timestamp', 'Text Length'])
        
        for row in cursor.fetchall():
            writer.writerow(row)
        
        return output.getvalue()


if __name__ == '__main__':
    # Initialize database when run directly
    init_database()
    print("Database setup complete!")
    
    # Show current statistics
    stats = get_statistics()
    print(f"\nCurrent Statistics:")
    print(f"Total Predictions: {stats['total_predictions']}")
    print(f"Fake News Detected: {stats['fake_count']}")
    print(f"Real News Detected: {stats['real_count']}")
