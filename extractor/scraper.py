from datetime import datetime


import configuraciones as conf 

from modelo import Producto
from helpers import realizar_peticion, quitarCola, counts, log
from extractores import Extractor 
from formato import limpiarTexto, limpiaPeso, limpiarPrecio, fixmarca

import eventlet
pool = eventlet.GreenPool(conf.max_hilos)
pile = eventlet.GreenPile(pool)

tiempo_inicio = datetime.now()
paula = "sku_15923319"
def iniciar_scraper():
    """ punto de partida para el scraping de datos de amazon
    """
    global tiempo_inicio

    sku = quitarCola(paula)
    
    log(f"INFO: Iniciando la extraccion del sku.", sku = sku)
    # if not sku:
    #     # print("ADVERTENCIA: sku no encotrado en cola. Reintentando...")
    #     log("ADVERTENCIA: sku no encotrado en cola. Reintentando...", sku = sku)
    #     pile.spawn(iniciar_scraper)
    #     return
    
    if not Producto.esta_en_DB(sku):
        soup = realizar_peticion(sku)

        if not soup:
            return
        
        ex = Extractor(soup.text)

        producto = Producto(
            sku = sku,
            titulo  = limpiarTexto(ex.titulo()),
            precio  =  limpiarPrecio(ex.precio()),
            marca  = fixmarca(ex.marca()),
            imagenes  = ex.imagenes(),
            disponibilidad = limpiarTexto(ex.disponibilidad()),
            stock = ex.stock(),
            caracteristicas  = limpiarTexto(ex.caracteristicas()),
            descripcion  = limpiarTexto(ex.descripcion()),
            peso = limpiaPeso(ex.peso()),
        )
        print(producto)
        producto.guardar()
        
    else:
        # print(f"El sku: {sku} ya esta en la base de datos ")
        log(f"ADVERTENCIA: El sku: {sku} ya esta en la base de datos.")
    
    # log(f"INFO: operacion terminada sku: {sku}.")

    
if __name__ == '__main__':
    paula = "sku_15923319"

    print(counts(paula))

    while(counts(paula) > 0):
        [pile.spawn(iniciar_scraper) for _ in range(conf.max_hilos)]
        
    pool.waitall()
    
    

    print(f"la extraccion inicio a {tiempo_inicio} y termino a {datetime.now()}")
    