from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db: str = "logo_lens"

    es_host: str = "http://localhost:9200"
    es_index: str = "logos"

    clip_model: str = "openai/clip-vit-base-patch32"

    model_config = {"env_file": ".env"}


settings = Settings()
