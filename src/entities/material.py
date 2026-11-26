
import uuid

from sqlalchemy import Column, String, Numeric
from sqlalchemy.dialects.postgresql import UUID

from src.database.connection import AuditModel


class Material(AuditModel):
    __tablename__ = "materiales"

    id_material = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    nombre = Column(String(100), nullable=False)
    tipo = Column(String(80), nullable=False)
    cantidad = Column(Numeric(12, 2), nullable=False, default=0)
    unidad = Column(String(30), nullable=False)
    precio = Column(Numeric(12, 2), nullable=False, default=0)

    def __repr__(self):
        return (
            f"Material(ID: {self.id_material}, "
            f"Nombre: {self.nombre})"
        )
