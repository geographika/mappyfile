"""
C:\VirtualEnvs\mappyfile\Scripts\activate
SET PATH=C:\MapServer\bin;%PATH%
SET PROJ_LIB=C:\MapServer\bin\proj\SHARE
"""
import mapscript
s = u"""
MAP
    LAYER
        TYPE POINT
        CLUSTER
            MAXDISTANCE 50
            REGION ELLIPSE
        END
    END
END
"""

map = mapscript.fromstring(s)

print(map.convertToString())