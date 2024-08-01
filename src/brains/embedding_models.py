import requests


class EmbeddingModel:
    def __init__(self) -> None:
        self.model = 'jina-embeddings-v2-base-en'
        self.authorization = 'Bearer jina_68bf5c2948544e35a150c76ee3642c7bFPBrLd_G2FJySxMDdnuSmY8KmbdF'

    def embed(self, text):
        url = 'https://api.jina.ai/v1/embeddings'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': self.authorization
        }

        payload = {
            'input': text,
            'model': self.model,
            'encoding_type': 'float'
        }

        response = requests.post(url, headers=headers, json=payload)

        return response.json()['data'][0]['embedding']


embedding_model = EmbeddingModel()
