from langchain_groq import ChatGroq


llm = ChatGroq(
    temperature=1, 
    groq_api_key="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",
    model_name="llama3-70b-8192"
)