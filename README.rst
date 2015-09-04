Sentinels Scientific Data Hub Client Library
============================================

Sentinels Scientific Data Hub provides an archive of Sentinels data. Currently only Sentinel-1 data is available, with Sentinel-2 to be available in the near future.

This is a client library that massages all responses into geojson for interoperability with various geojson-aware tools.

Usage
-----

To access data with this library an account with the Sentinels Scientific Data Hub is required.

https://scihub.esa.int/

Set your account credentials to environment variables. They are required to make all requests to the archive.

.. code-block:: bash

    export SENTINELS_USERNAME=[username]
    export SENTINELS_PASSWORD=[password]


Command line
************

.. code-block:: bash

    sentinel search
    cat aoi.geojson | sentinel search


Python
******

TBD


Reference
---------

https://scihub.esa.int//twiki/do/view/SciHubUserGuide/BatchScripting