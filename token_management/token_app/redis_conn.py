import redis

def connection():
    r = redis.Redis(decode_responses=True)
    return r

def db2():
    r=redis.Redis(db=1,decode_responses=True)
    return r