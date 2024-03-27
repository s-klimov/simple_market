from typing import List

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ProductSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class OrderSchema(BaseModel):
    id: int
    user: UserSchema

    class Config:
        from_attributes = True


class OrderExtendSchema(OrderSchema):
    products: List[ProductSchema] = []
