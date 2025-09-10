import os
from .transforms import TRANSFORMS

def get_env_value(name: str, default=None):
    return os.getenv(name, default)

def set_nested(d: dict, dotted_path: str, value):
    """Escribe d['a']['b']=value para 'a.b'. Ignora None."""
    if value is None:
        return
    parts = dotted_path.split(".")
    cur = d
    for p in parts[:-1]:
        cur = cur.setdefault(p, {})
    cur[parts[-1]] = value

def apply_mapping(row: dict, mapping: dict) -> dict:
    out = {}

    # 1) direct (renombre 1:1 y/o campos anidados)
    for src, dst in mapping.get("direct", {}).items():
        if src in row:
            set_nested(out, dst, row[src])

    # 2) transforms (aplica funciones registradas)
    for src, spec in mapping.get("transforms", {}).items():
        to = spec["to"]
        fn = TRANSFORMS[spec["fn"]]
        val = row.get(src, None)
        set_nested(out, to, fn(val))

    # 3) fallbacks (primer valor disponible; soporta @ENV.X)
    for dst, sources in mapping.get("fallbacks", {}).items():
        value = None
        for src in sources:
            if isinstance(src, str) and src.startswith("@ENV."):
                envname = src.replace("@ENV.", "", 1)
                value = get_env_value(envname)
            else:
                value = row.get(src)
            if value not in (None, ""):
                break
        if value not in (None, ""):
            set_nested(out, dst, value)

    return out
