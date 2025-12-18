.. _config-files:

Config Files
============

.. note:: New in mappyfile 1.1.0

MapServer 8.0 introduced a new `CONFIG <https://mapserver.org/mapfile/config.html>`__ file. mappyfile is able to parse
and write these config files similar to Mapfiles. Validation against a CONFIG schema is also supported.
The CONFIG file schema can be downloaded directly from this link - :download:`config.json <schemas/config.json>`.

Python Usage
------------

.. code-block:: python

    >>> import mappyfile
    >>> import json
    >>> fn = r"C:\MapServer\apps\mapserver.conf"
    >>> d = mappyfile.open(fn)
    >>> print(json.dumps(d["env"], indent=4))
    {
        "ms_map_pattern": ".",
        "proj_data": "C:/MapServer/bin/proj9/share",
        "proj_debug": "3",
        "gdal_driver_path": "C:/MapServer/bin/gdal/plugins",
        "ogcapi_html_template_directory": "C:/MapServer/apps/ogcapi/templates/html-bootstrap4/"
    }
    >>> d["env"]["curl_ca_bundle"] = "C:/MapServer/bin/curl-ca-bundle.crt"
    >>> print(json.dumps(d["env"], indent=4))
    {
        "ms_map_pattern": ".",
        "proj_data": "C:/MapServer/bin/proj9/share",
        "proj_debug": "3",
        "gdal_driver_path": "C:/MapServer/bin/gdal/plugins",
        "ogcapi_html_template_directory": "C:/MapServer/apps/ogcapi/templates/html-bootstrap4/",
        "curl_ca_bundle": "C:/MapServer/bin/curl-ca-bundle.crt"
    }
    >>> print(mappyfile.dumps(d, indent=4))
    CONFIG
        ENV
            ms_map_pattern "."
            proj_data "C:/MapServer/bin/proj9/share"
            proj_debug "3"
            gdal_driver_path "C:/MapServer/bin/gdal/plugins"
            ogcapi_html_template_directory "C:/MapServer/apps/ogcapi/templates/html-bootstrap4/"
            curl_ca_bundle "C:/MapServer/bin/curl-ca-bundle.crt"
        END
        MAPS
            itasca "D:\GitHub\mapserver-demo\itasca.map"
            hello_world "D:\mapserver\msautotest\config\hello_world.map"
        END
        PLUGINS
            "mssql" "C:\MapServer\bin\ms\plugins\mssql2008\msplugin_mssql2008.dll"
        END
    END
    >>> mappyfile.save(d, r"C:\MapServer\apps\mapserver.new.conf")
    'C:\\MapServer\\apps\\mapserver.new.conf'

Command-line Usage
------------------

To validate a config file:

.. code-block:: ps1

    mappyfile validate C:\MapServer\apps\mapserver.conf


To format a config file:

.. code-block:: ps1

    mappyfile format C:\MapServer\apps\mapserver.conf C:\MapServer\apps\mapserver.formatted.conf --indent 2

