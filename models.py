from random import choice

import urllib2, json

from pushbullet import PushBullet

''' 
Checks if the current login attempt is a security threat or not.
Performs the required action in each case
'''
def is_safe(form, mandrill):
    ip      = form.get('ip', None)
    geo     = form.get('geo', None)
    os      = form.get('os', None)
    browser = form.get('browser', None)
    # check against our database
    safety_status = choice(range(-1, 2))
    return {'safety_code': safety_status, 'debug': [ip, geo, os, browser]}# send SMS, mail...

def send_push(pushbullet_token, message, lat=40.4086, lon=-3.6922):
    """ Sends a foo location to Pushbullet """
    pb = PushBullet(pushbullet_token)
    success, push = pb.push_link("Login from suspicious location detected now!", "http://maps.google.com/maps?&z=10&q=%f,+%f&ll=%f+%f" % (lat, lon, lat, lon), "A suspicious login has appeared, try to guess who is it")
    return success

def send_mail(mandrill, to):
    mandrill.send_email(
        from_email='someone@yourdomain.com',
        subject='Blocked suspicious login attempt @twitter',
        to=[{'email': to}],
        text='''An attack has been detected and blocked (LND=>NY login with 5h difference).
            Authorize this access by [...]'''
    )

def geocode_ip(ip_addr):
    """ Geocodes a given IP Address """
    data = json.load(urllib2.urlopen("http://ip-api.com/json/%s" % ip_addr))
    print "Geocoded data: %s" % data
    return data

