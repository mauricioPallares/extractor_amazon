import os
from datetime import datetime
from urlparse import urlparse
import redis

redis = redis.Redis()

import eventlet

import configuraciones as conf 

num_request = 0

def realizar_peticion(url):
    pass


def enCola(sku):
    return redis.sadd("sku en cola", sku)

def 