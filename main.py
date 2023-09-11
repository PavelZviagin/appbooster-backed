import uvicorn
from fastapi import FastAPI

from experiments.router import api_router
from loader.load_data import load_data

app = FastAPI(
    title="Appbooster Backend",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.include_router(api_router)


@app.on_event("startup")
async def start():
    load_data()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
