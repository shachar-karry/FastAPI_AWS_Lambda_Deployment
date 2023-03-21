from mangum import Mangum
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/r1")
async def root():
    return {"message": "r1"}

@app.get("/r2")
async def root():
    return {"message": "r2"}

handler = Mangum(app=app)
