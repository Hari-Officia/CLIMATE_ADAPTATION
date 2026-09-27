import os
from typing import List, Optional
from pydantic import Field, field_validator, ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    ENVIRONMENT: str = Field("development", validation_alias="ENVIRONMENT")
    DEBUG: bool = Field(True, validation_alias="DEBUG")
    SECRET_KEY: str = Field("DEV_SECRET_KEY_FOR_LOCAL_TESTING_ONLY_32_CHARS", validation_alias="SECRET_KEY")
    
    # Infrastructure
    DATABASE_URL: str = Field("postgresql+psycopg://postgres:postgres@localhost:5432/climate_platform", validation_alias="DATABASE_URL")
    CHROMA_PERSIST_DIR: str = Field("knowledge_base/chroma", validation_alias="CHROMA_PERSIST_DIR")
    
    # Auth & CORS
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60, validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    ALLOWED_CORS_ORIGINS: str = Field("*", validation_alias="ALLOWED_CORS_ORIGINS")
    
    # Feature Flags
    ENABLE_QAOA: bool = Field(True, validation_alias="ENABLE_QAOA")
    ENABLE_LLM_EXPLANATIONS: bool = Field(True, validation_alias="ENABLE_LLM_EXPLANATIONS")
    ENABLE_RAG_EVIDENCE: bool = Field(True, validation_alias="ENABLE_RAG_EVIDENCE")
    
    # Logging
    LOG_LEVEL: str = Field("INFO", validation_alias="LOG_LEVEL")
    LOG_FORMAT: str = Field("JSON", validation_alias="LOG_FORMAT")


    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key_length(cls, v: str, info: ValidationInfo) -> str:
        env = info.data.get("ENVIRONMENT", "development")
        if env == "production" and (not v or len(v) < 32 or "DEV_" in v):
            raise ValueError("Production SECRET_KEY must be a secure random string of at least 32 characters.")
        return v

    @field_validator("DEBUG")
    @classmethod
    def validate_debug_in_production(cls, v: bool, info: ValidationInfo) -> bool:
        env = info.data.get("ENVIRONMENT", "development")
        if env == "production" and v is True:
            raise ValueError("DEBUG mode cannot be True in production environment.")
        return v

settings = Settings()

