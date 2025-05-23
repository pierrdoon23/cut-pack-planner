from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.main_page import router as main_router
from .routers.optimization_page import router as optimization_router
from .init_db import init_db

app = FastAPI(title="Backend for Desktop Dashboard")

init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # или ["http://localhost"]
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(main_router)
app.include_router(optimization_router)

