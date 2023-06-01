# Third Party Packages
from fastapi import APIRouter

# Local
from source.app.onedrive.views import onedrive_router

api_router = APIRouter()

api_router.include_router(onedrive_router)
