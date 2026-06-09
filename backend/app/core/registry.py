import pkgutil
import importlib
from types import ModuleType

_tool_registry: dict[str, dict] = {}


def register_tool(
    name: str,
    description: str = "",
    icon: str = "i-heroicons-cube",
    router: ModuleType | None = None,
):
    def decorator(func):
        _tool_registry[name] = {
            "name": name,
            "description": description,
            "icon": icon,
            "func": func,
            "router": router,
        }
        return func

    return decorator


def get_all_tools() -> list[dict]:
    return [
        {"name": v["name"], "description": v["description"], "icon": v["icon"]}
        for v in _tool_registry.values()
    ]


def get_tool_router(name: str):
    entry = _tool_registry.get(name)
    if entry and entry["router"] is not None:
        return entry["router"]
    return None


def discover_tools():
    package = importlib.import_module("app.tools")
    for _, modname, ispkg in pkgutil.iter_modules(package.__path__):
        if not ispkg and modname != "__init__":
            importlib.import_module(f"app.tools.{modname}")
        else:
            importlib.import_module(f"app.tools.{modname}")
