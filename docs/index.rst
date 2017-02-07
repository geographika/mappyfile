mappyfile
=========

A Python library to create, parse, and modify `MapServer <http://mapserver.org/documentation.html>`_ Mapfiles. 

+ Python 2 and 3 compatible
+ Pure Python - no MapServer dependencies

.. toctree::
    :maxdepth: 2
    :numbered:
    :titlesonly:

    parser.rst
    transformer.rst
    pretty_printing.rst
    mapfile.rst


.. image:: images/class_parsed.png    

What is mappyfile?
------------------

**Mapfile** Mapfile is the declarative language that MapServer uses to define data connections, 
map styling, templating, and server directives. Its format is xml-like and hierarchical, 
with closing END tags, but the format is not xml.

**MapScript** - MapScript is an alternative the the CGI application of mapserv that allows you to 
program the MapServer object API in many languages.

http://mapserver.org/el/glossary.html

Example use cases:

* Easily generate development, staging, and production Mapfiles from the same source
* Create Mapfiles for different datasets from the same source
* Create, manipulate, and test Mapfiles from within Python

Why?
----

MapScript "bindings" are available in several different languages thanks to SWIG - which creates wrapper 
code for C. 

Sean Gillies was the MapScript maintainer for several years (until 2006). A couple of his last blog
posts on MapScript make a strong case for working with Mapfiles rather than MapScript. 

	*"Cease, or at the very least, minimize your use of MapServer's various language bindings. 
	Instead, embrace MapServer's domain-specific language (DSL) and write more of the declarative 
	cartographic scripts known as mapfiles. Use the mapserv (or shp2img) program to compile these 
	scripts into images. This is the path to happiness and prosperity."*

	Sean Gillies - `Stop using MapScript`_

A later post listed the benefits of this approach. 

	*"the instructions encoded in a MapServer mapfile comprise a domain-specific language..
	to embrace the map language is to benefit from simplicity, usability, and portability."*

	Sean Gillies - `Declarative Maps`_

The concept of the Mapfile as a DSL has been implemented a few times. A Python
`Mapfile builder`_ written by Norman Vine used an XML approach.

More recently the Node module `node-mapserv`_ provides support for declarative mapfile programming. 
As the author notes: 

	*node-mapserv is not MapScript for Node. Instead it provides a simple declarative API for 
	rendering mapserver mapfiles..most of what can be accomplished imperatively 
	using mapscript can be done declaratively by custom generating new mapfiles and tweaking 
	existing mapfiles*

API Examples
------------

This section details the proposed use of the ``mappyfile`` library. The API will be similar to Python's `configparser API <https://docs.python.org/3/library/configparser.html#mapping-protocol-access>`_. 

+ all keys will be lower case
+ all values will be returned as strings by default from the parsing (assume this is the case, or could convert integers etc.)

Accessing Values
++++++++++++++++

.. literalinclude:: examples/accessing_values.py
   :language: python
  
Modifying Values
++++++++++++++++

.. literalinclude:: examples/modifying_values.py
   :language: python
   :start-after: # START OF API EXAMPLE
   :end-before: # END OF API EXAMPLE

Adding Items
++++++++++++

Adding a new layer:

.. literalinclude:: examples/adding_values.py
   :language: python
   :start-after: # START OF ADD LAYER EXAMPLE
   :end-before: # END OF ADD LAYER EXAMPLE

Adding a new class to a layer:

.. literalinclude:: examples/adding_values.py
   :language: python
   :start-after: # START OF ADD CLASS EXAMPLE
   :end-before: # END OF ADD CLASS EXAMPLE
   
.. _testing:

Testing
-------

Testing - there are many sample Mapfiles available in the testing suite of MapServer:

+ https://github.com/mapserver/mapserver/tree/master/msautotest/misc
+ https://github.com/mapserver/mapserver/tree/master/msautotest/wxs
+ https://github.com/mapserver/mapserver/tree/master/msautotest/renderers
+ https://github.com/mapserver/mapserver/tree/master/msautotest/gdal

These have been downloaded and added to the ``/tests`` folder. This folder also contains a script to download these files again in the future.

..
    https://tox.readthedocs.io/en/latest/

..
    http://stackoverflow.com/questions/600079/how-do-i-clone-a-subdirectory-only-of-a-git-repository

Future Development
------------------

+ Enable MapServer to accept a "Mapfile" as a stream: https://github.com/mapserver/mapserver/issues/4031
+ Read MapFiles from URLs

.. _Stop using MapScript: https://sgillies.net/2006/11/29/stop-using-mapscript.html
.. _Declarative Maps: https://sgillies.net/2006/12/01/declarative-maps.html
.. _Mapfile builder: https://web.archive.org/web/20090106070607/http://think.random-stuff.org/FrontPage/archive/2006/07/mapfile-builder
.. _node-mapserv: https://www.npmjs.com/package/mapserv