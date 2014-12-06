from random import  randint

import urllib2, json

from pushbullet import PushBullet
from os import environ

from cartodb_sql import mark_login_attempt

''' 
Checks if the current login attempt is a security threat or not.
Performs the required action in each case
'''
def is_safe(form, ip, geocoded_ip, mandrill):
    ip        = ip
    latitude  = form.get('latitude', None)
    longitude = form.get('longitude', None)
    os        = form.get('os', None)
    mobile    = form.get('isMobile', None)
    browser   = form.get('browser', None)

    if latitude == None and longitude == None:
        latitude = geocoded_ip['lat']
        longitude = geocoded_ip['lon']

    safety_status = mark_login_attempt(ip=ip, latitude=latitude, 
        longitude=longitude, os=os, mobile=mobile, browser=browser)

    auth_code = '%06d' % randint(0,999999)
    if safety_status < 1:
        send_push("Confirm your access", "Suspicious access detected from IP %s, confirm with code %s" % (ip, auth_code))
        send_mail(mandrill, 'zen@itram.es', latitude, longitude, ip, auth_code)
    return {
        'safety_code': safety_status, 
        'token': auth_code,
        'debug': [ip, latitude, longitude, os, mobile, browser]
        }# send SMS, mail...

def send_push(message, body, lat=40.4086, lon=-3.6922, pushbullet_token=environ.get('PUSHBULLET_TOKEN')):
    """ Sends a foo location to Pushbullet """
    pb = PushBullet(pushbullet_token)
    success, push = pb.push_link("Login from suspicious location detected now!", "http://maps.google.com/maps?&z=10&q=%f,+%f&ll=%f+%f" % (lat, lon, lat, lon), "A suspicious login has appeared, try to guess who is it")
    return success

def send_mail(mandrill, to, latitude, longitude, ip, safety_code):
    gmaps_uri = "http://maps.googleapis.com/maps/api/staticmap?center=%s,%s&zoom=15&size=400x400&markers=color:red%%7Clabel:S%%7C%s,%s&sensor=true" % (latitude, longitude, latitude, longitude)
    mandrill.send_email(
        from_email='someone@yourdomain.com',
        subject='[LogLock] Suspicious login attempt detected',
        to=[{'email': to}],
        html='''
        An access attempt has been logged from a suspicious location:
        <p><img src="%s" /></p>
        <p>IP address: %s</p>

        Please confirm it is you with the following code: <b>%s</b>

        ''' %(gmaps_uri, ip, safety_code)
    )

def geocode_ip(ip_addr):
    """ Geocodes a given IP Address """
    data = json.load(urllib2.urlopen("http://ip-api.com/json/%s" % ip_addr))
    print "Geocoded data: %s" % data
    return data

