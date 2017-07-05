import os, sys
from shapely.geometry import LineString
import mappyfile
from PIL import Image

sys.path.append(os.path.abspath("./docs/examples"))
from helper import create_image

def create_frame(mapfile, line, dist):

    pl = mappyfile.find(mapfile["layers"], "name", "polygon")
    dilated = line.buffer(dist, cap_style=3)
    pl["features"][0]["wkt"] = "'%s'" % dilated.wkt
    return create_image("animation_%s" % str(dist), mapfile, format="gif")

def create_frames(mapfile):

    min_buffer = 1
    max_buffer = 35
    step = 3

    line = LineString([(0, 0), (100, 100), (0, 200), (200, 200), (300, 100), (100, 0)])
    mapfile["extent"] = " ".join(map(str, line.buffer(max_buffer*2).bounds))

    all_images = []

    for dist in range(min_buffer, max_buffer, step):
        all_images.append(create_frame(mapfile, line, dist))

    for dist in range(max_buffer, min_buffer, -step):
        all_images.append(create_frame(mapfile, line, dist))

    return all_images

def create_animation(img_files):
    """
    http://pillow.readthedocs.io/en/4.2.x/handbook/image-file-formats.html?highlight=append_images#saving
    """

    open_images = []

    for fn in img_files:
        print fn
        im = Image.open(fn)
        open_images.append(im)

    im = open_images[0]
    im.save(r"C:\temp\animation.gif", save_all=True, append_images=open_images[1:], duration=120, loop=100, optimize=True)


bn = "animated_buffer.map"
mf = "./docs/examples/%s" % bn

mapfile = mappyfile.load(mf)
img_files = create_frames(mapfile)
create_animation(img_files)

print("Done!")