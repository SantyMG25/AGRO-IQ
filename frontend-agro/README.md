# Agro IQ — Frontend

Este repositorio contiene la interfaz frontend de Agro IQ, una plataforma de simulación y análisis agroclimático basada en una arquitectura multi-agente y hexagonal. La aplicación muestra paneles analíticos, recomendaciones generadas por agentes y controles para ejecutar simulaciones basadas en parámetros (riego, desfase de siembra, subsidios).

---

**Español (ES)**

Resumen
- Interfaz web construida con Next.js y TypeScript.
- Consume el backend de Agro IQ para lanzar simulaciones, obtener métricas y series temporales.
- Visualizaciones: métricas de resiliencia, seguridad alimentaria, proyección de rendimiento, tarjetas de acción y gráficos de tendencia.

Arquitectura
- Frontend: Next.js (app router), componentes React en `components/`, adaptadores HTTP en `adapters/outbound/`.
- Backend (ver `../backend-agro`): motor FastAPI con orquestador multi-agente, adaptadores para LLM y Microsoft IQ, y repositorio SQLite.

Endpoints principales (backend)
- `POST /api/analyze` — Ejecuta una simulación y devuelve `SimulationResult`.
- `GET /api/history` — Resumen del historial de simulaciones.
- `GET /api/analytics/dashboard` — Métricas agregadas del dashboard.
- `GET /api/analytics/trends` — Series temporales y tendencias.
- `GET /api/analytics/history` — Historial detallado de simulaciones.
- `POST /api/analytics/compare` — Compara escenarios por IDs.
- `GET /api/analytics/roi` — Análisis de ROI por inversión en riego.
- `GET /api/analytics/regional/{region}` — Resumen regional.
- `GET /health` — Health check del servicio.

Ejemplo rápido (curl)

```bash
curl -X POST http://127.0.0.1:8000/api/analyze \
	-H 'Content-Type: application/json' \
	-d '{"region":"Global Andean Region","crop_type":"Subsistence Corn","user_description":"Preventive monitoring","variables":{"irrigation_investment":40,"planting_window_shift":1,"fertilizer_subsidy":50}}'
```

Instalación (Frontend)

```bash
cd frontend-agro
npm install
```

Desarrollo (Frontend)

```bash
npm run dev
```

La app por defecto intenta conectar al backend en `http://127.0.0.1:8000`. Para cambiarlo, crea `.env.local` en `frontend-agro` con:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Instalación y ejecución (Backend) — resumen

Recomendado: Python 3.10+ y un entorno virtual.

```bash
cd backend-agro
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt   # si existe, o instala: fastapi uvicorn sqlalchemy openai
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Variables de entorno importantes (Backend)
- `OPENAI_API_KEY` — clave para el adaptador OpenAI (si se usa).
- `AZURE_OPENAI_DEPLOYMENT` — nombre de despliegue/modelo.
- `MICROSOFT_IQ_PROVIDER` — `mock` o `real`.
- `FOUNDRY_IQ_ENDPOINT`, `FABRIC_IQ_ENDPOINT` — endpoints opcionales.

Base de datos
- El backend usa SQLite por defecto en `backend-agro/agro_iq.db` (configurado en el adaptador de `adapters/outbound/database.py`).

Contribuir

1. Crea una rama descriptiva.
2. Envía un Pull Request con la explicación de cambios.



---

**English (EN)**

Overview
- Frontend for Agro IQ built with Next.js and TypeScript.
- Connects to the Agro IQ backend to run simulations, fetch analytics and trend data.
- UI includes resilience and food security metrics, projected yields, action cards, and trend charts.

Architecture
- Frontend: Next.js (app router), React components in `components/`, HTTP adapters in `adapters/outbound/`.
- Backend (see `../backend-agro`): FastAPI multi-agent orchestrator, LLM and Microsoft IQ adapters, SQLite repository.

Main backend endpoints
- `POST /api/analyze` — Run a simulation, returns `SimulationResult`.
- `GET /api/history` — Simulation history summary.
- `GET /api/analytics/dashboard` — Aggregated dashboard metrics.
- `GET /api/analytics/trends` — Time series trends.
- `GET /api/analytics/history` — Detailed simulation history.
- `POST /api/analytics/compare` — Compare scenarios by IDs.
- `GET /api/analytics/roi` — ROI analysis for irrigation investment.
- `GET /api/analytics/regional/{region}` — Regional summary.
- `GET /health` — Health check.

Quick curl example

```bash
curl -X POST http://127.0.0.1:8000/api/analyze \
	-H 'Content-Type: application/json' \
	-d '{"region":"Global Andean Region","crop_type":"Subsistence Corn","user_description":"Preventive monitoring","variables":{"irrigation_investment":40,"planting_window_shift":1,"fertilizer_subsidy":50}}'
```

Frontend setup

```bash
cd frontend-agro
npm install
npm run dev
```

Change backend base URL via `.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Backend quick start

```bash
cd backend-agro
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt   # or install fastapi uvicorn sqlalchemy openai
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Environment variables (backend)
- `OPENAI_API_KEY`, `AZURE_OPENAI_DEPLOYMENT`, `MICROSOFT_IQ_PROVIDER`, `FOUNDRY_IQ_ENDPOINT`, `FABRIC_IQ_ENDPOINT`.

Database
- The backend uses SQLite by default (see `adapters/outbound/database.py`).

Contributing

1. Create a descriptive branch.
2. Open a Pull Request with details of changes.

---

Archivo: [frontend-agro/README.md](frontend-agro/README.md)
