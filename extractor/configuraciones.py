import os

directorio_actual = os.path.dirname(os.path.realpath(__file__))

#base de datos 

DB = {
    'host': '192.168.1.25',
    'user': 'root',
    'password': '',
    'database': 'bawcommerce'
}

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
}


API_TOKEN ="8e34d636585f179c44adcc9ecb8ede92"

API_BASE_URL ="http://api.scraperapi.com/?"


max_requests = 2 * 10**6  # two million

# Threads
max_threads = 10



# Redis
redis_host  =  "localhost"
redis_port  =  6379
redis_db  =  0