from fastapi import APIRouter

from app.api.api_v1.endpoints import items, auth, users, utils, mediae, medialabels

api_router = APIRouter()
api_router.include_router(auth.router, tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(mediae.router, prefix="/mediae", tags=["medias"])
api_router.include_router(medialabels.router, prefix="/medialabels", tags=["medialabels"])

