from fastapi import APIRouter
from typing import List

from search_engine.search_engine_impl import search_engine
from model.search_engine_model import Message, SearchEngineResponse


search_engine_router = APIRouter(
    prefix='/search-engine',
    tags=['Search Engine']
)


@search_engine_router.post("/query", response_model=SearchEngineResponse)
async def query(messages: List[Message]) -> SearchEngineResponse:
    return search_engine.respond(messages)
