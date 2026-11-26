
from uuid import UUID
from decimal import Decimal, InvalidOperation
from datetime import date

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.database.connection import SessionLocal
from src.entities.compra import Compra
from src.entities.proveedor import Proveedor


class CompraCRUD:
    """CRUD de compras utilizando SQLAlchemy y Neon PostgreSQL."""

    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    def listar(self):
        with self.session_factory() as sesion:
            compras = sesion.scalars(
                select(Compra).order_by(Compra.fecha.desc())
            ).all()

            return [
                {
                    "id_compra": compra.id_compra,
                    "fecha": compra.fecha,
                    "valor_total": compra.valor_total,
                    "estado": compra.estado,
                    "id_proveedor": compra.id_proveedor,
                }
                for compra in compras
            ]

    def obtener(self, identificador):
        id_compra = self._convertir_id(identificador)

        with self.session_factory() as sesion:
            compra = self._buscar(sesion, id_compra)

            return {
                "id_compra": compra.id_compra,
                "fecha": compra.fecha,
                "valor_total": compra.valor_total,
                "estado": compra.estado,
                "id_proveedor": compra.id_proveedor,
            }

    def crear(self, fecha, valor_total, estado, id_proveedor):
        id_proveedor = self._convertir_id_proveedor(id_proveedor)

        compra = Compra(
            fecha=self._convertir_fecha(fecha),
            valor_total=self._convertir_valor(valor_total),
            estado=estado,
            id_proveedor=id_proveedor,
        )

        with self.session_factory() as sesion:
            self._validar_proveedor(sesion, id_proveedor)
            sesion.add(compra)

            try:
                sesion.commit()
                return compra.id_compra
            except IntegrityError as error:
                sesion.rollback()
                raise ValueError(
                    "No fue posible registrar la compra."
                ) from error

    def actualizar(self, identificador, fecha, valor_total, estado, id_proveedor):
        id_compra = self._convertir_id(identificador)
        id_proveedor = self._convertir_id_proveedor(id_proveedor)

        with self.session_factory() as sesion:
            compra = self._buscar(sesion, id_compra)
            self._validar_proveedor(sesion, id_proveedor)

            compra.fecha = self._convertir_fecha(fecha)
            compra.valor_total = self._convertir_valor(valor_total)
            compra.estado = estado
            compra.id_proveedor = id_proveedor

            try:
                sesion.commit()
            except IntegrityError as error:
                sesion.rollback()
                raise ValueError(
                    "No fue posible actualizar la compra."
                ) from error

    def eliminar(self, identificador):
        id_compra = self._convertir_id(identificador)

        with self.session_factory() as sesion:
            compra = self._buscar(sesion, id_compra)
            sesion.delete(compra)
            sesion.commit()

    @staticmethod
    def _buscar(sesion, id_compra):
        compra = sesion.get(Compra, id_compra)

        if compra is None:
            raise ValueError(
                f"No existe una compra con el ID {id_compra}."
            )

        return compra

    @staticmethod
    def _validar_proveedor(sesion, id_proveedor):
        proveedor = sesion.get(Proveedor, id_proveedor)

        if proveedor is None:
            raise ValueError(
                "El proveedor indicado no existe."
            )

    @staticmethod
    def _convertir_id(identificador):
        try:
            return UUID(str(identificador))
        except (TypeError, ValueError, AttributeError) as error:
            raise ValueError(
                "El ID de la compra debe ser un UUID válido."
            ) from error

    @staticmethod
    def _convertir_id_proveedor(identificador):
        try:
            return UUID(str(identificador))
        except (TypeError, ValueError, AttributeError) as error:
            raise ValueError(
                "El ID del proveedor debe ser un UUID válido."
            ) from error

    @staticmethod
    def _convertir_fecha(fecha):
        if isinstance(fecha, date):
            return fecha

        try:
            return date.fromisoformat(str(fecha))
        except (TypeError, ValueError) as error:
            raise ValueError(
                "La fecha debe tener el formato AAAA-MM-DD."
            ) from error

    @staticmethod
    def _convertir_valor(valor_total):
        try:
            valor = Decimal(str(valor_total))
        except (InvalidOperation, TypeError, ValueError) as error:
            raise ValueError(
                "El valor total debe ser un número válido."
            ) from error

        if not valor.is_finite() or valor < 0:
            raise ValueError(
                "El valor total no puede ser negativo ni inválido."
            )

        return valor
