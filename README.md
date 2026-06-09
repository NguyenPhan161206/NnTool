# NnTool

Hybrid-architecture Tool Hub: FastAPI backend + NuxtUI frontend + LangChain agent + Ollama LLM.

## Architecture

```
User (Browser)
    |
NuxtUI Frontend (port 3000)
    |  REST API (JSON)
FastAPI Backend (port 8000)
    |
LangChain Agent (ReAct loop)
    |
Tool Layer: csv_reader | statistics | charts | query_data
    |
Ollama / Qwen3 (LLM)
```

## Tech Stack

| Role | Technology |
|------|-----------|
| Language | Python 3.12+ |
| Data | Pandas, Plotly |
| Backend | FastAPI |
| Agent | LangChain (ReAct) |
| LLM | Ollama + Qwen3 |
| Frontend | Nuxt 3 + NuxtUI (Vue 3) |
| Charts | ECharts |
| Container | Docker |

## Quick Start

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# Swagger: http://localhost:8000/docs
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
# Browser: http://localhost:3000
```

### 3. Docker (full stack)

```bash
docker compose up --build
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

### 4. Ollama

```bash
ollama pull qwen3:1.7b
```

## Project Structure

```
tool-hub/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI app, CORS, routers
│   │   ├── config.py         # Settings (model, paths)
│   │   ├── core/
│   │   │   └── registry.py   # @register_tool() decorator
│   │   ├── tools/
│   │   │   ├── data_analytics/  # Tool #1
│   │   │   │   ├── router.py    # API endpoints
│   │   │   │   ├── schemas.py   # Pydantic models
│   │   │   │   ├── project_manager.py
│   │   │   │   ├── agent/
│   │   │   │   │   ├── analyst.py   # LangChain agent
│   │   │   │   │   └── prompts.py
│   │   │   │   └── analyst_tools/
│   │   │   │       ├── csv_reader.py
│   │   │   │       ├── statistics.py
│   │   │   │       ├── query_data.py
│   │   │   │       └── chart_generator.py
│   │   │   └── tool_template/  # Template for new tools
│   │   └── uploads/
│   ├── sample_data/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app.vue
│   ├── nuxt.config.ts
│   ├── layouts/default.vue     # Sidebar + main layout
│   ├── pages/
│   │   ├── index.vue           # Home: tool cards
│   │   └── tools/
│   │       └── data-analytics.vue
│   ├── components/
│   │   ├── hub/                # Shared hub components
│   │   └── data-analytics/     # Tool #1 components
│   ├── composables/useApi.ts
│   └── Dockerfile
├── ollama/
│   ├── Dockerfile
│   └── entrypoint.sh
├── docker-compose.yml
├── vercel.json
├── render.yaml
├── tool-hub-documentation.tex
└── tool-hub-documentation.pdf
```

## Adding a New Tool

1. Create `backend/app/tools/<tool_name>/router.py`
2. Use `@register_tool(name=..., description=...)` decorator
3. Add a Vue page at `frontend/pages/tools/<tool-name>.vue`

```python
@register_tool(name="translator", description="Translate text", icon="i-heroicons-language")
def translate_text(text: str) -> str:
    ...
```

## Deployment

- **Frontend**: Vercel (connect GitHub, set `API_BASE_URL` env)
- **Backend**: Render / Railway (connect GitHub, start: `uvicorn app.main:app --host 0.0.0.0 --port 8000`)
- **LLM**: Ollama runs locally or use OpenAI API as replacement

## License

MIT
