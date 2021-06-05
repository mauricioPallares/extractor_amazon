import redis

r = redis.Redis()

r.set('foo', 'bar')

r.get('foo')

print(r.get('foo'))