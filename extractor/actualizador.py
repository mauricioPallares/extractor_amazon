from datetime import datetime
import configuraciones as conf
from modelo import Producto
from extractores import Extractor
from formato import limpiarPrecio
from helpers import realizar_peticion, cola_actualizacion, num_cola, log

import eventlet

pool = eventlet.GreenPool(conf.max_threads)
pile = eventlet.GreenPile(pool)

tiempo_inicio = datetime.now()

def actualizar():
    sku = cola_actualizacion()
    log(f"INFO: extrayendo informacion actual el sku: {sku}.")
    
    soup = realizar_peticion(sku)

    ex = Extractor(soup.text)

    producto = Producto()

    producto.sku = sku
    producto.precio = limpiarPrecio(ex.precio())
    producto.stock = ex.stock()

    # print(producto)
    producto.actualizar_stock()

    log("INFO: Actualizado")

if __name__ == '__main__':
    # actualizar()
    while (num_cola() > 0) :
        [pile.spawn(actualizar) for _ in range(10)]

    pool.waitall()

    print(f"la extraccion inicio a {tiempo_inicio} y termino a {datetime.now()}")

def suma(num1: int = 1, num2: int =1) -> int:
    pass

