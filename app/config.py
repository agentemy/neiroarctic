from dataclasses import dataclass
from environs import Env

@dataclass
class DatabaseConfig:
    database_url: str
    db_user: str
    db_pass: str
    db_host: str
    db_port: str
    db_name: str


@dataclass
class Config:
    db: DatabaseConfig
    debug: bool



def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)  # Загружаем переменные окружения из файла .env

    db_conf = DatabaseConfig(
        database_url=env("DATABASE_URL"),
        db_user=env("DB_USER"),
        db_pass=env("DB_PASSWORD"),
        db_host=env("DB_HOST"),
        db_port=env("DB_PORT"),
        db_name=env("DB_NAME")
    )

    return Config(
        db=db_conf,
        debug=env.bool("DEBUG", default=True),
    )