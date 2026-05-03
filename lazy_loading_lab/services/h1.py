from fastapi import Request
from starlette.datastructures import URL

dependencies = {
    "request": Request,
}


async def index(request: Request) -> str:
    return request.url.path
