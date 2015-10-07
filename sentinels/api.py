
import os
import json
import requests

from requests.auth import HTTPBasicAuth

from sentinels import ODATA_ROOT_URI, SOLR_ROOT_URI
from sentinels import MaintenanceDowntimeError
from sentinels import parse, format


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


def search(
    aoi=None, rows=None, offset=None, platformname=None, begin_position=None, end_position=None,
    ingestion_date=None, filename=None, orbit_number=None, last_orbit_number=None,
    orbit_direction=None, polarization_mode=None, product_type=None, relative_orbit_number=None,
    last_relative_orbit_number=None, sensor_operational_mode=None, swath_identifier=None):
    """
    Get metadata on products hosted by the Scientific Data Hub.

    :param aoi:
        Area of interest as a dictionary representation of a geojson feature
    :param rows:
        The number of rows to return
    :param offset:
        The row starting offset
    :param platformname:
        The platform name (e.g. Sentinel-1, Sentinel-2)
    :param begin_position:
        A time interval search based on the sensing start time. This should be a tuple
        containing a start time and end time.
    :param end_position:
        A time interval search based on the sensing end time. This should be a tuple
        containing a start time and end time.
    :param ingestion_date:
        A time interval search based on the time of publication of the product on the Data Hub.
        This should be a tuple containing a start time and end time.
    :param filename:
    :param orbit_number:
    :param last_orbit_number:
    :param orbit_direction:
    :param polarization_mode:
    :param product_type:
    :param relative_orbit_number:
    :param last_relative_orbit_number:
    :param sensor_operational_mode:
    :param swath_identifier:
    """
    kwargs = locals()

    uri = os.path.join(SOLR_ROOT_URI, 'search')

    params = {}
    if rows:
        params['rows'] = rows
    if offset:
        params['start'] = offset
    if aoi:
        kwargs['footprint'] = format.feature(aoi)
    if begin_position:
        kwargs['begin_position'] = format.time_interval(begin_position)
    if end_position:
        kwargs['end_position'] = format.time_interval(end_position)
    if ingestion_date:
        kwargs['ingestion_date'] = format.time_interval(ingestion_date)

    params['q'] = format.query_string(**kwargs)

    r = requests.get(uri, auth=get_auth(), params=params)

    if len(r.history) > 0:
        if r.history[0].status_code == 302:
            raise MaintenanceDowntimeError()

    r.raise_for_status()
    return parse.search(r.text)


def thumbnail():
    """docstring for thumbnail"""
    pass