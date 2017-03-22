

mymap["metadata"]["ows_title"] = "Pavement Management System: %s" % title
#mymap.setMetaData("ows_title", "Pavement Management System: %s" % title)


    # the next line throws an error unless it is set to a file/location that exists
    try:
        mymap.setConfigOption("MS_ERRORFILE", error_log)



mymap["debug"] = debug_level
mymap.debug = debug_level # set debug level   


    if l["connectiontype"] == "PLUGIN":
        l["connection"] = connection
    else:
        raise Exception("Unsupported connection type!")

    #if l.connectiontype == mapscript.MS_PLUGIN:
    #    l.connection = connection
    #elif l.connectiontype == mapscript.MS_OGR:
    #    l.connection = "MSSQL:" + connection



    if "LOCALAUTHORITYID" in l["validation"].keys():
        l["validation"]["LOCALAUTHORITYID"] = filter

    #if l.validation.get('LOCALAUTHORITYID'):
    #    l.validation.set('LOCALAUTHORITYID', filter)


    for idx in reversed(range(0, layer.numclasses)):
        layer.removeClass(idx)

    for c in classes:
        clsObj = mapscript.fromstring(c)
        layer.classes.append(clsObj)

   layer["classes"] = [mappyfile.loads(ea) for ea in eas]
