# Third Party Packages
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Local
from source.core.routers import api_router
from source.core.settings import settings

app = FastAPI(title=settings.APP_TITLE, version=settings.VERSION)

app.include_router(api_router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["health"])
async def health_check() -> dict:
    return {"health": True}
