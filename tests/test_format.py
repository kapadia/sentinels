
import json
from sentinels import format


GEOJSON_FEATURE_COLLECTION = """{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              -83.67650985717773,
              37.77234303484361
            ],
            [
              -83.67650985717773,
              37.814123701604466
            ],
            [
              -83.616943359375,
              37.814123701604466
            ],
            [
              -83.616943359375,
              37.77234303484361
            ],
            [
              -83.67650985717773,
              37.77234303484361
            ]
          ]
        ]
      }
    }
  ]
}
"""

GEOJSON_FEATURE = """{
  "type": "Feature",
  "properties": {},
  "geometry": {
    "type": "Polygon",
    "coordinates": [
      [
        [
          -83.67650985717773,
          37.77234303484361
        ],
        [
          -83.67650985717773,
          37.814123701604466
        ],
        [
          -83.616943359375,
          37.814123701604466
        ],
        [
          -83.616943359375,
          37.77234303484361
        ],
        [
          -83.67650985717773,
          37.77234303484361
        ]
      ]
    ]
  }
}
"""

EXPECTED_FEATURE_QUERY = '"Intersects(POLYGON ((-83.6765098571777344 37.7723430348436082, -83.6765098571777344 37.8141237016044656, -83.6169433593750000 37.8141237016044656, -83.6169433593750000 37.7723430348436082, -83.6765098571777344 37.7723430348436082)))"'

def test_feature_feature_collection():
    geojson = json.loads(GEOJSON_FEATURE_COLLECTION)
    assert EXPECTED_FEATURE_QUERY == format.feature(geojson)


def test_feature_feature():
    geojson = json.loads(GEOJSON_FEATURE)
    assert EXPECTED_FEATURE_QUERY == format.feature(geojson)


def test_time_interval():

    time_interval = ('2015-09-15', '2015-09-16')
    expected = '[2015-09-15T00:00:00.000000Z TO 2015-09-16T00:00:00.000000Z]'

    assert expected == format.time_interval(time_interval)


def test_query_string():
    kwargs = {
        'ingestion_date': ('2015-09-15', '2015-09-16'),
        'orbit_number': '100',
        'platformname': 'Sentinel-1',
    }

    kwargs['ingestion_date'] = format.time_interval(kwargs['ingestion_date'])
    
    # TODO: Expected loop over dictionary may not be deterministic.
    expected = "orbitnumber:100 AND ingestiondate:[2015-09-15T00:00:00.000000Z TO 2015-09-16T00:00:00.000000Z] AND platformname:Sentinel-1"

    assert expected == format.query_string(**kwargs)
