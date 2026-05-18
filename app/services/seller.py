from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext

from app.api.schemas.seller import SellerCreate
from app.database.models import Seller
from app.utils import generate_access_token
from app.config import jwt_settings



password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SellerService:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get(self, id: int) -> Seller | None:
        result = await self.db.get(Seller, id)
        return result
    
    async def add(self, credentials: SellerCreate) -> Seller:
        seller = Seller(**credentials.model_dump(exclude={"password"}))
        seller.password_hash = password_context.hash(credentials.password)
        self.db.add(seller)
        await self.db.commit()
        await self.db.refresh(seller)
        return seller

    async def token(self, email: str, password: str) -> str | None:
        result = await self.db.execute(
            select(Seller).filter_by(email=email)
        )
        seller = result.scalar_one_or_none()
        if not seller or not password_context.verify(password, seller.password_hash):
            return None
        token = generate_access_token(
            data={
                "sub": str(seller.id),
                "email": seller.email
            },
            expiry=timedelta(minutes=jwt_settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return token