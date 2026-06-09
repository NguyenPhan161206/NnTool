import uuid
import pandas as pd
from typing import Dict


class Project:
    def __init__(self, name: str, description: str = ""):
        self.project_id: str = str(uuid.uuid4())
        self.name: str = name
        self.description: str = description
        self.tables: Dict[str, pd.DataFrame] = {}
        self.table_order: list[str] = []

    def add_table(self, name: str, df: pd.DataFrame):
        if name in self.tables:
            base, ext = name.rsplit(".", 1) if "." in name else (name, "")
            idx = 1
            while name in self.tables:
                name = f"{base}_{idx}.{ext}" if ext else f"{base}_{idx}"
                idx += 1
        self.tables[name] = df
        if name not in self.table_order:
            self.table_order.append(name)

    def remove_table(self, name: str):
        self.tables.pop(name, None)
        if name in self.table_order:
            self.table_order.remove(name)

    def get_table_names(self) -> list[str]:
        return list(self.table_order)

    def get_table(self, name: str) -> pd.DataFrame | None:
        return self.tables.get(name)

    def get_schema_summary(self) -> str:
        lines = []
        for name in self.table_order:
            df = self.tables[name]
            cols = []
            for col in df.columns:
                dtype = df[col].dtype
                sample = df[col].dropna().head(3).tolist()
                sample_str = ", ".join(str(s) for s in sample) if sample else "empty"
                cols.append(f"    - {col} ({dtype}): [{sample_str}]")
            col_list = ", ".join(str(c) for c in df.columns)
            lines.append(f"- {name} ({len(df)} rows, {len(df.columns)} cols): {col_list}")
            lines.extend(cols)
        return "\n".join(lines)

    def get_context_for_agent(self) -> str:
        parts = [f"Project: {self.name}", f"Description: {self.description}", ""]
        if not self.tables:
            parts.append("No tables loaded yet.")
            return "\n".join(parts)
        parts.append(f"Tables ({len(self.tables)}):")
        for name in self.table_order:
            df = self.tables[name]
            preview = df.head(3).to_string(index=False)
            parts.append(f"\n  Table: {name}")
            parts.append(f"  Rows: {len(df)}, Columns: {len(df.columns)}")
            parts.append(f"  Preview:\n{preview}")
        return "\n".join(parts)


class ProjectManager:
    _instance = None
    _projects: Dict[str, Project] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def create_project(self, name: str, description: str = "") -> Project:
        project = Project(name, description)
        self._projects[project.project_id] = project
        return project

    def get_project(self, project_id: str) -> Project | None:
        return self._projects.get(project_id)

    def delete_project(self, project_id: str):
        self._projects.pop(project_id, None)

    def list_projects(self) -> list[dict]:
        return [
            {
                "project_id": p.project_id,
                "name": p.name,
                "description": p.description,
                "table_count": len(p.tables),
            }
            for p in self._projects.values()
        ]


project_manager = ProjectManager()
