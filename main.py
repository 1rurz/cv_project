import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from core.models import Base, db_helper
from api_v1 import router as router_v1
from core.config import settings
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("server.log"),
        logging.StreamHandler()
    ]
)

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost:5173",
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.on_event("startup")
async def startup_event():
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(router=router_v1, prefix=settings.api_v1_prifix)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8001)
