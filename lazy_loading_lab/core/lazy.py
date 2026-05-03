from functools import wraps
from typing import Any, Callable, Dict, Type
from fastapi import FastAPI
import importlib
import pathlib
import inspect

loaded_view_cache = {}


def should_ignore_file_or_dir(name: str) -> bool:
    return (
        name.__contains__("__")
        or name.startswith("_")
        or name.__contains__("Request")
        or name == "dependencies"
    )


def lazy_view_entrypoint(func: Callable, url: str):

    @wraps(func)
    async def _lazy_view_entrypoint(**kwargs):
        return await func(**kwargs)

    return _lazy_view_entrypoint


def lazy_view_factory(app: FastAPI) -> FastAPI:
    services_path = "lazy_loading_lab/services"
    services = pathlib.Path(services_path)

    for service in services.iterdir():
        if should_ignore_file_or_dir(service.name):
            continue

        service_name = service.name.replace(".py", "")
        service_module = importlib.import_module(
            f"{services_path.replace('/', '.')}.{service_name}"
        )

        routes_names = list(
            filter(
                lambda x: not should_ignore_file_or_dir(x),
                [route for route in dir(service_module)],
            )
        )

        for name in routes_names:
            url = f"/{service_name}/{name}"
            app.add_api_route(
                path=url,
                methods=["GET", "POST"],
                status_code=200,
                endpoint=lazy_view_entrypoint(
                    func=getattr(service_module, name),
                    url=url
                ),
            )

    return app
