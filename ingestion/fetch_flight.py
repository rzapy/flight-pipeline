import requests
import os
from dotenv import load_dotenv # type: ignore
import psycopg2 # type: ignore
from datetime import datetime

load_dotenv()

API_URL = os.getenv('API_URL')
DB_URL = os.getenv('DB_URL')

FIELD_MAP = {
    'icao24':          0,
    'callsign':        1,
    'origin_country':  2,
    'time_position':   3,
    'last_contact':    4,
    'longitude':       5,
    'latitude':        6,
    'baro_altitude':   7,
    'on_ground':       8,
    'velocity':        9,
    'true_track':      10,
    'vertical_rate':   11,
    'geo_altitude':    13,
    'squawk':          14,
    'spi':             15,
    'position_source': 16
}

columns     = list(FIELD_MAP.keys()) + ['fetched_at']
columns_str = ', '.join(columns)
placeholders = ', '.join(['%s'] * len(columns))

insert_query = f'INSERT INTO airplanes ({columns_str}) VALUES ({placeholders})'

conn = psycopg2.connect(DB_URL)
cur  = conn.cursor()

r    = requests.get(API_URL)
data = r.json()['states']

for row in data:
    values = [row[pos] for pos in FIELD_MAP.values()]
    values.append(datetime.now())
    cur.execute(insert_query, values)

conn.commit()
cur.close()
conn.close()