from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.product import Producto
from app.models.category import Categoria
from app.schemas.product import ProductoCrear, ProductoActualizar


def listar_productos(
    db: Session,
    categoria_id: Optional[int] = None,
    solo_activos: bool = False
) -> List[Producto]:
    query = db.query(Producto)

    if categoria_id is not None:
        query = query.filter(Producto.categoria_id == categoria_id)

    if solo_activos:
        query = query.filter(Producto.activo.is_(True))

    return query.all()


def obtener_producto_por_id(
    db: Session,
    producto_id: int
) -> Producto:
    producto = db.query(Producto).filter(
        Producto.id == producto_id
    ).first()

    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    return producto


def crear_producto(
    db: Session,
    datos: ProductoCrear
) -> Producto:
    nombre_limpio = datos.nombre.strip()
    if not nombre_limpio:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre del producto es obligatorio"
        )

    if datos.precio <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El precio debe ser mayor a 0"
        )

    categoria = db.query(Categoria).filter(
        Categoria.id == datos.categoria_id
    ).first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La categoría especificada no existe"
        )

    nuevo_producto = Producto(
        nombre=nombre_limpio,
        descripcion=datos.descripcion,
        precio=datos.precio,
        categoria_id=datos.categoria_id,
        activo=True
    )

    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)

    return nuevo_producto


def actualizar_producto(
    db: Session,
    producto_id: int,
    datos: ProductoActualizar
) -> Producto:
    producto = obtener_producto_por_id(db, producto_id)

    if datos.nombre is not None:
        nombre_limpio = datos.nombre.strip()
        if not nombre_limpio:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre del producto no puede estar vacío"
            )
        producto.nombre = nombre_limpio

    if datos.precio is not None:
        if datos.precio <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El precio debe ser mayor a 0"
            )
        producto.precio = datos.precio

    if datos.categoria_id is not None:
        categoria = db.query(Categoria).filter(
            Categoria.id == datos.categoria_id
        ).first()

        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La categoría especificada no existe"
            )
        producto.categoria_id = datos.categoria_id

    if datos.descripcion is not None:
        producto.descripcion = datos.descripcion

    if datos.activo is not None:
        producto.activo = datos.activo

    db.commit()
    db.refresh(producto)

    return producto


def eliminar_producto(
    db: Session,
    producto_id: int
) -> Producto:
    producto = obtener_producto_por_id(db, producto_id)
    producto.activo = False

    db.commit()
    db.refresh(producto)

    return producto
