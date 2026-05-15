

from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import transaction, auth  # <-- importa auth
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://tracflow-easy-money.lovable.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)        
app.include_router(transaction.router)  