from fastapi import APIRouter

from app.api.routers.shipment import router as shipemnt_router
from app.api.routers.seller import router as seller_router

api_router = APIRouter(
    prefix="/api/v1"
)

api_router.include_router(shipemnt_router)
api_router.include_router(seller_router)