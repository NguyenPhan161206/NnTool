from fastapi import APIRouter
from app.core.registry import register_tool

router = APIRouter(prefix="/api/tools/template")


@register_tool(
    name="template",
    description="Template tool — copy me to add a new tool",
    icon="i-heroicons-cube",
    router=router,
)
def template_function():
    pass


@router.get("/hello")
async def hello():
    return {"message": "Hello from template tool!"}
