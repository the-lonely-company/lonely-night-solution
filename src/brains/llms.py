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
