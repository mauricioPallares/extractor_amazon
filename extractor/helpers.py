import eventlet
import os
import random
from datetime import datetime
from urllib.parse import urlencode
import redis
import configuraciones as conf
from ua import users_agents

redis = redis.StrictRedis(host=conf.redis_host,
                          port=conf.redis_port, db=conf.redis_db)


requests = eventlet.import_patched('requests.__init__')
time = eventlet.import_patched('time')


REINTENTOS = 5


def realizar_peticion(sku: str):
    """[summary]

    Args:
        sku (str): Sku de amazon

    Returns:
        [requets.Response]: [description]
    """
    proxies = get_proxy()

    for _ in range(REINTENTOS):
        try:
            r = requests.get(
                url=amazon_url(sku),
                headers=get_header(),
                proxies=proxies)

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
    """[summary]

    Args:
        msg (str): Mensaje para el archivo de logs
    """
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
    return redis.scard("lista_skus")


def num_cola():
    return redis.scard("sku_652703678")


def lista_actualizados(sku: str):
    return redis.sadd("actualizados", sku)

########################################################################
######## funciones aux ######
########################################################################
def amazon_url(sku: str) -> str:
    """ Recibe un sku y retorna la url del producto en amazon

    Args:
        sku (str): Sku de producto en amazon

    Returns:
        str: Url formateada del producto
    """
    url = f"https://amazon.com/dp/{sku}"
    # playload = {'api_key': conf.API_TOKEN, 'url': url}
    # proxy_url = conf.API_BASE_URL + urlencode(playload)
    # print(url)
    return url


def get_header() -> dict:
    """ Retorna un diccionario con los encabezados para la peticion con rotacion de users Agents

    Returns:
        dict: diccionario de encabezados
    """
    conf.headers.update({"User-Agent": random.choice(users_agents)})
    return conf.headers


def get_proxy() -> dict:

    """ Esta funcion toma el listado de  proxies ingresados en el archivo configuracion.py y retorna uno aleatoriamente en cada peticion

    Returns:
        dict: Diccionario de proxies
    """
    if not conf.proxy or len(conf.proxy) == 0:
        return None

    # proxy =

    proxy_url = "http://{user}:{passwd}@{ip}".format(
        user=conf.proxy_user,
        passwd=conf.proxy_password,
        ip=random.choice(conf.proxy),

    )

    return {
        "http": proxy_url,
        "https": proxy_url
    }


if __name__ == '__main__':

    # print(get_proxy())
    r = realizar_peticion("B00FLYWNYQ")
    print(r.status_code)
