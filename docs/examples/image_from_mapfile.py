import subprocess
from subprocess import Popen, PIPE
import tempfile
import logging
import sys
import os


def open_file(path: str):
    if sys.platform == "win32":
        os.startfile(path)  # subprocess not needed here
    elif sys.platform == "darwin":
        subprocess.run(["open", path], check=True)
    else:
        subprocess.run(["xdg-open", path], check=True)


def create_image_from_map(map_file, dll_location):
    of = tempfile.NamedTemporaryFile(delete=False, suffix=".png", prefix="tmp_")
    of.close()

    logging.debug("Creating file %s", of.name)
    # [SHP2IMG] -m [MAPFILE] -i png -o [RESULT]
    params = ["shp2img", "-m", map_file, "-i", "png", "-o", of.name]

    os.environ["PATH"] = dll_location + ";" + os.environ["PATH"]
    os.environ["PROJ_LIB"] = os.path.join(dll_location, r"proj\SHARE")

    logging.debug(" ".join(params))

    p = Popen(params, stdout=PIPE, bufsize=1)
    assert p.stdout is not None

    with p.stdout:
        print(map_file)
        for line in iter(p.stdout.readline, b""):
            print(line)

    p.wait()  # wait for the subprocess to exit

    open_file(of.name)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    mf = r"D:\GitHub\mapserver\msautotest\gdal\256_overlay_res.map"
    dll_location = r"C:\MapServer\bin"
    create_image_from_map(mf, dll_location)  # fn for original map
    print("Done!")
