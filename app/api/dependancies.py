from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.services.shipment import ShipmentService

SesionDep = Annotated[AsyncSession, Depends(get_session)]

def get_shipment_service(session: SesionDep):
    return ShipmentService(session)

ShipmentServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]