from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/productos/", response_model=schemas.Producto)
def create_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    return crud.create_producto(db=db, producto=producto)

@app.get("/productos/", response_model=List[schemas.Producto])
def read_productos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    productos = crud.get_productos(db, skip=skip, limit=limit)
    return productos

@app.put("/productos/{producto_id}", response_model=schemas.Producto)
def update_producto(producto_id: int, producto: schemas.ProductoUpdate, db: Session = Depends(get_db)):
    db_producto = crud.get_producto(db, producto_id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return crud.update_producto(db=db, producto=producto, producto_id=producto_id)

@app.delete("/productos/{producto_id}", response_model=schemas.Producto)
def delete_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = crud.get_producto(db, producto_id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return crud.delete_producto(db=db, producto_id=producto_id)
