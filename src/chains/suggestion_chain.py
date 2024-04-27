from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from models.api_models import Alcohol
from llms import llm


parser = JsonOutputParser(pydantic_object=Alcohol)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            'system',
            'You are alcohol customer service AI.'
        ),
        MessagesPlaceholder(variable_name='chat_history'),
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template='{format_instructions}\n{content}',
                input_variables=['content'],
                partial_variables={'format_instructions': parser.get_format_instructions()}    
            )
        )
    ]
)

suggestion_chain = prompt | llm | parser