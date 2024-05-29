import json
from loguru import logger

from brains.llms import groq_client
from brains.embedding_models import embedding_model
from connections.mongodb.mongodb_client import vector_search
from models.api_models import AssistantResponse
from agents.prompts import SYS_PROMPT


class CustomerServiceAssistant():
    def __init__(self):
        self.llm_client = groq_client
        self.llm = 'llama3-70b-8192'
        self.embedding_model = embedding_model
        self.system_prompt = SYS_PROMPT
        self.messages = [
            {'role': 'system', 'content': self.system_prompt}
        ]

    def recommend(self, assistant_response: AssistantResponse):
        # if assistant_response.price_negotiating:
        #     return f'CARD INFO about {assistant_response.preference} PRICE {assistant_response.budget}'
            
        embedding = embedding_model.embed(assistant_response.characteristic)
        recommendation = vector_search(embedding)

        return recommendation

    def format_output(self, assistant_response: AssistantResponse):
        if assistant_response.recommend_status:
            return assistant_response.content, self.recommend(assistant_response)

        return assistant_response.content
    
    def get_completion(self, messages):
        response = self.llm_client.chat.completions.create(
            model=self.llm,
            messages=self.messages + messages,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            response_format={"type": "json_object"},
            stop=None,
        )
    
        return response.choices[0].message.content

    def respond(self, messages):
        completion = self.get_completion(messages)

        assistant_response = AssistantResponse.model_validate(
            json.loads(completion)
        )

        logger.debug(assistant_response)

        return self.format_output(assistant_response)


customer_service_assistant = CustomerServiceAssistant()
