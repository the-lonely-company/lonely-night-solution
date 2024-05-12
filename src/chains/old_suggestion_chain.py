from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from models.api_models import Alcohol
from llms import llm


parser = JsonOutputParser(pydantic_object=Alcohol)

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template='You are alcohol customer service AI. Look at the request, then suggest 1 alcohol only.\n{format_instructions}\nReminder to ALWAYS enclose the json blob with triple backticks only.',
                input_variables=[],
                partial_variables={'format_instructions': parser.get_format_instructions()}
            )
        ),
        MessagesPlaceholder(variable_name='chat_history'),
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template='Request: {content}',
                input_variables=['content']    
            )
        )
    ]
)

suggestion_chain = prompt | llm | parser