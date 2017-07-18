var MapWidget = (function (options) {

    var me = {};
    options = options ? options : {};

    var center = options.center ? options.center : [2.58738, 48.84092];
    var msURL = options.msURL ? options.msURL : 'http://46.101.91.225/cgi-bin/mapserv?MAP=/srv/foss4ge/mapfile.map&'; // http://localhost/mapserver/?map=C:/MapServer/apps/foss4ge/mapfile.map&
    var zoom = options.zoom ? options.zoom : 16;
    var DIVNAME = options.divName ? options.divName : 'map';

    var layers = [
        new ol.layer.Image({
            source: new ol.source.ImageWMS({
                url: msURL,
                params: { 'LAYERS': 'pointer,lines,multipolygons', 'transparent': false, 'TILED': false }
            })
        })
    ];

    var map = new ol.Map({
        controls: ol.control.defaults().extend([
            new ol.control.FullScreen()
        ]),
        layers: layers,
        target: 'map',
        view: new ol.View({
            center: ol.proj.transform(center, 'EPSG:4326', 'EPSG:3857'),
            zoom: zoom
        })
    });

    return me;
});