from typing import List

import json
from loguru import logger
from pydantic import parse_obj_as

from brains.llms import llm
from brains.embedding_models import embedding_model
from connections.mongodb.mongodb_client import vector_search, get_beverages_by_query
from models.api_models import AssistantResponse, Stock, InvokeResponse
from agents.prompts import SYS_PROMPT, TEXT_TO_QUERY_PROMPT


class CustomerServiceAssistant():
    def __init__(self):
        self.llm = llm
        self.embedding_model = embedding_model

    def recommend(self, assistant_response: AssistantResponse, messages) -> List[Stock]:
        if assistant_response.inventory_query:
            messages_with_sys = self.format_messages(TEXT_TO_QUERY_PROMPT, messages)
            completion = self.llm.get_completion(messages_with_sys)
            logger.debug(completion)

            query = json.loads(completion)
            stocks = parse_obj_as(List[Stock], get_beverages_by_query(query))

            return stocks

        embedding = embedding_model.embed(f'{assistant_response.preference}, {assistant_response.characteristic}')
        stocks = parse_obj_as(List[Stock], vector_search(embedding))

        return stocks

    def format_output(self, assistant_response: AssistantResponse, messages) -> InvokeResponse:
        if assistant_response.recommend_status:
            recommendation = self.recommend(assistant_response, messages)
        else: 
            recommendation = []

        return InvokeResponse.model_validate(
            {
                'assistant_response': assistant_response,
                'recommendation': recommendation
            }
        )
    
    def format_messages(self, prompt, messages):
        return [
            {'role': 'system', 'content': prompt}
        ] + messages
    
    def respond(self, messages) -> InvokeResponse:
        messages_with_sys = self.format_messages(SYS_PROMPT, messages)
        completion = self.llm.get_completion(messages_with_sys)

        logger.debug(completion)

        assistant_response = AssistantResponse.model_validate(
            json.loads(completion)
        )

        return self.format_output(assistant_response, messages)


customer_service_assistant = CustomerServiceAssistant()
