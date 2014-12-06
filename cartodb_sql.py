from cartodb import CartoDBAPIKey, CartoDBException
import os

CDB_USER = os.environ.get('CDB_USER')
CDB_API_KEY = os.environ.get('CDB_API_KEY')

cl = CartoDBAPIKey('3b5307c17734143a63adaacf0e9544f59264fdfb', 'loglock')

def location_intersects(lat, lon):
    results = cl.sql('select count(*) from bboxes where st_intersects(CDB_LatLng(%f, %f), the_geom)' %(lat,lon))
    return results['rows'][0]['count']

