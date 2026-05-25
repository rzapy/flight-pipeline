import os
from dotenv import load_dotenv # type: ignore
import psycopg2 # type: ignore
from pathlib import Path

load_dotenv()

DB_URL = os.getenv('DB_URL')
SQL_FILE_DIR = Path(__file__).parent.resolve()
FILE_NAME = 'create_tables.sql'
FULL_PATH = SQL_FILE_DIR / FILE_NAME


conn = psycopg2.connect(DB_URL)

cur = conn.cursor()

with open(FULL_PATH, "r", encoding="utf-8") as f:
    script = f.read()

cur.execute(script)
cur.execute('''select exists
            (select 1 from pg_tables where schemaname = 'public' and tablename = 'airplanes'); ''')
cur.close()
conn.commit()
conn.close()