Integrating with Python
=======================

This page gives some examples of integrating mappyfile into Python based work flows. 

Displaying Geometry
-------------------

The examples below recreates the sample images used in the `Shapely documentation <https://pypi.python.org/pypi/Shapely>`_.

See :download:`geometry.py <examples/geometry/geometry.py>` and :download:`geometry.map <examples/geometry/geometry.map>`. 

.. image:: images/shapely.jpg

.. code-block:: python

    mapfile["size"] = [600, 600]

Dilated
+++++++

.. literalinclude:: examples/geometry/geometry.py
   :pyobject: dilation

.. image:: images/dilated.png
    :scale: 80%

Eroded
++++++

.. literalinclude:: examples/geometry/geometry.py
   :pyobject: erosion

.. image:: images/erosion.png
    :scale: 80%

Shadows and Shading
-------------------

.. raw:: html

    <style>
      .map:-moz-full-screen {
        height: 100%;
      }
      .map:-webkit-full-screen {
        height: 100%;
      }
      .map:-ms-fullscreen {
        height: 100%;
      }
      .map:fullscreen {
        height: 100%;
      }
      .ol-rotate {
        top: 3em;
      }
      .map {
        width: 100%; 
        height: 300px;
      }
    </style>

    <div id='map' class='map'></div>
    <script>
        MapWidget();
    </script>


Animated Buffers
----------------

.. image:: images/animation.gif

See :download:`animated_buffer.py <examples/animation/animated_buffer.py>` and :download:`animated_buffer.map <examples/animation/animated_buffer.map>`. 

..
    Colormaps http://matplotlib.org/cmocean/
    https://pypi.python.org/pypi/colour