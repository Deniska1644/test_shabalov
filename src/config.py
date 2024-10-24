from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    PG_USER: str
    PG_PASS: str
    PG_HOST: str
    PG_PORT: str
    PG_BASE: str

    REDIS_HOST: str
    REDIS_PORT: str

    SECRET_KEY: str
    ALGORITM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(env_file='../.env')

    def get_pg_dns(self):
        return f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASS}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_BASE}"


setting = Setting()
