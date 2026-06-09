import time

import redis
from flask import Flask
# Flask приложение
app = Flask(__name__)
# Клиент для подключения к Redis по адресу redis:6379
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    return cache.incr('hits')


@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)
import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    return cache.incr('hits')


@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)
