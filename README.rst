Sentinels Scientific Data Hub Client Library
============================================

Reference: https://scihub.esa.int//twiki/do/view/SciHubUserGuide/BatchScripting


Usage
-----

This client uses ESA's Sentinels Scientific Data Hub. An account with their service is required to use the library.

https://scihub.esa.int/


Set your account credentials to environment variables:

.. code-block:: bash

    export SENTINEL_USERNAME=[username]
    export SENTINEL_PASSWORD=[password]


These credentials are required to make all requests.


.. code-block:: bash

    sentinel search
    cat aoi.geojson | sentinel search