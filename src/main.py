
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routers.material import material_router
from routers.compra import compra_router
from routers.proveedor import proveedor_router
from routers.clientes import router
from routers.productos import router
from routers.pedidos import router
from routers.detalles_pedido import router

import os
from dotenv import load_dotenv

# Esto fuerza a leer el .env que está en la carpeta padre (la raíz)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))

# Creamos la aplicación FastAPI.
app = FastAPI(
    title="API Banco — Programacion de software 2026-2",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def raiz():
    return {"mensaje": "API en marcha"}

app.include_router(material_router)
app.include_router(compra_router)
app.include_router(proveedor_router)
app.include_router(router)
app.include_router(router)
app.include_router(router)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
