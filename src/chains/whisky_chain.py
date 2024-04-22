from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers.string import StrOutputParser


llm = ChatGroq(
    temperature=0, 
    groq_api_key="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",
    model_name="mixtral-8x7b-32768"
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            'system',
            'You are an expert at alcohol.'
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        (
            'user',
            '{input}'
        )
    ]
)

whisky_chain = (
    {
        'input': lambda x: x['input'],
        'chat_history': lambda x: x['chat_history']
    }
    | prompt
    | llm
    | StrOutputParser()
)
