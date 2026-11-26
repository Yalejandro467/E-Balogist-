
import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.connection import AuditModel


class Proveedor(AuditModel):
    __tablename__ = "proveedores"

    id_proveedor = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    nombre = Column(String(100), nullable=False)
    tel = Column(String(30), nullable=False)
    direccion = Column(String(150), nullable=False)
    correo = Column(String(120), nullable=False)

    compras = relationship(
        "Compra",
        back_populates="proveedor",
    )

    def __repr__(self):
        return (
            f"Proveedor(ID: {self.id_proveedor}, "
            f"Nombre: {self.nombre})"
        )
