import sys
import os
import socket
from redis import Redis, RedisError

redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

def application(environ, start_response):
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"
    status = '200 OK'
    output = bytes(html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits), 'utf-8')

    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]

