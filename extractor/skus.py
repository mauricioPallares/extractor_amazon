import pandas as pd
import math, os, redis

r = redis.Redis()




def cargar_set_sku():
    base = os.path.dirname(os.path.realpath(__file__))
    print(base)
    lista = pd.read_excel(base + r"/skus.xlsx")
    
    lista_skus = set(lista['asin'].to_list())
    
    
    for sku in lista_skus:
        r.sadd('lista_skus', sku)