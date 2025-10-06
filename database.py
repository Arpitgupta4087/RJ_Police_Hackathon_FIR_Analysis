import os
import psycopg2
import json
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except psycopg2.OperationalError as e:
        raise Exception(f"Could not connect to the database: {e}")

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS fir_cases (
            id SERIAL PRIMARY KEY,
            filename VARCHAR(255) NOT NULL,
            pdf_data BYTEA NOT NULL,
            summary TEXT,
            predicted_ipc JSONB,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def save_fir_data(filename, pdf_bytes, summary, ipc_predictions):
    conn = get_db_connection()
    cur = conn.cursor()
    ipc_json = json.dumps(ipc_predictions)
    cur.execute(
        "INSERT INTO fir_cases (filename, pdf_data, summary, predicted_ipc) VALUES (%s, %s, %s, %s)",
        (filename, pdf_bytes, summary, ipc_json)
    )
    conn.commit()
    cur.close()
    conn.close()
