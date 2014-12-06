from flask import Flask, jsonify, request
import json, urllib2, os

from utils import jsonp
from models import is_safe, send_push, geocode_ip

from flask.ext.mandrill import Mandrill

app = Flask(__name__)
app.config.from_object('settings')

mandrill = Mandrill(app)


@app.route("/test/push")
def token_push():
    send_push(os.environ.get('PUSHBULLET_TOKEN'), 'foo')
    return "push sent"

@app.route("/test/ip")
def ip_locate():
    if len(request.access_route) > 1:
        ip = request.access_route[-1]
    else:
        ip = request.access_route[0]
    return jsonify(geocode_ip(ip))

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/auth', methods=['POST'])
@jsonp
def auth():
    return jsonify(safe=is_safe(request.form, mandrill)) # ugh

@app.route('/config')
def config():
    if request.method == 'GET':
        return jsonify(data=None)
    return jsonify(status='ok')

if __name__ == '__main__':
    app.debug = True
    app.run()
