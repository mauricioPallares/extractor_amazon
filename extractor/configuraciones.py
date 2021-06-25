import os
import random
directorio_actual = os.path.dirname(os.path.realpath(__file__))

# base de datos

# DB = {
#     'host': '192.168.1.25',
#     'user': 'root',
#     'password': '',
#     'database': 'bawcommerce'
# }

DB = {
    'host': 'db-bawconexion.c3cy223njycx.us-east-1.rds.amazonaws.com',
    'user': 'admin',
    'password': '#125899+*',
    'database': 'bawcommerce'
}


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US,en;q=0.8",
    "Referer": "http://www.google.com/"

}

# headers.update({"User-Agent": random.choice(User_Agent)})

# print(headers)
API_TOKEN = "8e34d636585f179c44adcc9ecb8ede92"

API_BASE_URL = "http://api.scraperapi.com/?"


# max_requests = 2 * 10**6  # two million

# Threads
max_threads = 100


# Redis
# redis_host  =  "localhost"
redis_host = "192.168.1.34"
redis_port = 6379
redis_db = 0


log_stdout = True


proxy = []

proxy_user = ""
proxy_password = ""
proxy_port = ""