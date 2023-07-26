import os
import sys
from shapely.geometry import LineString
import mappyfile

try:
    from PIL import Image
except ImportError:
    raise

from helper import create_image


sys.path.append(os.path.abspath("./docs/examples"))


def create_frame(mapfile, line, dist):
    # get the polygon layer
    pl = mappyfile.find(mapfile["layers"], "name", "polygon")
    # buffer the line
    dilated = line.buffer(dist, cap_style=3)
    # now set the FEATURES in the Mapfile to be the WKT from Shapely
    pl["features"][0]["wkt"] = "'%s'" % dilated.wkt
    # create an image from this Mapfile
    return create_image("animation_%s" % str(dist), mapfile, format="gif")


def create_frames(mapfile):
    # increment in steps of 3 units from 1 to 35
    min_buffer = 1
    max_buffer = 35
    step = 3

    # create a line
    line = LineString([(0, 0), (100, 100), (0, 200), (200, 200), (300, 100), (100, 0)])
    # set the map extent to this line
    mapfile["extent"] = " ".join(map(str, line.buffer(max_buffer * 2).bounds))

    all_images = []

    # create expanding buffers
    for dist in range(min_buffer, max_buffer, step):
        all_images.append(create_frame(mapfile, line, dist))

    # create shrinking buffers
    for dist in range(max_buffer, min_buffer, -step):
        all_images.append(create_frame(mapfile, line, dist))

    return all_images


def create_animation(img_files):
    """
    See http://pillow.readthedocs.io/en/4.2.x/handbook/image-file-formats.html?highlight=append_images#saving
    """

    open_images = []

    for fn in img_files:
        print(fn)
        im = Image.open(fn)
        open_images.append(im)

    im = open_images[0]
    im.save(
        r"C:\temp\animation.gif",
        save_all=True,
        append_images=open_images[1:],
        duration=120,
        loop=100,
        optimize=True,
    )


def main():
    mf = "./docs/examples/animation/animated_buffer.map"
    mapfile = mappyfile.load(mf)
    img_files = create_frames(mapfile)
    create_animation(img_files)


if __name__ == "__main__":
    main()
    print("Done!")
