from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    ENV_STATE: str | None = "dev"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class GlobalConfig(BaseConfig):
    DATABASE_HOSTNAME: str | None = None
    DATABASE_USERNAME: str | None = None
    DATABASE_PASSWORD: str | None = None
    DATABASE_NAME: str | None = None
    DATABASE_PORT: str | None = None
    DATABASE_URL: str | None = None
    DEBUG: bool = False
    DB_FORCE_ROLL_BACK: bool = False
    SECRET_KEY: str | None = None
    ALGORITHM: str | None = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int | None = None


class DevConfig(GlobalConfig):
    DEBUG: bool = True
    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=True, extra="ignore"
    )


class TestConfig(GlobalConfig):
    # DATABASE_URL: str = "sqlite:///test_practice.db"
    DB_FORCE_ROLL_BACK: bool = True
    DEBUG: bool = True
    model_config = SettingsConfigDict(env_prefix="TEST_", env_file=".env")


class ProdConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="PROD_", env_file=".env")


def get_settings() -> GlobalConfig:
    base = BaseConfig()
    env_state = (base.ENV_STATE or "dev").lower()
    configs = {"dev": DevConfig, "test": TestConfig, "prod": ProdConfig}
    config_class = configs.get(env_state, DevConfig)
    return config_class()


settings = get_settings()
