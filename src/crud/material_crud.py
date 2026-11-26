
from uuid import UUID
from decimal import Decimal, InvalidOperation

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.database.connection import SessionLocal
from src.entities.material import Material


class MaterialCRUD:
    """CRUD de materiales utilizando SQLAlchemy y Neon PostgreSQL."""

    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    def listar(self):
        with self.session_factory() as sesion:
            materiales = sesion.scalars(
                select(Material).order_by(Material.nombre)
            ).all()

            return [
                {
                    "id_material": material.id_material,
                    "nombre": material.nombre,
                    "tipo": material.tipo,
                    "cantidad": material.cantidad,
                    "unidad": material.unidad,
                    "precio": material.precio,
                }
                for material in materiales
            ]

    def obtener(self, identificador):
        id_material = self._convertir_id(identificador)

        with self.session_factory() as sesion:
            material = self._buscar(sesion, id_material)

            return {
                "id_material": material.id_material,
                "nombre": material.nombre,
                "tipo": material.tipo,
                "cantidad": material.cantidad,
                "unidad": material.unidad,
                "precio": material.precio,
            }

    def crear(self, nombre, tipo, cantidad, unidad, precio):
        material = Material(
            nombre=nombre,
            tipo=tipo,
            cantidad=self._convertir_numero(cantidad, "cantidad"),
            unidad=unidad,
            precio=self._convertir_numero(precio, "precio"),
        )

        with self.session_factory() as sesion:
            sesion.add(material)

            try:
                sesion.commit()
                return material.id_material
            except IntegrityError as error:
                sesion.rollback()
                raise ValueError(
                    "No fue posible registrar el material."
                ) from error

    def actualizar(self, identificador, nombre, tipo, cantidad, unidad, precio):
        id_material = self._convertir_id(identificador)

        with self.session_factory() as sesion:
            material = self._buscar(sesion, id_material)

            material.nombre = nombre
            material.tipo = tipo
            material.cantidad = self._convertir_numero(cantidad, "cantidad")
            material.unidad = unidad
            material.precio = self._convertir_numero(precio, "precio")

            try:
                sesion.commit()
            except IntegrityError as error:
                sesion.rollback()
                raise ValueError(
                    "No fue posible actualizar el material."
                ) from error

    def eliminar(self, identificador):
        id_material = self._convertir_id(identificador)

        with self.session_factory() as sesion:
            material = self._buscar(sesion, id_material)
            sesion.delete(material)

            try:
                sesion.commit()
            except IntegrityError as error:
                sesion.rollback()
                raise ValueError(
                    "No fue posible eliminar el material porque tiene registros asociados."
                ) from error

    @staticmethod
    def _buscar(sesion, id_material):
        material = sesion.get(Material, id_material)

        if material is None:
            raise ValueError(
                f"No existe un material con el ID {id_material}."
            )

        return material

    @staticmethod
    def _convertir_id(identificador):
        try:
            return UUID(str(identificador))
        except (TypeError, ValueError, AttributeError) as error:
            raise ValueError(
                "El ID del material debe ser un UUID válido."
            ) from error

    @staticmethod
    def _convertir_numero(valor, campo):
        try:
            numero = Decimal(str(valor))
        except (InvalidOperation, TypeError, ValueError) as error:
            raise ValueError(
                f"El campo {campo} debe ser un número válido."
            ) from error

        if not numero.is_finite() or numero < 0:
            raise ValueError(
                f"El campo {campo} no puede ser negativo ni inválido."
            )

        return numero
