from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Seller
from app.database.session import get_session
from app.services.shipment import ShipmentService
from app.services.seller import SellerService
from app.core.security import oauth2_scheme
from app.utils import decode_access_token

SesionDep = Annotated[AsyncSession, Depends(get_session)]

def get_shipment_service(session: SesionDep):
    return ShipmentService(session)
def get_seller_service(session: SesionDep):
    return SellerService(session)

ShipmentServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]
SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]

async def get_current_seller(service: SellerServiceDep, token: Annotated[str, Depends(oauth2_scheme)]):
    data = decode_access_token(token)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    seller_id = data.get("sub")
    if not seller_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    return await service.get(int(seller_id))

SellerDep = Annotated[Seller, Depends(get_current_seller)]