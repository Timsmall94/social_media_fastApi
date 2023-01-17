from pydantic import BaseSettings


class Setting(BaseSettings):
    database_hostname:str
    database_port:str
    database_password:str
    database_name:str
    database_username:str
    secret_key:str
    algorithm:str
    access_token_expire_minutes:int

    class Config:
        env_file= ".env" #how to tell pydantic to import value from .env

setting = Setting()