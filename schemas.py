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
    # todo products: List[ProductSchema]

    class Config:
        from_attributes = True
