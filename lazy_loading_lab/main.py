from fastapi import FastAPI
import uvicorn
from lazy_loading_lab.services.lazy import lazy_view_factory

app = FastAPI()


lazy_view_factory(app)

if __name__ == "__main__":
    uvicorn.run("lazy_loading_lab.main:app",
                host="0.0.0.0", port=8000, reload=True)
