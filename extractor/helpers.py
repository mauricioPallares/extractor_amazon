import eventlet
import os
import random
from datetime import datetime
from urllib.parse import urlencode
import redis
import configuraciones as conf
from ua import users_agents
from google_trans_new import google_translator

trans = google_translator()
redis = redis.StrictRedis(host=conf.redis_host,
                          port=conf.redis_port, db=conf.redis_db)


requests = eventlet.import_patched('requests.__init__')
time = eventlet.import_patched('time')


REINTENTOS = 5


def realizar_peticion(sku):

    for _ in range(REINTENTOS):
        try:
            r = requests.get(url=api_url(sku), headers=get_header())
            if r.status_code in [200, 404]:
                break
        except Exception as e:
            # error quitar r
            log(f"ERROR: {e}")

            r = ""

    if r.status_code == 429:
        log(f"ERROR: requests status_code {r.status_code}")
        enCola(sku)

    if r.status_code != 200:

        return None

    return r


def log(msg: str):
    if conf.log_stdout:
        try:
            fecha = datetime.now().strftime("%m-%d-%Y_%H:%M:%S")
            print(f"[{fecha}]: {msg}")
        except UnicodeEncodeError:
            pass

# colas de skus


def enCola(sku):
    return redis.sadd("lista_skus", sku)


def quitarCola():
    return redis.spop("lista_skus").decode("utf-8")


def cola_actualizacion():
    return redis.spop("sku_652703678").decode("utf-8")


def cola_url():
    return redis.spop("lista_urls").decode("utf-8")


def counts():
    return len(redis.smembers("lista_skus"))


def num_cola():
    return redis.scard("sku_652703678")


def lista_actualizados(sku: str):
    return redis.sadd("actualizados", sku)


def api_url(sku):
    url = f"https://amazon.com/-es/dp/{sku}"
    playload = {'api_key': conf.API_TOKEN, 'url': url}
    proxy_url = conf.API_BASE_URL + urlencode(playload)
    print(url)
    return url


def traducir(texto: str) -> str:

    traduccion = trans.translate(
        text=texto, lang_src="en", lang_tgt="es") if texto is not None else ""
    return traduccion


def get_header():
    print("o")
    conf.headers.update({"User-Agent": random.choice(users_agents)})
    return conf.headers


def get_proxy():
    if not conf.proxy or len(conf.proxy) == 0:
        return None

    proxy_ip = random.choice(conf.proxy)

    proxy_url = "socks5://{user}:{passwd}@{ip}:{port}/".format(
        user=conf.proxy_user,
        passwd=conf.proxy_password,
        ip=proxy_ip,
        port=conf.proxy_port
    )

    return {
        "http": proxy_url,
        "https": proxy_url
    }


if __name__ == '__main__':

    from extractores import Extractor

    # listasku = ["B00002255O", "157982482X", "B00004RDF0", "B00004WA4H"]
    # for sku in listasku:

    #     pet = realizar_peticion(sku)
    #     ex = Extractor(pet.text)

    #     print(pet.status_code)
    #     # print(pet.headers)
    #     print("\n\n", ex.precio())
    #     print("\n\n", ex.stock())
    #     print("\n\n", ex.imagenes())
    #     print("\n\n", ex.titulo())
    #     print("_______________________________________")

    print(get_proxy())
    print(random.choice(conf.proxy))