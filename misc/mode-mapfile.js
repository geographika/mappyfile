
define('ace/mode/mapfile', function (require, exports, module) {
    "use strict";

    var oop = require("../lib/oop");
    var TextMode = require("./text").Mode;
    var BaseFoldMode = require("./folding/fold_mode").FoldMode;

    var TextHighlightRules = require("./text_highlight_rules").TextHighlightRules;

    var MapfileHighlightRules = function () {

        var keywords = (
            'tilesrs|text|minsize|compfilter|intervals|font|imagetype|outlinecolor|overlayoutlinecolor|web|style|imagepath|group|title|filteritem|mingeowidth|character|labelminscale|labelcache|scaledenom|bandsitem|to|outlinewidth|include|image|backgroundcolor|mininterval|scalebar|maxtemplate|browseformat|relativeto|grid|bindvals|labelmaxscale|transparent|name|labelrequires|maxscaledenom|temppath|debug|maxsubdivide|maxdistance|align|tileitem|force|dump|map|maxscale|marker|repeatdistance|minscaledenom|latlon|index|scale|utfitem|maxwidth|mintemplate|label|partials|minsubdivide|template|pattern|labelformat|tolerance|leader|filled|metadata|classitem|graticule|processing|linejoinmaxsize|shadowcolor|extent|offset|linejoin|overlaymaxsize|legend|maxarcs|log|extension|items|region|interlace|datapattern|overlaybackgroundcolor|filter|connection|keysize|maxlength|expression|opacity|projection|labelitem|encoding|color|defresolution|connectiontype|minwidth|header|wrap|table|imageurl|size|utfdata|overlaysize|from|reference|linecap|transform|compop|priority|width|maxsize|classgroup|mindistance|geomtransform|type|empty|maxgeowidth|keyimage|composite|symbolscaledenom|gridstep|labelminscaledenom|symbolscale|maxinterval|symbolset|minfeaturesize|initialgap|join|imagequality|cluster|tileindex|imagecolor|styleitem|values|transparency|error|templatepattern|toleranceunits|layer|maxfeatures|queryformat|offsite|sizeunits|imagemode|anchorpoint|wkt|postlabelcache|end|minlength|feature|querymap|units|overlayminsize|maxoverlapangle|config|fontset|status|minarcs|outputformat|markersize|legendformat|overlaycolor|buffer|symbol|shapepath|driver|antialias|maxboxsize|angle|minscale|gap|data|class|minboxsize|mimetype|overlaysymbol|shadowsize|footer|requires|mask|points|labelmaxscaledenom|formatoption|scaletoken|position|validation|resolution|keyspacing'
        );

        var builtinConstants = (
            'bitmap|auto2|generalize|qstring|mysql|follow|pixmap|touches|difference|fromtext|wms|miter|cl|ows_srs|simple|lr|circle|overlaps|triangle|auto|dd|one-to-many|tostring|false|hilite|one-to-one|postgis|large|truetype|miles|small|commify|round|upper|smoothsia|right|meters|query|beyond|contour|ows_enable_request|selected|vector|javascript|giant|equals|initcap|base|kilometers|pixels|lc|on|postgresql|plugin|length|ll|dwithin|default_base|point|cc|within|feet|square|cr|ellipse|area|union|contains|tiny|ows_onlineresource|medium|inches|raster|ogr|ms_errorfile|butt|kerneldensity|line|rangeitem|true|colorrange|bevel|none|crosses|datarange|default|nauticalmiles|ur|ul|wfs|embed|uc|intersects|polaroffset|simplifypt|single|disjoint|uvraster|polygon|hatch|csv|multiple|normal|buffer|chart|simplify|annotation|lower|off|center|percentages|svg|firstcap|oraclespatial|left'
        );

        var builtinFunctions = (
            "tostring"
        );

        var dataTypes = (
            "float"
            //"int|numeric|decimal|date|varchar|char|bigint|float|double|bit|binary|text|set|timestamp|" +
            //"money|real|number|integer"
        );

        var keywordMapper = this.createKeywordMapper({
            "support.function": builtinFunctions,
            "keyword": keywords,
            "constant.language": builtinConstants,
            "storage.type": dataTypes
        }, "identifier", true);

        this.$rules = {
            "start": [{
                token: "comment",
                regex: "#.*$"
            }, {
                token: "comment",
                start: "/\\*",
                end: "\\*/"
            }, {
                token: "string",           // " string
                regex: '".*?"'
            }, {
                token: "string",           // ' string
                regex: "'.*?'"
            }, {
                token: "constant.numeric", // float
                regex: "[+-]?\\d+(?:(?:\\.\\d*)?(?:[eE][+-]?\\d+)?)?\\b"
            }, {
                token: keywordMapper,
                regex: "[a-zA-Z_$][a-zA-Z0-9_$]*\\b"
            }, {
                token: "keyword.operator",
                regex: "\\+|\\-|\\/|\\/\\/|%|<@>|@>|<@|&|\\^|~|<|>|<=|=>|==|!=|<>|="
            }, {
                token: "paren.lparen",
                regex: "[\\(]"
            }, {
                token: "paren.rparen",
                regex: "[\\)]"
            }, {
                token: "text",
                regex: "\\s+"
            }]
        };
        this.normalizeRules();
    };

    oop.inherits(MapfileHighlightRules, TextHighlightRules);

    // folding



    var FoldMode = exports.FoldMode = function (markers) {
        this.foldingStartMarker = new RegExp("([\\[{])(?:\\s*)$|(" + markers + ")(?:\\s*)(?:#.*)?$");
    };
    oop.inherits(FoldMode, BaseFoldMode);

    (function () {

        this.getFoldWidgetRange = function (session, foldStyle, row) {
            var line = session.getLine(row);
            var match = line.match(this.foldingStartMarker);
            if (match) {
                if (match[1])
                    return this.openingBracketBlock(session, match[1], row, match.index);
                if (match[2])
                    return this.indentationBlock(session, row, match.index + match[2].length);
                return this.indentationBlock(session, row);
            }
        }

    }).call(FoldMode.prototype);

    var Mode = function () {
        this.HighlightRules = MapfileHighlightRules;
        //this.foldingRules = new FoldMode();
        this.$behaviour = this.$defaultBehaviour;
    };
    oop.inherits(Mode, TextMode);

    (function () {

        this.lineCommentStart = "#";

        this.$id = "ace/mode/mapfile";
    }).call(Mode.prototype);

    exports.Mode = Mode;

});