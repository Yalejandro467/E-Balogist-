
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class ProveedorCreate(BaseModel):
    nombre: str
    tel: str
    direccion: str
    correo: str


class ProveedorUpdate(BaseModel):
    nombre: str
    tel: str
    direccion: str
    correo: str


class ProveedorResponse(BaseModel):
    id_proveedor: UUID
    nombre: str
    tel: str
    direccion: str
    correo: str

    model_config = ConfigDict(from_attributes=True)
