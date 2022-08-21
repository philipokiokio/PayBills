from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class User(BaseModel):
    email:EmailStr
    username:str
    first_name:str
    last_name:str
    username:str
    phone_number:str
    password:str
    is_verified:bool = False
    # super_user:bool = False
    terms_of_service:bool = False
    # date_joined:datetime
    
    

class TokenData(BaseModel):
    id: Optional[str] = None

    
    

class UserCreate(User):
    pass


class ResponseUser(BaseModel):
    id:int
    email:EmailStr
    username:str
    first_name:str
    last_name:str
    username:str
    is_verified:bool = False
    super_user:bool = False
    terms_of_service:bool = False
    date_joined:datetime

    class Config:
        orm_mode = True

    
class AuthToken(BaseModel):

    refresh_token:str
    data:ResponseUser

    class Config:
        orm_mode = True

class LoginResponse(BaseModel):
    access_token:str
    token_type:str    
    message:str
    data: AuthToken
    status: int
    

class RegistrationResponse(BaseModel):
    message: str
    data: ResponseUser
    status: int

class loginData(BaseModel):
    email: EmailStr
    password: str



#INvites 
# 

class ContractualInvitesCreate(BaseModel):
    email_invited:EmailStr


class UpdateContractualInvites(BaseModel):
    confirmation: bool
    email_invited: EmailStr


class ContractualInviteResponse(BaseModel):
    id: int
    inviter_id: int
    confirmation: bool
    email_invited: EmailStr


    class Config:
        orm_mode = True


class ContractualMessageRespsonse(BaseModel):
    message:str
    data: ContractualInviteResponse
    status: int


class ContractualListMessageRespsonse(BaseModel):
    message:str
    data: List[ContractualInviteResponse]
    status: int    