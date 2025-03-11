from models.producto import Producto
from models.ingrediente import Ingrediente
from config.db import db

def obtener_menu():
    productos = Producto.query.all()
    return [{"nombre": p.nombre, "precio": p.precio_publico} for p in productos]

def procesar_venta(nombre_producto):
    try:
        return vender(nombre_producto)
    except ValueError as e:
        return str(e)
    
def vender(nombre_producto):
    producto = Producto.query.filter_by(nombre=nombre_producto).first()
    if not producto:
        return f"¡Oh no! No tenemos {nombre_producto}"

    ingredientes = [producto.ingrediente1, producto.ingrediente2, producto.ingrediente3]
    
    for ingrediente in ingredientes:
        if ingrediente.inventario <= 0:
            return f"¡Oh no! Nos hemos quedado sin {ingrediente.nombre}"

    # Reducir inventario y guardar en la BD
    for ingrediente in ingredientes:
        ingrediente.inventario -= 1

    db.session.commit()  # IMPORTANTE: Guardar cambios en la BD

    return "¡Vendido!"