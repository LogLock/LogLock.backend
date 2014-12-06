from flask import Flask, jsonify, request, url_for
import json, urllib2, os

from utils import jsonp, safe_url_for
from models import is_safe, send_push, geocode_ip
from cartodb_sql import location_intersects

from flask.ext.cache import Cache
from flask.ext.mandrill import Mandrill

app = Flask(__name__)
app.config.from_object('settings')

if os.environ.get('REDISTOGO_URL'):
    cache = Cache(app,config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': os.environ.get('REDISTOGO_URL')})
else:
    cache = Cache(app,config={'CACHE_TYPE': 'simple'})

mandrill = Mandrill(app)


@app.route("/test/push")
def token_push():
    send_push(os.environ.get('PUSHBULLET_TOKEN'), 'foo')
    return "push sent"

@app.route("/test/ip")
def ip_locate():
    ip = request.access_route[0]
    geocode = cached_geocode_ip(ip)
    return jsonify(ip=geocode, 
                   route=request.access_route, 
                   location_intersects=location_intersects(geocode['lat'], geocode['lon']) if 'lon' in geocode.keys() else False)

@app.route('/')
def hello():
    data = []
    for rule in app.url_map.iter_rules():
        if safe_url_for(rule):
            data.append([list(rule.methods), rule.endpoint, url_for(rule.endpoint)])
    return jsonify(routes=data)

@app.route('/auth', methods=['POST'])
@jsonp
def auth():
    return jsonify(response=is_safe(request.form, mandrill)) # ugh

@app.route('/config')
def config():
    if request.method == 'GET':
        return jsonify(data=None)
    return jsonify(status='ok')


@cache.memoize(timeout=36000)
def cached_geocode_ip(ip_address):
    return geocode_ip(ip_address)

app.config['DEBUG'] = os.environ.get('DEBUG', False)
if __name__ == '__main__':
    app.debug = True
    app.run()
