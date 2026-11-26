
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from src.crud.proveedor_crud import ProveedorCRUD
from src.schemas.proveedor import (
    ProveedorCreate,
    ProveedorUpdate,
    ProveedorResponse
)

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])

proveedor_crud = ProveedorCRUD()


@router.get("/", response_model=list[ProveedorResponse])
def listar_proveedores():
    return proveedor_crud.listar()


@router.get("/{id_proveedor}", response_model=ProveedorResponse)
def obtener_proveedor(id_proveedor: UUID):
    try:
        return proveedor_crud.obtener(id_proveedor)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.post("/", response_model=ProveedorResponse, status_code=status.HTTP_201_CREATED)
def crear_proveedor(datos: ProveedorCreate):
    try:
        id_proveedor = proveedor_crud.crear(
            datos.nombre,
            datos.tel,
            datos.direccion,
            datos.correo
        )
        return proveedor_crud.obtener(id_proveedor)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.put("/{id_proveedor}", response_model=ProveedorResponse)
def actualizar_proveedor(id_proveedor: UUID, datos: ProveedorUpdate):
    try:
        proveedor_crud.actualizar(
            id_proveedor,
            datos.nombre,
            datos.tel,
            datos.direccion,
            datos.correo
        )
        return proveedor_crud.obtener(id_proveedor)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.delete("/{id_proveedor}")
def eliminar_proveedor(id_proveedor: UUID):
    try:
        proveedor_crud.eliminar(id_proveedor)
        return {"mensaje": "Proveedor eliminado correctamente"}
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
