import requests


class EmbeddingModel:
    def __init__(self) -> None:
        self.model = 'jina-embeddings-v2-base-en'
        self.authorization = 'Bearer jina_7f7335a14ef948ee97378ec427278824Wo92jaKw5qRvea8b1VYtEK7s7Mjf'

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
