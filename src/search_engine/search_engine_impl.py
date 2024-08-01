from typing import List, Dict, Any, Callable

import json
from loguru import logger
from pydantic import parse_obj_as

from brain.llm import llm
from brain.embedding_model import embedding_model
from connection.mongodb.mongodb_client import beverage_resource
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
        self.beverage_resource = beverage_resource

    @add_sys_prompt(FIRST_LAYER_PROMPT)
    def first_layer(self, messages: List[Message]):
        response = self.llm.invoke(messages)

        logger.info(response)

        wine_profile = WineProfile.model_validate_json(response)

        return wine_profile
    
    def second_layer(self, sys_prompt, detail_as_json):
        messages_with_sys = [
            {
                'role': 'system', 
                'content': sys_prompt
            },
            {
                'role': 'user',
                'content': detail_as_json
            }
        ]
        response = self.llm.invoke(messages_with_sys)

        return json.loads(response)
    
    def construct_beverage_references(self, wine_profile_detail):
        feature_mapping = {
            'grapes': 'grape',
            'regions': 'region',
            'wineries': 'winery'
        }

        beverage_references = []
        selected_features = []
        for feature, singular in feature_mapping.items():
            feature_value = getattr(wine_profile_detail, feature)
            if feature_value is not None:
                selected_features.extend([{singular: value} for value in feature_value])

        if selected_features:
            selected_features_json = [json.dumps(feature) for feature in selected_features]

            logger.info(selected_features_json)

            meta_embedding = self.embedding_model.embed(selected_features_json)

            matches = []
            for e in meta_embedding:
                matches.extend(self.beverage_resource.meta_vector_search(e['embedding']))

            beverage_references += matches

        [logger.info(b_r) for b_r in beverage_references]

        return beverage_references

    def construct_second_layer_prompt(self, beverage_references: List[Dict[str, Any]]):
        updated_second_layer_prompt = SECOND_LAYER_PROMPT

        for reference in beverage_references:
            reference_json = json.dumps(reference)

            logger.info(reference_json)

            updated_second_layer_prompt += f"\n{reference_json}\n"

        logger.info(updated_second_layer_prompt)

        return updated_second_layer_prompt
    
    def get_relavent_wine_detaiL(self, wine_profile_detail):
        detail_as_dict = {k: v for k, v in wine_profile_detail.dict().items() if v is not None and k != 'price' and k != 'description' and k != 'quantity'}
        logger.info(detail_as_dict)

        return detail_as_dict
    
    def respond(self, messages: List[Message]):
        wine_profile = self.first_layer(messages)

        wine_profile_detail = wine_profile.detail

        beverage_references = self.construct_beverage_references(wine_profile_detail)

        updated_second_layer_prompt = self.construct_second_layer_prompt(beverage_references)

        detail_as_dict = self.get_relavent_wine_detaiL(wine_profile_detail)

        detail_sentence = "The wine profile details are: "
        for key, value in detail_as_dict.items():
            detail_sentence += f"The {key} is {value}, "
        detail_sentence = detail_sentence.rstrip(', ') + "."
        logger.info(detail_sentence)

        beverage_query = self.second_layer(updated_second_layer_prompt, detail_sentence)

        logger.info(beverage_query)

        description_embedding = self.embedding_model.embed(wine_profile_detail.description)[0]['embedding']

        matched_beverages = self.beverage_resource.get_matched_beverages(beverage_query, description_embedding, 4)

        return matched_beverages


search_engine = SearchEngineImpl()