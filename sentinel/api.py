
import os
import json
import requests
from requests.auth import HTTPBasicAuth

from sentinel import ODATA_ROOT_URI, SOLR_ROOT_URI
from sentinel import parse


def get_auth():

    username = os.environ.get('SENTINEL_USERNAME')
    password = os.environ.get('SENTINEL_PASSWORD')

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


def search(rows=None, start=None):
    """
    Get metadata on products hosted by the Scientific Data Hub.
    """
    uri = os.path.join(SOLR_ROOT_URI, 'search')

    params = { 'q': '*' }
    if rows:
        params['rows'] = rows
    if start:
        params['start'] = start
    r = requests.get(uri, auth=get_auth(), params=params)

    return parse.search(r.text)


def thumbnail():
    """docstring for thumbnail"""
    pass