from fastapi.requests import Request


class BaseService:
    request: Request

    def __init__(self, request: Request) -> None:
        self.request = request

    @classmethod
    def get_service_session(cls, request: Request):
        return cls(request=request)


class DefaultService(BaseService):
    def index(self) -> str:
        return self.request.url.path
