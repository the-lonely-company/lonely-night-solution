from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
# from models.postgresql_model import User
from models.database_models.postgreSQL_schemas import User
from connections.postgreSQL.postgresql_client import postgresqlClient
from connections.postgreSQL.postgresql_connection import SessionLocal


account_router = APIRouter(
    prefix='/account',
    tags=['Account']
)

def get_db():
        db_session = SessionLocal()
        try:
            yield db_session
        finally:
            db_session.close()

@account_router.get('/get_user', response_model=User)
async def get_user(user_id: int, session: Session = Depends(get_db)) -> User:
    db_user = postgresqlClient.get_user(user_id=user_id, session=session)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
