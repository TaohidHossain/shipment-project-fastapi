from fastapi import APIRouter

from app.api.schemas.seller import SellerCreate, SellerRead
from app.api.dependancies import SellerServiceDep

router = APIRouter(prefix="/seller", tags=["Seller"])

@router.post("/signup", response_model=SellerRead)
async def seller_signup(credentials: SellerCreate, service: SellerServiceDep):
    return await service.add(credentials)
