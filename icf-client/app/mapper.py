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

    # DIRECT: copias 1:1 (pueden ser nested con 'a.b.c')
    for src, dst in mapping.get("direct", {}).items():
        if src in row and row[src] not in (None, ""):
            set_nested(out, dst, row[src])

    # DERIVED: con funciones de 'transforms'
    for src, rule in mapping.get("derived", {}).items():
        fn_name = rule.get("fn")
        dst = rule.get("to")
        if fn_name and dst:
            fn = TRANSFORMS.get(fn_name)
            if fn:
                val = fn(row.get(src))
                if val not in (None, ""):
                    set_nested(out, dst, val)

    # COMPUTED: valores que nacen sólo de funciones (sin src)
    for rule in mapping.get("computed", []):
        fn_name = rule.get("fn")
        dst = rule.get("to")
        arg = rule.get("arg")
        if fn_name and dst:
            fn = TRANSFORMS.get(fn_name)
            if fn:
                val = fn(arg)
                if val not in (None, ""):
                    set_nested(out, dst, val)

    # FALLBACKS: toma el primero que exista (incluye @ENV.*)
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

    # 🔧 Normalizaciones finales para cumplir el esquema FERM
    if out.get('external_id') is not None and not isinstance(out['external_id'], str):
        out['external_id'] = str(out['external_id'])

    return out

