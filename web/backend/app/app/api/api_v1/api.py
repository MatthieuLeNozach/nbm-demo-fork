from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, users, utils, mediae, medialabels, devices, sites, species, standardlabels

api_router = APIRouter()
api_router.include_router(auth.router, tags=["Auth"])
api_router.include_router(devices.router, prefix="/devices", tags=["Devices"])
api_router.include_router(mediae.router, prefix="/mediae", tags=["Mediae"])
api_router.include_router(medialabels.router, prefix="/medialabels", tags=["Media labels"])
api_router.include_router(sites.router, prefix="/sites", tags=["Sites"])
api_router.include_router(species.router, prefix="/species", tags=["Species"])
api_router.include_router(standardlabels.router, prefix="/standardlabels", tags=["Standard labels"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(utils.router, prefix="/utils", tags=["Utils"])

