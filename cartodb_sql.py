from cartodb import CartoDBAPIKey, CartoDBException

import os
from random import choice

CDB_USER = os.environ.get('CDB_USER', None)
CDB_API_KEY = os.environ.get('CDB_API_KEY', None)

cl = CartoDBAPIKey(CDB_API_KEY, CDB_USER)

def location_intersects(lat, lon):
    results = cl.sql('select allowed from bboxes where st_intersects(CDB_LatLng(%f, %f), the_geom) limit 1' %(lat,lon))
    if results['total_rows'] == 0:
        return None
    else:
        allow = results['rows'][0]['allowed']
        return allow

def mark_login_attempt(ip, latitude, longitude, os, mobile, browser):
    args = locals()
    SQL = '''
        insert into attempt(the_geom,info) values(CDB_LatLng({lat}, {lon}), '{data}')
    '''
    query = SQL.format(data=', '.join(['%s => "%s"' %(el, args[el]) for el in args]), lat=latitude, lon=longitude)
    print cl.sql(query)
    return choice(range(-1, 2))

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
    
