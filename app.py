from flask import Flask, jsonify, request, url_for
import json, urllib2, os

from utils import jsonp, safe_url_for
from models import is_safe, send_push, geocode_ip
from cartodb_sql import location_intersects

from flask.ext.cache import Cache
from flask.ext.mandrill import Mandrill
from flask.ext.cors import CORS, cross_origin

app = Flask(__name__)
app.config.from_object('settings')

if os.environ.get('REDISTOGO_URL'):
    cache = Cache(app,config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': os.environ.get('REDISTOGO_URL')})
else:
    cache = Cache(app,config={'CACHE_TYPE': 'simple'})

mandrill = Mandrill(app)
cors = CORS(app)

CLIENT_IP = None

__VERSION__ = 0.1

@app.before_request
def before():
    CLIENT_IP = request.access_route[0]

@app.route("/test/push")
def token_push():
    send_push(os.environ.get('PUSHBULLET_TOKEN'), 'foo')
    return "push sent"

@app.route("/test/ip")
def ip_locate():
    ip = CLIENT_IP
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
@cross_origin()
@jsonp
def auth():
    return jsonify(response=is_safe(request.form, CLIENT_IP, mandrill)) # ugh

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
    app.run(debug=True)
