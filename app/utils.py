from datetime import datetime, timedelta
import jwt
from app.config import jwt_settings

def generate_access_token(data: dict, expiry: timedelta = timedelta(days=1)) -> str:
    token = jwt.encode(
        {
            **data,
            "exp": datetime.now() + expiry
        },
        key=jwt_settings.JWT_SECRET,
        algorithm=jwt_settings.JWT_ALGORITHM
    )
    return token

def decode_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(
            token,
            key=jwt_settings.JWT_SECRET,
            algorithms=[jwt_settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None