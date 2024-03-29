from typing import List

from pydantic import BaseModel

from schemas.products import ProductSchema
from schemas.users import UserSchema


class OrderSchema(BaseModel):
    id: int
    user: UserSchema

    class Config:
        from_attributes = True


class OrderExtendSchema(OrderSchema):
    products: List[ProductSchema] = []
