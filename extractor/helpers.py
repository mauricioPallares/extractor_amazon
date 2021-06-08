# from extractor.configuraciones import API_BASE_URL
import os
from datetime import datetime

from urllib.parse import urlencode
import redis
import configuraciones as conf
redis = redis.Redis()

import eventlet

requests = eventlet.import_patched('requests.__init__')
time = eventlet.import_patched('time')

import configuraciones as conf 

REINTENTOS = 5

def realizar_peticion(sku):
    
    for _ in range(REINTENTOS):
        try:
            r = requests.get(api_url(sku))
            if r.status_code in [200,404]:
                break
        except:
            r = ""
        
    
    if r.status_code != 200:
        return None
    
    return r

def enCola(sku):
    return redis.sadd("lista_skus", sku)

def quitarCola():
    return redis.spop("lista_skus").decode("utf-8")

def api_url(sku):
    url = f"https://amazon.com/-es/dp/{sku}"
    playload = {'api_key': conf.API_TOKEN, 'url': url}
    proxy_url = conf.API_BASE_URL + urlencode(playload)
    return proxy_url


if __name__ == '__main__':
    # test proxy server IP masking
    r = realizar_peticion("B09201FVGRK")
    
    
    if r:
        print(r.text)
    else:
        print(r)