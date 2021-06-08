import redis, re

r = redis.Redis()


var = None
patron = re.compile('(?<="hiRes":")(.*?)(?=")', re.MULTILINE | re.DOTALL)
print(type(str(var)))
print(str(var))

imagenes = re.findall(patron, str(var))
# print(r.spop('set'))
print(imagenes)