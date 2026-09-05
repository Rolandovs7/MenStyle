from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.auth import router as auth_router
from app.api.routes.categories import router as categories_router
from app.api.routes.products import router as products_router
from app.api.routes.inventory import router as inventory_router
from app.api.routes.cart import router as cart_router
from app.api.routes.reservations import router as reservations_router
from app.api.routes.notifications import router as notifications_router
from app.api.routes.orders import router as orders_router
from app.api.routes.payments import router as payments_router
from app.api.routes.returns import router as returns_router
from app.api.routes.users import router as users_router
from app.api.routes.permissions import router as permissions_router


app = FastAPI(
    title="MenStyle API",
    description="API de comercio electrónico de ropa masculina",
    version="1.0.0"
)

# ============================================
# CONFIGURACIÓN CORS
# ============================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# ROUTERS
# ============================================
app.include_router(auth_router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(categories_router, prefix="/api/categorias", tags=["Categorías"])
app.include_router(products_router, prefix="/api/productos", tags=["Productos"])
app.include_router(inventory_router, prefix="/api/inventario", tags=["Inventario"])
app.include_router(cart_router, prefix="/api/carrito", tags=["Carrito"])
app.include_router(reservations_router, prefix="/api/reservas", tags=["Reservas"])
app.include_router(notifications_router, prefix="/api/notificaciones", tags=["Notificaciones"])
app.include_router(orders_router, prefix="/api/pedidos", tags=["Pedidos"])
app.include_router(payments_router, prefix="/api/pagos", tags=["Pagos"])
app.include_router(returns_router, prefix="/api/devoluciones", tags=["Devoluciones"])
app.include_router(users_router, prefix="/api")
app.include_router(permissions_router, prefix="/api")

# ============================================
# ENDPOINTS DE PRUEBA
# ============================================
@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a MenStyle API",
        "estado": "funcionando",
        "documentacion": "/docs"
    }


@app.get("/saludo")
def saludo():
    return {
        "mensaje": "MenStyle está funcionando correctamente"
    }