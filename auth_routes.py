from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependecies import take_session
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from eschemas import schema_user, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def token_create(user_id):
    trial_date = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dic_info = {"sub": user_id, "exp": trial_date}
    encoded_jwt = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return encoded_jwt

def user_authenticate(email,password,session):
    user = session.query(User).filter(User.email==email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(password, user.password):
        return False
    return user

@auth_router.get("/")
async def auths():
    return {"Message": "You have accessed the default authentication route"}

@auth_router.post("/acount_create")
async def acount_create(schema_user_data: schema_user, session: Session = Depends(take_session)):
    user = session.query(User).filter(User.email==schema_user_data.email).first()
    if user:
        raise HTTPException(status_code=400,detail="There is Already a User With This Email")
    else:
        encrypted_password = bcrypt_context.hash(schema_user_data.password)
        new_user = User(schema_user_data.name, schema_user_data.email, encrypted_password, schema_user_data.active, schema_user_data.admin)
        session.add(new_user)
        session.commit()
        return {"Message":f"User Registered Successfully {schema_user_data.email}"}
    
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(take_session)):
    user = user_authenticate(login_schema.email, login_schema.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="User not founded or invalid credentials")
    else:
        acess_token = token_create(user.id)
        return {"acess_token":acess_token,
                "token_type":"Bearer"
                }