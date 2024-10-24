from fastapi import FastAPI
import uvicorn

from auth.routers import router as auth_router
from referal_api.routers import router as referal_router
from db import DbWorcker


app = FastAPI(
    title='test_referal_app'
)

db_worcker = DbWorcker()


app.include_router(auth_router, tags=['auth'])
app.include_router(referal_router, tags=['referal'])


if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host='0.0.0.0',
        port=8000,
    )
