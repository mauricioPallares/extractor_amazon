import pandas as pd
import math, os, redis
from helpers import counts
r = redis.Redis()




def cargar_set_sku():
    base = os.path.dirname(os.path.realpath(__file__))
    print(base)
    lista = pd.read_excel(base + r"/SKU_ANDRES.xlsx")
    
    lista_skus = set(lista['asin'].to_list())
    # extractor/SKU_ANDRES.xlsx
    
    for sku in lista_skus:
        r.sadd('lista_skus', sku)
    
    print("done")

# cargar_set_sku()
print(counts())