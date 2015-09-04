
# ESA's Scientific Data Hub has two endpoints that
# accept requests in a different format.

# Open Search (SOLR) seems to allow more flexible queries, including geographic searches.


ODATA_ROOT_URI = 'https://scihub.esa.int/dhus/odata/v1'
SOLR_ROOT_URI = 'https://scihub.esa.int/dhus'

SUPPORTED_KEYWORDS = [
    'platformname', 'beginposition', 'endposition', 'ingestiondate',
    'collection', 'filename', 'footprint', 'orbitnumber', 'lastorbitnumber',
    'orbitdirection', 'polarisationmode', 'producttype', 'relativeorbitnumber',
    'lastrelativeorbitnumber', 'sensoroperationalmode', 'swathidentifier'
]