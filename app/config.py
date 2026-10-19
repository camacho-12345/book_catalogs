import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuracion centralizada de la aplicacion compatible con Vercel y MongoDB Atlas / Storage."""
    APP_NAME: str = "Catalogo de Libros API"
    APP_ENV: str = os.getenv("APP_ENV", "production")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")

    # MongoDB Atlas / Vercel Storage
    # Soporta multiples aliases (MONGODB_URI es el inyectado automaticamente por Vercel)
    MONGODB_URL: str = (
        os.getenv("MONGODB_URI")
        or os.getenv("MONGODB_URL")
        or os.getenv("MONGO_URI")
        or os.getenv("DATABASE_URL")
        or "mongodb://localhost:27017"
    )
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "catalogo_libros_db")
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "libros")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
