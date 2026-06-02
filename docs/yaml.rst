.. _yaml:

YAML Support
============

YAML support was added in **version 1.2.0** of Mappyfile. The YAML format is supported for both loading and dumping Mapfiles.
YAML is a human-readable data serialization format that is commonly used for configuration files.
It is often preferred over JSON for its readability and support for comments.

Python API Support:

- :ref:`yaml-api`

CLI Support:

- :ref:`client-yaml-export`
- :ref:`client-yaml-import`

Python Example
++++++++++++++

.. literalinclude:: examples/yaml_example.py
   :language: python

Example YAML
------------

The following example shows how to export a Mapfile to YAML format using the command-line interface.

.. code-block:: bat

    mappyfile yaml-export ./tests/mapfiles/itasca2.map ./docs/examples/itasca.yaml

The Mapfile used in this example is the "classic" MapServer Itasca map (``itasca2.map`` from the tests folder),
and the output YAML file is saved to ``docs/examples/itasca.yaml`` and displayed below.

.. literalinclude:: examples/itasca.yaml
   :language: yaml

.. literalinclude:: ../tests/mapfiles/itasca2.map
   :language: mapfile
