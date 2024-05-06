from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from models.api_models import WinePreference
from llms import llm


parser = JsonOutputParser(pydantic_object=WinePreference)

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template='Look at the request, classify user preference on wine. Use sweetness, acidity and body aspect to analyse. For sweetness, there are 3 levels, low, medium and high. For acidity, there are 3 levels, low, medium and high. For body, there are 3 levels, light, medium and bold.\n{format_instructions}\nReminder to ALWAYS enclose the json blob with triple backticks only.',
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

db_chain = prompt | llm | parser