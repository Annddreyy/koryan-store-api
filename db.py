import sqlite3

def get_connection():
    conn = sqlite3.connect(r'./koreyan-store.db')
    return conn