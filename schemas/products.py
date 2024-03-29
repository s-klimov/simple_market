from pydantic import BaseModel


class ProductSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
