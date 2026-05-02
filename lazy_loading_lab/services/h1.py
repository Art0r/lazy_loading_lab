from fastapi import Request

dependencies = [
    Request,
]


def index(*args) -> str:
    request: Request = args[0]
    return request.url.path
