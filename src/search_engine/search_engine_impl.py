from typing import List, Callable

import json
from loguru import logger
from pydantic import parse_obj_as

from brain.llm import llm
from brain.embedding_model import embedding_model
from connection.mongodb.mongodb_client import vector_search, get_beverages_by_query
from model.search_engine_model import Message, WineProfile
from search_engine.prompt import FIRST_LAYER_PROMPT, SECOND_LAYER_PROMPT


def add_sys_prompt(prompt: str):
    def decorator(func: Callable):
        def wrapper(self, messages: List[Message]):
            messages_with_sys = [{'role': 'system', 'content': prompt}] + messages
            return func(self, messages_with_sys)
        return wrapper
    return decorator


class SearchEngineImpl:
    def __init__(self):
        self.llm = llm
        self.embedding_model = embedding_model

    @add_sys_prompt(FIRST_LAYER_PROMPT)
    def first_layer(self, messages: List[Message]):
        response = self.llm.invoke(messages)

        wine_profile = WineProfile.model_validate_json(response)

        return wine_profile
    
    @add_sys_prompt(SECOND_LAYER_PROMPT)
    def second_layer(self, profile):
        response = self.llm.invoke(profile)
        return json.loads(response)
    
    # def third_layer(self, profile, matches):
    #     response = self.llm.invoke(profile, matches)
    #     return json.loads(response)
    
    def respond(self, messages: List[Message]):
        wine_profile = self.first_layer(messages)
        second_layer_response = self.second_layer(wine_profile)

        return second_layer_response


search_engine = SearchEngineImpl()
