import pytest
from mappyfile.pprint import PrettyPrinter
from tests.point_vector import create_map
import os, logging
import subprocess
import tempfile, shutil
import codecs

from mappyfile.types import Container, MAPFILE_TYPE

from subprocess import call
#call(["ls", "-l"])


def setup():

    tempdir = tempfile.gettempdir()
    shutil.copy("./tests/symbolset", tempdir)
    src = r"C:\MapServerBuild\mapserver\msautotest\misc\data"
    dest = os.path.join(tempdir, "data")

    try:
        shutil.copytree(src, dest)
    except Exception as ex:
        logging.error(ex)

    return tempdir
    
def write_map_to_file(map_string, output_file):

    with codecs.open(output_file, "w", encoding="utf-8") as f:
        f.write(map_string)

    return output_file

def create_image_from_map(map_file):

    #f = tempfile.NamedTemporaryFile(dir=output_folder, delete=False, suffix=".map", prefix="tmp_")


    #f.close()

    of = tempfile.NamedTemporaryFile(delete=False, suffix=".png", prefix="tmp_")
    of.close()

    logging.debug("Creating file %s", of.name)

    params = ["shp2img","-m", map_file,"-i","png","-o", of.name]

    dll_location = r"C:\MapServer\bin"
    os.environ['PATH'] = dll_location + ';' + os.environ['PATH']
    os.environ['PROJ_LIB'] = os.path.join(dll_location, "proj\SHARE")

    logging.debug(" ".join(params))

    # [SHP2IMG] -m [MAPFILE] -i png -o [RESULT]

    #call(params)
    p = subprocess.Popen(params)
    logging.info(p.stdout)

    #if p.returncode == 0:
    #os.startfile(of.name)