from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Vishal's API"
    admin_email: str = "admin@email.com"
    items_per_user: int = 50
    database_url: str
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
app = FastAPI()

@app.get("/info")
async def info():
    return {
        'app_name': settings.app_name,
        'admin_email': settings.admin_email,
        'items_per_user': settings.items_per_user,
    }