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
        except Exception as e:
            #error quitar r
            log(f"ERROR: {e}")
            
            r = ""
        
           
    if r.status_code == 429:
        log(f"ERROR: requests status_code {r.status_code}")
        enCola(sku)
    
    if r.status_code != 200:
        
        return None
    
    return r

def log(msg:str):
    if conf.log_stdout:
        try:
            fecha = datetime.now().strftime("%m-%d-%Y_%H:%M:%S")
            print(f"[{fecha}]: {msg}")
        except UnicodeEncodeError:
            pass
        
def enCola(sku):
    return redis.sadd("lista_skus", sku)

def quitarCola():
    return redis.spop("lista_skus").decode("utf-8")

def counts():
    return len(redis.smembers("lista_skus"))

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