from datetime import datetime

import configuraciones as conf 

from modelo import Producto
from helpers import realizar_peticion, quitarCola, counts, log, traducir
from extractores import Extractor 
from formato import limpiarTexto, limpiaPeso, limpiarPrecio, fixmarca

import eventlet
pool = eventlet.GreenPool(conf.max_threads)
pile = eventlet.GreenPile(pool)

tiempo_inicio = datetime.now()

def iniciar_scraper():
    global tiempo_inicio

    sku = quitarCola()
    # print(sku)
    log(f"INFO: Iniciando la extraccion del sku: {sku}.")
    if not sku:
        # print("ADVERTENCIA: sku no encotrado en cola. Reintentando...")
        log("ADVERTENCIA: sku no encotrado en cola. Reintentando...")
        pile.spawn(iniciar_scraper)
        return
    
    if not Producto.esta_en_DB(sku):
        soup = realizar_peticion(sku)

        if not soup:
            return
        
        ex = Extractor(soup.text)

        producto = Producto(
            sku = sku,
            titulo  = traducir(limpiarTexto(ex.titulo())),
            precio  =  limpiarPrecio(ex.precio()),
            marca  = fixmarca(ex.marca()),
            imagenes  = ex.imagenes(),
            disponibilidad = limpiarTexto(ex.disponibilidad()),
            stock = ex.stock(),
            caracteristicas  = traducir(limpiarTexto(ex.caracteristicas())),
            descripcion  = traducir(limpiarTexto(ex.descripcion())),
            peso = limpiaPeso(ex.peso()),
        )

        print(producto)

        producto.guardar()
    else:
        # print(f"El sku: {sku} ya esta en la base de datos ")
        log(f"ADVERTENCIA: El sku: {sku} ya esta en la base de datos.")
    
    # log(f"INFO: operacion terminada sku: {sku}.")

    
if __name__ == '__main__':

    # print(f"iniciando extraccion at {tiempo_inicio}")

    print(f"skus en cola {counts() :,}")

    while(counts() > 0):
        [pile.spawn(iniciar_scraper) for _ in range(conf.max_threads)]
    pool.waitall()
    # iniciar_scraper()

    print(tiempo_inicio)
    print(datetime.now())