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

postgresqlClient = PostgresqlClient(global_sql_session)