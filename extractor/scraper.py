from datetime import datetime

import configuraciones as conf 

from modelo import Producto
from helpers import realizar_peticion, quitarCola
from extractores import Extractor 
from formato import limpiarTexto, limpiaPeso, limpiarPrecio, fixmarca

import eventlet
pool = eventlet.GreenPool(conf.max_threads)
pile = eventlet.GreenPile(pool)

tiempo_inicio = datetime.now()

def iniciar_scraper():
    global tiempo_inicio

    sku = quitarCola()
    print(sku)
    if not sku:
        print("ADVERTENCIA: sku no encotrado en cola. Reintentando...")
        pile.spawn(iniciar_scraper)
        return
    
    if not Producto.esta_en_DB(sku):
        soup = realizar_peticion(sku)

        if not soup:
            return
        
        ex = Extractor(soup.text)

        item = {
            'sku': sku,
            'titulo' : limpiarTexto(ex.titulo()),
            'precio' :  limpiarPrecio(ex.precio()),
            'marca' : fixmarca(ex.marca()),
            'imagenes' : ex.imagenes(),
            'disponibilidad' : limpiarTexto(ex.disponibilidad()),
            'caracteristicas' : limpiarTexto(ex.caracteristicas()),
            'descripcion' : limpiarTexto(ex.descripcion()),
            'peso': limpiaPeso(ex.peso()),
        } 

        producto = Producto(item)

        producto.guardar()
    else:
        print(f"El sku: {sku} ya esta en la base de datos ")

    
if __name__ == '__main__':

    print(f"iniciando estraccion at {tiempo_inicio}")

    for i in range(5):
        [pile.spawn(iniciar_scraper) for _ in range(conf.max_threads)]
        pool.waitall()
    # iniciar_scraper()