from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
    
    # DATABASE_HOST: str
    # DATABASE_NAME: str
    # DATABASE_USER: str
    # DATABASE_PASSWORD: str
    # DATABASE_PORT: int
    # app_name: str = "Full Stack To Do App"

    # Configuración de la base de datos con NEON

    DATABASE_URL: str
    app_name: str = "Full Stack To Do App"


    OPENAI_API_KEY: str = None
    