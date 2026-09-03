from fastapi import FastAPI

app = FastAPI(
    title="MenStyle API",
    description="API de comercio electrónico de ropa masculina",
    version="1.0.0"
)


@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a MenStyle API",
        "estado": "funcionando"
    }


@app.get("/saludo")
def saludo():
    return {
        "mensaje": "MenStyle está funcionando correctamente"
    }
