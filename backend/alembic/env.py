from logging.config import fileConfig

from alembic import context  # pyright: ignore
from sqlalchemy import engine_from_config, pool  # pyright: ignore

from app.core.config import config
from app.core.database import Base

alembic_config = context.config

# Safely set up logging
if alembic_config.config_file_name is not None:
    fileConfig(alembic_config.config_file_name)

# Set the database URL from config
alembic_config.set_main_option("sqlalchemy.url", config.database_url)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (non-database operations)."""
    url = alembic_config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode (with database connection)."""
    connectable = engine_from_config(
        alembic_config.get_section(alembic_config.config_ini_section), # type: ignore[attr-defined]
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,  # type: ignore[attr-defined]
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


# Execute migrations based on context
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
