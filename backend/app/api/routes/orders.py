from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import obtener_db, obtener_usuario_actual, requerir_rol
from app.models.user import Usuario
from app.schemas.order import (
    PedidoCrear,
    PedidoCambiarEstadoAdmin,
    PedidoRespuesta
)
from app.services import order_service

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)


@router.get(
    "",
    response_model=List[PedidoRespuesta]
)
def listar_mis_pedidos(
    estado: Optional[str] = None,
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(obtener_db)
):
    return order_service.listar_pedidos_usuario(
        db,
        usuario_actual.id,
        estado=estado
    )


@router.get(
    "/{pedido_id}",
    response_model=PedidoRespuesta
)
def obtener_mi_pedido(
    pedido_id: int,
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(obtener_db)
):
    return order_service.obtener_pedido_por_id(
        db,
        usuario_actual.id,
        pedido_id
    )


@router.post(
    "",
    response_model=PedidoRespuesta,
    status_code=status.HTTP_201_CREATED
)
def crear_pedido_desde_carrito(
    datos: PedidoCrear,
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(obtener_db)
):
    return order_service.crear_pedido_desde_carrito(
        db,
        usuario_actual.id,
        datos
    )


@router.put(
    "/{pedido_id}/cancelar",
    response_model=PedidoRespuesta
)
def cancelar_mi_pedido(
    pedido_id: int,
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(obtener_db)
):
    return order_service.cancelar_pedido_cliente(
        db,
        usuario_actual.id,
        pedido_id
    )


@router.put(
    "/{pedido_id}/estado",
    response_model=PedidoRespuesta
)
def cambiar_estado_pedido_admin(
    pedido_id: int,
    datos: PedidoCambiarEstadoAdmin,
    db: Session = Depends(obtener_db),
    _usuario_admin=Depends(requerir_rol("administrador"))
):
    return order_service.cambiar_estado_pedido_admin(
        db,
        pedido_id,
        datos
    )
