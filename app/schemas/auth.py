from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class RefreshResponse(BaseModel):
    access_token: str


class MeResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    roles: list[str]
    permissions: list[str]

