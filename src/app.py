from typing import List

from loguru import logger

from langchain_core.messages import AIMessage, HumanMessage
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

from chains.whisky_chain import whisky_chain

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

class Message(BaseModel):
    content: str
    chat_history: List


def gen(content: str, chat_history: List) -> str:
    logger.debug(content)
    logger.debug(chat_history)
    for chunk in whisky_chain.stream({"input": content, "chat_history": chat_history}):
        logger.debug(chunk, end='')
        yield chunk


@app.post("/stream")
def stream(message: Message):
    content = message.content
    chat_history = message.chat_history
    gen_init = gen(message.content, chat_history)

    return StreamingResponse(gen_init, media_type="text/event-stream")
