import os
import threading
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

_SCHEMA = """
CREATE TABLE IF NOT EXISTS materiales (
    id_material TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    tipo TEXT NOT NULL,
    cantidad DOUBLE PRECISION NOT NULL,
    unidad TEXT NOT NULL,
    precio DOUBLE PRECISION NOT NULL
);
CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    tel TEXT NOT NULL,
    direccion TEXT NOT NULL,
    correo TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS compras (
    id_compra TEXT PRIMARY KEY,
    fecha TEXT NOT NULL,
    valor_total DOUBLE PRECISION NOT NULL,
    estado TEXT NOT NULL,
    id_proveedor TEXT NOT NULL REFERENCES proveedores(id_proveedor)
);
"""


class Database:
    """Conexión a PostgreSQL (Neon) con la misma interfaz que la versión SQLite:
    rows(), run() y close(). Usa un pool de conexiones (seguro con los hilos de FastAPI).
    No se conecta al crear el objeto: se conecta en la primera consulta, así un corte
    de internet al arrancar no tumba el servidor."""

    def __init__(self, path: Path | None = None):
        # 'path' se ignora; se conserva para no romper Database(Path("...")).
        url = os.getenv("DATABASE_URL")
        if not url:
            raise RuntimeError("DATABASE_URL no está definida. Revisa el archivo .env")

        self.engine = create_engine(
            url,
            pool_pre_ping=True,   # descarta conexiones muertas (Neon se suspende si no se usa)
            pool_recycle=300,     # renueva conexiones cada 5 minutos
            pool_size=5,
            max_overflow=5,
            connect_args={"connect_timeout": 15},
        )
        self._tablas_listas = False
        self._lock = threading.Lock()

    def _asegurar_tablas(self):
        if self._tablas_listas:
            return
        with self._lock:
            if not self._tablas_listas:
                with self.engine.begin() as conn:
                    conn.exec_driver_sql(_SCHEMA)
                self._tablas_listas = True

    @staticmethod
    def _pg(query: str) -> str:
        # SQLite usa ? como marcador; psycopg2 (PostgreSQL) usa %s
        return query.replace("?", "%s")

    def rows(self, query, values=()):
        self._asegurar_tablas()
        with self.engine.connect() as conn:
            result = conn.exec_driver_sql(self._pg(query), tuple(values))
            return [tuple(r) for r in result.fetchall()]

    def run(self, query, values=()):
        self._asegurar_tablas()
        with self.engine.begin() as conn:  # commit al salir, rollback si hay error
            conn.exec_driver_sql(self._pg(query), tuple(values))

    def close(self):
        self.engine.dispose()


# Instancia única para toda la app: en los routers usa  from crud.database import db
db = Database()