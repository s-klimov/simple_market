from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    hashed_password: str = Field(exclude=True)
    disabled: bool | None = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
