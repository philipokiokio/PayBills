from core.config import settings
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from core.user_auth.schemas import TokenData
from core.utils.database_utils import get_db
from sqlalchemy.orm import Session
from core.user_auth.models import User
from fastapi.security import OAuth2PasswordBearer



oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "auth/login/")





secret_key =  settings.secret_key
algorithm_ = settings.algorithm
access_token_expire_minutes = settings.access_token_expire_minutes
refresh_token_expire_minutes = 60 * 24 * 7
refresh_token_secret_key = settings.refresh_secret_key


def create_access_token(data:dict):
    
    
    
    to_encode = data.copy()
    expire = timedelta(minutes=access_token_expire_minutes) + datetime.utcnow()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm_)
    return encoded_jwt

def create_refresh_token(data:dict):
    to_encode = data.copy()
    expire = timedelta(minutes=refresh_token_expire_minutes) + datetime.utcnow()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, refresh_token_secret_key, algorithm=algorithm_)
    return encoded_jwt

    
    

    
    
def verify_access_token(token:str, credential_exception):

    try:
        payload = jwt.decode(token, secret_key, algorithms=algorithm_)

        id:str = payload.get("id")
        if id is None:
            raise credential_exception
        token_data = TokenData(id=id)
    except JWTError:
        raise credential_exception

    return token_data

    


def get_current_user(token:str=Depends(oauth2_scheme), db:Session = Depends(get_db)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}        
    )
    token = verify_access_token(token, credentials_exception)
    user=  db.query(User).filter(User.id == token.id).first()
    return user

    