from sqlalchemy.orm import Session
from models.database_models import postgresql_schemas
from models import postgresql_model
from connections.postgreSQL.postgresql_connection import engine 
from fastapi import Depends, FastAPI
from connections.postgreSQL.postgresql_connection import global_sql_session

class PostgresqlClient:
    def __init__(self, session: Session):
        self.session = session

    # 1. Get user by user_id
    def get_user(self, user_id: int):
        return self.session.query(postgresql_model.Users).filter(postgresql_model.Users.user_id == user_id).first()

    #  create a user
    def create_user(self, user: postgresql_schemas.UserCreate):
        user = postgresql_model.Users(
            firebase_uid=user.firebase_uid,
            email=user.email,
            name=user.name
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

postgresql_client = PostgresqlClient(global_sql_session)