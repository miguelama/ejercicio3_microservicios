# test/test_main.py
import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.models import Base

# Configuración de la base de datos de prueba
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear las tablas en la base de datos de prueba
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="module")
def test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
async def client():
    # Sobrescribir la dependencia get_db para usar la base de datos de prueba
    app.dependency_overrides[get_db] = lambda: test_db()

    # Usar AsyncClient para interactuar con la API
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_create_producto(client):
    response = await client.post("/productos/", json={"nombre": "Producto 1", "precio": 10.0, "cantidad": 5,
                                                      "categoria": "Categoría 1"})
    assert response.status_code == 200
    assert response.json()["nombre"] == "Producto 1"


@pytest.mark.asyncio
async def test_read_productos(client):
    response = await client.get("/productos/")
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.asyncio
async def test_update_producto(client):
    response = await client.put("/productos/1", json={"nombre": "Producto 1 Updated", "precio": 12.0, "cantidad": 10,
                                                      "categoria": "Categoría 1"})
    assert response.status_code == 200
    assert response.json()["nombre"] == "Producto 1 Updated"


@pytest.mark.asyncio
async def test_delete_producto(client):
    response = await client.delete("/productos/1")
    assert response.status_code == 200
    assert response.json()["mensaje"] == "Producto eliminado"
