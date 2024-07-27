from sqlalchemy.orm import Session
from models.database_models import postgreSQL_schemas
from models import postgresql_model
from connections.postgreSQL.postgresql_connection import SessionLocal, engine
from fastapi import Depends, FastAPI

class PostgresqlClient:
    def __init__(self):
        pass

    def get_db(self):
        db_session = SessionLocal()
        try:
            yield db_session
        finally:
            db_session.close()

    # 1. Get user by user_id
    def get_user(self, user_id: int, session: Session = Depends(get_db)):
        return session.query(postgresql_model.User).filter(postgresql_model.User.user_id == user_id).first()

postgresqlClient = PostgresqlClient()