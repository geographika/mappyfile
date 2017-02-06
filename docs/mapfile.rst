Mapfile Notes
=============

* Quoted strings. Used for quoted property values e.g.

  .. code-block:: mapfile

     NAME "Layer1"
     DATA "lakes.shp"

* Non-quoted lists. E.g. a POINTS block can be defined as follows:

  .. code-block:: mapfile
  
      POINTS
          0 100
          100 200
          40 90
      END

* Quoted lists. Used for property lists that should be quoted. E.g. the PROJECTION block can be defined as follows:

  .. code-block:: mapfile
  
      PROJECTION
          'proj=utm'
          'ellps=GRS80'
          'datum=NAD83'
          'zone=15'
          'units=m'
          'north'
          'no_defs'
      END

* Key-value lists. 

  .. code-block:: mapfile
  
      PROCESSING "BANDS=1"
      PROCESSING "CONTOUR_ITEM=elevation"
      PROCESSING "CONTOUR_INTERVAL=20"

* Key-double-value lists. As above but there are two strings for each directive. 

  .. code-block:: mapfile
  
        CONFIG MS_ERRORFILE "stderr"
        CONFIG "PROJ_DEBUG" "OFF"
        CONFIG "ON_MISSING_DATA" "IGNORE"

* Composite types- container declarations which finish with the
  keyword END. Examples:
    
  .. code-block:: mapfile

     MAP ... END
     LAYER ... END
     CLASS ... END
     STYLE ... END


Mappyfile Additions
-------------------

Hidden containers - these containers are not outputted as part of the pprint. They are used to store objects of the same type 
e.g. LAYERs, CLASSes, STYLEs
