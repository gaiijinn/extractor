from pydantic import BaseSettings

class Settings(BaseSettings):
    POSTGRES_DB: str = "citus"
    POSTGRES_USER: str = "citus"
    POSTGRES_PASSWORD: str = "z4peRnZYXSFwjkB"
    POSTGRES_HOST: str = "c-vc-board.sdp7gta73xhnts.postgres.cosmos.azure.com"
    POSTGRES_PORT: int = 5432

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

settings = Settings()