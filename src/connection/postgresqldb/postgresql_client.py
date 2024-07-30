from sqlalchemy.orm import Session
from model.database_model.postgresql_model import User
from model.account_model import UserDetail
from connection.postgresqldb.postgresql_connection import global_sql_session


class PostgresqlClient:
    def __init__(self, session: Session):
        self.session = session

    # 1. Get user by user_id
    def get_user(self, user_id: int):
        return self.session.query(User).filter(User.user_id == user_id).first()

    #  create a user
    def create_user(self, detail: UserDetail):
        user = User(
            firebase_uid=detail.firebase_uid,
            email=detail.email,
            name=detail.name
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

postgresql_client = PostgresqlClient(global_sql_session)