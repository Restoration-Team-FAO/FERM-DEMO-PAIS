from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from uuid import uuid4

app = FastAPI(title="FERM Mock API", version="0.1.0")

# Habilitar CORS (opcional, útil para pruebas desde navegador)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Project(BaseModel):
    # 👉 Esto permite aceptar campos extra sin fallar
    model_config = ConfigDict(extra='allow')

    external_id: Optional[str] = None
    title: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    area_ha: Optional[float] = None
    activity_type: Optional[str] = None
    status: Optional[str] = "en_ejecucion"
    geometry: Optional[dict] = None
    country_code: Optional[str] = None

DB = {}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/projects", status_code=status.HTTP_201_CREATED)
async def create_project(p: Project, request: Request):
    pid = f"mock-{uuid4().hex[:8]}"
    data = p.dict()
    data["id"] = pid
    DB[pid] = data
    print("📦 Proyecto recibido:", data)
    return {"id": pid, "status": "created"}

@app.post("/projects/bulk", status_code=status.HTTP_201_CREATED)
async def create_projects_bulk(projects: List[Project]):
    created = []
    for p in projects:
        pid = f"mock-{uuid4().hex[:8]}"
        data = p.dict()
        data["id"] = pid
        DB[pid] = data
        created.append({"id": pid, "status": "created"})
    print(f"📦 Bulk recibido: {len(created)} items")
    return {"items": created}

@app.get("/projects/{pid}")
def get_project(pid: str):
    return DB.get(pid, {"detail": "Not found"})
