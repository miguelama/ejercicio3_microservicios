from pydantic import BaseModel
from datetime import datetime

class ProductoBase(BaseModel):
    nombre: str
    precio: float
    cantidad: int
    categoria: str

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int
    fecha_creacion: datetime

    class Config:
        orm_mode = True
