import os, json, psycopg2, requests, datetime
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
COUNTRY  = os.getenv("COUNTRY_CODE", "HN")

def headers():
    h = {"Content-Type": "application/json", "Accept":"application/json"}
    if API_KEY:
        h["x-api-key"] = API_KEY
    return h

def as_float(v):
    try:
        return float(v) if v is not None else None
    except:
        return None

def as_int(v):
    try:
        return int(v) if v not in (None, "") else None
    except:
        return None

def fetch_rows(limit=50):
    sql = """
    SELECT
      cod_proye,
      id,
      titulo,
      descripcion,
      zip_foto,
      sitio_web,
      anio_inicio,
      anio_finalizacion,
      estado_restauracion,
      tipo_resstauracion,
      objetivo,
      actividad_plantacion,
      sistema_plantacion,
      disenio_arreglo,
      opciones_foresteria,
      tenencia,
      ods,
      documento_iniciativa,
      nombre_responsable,
      informacion_contacto,
      palabras_clave,
      tipo_org,
      pais,
      departamento,
      municipio,
      area_comprometida,
      area_total,
      unidad,
      nombre_sitio,
      planes_restauracion,
      tipologia_ecosistemas,
      actividad,
      indicadores_aurora,
      ST_AsGeoJSON(geom) AS geom
    FROM pnr.ferm_query
    LIMIT %s;
    """
    conn = psycopg2.connect(**PG_CONN)
    cur  = conn.cursor()
    cur.execute(sql, (limit,))
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

def map_row_to_payload(row):
    (
      cod_proye, id_, titulo, descripcion, zip_foto, sitio_web,
      anio_inicio, anio_finalizacion, estado_restauracion, tipo_resstauracion,
      objetivo, actividad_plantacion, sistema_plantacion, disenio_arreglo,
      opciones_foresteria, tenencia, ods, documento_iniciativa,
      nombre_responsable, informacion_contacto, palabras_clave, tipo_org,
      pais, departamento, municipio, area_comprometida, area_total, unidad,
      nombre_sitio, planes_restauracion, tipologia_ecosistemas, actividad,
      indicadores_aurora, geom_json
    ) = row

    # Normalizaciones básicas
    year_start = as_int(anio_inicio)
    year_end   = as_int(anio_finalizacion)
    geometry   = json.loads(geom_json) if geom_json else None

    # Campo país preferimos el del registro; si viene vacío usamos COUNTRY_CODE del .env
    country_code = (pais or "").strip() or COUNTRY

    # Payload “FERM-like” (dejamos nombres claros + conservamos los originales)
    payload = {
        # Claves mínimas de proyecto
        "external_id": id_ or cod_proye,
        "title": titulo,
        "description": descripcion,
        "country_code": country_code,
        "geometry": geometry,

        # Metadatos de tiempo/estado
        "year_start": year_start,
        "year_end": year_end,
        "restoration_status": estado_restauracion,
        "restoration_type": tipo_resstauracion,  # ojo: en tu vista está escrito con doble 's'

        # Área: dejamos ambas si existen
        "area_committed": as_float(area_comprometida),
        "area_total": as_float(area_total),
        "area_unit": unidad,

        # Ubicación administrativa
        "admin": {
            "department": departamento,
            "municipality": municipio,
            "site_name": nombre_sitio,
        },

        # Diseño / técnicas
        "planting_activity": actividad_plantacion,
        "planting_system": sistema_plantacion,
        "design_layout": disenio_arreglo,
        "forestry_options": opciones_foresteria,

        # Gobernanza / otros
        "tenure": tenencia,
        "sdg": ods,
        "initiative_document": documento_iniciativa,
        "responsible_name": nombre_responsable,
        "contact_info": informacion_contacto,
        "keywords": palabras_clave,
        "org_type": tipo_org,
        "website": sitio_web,
        "photo_zip": zip_foto,
        "restoration_plans": planes_restauracion,
        "ecosystem_typology": tipologia_ecosistemas,
        "activity": actividad,
        "aurora_indicators": indicadores_aurora,

        # Fuente de datos (útil para trazabilidad)
        "source": {
            "schema": "pnr",
            "view": "ferm_query",
            "fetched_at": datetime.datetime.utcnow().isoformat() + "Z",
            "country_hint": COUNTRY
        }
    }
    return payload

def post_one(payload):
    url = f"{API_BASE}/projects"
    r = requests.post(url, headers=headers(), data=json.dumps(payload), timeout=30)
    print(f"[POST] {url} -> {r.status_code} {r.text[:200]}")
    return r.ok

def main():
    print(f"🌱 PG → {PG_CONN['host']}:{PG_CONN['port']} | DB={PG_CONN['dbname']} | API → {API_BASE}")
    rows = fetch_rows(limit=50)
    print(f"Encontrados {len(rows)} registros. Enviando...")
    ok = 0
    for row in rows:
        payload = map_row_to_payload(row)
        if post_one(payload):
            ok += 1
    print(f"✅ Envío terminado. Éxitos: {ok}/{len(rows)}")

if __name__ == "__main__":
    main()
