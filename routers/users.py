from typing import List

from fastapi import APIRouter, status, HTTPException
from sqlalchemy import update, delete
from sqlalchemy.future import select

import models
import schemas
from database import session

router = APIRouter()


@router.get("/", tags=["users"], response_model=List[schemas.ProductSchema])
async def get_products() -> List[models.Product]:
    response = await session.execute(select(models.Product))

    return response.scalars().all()


@router.get("/{id}", tags=["users"], response_model=schemas.ProductSchema)
async def get_product(id: int) -> models.Product:
    response = await session.execute(
        select(models.Product).where(models.Product.id == id)
    )
    user = response.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return user


@router.post(
    "/",
    tags=["users"],
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ProductSchema,
)
async def create_product(name: str) -> models.Product:
    user = models.Product(name=name)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.put("/{id}", tags=["users"], response_model=schemas.ProductSchema)
async def edit_product(id: int, name: str) -> models.Product:
    response = await session.execute(
        select(models.Product).where(models.Product.id == id)
    )
    user = response.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Item not found")

    await session.execute(
        update(models.Product).where(models.Product.id == id).values(name=name)
    )
    await session.commit()

    return user


@router.delete("/{id}", tags=["users"])
async def delete_product(id: int) -> dict:
    response = await session.execute(
        select(models.Product).where(models.Product.id == id)
    )
    user = response.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Item not found")

    await session.execute(delete(models.Product).where(models.Product.id == id))
    await session.commit()

    return {"message": "Item deleted successfully"}
