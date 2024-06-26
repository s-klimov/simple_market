from typing import List, Annotated

from fastapi import APIRouter, status, HTTPException, Query, Path, Depends
from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.orm import Session

import models
import schemas
from database import get_session
from routers.users import get_current_user

router = APIRouter()


@router.get("/", tags=["orders"], response_model=List[schemas.OrderSchema])
async def get_orders(session: Session = Depends(get_session)) -> List[models.Order]:
    response = await session.execute(select(models.Order).join(models.Order.user))

    return response.scalars().all()


@router.get("/{id}", tags=["orders"], response_model=schemas.OrderExtendSchema)
async def get_order(id: int, session: Session = Depends(get_session)) -> models.Order:
    response = await session.execute(select(models.Order).join(models.Order.user).where(models.Order.id == id))
    order = response.scalar_one_or_none()
    if order is None:
        raise HTTPException(status_code=404, detail="Item not found")

    response = await session.execute(
        select(models.Product).join(models.OrderProduct).where(models.OrderProduct.order_id == order.id)
    )
    order.__dict__["products"] = response.scalars().all()

    return order


@router.post(
    "/",
    tags=["orders"],
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.OrderSchema,
)
async def create_order(
    current_user: Annotated[schemas.UserSchema, Depends(get_current_user)],
    product_ids: List[int],
    session: Session = Depends(get_session),
) -> models.Order:
    """Создание заказа."""
    order = models.Order(user_id=current_user.id)
    session.add(order)
    await session.flush()

    order_products = [models.OrderProduct(order_id=order.id, product_id=product_id) for product_id in product_ids]
    [session.add(order_product) for order_product in order_products]  # todo заменить на bulk create
    await session.commit()
    await session.refresh(order)
    return order


@router.put("/{id}", tags=["orders"], response_model=schemas.OrderSchema)
async def edit_order(
    id: int = Path(..., gt=0, description="Идентификатор заказа"),
    product_ids: Annotated[List[int], Query(description="Список идентификаторов продуктов")] = ...,
    session: Session = Depends(get_session),
) -> models.Order:
    """Редактирование заказа."""

    response = await session.execute(select(models.Order).where(models.Order.id == id))
    order = response.scalar_one_or_none()
    if order is None:
        raise HTTPException(status_code=404, detail="Item not found")

    await session.execute(delete(models.OrderProduct).where(models.OrderProduct.order_id == id))
    order_products = [models.OrderProduct(order_id=id, product_id=product_id) for product_id in product_ids]
    [session.add(order_product) for order_product in order_products]  # todo заменить на bulk create
    await session.commit()

    return order


@router.delete("/{id}", tags=["orders"])
async def delete_order(id: int, session: Session = Depends(get_session)) -> dict:
    response = await session.execute(select(models.Order).where(models.Order.id == id))
    order = response.scalar_one_or_none()
    if order is None:
        raise HTTPException(status_code=404, detail="Item not found")

    await session.execute(delete(models.Order).where(models.Order.id == id))
    await session.commit()

    return {"message": "Item deleted successfully"}
