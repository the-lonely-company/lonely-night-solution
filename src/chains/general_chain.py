from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers.string import StrOutputParser

from llms import llm


prompt = ChatPromptTemplate.from_messages(
    [
        (
            'system',
            'You are alcohol customer service AI.'
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        (
            'user',
            '{content}'
        )
    ]
)

general_chain = (
    {
        'content': lambda x: x['content'],
        'chat_history': lambda x: x['chat_history'] if x['chat_history'] else []
    }
    | prompt
    | llm
    | StrOutputParser()
)