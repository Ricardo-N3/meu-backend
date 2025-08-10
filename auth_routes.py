from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependecies import take_session, verification_token
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from eschemas import schema_user, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def token_create(id_user,duration_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    trial_date = datetime.now(timezone.utc) + duration_token
    dic_info = {"sub": str(id_user), "exp": trial_date}
    encoded_jwt = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def user_authenticate(email,passwords,session):
    user = session.query(User).filter(User.email==email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(passwords, user.passwords):
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
        encrypted_passwords = bcrypt_context.hash(schema_user_data.passwords)
        new_user = User(schema_user_data.name, schema_user_data.email, encrypted_passwords, schema_user_data.active, schema_user_data.admin)
        session.add(new_user)
        session.commit()
        return {"Message":f"User Registered Successfully {schema_user_data.email}"}
    
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(take_session)):
    user = user_authenticate(login_schema.email, login_schema.passwords, session)
    if not user:
        raise HTTPException(status_code=400, detail="User not founded or invalid credentials")
    else:
        access_token = token_create(user.id)
        refresh_token = token_create(user.id, duration_token=timedelta(days=7))

        return {"acess_token":access_token,
                "refresh_token":refresh_token,
                "token_type":"Bearer"
                }

@auth_router.post("/login-form")
async def login_form(form_datas: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(take_session)):
    user = user_authenticate(form_datas.username, form_datas.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="User not founded or invalid credentials")
    else:
        access_token = token_create(user.id)
        return {"acess_token":access_token,
                "token_type":"Bearer"
                }

@auth_router.get("/refresh")
async def use_refresh_token(user: User = Depends(verification_token)):
    access_token = token_create(user.id)
    return{
        "access_token":access_token,
        "token_type":"Bearer"
    }