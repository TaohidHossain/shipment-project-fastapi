from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.api.schemas.seller import SellerCreate, SellerRead
from app.api.dependancies import SellerServiceDep

router = APIRouter(prefix="/seller", tags=["Seller"])

@router.post("/signup", response_model=SellerRead)
async def seller_signup(credentials: SellerCreate, service: SellerServiceDep):
    return await service.add(credentials)

@router.post("/token")
async def seller_login(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: SellerServiceDep
):
    token = await service.token(request_form.username, request_form.password)
    if not token:
        return {"error": "Invalid credentials"}
    return {"access_token": token, "token_type": "bearer"}
