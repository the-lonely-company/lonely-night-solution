from langchain_groq import ChatGroq
from groq import Groq


llm_client = ChatGroq(
    temperature=1, 
    groq_api_key="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",
    model_name="llama3-70b-8192"
)

groq_client = Groq(
    api_key='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'
)


class LLM:
    def __init__(self):
        self.llm_client = groq_client
        self.llm = 'llama3-70b-8192'        

    def get_completion(self, messages):
        response = self.llm_client.chat.completions.create(
            model=self.llm,
            messages=messages,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            response_format={"type": "json_object"},
            stop=None,
        )
    
        return response.choices[0].message.content

llm = LLM()
