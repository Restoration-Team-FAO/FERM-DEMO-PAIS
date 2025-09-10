from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any

class FermProject(BaseModel):
    model_config = ConfigDict(extra="allow")  # aceptamos campos adicionales

    # Mínimos indispensables:
    external_id: str
    title: str
    country_code: str
    geometry: Dict[str, Any]

    # Recomendados/útiles:
    year_start: Optional[int] = None
    year_end: Optional[int] = None
    restoration_status: Optional[str] = None
    restoration_type: Optional[str] = None

    area_committed: Optional[float] = None
    area_total: Optional[float] = None
    area_unit: Optional[str] = None

    # Objetos anidados
    admin: Optional[Dict[str, Any]] = None
