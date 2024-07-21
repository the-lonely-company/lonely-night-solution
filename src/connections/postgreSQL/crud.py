from sqlalchemy.orm import Session
from models.database_models import postgreSQL_schemas

from models import postgreSQL_model

# 1. Get user by user_id
def get_user(db: Session, user_id: str):
    return db.query(postgreSQL_model.User).filter(postgreSQL_model.User.user_id == user_id).first()

# 2. Create user
def create_user(db: Session, user: postgreSQL_schemas.UserCreate):
    db_user = postgreSQL_model.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 3. Update user
def update_user(db: Session, user_id: str, user_update: postgreSQL_schemas.UserCreate):
    db_user = db.query(postgreSQL_model.User).filter(postgreSQL_model.User.user_id == user_id).first()
    if db_user:
        for key, value in user_update.dict().items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

# 4. Create merchant
def create_merchant(db: Session, merchant: postgreSQL_schemas.MerchantCreate):
    db_merchant = postgreSQL_model.Merchant(**merchant.dict())
    db.add(db_merchant)
    db.commit()
    db.refresh(db_merchant)
    return db_merchant

# 5. Update merchant
def update_merchant(db: Session, merchant_id: str, merchant_update: postgreSQL_schemas.MerchantCreate):
    db_merchant = db.query(postgreSQL_model.Merchant).filter(postgreSQL_model.Merchant.merchant_id == merchant_id).first()
    if db_merchant:
        for key, value in merchant_update.dict().items():
            setattr(db_merchant, key, value)
        db.commit()
        db.refresh(db_merchant)
    return db_merchant

# 6. Create transaction
def create_transaction(db: Session, transaction: postgreSQL_schemas.TransactionCreate):
    db_transaction = postgreSQL_model.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# 7. Update transaction
def update_transaction(db: Session, transaction_id: int, transaction_update: postgreSQL_schemas.TransactionCreate):
    db_transaction = db.query(postgreSQL_model.Transaction).filter(postgreSQL_model.Transaction.id == transaction_id).first()
    if db_transaction:
        for key, value in transaction_update.dict().items():
            setattr(db_transaction, key, value)
        db.commit()
        db.refresh(db_transaction)
    return db_transaction