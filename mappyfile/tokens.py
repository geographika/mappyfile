# =================================================================
#
# Authors: Erez Shinan, Seth Girvin
#
# Copyright (c) 2020 Seth Girvin
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

# Types, that require an "END"
COMPLEX_TYPES = frozenset("""
    symbolset
    projection
    points
    pattern
    values
    metadata
    validation
    connectionoptions
    class
    cluster
    composite
    feature
    grid
    join
    label
    leader
    legend
    map
    outputformat
    querymap
    reference
    scalebar
    scaletoken
    style
    web
    layer
    symbol
    """.split())

COMPOSITE_NAMES = frozenset("""
    align
    anchorpoint
    angle
    antialias
    backgroundcolor
    bandsitem
    bindvals
    browseformat
    buffer
    character
    class
    classitem
    classgroup
    color
    compfilter
    composite
    compop
    config
    connection
    connectiontype
    data
    datapattern
    debug
    driver
    dump
    empty
    encoding
    end
    error
    expression
    extent
    extension
    feature
    filled
    filter
    filteritem
    footer
    font
    fontset
    force
    formatoption
    from
    gap
    geomtransform
    grid
    gridstep
    graticule
    group
    header
    image
    imagecolor
    imagetype
    imagequality
    imagemode
    imagepath
    temppath
    imageurl
    include
    index
    initialgap
    interlace
    intervals
    join
    keyimage
    keysize
    keyspacing
    label
    labelcache
    labelformat
    labelitem
    labelmaxscale
    labelmaxscaledenom
    labelminscale
    labelminscaledenom
    labelrequires
    latlon
    layer
    leader
    legendformat
    linecap
    linejoin
    linejoinmaxsize
    log
    map
    marker
    markersize
    mask
    maxarcs
    maxboxsize
    maxdistance
    maxfeatures
    maxinterval
    maxscale
    maxscaledenom
    maxgeowidth
    maxlength
    maxsize
    maxsubdivide
    maxtemplate
    maxwidth

    mimetype
    minarcs
    minboxsize
    mindistance
    repeatdistance
    maxoverlapangle
    minfeaturesize
    mininterval
    minscale
    minscaledenom
    mingeowidth
    minlength
    minsize
    minsubdivide
    mintemplate
    minwidth
    name
    offset
    offsite
    opacity
    outlinecolor
    outlinewidth
    outputformat
    overlaybackgroundcolor
    overlaycolor
    overlaymaxsize
    overlayminsize
    overlayoutlinecolor
    overlaysize
    overlaysymbol
    partials
    pattern
    points
    items
    position
    postlabelcache
    priority
    processing
    projection
    queryformat
    reference
    region
    relativeto
    requires
    resolution
    defresolution
    scale
    scaledenom
    scaletoken
    shadowcolor
    shadowsize
    shapepath
    size
    sizeunits
    status
    style
    styleitem
    symbol
    symbolscale
    symbolscaledenom
    symbolset
    table
    template
    templatepattern
    text
    tileindex
    tileitem
    tilesrs
    title
    to
    tolerance
    toleranceunits
    transparency
    transparent
    transform
    type
    units
    utfdata
    utfitem



    width
    wkt
    wrap
""".split())

SINGLETON_COMPOSITE_NAMES = frozenset("""
    cluster
    connectionoptions
    grid
    leader
    legend
    metadata
    pattern
    projection
    querymap
    reference
    scalebar
    validation
    values
    web
""".split())

ATTRIBUTE_NAMES = frozenset("""
area
length
tostring
commify
round
upper
lower
initcap
firstcap

buffer
difference
simplify
simplifypt
generalize
smoothsia
javascript

intersects
disjoint
touches
overlaps
crosses
within
contains
equals
beyond
dwithin

fromtext

true
false

colorrange
datarange
rangeitem


annotation
auto
auto2
bevel
bitmap
butt
cc
center
chart
circle
cl
cr
csv
postgresql
mysql
default
dd
ellipse
embed
false
feet
follow
giant
hatch
kerneldensity
hilite
inches
kilometers
large
lc
left
line
ll
lr
medium
meters
nauticalmiles
miles
miter
multiple
none
normal
off
ogr
on
one-to-one
one-to-many
oraclespatial
percentages
pixmap
pixels
point
polygon
postgis
plugin
query
raster
right
round
selected
simple
single
small
square
svg
polaroffset
tiny
triangle
true
truetype
uc
ul
ur
union
uvraster
contour
vector
wfs
wms

qstring
base
default_base
ows_onlineresource
ows_srs
ows_enable_request
ms_errorfile
""".split()) | COMPOSITE_NAMES

# some keywords can be added multiple times to a composite type
REPEATED_KEYS = ('processing', 'formatoption', 'include', 'data', 'compfilter')

# these are keywords used in the schema to store collections of composite objects
# for example lists of layers
OBJECT_LIST_KEYS = frozenset("""
layers
classes
styles
symbols
labels
outputformats
features
scaletokens
composites
joins
""".split())
