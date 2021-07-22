import os
directorio_actual = os.path.dirname(os.path.realpath(__file__))

# base de datos

DB = {
    'host': '192.168.1.25',
    'user': 'root',
    'password': '',
    'database': 'bawcommerce'
}

# DB = {
#     'host': 'db-bawconexion.c3cy223njycx.us-east-1.rds.amazonaws.com',
#     'user': 'admin',
#     'password': '#125899+*',
#     'database': 'bawcommerce'
# }


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US,en;q=0.8",
    "Referer": "https://www.google.com/"

}


# print(headers)
# API_TOKEN = "8e34d636585f179c44adcc9ecb8ede92"

# API_BASE_URL = "http://api.scraperapi.com/?"


# max_requests = 2 * 10**6  # two million

# Threads - Hilos
#para 50 proxies mantener hilos al 40% de la totalidad de estos, en este caso 20 hilos
max_hilos = 18


# Redis
# redis_host  =  "localhost"
redis_host = "192.168.1.34"
redis_port = 6379
redis_db = 0


log_stdout = True

#listado de proxies
proxy = [
    "192.198.117.139:7732",
    "154.13.88.167:6256",
    "23.229.19.57:8652",
    "154.13.91.207:7553",
    "107.152.250.215:8271",
    "170.244.92.201:8761",
    "209.127.96.136:7731",
    "23.254.69.229:9235",
    "45.57.243.224:7765",
    "191.102.158.184:8248",
    "209.127.165.109:7201",
    "23.250.71.178:6769",
    "45.72.119.180:9256",
    "23.250.57.141:8648",
    "154.13.90.147:7237",
    "185.245.24.197:6202",
    "69.58.9.49:7119",
    "23.236.196.148:6238",
    "23.254.113.151:6220",
    "209.127.96.175:7770",
    "23.236.247.240:8272",
    "23.236.196.123:6213",
    "209.127.170.194:8287",
    "45.72.40.147:9241",
    "170.244.92.59:8619",
    "23.254.76.142:7234",
    "23.236.247.156:8188",
    "192.241.104.236:8330",
    "104.144.34.68:7652",
    "192.241.104.216:8310",
    "144.168.241.22:8616",
    "170.244.92.43:8603",
    "192.186.176.122:8172",
    "192.198.117.224:7817",
    "107.152.192.101:7156",
    "23.236.196.194:6284",
    "138.128.97.103:7693",
    "191.102.158.97:8161",
    "107.152.170.129:9180",
    "138.128.97.181:7771",
    "23.254.76.22:7114",
    "170.244.93.231:7792",
    "45.72.95.236:8274",
    "104.144.3.110:6189",
    "154.13.93.147:8494",
    "45.224.255.161:9727",
    "45.224.255.186:9752",
    "23.236.196.206:6296",
    "45.72.65.187:8770",
    "45.57.242.83:8623",

]

proxy_user = "ikssgzcs"
proxy_password = "d785os9z1igd"