from typing import List

from fastapi import APIRouter, status, HTTPException
from sqlalchemy import update, delete
from sqlalchemy.future import select

import models
import schemas
from database import session

router = APIRouter()


@router.get("/", tags=["products"], response_model=List[schemas.ProductSchema])
async def get_products() -> List[models.Product]:
    response = await session.execute(select(models.Product))

    return response.scalars().all()


@router.get("/{id}", tags=["products"], response_model=schemas.ProductSchema)
async def get_product(id: int) -> models.Product:
    response = await session.execute(select(models.Product).where(models.Product.id == id))
    product = response.scalar_one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return product


@router.post(
    "/",
    tags=["products"],
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ProductSchema,
)
async def create_product(name: str) -> models.Product:
    product = models.Product(name=name)
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


@router.put("/{id}", tags=["products"], response_model=schemas.ProductSchema)
async def edit_product(id: int, name: str) -> models.Product:
    response = await session.execute(select(models.Product).where(models.Product.id == id))
    product = response.scalar_one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail="Item not found")

    await session.execute(update(models.Product).where(models.Product.id == id).values(name=name))
    await session.commit()

    return product


@router.delete("/{id}", tags=["products"])
async def delete_product(id: int) -> dict:
    response = await session.execute(select(models.Product).where(models.Product.id == id))
    product = response.scalar_one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail="Item not found")

    await session.execute(delete(models.Product).where(models.Product.id == id))
    await session.commit()

    return {"message": "Item deleted successfully"}
