from typing import List
from sqlalchemy.future import select

from pydantic import BaseModel, computed_field

import models
from database import session


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

    @computed_field
    @property
    def products(self) -> List[ProductSchema]:
        return []  # todo products: List[ProductSchema]

    class Config:
        from_attributes = True
