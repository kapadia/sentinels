
import json
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, tostring

from shapely import wkt
from shapely.geometry import mapping


NAMESPACES = {
    "opensearch": "http://a9.com/-/spec/opensearch/1.1/",
    "atom": "http://www.w3.org/2005/Atom"
}


def get_text(item):
    name = item.tag.split('}')[-1]
    return name, item.text


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


def get_array(item):
    name = item.attrib.get('name')
    value = [ c.text for c in item.getchildren() ]

    return name, value


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
        'date': get_string,
        'link': get_link,
        'id': get_string,
        'summary': get_text,
        'title': get_text,
        'arr': get_array,
    }

    blacklist = ['gmlfootprint', 'footprint']

    feature = {
        'type': 'Feature',
        'properties': {
            'links': {}
        }
    }

    for c in entry.getchildren():
        tag = c.tag.split('}')[-1]

        key, value = _get[tag](c)

        if tag == 'id':
            feature['id'] = value
        elif tag == 'link':
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

    .. todo: Assert that the response contains `totalResults`,
             `startIndex` and `itemsPerPage`. Fix if issue arises.
    """
    root = ElementTree.fromstring(response)

    return {
        "title": root.find("atom:title", NAMESPACES).text,
        "subtitle": root.find("atom:subtitle", NAMESPACES).text,
        "updated": root.find("atom:updated", NAMESPACES).text,
        "id": root.find("atom:id", NAMESPACES).text,
        "totalResults": int(root.find("opensearch:totalResults", NAMESPACES).text),
        "startIndex": int(root.find("opensearch:startIndex", NAMESPACES).text),
        "itemsPerPage": int(root.find("opensearch:itemsPerPage", NAMESPACES).text),
        "type": "FeatureCollection",
        "features": [
            get_entry(entry) for entry in root.findall('atom:entry', NAMESPACES)
        ]
    }

