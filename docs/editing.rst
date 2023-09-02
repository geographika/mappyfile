.. _editing:

Editing a Mapfile
=================

This page gives an overview of how a Mapfile that has been :ref:`transformed <transformer>` into a mappyfile Python
dictionary can be edited. Example of using mappyfile and MapServer Python MapScript are provided side-by-side.

Converting from MapScript
-------------------------

This section has some side-by-side examples of Python MapScript code, and its mappyfile equivalent. 
The simple examples have little difference between them. The power of mappyfile becomes more apparent with the more complicated Mapfile manipulations. 

As mappyfile is simply working with text, you don't have to worry that paths referenced in the Mapfile 
exist on the local machine. This is particularly useful when updating an existing local Mapfile to deploy 
on a production server. 

Updating a Metadata Value
+++++++++++++++++++++++++

Note some of the Python MapScript API has been modified since v7.2 to better match and work
with mappyfile. 

.. code-block:: python

    # mapscript - standard MapScript API
    mymap.setMetaData("ows_title", "My WMS Map")

    # mapscript - new hash table API - added as a convenience 
    # to the Python MapScript bindings only
    mymap["metadata"]["ows_title"] = "My WMS Map"

    # mappyfile
    mymap["metadata"]["ows_title"] = "My WMS Map"

Changing the Error Log Location
+++++++++++++++++++++++++++++++

.. code-block:: python

    # mapscript
    # the next line throws an error unless it is set to a file/location that exists
    mymap.setConfigOption("MS_ERRORFILE", error_log)
    mymap.debug = debug_level # set debug level 

    # mappyfile
    mymap["config"]["ms_errorfile"] = error_log
    mymap["debug"] = debug_level

  
Updating a Validation Setting
+++++++++++++++++++++++++++++

.. code-block:: python

    # mapscript
    if l.validation.get('MYPARAMETER'):
        l.validation.set('MYPARAMETER', filter)


    # mappyfile
    if "MYPARAMETER" in l["validation"]:
        l["validation"]["MYPARAMETER"] = filter

Replacing Classes in a Layer
++++++++++++++++++++++++++++

MapScript (using ``fromstring``): 

.. code-block:: python

    # define class strings
    c1 = """
    CLASS 
        NAME 'The World' 
        STYLE 
            OUTLINECOLOR 0 255 0 
        END
    END"""

    c2 = """
    CLASS
        NAME 'Roads'
        STYLE
            OUTLINECOLOR 0 0 0 
        END
    END"""

    # remove existing classes
    for idx in reversed(range(0, layer.numclasses)):
        layer.removeClass(idx)

    # create a new class object from the strings and add to the layer
    for c in classes:
        clsObj = mapscript.fromstring(c)
        layer.classes.append(clsObj)

mappyfile:

.. code-block:: python

    # define all classes in a single string
    classes = """
    CLASS 
        NAME 'The World' 
        STYLE 
            OUTLINECOLOR 0 255 0 
        END
    END
    CLASS
        NAME 'Roads'
        STYLE
            OUTLINECOLOR 0 0 0 
        END
    END
    """

    # parse the string and replace the existing classes for the layer
    layer["classes"] = mappyfile.loads(classes)


