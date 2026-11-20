from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.config import settings
from app.database import Base
from app.models import usuario, mascota, veterinaria, recordatorio, producto, resena, mensaje # Importamos los modelos para que Alembic los detecte

# Importamos los modelos aquí para que Alembic los detecte.
# Por ahora no hay ninguno (los iremos agregando en cada fase),
# pero dejamos el import preparado como referencia:
# from app.models import usuario, mascota, veterinaria, ...

# Objeto de configuración de Alembic (lee alembic.ini)
config = context.config

# Inyectamos la URL real de la base de datos desde nuestro settings,
# en vez de dejarla escrita en alembic.ini
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Configuración de logging de Alembic
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata de nuestros modelos (Alembic la usa para autogenerar migraciones)
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Ejecuta migraciones en modo 'offline' (genera SQL sin conectarse a la DB)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecuta migraciones en modo 'online' (conectado directamente a la DB)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()