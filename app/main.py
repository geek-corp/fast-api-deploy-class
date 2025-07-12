from fastapi import FastAPI
from datetime import datetime
app = FastAPI()

@app.get("/")
def leer_root():
    return {"mensaje": "¡Hola mundo desde FastAPI 2!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/calcular-edad/{nombre}/{fecha_nacimiento}")
def calcular_edad(nombre: str, fecha_nacimiento: str):
    hoy = datetime.now()
    fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
    edad = fecha_nacimiento.year - hoy.year
    if hoy.month < fecha_nacimiento.month or (hoy.month == fecha_nacimiento.month and hoy.day < fecha_nacimiento.day):
        edad -= 1
    return {"nombre": nombre, "edad": edad}

