# Night Solution

An AI-powered wine recommendation REST API built with FastAPI. Users describe what they are looking for (a mood, a meal, a taste preference) and the engine returns personalised wine suggestions with human-readable explanations.

## How it works

Recommendations are produced by a three-layer pipeline:

1. **Query understanding** – A Groq LLM (llama3-70b-8192) parses the natural-language query and extracts a structured wine profile (type, grape, region, price range, etc.).
2. **Semantic search** – Jina AI embeddings and MongoDB Atlas vector search retrieve the closest matching wines from the catalogue.
3. **Explanation generation** – The LLM produces a markdown explanation of why each wine fits the request.

## Endpoints

| Router | Path | Description |
|--------|------|-------------|
| Search Engine | `POST /search-engine/query` | AI-powered wine recommendations |
| Beverage | `GET /beverage/get-beverage` | Fetch wine details by ID |
| Account | `GET /account/get_user` | Get user profile |
| Account | `POST /account/create_user` | Create user account |
| Document | `GET /document/terms-and-conditions` | Terms and conditions |

## Tech stack

- **Framework**: FastAPI + uvicorn (port 8081)
- **LLM**: Groq API (llama3-70b-8192) via LangChain
- **Embeddings**: Jina AI (jina-embeddings-v2-base-en)
- **Wine catalogue**: MongoDB Atlas (vector search)
- **User accounts**: PostgreSQL via SQLAlchemy + Alembic

## Start the app

```bash
cd src
uvicorn app:app --host 0.0.0.0 --port 8081
```

## External dependencies

- MongoDB Atlas: https://cloud.mongodb.com/
- LangChain Smith: https://smith.langchain.com/

