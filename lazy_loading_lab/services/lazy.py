from dataclasses import dataclass
from typing import Callable, Literal
from fastapi import FastAPI


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


def lazy_view_factory(app: FastAPI):

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

    for route in routes:
        app.add_api_route(
            path=route.path,
            methods=[route.method],
            status_code=200,
            endpoint=lazy_view_entrypoint(route.name),
        )
