from typing import List, Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    name: str
    count: Optional[int]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class OrderBase(BaseModel):
    user: UserSchema
    count: Optional[int]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ProductSchema(ProductBase):
    orders: List[OrderBase]


class OrderSchema(OrderBase):
    products: List[ProductBase]
