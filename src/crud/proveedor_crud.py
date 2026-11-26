
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from src.database.connection import SessionLocal
from src.entities.proveedor import Proveedor
from src.entities.compra import Compra


class ProveedorCRUD:
    """CRUD de proveedores utilizando SQLAlchemy y Neon PostgreSQL."""

    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    def listar(self):
        with self.session_factory() as sesion:
            proveedores = sesion.scalars(
                select(Proveedor).order_by(Proveedor.nombre)
            ).all()

            return [
                {
                    "id_proveedor": proveedor.id_proveedor,
                    "nombre": proveedor.nombre,
                    "tel": proveedor.tel,
                    "direccion": proveedor.direccion,
                    "correo": proveedor.correo,
                }
                for proveedor in proveedores
            ]

    def obtener(self, identificador):
        id_proveedor = self._convertir_id(identificador)

        with self.session_factory() as sesion:
            proveedor = self._buscar(sesion, id_proveedor)

            return {
                "id_proveedor": proveedor.id_proveedor,
                "nombre": proveedor.nombre,
                "tel": proveedor.tel,
                "direccion": proveedor.direccion,
                "correo": proveedor.correo,
            }

    def crear(self, nombre, tel, direccion, correo):
        proveedor = Proveedor(
            nombre=nombre,
            tel=tel,
            direccion=direccion,
            correo=correo,
        )

        with self.session_factory() as sesion:
            sesion.add(proveedor)

            try:
                sesion.commit()
                return proveedor.id_proveedor
            except IntegrityError as error:
                sesion.rollback()
                raise ValueError(
                    "No fue posible registrar el proveedor."
                ) from error

    def actualizar(self, identificador, nombre, tel, direccion, correo):
        id_proveedor = self._convertir_id(identificador)

        with self.session_factory() as sesion:
            proveedor = self._buscar(sesion, id_proveedor)

            proveedor.nombre = nombre
            proveedor.tel = tel
            proveedor.direccion = direccion
            proveedor.correo = correo

            try:
                sesion.commit()
            except IntegrityError as error:
                sesion.rollback()
                raise ValueError(
                    "No fue posible actualizar el proveedor."
                ) from error

    def eliminar(self, identificador):
        id_proveedor = self._convertir_id(identificador)

        with self.session_factory() as sesion:
            proveedor = self._buscar(sesion, id_proveedor)

            compras = sesion.scalar(
                select(func.count())
                .select_from(Compra)
                .where(Compra.id_proveedor == id_proveedor)
            )

            if compras:
                raise ValueError(
                    "No se puede eliminar el proveedor porque tiene compras asociadas."
                )

            sesion.delete(proveedor)

            try:
                sesion.commit()
            except IntegrityError as error:
                sesion.rollback()
                raise ValueError(
                    "No se puede eliminar el proveedor porque tiene registros asociados."
                ) from error

    @staticmethod
    def _buscar(sesion, id_proveedor):
        proveedor = sesion.get(Proveedor, id_proveedor)

        if proveedor is None:
            raise ValueError(
                f"No existe un proveedor con el ID {id_proveedor}."
            )

        return proveedor

    @staticmethod
    def _convertir_id(identificador):
        try:
            return UUID(str(identificador))
        except (TypeError, ValueError, AttributeError) as error:
            raise ValueError(
                "El ID del proveedor debe ser un UUID válido."
            ) from error
