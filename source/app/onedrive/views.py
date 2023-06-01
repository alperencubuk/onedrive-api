# Third Party Packages
from fastapi import APIRouter
from fastapi.background import BackgroundTasks
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

# Local
from source.app.onedrive.onedrive import OneDriveStorage

onedrive_router = APIRouter(prefix="/onedrive", tags=["onedrive"])

storage = OneDriveStorage()


@onedrive_router.get("/auth")
async def auth() -> RedirectResponse:
    return RedirectResponse(storage.get_auth_url())


@onedrive_router.get("/callback")
async def callback(request: Request) -> dict:
    if storage.authenticate(str(request.url).replace("http://", "https://")):
        return {"auth": True}
    return {"auth": False}


@onedrive_router.get("/list")
async def list_items() -> dict:
    if storage.check_connection():
        return storage.get_file_list()
    return {"error": "Authentication failed"}


@onedrive_router.get("/download")
async def download_all(background_tasks: BackgroundTasks) -> dict:
    if storage.check_connection():
        background_tasks.add_task(storage.download_all)
        return {"result": "Download process started"}
    return {"error": "Authentication failed"}
