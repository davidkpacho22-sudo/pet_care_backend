from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, usuarios, mascotas, veterinarias, recordatorios, productos, resenas, mensajes

app = FastAPI(
    title="PeludOS API",
    description="Backend de la plataforma de cuidado de mascotas",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(mascotas.router)
app.include_router(veterinarias.router)
app.include_router(recordatorios.router)
app.include_router(productos.router)
app.include_router(resenas.router)
app.include_router(mensajes.router)


@app.get("/health")
def health():
    return {"status": "ok", "message": "PeludOS API funcionando 🐾"}