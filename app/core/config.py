import os

from pydantic import BaseModel


class JWTSettings(BaseModel):
    authjwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "change-this-secret-key")
    authjwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    authjwt_access_token_expires: int = int(os.getenv("JWT_ACCESS_EXPIRES", "3600"))
    authjwt_refresh_token_expires: int = int(os.getenv("JWT_REFRESH_EXPIRES", "86400"))

