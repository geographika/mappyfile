import os
from subprocess import Popen, PIPE
import mappyfile

DLL_LOCATION = r"C:\MapServer\bin"


def create_image(name, mapfile, output_folder, format="png"):
    out_map = os.path.join(output_folder, "%s.map" % name)
    mappyfile.save(mapfile, out_map)

    out_img = os.path.join(output_folder, name)

    return _create_image_from_map(out_map, out_img, format=format)


def _create_image_from_map(map_file, out_img, format):
    out_img += ".%s" % format
    # print out_img
    params = ["shp2img", "-m", map_file, "-i", format, "-o", out_img]

    os.environ["PATH"] = DLL_LOCATION + ";" + os.environ["PATH"]

    p = Popen(params, stdout=PIPE, bufsize=1)
    with p.stdout:
        for line in iter(p.stdout.readline, b""):
            print(line)

    p.wait()  # wait for the subprocess to exit

    # os.startfile(out_img)
    return out_img
