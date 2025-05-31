import sqlite3
import pandas as pd

DB_PATH = "results.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            real_data_path TEXT,
            gen_params TEXT,
            method1_result INTEGER,
            method2_result INTEGER,
            method3_result INTEGER
        )
    """)
    conn.commit()
    conn.close()

def save_experiment(date, real_data_path, gen_params, method1, method2, method3):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO results (date, real_data_path, gen_params, method1_result, method2_result, method3_result)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, real_data_path, gen_params, method1, method2, method3))
    conn.commit()
    conn.close()

def load_results():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM results", conn)
    conn.close()
    return df

def load_experiment_by_id(exp_id):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM results WHERE id = ?", conn, params=(exp_id,))
    conn.close()
    return df
