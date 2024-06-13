from langchain_groq import ChatGroq
from groq import Groq


llm = ChatGroq(
    temperature=1, 
    groq_api_key="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",
    model_name="llama3-70b-8192"
)

groq_client = Groq(
    api_key='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'
)
