from typing import List

from fastapi import APIRouter, status, HTTPException
from sqlalchemy import delete
from sqlalchemy.future import select

import models
import schemas
from database import session

router = APIRouter()


@router.get("/", tags=["orders"], response_model=List[schemas.OrderSchema])
async def get_orders() -> List[models.Order]:
    response = await session.execute(
        select(models.Order).join(models.Order.user)
        # todo добавить подзадпрос для получения списка продуктов
    )

    return response.scalars().all()


@router.get("/{id}", tags=["orders"], response_model=schemas.OrderSchema)
async def get_order(id: int) -> models.Order:
    response = await session.execute(
        select(models.Order)
        .join(models.Order.user)
        .where(models.Order.id == id)
        # todo добавить подзадпрос для получения списка продуктов
    )
    order = response.scalar_one_or_none()
    if order is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return order


@router.post(
    "/",
    tags=["orders"],
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.OrderSchema,
)
async def create_order(user_id: int, product_ids: List[int]) -> models.Order:
    order = models.Order(user_id=user_id)
    session.add(order)
    await session.flush()

    order_products = [
        models.OrderProduct(order_id=order.id, product_id=product_id)
        for product_id in product_ids
    ]
    [
        session.add(order_product) for order_product in order_products
    ]  # todo заменить на bulk create
    await session.commit()
    await session.refresh(order)
    return order


@router.put("/{id}", tags=["orders"], response_model=schemas.OrderSchema)
async def edit_order(id: int, product_ids: List[int]) -> models.Order:
    response = await session.execute(select(models.Order).where(models.Order.id == id))
    order = response.scalar_one_or_none()
    if order is None:
        raise HTTPException(status_code=404, detail="Item not found")

    await session.execute(
        delete(models.OrderProduct).where(models.OrderProduct.order_id == id)
    )
    order_products = [
        models.OrderProduct(order_id=id, product_id=product_id)
        for product_id in product_ids
    ]
    [
        session.add(order_product) for order_product in order_products
    ]  # todo заменить на bulk create
    await session.commit()

    return order


@router.delete("/{id}", tags=["orders"])
async def delete_order(id: int) -> dict:
    response = await session.execute(select(models.Order).where(models.Order.id == id))
    order = response.scalar_one_or_none()
    if order is None:
        raise HTTPException(status_code=404, detail="Item not found")

    await session.execute(delete(models.Order).where(models.Order.id == id))
    await session.commit()

    return {"message": "Item deleted successfully"}
