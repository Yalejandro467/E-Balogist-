
from uuid import UUID
from datetime import date
from pydantic import BaseModel, ConfigDict


class CompraCreate(BaseModel):
    fecha: date
    valor_total: float
    estado: str = "Pendiente"
    id_proveedor: UUID


class CompraUpdate(BaseModel):
    fecha: date
    valor_total: float
    estado: str
    id_proveedor: UUID


class CompraResponse(BaseModel):
    id_compra: UUID
    fecha: date
    valor_total: float
    estado: str
    id_proveedor: UUID

    model_config = ConfigDict(from_attributes=True)
