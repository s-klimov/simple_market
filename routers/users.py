@app.get(
    "/users/{id}", response_model=schemas.UserSchema, response_model_by_alias=False
)
async def get_user(id: int) -> models.User:
    res = await session.execute(select(models.User).where(models.User.id == id))
    try:
        user = res.scalars().one()
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

    return user
