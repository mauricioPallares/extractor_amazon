from datetime import datetime


import configuraciones as conf 

from modelo import Producto
from helpers import splash_request, quitarCola, counts, log, normal_request, enCola
from extractores import Extractor 
from formato import limpiarTexto, limpiaPeso, limpiarPrecio, fixmarca

import eventlet
pool = eventlet.GreenPool(conf.max_hilos)
pile = eventlet.GreenPile(pool)

tiempo_inicio = datetime.now()

bd_redis = "sku_652703678" #listado de bd_redis
tabla_bd = "productos_junior" #listado de

def iniciar_scraper():
    """ punto de partida para el scraping de datos de amazon
    """
    global tiempo_inicio

    sku = quitarCola(bd_redis) #"B01EK3YBGG"
    
    log(f"INFO: Iniciando la extraccion del sku.", sku = sku)
    # if not sku:
    #     # print("ADVERTENCIA: sku no encotrado en cola. Reintentando...")
    #     log("ADVERTENCIA: sku no encotrado en cola. Reintentando...", sku = sku)
    #     pile.spawn(iniciar_scraper)
    #     return
    
    # if not Producto.esta_en_DB(sku, tabla_bd):
    soup = normal_request(sku)
    if not soup:
        return
    
    ex = Extractor(soup.text)

    producto = Producto(
        sku = sku,
        tabla= tabla_bd,
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
    
    if producto.titulo == "":
        print("Error captcha es solicitado")
        exit()

    if producto.precio == "Precio no encontrado" and producto.stock == "En Stock":
        print(sku + " pasado a cola de extraccion de splash")
        enCola("splash_junior_2", sku)
        # new_soup = splash_request(sku=sku)
        # ex = Extractor(new_soup.text)
        # producto.precio = ex.precio_splash()

        # print(producto)
    
    producto.guardar()
    # producto.act_disp()
        
    # else:
    #     # print(f"El sku: {sku} ya esta en la base de datos ")
    #     log(f"ADVERTENCIA: El sku: {sku} ya esta en la base de datos.")
    
    # log(f"INFO: operacion terminada sku: {sku}.")

    
if __name__ == '__main__':
   

    print(counts(bd_redis))

    while(counts(bd_redis) > 0):
        [pile.spawn(iniciar_scraper) for _ in range(conf.max_hilos)]
        
    pool.waitall()
    # iniciar_scraper()
    

    print(f"la extraccion inicio a {tiempo_inicio} y termino a {datetime.now()}")
    
    