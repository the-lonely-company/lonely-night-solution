from fastapi import APIRouter, HTTPException, Depends
from models.database_models.postgresql_schemas import User, UserCreate
from connections.postgreSQL.postgresql_client import postgresql_client


account_router = APIRouter(
    prefix='/account',
    tags=['Account']
)

@account_router.get('/get_user', response_model=User)
async def get_user(user_id: int) -> User:
    db_user = postgresql_client.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@account_router.post('/create_user', response_model=User)
async def create_user(user: UserCreate) -> User:
    db_user = postgresql_client.create_user(user)
    return db_user