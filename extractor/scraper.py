import sys
from datetime import datetime

import configuraciones as conf 

import eventlet

from modelo import Producto
from helpers import realizar_peticion
from extractores import *

scrap_time = datetime.now()

pool = eventlet.GreenPool(conf.max_threads)
pile = eventlet.GreenPile(pool)


def iniciar_scraper():
    pass
