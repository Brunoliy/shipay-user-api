# pylint: skip-file
# flake8: noqa
import sys
from logging.config import fileConfig

from alembic import context
from environs import Env
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

sys.path.append("./src")

from interface_adapters.data.models.base import Model

config = context.config
env = Env()
env.read_env()

section = config.config_ini_section

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Model.metadata


def get_db_uri() -> URL:
    return URL.create(
        drivername="postgresql",
        username=env.str("DB_USER", "postgres"),
        password=env.str("DB_PASSWORD", "postgres"),
        host=env.str("DB_HOST", "localhost"),
        port=env.str("DB_PORT", "5435"),
        database=env.str("DB_DATABASE", "shipay_users_db"),
    )


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_db_uri()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    url = get_db_uri()
    connectable = create_engine(url)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
