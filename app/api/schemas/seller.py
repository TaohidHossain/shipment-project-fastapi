from pydantic import BaseModel, EmailStr


class BaseSeller(BaseModel):
    name: str
    email: EmailStr

class SellerRead(BaseSeller):
    id: int

class SellerCreate(BaseSeller):
    password: str