
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from src.crud.compra_crud import CompraCRUD
from src.schemas.compra import (
    CompraCreate,
    CompraUpdate,
    CompraResponse
)

router = APIRouter(prefix="/compras", tags=["Compras"])

compra_crud = CompraCRUD()


@router.get("/", response_model=list[CompraResponse])
def listar_compras():
    return compra_crud.listar()


@router.get("/{id_compra}", response_model=CompraResponse)
def obtener_compra(id_compra: UUID):
    try:
        return compra_crud.obtener(id_compra)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.post("/", response_model=CompraResponse, status_code=status.HTTP_201_CREATED)
def crear_compra(datos: CompraCreate):
    try:
        id_compra = compra_crud.crear(
            datos.fecha,
            datos.valor_total,
            datos.estado,
            datos.id_proveedor
        )
        return compra_crud.obtener(id_compra)
    except ValueError as error:
        mensaje = str(error)
        codigo = 404 if "proveedor" in mensaje.lower() else 400
        raise HTTPException(status_code=codigo, detail=mensaje)


@router.put("/{id_compra}", response_model=CompraResponse)
def actualizar_compra(id_compra: UUID, datos: CompraUpdate):
    try:
        compra_crud.actualizar(
            id_compra,
            datos.fecha,
            datos.valor_total,
            datos.estado,
            datos.id_proveedor
        )
        return compra_crud.obtener(id_compra)
    except ValueError as error:
        mensaje = str(error)
        codigo = 404 if "no existe" in mensaje.lower() else 400
        raise HTTPException(status_code=codigo, detail=mensaje)


@router.delete("/{id_compra}")
def eliminar_compra(id_compra: UUID):
    try:
        compra_crud.eliminar(id_compra)
        return {"mensaje": "Compra eliminada correctamente"}
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
