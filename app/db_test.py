# test_supabase.py
import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv()
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DBNAME = os.getenv("DBNAME")
DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

print(DATABASE_URL)
try:
    # Connect to Supabase
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    # Test query
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()
    print("Connection successful! Current time:", result)

    cursor.close()
    conn.close()

except Exception as e:
    print("Failed to connect:", e)
