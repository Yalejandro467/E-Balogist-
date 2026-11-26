
import uuid
from datetime import date

from sqlalchemy import Column, Date, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.connection import AuditModel


class Compra(AuditModel):
    __tablename__ = "compras"

    id_compra = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    fecha = Column(Date, nullable=False, default=date.today)
    valor_total = Column(Numeric(12, 2), nullable=False, default=0)
    estado = Column(String(30), nullable=False, default="Pendiente")

    id_proveedor = Column(
        UUID(as_uuid=True),
        ForeignKey("proveedores.id_proveedor"),
        nullable=False,
    )

    proveedor = relationship(
        "Proveedor",
        back_populates="compras",
    )

    def __repr__(self):
        return (
            f"Compra(ID: {self.id_compra}, "
            f"Estado: {self.estado}, "
            f"Total: {self.valor_total})"
        )
