import json

def to_int(v):
    try:
        return int(v) if v not in (None, "") else None
    except Exception:
        return None

def to_float(v):
    try:
        return float(v) if v not in (None, "") else None
    except Exception:
        return None

def to_str(v):
    return None if v in (None, "") else str(v)

def to_geojson(v):
    if v is None:
        return None
    if isinstance(v, (dict, list)):
        return v
    if isinstance(v, str) and v.strip():
        try:
            return json.loads(v)
        except Exception:
            return None
    return None

# Normaliza país a ISO-3166 alpha-2 (usa HN por defecto)
def country_alpha2(v, default=None):
    if v is None:
        return default or "HN"
    s = str(v).strip().lower()
    mapping = {
        "hn": "HN",
        "honduras": "HN",
        "iso 3166 honduras": "HN",
        "iso-3166 honduras": "HN",
        "iso3166 honduras": "HN",
    }
    return mapping.get(s, default or "HN")

TRANSFORMS = {
    "to_int": to_int,
    "to_float": to_float,
    "to_str": to_str,
    "to_geojson": to_geojson,
    "country_alpha2": country_alpha2,
}
