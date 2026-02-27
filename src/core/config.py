from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    aws_region: str
    portfolio_table: str

    class Config:
        env_file: str = ".env"
        env_file_encoding: str = "utf-8"


settings: Settings = Settings()  # pyright: ignore[reportCallIssue]
