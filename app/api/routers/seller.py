from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.api.schemas.seller import SellerCreate, SellerRead
from app.api.dependancies import SellerServiceDep, SellerDep
from app.core.security import oauth2_scheme
from app.utils import decode_access_token

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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}

@router.get("/dashboard")
async def seller_dashboard(
    seller: SellerDep
):
    if not seller:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return {"message": f"Hello, {seller.email}!"}