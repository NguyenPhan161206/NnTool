from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.tools import Tool
from app.config import settings
from app.tools.data_analytics.project_manager import Project
from app.tools.data_analytics.analyst_tools.statistics import get_statistics as _get_statistics
from app.tools.data_analytics.analyst_tools.query_data import query_data as _query_data
from app.tools.data_analytics.analyst_tools.chart_generator import generate_chart as _generate_chart
from app.tools.data_analytics.agent.prompts import SYSTEM_PROMPT
import pandas as pd
import json


def create_project_agent(project: Project):
    llm = ChatOllama(
        model=settings.model_name,
        temperature=0.3,
        base_url=settings.ollama_host,
    )

    project_context = project.get_context_for_agent()
    full_prompt = SYSTEM_PROMPT.format(project_context=project_context)

    def list_tables_tool(_input: str) -> str:
        names = project.get_table_names()
        if not names:
            return "No tables in project."
        return "Available tables:\n" + "\n".join(f"- {name}" for name in names)

    def get_table_schema_tool(_input: str) -> str:
        df = project.get_table(_input.strip())
        if df is None:
            return f"Table '{_input}' not found. Available: {project.get_table_names()}"
        return project.get_schema_summary()

    def stats_tool(_input: str) -> str:
        table_name = _input.strip()
        df = project.get_table(table_name)
        if df is None:
            return f"Table '{table_name}' not found. Available: {project.get_table_names()}"
        result = _get_statistics(df)
        return f"Statistics for '{table_name}':\n" + json.dumps(result, ensure_ascii=False, indent=2)

    def query_tool(_input: str) -> str:
        try:
            params = json.loads(_input)
            table_name = params.get("table", "")
            question = params.get("question", _input)
        except json.JSONDecodeError:
            parts = _input.split("|", 1)
            table_name = parts[0].strip() if len(parts) > 1 else ""
            question = parts[1].strip() if len(parts) > 1 else _input
        df = project.get_table(table_name)
        if df is None:
            return f"Table '{table_name}' not found. Available: {project.get_table_names()}"
        return _query_data(df, question)

    def join_tables_tool(_input: str) -> str:
        try:
            params = json.loads(_input)
            table1 = params.get("table1", "")
            table2 = params.get("table2", "")
            on_col = params.get("on", None)
        except json.JSONDecodeError:
            parts = _input.split(",")
            table1 = parts[0].strip() if len(parts) > 0 else ""
            table2 = parts[1].strip() if len(parts) > 1 else ""
            on_col = parts[2].strip() if len(parts) > 2 else None
        df1 = project.get_table(table1)
        df2 = project.get_table(table2)
        if df1 is None:
            return f"Table '{table1}' not found."
        if df2 is None:
            return f"Table '{table2}' not found."
        if on_col is None:
            common = list(set(df1.columns) & set(df2.columns))
            if not common:
                return f"No common columns found between '{table1}' ({list(df1.columns)}) and '{table2}' ({list(df2.columns)}). Please specify a join column."
            on_col = common[0]
        try:
            merged = pd.merge(df1, df2, on=on_col, how="inner")
            preview = merged.head(10).to_string(index=False)
            return f"Joined '{table1}' + '{table2}' on '{on_col}': {len(merged)} rows, {len(merged.columns)} cols\nPreview:\n{preview}"
        except Exception as e:
            return f"Join failed: {str(e)}"

    def chart_tool(_input: str) -> str:
        try:
            params = json.loads(_input)
            table_name = params.get("table", "")
            chart_type = params.get("chart_type", "auto")
            x_col = params.get("x_col", None)
            y_col = params.get("y_col", None)
        except json.JSONDecodeError:
            return "Invalid JSON input. Use: {\"table\": \"name\", \"chart_type\": \"bar\"}"
        df = project.get_table(table_name)
        if df is None:
            return f"Table '{table_name}' not found. Available: {project.get_table_names()}"
        result = _generate_chart(df, chart_type=chart_type, x_col=x_col, y_col=y_col)
        return json.dumps(result, ensure_ascii=False)

    tools = [
        Tool(name="list_tables", func=list_tables_tool, description="List all table names in the current project"),
        Tool(name="get_table_schema", func=get_table_schema_tool, description="Get column info and sample data for a specific table. Input: table name"),
        Tool(name="get_statistics", func=stats_tool, description="Get statistical summary of a specific table. Input: table name"),
        Tool(name="query_table", func=query_tool, description="Query a specific table. Input: JSON {\"table\": \"name\", \"question\": \"your question\"} or 'table_name|question'"),
        Tool(name="join_tables", func=join_tables_tool, description="Join two tables on a column. Input: JSON {\"table1\": \"a\", \"table2\": \"b\", \"on\": \"col\"}"),
        Tool(name="generate_chart", func=chart_tool, description="Create chart from a table. Input: JSON {\"table\": \"name\", \"chart_type\": \"bar|line|histogram|heatmap\"}"),
    ]

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=full_prompt,
    )
    return agent
