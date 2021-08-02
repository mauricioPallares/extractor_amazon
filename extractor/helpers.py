import eventlet
import json
import redis
import random
from datetime import datetime
import configuraciones as conf
from user_agent import generate_user_agent

redis = redis.StrictRedis(host=conf.redis_host,
                          port=conf.redis_port, db=conf.redis_db)

requests = eventlet.import_patched('requests.__init__')
time = eventlet.import_patched('time')


REINTENTOS = 5


def normal_request(sku: str):
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
            
            r = requests.get(
                url=amazon_url(sku),
                headers=get_header(),
                proxies=proxies)
            
            if r.status_code in [200, 404]:
                ya_descargado("totales", sku)
                break

            # r = ""
        except Exception as e:
            # error quitar r
            log(f"ERROR: {e}", sku=sku)
            no_descargado("totales", sku)
            time.sleep(5)
            reintentos += 1

    if r.status_code == 429:
        log(f"ERROR: requests status_code {r.status_code}", sku=sku)
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


def cola_actualizacion():
    return redis.spop("sku_652703678").decode("utf-8")


def cola_url():
    return redis.spop("lista_urls").decode("utf-8")


def counts(conjunto):
    return redis.scard(conjunto)


def num_cola():
    return redis.scard("sku_652703678")


def no_descargado(cliente, sku):
    return redis.sadd(f"no_descargados_{cliente}", sku)


def ya_descargado(cliente, sku):
    return redis.sadd(f"descargados_{cliente}", sku)


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


def get_proxy_splash():
    if not conf.proxy or len(conf.proxy) == 0:
        return None
    
    return random.choice(conf.proxy).split(":")


def splash_request(sku: str, endpoint: str = "execute"):
    splash_url = f"http://localhost:8050/{endpoint}"
    target_url = f"https://www.amazon.com/dp/{sku}/ref=olp_aod_redir_impl1?_encoding=UTF8&aod=1"

    ip, port = get_proxy_splash()

    lua_source = """function main(splash, args)

    splash:on_request(
        function(request)

            request:set_proxy{
                host = "{ip}",
                port = {port},
                username = "{proxy_user}",
                password = "{proxy_pass}",
                type = "SOCKS5"
            }
        end
    )
    splash:go(args.url)

    splash:wait(0.5)

    return splash:html()

end"""

    lua_source = lua_source.replace("{proxy_user}", conf.proxy_user)
    lua_source = lua_source.replace("{proxy_pass}", conf.proxy_password)
    lua_source = lua_source.replace("{ip}", ip)
    lua_source = lua_source.replace("{port}", port)

    headers = {
        "Content-Type": "application/json",
        "User-Agent": generate_user_agent(),
        }
    try:
        print("realizando peticion")
        response = requests.get(
            url=splash_url,
            headers=headers,
            params={'lua_source': lua_source, 'url': target_url})

    except Exception as e:
        print(e, "error de peticion")
        return None

    else:
        if response.status_code not in [200, 404]:
            # print(response.text)
            no_descargado("totales", sku)

        if response.status_code != 200:
            return None

        print("devolviendo la salida")
        return response



if __name__ == '__main__':


    splash_request(sku="1574869493")


    # from modelo import con, cursor

    # nombre_paquete = "skus_totales"

    # # sql = "SELECT sku FROM productos_andres"

    # # cursor.execute(sql,)
    # # datos = cursor.fetchall()

    # # print(f"Agregando la primera carga de {len(datos)}")

    # # for dato in datos:
    # #     enCola(nombre_paquete, dato['sku'])

    # sql = "SELECT sku FROM productos_paula"

    # cursor.execute(sql,)
    # datos = cursor.fetchall()

    # print(f"Agregando la segunda carga de {len(datos)}")
    # for dato in datos:
    #     enCola(nombre_paquete, dato['sku'])
