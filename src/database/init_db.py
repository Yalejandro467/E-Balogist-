
from src.database.connection import Base, engine

# Importar las entidades existentes
from src.entities.cliente import Cliente
from src.entities.producto import Producto
from src.entities.pedido import Pedido
from src.entities.detalle_pedido import DetallePedido
from src.entities.empleado import Empleado
from src.entities.produccion import Produccion
from src.entities.transporte import Transporte
from src.entities.instalacion import Instalacion
from src.entities.usuario import Usuario

# Importar las nuevas entidades
from src.entities.proveedor import Proveedor
from src.entities.material import Material
from src.entities.compra import Compra


def crear_tablas():
    Base.metadata.create_all(bind=engine)
    print("Tablas verificadas y creadas si no existían.")


if __name__ == "__main__":
    crear_tablas()
