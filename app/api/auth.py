from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.database import get_db
from app.models import Role, User
from app.schemas.auth import LoginRequest, MeResponse, RefreshResponse, RegisterRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["Auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _serialize_access_profile(user: User) -> tuple[list[str], list[str]]:
    role_names = sorted(role.name for role in user.roles)
    permission_codes = sorted(
        {permission.code for role in user.roles for permission in role.permissions}
    )
    return role_names, permission_codes


def _build_token_response(Authorize: AuthJWT, user: User) -> TokenResponse:
    roles, permissions = _serialize_access_profile(user)
    claims = {"roles": roles, "permissions": permissions}
    access_token = Authorize.create_access_token(subject=str(user.id), user_claims=claims)
    refresh_token = Authorize.create_refresh_token(subject=str(user.id))
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> dict[str, str]:
    existing_user = db.scalar(select(User).where(User.email == payload.email))
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email is already registered"
        )

    user = User(
        full_name=payload.full_name,
        email=payload.email,
        password_hash=pwd_context.hash(payload.password),
        is_active=True,
    )
    db.add(user)
    db.commit()
    return {"message": "User registered"}


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)) -> TokenResponse:
    query = (
        select(User)
        .where(User.email == payload.email)
        .options(selectinload(User.roles).selectinload(Role.permissions))
    )
    user = db.scalar(query)

    if not user or not pwd_context.verify(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is inactive")

    return _build_token_response(Authorize, user)


@router.post("/refresh", response_model=RefreshResponse)
def refresh(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)) -> RefreshResponse:
    Authorize.jwt_refresh_token_required()
    user_id = Authorize.get_jwt_subject()

    user = db.scalar(
        select(User)
        .where(User.id == int(user_id))
        .options(selectinload(User.roles).selectinload(Role.permissions))
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    roles, permissions = _serialize_access_profile(user)
    access_token = Authorize.create_access_token(
        subject=str(user.id), user_claims={"roles": roles, "permissions": permissions}
    )
    return RefreshResponse(access_token=access_token)


@router.get("/me", response_model=MeResponse)
def me(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)) -> MeResponse:
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    user = db.scalar(
        select(User)
        .where(User.id == int(user_id))
        .options(selectinload(User.roles).selectinload(Role.permissions))
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    roles, permissions = _serialize_access_profile(user)
    return MeResponse(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        roles=roles,
        permissions=permissions,
    )
