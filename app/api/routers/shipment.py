from fastapi import APIRouter, HTTPException, status

from app.api.dependancies import SellerDep, ShipmentServiceDep
from app.api.schemas.shipment import ShipmentCreate, ShipmentRead, ShipmentUpdate

router = APIRouter(prefix="/shipment", tags=["Shipment"])

@router.get("/", response_model=ShipmentRead)
async def get_shipment(id: int, service: ShipmentServiceDep):
    shipemnt = await service.get(id)

    if not shipemnt:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist"
        )
    return shipemnt

@router.post("/", response_model=ShipmentRead)
async def submit_shipment(
    shipment: ShipmentCreate,
    service: ShipmentServiceDep,
    _: SellerDep
):
    return await service.add(shipment)

@router.patch("/", response_model=ShipmentRead)
async def update_shipment(
    id: int,
    shipment_update: ShipmentUpdate,
    service: ShipmentServiceDep,
    _: SellerDep
):
    # Update data with given fields
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update",
        )

    updated_shipement = await service.update(id, update)
    if not updated_shipement:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist"
        )
    return updated_shipement

@router.delete("/")
async def delete_shipment(id: int, service: ShipmentServiceDep, _: SellerDep) -> dict[str, str]:
    shipment = await service.get(id)
    if not shipment:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist"
        )
    # Remove from database
    await service.delete(shipment)

    return {"detail": f"Shipment with id #{id} is deleted!"}