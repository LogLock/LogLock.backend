from cartodb import CartoDBAPIKey, CartoDBException

import os
from random import choice

CDB_USER = os.environ.get('CDB_USER', None)
CDB_API_KEY = os.environ.get('CDB_API_KEY', None)

cl = CartoDBAPIKey(CDB_API_KEY, CDB_USER)

def location_intersects(lat, lon):
    results = cl.sql('select count(*) from bboxes where st_intersects(CDB_LatLng(%f, %f), the_geom)' %(lat,lon))
    return results['rows'][0]['count']

def mark_login_attempt(ip, latitude, longitude, os, mobile, browser):
    SQL = '''
        insert into attempt(info) values('{data}')
    '''
    args = locals()
    query = SQL.format(data=', '.join(['%s => "%s"' %(el, args[el]) for el in args]))
    print cd.sql(query)
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
    
