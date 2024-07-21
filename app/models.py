from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Producto(Base):
    __tablename__ = 'productos'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    precio = Column(Float)
    cantidad = Column(Integer)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    categoria = Column(String)
