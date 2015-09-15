
from dateutil.parser import parse
from sentinels import SUPPORTED_KEYWORDS


def feature(geojson):
    """
    Format an area of interest to the format required
    by this service.
    
    :param geojson:
        Dictionary representation of geojson describing a
        region of interest.
    """

    if geojson.get('type') == 'Feature':
        geometry = geojson.get('geometry')
    else:
        geometry = geojson.get('features')[0].get('geometry')

    c = geometry.get('coordinates')
    wkt = 'POLYGON ((%s))' % ', '.join([ "%.16f %.16f" % (x[0], x[1]) for x in c[0] ])

    return '"Intersects(%s)"' % wkt


def time_interval(position):
    """
    Format a time range to the format required by
    the service.
    
    :param position:
        Tuple containing two datetime strings.
    """
    time_range = map(lambda d: parse(d).strftime('%Y-%m-%dT%H:%M:%S.%fZ'), position)
    return '[%s]' % ' TO '.join(time_range)


def query_string(**kwargs):
    """
    Construct a search query compatible with the OpenSearch endpoint.
    """
    query = ' AND '.join([ "%s:%s" % (k.replace('_', ''), v) for k, v in kwargs.iteritems() if (k.replace('_', '') in SUPPORTED_KEYWORDS) and v ])
    query = query or '*'

    return query