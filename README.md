# 🌱 FERM-DEMO-PAIS

Este repositorio contiene un paquete Docker **todo-en-uno** para demostrar la interoperabilidad entre bases de datos PostgreSQL/PostGIS de un país y el **API-FERM**.  
Incluye:

- **Postgres demo** con 2 proyectos de restauración.
- **Mock-FERM** (API simulada en FastAPI).
- **ICF-Client** (conector que extrae datos de Postgres y los envía al API).

---

## 🚀 Requisitos previos

En el servidor (Ubuntu 22.04 LTS):

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin
sudo usermod -aG docker $USER
newgrp docker
```

---

## 📁 Estructura

```
FERM-DEMO-PAIS/
├─ docker-compose.yml
├─ .env.example
├─ db/
│  └─ init.sql
├─ mock-ferm/
│  ├─ Dockerfile
│  ├─ requirements.txt
│  └─ app.py
└─ icf-client/
   ├─ Dockerfile
   └─ app/
      ├─ main.py
      ├─ requirements.txt
      └─ mapping.json
```

---

## 🔧 Configuración

1. Copiar el archivo `.env.example` → `.env`:

```bash
cp .env.example .env
nano .env
```

2. Editar las variables si es necesario:

```env
# Postgres del compose
PGHOST=postgres
PGDATABASE=icf_restauracion
PGUSER=icf_user
PGPASSWORD=secret
PGPORT=5432

# API destino (mock por ahora)
FERM_API_BASE=http://mock-ferm:8080
FERM_API_KEY=
COUNTRY_CODE=HN
```

---

## ▶️ Uso

### 1. Construir y levantar servicios

```bash
docker compose build
docker compose up -d
```

### 2. Ver estado de contenedores

```bash
docker compose ps
```

### 3. Ver logs del cliente (ICF-Client)

```bash
docker compose logs -f icf-client
```

Deberías ver:

```
🌱 PG → postgres | API → http://mock-ferm:8080
POST /projects 201 {"id":"mock-xxxx","status":"created"}
```

Y en los logs del mock:

```
📦 Proyecto recibido: { "title":"Proyecto Demo 1", ... }
```

---

## 📊 Endpoints disponibles

- **Mock-FERM**  
  - Salud: [http://localhost:8080/health](http://localhost:8080/health)  
  - Swagger: [http://localhost:8080/docs](http://localhost:8080/docs)  

- **Postgres demo**  
  - Usuario: `icf_user`  
  - Password: `secret`  
  - DB: `icf_restauracion`

---

## 🌍 Pasar a producción

Cuando el FERM real esté en línea:

1. Editar `.env` y cambiar:

```env
FERM_API_BASE=https://api-ferm-real.a.run.app
FERM_API_KEY=<tu_api_key_si_aplica>
```

2. Si se usa Postgres del ICF, poner credenciales reales en `.env`.

3. Levantar solo el cliente:

```bash
docker compose up -d --build icf-client
```

---

## 📜 Licencia

Uso institucional FAO/FERM – Demo de interoperabilidad.
