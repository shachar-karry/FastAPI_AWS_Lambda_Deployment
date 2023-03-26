from mangum import Mangum
from fastapi import FastAPI
import subprocess

#app = FastAPI(root_path="/dev/")
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Does not work trivially in Lambda
# @app.get("/gitlog")
# async def root():
#     return {"message": subprocess.check_output(["git", "log", "-n", "1"]) }


@app.get("/r1")
async def root():
    return {"message": "r1"}


@app.get("/r2")
async def root():
    return {"message": "r2"}

handler = Mangum(app=app)
