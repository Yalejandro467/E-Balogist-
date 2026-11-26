
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class MaterialCreate(BaseModel):
    nombre: str
    tipo: str
    cantidad: float
    unidad: str
    precio: float


class MaterialUpdate(BaseModel):
    nombre: str
    tipo: str
    cantidad: float
    unidad: str
    precio: float


class MaterialResponse(BaseModel):
    id_material: UUID
    nombre: str
    tipo: str
    cantidad: float
    unidad: str
    precio: float

    model_config = ConfigDict(from_attributes=True)
