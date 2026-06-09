import uuid
import json
import pandas as pd
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.config import settings
from app.core.registry import register_tool
from .schemas import (
    UploadResponse,
    AnalyzeRequest,
    AnalyzeResponse,
    CreateProjectRequest,
    ProjectResponse,
    ProjectAnalyzeRequest,
    ProjectAnalyzeResponse,
)
from .analyst_tools.csv_reader import load_csv
from .analyst_tools.statistics import get_statistics
from .project_manager import project_manager, Project
from .agent.analyst import create_project_agent

router = APIRouter(prefix="/api/tools/data-analytics")


@register_tool(
    name="data-analytics",
    description="Phan tich du lieu CSV voi thong ke, bieu do, va bao cao LLM",
    icon="i-heroicons-chart-bar",
    router=router,
)
def data_analytics_tool():
    pass


@router.post("/upload", response_model=UploadResponse)
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only .csv files are accepted")

    max_upload_bytes = settings.max_upload_mb * 1024 * 1024

    content = await file.read()
    if len(content) > max_upload_bytes:
        raise HTTPException(status_code=400, detail=f"File too large, max {settings.max_upload_mb}MB")

    file_id = str(uuid.uuid4())
    upload_dir = settings.upload_path
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / f"{file_id}.csv"
    file_path.write_bytes(content)

    df = load_csv(str(file_path))
    stats = get_statistics(df)

    return UploadResponse(
        file_id=file_id,
        filename=file.filename,
        columns=list(df.columns),
        rows=len(df),
        preview=df.head(5).to_dict(orient="records"),
    )


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(req: AnalyzeRequest):
    file_path = settings.upload_path / f"{req.file_id}.csv"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    df = load_csv(str(file_path))
    stats = get_statistics(df)

    project = Project(name="adhoc", description="Single-file analysis")
    project.add_table("data.csv", df)

    try:
        agent = create_project_agent(project)
        result = agent.invoke({"input": req.question})
        messages = result.get("messages", [])
        if messages:
            report = messages[-1].content
        else:
            report = result.get("structured_response", "No output from agent")
    except Exception as e:
        report = f"Agent error: {str(e)}"

    return AnalyzeResponse(
        stats=stats,
        charts=[],
        report=report,
    )


@router.post("/project/create", response_model=dict)
async def create_project(req: CreateProjectRequest):
    project = project_manager.create_project(req.name, req.description)
    return {
        "project_id": project.project_id,
        "name": project.name,
        "description": project.description,
    }


@router.get("/projects")
async def list_projects():
    return project_manager.list_projects()


@router.post("/project/{project_id}/upload", response_model=dict)
async def upload_to_project(project_id: str, file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only .csv files are accepted")

    project = project_manager.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    max_upload_bytes = settings.max_upload_mb * 1024 * 1024

    content = await file.read()
    if len(content) > max_upload_bytes:
        raise HTTPException(status_code=400, detail=f"File too large, max {settings.max_upload_mb}MB")

    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    df = load_csv(tmp_path)
    Path(tmp_path).unlink(missing_ok=True)

    project.add_table(file.filename, df)

    return {
        "filename": file.filename,
        "columns": list(df.columns),
        "rows": len(df),
        "preview": df.head(5).to_dict(orient="records"),
    }


@router.get("/project/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str):
    project = project_manager.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    tables = []
    for name in project.get_table_names():
        df = project.get_table(name)
        tables.append(
            {
                "name": name,
                "columns": list(df.columns) if df is not None else [],
                "rows": len(df) if df is not None else 0,
            }
        )
    return ProjectResponse(
        project_id=project.project_id,
        name=project.name,
        description=project.description,
        tables=tables,
        table_count=len(tables),
    )


@router.delete("/project/{project_id}")
async def delete_project(project_id: str):
    project = project_manager.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project_manager.delete_project(project_id)
    return {"status": "deleted"}


@router.delete("/project/{project_id}/table/{table_name}")
async def delete_table(project_id: str, table_name: str):
    project = project_manager.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project.remove_table(table_name)
    return {"status": "deleted"}


@router.post("/project/{project_id}/analyze", response_model=ProjectAnalyzeResponse)
async def analyze_project(project_id: str, req: ProjectAnalyzeRequest):
    project = project_manager.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    tables_context = []
    for name in project.get_table_names():
        df = project.get_table(name)
        if df is not None:
            tables_context.append(
                {
                    "name": name,
                    "columns": list(df.columns),
                    "rows": len(df),
                    "preview": df.head(3).to_dict(orient="records"),
                }
            )

    try:
        agent = create_project_agent(project)
        result = agent.invoke({"input": req.question})
        messages = result.get("messages", [])
        if messages:
            report = messages[-1].content
        else:
            report = result.get("structured_response", "No output from agent")
    except Exception as e:
        report = f"Agent error: {str(e)}"

    return ProjectAnalyzeResponse(
        project_id=project_id,
        tables_context=tables_context,
        report=report,
    )
