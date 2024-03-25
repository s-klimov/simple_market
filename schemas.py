from typing import List

from pydantic import BaseModel


class UserSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    user: UserSchema

    class Config:
        orm_mode = True


class ProductSchema(ProductBase):
    orders: List[OrderBase]


class OrderSchema(OrderBase):
    products: List[ProductBase]
