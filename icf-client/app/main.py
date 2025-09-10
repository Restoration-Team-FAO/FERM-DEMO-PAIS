import os, json, psycopg2, requests
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from .mapper import apply_mapping
from .ferm_schema import FermProject

load_dotenv()

PG_CONN = {
    "dbname": os.getenv("PGDATABASE"),
    "user": os.getenv("PGUSER"),
    "password": os.getenv("PGPASSWORD"),
    "host": os.getenv("PGHOST"),
    "port": int(os.getenv("PGPORT", 5432)),
}
API_BASE = os.getenv("FERM_API_BASE")
API_KEY  = os.getenv("FERM_API_KEY")
CONFIG_NAME = os.getenv("CONFIG_NAME", "HN")

BASE_DIR = os.path.dirname(__file__)
MAPPING_PATH = os.path.join(BASE_DIR, "config", f"mapping.{CONFIG_NAME}.json")
SQL_PATH     = os.path.join(BASE_DIR, "config", f"sql.{CONFIG_NAME}.sql")

def headers():
    h = {"Content-Type": "application/json", "Accept": "application/json"}
    if API_KEY:
        h["x-api-key"] = API_KEY
    return h

def fetch_rows():
    with open(SQL_PATH, "r", encoding="utf-8") as f:
        sql = f.read()
    conn = psycopg2.connect(**PG_CONN)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

def load_mapping():
    with open(MAPPING_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def validate(payload: dict) -> FermProject:
    return FermProject(**payload)  # Pydantic v2

def post_one(payload: dict):
    url = f"{API_BASE}/projects"
    r = requests.post(url, headers=headers(), data=json.dumps(payload), timeout=30)
    print(f"[POST] {url} -> {r.status_code} {r.text[:200]}")
    return r.ok

def main():
    print(f"🌱 PG → {PG_CONN['host']}:{PG_CONN['port']} | DB={PG_CONN['dbname']} | API → {API_BASE} | CONFIG={CONFIG_NAME}")
    mapping = load_mapping()
    rows = fetch_rows()
    print(f"Encontrados {len(rows)} registros. Mapeando y enviando...")
    ok = 0
    for row in rows:
        payload_raw = apply_mapping(row, mapping)
        try:
            payload = validate(payload_raw).model_dump()  # v2: dict limpio
        except Exception as e:
            print("❌ Error de validación:", e, "payload:", payload_raw)
            continue
        if post_one(payload):
            ok += 1
    print(f"✅ Envío terminado. Éxitos: {ok}/{len(rows)}")

if __name__ == "__main__":
    main()
