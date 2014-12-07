# -*- coding: utf-8 -*-
from cartodb import CartoDBAPIKey, CartoDBException

import os
from random import choice

CDB_USER = os.environ.get('CDB_USER', None)
CDB_API_KEY = os.environ.get('CDB_API_KEY', None)

cl = CartoDBAPIKey(CDB_API_KEY, CDB_USER)


def check_login(clientname, username, password):
    
    q = "select geolocation, operating_systems, browsers from company where company_name = '%s' and email = '%s' and password = '%s'" % (clientname, username, password)
    results = cl.sql(q)
    
    print q
    print results
    
    if results['total_rows'] > 0:
        return results['rows']
    
    return None


def get_log(clientname):
    q = "select st_x(a.the_geom) as lng, st_y(a.the_geom) as lat, ip, result, info->'os' as os, info->'browser' as browser from attempt a, company b where a.company_id = b.cartodb_id and b.company_name = '%s'" % clientname
    results = cl.sql(q)
    
    print q
    print results['rows']
    
    if results['total_rows'] > 0:
        return results['rows']

def location_intersects(lat, lon):
    results = cl.sql('select allowed from bboxes where st_intersects(CDB_LatLng(%f, %f), the_geom) limit 1' %(lat,lon))
    print results
    if results['total_rows'] == 0:
        return None
    
    allow = results['rows'][0]['allowed']
    return allow

def mark_login_attempt(ip, latitude, longitude, os, mobile, browser, result):
    args = locals()
    SQL = '''
        insert into attempt(the_geom,ip,info,result) values(CDB_LatLng({lat}, {lon}), '{ip}', '{data}',{result})
    '''
    query = SQL.format(data=', '.join(['%s => "%s"' %(el, args[el]) for el in args]), lat=latitude, lon=longitude, ip=ip, result=result)
    print cl.sql(query)
    

def dummy_create_company(data):
    SQL = '''
            INSERT INTO company 
	            (email, password, company_name, 
	                phone, geolocation_methods, 
                    enabled_browsers, operating_systems)
            VALUES ('{email}', '{password}', '{company_name}', 
       	        '{phone}', {geolocation_methods}, {enabled_browsers}, {operating_systems})'''
    query = SQL.format(*data)
    results = cl.sql(query)
    return results
    
