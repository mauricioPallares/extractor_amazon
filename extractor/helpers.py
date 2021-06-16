import os
from datetime import datetime
from urllib.parse import urlencode
import redis
import configuraciones as conf
from google_trans_new import google_translator

trans = google_translator()
redis = redis.StrictRedis(host= conf.redis_host, port= conf.redis_port, db = conf.redis_db)

import eventlet

requests = eventlet.import_patched('requests.__init__')
time = eventlet.import_patched('time')



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

#colas de skus
def enCola(sku):
    return redis.sadd("lista_skus", sku)

def quitarCola():
    return redis.spop("lista_skus").decode("utf-8")

def cola_actualizacion():
    return redis.spop("lista_actualizacion").decode("utf-8")

def cola_url():
    return redis.spop("lista_urls").decode("utf-8")
    
def counts():
    return len(redis.smembers("lista_skus"))

def api_url(sku):
    url = f"https://amazon.com/-es/dp/{sku}"
    playload = {'api_key': conf.API_TOKEN, 'url': url}
    proxy_url = conf.API_BASE_URL + urlencode(playload)
    return proxy_url

def traducir(texto: str) -> str:

    traduccion = trans.translate(text=texto, lang_src="en", lang_tgt="es") if texto is not None else ""
    return traduccion

if __name__ == '__main__':
    # test proxy server IP masking
    texto = "good job, it is great"

    print(traducir(texto))