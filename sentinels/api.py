
import os
import json
import requests
from requests.auth import HTTPBasicAuth
from shapely.geometry import shape

from sentinels import ODATA_ROOT_URI, SOLR_ROOT_URI, SUPPORTED_KEYWORDS
from sentinels import parse


def get_auth():

    username = os.environ.get('SENTINELS_USERNAME')
    password = os.environ.get('SENTINELS_PASSWORD')

    return HTTPBasicAuth(username, password)


def ping():
    """
    Test function for pinging the API.
    """
    uri = ODATA_ROOT_URI
    
    params = { '$format': 'json' }
    r = requests.get(uri, auth=get_auth(), params=params)
    
    return r.text


def metadata_service():
    """
    Returns a description the data model hosted by the Scientific Data Hub.
    """
    uri = os.path.join(ODATA_ROOT_URI, '$metadata')
    
    r = requests.get(uri, auth=get_auth())
    
    return r.text


def collections(raw=False):
    """
    Get metadata on products hosted by the Scientific Data Hub.
    
    :param raw:
        Flag to return the raw form response from the data hub.
    """
    uri = os.path.join(ODATA_ROOT_URI, 'Collections')

    params = { '$format': 'json' }
    r = requests.get(uri, auth=get_auth(), params=params)

    if raw:
        return json.loads(r.text)
    else:
        return parse.collections(r.text)


def construct_query_string(**kwargs):
    """
    Construct a search query compatible with the OpenSearch endpoint.
    """
    query = ' AND '.join([ "%s:%s" % (k.replace('_', ''), v) for k, v in kwargs.iteritems() if (k.replace('_', '') in SUPPORTED_KEYWORDS) and v ])
    query = query or '*'

    return query


def search(
    aoi=None, rows=None, offset=None, platformname=None, begin_position=None, end_position=None,
    start_date=None, end_date=None, filename=None, orbit_number=None, last_orbit_number=None,
    orbit_direction=None, polarization_mode=None, product_type=None, relative_orbit_number=None,
    last_relative_orbit_number=None, sensor_operational_mode=None, swath_identifier=None):
    """
    Get metadata on products hosted by the Scientific Data Hub.
    """
    kwargs = locals()

    uri = os.path.join(SOLR_ROOT_URI, 'search')

    params = {}
    if rows:
        params['rows'] = rows
    if offset:
        params['start'] = offset
    if aoi:
        if aoi.get('Type') == 'Feature':
            geometry = aoi.get('geometry')
        else:
            geometry = aoi.get('features')[0].get('geometry')
        wkt = shape(geometry).to_wkt()
        kwargs['footprint'] = '"Intersects(%s)"' % wkt

    params['q'] = construct_query_string(**kwargs)

    r = requests.get(uri, auth=get_auth(), params=params)

    return parse.search(r.text)


def thumbnail():
    """docstring for thumbnail"""
    pass