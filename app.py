from flask import Flask
from pushbullet import PushBullet
import json, urllib2, os
app = Flask(__name__)


def geocode_ip(ip_addr):
    """ Geocodes a given IP Address """
    data = json.load(urllib2.urlopen("http://ip-api.com/json/%s" % ip_addr))
    print "Geocoded data: %s" % data
    return data

def send_push(pushbullet_token, message):
    pb = PushBullet(pushbullet_token)
    pb.push_address("Login from suspicious location detected!", "40.4086, -3.6922")

@app.route("/")
def hello():
    return geocode_ip('47.61.247.27')

@app.route("/push")
def token_push():
    send_push(os.environ.get('PUSHBULLET_TOKEN'), 'foo')

if __name__ == "__main__":
    app.debug = True
    app.run()
