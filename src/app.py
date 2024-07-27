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
from routers.document import document_router
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
app.include_router(document_router)


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
