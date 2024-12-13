from fastapi import FastAPI

from api.routers.db_router import router as db_router
from api.routers.parser import router as parser_router


app = FastAPI()
app.include_router(router=db_router, prefix="/db")
app.include_router(router=parser_router, prefix="/parser")

