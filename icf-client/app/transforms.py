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

TRANSFORMS = {
    "to_int": to_int,
    "to_float": to_float,
    "to_geojson": to_geojson,
}
