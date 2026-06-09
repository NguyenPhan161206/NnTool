from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.core.registry import get_all_tools, get_tool_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    import app.tools
    yield


app = FastAPI(title="Tool Hub", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/tools")
async def list_tools():
    return get_all_tools()


from app.tools.data_analytics import router as da_router
app.include_router(da_router)
