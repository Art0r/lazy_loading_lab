from typing import Annotated
from fastapi import Depends, FastAPI
import uvicorn
from lazy_loading_lab.core.base import DefaultService
from lazy_loading_lab.core.lazy import lazy_view_factory

app = FastAPI()


lazy_view_factory(app)


@app.get("/")
async def index(
    service: Annotated[DefaultService, Depends(DefaultService.get_service_session)],
):
    return service.index()


if __name__ == "__main__":
    uvicorn.run("lazy_loading_lab.main:app",
                host="0.0.0.0", port=8000, reload=True)
