from typing import List

from loguru import logger

from langchain_core.messages import AIMessage, HumanMessage
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

from fastapi.middleware.cors import CORSMiddleware

from chains.whisky_chain import whisky_chain
from models.request_models import Message, Turn


app = FastAPI(
    title='Alcohol Backend'
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def gen(content: str, chat_history: List) -> str:
    for chunk in whisky_chain.stream({"input": content, "chat_history": chat_history}):
        yield chunk


def convert_to_langchain_message(turn: Turn):
    if turn.party == 'ai':
        return AIMessage(content=turn.content)
    
    return HumanMessage(content=turn.content)


@app.post("/stream")
def stream(message: Message, request: Request):
    content = message.content
    chat_history = [
        convert_to_langchain_message(turn)
        for turn in message.chat_history
    ]

    logger.info(request.headers)

    gen_init = gen(message.content, chat_history)

    return StreamingResponse(gen_init, media_type="text/event-stream")

@app.post("/invoke", response_model=str)
def invoke(message: Message, request: Request) -> str:
    content = message.content
    chat_history = [
        convert_to_langchain_message(turn)
        for turn in message.chat_history
    ]

    logger.info(request.headers)

    return whisky_chain.invoke({'input': content, 'chat_history': chat_history})
