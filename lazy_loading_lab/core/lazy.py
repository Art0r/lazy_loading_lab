from dataclasses import dataclass
from typing import Callable, Literal
from fastapi import FastAPI
import importlib
import pathlib


@dataclass
class Route:
    name: str
    method: Literal["GET"]
    path: str
    func: Callable


routes = [
    Route(name="h1", method="GET", func=lambda: "Hello World - 1", path="/h1"),
    Route(name="h2", method="GET", func=lambda: "Hello World - 2", path="/h2"),
    Route(name="h3", method="GET", func=lambda: "Hello World - 3", path="/h3"),
]


loaded_view_cache = {}


def should_ignore_file_or_dir(path: pathlib.Path) -> bool:
    name = path.name
    return name.__contains__("__") or name.startswith("_")


def lazy_view_entrypoint(name: str):

    def _lazy_view_entrypoint():
        route = list(filter(lambda x: x.name == name, routes))[0]

        is_view_loaded = loaded_view_cache.get(name) is not None
        if not is_view_loaded:
            loaded_view_cache[name] = route
            route = loaded_view_cache[name]
            print(f"Loaded {name}")

        return route.func()

    return _lazy_view_entrypoint


def lazy_view_factory(app: FastAPI) -> FastAPI:

    services = pathlib.Path("lazy_loading_lab/services")

    for service in services.iterdir():
        if should_ignore_file_or_dir(service):
            continue

        service_name = service.name.replace(".py", "")

        app.add_api_route(
            path=f"/{service_name}",
            methods=["GET", "POST"],
            status_code=200,
            endpoint=lazy_view_entrypoint(service_name),
        )

    return app
