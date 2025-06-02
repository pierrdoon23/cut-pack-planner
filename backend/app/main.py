from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.main_page import router as main_router
from .routers.optimization_page import router as optimization_router
from .routers.creation_page import router as creation_router
from .routers.reports import router as report_router
from .routers.login_page import router as login_router

from .init_db import init_db

app = FastAPI(title="Backend for Desktop Dashboard")

init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(main_router)
app.include_router(login_router)
app.include_router(optimization_router)
app.include_router(creation_router)
app.include_router(report_router)


