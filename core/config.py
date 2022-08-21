from pydantic import BaseSettings, EmailStr
from typing import Optional 





class Settings(BaseSettings):
    app_name:str
    environment: Optional[str]
    db_username:str
    db_password:str
    db_hostname:str
    db_port:int
    db_name:str
    db_type:str
    secret_key:str
    algorithm:str
    access_token_expire_minutes:int 
    refresh_secret_key:str
    token_secret_key:str
    frontend_url:str
    

    class Config:
        env_file = '.env'



class MailSettings(BaseSettings):
    mail_username:str
    mail_password: str
    mail_server:str
    mail_port:int
    mail_tls: bool
    mail_ssl:bool
    mail_from:EmailStr
    mail_from_name:str

    class Config:
        env_file = ".env"

















        
settings:Settings = Settings() 
mail_settings = MailSettings()