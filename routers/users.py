from typing import List

from fastapi import APIRouter, status, HTTPException
from passlib.context import CryptContext
from sqlalchemy import update
from sqlalchemy.future import select

import models
import schemas
from database import session

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/", tags=["users"], response_model=List[schemas.UserSchema])
async def get_users() -> List[models.User]:
    response = await session.execute(select(models.User))

    return response.scalars().all()


@router.get("/{id}", tags=["users"], response_model=schemas.UserSchema)
async def get_user(id: int) -> models.User:
    response = await session.execute(select(models.User).where(models.User.id == id))
    user = response.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return user


@router.post(
    "/registration",
    tags=["users"],
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserSchema,
)
async def create_user(name: str, email: str, password: str) -> models.User:
    user = models.User(
        name=name,
        email=email,
        hashed_password=pwd_context.hash(password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.put("/{id}", tags=["users"], response_model=schemas.UserSchema)
async def edit_user(id: int, name: str | None, email: str | None) -> models.User:
    response = await session.execute(select(models.User).where(models.User.id == id))
    user = response.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Item not found")

    data = {}
    if name is not None:
        data["name"] = name
    if email is not None:
        data["email"] = email

    await session.execute(
        update(models.User).where(models.User.id == id).values(**data)
    )
    await session.commit()

    return user
