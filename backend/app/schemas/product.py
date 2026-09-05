from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=150)
    descripcion: Optional[str] = None
    precio: float = Field(..., gt=0)
    categoria_id: int


class ProductoCrear(ProductoBase):
    pass


class ProductoActualizar(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=150)
    descripcion: Optional[str] = None
    precio: Optional[float] = Field(None, gt=0)
    categoria_id: Optional[int] = None
    activo: Optional[bool] = None


class ProductoRespuesta(ProductoBase):
    id: int
    activo: bool

    model_config = ConfigDict(from_attributes=True)