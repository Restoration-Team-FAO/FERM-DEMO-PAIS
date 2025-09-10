import json, os
from app.mapper import apply_mapping

def test_apply_mapping_hn():
    base = os.path.dirname(__file__)
    mapping = json.load(open(os.path.join(base, "..", "config", "mapping.HN.json")))
    row = {
        "id": "HND-001",
        "titulo": "Proyecto Demo",
        "pais": "HN",
        "anio_inicio": "2021",
        "anio_finalizacion": "2024",
        "area_total": "33.2",
        "geom": '{"type":"Point","coordinates":[-88.0,15.5]}',
        "departamento": "Cortés",
        "municipio": "SPS",
        "nombre_sitio": "Río Cacao"
    }
    out = apply_mapping(row, mapping)
    assert out["external_id"] == "HND-001"
    assert out["title"] == "Proyecto Demo"
    assert out["country_code"] == "HN"
    assert out["year_start"] == 2021
    assert out["year_end"] == 2024
    assert abs(out["area_total"] - 33.2) < 1e-6
    assert out["geometry"]["type"] == "Point"
    assert out["admin"]["department"] == "Cortés"
