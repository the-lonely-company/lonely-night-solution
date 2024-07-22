from sqlalchemy.orm import Session
from models.database_models import postgreSQL_schemas
from models import postgreSQL_model
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
    def get_user(self, user_id: str, session: Session = Depends(get_db)):
        return session.query(postgreSQL_model.User).filter(postgreSQL_model.User.user_id == user_id).first()

    # # 2. Create user
    # def create_user(self, user: postgreSQL_schemas.UserCreate):
    #     db_user = postgreSQL_model.User(**user.dict())
    #     self.session.add(db_user)
    #     self.session.commit()
    #     self.session.refresh(db_user)
    #     return db_user

    # # 3. Update user
    # def update_user(self, user_id: str, user_update: postgreSQL_schemas.UserCreate):
    #     db_user = self.session.query(postgreSQL_model.User).filter(postgreSQL_model.User.user_id == user_id).first()
    #     if db_user:
    #         for key, value in user_update.dict().items():
    #             setattr(db_user, key, value)
    #         self.session.commit()
    #         self.session.refresh(db_user)
    #     return db_user

    # # 4. Create merchant
    # def create_merchant(self, merchant: postgreSQL_schemas.MerchantCreate):
    #     db_merchant = postgreSQL_model.Merchant(**merchant.dict())
    #     self.session.add(db_merchant)
    #     self.session.commit()
    #     self.session.refresh(db_merchant)
    #     return db_merchant

    # # 5. Update merchant
    # def update_merchant(self, merchant_id: str, merchant_update: postgreSQL_schemas.MerchantCreate):
    #     db_merchant = self.session.query(postgreSQL_model.Merchant).filter(postgreSQL_model.Merchant.merchant_id == merchant_id).first()
    #     if db_merchant:
    #         for key, value in merchant_update.dict().items():
    #             setattr(db_merchant, key, value)
    #         self.session.commit()
    #         self.session.refresh(db_merchant)
    #     return db_merchant

    # # 6. Create transaction
    # def create_transaction(self, transaction: postgreSQL_schemas.TransactionCreate):
    #     db_transaction = postgreSQL_model.Transaction(**transaction.dict())
    #     self.session.add(db_transaction)
    #     self.session.commit()
    #     self.session.refresh(db_transaction)
    #     return db_transaction

    # # 7. Update transaction
    # def update_transaction(self, transaction_id: int, transaction_update: postgreSQL_schemas.TransactionCreate):
    #     db_transaction = self.session.query(postgreSQL_model.Transaction).filter(postgreSQL_model.Transaction.id == transaction_id).first()
    #     if db_transaction:
    #         for key, value in transaction_update.dict().items():
    #             setattr(db_transaction, key, value)
    #         self.session.commit()
    #         self.session.refresh(db_transaction)
    #     return db_transaction