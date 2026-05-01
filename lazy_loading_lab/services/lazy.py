from fastapi import FastAPI

routes = [
    {"method": "GET", "name": "h1", "func": lambda: "Hello world - 1", "path": "/h1"},
    {"method": "GET", "name": "h2", "func": lambda: "Hello world - 2", "path": "/h2"},
    {"method": "GET", "name": "h3", "func": lambda: "Hello world - 3", "path": "/h3"},
]


loaded_view_cache = {}


def lazy_view_factory(app: FastAPI):

    def lazy_view_entrypoint(name: str):

        def _lazy_view_entrypoint():
            route = list(filter(lambda x: x.get("name") == name, routes))[0]

            is_view_loaded = loaded_view_cache.get(name) is not None
            if not is_view_loaded:
                loaded_view_cache[name] = route.get("func")
                print(f"Loaded {name}")

            return route.get("func")()

        return _lazy_view_entrypoint

    for route in routes:
        app.add_api_route(
            path=route.get("path"),
            methods=[route.get("method")],
            status_code=200,
            endpoint=lazy_view_entrypoint(route.get("name")),
        )
