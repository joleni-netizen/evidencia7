from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, select

# Configuración de la base de datos
DATABASE_URL = "postgresql+asyncpg://postgres:root@localhost/pruebas"
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# Modelo de la tabla usuarios
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String, nullable=False)
    correo = Column(String, unique=True, nullable=False)
    clave = Column(String, nullable=False)

# Pydantic Schemas
class UsuarioCreate(BaseModel):
    nombre_completo: str
    correo: str
    clave: str

class UsuarioResponse(BaseModel):
    id: int
    nombre_completo: str
    correo: str

class LoginRequest(BaseModel):
    correo: str
    clave: str

# FastAPI app
app = FastAPI()
# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔴 Permite todas las solicitudes (puedes cambiarlo)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los headers
)

# Función para obtener sesión de base de datos
async def get_db():
    async with SessionLocal() as session:
        yield session

# Endpoint: Registro de usuario
@app.post("/registro", response_model=UsuarioResponse)
async def registrar_usuario(user: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    nuevo_usuario = Usuario(
        nombre_completo=user.nombre_completo,
        correo=user.correo,
        clave=user.clave  # 🔴 No se encripta la clave (⚠ No recomendado en producción)
    )
    db.add(nuevo_usuario)
    await db.commit()
    await db.refresh(nuevo_usuario)
    return nuevo_usuario

# Endpoint: Login (verifica email y clave)
@app.post("/login")
async def login(user: LoginRequest, db: AsyncSession = Depends(get_db)):
    query = select(Usuario).where(Usuario.correo == user.correo, Usuario.clave == user.clave)
    result = await db.execute(query)
    usuario = result.scalar()

    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")

    return {"message": "Inicio de sesión exitoso", "usuario_id": usuario.id, "nombre": usuario.nombre_completo}




#py -m pip install fastapi uvicorn sqlalchemy asyncpg
#cd back && py -m uvicorn main:app --reload