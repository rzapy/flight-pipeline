import pandas as pd # type: ignore
from dotenv import load_dotenv # type: ignore
import os
import sqlalchemy as sql # type: ignore

load_dotenv()

DB_URL = os.getenv('DB_URL')

conn = sql.create_engine(DB_URL)

df = pd.read_sql_table("airplanes", conn)

for column in df.columns.values:
    if df[column].dtype == object:
        df[column] = df[column].str.strip()
        df[column] = df[column].replace('', 'UNKNOWN')
        df[column] = df[column].fillna('UNKNOWN')