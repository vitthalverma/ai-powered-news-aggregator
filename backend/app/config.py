from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_hostname : str
    database_port: str
    database_name: str
    database_username :str
    database_password : str
    secret_key : str
    algorithm : str
    access_token_expiration_minutes : int
    gemini_api_key: str
    news_api_key: str
    
    model_config = SettingsConfigDict(env_file=".env")
        
        
settings = Settings()        
