"""Schema Pydantic untuk kebutuhan autentikasi API."""

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """Payload registrasi user."""

    full_name: str = Field(
        min_length=2, max_length=120, description="Nama lengkap pengguna."
    )
    email: EmailStr = Field(description="Alamat email unik untuk login.")
    password: str = Field(
        min_length=6,
        max_length=128,
        description="Password plaintext yang akan di-hash sebelum disimpan.",
    )


class LoginRequest(BaseModel):
    """Payload login user."""

    email: EmailStr = Field(description="Email terdaftar pengguna.")
    password: str = Field(
        min_length=6, max_length=128, description="Password akun pengguna."
    )


class TokenResponse(BaseModel):
    """Response token setelah login berhasil."""

    access_token: str = Field(
        description="JWT access token untuk mengakses endpoint terlindungi."
    )
    refresh_token: str = Field(
        description="JWT refresh token untuk meminta access token baru."
    )


class RefreshResponse(BaseModel):
    """Response access token baru dari endpoint refresh."""

    access_token: str = Field(
        description="JWT access token baru hasil proses refresh."
    )


class MeResponse(BaseModel):
    """Response profil user yang sedang terautentikasi."""

    id: int
    full_name: str = Field(description="Nama lengkap pengguna.")
    email: EmailStr = Field(description="Email pengguna.")
    roles: list[str] = Field(description="Daftar role yang dimiliki pengguna.")
    permissions: list[str] = Field(
        description="Daftar permission efektif dari seluruh role pengguna."
    )
