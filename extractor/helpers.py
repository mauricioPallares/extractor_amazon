import eventlet
import json
import random

from user_agent import generate_user_agent
import random
from datetime import datetime
from urllib.parse import urlencode
import redis
import configuraciones as conf
# from ua import users_agents
# from requests.exceptions import ConnectionError

redis = redis.StrictRedis(host=conf.redis_host,
                          port=conf.redis_port, db=conf.redis_db)


requests = eventlet.import_patched('requests.__init__')
# exepcionConecio = eventlet.import_patched('requests.exceptions.ConnectionError')
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
    reintentos = 0
    while (reintentos < REINTENTOS):
        try:
            # time.sleep(random.randint(1,6))
            r = requests.get(
                url=amazon_url(sku),
                headers=get_header(),
                proxies=proxies)
            # print(r.status_code)
            if r.status_code in [200, 404]:
                ya_descargado(sku)
                break

        # except requests.ConnectionError as e:
        #     # print(e, "Error de coneccion maximo intento de coneciones")
        #     log(e, sku= sku)
        #     reintentos += 1
        #     time.sleep(5)
        #     log(f"reintentado {reintentos}", sku=sku)

        #     realizar_peticion(sku=sku)


            # r = ""
        except Exception as e:
            # error quitar r
            log(f"ERROR: {e}", sku = sku)
            time.sleep(5)
            reintentos += 1


    if r.status_code == 429:
        log(f"ERROR: requests status_code {r.status_code}", sku = sku)
        enCola(sku)

    if r.status_code != 200:

        return None

    return r


def log(msg: str, sku: str = None):
    """[summary]

    Args:
        msg (str): Mensaje para el archivo de logs
    """
    if conf.log_stdout:
        try:
            fecha = datetime.now().strftime("%m-%d-%Y_%H:%M:%S")
            print(f"[{fecha}]: {sku}=>{msg}")
        except UnicodeEncodeError:
            pass

# colas de skus


def enCola(conjunto, sku):
    return redis.sadd(conjunto, sku)


def quitarCola(conjunto):
    return redis.spop(conjunto).decode("utf-8")

def ya_descargado(sku):
    return redis.sadd("descargado", sku)

def cola_actualizacion():
    return redis.spop("sku_652703678").decode("utf-8")


def cola_url():
    return redis.spop("lista_urls").decode("utf-8")


def counts(conjunto):
    return redis.scard(conjunto)


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
    url = f"https://amazon.com/-es/dp/{sku}"
    # playload = {'api_key': conf.API_TOKEN, 'url': url}
    # proxy_url = conf.API_BASE_URL + urlencode(playload)
    # print(url)
    return url


def get_header() -> dict:
    """ Retorna un diccionario con los encabezados para la peticion con rotacion de users Agents

    Returns:
        dict: diccionario de encabezados
    """
    # conf.headers.update({"User-Agent": random.choice(users_agents)})
    conf.headers.update({"User-Agent": generate_user_agent()})
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
        "http": proxy_url
    }


    
def sku_titulo(conjunto):
    return json.loads(redis.spop(conjunto).decode("utf-8"))
    
if __name__ == '__main__':
    print(sku_titulo("skus_extract_andres")['sku'])
