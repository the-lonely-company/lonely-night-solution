from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router.database import db_router
from router.account import account_router
from router.document import document_router
from router.search_engine import search_engine_router


app = FastAPI(
    title='Night Solution'
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(db_router)
app.include_router(account_router)
app.include_router(document_router)
app.include_router(search_engine_router)
