from fastapi import APIRouter, HTTPException, Depends
from pydantic import ValidationError, IntegrityError
from loguru import logger

from models.account_model import User, UserDetail
from connections.postgresqldb.postgresql_client import postgresql_client


account_router = APIRouter(
    prefix='/account',
    tags=['Account']
)

@account_router.get('/get_user', response_model=User)
async def get_user(user_id: int) -> User:
    user = postgresql_client.get_user(user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@account_router.post('/create_user', response_model=User)
async def create_user(detail: UserDetail) -> User:
    try:
        user = postgresql_client.create_user(detail)
        return user
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=422, detail="Invalid input data.")
    except IntegrityError as e:
        logger.error(f"Integrity error: {e}")
        raise HTTPException(status_code=409, detail="A user with this email already exists.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the user.")