from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.shipment import ShipmentCreate
from app.database.models import Shipment, ShipmentStatus


class ShipmentService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, id: int) -> Shipment | None:
        return await self.session.get(Shipment, id)
    
    async def add(self, shipment_create: ShipmentCreate) -> Shipment:
        shipment = Shipment(
            **shipment_create.model_dump(),
            status = ShipmentStatus.placed,
            estimated_delivery = datetime.now() + timedelta(days=3)
        )

        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)

        return shipment
    
    async def update(self, id: int, shipment_update: dict[str, str]) -> Shipment | None:
        shipment = await self.get(id)
        if not shipment:
            return None
        
        shipment.sqlmodel_update(shipment_update)
        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)

        return shipment
    
    async def delete(self, shipment: Shipment) -> None:
        await self.session.delete(shipment)
        await self.session.commit()