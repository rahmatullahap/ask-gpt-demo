from fastapi import APIRouter

from app.api.ask import router as ask_router


routers = APIRouter()
router_list = [ask_router]

for router in router_list:
    routers.include_router(router)
