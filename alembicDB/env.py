from logging.config import fileConfig
from alembic import context
from sqlalchemy import create_engine, pool

from app.models import Base
from app.config import settings

config = context.config
print("ENV.PY IS RUNNING")


config.set_main_option(
    "sqlalchemy.url",
    f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)
print("ALEMBIC DATABASE URL =", config.get_main_option("sqlalchemy.url"))
if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_online():
    engine = create_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        context.run_migrations()


run_migrations_online()
