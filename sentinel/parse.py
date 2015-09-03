
# The Data Hub JSON response is messy. These functions select
# relevant information to be passed to the user in a less messy
# form. Please submit a GitHub issue if there's a field that
# should be included in the parsed response.

import json
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, tostring

from shapely import wkt
from shapely.geometry import mapping


NAMESPACES = {
    "opensearch": "http://a9.com/-/spec/opensearch/1.1/",
    "atom": "http://www.w3.org/2005/Atom"
}


def get_string(item):
    name = item.attrib.get('name')
    value = item.text

    return name, value


def get_integer(item):
    name = item.attrib.get('name')
    value = int(item.text)

    return name, value


def get_boolean(item):
    name = item.attrib.get('name')
    value = True if item.text == 'true' else False

    return name, value


def get_date(item):
    name = item.attrib.get('name')
    value = item.text

    return name, value


def get_array():
    pass


def get_footprint(footprint):
    g = wkt.loads(footprint)
    return mapping(g)


def get_link(item):
    
    rel = item.attrib.get('rel')
    href = item.attrib.get('href')

    if rel == 'icon':
        return 'thumbnail', href
    elif rel == 'alternative':
        return 'alternative', href
    else:
        return 'full', href


def get_entry(entry):

    _get = {
        'str': get_string,
        'int': get_integer,
        'bool': get_boolean,
        'arr': get_array,
        'date': get_date,
        'link': get_link
    }

    blacklist = ['title', 'id', 'summary', 'gmlfootprint', 'footprint']
    whitelist = ['str', 'int', 'bool', 'date', 'link']

    feature = {
        'type': 'Feature',
        'properties': {
            'links': {}
        }
    }
    for c in entry.getchildren():
        tag = c.tag.split('}')[-1]

        if (tag in whitelist):
            key, value = _get[tag](c)
            
            if tag == 'link':
                feature['properties']['links'][key] = value
            elif key not in blacklist:
                feature['properties'][key] = value

            if key == 'footprint':
                feature['geometry'] = get_footprint(value)
            

    return feature


def collections(response):

    data = json.loads(response)['d']['results']

    return [
        { "name": d["Name"], "description": d["Description"] }
        for d in data
    ]


def search(response):
    """
    Parse an XML response from the SOLR endpoint.
    """
    root = ElementTree.fromstring(response)
    
    return {
        "totalResults": int(root.find("opensearch:totalResults", NAMESPACES).text),
        "startIndex": int(root.find("opensearch:startIndex", NAMESPACES).text),
        "itemsPerPage": int(root.find("opensearch:itemsPerPage", NAMESPACES).text),
        "type": "FeatureCollection",
        "features": [
            get_entry(entry) for entry in root.findall('atom:entry', NAMESPACES)
        ]
    }
    
    