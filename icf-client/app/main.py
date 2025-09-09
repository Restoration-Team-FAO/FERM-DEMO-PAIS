import os, json, psycopg2, requests
from dotenv import load_dotenv

load_dotenv()

PG_CONN = {
    "dbname": os.getenv("PGDATABASE"),
    "user": os.getenv("PGUSER"),
    "password": os.getenv("PGPASSWORD"),
    "host": os.getenv("PGHOST"),
    "port": os.getenv("PGPORT", 5432)
}
API_BASE = os.getenv("FERM_API_BASE")
API_KEY  = os.getenv("FERM_API_KEY")

def headers():
    h = {"Content-Type": "application/json"}
    if API_KEY:
        h["x-api-key"] = API_KEY
    return h

def fetch_projects():
    conn = psycopg2.connect(**PG_CONN)
    cur = conn.cursor()
    cur.execute("""
      SELECT id, nombre_proyecto, area_ha, tipo_actividad,
             ST_AsGeoJSON(geometry) as geom
      FROM restauracion_proyectos
      LIMIT 5;
    """)
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

def map_to_ferm(row):
    return {
        "external_id": row[0],
        "title": row[1],
        "area_ha": float(row[2]) if row[2] is not None else None,
        "activity_type": row[3],
        "geometry": json.loads(row[4]) if row[4] else None,
        "country_code": os.getenv("COUNTRY_CODE", "HN")
    }

def push_to_ferm(payload):
    r = requests.post(f"{API_BASE}/projects", headers=headers(), json=payload, timeout=20)
    print(f"POST /projects {r.status_code} {r.text[:200]}")
    return r.ok

def main():
    print(f"🌱 PG → {PG_CONN['host']} | API → {API_BASE}")
    rows = fetch_projects()
    for row in rows:
        payload = map_to_ferm(row)
        push_to_ferm(payload)

if __name__ == "__main__":
    main()
