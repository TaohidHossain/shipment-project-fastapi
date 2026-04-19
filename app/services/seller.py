from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.api.schemas.seller import SellerCreate
from app.database.models import Seller


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SellerService:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def add(self, credentials: SellerCreate) -> Seller:
        seller = Seller(**credentials.model_dump(exclude={"password"}))
        seller.password_hash = password_context.hash(credentials.password)
        self.db.add(seller)
        await self.db.commit()
        await self.db.refresh(seller)
        return seller