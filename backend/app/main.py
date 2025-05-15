from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.main_page import router as main_router

app = FastAPI(title="Backend for Desktop Dashboard")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # или ["http://localhost"] если хочешь ограничить
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(main_router)
