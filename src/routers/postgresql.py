from fastapi import APIRouter, HTTPException
# from models.postgresql_model import User
from models.database_models.postgreSQL_schemas import User
from connections.postgreSQL.postgresql_client import postgresqlClient


account_router = APIRouter(
    prefix='/account',
    tags=['Account']
)


@account_router.get('/get_user', response_model=User)
async def get_user(user_id: str) -> User:
    db_user = postgresqlClient.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
