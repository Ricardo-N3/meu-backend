from models import User, db
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from main import SECRET_KEY, ALGORITHM, oauth2_schema

def take_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()

        yield session
    finally:
        session.close()

def verification_token(token: str = Depends(oauth2_schema), session: Session = Depends(take_session)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = int(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Access Denied, please check the validity of the token")
    user = session.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Access")
    return user