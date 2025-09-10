from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict

class FermProject(BaseModel):
    # aceptamos campos adicionales que no estén listados
    model_config = ConfigDict(extra="allow")

    # mínimos indispensables
    external_id: str
    title: str
    country_code: str
    geometry: Dict[str, Any]

    # recomendados
    year_start: Optional[int] = None
    year_end: Optional[int] = None
    restoration_status: Optional[str] = None
    restoration_type: Optional[str] = None

    area_committed: Optional[float] = None
    area_total: Optional[float] = None
    area_unit: Optional[str] = None

    admin: Optional[Dict[str, Any]] = None
