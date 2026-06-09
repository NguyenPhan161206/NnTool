from pydantic import BaseModel


class UploadResponse(BaseModel):
    file_id: str
    filename: str
    columns: list[str]
    rows: int
    preview: list[dict]


class AnalyzeRequest(BaseModel):
    question: str
    file_id: str


class AnalyzeResponse(BaseModel):
    stats: dict
    charts: list[dict]
    report: str


class CreateProjectRequest(BaseModel):
    name: str
    description: str = ""


class ProjectResponse(BaseModel):
    project_id: str
    name: str
    description: str
    tables: list[dict]
    table_count: int


class ProjectAnalyzeRequest(BaseModel):
    question: str


class ProjectAnalyzeResponse(BaseModel):
    project_id: str
    tables_context: list[dict]
    report: str
