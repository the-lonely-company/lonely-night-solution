from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from models.database_models.postgresql_model import User
from models.account_model import UserDetail
from connections.postgresqldb.postgresql_connection import global_sql_session


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
        try:
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user
        except Exception as e:
            self.session.rollback()
            raise e

postgresql_client = PostgresqlClient(global_sql_session)