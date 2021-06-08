import sys
from datetime import datetime

import configuraciones as conf 

import eventlet

from modelo import Producto
from helpers import realizar_peticion, quitarCola
from extractores import Extractor 

scrap_time = datetime.now()

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
            'titulo' : ex.titulo(),
            'precio' : ex.precio(),
            'marca' : ex.marca(),
            'imagenes' : ex.imagenes(),
            'disponibilidad' : ex.disponibilidad(),
            'caracteristicas' : ex.caracteristicas(),
            'descripcion' : ex.descripcion(),
            'peso': ex.peso(),
        } 

        producto = Producto(item)

        producto.guardar()
    else:
        print(f"El sku: {sku} ya esta en la base de datos ")

    
if __name__ == '__main__':

    print(f"iniciando estraccion at {tiempo_inicio}")

    # [pile.spawn(iniciar_scraper) for _ in range(conf.max_threads)]
    # pool.waitall()
    iniciar_scraper()