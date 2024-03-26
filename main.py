from fastapi import FastAPI


import models
from database import engine, session

from routers import users


app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await engine.dispose()


app.include_router(users.router, prefix="/users")


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
