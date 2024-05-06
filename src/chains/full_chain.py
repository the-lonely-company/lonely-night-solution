from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers.string import StrOutputParser

from chains.utils import route
from llms import llm


gate_chain = (
    PromptTemplate.from_template(
        'Given the user query content below, classify it as either being about `alcohol suggestion` or `Other`. Do not respond with more than two words.\n{chat_history}\n{content}'
    )
    | llm
    | StrOutputParser()
)

full_chain = (
    {
        'topic': gate_chain,
        'content': lambda x: x['content'],
        'chat_history': lambda x: x['chat_history']
    }
    | RunnableLambda (route)
)