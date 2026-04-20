from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_host: str = Field(default="0.0.0.0", alias="APP_HOST")
    app_port: int = Field(default=8000, alias="APP_PORT")
    cors_origins: list[str] = Field(default=["*"], alias="CORS_ORIGINS")

    postgres_user: str = Field(default="upvearth", alias="POSTGRES_USER")
    postgres_password: str = Field(default="upvearth", alias="POSTGRES_PASSWORD")
    postgres_db: str = Field(default="upvearth", alias="POSTGRES_DB")
    postgres_host: str = Field(default="db", alias="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, alias="POSTGRES_PORT")

    max_upload_size_mb: int = Field(default=30, alias="MAX_UPLOAD_SIZE_MB")
    upload_dir: str = Field(default="/app/data/uploads", alias="UPLOAD_DIR")

    embeddings_model_name: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        alias="EMBEDDINGS_MODEL_NAME",
    )
    pb_reference_csv: str = Field(
        default="/app/corpus_PB/data/pb_reference.csv",
        alias="PB_REFERENCE_CSV",
    )
    pb_top_k: int = Field(default=3, alias="PB_TOP_K")

    llm_enabled: bool = Field(default=True, alias="LLM_ENABLED")
    ollama_url: str = Field(default="http://127.0.0.1:11434/api/generate", alias="OLLAMA_URL")
    ollama_model_name: str = Field(default="gemma4:26b", alias="OLLAMA_MODEL_NAME")
    llm_temperature: float = Field(default=0.0, alias="LLM_TEMPERATURE")
    database_url_override: str | None = Field(default=None, alias="DATABASE_URL")

    @property
    def database_url(self) -> str:
        if self.database_url_override:
            return self.database_url_override
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
