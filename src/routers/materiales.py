
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from src.crud.material_crud import MaterialCRUD
from src.schemas.material import (
    MaterialCreate,
    MaterialUpdate,
    MaterialResponse
)

router = APIRouter(prefix="/materiales", tags=["Materiales"])

material_crud = MaterialCRUD()


@router.get("/", response_model=list[MaterialResponse])
def listar_materiales():
    return material_crud.listar()


@router.get("/{id_material}", response_model=MaterialResponse)
def obtener_material(id_material: UUID):
    try:
        return material_crud.obtener(id_material)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.post("/", response_model=MaterialResponse, status_code=status.HTTP_201_CREATED)
def crear_material(datos: MaterialCreate):
    try:
        id_material = material_crud.crear(
            datos.nombre,
            datos.tipo,
            datos.cantidad,
            datos.unidad,
            datos.precio
        )
        return material_crud.obtener(id_material)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.put("/{id_material}", response_model=MaterialResponse)
def actualizar_material(id_material: UUID, datos: MaterialUpdate):
    try:
        material_crud.actualizar(
            id_material,
            datos.nombre,
            datos.tipo,
            datos.cantidad,
            datos.unidad,
            datos.precio
        )
        return material_crud.obtener(id_material)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.delete("/{id_material}")
def eliminar_material(id_material: UUID):
    try:
        material_crud.eliminar(id_material)
        return {"mensaje": "Material eliminado correctamente"}
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
