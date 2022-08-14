from curses import use_env
from pydantic import BaseSettings
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
    

    class Config:
        env_file = '.env'
























        
settings:Settings = Settings() 
# print(settings)       