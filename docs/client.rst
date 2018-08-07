Command-line Interface
======================


On the development roadmap are plans to allow validation against different versions of MapServer, for example validating Mapfiles for MapServer 7.0, 
or for 7.2. It is unlikely versions before version 7.0 will be considered. 

A command line interface (CLI), allows mappyfile to be easily integrated into Continuous Integration (CI) platforms such as Travis and Appveyor. 


Search subfolders: mappyfile validate ``D:\Installation\ms-ogc-workshop\ms4w\apps\ms-ogc-workshop\**\*.map``

Glob module in Python only goes one level-deep. On Linux wildcards are typically expanded in the shell. 


mappyfile validate --help

