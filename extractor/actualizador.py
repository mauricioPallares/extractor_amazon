from datetime import datetime
import configuraciones as conf
from modelo import Producto
from extratores import Extractor
from formato import limpiarPrecio
from helpers import realizar_peticion, cola_actualizacion

import eventlet

pool = eventlet.GreenPool(conf.max_threads)
pile = eventlet.GreenPile(pool)

tiempo_inicio = datetime.now()

def actualizar():
    sku = cola_actualizacion()

    soup = realizar_peticion(sku)

    ex = Extractor(soup.text)

    producto = Producto()

    producto.sku = sku
    producto.precio = limpiarPrecio(ex.precio())
    producto.disponibilidad = ex.disponibilidad()

    producto.actualizar()

    
