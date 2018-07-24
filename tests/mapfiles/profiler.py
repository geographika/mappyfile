import sys
import cProfile
import pstats
import glob
import os
import mappyfile


def parse(mf):
    m = mappyfile.open(mf, expand_includes=False)
    s = mappyfile.dumps(m)
    return s


def profile(mf, test_name):
    sortby = 'time'

    pr = cProfile.Profile()
    pr.enable()
    parse(mf)
    pr.disable()

    fn = os.path.join(os.path.dirname(__file__), "performance", test_name, "{}.txt".format(os.path.basename(mf)))

    with open(fn, "w") as f:
        ps = pstats.Stats(pr, stream=f).sort_stats(sortby)
        ps.print_stats()
    # pr.dump_stats(fn)
    # pr.print_stats(sort='time')


def run(test_name):

    sample_dir = os.path.dirname(__file__)
    pth = sample_dir + '/*.map'
    mapfiles = glob.glob(pth)

    for fn in mapfiles:
        print(fn)
        profile(fn, test_name)


if __name__ == "__main__":
    test_name = "run3-py27"
    run(test_name)
    print("Done!")
