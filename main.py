from fastapi import FastAPI

from routers import products, users, orders


app = FastAPI()


app.include_router(users.router, prefix="/users")
app.include_router(products.router, prefix="/products")
app.include_router(orders.router, prefix="/orders")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
