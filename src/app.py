import os
from typing import List

from loguru import logger

from langchain_core.messages import AIMessage, HumanMessage
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

from fastapi.middleware.cors import CORSMiddleware

from chains.full_chain import full_chain
from models.request_models import Messages, Message
from models.api_models import InvokeResponse
from connections.mongodb.mongodb_client import db_client
from routers.database import db_router
from agents.customer_service_assistant import customer_service_assistant


os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"]="https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"]="ls__77cfce357c894d9b9c86905ccac64de6"
os.environ["LANGCHAIN_PROJECT"]="Alcohol"


app = FastAPI(
    title='Lonely Backend'
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(db_router)


def gen(content: str, chat_history: List) -> str:
    for chunk in full_chain.stream({"content": content, "chat_history": chat_history}):
        yield chunk


# def convert_to_langchain_message(turn: Turn):
#     logger.debug(turn.content)
#     if turn.party == 'ai':
#         return AIMessage(content=turn.content)
    
#     return HumanMessage(content=turn.content)


@app.post("/stream")
def stream(message: Messages, request: Request):
    content = message.content
    chat_history = [
        # convert_to_langchain_message(turn)
        # for turn in message.chat_history
    ]

    logger.info(request.headers)

    gen_init = gen(message.content, chat_history)

    return StreamingResponse(gen_init, media_type="text/event-stream")

@app.post("/invoke", response_model=InvokeResponse)
def invoke(messages: List[Message], request: Request) -> InvokeResponse:
    logger.info(request.headers)

    response = customer_service_assistant.respond(messages)

    return response

# ----- PostgreSQL API -----


from fastapi import Depends, FastAPI, HTTPException

from sqlalchemy.orm import Session
from connections.postgreSQL import postgresql_client
from models.database_models import postgreSQL_schemas
from models import postgreSQL_model
from connections.postgreSQL.postgresql_connection import SessionLocal, engine

postgreSQL_model.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get user by user_id
@app.get("/users/{user_id}", response_model=postgreSQL_schemas.User)
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = postgresql_client.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Create a new user
@app.post("/users/", response_model=postgreSQL_schemas.User)
def create_user(user: postgreSQL_schemas.UserCreate, db: Session = Depends(get_db)):
    return postgresql_client.create_user(db=db, user=user)

# Update an existing user
@app.put("/users/{user_id}", response_model=postgreSQL_schemas.User)
def update_user(user_id: str, user: postgreSQL_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = postgresql_client.update_user(db=db, user_id=user_id, user_update=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Create a new merchant
@app.post("/merchants/", response_model=postgreSQL_schemas.Merchant)
def create_merchant(merchant: postgreSQL_schemas.MerchantCreate, db: Session = Depends(get_db)):
    return postgresql_client.create_merchant(db=db, merchant=merchant)

# Update an existing merchant
@app.put("/merchants/{merchant_id}", response_model=postgreSQL_schemas.Merchant)
def update_merchant(merchant_id: str, merchant: postgreSQL_schemas.MerchantCreate, db: Session = Depends(get_db)):
    db_merchant = postgresql_client.update_merchant(db=db, merchant_id=merchant_id, merchant_update=merchant)
    if db_merchant is None:
        raise HTTPException(status_code=404, detail="Merchant not found")
    return db_merchant

# Create a new transaction
@app.post("/transactions/", response_model=postgreSQL_schemas.Transaction)
def create_transaction(transaction: postgreSQL_schemas.TransactionCreate, db: Session = Depends(get_db)):
    return postgresql_client.create_transaction(db=db, transaction=transaction)

# Update an existing transaction
@app.put("/transactions/{transaction_id}", response_model=postgreSQL_schemas.Transaction)
def update_transaction(transaction_id: int, transaction: postgreSQL_schemas.TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = postgresql_client.update_transaction(db=db, transaction_id=transaction_id, transaction_update=transaction)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction