from typing import List

from fastapi import APIRouter, status, HTTPException
from sqlalchemy import update, delete
from sqlalchemy.future import select

import models
import schemas
from database import session

router = APIRouter()


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
    "/",
    tags=["users"],
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserSchema,
)
async def create_user(name: str) -> models.User:
    user = models.User(name=name)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.put("/{id}", tags=["users"], response_model=schemas.UserSchema)
async def edit_user(id: int, name: str) -> models.User:
    response = await session.execute(select(models.User).where(models.User.id == id))
    user = response.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Item not found")

    await session.execute(
        update(models.User).where(models.User.id == id).values(name=name)
    )
    await session.commit()

    return user


@router.delete("/{id}", tags=["users"])
async def delete_user(id: int) -> dict:
    response = await session.execute(select(models.User).where(models.User.id == id))
    user = response.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Item not found")

    await session.execute(delete(models.User).where(models.User.id == id))
    await session.commit()

    return {"message": "Item deleted successfully"}
