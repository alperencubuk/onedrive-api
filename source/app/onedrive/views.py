# Third Party Packages
from fastapi import APIRouter
from fastapi.background import BackgroundTasks
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

# Local
from source.app.onedrive.onedrive import OneDriveStorage

onedrive_router = APIRouter(prefix="/onedrive", tags=["onedrive"])


@onedrive_router.get("/auth/{user_id}")
async def auth(user_id: str) -> RedirectResponse:
    return RedirectResponse(OneDriveStorage(user_id=user_id).get_auth_url())


@onedrive_router.get("/callback")
async def callback(state: str, request: Request) -> dict:
    if OneDriveStorage(user_id=state).authenticate(
        str(request.url).replace("http://", "https://")
    ):
        return {"auth": True}
    return {"auth": False}


@onedrive_router.get("/list/{user_id}")
async def list_items(user_id: str) -> dict:
    storage = OneDriveStorage(user_id=user_id)
    if storage.check_connection():
        return storage.get_file_list()
    return {"error": "Authentication failed"}


@onedrive_router.get("/download/{user_id}")
async def download_all(user_id: str, background_tasks: BackgroundTasks) -> dict:
    storage = OneDriveStorage(user_id=user_id)
    if storage.check_connection():
        background_tasks.add_task(storage.download_all)
        return {"result": "Download process started"}
    return {"error": "Authentication failed"}
